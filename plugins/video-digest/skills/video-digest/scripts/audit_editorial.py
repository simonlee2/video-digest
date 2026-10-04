#!/usr/bin/env python3
"""Read-only editorial review metrics; no automatic quality score or quota."""
import argparse
import json
import re
from pathlib import Path


def words(text):
    return len(text.split())


def audit(item):
    item = Path(item)
    data = json.loads((item / 'highlights.json').read_text())
    report = {'purpose': 'Human review prompts, not a quality score', 'talks': {}}
    for stem, talk in data.items():
        selection_path = item / 'frames' / f'sel_{stem}.json'
        selection = json.loads(selection_path.read_text()) if selection_path.exists() else {}
        seen, duplicates, selected, missing, unillustrated = {}, [], [], [], []
        text_words = note_words = application_words = note_count = 0
        highlights = talk['highlights']
        for h in highlights:
            key = h['i']
            notes = h.get('editorial_notes', [])
            text_words += words(h.get('text', ''))
            note_words += sum(words(n) for n in notes)
            application_words += words(h.get('editorial_inference', ''))
            note_count += len(notes)
            blocks = [('text', h.get('text', ''))] + [('note', n) for n in notes]
            blocks += [('application', h.get('editorial_inference', ''))]
            for kind, text in blocks:
                normalized = ' '.join(re.findall(r'\w+', text.casefold()))
                if not normalized:
                    continue
                location = {'highlight': key, 'field': kind}
                if normalized in seen:
                    duplicates.append({'first': seen[normalized], 'repeat': location})
                else:
                    seen[normalized] = location
            start, end = h.get('evidence_start_seconds'), h.get('evidence_end_seconds')
            if notes and (not isinstance(start, (int, float)) or not isinstance(end, (int, float)) or not 0 <= start < end):
                missing.append(key)
            pick = selection.get(str(key))
            if pick is None:
                if h.get('weight', 1) > 1:
                    unillustrated.append(key)
                continue
            files, offsets = h.get('files', []), h.get('frame_seconds', [])
            if isinstance(pick, bool) or not isinstance(pick, int) or not 0 <= pick < len(files):
                raise ValueError(f'{stem} highlight {key}: invalid selection index')
            offset = offsets[pick] if pick < len(offsets) else None
            if not isinstance(offset, (int, float)) or isinstance(offset, bool) or offset < 0:
                raise ValueError(f'{stem} highlight {key}: missing actual frame time')
            if not (item / 'frames' / stem / files[pick]).is_file():
                raise ValueError(f'{stem} highlight {key}: selected frame missing')
            selected.append({'highlight': key, 'seconds': offset})
        times = sorted(set(s['seconds'] for s in selected))
        gaps = [{'start_seconds': a, 'end_seconds': b, 'seconds': b-a} for a, b in zip(times, times[1:])]
        report['talks'][stem] = {
            'highlights': len(highlights), 'notes': note_count,
            'highlight_words': text_words, 'note_words': note_words,
            'application_words': application_words,
            'editorial_words': text_words + note_words + application_words,
            'exact_repeated_blocks': duplicates,
            'missing_or_invalid_evidence_highlights': missing,
            'unillustrated_priority_highlights': unillustrated,
            'selected_frames': selected,
            'largest_between_frame_gap': max(gaps, key=lambda g: g['seconds']) if gaps else None,
            'review_required': 'Read for semantic repetition and argument coverage; inspect useful visuals in unillustrated passages. No-frame talks may be correct.'
        }
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('item_dir', type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(audit(args.item_dir), indent=2, ensure_ascii=False))
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(1, f'Editorial audit: {error}\n')


if __name__ == '__main__':
    main()
