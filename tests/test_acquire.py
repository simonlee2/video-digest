import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / 'plugins/video-digest/skills/video-digest/stages/video-digest-ingest/scripts/vd_acquire.py'
spec = importlib.util.spec_from_file_location('acquire', SCRIPT)
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)


class AcquireTests(unittest.TestCase):
    def test_audio_only_and_error_html_are_rejected(self):
        with patch.object(a.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, json.dumps({'streams':[{'codec_type':'audio'}],'format':{'duration':'10'}}))):
            with self.assertRaisesRegex(ValueError, 'video, audio'):
                a.validate(Path('audio.mp4'))
        with patch.object(a.subprocess, 'run', side_effect=subprocess.CalledProcessError(1, 'ffprobe', stderr='Invalid data')):
            with self.assertRaises(subprocess.CalledProcessError):
                a.validate(Path('error.html'))

    def test_failed_decode_is_not_accepted(self):
        result = subprocess.CompletedProcess([], 0, json.dumps({'streams':[{'codec_type':'audio'},{'codec_type':'video'}],'format':{'duration':'10'}}))
        with patch.object(a.subprocess, 'run', side_effect=[result, subprocess.CalledProcessError(1, 'ffmpeg')]):
            with self.assertRaises(subprocess.CalledProcessError):
                a.validate(Path('broken.mp4'))

    def test_defaults_accept_actual_download_container(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d).resolve(); media=root/'video.webm';media.write_bytes(b'fixture')
            # No cache exists when acquisition begins; yt-dlp reports its completed path.
            with patch.object(Path,'glob',return_value=[]), patch.object(a.subprocess,'run',return_value=subprocess.CompletedProcess([],0,str(media)+'\n')) as run, patch.object(a,'validate',return_value={'validated':True}):
                a.acquire(root,'https://example.com/video')
            command=run.call_args.args[0]
            self.assertEqual(command[0],'yt-dlp')
            self.assertNotIn('--extractor-args',command)
            self.assertNotIn('-f',command)
            self.assertEqual((root/'source.mp4').resolve(),media)

    def test_cached_media_is_revalidated_without_redownload(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d).resolve();media=root/'video.mkv';media.write_bytes(b'fixture')
            with patch.object(a,'validate',side_effect=ValueError('invalid cache')) as validate, patch.object(a.subprocess,'run') as run:
                with self.assertRaisesRegex(ValueError,'invalid cache'):
                    a.acquire(root,'https://example.com/video')
                validate.assert_called_once_with(media)
                run.assert_not_called()
