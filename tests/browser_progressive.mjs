// Optional real-browser regression: existing Chromium + Node 22, no package install.
import {spawn} from 'node:child_process';
import {readFile, writeFile, mkdir, mkdtemp, rm, readdir} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {resolve, join} from 'node:path';
import {pathToFileURL} from 'node:url';
import assert from 'node:assert/strict';
const project=resolve(process.argv[2]);
const profile=await mkdtemp(join(tmpdir(),'video-digest-browser-'));
const artifacts=process.env.VIDEO_DIGEST_BROWSER_ARTIFACTS;
if(artifacts)await mkdir(artifacts,{recursive:true});
const browser=spawn(process.env.VIDEO_DIGEST_CHROME,['--headless','--remote-debugging-port=0',
 '--user-data-dir='+profile,'--no-first-run','--no-default-browser-check',
 '--disable-background-networking','--disable-component-update','--disable-sync','about:blank'],
 {stdio:['ignore','ignore','pipe']});
let stderr='',launchError;browser.stderr.on('data',x=>stderr+=x);browser.on('error',e=>launchError=e);
const pause=ms=>new Promise(r=>setTimeout(r,ms));
let ws,next=0;const pending=new Map(),exceptions=[],networkFailures=[];
async function send(method,params={}){return new Promise((resolve,reject)=>{
 const id=++next;const timer=setTimeout(()=>{pending.delete(id);reject(Error('Timeout '+method));},10000);
 pending.set(id,{resolve,reject,timer});ws.send(JSON.stringify({id,method,params}));
});}
async function evaluate(expression){const r=await send('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});
 if(r.exceptionDetails)throw Error(JSON.stringify(r.exceptionDetails));return r.result.value;}
async function until(expression){for(let i=0;i<50;i++){if(await evaluate(expression))return;await pause(100);}throw Error('Not ready: '+expression);}
async function click(selector){await evaluate(`document.querySelector(${JSON.stringify(selector)}).scrollIntoView({block:'center',behavior:'instant'})`);
 const p=await evaluate(`(()=>{const r=document.querySelector(${JSON.stringify(selector)}).getBoundingClientRect();return {x:r.x+r.width/2,y:r.y+r.height/2}})()`);
 await send('Input.dispatchMouseEvent',{type:'mousePressed',button:'left',clickCount:1,...p});
 await send('Input.dispatchMouseEvent',{type:'mouseReleased',button:'left',clickCount:1,...p});await pause(400);}
async function screenshot(name){if(!artifacts)return;const r=await send('Page.captureScreenshot',{format:'png'});await writeFile(join(artifacts,name+'.png'),Buffer.from(r.data,'base64'));}
async function collect(dir){let texts=[];for(const entry of await readdir(dir,{withFileTypes:true})){
 const path=join(dir,entry.name);if(entry.isDirectory())texts.push(...await collect(path));
 else if(entry.name==='highlights.json')for(const talk of Object.values(JSON.parse(await readFile(path,'utf8'))))
 for(const h of talk.highlights)texts.push(h.text,h.editorial_heading,...(h.editorial_notes||[]));
}return texts.filter(Boolean);}
const expected=await collect(join(project,'groups'));
const report={cases:[],scope:'Existing isolated Chromium, not physical iOS/Safari preview'};
try{
 let port;for(let i=0;i<100;i++){if(launchError)throw launchError;try{port=Number((await readFile(join(profile,'DevToolsActivePort'),'utf8')).split('\n')[0]);break;}catch{}await pause(100);}
 assert(port,'Chromium did not start: '+stderr.slice(-1000));
 const pages=await(await fetch(`http://127.0.0.1:${port}/json/list`)).json();
 ws=new WebSocket(pages.find(p=>p.type==='page').webSocketDebuggerUrl);
 await new Promise((r,j)=>{ws.onopen=r;ws.onerror=j});
 ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id){const p=pending.get(m.id);if(!p)return;clearTimeout(p.timer);pending.delete(m.id);m.error?p.reject(Error(JSON.stringify(m.error))):p.resolve(m.result);}
 else if(m.method==='Runtime.exceptionThrown')exceptions.push(m.params);else if(m.method==='Network.loadingFailed')networkFailures.push(m.params);};
 await send('Page.enable');await send('Runtime.enable');await send('Network.enable');
 for(const enabled of [false,true])for(const format of ['digest.html','dist/index.html'])for(const width of [1280,390,320]){
  const label=(enabled?'js':'no-js')+'-'+(format==='digest.html'?'single':'folder')+'-'+width;
  await send('Emulation.setScriptExecutionDisabled',{value:!enabled});
  await send('Emulation.setDeviceMetricsOverride',{width,height:900,deviceScaleFactor:1,mobile:false});
  await send('Page.navigate',{url:pathToFileURL(join(project,format)).href});
  await until("document.readyState==='complete'");
  assert.equal(await evaluate("document.documentElement.classList.contains('enhanced')"),enabled,label);
  const native=await evaluate(`(()=>{const visible=e=>getComputedStyle(e).display!=='none'&&e.getClientRects().length>0;return {overview:visible(document.querySelector('.ovgrid')),article:visible(document.querySelector('.session')),essay:visible(document.querySelector('.essaywrap')),missingTargets:[...document.querySelectorAll('a[href^="#"]')].filter(a=>!document.getElementById(a.hash.slice(1))).map(a=>a.hash)}})()`);
  assert(native.overview,label);assert.equal(native.article,!enabled,label);assert.equal(native.essay,!enabled,label);assert.deepEqual(native.missingTargets,[],label);
  await click('.card');
  if(enabled){await until("document.body.dataset.view==='detail'");await until("window.scrollY<2");}
  else await until("document.querySelector('.session').getBoundingClientRect().top>=0 && document.querySelector('.session').getBoundingClientRect().top<300");
  const detail=await evaluate("({text:document.querySelector('.session').innerText,visible:document.querySelector('.session').getClientRects().length>0,width:document.documentElement.scrollWidth})");
  assert(detail.visible,label);assert(detail.width<=width+1,label+' overflow');
  for(const t of expected)assert(detail.text.includes(t),label+' missing editorial: '+t);
  await screenshot(label+'-article');
  const count=await evaluate("document.querySelectorAll('figure.slide img').length");assert.equal(count,2,label);
  for(let i=0;i<count;i++){
   await evaluate(`document.querySelectorAll('figure.slide img')[${i}].scrollIntoView({block:'center',behavior:'instant'})`);
   await until(`document.querySelectorAll('figure.slide img')[${i}].complete && document.querySelectorAll('figure.slide img')[${i}].naturalWidth>0`);
   assert(await evaluate(`(()=>{const r=document.querySelectorAll('figure.slide img')[${i}].getBoundingClientRect();return r.width>0&&r.left>=-1&&r.right<=innerWidth+1})()`),label+' clipped frame');
  }
  await click('.session .back');
  if(enabled){await until("document.body.dataset.view==='overview'");await evaluate('history.back()');await until("document.body.dataset.view==='detail'");await send('Page.reload');await until("document.readyState==='complete' && document.body.dataset.view==='detail'");}
  else assert.equal(await evaluate('location.hash'),'#demo',label+' native overview');
  await click('.essaytab');
  if(enabled){await until("document.body.dataset.view==='essay'");await until("window.scrollY<2");}
  else await until("document.querySelector('#essay').getBoundingClientRect().top>=0 && document.querySelector('#essay').getBoundingClientRect().top<300");
  const essay=await evaluate("({text:document.querySelector('#essay').innerText,visible:document.querySelector('#essay').getClientRects().length>0,width:document.documentElement.scrollWidth})");
  assert(essay.visible&&essay.text.includes('Final discussion conclusion.'),label);assert(essay.width<=width+1,label+' essay overflow');
  await screenshot(label+'-discussion');
  report.cases.push({enabled,format,width,allEditorialVisible:true,frames:count,navigation:true,discussion:true,noOverflow:true});
 }
 assert.deepEqual(exceptions,[]);assert.deepEqual(networkFailures,[]);report.status='passed';
 console.log(JSON.stringify({status:report.status,cases:report.cases.length}));
}catch(e){report.status='failed';report.error=e.stack;process.exitCode=1;console.error(e);}
finally{
 report.exceptions=exceptions;report.networkFailures=networkFailures;
 if(artifacts)await writeFile(join(artifacts,'report.json'),JSON.stringify(report,null,2));
 if(ws){try{await send('Browser.close');}catch{}ws.close();}
 browser.kill('SIGTERM');for(const p of pending.values())clearTimeout(p.timer);
 await rm(profile,{recursive:true,force:true});
}
process.exit(process.exitCode||0);
