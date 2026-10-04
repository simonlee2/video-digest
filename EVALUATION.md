# Bounded editorial evaluation

This compares two independent Codex generations plus a bounded editorial revision for Dan Shipper’s [How to run your product team like a research lab](https://www.youtube.com/watch?v=DqF08Dz3nok), using an existing 18:31 recording and full cached automatic transcript. The earlier run used commit `1b83bdf`; the first follow-up tested broader frame search and lighter notes. It improved images but remained wordy. The final bundled guidance adds an explicit compression pass, tested as a revision of that follow-up draft.

## Observed results

| Measure | Previous evaluation | First follow-up draft | After explicit revision |
| --- | ---: | ---: | ---: |
| Chronological highlights | 12 | 14 | 10 |
| Substantive notes | 25 | 22 | 13 |
| Editorial words | 892 | 987 | 587 |
| Per-point applications | 7 | 0 | 0 |
| Selected source frames | 4 | 7 | 5 |
| Largest gap between selected frames | 638 seconds | 400 seconds | 400 seconds |

The final text is about 34% shorter than the previous evaluation and 41% shorter than the follow-up draft. These changes resulted from an explicit revision, not an automatically concise first pass. The revised overall takeaway remains labeled editorial application; removing repeated per-point applications did not remove practical guidance.

The previous digest jumped from an opening frame at 1:19 to the pipeline at 11:57. Broader passage sampling found the organizational structure and protected-assignment diagrams. Final selection retains the explanatory [lab-of-one slide at 5:25](https://www.youtube.com/watch?v=DqF08Dz3nok&t=325s), plus frames at 0:40, 12:05, 13:55 and 14:38. The intermediate speaker-view stretch remains text-only after broader sampling; this does not establish that every intervening frame lacks a slide. All seven first-draft images were inspected at native resolution and independently re-extracted byte-identically. The final five reuse those verified bytes and preserve actual frame links separately from highlight times.

### What the editing changed

- **Organizational model:** combined the exploration/delivery conflict with the protected lab assignment. The final block preserves early-adopter motivation, embedded or rotating staffing, disposal expectations and the product team's obligation to existing customers.
- **Operating practice:** combined parallel approaches with real-work feedback. It retains both the uncertain-frontier rationale and the fallback to early customers when employees are not the users.
- **Concrete example:** combined the editing bottleneck and voluntary adoption into one progression. Kept instrumentation as a separate lesson because it introduces different evidence and limitations.
- **Decision:** combined weekly pipeline review with promotion criteria. Repeat use, advantage over the baseline and serving cost survive, followed by the later integration conclusion.
- **Caveats:** the dashboard still distinguishes a 12-percentage-point change from a time-saving claim, notes estimated measurements and the declining acceptance metric, and treats external trials as prospective. General notes about unverified company history moved to the footer.

For example, the revised recommendation is one decision: before committing product capacity to a review assistant, require repeat use, measure remaining corrections alongside accepted suggestions, and estimate cost per completed draft. It is labeled editorial application, not something the speaker is quoted as prescribing verbatim.

### Checks and remaining uncertainty

All final approved highlights and notes are checked in the actual renderer, including text-only points and the final conclusion; both folder and standalone HTML are built. Frame bytes, timestamp links and installed-skill integrity are checked independently of the model's own report. The deterministic suite has 24 tests, including original fictional audit fixtures, actual renderer content retention, missing-image paths, and isolated installs. Python compilation, shell syntax and whitespace checks pass.

The audit finds no exact repeated blocks or missing numeric evidence ranges in either final comparison output. That did not diagnose the first draft's semantic repetition: human/model editorial judgment was still required. One team-composition note cites the later adoption example beyond its local evidence window; the later case block supplies that evidence. The metrics do not establish sentence-level provenance completeness. No unsupported material factual claim was found in the reviewed final editorial, but this remains source-grounded review of automatic transcription, not an external fact-check.

Final compression was exercised as a bounded revision with an explicit request to run that stage. A fresh unattended end-to-end run of the final guidance has not been repeated. Do not claim consistent first-pass concision or general improvement across talks from this result. Chromium browser acceptance now passes as described below; Claude inference remains unverified.

## Method and limits

Both runs used Codex CLI 0.156.1 with the same evaluation prompt, source media and transcript, in fresh project-local skill copies. Logs identify the same configured model, `gpt-6-astra`. Prior digest outputs were hidden from generation. The prompt explicitly requests source-grounded editorial, meaningful frames, evidence ranges and actual renderer output; this is not a minimal-prompt benchmark. The reviewer knows which version is which.

The existing ChatGPT-authenticated subscription was used with provider API-key environment variables removed. No new media/model download, install, account change or paid API was requested. Subscription inference is not fully on-device and this report does not independently establish its monetary cost. Claude inference remains pending safe authorized capacity.

Word counts include highlight text, editorial notes and labeled per-point applications; exclude headings, captions, summary and overall takeaway. They are descriptive, not a quality target. Shorter output only helps if it preserves the argument and necessary evidence. Selected-frame gaps identify passages worth inspecting, not mandatory spacing.

Full automatic transcripts and recordings remain outside the repository. Source fidelity was reviewed against the local transcript and actual frames; the full audio was not independently re-listened. Unresolved names and external-company anecdotes should not become asserted facts. A single same-talk repeat cannot isolate prompt effects from model variation or establish general reliability.

## Browser acceptance follow-up

The already-installed Chrome for Testing 153.0.8010.12 rendered both standalone and folder HTML from local files in an isolated headless profile. No installation, public deployment or Safari/security setting change was needed. Native Chromium DevTools Protocol exercised the page at 1280, 390 and 320 CSS pixels wide (900 high).

All six format/width combinations passed: the overview card opened the talk, the overview link returned, browser Back restored the detail, and a direct-link reload retained it. Every selected frame was scrolled into view and decoded successfully. All ten approved highlights and thirteen notes were visible in the rendered detail. There was no horizontal overflow, missing-image fallback, failed resource request or JavaScript exception. Screenshots of the overview, detail, lab diagram and final highlights were visually inspected. This particular digest has no expandable sections or bilingual toggle to exercise. External source URL/offset targets were checked; YouTube playback was not retested.

The browser review exposed one small renderer defect: singular counts displayed as “1 talks” (and “1 slides” in the fixture). The shared renderer now handles singular English labels; the existing one-talk/one-slide renderer test covers the fix. Both real digest formats were rebuilt and the six browser cases rerun successfully. The editorial content was unchanged.

This establishes headless Chromium layout and navigation at wide/narrow widths, not physical-device touch behavior or Safari compatibility. Dense slide fine print still needs a larger/source view; the adjacent editorial remains readable on narrow screens. The test harness initially measured before smooth scrolling settled; waiting for settled navigation and using immediate test scrolling resolved that harness timing issue, without changing the page’s scrolling behavior.

## Release boundary

Keep the PR as the review source. The smallest next decision is a Codex-first release with the Claude limitation explicit, or waiting for an authorized Claude pilot. Neither merging, tagging, release publication nor a public conference demo is implied by these tests. Safari WebDriver remains disabled, but already-installed Chromium supplied the local browser acceptance route without any global setting change.
