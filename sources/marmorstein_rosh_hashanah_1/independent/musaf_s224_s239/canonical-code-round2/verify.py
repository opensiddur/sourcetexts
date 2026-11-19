"""Report actual coverage; --check requires the complete, independently reviewed volume."""
import argparse
import json
from pathlib import Path

from opensiddur.common.constants import SOURCETEXTS_ROOT
from opensiddur.importer.scan.review import review_is_current
from opensiddur.importer.util.internet_archive import write_if_changed
from . import BOOK
from .build import unit_review_text, front_text, instruction_review_text
from .realizations import review_payloads, validate_occurrences


def report(source):
    pages = json.loads((source/'pages.json').read_text())['pages']
    readings = json.loads((source/'readings.json').read_text())
    validate_occurrences(readings)
    reviews_path = source/'reviews.json'
    reviews = json.loads(reviews_path.read_text()) if reviews_path.exists() else {}
    completion_path = source/'page_completion.json'
    completion = json.loads(completion_path.read_text()) if completion_path.exists() else {}
    fragments = {}
    pending = []
    for unit in readings['units']:
        for lang, segments in unit['languages'].items():
            key = unit['stem']+'/'+lang
            entry = reviews.get(key, {})
            complete = review_is_current(entry, unit_review_text(unit, lang))
            if not complete:
                pending.append(key)
            for segment in segments:
                for fragment in segment['fragments']:
                    fragments.setdefault(fragment['scan'], []).append(key)
            for index, citation in enumerate(unit.get('citations', {}).get(lang, [])):
                key = f"citation/{unit['stem']}/{lang}/{index}"
                fragments.setdefault(citation['scan'], []).append(key)
                if not review_is_current(reviews.get(key, {}), instruction_review_text(citation)):
                    pending.append(key)
    for name, navigation in readings.get('navigation', {}).items():
        for lang in navigation['scan']:
            key = 'navigation/'+name+'/'+lang
            if not review_is_current(reviews.get(key, {}), navigation['raw']):
                pending.append(key)
    for name, instruction in readings.get('documentary_instructions', {}).items():
        key = 'instruction/'+name
        fragments.setdefault(instruction['scan'], []).append(key)
        if not review_is_current(reviews.get(key, {}), instruction_review_text(instruction)):
            pending.append(key)
    front_path = source/'front.json'
    if front_path.exists():
        for page in json.loads(front_path.read_text())['pages']:
            key = 'front/'+page['scan']
            fragments.setdefault(page['scan'], []).append(key)
            if not review_is_current(reviews.get(key, {}), front_text(page)):
                pending.append(key)
    for key, payload, scans in review_payloads(readings):
        for scan in scans:
            fragments.setdefault(scan, []).append(key)
        if not review_is_current(reviews.get(key, {}), payload):
            pending.append(key)
    independently_read = set()
    inventory_scans = {'s'+str(page['scan_page']) for page in pages}
    for path in (source/'independent').rglob('*.json'):
        payload = json.loads(path.read_text())
        if isinstance(payload, dict) and payload.get('reviewer'):
            independently_read.update(scan for p in payload.get('pages', [])
                                      if (scan := p['scan'].removesuffix('.jpg')) in inventory_scans)
    complete_pages = []
    for page in pages:
        scan = 's'+str(page['scan_page'])
        entry = completion.get(scan, {})
        if (entry.get('status') == 'complete' and entry.get('evidence')
                and entry.get('independent_model') and scan in independently_read
                and entry.get('reading_keys') == sorted(set(fragments.get(scan, [])))
                and all(key not in pending for key in fragments.get(scan, []))):
            complete_pages.append(scan)
    result = {'scan_leaves': len(pages), 'verified_page_labels': sum(bool(p.get('evidence')) for p in pages),
              'leaves_with_transcribed_excerpts': len(fragments),
              'leaves_independently_read': len(independently_read),
              'leaves_fully_transcribed_and_reviewed': len(complete_pages),
              'pending_unit_reviews': pending,
              'complete': len(complete_pages) == len(pages) and not pending,
              'note': 'OCR availability and excerpt coverage never imply complete page transcription.'}
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root', type=Path, default=SOURCETEXTS_ROOT)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--write-report', action='store_true')
    args = parser.parse_args(argv)
    source = args.source_root/BOOK
    result = report(source)
    text = json.dumps(result, ensure_ascii=False, indent=2)+'\n'
    if args.write_report:
        write_if_changed(source/'progress.json', text)
    print(text, end='')
    return int(args.check and not result['complete'])


if __name__ == '__main__':
    raise SystemExit(main())
