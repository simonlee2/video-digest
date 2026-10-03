#!/usr/bin/env python3
"""Repository wrapper for the self-contained skill's fictional example."""
import importlib.util
from pathlib import Path
import runpy
SOURCE = Path(__file__).resolve().parents[1] / 'plugins/video-digest/skills/video-digest/scripts/create_demo.py'
spec = importlib.util.spec_from_file_location('bundled_demo', SOURCE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
create = module.create
if __name__ == '__main__':
    runpy.run_path(str(SOURCE), run_name='__main__')
