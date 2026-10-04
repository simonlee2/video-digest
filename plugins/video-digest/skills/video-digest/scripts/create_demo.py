#!/usr/bin/env python3
"""Create an original, fictional digest fixture. Never downloads media or calls AI."""
import argparse
import json
from pathlib import Path
from PIL import Image, ImageDraw


def create(project):
    project.mkdir(parents=True, exist_ok=False)
    item = project / 'groups/demo/01-small-feedback-loops'
    stem = '01_small-feedback-loops'
    frames = item / 'frames' / stem
    frames.mkdir(parents=True)
    (item / 'sessions').mkdir()

    def write(path, value):
        path.write_text(json.dumps(value, indent=2) + '\n')

    write(project / 'digest.json', {
        'title': 'Video Digest · Synthetic demo', 'brand': 'VIDEO DIGEST',
        'headline': 'A talk, ready to skim.',
        'lede': 'An original fictional example showing takeaways and slides. No real speaker or event is represented.',
        'footer': 'Synthetic demonstration content. No source video or AI-generated summary.',
        'languages': ['en'], 'slide_cap': 2,
    })
    write(item.parent / 'group.json', {'key': 'demo', 'label': 'Demo'})
    write(item / 'source.json', {'key': item.name, 'label': 'Small feedback loops', 'subtitle': 'Fictional example', 'url': ''})
    write(item / 'manifest.json', {'talks': [{'clip': f'clips/{stem}.mp4'}]})
    highlights = []
    # Original fictional evidence: deliberately includes later findings, not just
    # the opening thesis. No claim below represents an actual experiment.
    beats = [
        ('Ask one question', 'Test the uncertainty that could change the decision.',
         'The fictional team asks whether shoppers understand when a delivery will arrive.',
         ['The team initially blames checkout abandonment on price. Instead of redesigning checkout, it tests whether people can explain the delivery promise.', 'A narrow question makes the observation actionable: if people understand the promise, this experiment has not supported changing the copy.']),
        ('Observe behavior', 'Watch someone attempt the task before proposing a fix.',
         'In the fictional sessions, four of six participants misread the delivery estimate.',
         ['Participants narrate what they expect to happen after ordering. Four of six interpret the estimate as the dispatch date rather than arrival.', 'This small sample identifies a plausible misunderstanding; it does not estimate how common the problem is across all customers.']),
        ('Change one thing', 'Compare two explanations of the same promise.',
         'The team changes the wording while retaining the price and delivery service.',
         ['The revision says when the parcel should arrive and separately explains dispatch. Holding the service constant makes comprehension the immediate comparison.', 'The team checks whether participants can restate the promise, rather than asking whether they like the new wording.']),
        ('Close the loop', 'Use the result to decide the next experiment.',
         'Five of six participants understand the revised wording, but conversion remains untested.',
         ['The follow-up gives the team a reason to test the wording with real traffic. It has evidence of improved comprehension in these sessions, not proof of increased sales.', 'The next decision is a limited rollout with conversion and support contacts monitored together.']),
        ('Keep a guardrail', 'A better local measure can hide a worse outcome.',
         'The fictional rollout tracks delivery-related support contacts alongside completion.',
         ['A message that encourages checkout but creates unrealistic delivery expectations would move the wrong metric.', 'The team therefore checks support contacts and promise accuracy before expanding the rollout.']),
        ('Record the decision', 'Keep the learning even when the test does not win.',
         'The team records the question, observation, limitation, and next decision.',
         ['A short decision record lets the next team distinguish observed comprehension from an unproven conversion hypothesis.', 'A neutral conversion result still leaves useful evidence about which wording people understood and what remains unknown.']),
    ]
    transcript = []
    for i, (heading, image_caption, claim, notes) in enumerate(beats):
        files = []
        if i in (0, 3):
            image = Image.new('RGB', (1280, 720), '#173545' if i == 0 else '#e6d9bc')
            draw = ImageDraw.Draw(image)
            color = '#ffffff' if i == 0 else '#173545'
            draw.text((80, 100), f'{i+1:02d} / FICTIONAL REFERENCE', fill=color, font_size=24)
            draw.text((80, 250), heading, fill=color, font_size=60)
            draw.text((80, 380), image_caption, fill=color, font_size=26)
            image.save(frames / f'{i}.jpg')
            files = [f'{i}.jpg']
        highlights.append({'i': i, 'ts': f'00:0{i}:00', 'sec': i * 60,
            'text': claim, 'files': files, 'frame_seconds': [i * 60] if files else [],
            'caption': image_caption if files else '', 'image_alt': f'Fictional slide: {heading}',
            'editorial_heading': heading, 'editorial_notes': notes,
            'evidence_start_seconds': i * 60, 'evidence_end_seconds': i * 60 + 50,
            'editorial_inference': 'Use a decision log to preserve uncertainty as well as results.' if i == 5 else ''})
        transcript.append(f'[00:0{i}:00] {claim} ' + ' '.join(notes))
    (item / 'sessions' / f'{stem}.txt').write_text(
        'FICTIONAL SCRIPT: original reference, not a recording or measured study.\n' + '\n'.join(transcript) + '\n')
    write(item / 'highlights.json', {stem: {
        'program': {'kind': 'talk'}, 'title': 'Small feedback loops', 'speaker': 'Fictional presenter',
        'start': '00:00:00', 'highlights': highlights,
    }})
    write(item / 'frames' / f'sel_{stem}.json', {str(i): (0 if i in (0, 3) else None) for i in range(len(beats))})
    write(item / 'sessions' / f'{stem}.take.json', {
        'tldr': 'Small experiments turn an uncertain idea into something you can learn from.',
        'takeaway': 'Write down one question, run a small experiment, and use the result to choose your next step.',
    })
    return project


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path, help='new directory (must not already exist)')
    args = parser.parse_args()
    try:
        print(create(args.output))
    except FileExistsError:
        parser.exit(1, f'Output already exists: {args.output}. Choose a new directory.\n')
