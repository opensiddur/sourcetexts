"""Build source witnesses and the expanded mahzor from image readings.

Unreviewed material requires --draft and is visibly labeled as such. Missing
English witnesses produce no English file and never acquire substitute words.
"""
import argparse
import json
import re
from copy import deepcopy
from pathlib import Path

from lxml import etree
import yaml

from opensiddur.common.constants import PROJECT_DIRECTORY, SOURCETEXTS_ROOT
from opensiddur.common.urn_registry import load_registry, parse_urn
from opensiddur.importer.scan.authoring import (
    TEI, J, XML, element, mixed_words, append_words, write_documents, apply_corrections,
)
from opensiddur.importer.scan.navigation import append_instruction
from opensiddur.importer.scan.review import review_is_current
from opensiddur.importer.util.internet_archive import page_image_url, write_if_changed
from opensiddur.importer.util.validation import validate
from . import BOOK, IDENTIFIER, PROJECTS, EXPANDED, ROOT_URN, EXPANDED_URN
from .realizations import prepare_unit, prepare_documents, selection, review_payloads, validate_occurrences

FRONT_KINDS = ('cover', 'title', 'copyright', 'preface')
ROLE_LABELS = {'reader': 'חזן', 'congregation': 'קהל',
               'reader_and_congregation': 'קהל וחזן', 'oleh': 'העולה לתורה',
               'blower': 'תוקע'}


def document(lang, project, title, urn, *, index=False, draft=False):
    root = etree.Element(f'{{{TEI}}}TEI', nsmap={'tei': TEI, 'j': J}, attrib={XML+'lang': lang})
    desc = element(element(root, 'teiHeader'), 'fileDesc')
    titles = element(desc, 'titleStmt')
    element(titles, 'title', title, type='main')
    responsibility = element(titles, 'respStmt')
    element(responsibility, 'resp', 'AI-assisted scan reading and JLPTEI encoding', key='trc')
    element(responsibility, 'name', 'Codex', ref='urn:x-opensiddur:contributor:opensiddur.org/codex')
    edition = element(desc, 'editionStmt')
    element(edition, 'edition', ('DRAFT: independent adjudication pending. ' if draft else '')
            + 'Digitization in progress. Independent image readings and '
              'adjudications are recorded in sources/marmorstein_rosh_hashanah_1/.')
    publication = element(desc, 'publicationStmt')
    element(element(publication, 'distributor'), 'ref', 'Open Siddur Project', target='https://opensiddur.org')
    element(publication, 'idno', urn+'@'+project, type='urn')
    availability = element(publication, 'availability', status='free')
    element(availability, 'licence', 'CC0 1.0 Universal', target='https://creativecommons.org/publicdomain/zero/1.0/')
    source = element(desc, 'sourceDesc')
    if index:
        bibl = element(source, 'bibl')
        bibl.set(XML+'id', 'project_source_bibl')
        element(bibl, 'title', 'Prayerbook for the New Year [First Day]')
        element(bibl, 'editor', 'Wolf Heidenheim', role='arranger')
        element(bibl, 'editor', 'Jenny Marmorstein', role='translator')
        element(bibl, 'publisher', 'Victor Goldschmidt Publishers')
        element(bibl, 'pubPlace', 'Basle')
        element(bibl, 'date', '1965', when='1965')
        element(bibl, 'idno', f'https://archive.org/details/{IDENTIFIER}', type='url')
        element(bibl, 'idno', IDENTIFIER, type='internet_archive')
        element(bibl, 'date', '2026-11-08', type='accessed', when='2026-11-08')
        element(bibl, 'ref', 'Open Siddur source record', target='https://opensiddur.org/?p=69112')
        element(bibl, 'note', 'Digital imaging and document preparation: Aharon N. Varady; '
                'copy held by the HUC-JIR Klau Library, Cincinnati. The scan is the source. '
                'Independent reader: Claude Opus 5.5; CLI configured for medium reasoning. '
                'No translations have been supplied for passages absent from the English edition.')
    else:
        element(element(source, 'bibl'), 'ptr', target=f'/{project}/index#project_source_bibl')
    return root, element(element(root, 'text'), 'body')


def words(parent, text, lang):
    if lang == 'en':
        mixed_words(parent, text)
    else:
        # Preserve the source spelling/pointing, including its abbreviated Name.
        end = 0
        # Maqaf and sof pasuq are boundaries, despite sharing the Hebrew block.
        points = r'[\u0591-\u05bd\u05bf\u05c1\u05c2\u05c4\u05c5\u05c7]'
        letters_and_points = r'[\u05d0-\u05ea\u0591-\u05bd\u05bf\u05c1\u05c2\u05c4\u05c5\u05c7]'
        name = rf'([ובלמכש]?{points}*)(י{points}*(?:י{points}*|ה{points}*ו{points}*ה{points}*))'
        for match in re.finditer(r'(?<!'+letters_and_points+')'+name+'(?!'+letters_and_points+')', text):
            append_words(parent, text[end:match.start()]+match[1])
            element(parent, 'j:divineName', match[2])
            end = match.end()
        append_words(parent, text[end:])


def quotation_words(parent, text, quotations, lang):
    """Bound excerpts inside a fragment without splitting its source condition."""
    for quotation in quotations:
        quoted = quotation['text']
        if not quoted or text.count(quoted) != 1:
            raise ValueError('Quotation must identify one remaining source span')
        before, _, text = text.partition(quoted)
        words(parent, before, lang)
        source = quotation['source_reference']
        book, chapter, verse = source.rsplit(':', 1)[-1].split('/')
        part = quotation.get('source_reference_part')
        if part:
            if (part.get('unit') != 'half-verse' or part.get('n') not in ('a', 'b')
                    or part.get('corresp') != source+'/'+part['n']):
                raise ValueError('Quotation half-verse must identify its canonical verse part')
            if quotation.get('chapter_corresp') or quotation.get('source_reference_corresp'):
                raise ValueError('A partial quotation must not map the whole chapter or verse')
        elif not quotation.get('chapter_corresp') or not quotation.get('source_reference_corresp'):
            raise ValueError('Quotation requires chapter and verse correspondences or a canonical half-verse')
        element(parent, 'milestone', unit='chapter', n=chapter,
                **({'corresp': quotation['chapter_corresp']} if quotation.get('chapter_corresp') else {}))
        element(parent, 'milestone', unit='verse', n=verse,
                **({'corresp': quotation['source_reference_corresp']} if quotation.get('source_reference_corresp') else {}))
        if part:
            element(parent, 'milestone', **part)
        words(element(parent, 'seg', source=source), quoted, lang)
        if part:
            element(parent, 'milestone', unit=part['unit'])
        element(parent, 'milestone', unit='verse')
        element(parent, 'milestone', unit='chapter')
    words(parent, text, lang)


def rubric_words(parent, rubric, lang):
    """Keep source abbreviations selectable without losing their printed form."""
    if isinstance(rubric, str):
        words(parent, rubric, lang)
        return
    if rubric.get('resp'):
        parent.set('resp', rubric['resp'])
    text = rubric['text']
    if rubric.get('language_spans') and rubric.get('abbreviations'):
        raise ValueError('Overlapping abbreviation and language-span interpretation is not supported')
    for span in rubric.get('language_spans', []):
        before, found, text = text.partition(span['text'])
        if not found:
            raise ValueError('Language span missing from its source text')
        words(parent, before, lang)
        foreign = element(parent, 'foreign')
        foreign.set(XML+'lang', span['language'])
        words(foreign, span['text'], span['language'])
    for abbreviation in rubric.get('abbreviations', []):
        before, found, text = text.partition(abbreviation['abbr'])
        if not found:
            raise ValueError('Rubric abbreviation missing from its source text')
        words(parent, before, lang)
        choice = element(parent, 'choice')
        element(choice, 'abbr', abbreviation['abbr'])
        element(choice, 'expan', abbreviation['expan'])
    words(parent, text, lang)
    for uncertain in rubric.get('uncertain_characters', []):
        word, character = uncertain['word'], uncertain['character']
        if len(character) != 1 or word.count(character) != 1:
            raise ValueError('An uncertain character must occur once in its source word')
        matches = [(node, field, value)
                   for node in parent.iter() for field in ('text', 'tail')
                   if (node is not parent or field == 'text')
                   and (value := getattr(node, field)) and word in value]
        if len(matches) != 1 or matches[0][2].count(word) != 1:
            raise ValueError('Uncertain source word is missing or ambiguous')
        node, field, value = matches[0]
        offset = value.index(word) + word.index(character)
        glyph = etree.Element('{'+TEI+'}c', cert='low')
        glyph.text, glyph.tail = character, value[offset+1:]
        setattr(node, field, value[:offset])
        if field == 'text':
            node.insert(0, glyph)
        else:
            container = node.getparent()
            container.insert(container.index(node)+1, glyph)


def instruction_review_text(instruction):
    parts = [instruction['text']]
    parts.extend(a['abbr']+' ['+a['expan']+']' for a in instruction.get('abbreviations', []))
    parts.extend(span['text']+' ['+span['language']+']'
                 for span in instruction.get('language_spans', []))
    parts.extend(item['word']+' [uncertain '+item['character']+'; cert=low]'
                 for item in instruction.get('uncertain_characters', []))
    parts.extend('[quotation '+json.dumps(quotation, ensure_ascii=False, sort_keys=True)+']'
                 for quotation in instruction.get('quotations', []))
    return ' '.join(parts)


def unit_urn(unit):
    """Name the actual excerpt rather than its containing chapter."""
    if unit.get('publication_context'):
        return unit['publication_context']
    target = unit.get('start', unit['urn'])
    if unit.get('end'):
        if target.partition('/')[0] != unit['end'].partition('/')[0]:
            raise ValueError('A documentary unit cannot span different works')
        target += '-/'+unit['end'].partition('/')[2]
    return target


def unit_instructions(unit, lang):
    return [note for note in unit.get('instructions', [])
            if lang in note.get('witnesses', [lang])]


def unit_document(unit, lang, draft):
    project = PROJECTS[lang]
    root, body = document(lang, project, unit['title'][lang], unit_urn(unit), draft=draft)
    if unit.get('omit_publication_urn'):
        idno = root.find(f'.//{{{TEI}}}publicationStmt/{{{TEI}}}idno')
        idno.getparent().remove(idno)
    title_language = unit.get('title_languages', {}).get(lang)
    if title_language:
        root.find(f'.//{{{TEI}}}titleStmt/{{{TEI}}}title').set(XML+'lang', title_language)
    if unit.get('publication_context'):
        body = element(body, 'div', corresp=unit['publication_context'])
    biblical_root = ':bible:' in unit['urn']
    reuse = unit.get('reuse', {}).get(lang)
    div = element(body, 'div', **({'corresp': unit['urn']} if not reuse and unit.get('map_root', not biblical_root) else {}))
    opening = unit['languages'][lang][0]['fragments'][0]
    div.set('facs', page_image_url(IDENTIFIER, int(opening['scan'][1:])-1, size=''))
    last = unit['languages'][lang][-1]['fragments'][-1]
    if opening.get('printed_page') is not None and last.get('printed_page') is not None:
        element(root.find(f'.//{{{TEI}}}sourceDesc/{{{TEI}}}bibl'), 'biblScope',
                unit='pages', **{'from': opening['printed_page'], 'to': last['printed_page']})
    pages = {(opening.get('printed_page'), last.get('printed_page'))}
    for printing in unit.get('source_printings', {}).get(lang, []):
        pair = (printing['printed_page'], printing['printed_page'])
        if pair not in pages:
            element(root.find(f'.//{{{TEI}}}sourceDesc/{{{TEI}}}bibl'), 'biblScope', unit='pages',
                    **{'from': pair[0], 'to': pair[1]})
            pages.add(pair)
    if reuse:
        # A documentary occurrence can reuse an identical earlier witness
        # without registering the canonical prayer a second time.
        element(element(div, 'p'), 'j:transclude', type='inline', target=reuse+'@'+project)
        return root
    wording = unit.get('wording_selection', [])
    if wording:
        declaration = element(div, 'j:declare')
        declaration.set(XML+'id', unit['stem']+'_wording')
        feature_structures(declaration, wording)
    conditions = unit.get('conditions', [])
    if unit.get('marked') and not conditions:
        raise ValueError('Marked source unit requires a condition')
    if conditions:
        conditional = element(div, 'j:conditional', **({'type': 'marked'} if unit.get('marked') else {}))
        conditional.set(XML+'id', unit['stem']+'_condition')
        feature_structures(element(conditional, 'j:all'), conditions)
    current_page = None
    if unit.get('opening_page', {}).get(lang):
        element(div, 'pb', ed='1965', n=opening['printed_page'],
                facs=page_image_url(IDENTIFIER, int(opening['scan'][1:])-1, size=''))
        current_page = opening['scan']
    if unit.get('head', {}).get(lang):
        opening = unit['languages'][lang][0]['fragments'][0]
        if current_page != opening['scan'] and opening.get('page_start', True):
            element(div, 'pb', ed='1965', n=opening['printed_page'],
                    facs=page_image_url(IDENTIFIER, int(opening['scan'][1:])-1, size=''))
        current_page = opening['scan']
        element(div, 'head', unit['head'][lang]).set(XML+'lang', lang)
    for instruction in unit_instructions(unit, lang):
        if instruction.get('placement') == 'condition' and not conditions:
            raise ValueError('A condition rubric requires a condition')
        parent = conditional if instruction.get('placement') == 'condition' else div
        note = element(parent, 'note', type=instruction.get('type', 'instruction'))
        if parent is not div:
            parent.remove(note)
            parent.insert(len(parent)-1, note)
        note.set(XML+'lang', instruction['language'])
        rubric_words(note, instruction, instruction['language'])
    citations = unit.get('citations', {}).get(lang, [])
    if citations:
        notes = element(root, 'standOff', type='notes')
        root.remove(notes)
        root.insert(list(root).index(body.getparent()), notes)
        passage_scans = {fragment['scan'] for segment in unit['languages'][lang]
                         for fragment in segment['fragments']}
        for citation in citations:
            if citation['scan'] not in passage_scans:
                raise ValueError('Citation scan is outside the passage')
            note = element(notes, 'note', type=citation.get('note_type', 'citation'),
                           target=citation.get('target', unit.get('start', unit['urn'])))
            if citation.get('language'):
                note.set(XML+'lang', citation['language'])
            if citation.get('resp'):
                note.set('resp', citation['resp'])
            if citation.get('conditions'):
                condition = element(note, 'j:condition')
                feature_structures(element(condition, 'j:all'), citation['conditions'])
            citation_text = citation['text'].strip()
            if citation_text.startswith('(') and citation_text.endswith(')'):
                citation_text = citation_text[1:-1].strip()
            paragraph = element(note, 'p')
            if citation.get('reference'):
                element(paragraph, 'ref', citation_text, target=citation['reference'])
            elif citation.get('text_type'):
                element(paragraph, 'seg', citation_text, type=citation['text_type'])
            elif citation.get('uncertain_characters') or citation.get('abbreviations'):
                rubric_words(paragraph, dict(citation, text=citation_text), lang)
            else:
                paragraph.text = citation_text
    paragraph = None
    current_paragraph = None
    current_chapter = None
    seen_chapters = set()
    active_reference = None
    active_reference_urn = None
    line_group = None
    poetry = unit.get('poetry', {}).get(lang, False)

    def close_references():
        nonlocal active_reference, active_reference_urn, current_chapter
        if active_reference:
            element(paragraph, 'milestone', unit=active_reference)
            active_reference = None
            active_reference_urn = None
        if current_chapter:
            element(paragraph, 'milestone', unit='chapter')
            current_chapter = None

    segment_condition_scopes = []
    for segment_index, segment in enumerate(unit['languages'][lang]):
        if segment.get('transclude'):
            if paragraph is not None:
                close_references()
            element(div, 'j:transclude', type='external', target=segment['transclude']+'@'+project)
            paragraph = current_paragraph = None
            line_group = None
            continue
        identity = segment['fragments'][0].get('line', segment.get('paragraph', 1))
        text_language = segment.get('language', lang)
        if paragraph is None or identity != current_paragraph:
            if poetry and line_group is None:
                line_group = element(div, 'lg')
            paragraph = element(line_group if poetry else div, 'l' if poetry else 'p')
            if text_language != lang:
                paragraph.set(XML+'lang', text_language)
            current_paragraph = identity
        segment_conditions = segment.get('conditions', [])
        opening_fragment = segment['fragments'][0]
        if (segment_conditions and opening_fragment['scan'] != current_page
                and opening_fragment.get('page_start', True)):
            # A continuation rubric belongs to the new source page too.
            # Emit its boundary before the conditional's own note.
            attributes = {'ed': '1965', 'facs': page_image_url(
                IDENTIFIER, int(opening_fragment['scan'][1:])-1, size='')}
            if opening_fragment.get('printed_page') is not None:
                attributes['n'] = opening_fragment['printed_page']
            element(paragraph, 'pb', **attributes)
            current_page = opening_fragment['scan']
        scope_end = segment.get('condition_end_corresp')
        if scope_end and not segment_conditions:
            raise ValueError('A condition endpoint requires a condition')
        if segment_conditions:
            # A repeated source rubric can govern the remaining stanzas, across
            # their independent correspondence boundaries and page breaks.
            scope_end_index = segment_index
            if scope_end:
                matches = [i for i, candidate in enumerate(unit['languages'][lang])
                           if candidate.get('corresp') == scope_end
                           and not candidate.get('transclude')]
                if len(matches) != 1 or matches[0] < segment_index:
                    raise ValueError('Condition endpoint must identify one current or later segment')
                scope_end_index = matches[0]
                if segment.get('marked') and scope_end_index != segment_index:
                    raise ValueError('Marked source condition must end in its own segment')
            if segment_condition_scopes and scope_end_index > segment_condition_scopes[-1][0]:
                raise ValueError('Condition scopes cannot cross')
            segment_condition_id = unit['stem']+'_segment_'+str(segment_index)
            segment_condition_scopes.append((scope_end_index, segment_condition_id))
            condition = element(paragraph, 'j:conditional', **({'type': 'marked'} if segment.get('marked') else {}))
            condition.set(XML+'id', segment_condition_id)
            if segment.get('condition_instruction'):
                note = element(condition, 'note', type='instruction')
                rubric_language = segment.get('condition_instruction_language', lang)
                note.set(XML+'lang', rubric_language)
                words(note, segment['condition_instruction'], rubric_language)
            feature_structures(element(condition, 'j:all'), segment_conditions)
        fragments = segment['fragments']
        if segment.get('marked'):
            if not segment_conditions or not fragments[0]['text'].startswith('(') or not fragments[-1]['text'].endswith(')'):
                raise ValueError('Marked source condition requires paired source parentheses')
            fragments = deepcopy(fragments)
            fragments[0]['text'] = fragments[0]['text'][1:]
            fragments[-1]['text'] = fragments[-1]['text'][:-1]
        for index, fragment in enumerate(fragments):
            if 'line' in fragment:
                if not poetry or segment_conditions:
                    raise ValueError('Fragment lines require unconditional poetry')
                if fragment['line'] != current_paragraph:
                    paragraph = element(line_group, 'l')
                    if text_language != lang:
                        paragraph.set(XML+'lang', text_language)
                    current_paragraph = fragment['line']
            if fragment['scan'] != current_page:
                attributes = {'ed': '1965', 'facs': page_image_url(IDENTIFIER, int(fragment['scan'][1:])-1, size='')}
                if fragment.get('printed_page') is not None:
                    attributes['n'] = fragment['printed_page']
                if fragment.get('page_start', True):
                    element(paragraph, 'pb', **attributes)
                current_page = fragment['scan']
            if index == 0 and segment.get('edition_label'):
                close_references()
                if not segment.get('edition_label_in_reference'):
                    element(paragraph, 'label', segment['edition_label'])
                    append_words(paragraph, ' ')
            if index == 0:
                if segment.get('end_reference_before_instructions'):
                    if not segment.get('instructions'):
                        raise ValueError('A rubric boundary requires an instruction')
                    if not re.fullmatch(r'urn:x-opensiddur:text:bible:[^/]+/\d+/\d+',
                                        segment.get('corresp', '')):
                        raise ValueError('A rubric boundary requires a verse correspondence')
                    if active_reference:
                        element(paragraph, 'milestone', unit=active_reference)
                        active_reference = active_reference_urn = None
                for instruction in segment.get('instructions', []):
                    note = element(paragraph, 'note', type=instruction.get('type', 'instruction'))
                    note.set(XML+'lang', instruction.get('language', lang))
                    rubric_words(note, instruction, instruction.get('language', lang))
            for instruction in fragment.get('instructions', []):
                note = element(paragraph, 'note', type=instruction.get('type', 'description'))
                note.set(XML+'lang', instruction.get('language', lang))
                rubric_words(note, instruction, instruction.get('language', lang))
            if segment_index == 0 and index == 0 and unit.get('text_corresp'):
                element(paragraph, 'milestone', unit='prayer-part', corresp=unit['text_corresp'])
            reference_marker = None
            if index == 0 and segment.get('speaker_before_reference') and segment.get('speaker') and active_reference:
                element(paragraph, 'milestone', unit=active_reference)
                active_reference = None
                active_reference_urn = None
            if index == 0 and segment.get('corresp'):
                urn = segment['corresp']
                biblical = ':bible:' in urn
                if biblical:
                    parts = urn.split(':')[-1].split('/')
                    chapter = urn.rsplit('/', len(parts)-2)[0]
                    if chapter != current_chapter:
                        close_references()
                        attributes = {'unit': 'chapter', 'n': parts[1]}
                        # Excerpted chapters supply context, not a substitute
                        # witness for the whole chapter.
                        if chapter not in seen_chapters and ((chapter == unit['urn'] and not unit.get('start')) or chapter in unit.get('complete_chapters', [])):
                            attributes['corresp'] = chapter
                            seen_chapters.add(chapter)
                        element(paragraph, 'milestone', **attributes)
                        current_chapter = chapter
                    reference_unit = ('verse' if len(parts) == 3 else
                                      'half-verse' if parts[-1] in ('a', 'b') else 'verse-part')
                    attributes = {'n': parts[-1]}
                else:
                    reference_unit, attributes = segment.get('reference_unit', 'prayer-part'), {}
                    quoted_source = segment.get('source', '')
                    if reference_unit == 'verse' and ':bible:' in quoted_source:
                        parts = quoted_source.rsplit(':', 1)[-1].split('/')
                        chapter = quoted_source.rsplit('/', len(parts)-2)[0]
                        if chapter != current_chapter:
                            close_references()
                            chapter_attributes = {'unit': 'chapter', 'n': parts[1]}
                            if segment.get('chapter_corresp'):
                                chapter_attributes['corresp'] = segment['chapter_corresp']
                            element(paragraph, 'milestone', **chapter_attributes)
                            current_chapter = chapter
                        # The occurrence marker is a verse even when its bounded
                        # source names a half-verse or named verse-part.
                        attributes = {'n': parts[2]}
                    elif current_chapter:
                        close_references()
                if active_reference and active_reference != reference_unit:
                    element(paragraph, 'milestone', unit=active_reference)
                reference_marker = element(paragraph, 'milestone', unit=reference_unit, corresp=urn, **attributes)
                active_reference = reference_unit
                active_reference_urn = urn
            if index == 0 and segment.get('edition_label_in_reference'):
                if not segment.get('edition_label') or not segment.get('corresp'):
                    raise ValueError('A referenced edition label needs its text and correspondence')
                element(paragraph, 'label', segment['edition_label'])
                append_words(paragraph, ' ')
            if index == 0 and segment.get('speaker'):
                speaker = segment['speaker']
                if 'label' in speaker:
                    role = speaker['role']
                    if role not in ROLE_LABELS:
                        raise ValueError(f'Unknown speaker role: {role}')
                else:
                    expansion = speaker['expan']
                    try:
                        roles = {label: role for role, label in ROLE_LABELS.items()}
                        roles['חזן וקהל'] = 'reader_and_congregation'
                        role = roles[expansion]
                    except KeyError:
                        raise ValueError(f'Unknown speaker expansion: {expansion}') from None
                identity = 'urn:x-opensiddur:instruction:role/'+role
                description = element(paragraph, 'note', type='description', corresp=identity)
                if speaker.get('resp'):
                    description.set('resp', speaker['resp'])
                description.set(XML+'lang', speaker.get('language', 'he'))
                if 'label' in speaker:
                    words(description, speaker['label'], speaker.get('language', 'he'))
                else:
                    choice = element(description, 'choice')
                    element(choice, 'abbr', speaker['abbr'])
                    element(choice, 'expan', speaker['expan'])
                append_words(paragraph, ' ')
                if segment.get('speaker_before_reference') and reference_marker is not None:
                    paragraph.remove(description)
                    paragraph.insert(paragraph.index(reference_marker), description)
            if segment.get('canonical'):
                close_references()
                attributes = {'target': segment['canonical']+'@'+project}
                if segment.get('canonical_end'):
                    attributes['targetEnd'] = segment['canonical_end']
                element(paragraph, 'j:transclude', type='inline', **attributes)
                if not fragment.get('join_next'):
                    append_words(paragraph, ' ')
                continue
            if segment.get('repeat'):
                # Repeated recitation reuses the witness; it does not define a
                # second element with the same canonical identity in one file.
                close_references()
                element(paragraph, 'j:transclude', type='inline', target=segment['repeat']+'@'+project)
                append_words(paragraph, ' ')
                continue
            source_reference = segment.get('source_reference')
            if source_reference and index == 0:
                if active_reference == 'prayer-part' and active_reference_urn:
                    enclosing_depth = active_reference_urn.rsplit(':', 1)[-1].count('/')
                    for key in ('chapter_corresp', 'source_reference_corresp'):
                        context = segment.get(key)
                        if context and context.rsplit(':', 1)[-1].count('/') <= enclosing_depth:
                            raise ValueError('Quote context must be deeper than its enclosing prayer-part: '+context)
                book, chapter, verse = source_reference.rsplit(':', 1)[-1].split('/')
                chapter_attributes = {'unit': 'chapter', 'n': chapter}
                if segment.get('chapter_corresp'):
                    chapter_attributes['corresp'] = segment['chapter_corresp']
                element(paragraph, 'milestone', **chapter_attributes)
                element(paragraph, 'milestone', unit='verse', n=verse,
                        corresp=segment.get('source_reference_corresp', source_reference))
                if part := segment.get('source_reference_part'):
                    if (part['unit'] not in ('half-verse', 'verse-part') or
                            (part['unit'] == 'half-verse' and part['n'] not in ('a', 'b'))):
                        raise ValueError('Invalid quotation subverse boundary')
                    parent_verse = segment.get('source_reference_corresp', source_reference)
                    if part['corresp'] != parent_verse+'/'+part['n']:
                        raise ValueError('Quotation subverse must belong to its verse context')
                    element(paragraph, 'milestone', **part)
            if index == 0 and segment.get('anchor'):
                element(paragraph, 'anchor').set(XML+'id', segment['anchor'])
            content = paragraph
            if segment.get('source'):
                attributes = {'source': segment['source']}
                if segment.get('source_type'):
                    attributes['type'] = segment['source_type']
                content = element(paragraph, 'seg', **attributes)
            if fragment.get('quotations') and any(fragment.get(key) for key in (
                    'alternatives', 'qere_ketiv', 'expansion', 'abbreviations',
                    'uncertain_characters', 'enlarged_letters')):
                raise ValueError('Quotation spans cannot overlap other fragment interpretations')
            if fragment.get('text_type'):
                content = element(content, 'seg', type=fragment['text_type'])
                if fragment.get('text_subtype'):
                    content.set('subtype', fragment['text_subtype'])
            if fragment.get('optional_spans'):
                text = fragment['text']
                for number, span in enumerate(fragment['optional_spans']):
                    before, found, text = text.partition(span['printed'])
                    if not found:
                        raise ValueError('Optional word not found in its source fragment')
                    words(content, before, text_language)
                    identifier = unit['stem']+'_optional_'+str(segment_index)+'_'+str(index)+'_'+str(number)
                    condition = element(content, 'j:conditional', type='marked')
                    condition.set(XML+'id', identifier)
                    feature_structures(element(condition, 'j:all'), [dict(type='opensiddur:variant', features={span['condition']: True})])
                    words(content, span['text'], text_language)
                    element(content, 'j:endConditional', target='#'+identifier)
                words(content, text, text_language)
            elif fragment.get('alternatives'):
                if any(fragment.get(key) for key in ('qere_ketiv', 'expansion', 'abbreviations',
                                                     'uncertain_characters', 'enlarged_letters')):
                    raise ValueError('Alternatives cannot be combined with other fragment readings')
                text = fragment['text']
                for alternative in fragment['alternatives']:
                    printed, readings = alternative['printed'], alternative['readings']
                    if not printed or text.count(printed) != 1 or len(readings) < 2:
                        raise ValueError('Alternatives require one printed span and at least two readings')
                    before, text = text.split(printed, 1)
                    words(content, before, text_language)
                    choice = element(content, 'choice')
                    if alternative.get('xml_id'):
                        choice.set(XML+'id', alternative['xml_id'])
                    for reading in readings:
                        option = element(choice, 'j:option')
                        if isinstance(reading, dict):
                            for attribute in ('corresp','facs'):
                                if reading.get(attribute):
                                    option.set(attribute, reading[attribute])
                            if reading.get('quotations'):
                                if any(reading.get(key) for key in ('abbreviations', 'language_spans', 'uncertain_characters')):
                                    raise ValueError('Quotation option cannot overlap other interpretations')
                                quotation_words(option, reading['text'], reading['quotations'], text_language)
                            else:
                                rubric_words(option, reading, text_language)
                        else:
                            words(option, reading, text_language)
                words(content, text, text_language)
            elif fragment.get('qere_ketiv'):
                if any(fragment.get(key) for key in ('expansion', 'abbreviations',
                                                     'uncertain_characters', 'enlarged_letters')):
                    raise ValueError('Qere/ketiv cannot be combined with other fragment readings')
                text = fragment['text']
                for reading in fragment['qere_ketiv']:
                    written = reading['written']
                    word_character = r'[א-ת\u0591-\u05bd\u05bf\u05c1\u05c2\u05c4\u05c5\u05c7\u034f\u200c\u200d]'
                    matches = list(re.finditer(r'(?<!'+word_character+')'+re.escape(written)+
                                               r'(?!'+word_character+')', text)) if written else []
                    if len(matches) != 1:
                        raise ValueError('Qere/ketiv must identify one printed span')
                    match = matches[0]
                    before, text = text[:match.start()], text[match.end():]
                    words(content, before, text_language)
                    choice = element(content, 'choice')
                    words(element(choice, 'j:read'), reading['read'], text_language)
                    words(element(choice, 'j:written'), written, text_language)
                words(content, text, text_language)
            elif fragment.get('expansion'):
                choice = element(content, 'choice')
                abbreviation = element(choice, 'abbr')
                if fragment.get('divine_name_tail'):
                    start = fragment['text'].rindex('י')
                    append_words(abbreviation, fragment['text'][:start])
                    element(abbreviation, 'j:divineName', fragment['text'][start:])
                else:
                    words(abbreviation, fragment['text'], lang)
                words(element(choice, 'expan'), fragment['expansion'], lang)
            elif fragment.get('abbreviations') or fragment.get('uncertain_characters'):
                rubric_words(content, fragment, text_language)
            elif fragment.get('enlarged_letters'):
                letters = fragment['enlarged_letters']
                if any(len(letter) != 1 or fragment['text'].count(letter) != 1 for letter in letters):
                    raise ValueError('Each enlarged letter must identify one source character')
                for part in re.split('(['+re.escape(''.join(letters))+'])', fragment['text']):
                    if part in letters:
                        element(content, 'c', part, rend='large')
                    else:
                        words(content, part, text_language)
            elif fragment.get('quotations'):
                quotation_words(content, fragment['text'], fragment['quotations'], text_language)
            else:
                words(content, fragment['text'], text_language)
            if source_reference and index == len(segment['fragments']) - 1:
                if part := segment.get('source_reference_part'):
                    element(paragraph, 'milestone', unit=part['unit'])
                element(paragraph, 'milestone', unit='verse')
                element(paragraph, 'milestone', unit='chapter')
            next_fragment = None
            if unit.get('join_source_fragments'):
                if index+1 < len(fragments):
                    next_fragment = fragments[index+1]
                elif segment_index+1 < len(unit['languages'][lang]):
                    next_fragment = unit['languages'][lang][segment_index+1]['fragments'][0]
            owns_separator = (next_fragment and next_fragment['text'] and
                              (next_fragment['text'][0].isspace() or next_fragment['text'][0] in ',.;:!?)]'))
            if not owns_separator and not fragment.get('join_next') and not fragment['text'].rstrip().endswith('־'):
                append_words(paragraph, ' ')
        if segment.get('end_reference'):
            close_references()
        while segment_condition_scopes and segment_condition_scopes[-1][0] == segment_index:
            _, condition_id = segment_condition_scopes.pop()
            element(paragraph, 'j:endConditional', target='#'+condition_id)
        if segment.get('repeat_cue'):
            close_references()
            cue = segment['repeat_cue']
            if cue.get('corresp'):
                element(paragraph, 'milestone', unit='navigation', corresp=cue['corresp'])
            note = element(paragraph, 'note', type='instruction')
            note.set(XML+'lang', lang)
            element(note, 'ref', cue['text'], target=cue['target']+'@'+project)
            if cue.get('corresp'):
                element(paragraph, 'milestone', unit='navigation')
    if segment_condition_scopes:
        raise ValueError('Unclosed condition scope')
    if paragraph is not None:
        close_references()
    if unit.get('text_corresp'):
        element(paragraph, 'milestone', unit='prayer-part')
    if conditions:
        element(div, 'j:endConditional', target='#'+unit['stem']+'_condition')
    if wording:
        element(div, 'j:endDeclare', target='#'+unit['stem']+'_wording')
    if unit.get('page_context') or unit.get('canonical_whole') or any(s.get('canonical') for s in unit['languages'][lang]):
        context = unit.get('page_context') or unit_urn(unit).partition(':siddur:')[2]
        if not context:
            raise ValueError('A repeated printing needs its siddur context')
        for page in div.iter('{'+TEI+'}pb'):
            page.set('ed', '1965 '+context)
    return root


def unit_text(unit, lang):
    return ' '.join(fragment['text'] for segment in unit['languages'][lang] for fragment in segment['fragments'])


def unit_review_text(unit, lang):
    # This is a review payload, not printed prayer text. Include both the
    # source abbreviation and its interpretation so either change needs review.
    parts = ([unit['head'][lang]] if unit.get('head', {}).get(lang) else [])
    if unit.get('opening_page', {}).get(lang):
        parts.append('[source page starts before opening rubric]')
    if unit.get('marked'):
        parts.append('[source condition is parenthesized]')
    parts.extend(instruction['text'] for instruction in unit_instructions(unit, lang))
    for instruction in unit_instructions(unit, lang):
        parts.extend(a['abbr']+' ['+a['expan']+']' for a in instruction.get('abbreviations', []))
        parts.extend(span['text']+' ['+span['language']+']'
                     for span in instruction.get('language_spans', []))
    for segment in unit['languages'][lang]:
        if segment.get('edition_label'):
            parts.append(segment['edition_label'])
        for instruction in segment.get('instructions', []):
            parts.append(instruction_review_text(instruction))
        if segment.get('end_reference_before_instructions'):
            parts.append('[reference ends before rubric; chapter continues]')
        if segment.get('condition_instruction'):
            parts.append(segment['condition_instruction'])
        if segment.get('condition_end_corresp'):
            parts.append('[condition through '+segment['condition_end_corresp']+']')
        if segment.get('source_reference_part'):
            parts.append('[quotation '+segment['source']+'; '+
                         segment['source_reference_part']['corresp']+']')
        if segment.get('speaker'):
            speaker = segment['speaker']
            parts.append(speaker['label']+' ['+speaker['role']+']' if 'label' in speaker else
                         speaker['abbr']+' ['+speaker['expan']+']')
        for fragment in segment['fragments']:
            parts.extend(instruction_review_text(instruction)
                         for instruction in fragment.get('instructions', []))
            parts.append(fragment['text'])
            parts.extend('[quotation '+json.dumps(quotation, ensure_ascii=False, sort_keys=True)+']'
                         for quotation in fragment.get('quotations', []))
            if fragment.get('text_type'):
                parts.append('['+fragment['text_type']+']')
                if fragment.get('text_subtype'):
                    parts.append('[subtype '+fragment['text_subtype']+']')
            if fragment.get('expansion'):
                parts.append('['+fragment['expansion']+']')
            parts.extend('[written '+reading['written']+'; read '+reading['read']+']'
                         for reading in fragment.get('qere_ketiv', []))
            parts.extend('[printed '+alternative['printed']+'; alternatives '+
                         ' | '.join(instruction_review_text(reading) if isinstance(reading, dict)
                                    else reading for reading in alternative['readings'])+
                         ('; anchor '+alternative['xml_id'] if alternative.get('xml_id') else '')+']'
                         for alternative in fragment.get('alternatives', []))
            parts.extend(a['abbr']+' ['+a['expan']+']' for a in fragment.get('abbreviations', []))
            parts.extend(item['word']+' [uncertain '+item['character']+'; cert=low]'
                         for item in fragment.get('uncertain_characters', []))
        if segment.get('repeat_cue'):
            cue = segment['repeat_cue']
            parts.append(cue['text']+' ['+cue['target']+']')
    return ' '.join(parts)


def reference(unit):
    return {'target': unit.get('start', unit['urn']),
            **({'targetEnd': unit['end']} if unit.get('end') else {})}


def feature_structures(parent, structures):
    for structure in structures:
        if 'operator' in structure:
            if structure['operator'] not in ('all', 'any', 'none', 'one'):
                raise ValueError('Unknown condition operator')
            feature_structures(element(parent, 'j:'+structure['operator']), structure['conditions'])
            continue
        features = element(parent, 'fs', type=structure['type'])
        for name, value in structure['features'].items():
            feature = element(features, 'f')
            feature.set('name', name)
            kind = ('binary' if isinstance(value, bool) else
                    'symbol' if isinstance(value, str) else 'numeric')
            element(feature, kind,
                    value=str(value).lower() if isinstance(value, bool) else str(value))


def transclude_unit(parent, unit, readings, *, project=None, documentary=False):
    settings = [] if unit.get('canonical_home') else selection(readings, unit['stem'])
    if settings:
        index = len(parent.getroottree().xpath('//*[local-name()="declare"]'))
        identifier = unit['stem']+'_printed_wording_'+str(index)
        declaration = element(parent, 'j:declare')
        declaration.set(XML+'id', identifier)
        feature_structures(declaration, settings)
    attributes = {'target': unit_urn(unit)} if documentary else reference(unit)
    if project:
        attributes['target'] += '@'+project
    element(parent, 'j:transclude', type='external', **attributes)
    if settings:
        element(parent, 'j:endDeclare', target='#'+identifier)


def expanded_order(parent, order, readings, by_stem):
    """Keep service choices local while sharing one sequence across languages."""
    for occurrence in order:
        if 'section' in occurrence:
            outer = element(parent, 'div')
            identifier = 'section_'+occurrence['section']
            outer.set(XML+'id', identifier)
            conditions = occurrence.get('conditions', [])
            if conditions:
                conditional = element(outer, 'j:conditional')
                conditional.set(XML+'id', identifier+'_condition')
                if occurrence.get('condition_rubrics'):
                    rubric = element(conditional, 'note', type='instruction')
                    for language, text in occurrence['condition_rubrics'].items():
                        part = element(rubric, 'foreign')
                        part.set(XML+'lang', language)
                        rubric_words(part, text, language)
                        append_words(rubric, ' ')
                all_conditions = element(conditional, 'j:all')
                feature_structures(all_conditions, conditions)
            content = element(outer, 'div')
            for language, heading in occurrence.get('heads', {}).items():
                element(content, 'head', heading).set(XML+'lang', language)
            if occurrence.get('role'):
                role = occurrence['role']
                try:
                    label = ROLE_LABELS[role]
                except KeyError:
                    raise ValueError(f'Unknown speaker role: {role}') from None
                element(content, 'note', label,
                        type='description', corresp='urn:x-opensiddur:instruction:role/'+role).set(XML+'lang', 'he')
            for language, rubric in occurrence.get('rubrics', {}).items():
                for text in rubric if isinstance(rubric, list) else [rubric]:
                    note = element(content, 'note', type='description')
                    note.set(XML+'lang', language)
                    rubric_words(note, text, language)
            if occurrence.get('declarations'):
                declaration = element(content, 'j:declare')
                declaration.set(XML+'id', identifier+'_settings')
                feature_structures(declaration, occurrence['declarations'])
            expanded_order(content, occurrence['order'], readings, by_stem)
            if occurrence.get('declarations'):
                element(content, 'j:endDeclare', target='#'+identifier+'_settings')
            if conditions:
                element(outer, 'j:endConditional', target='#'+identifier+'_condition')
        elif 'instruction' in occurrence:
            keys = occurrence['instruction']
            keys = keys if isinstance(keys, list) else [keys]
            instructions = [readings['documentary_instructions'][key] for key in keys]
            kinds = {instruction.get('type', 'instruction') for instruction in instructions}
            if len(kinds) != 1:
                raise ValueError('A shared bilingual rubric must have one semantic kind')
            note = element(parent, 'note', type=kinds.pop())
            for instruction in instructions:
                content = element(note, 'foreign') if len(instructions) > 1 else note
                content.set(XML+'lang', instruction['language'])
                rubric_words(content, instruction, instruction['language'])
                if content is not note:
                    append_words(note, ' ')
        elif 'navigation' in occurrence:
            navigation = readings['navigation'][occurrence['navigation']]
            clauses = deepcopy(navigation['clauses'])
            for clause in clauses:
                if 'target' in clause:
                    clause['target'] = clause['target'].format(project=PROJECTS['he'])
            append_instruction(parent, clauses, expanded=True)
        elif 'reference' in occurrence:
            element(parent, 'j:transclude', type='external', **occurrence['reference'])
        else:
            transclude_unit(parent, by_stem[occurrence['unit']], readings)


def front_text(page):
    return ' '.join(([page['head']] if page.get('head') else [])+page['paragraphs'])


def paratext_gate(parent, identifier, feature):
    conditional = element(parent, 'j:conditional')
    conditional.set(XML+'id', identifier)
    feature_structures(conditional, [{'type': 'opensiddur:paratext', 'features': {feature: True}}])


def add_front(root, pages, *, expanded=False):
    text = root.find(f'{{{TEI}}}text')
    front = etree.Element(f'{{{TEI}}}front')
    text.insert(0, front)
    if expanded:
        paratext_gate(front, 'expanded_editorial_front', 'include')
        title = element(front, 'div')
        title.set(XML+'lang', 'en')
        element(title, 'head', 'Expanded Ashkenazi Mahzor')
        element(title, 'p', 'First day of Rosh ha-Shanah')
        element(title, 'note', 'An editorial arrangement of the reviewed Heidenheim–Marmorstein passages. Digitization remains in progress.', type='description')
        element(front, 'j:endConditional', target='#expanded_editorial_front')
        return
    for page in pages:
        if page['kind'] not in FRONT_KINDS:
            continue
        facs = page_image_url(IDENTIFIER, int(page['scan'][1:])-1, size='')
        element(front, 'pb', ed='1965', facs=facs)
        identifier = 'front_'+page['scan']
        paratext_gate(front, identifier, 'title-page' if page['kind'] in ('title', 'copyright') else 'include')
        if page['kind'] == 'copyright':
            title = element(front, 'titlePage')
            title.set(XML+'lang', page['language'])
            imprint = element(title, 'docImprint')
            for index, paragraph in enumerate(page['paragraphs']):
                if index:
                    element(imprint, 'lb')
                words(imprint, paragraph, page['language'])
        elif page['kind'] == 'title':
            title = element(front, 'titlePage')
            title.set(XML+'lang', page['language'])
            titles = element(title, 'docTitle')
            layout = page.get('title_layout', {'main': 0, 'bylines': [1, 2], 'publisher': 3, 'place': 4})
            element(titles, 'titlePart', page['paragraphs'][layout['main']], type='main')
            if 'sub' in layout:
                element(titles, 'titlePart', page['paragraphs'][layout['sub']], type='sub')
            for index in layout['bylines']:
                byline = element(title, 'byline')
                language = page.get('paragraph_languages', {}).get(str(index), page['language'])
                if language != page['language']:
                    byline.set(XML+'lang', language)
                    byline = element(byline, 'foreign')
                    byline.set(XML+'lang', language)
                words(byline, page['paragraphs'][index], language)
            if any(key in layout for key in ('publisher', 'place', 'date')):
                imprint = element(title, 'docImprint')
                for key, tag in [('publisher', 'publisher'), ('place', 'pubPlace'), ('date', 'docDate')]:
                    if key in layout:
                        element(imprint, tag, page['paragraphs'][layout[key]])
        else:
            div = element(front, 'div')
            div.set(XML+'lang', page['language'])
            if page.get('head'):
                element(div, 'head', page['head'])
            for index, paragraph in enumerate(page['paragraphs']):
                language = page.get('paragraph_languages', {}).get(str(index), page['language'])
                node = element(div, 'p')
                if language != page['language']:
                    node.set(XML+'lang', language)
                    # Keep the whole foreign-language line, including abbreviation
                    # punctuation, in one directional span in the print stream.
                    node = element(node, 'foreign')
                    node.set(XML+'lang', language)
                words(node, paragraph, language)
        element(front, 'j:endConditional', target='#'+identifier)


def require_review(readings, reviews):
    for key, payload, _ in review_payloads(readings):
        if not review_is_current(reviews.get(key, {}), payload):
            raise ValueError('Independent canonical realization review pending or stale: '+key)
    for unit in readings['units']:
        for lang in unit['languages']:
            review = reviews.get(unit['stem']+'/'+lang, {})
            if not review_is_current(review, unit_review_text(unit, lang)):
                raise ValueError(f"Independent review pending or stale: {unit['stem']}/{lang}; use --draft for inspection")
            for index, citation in enumerate(unit.get('citations', {}).get(lang, [])):
                key = f"citation/{unit['stem']}/{lang}/{index}"
                if not review_is_current(reviews.get(key, {}), instruction_review_text(citation)):
                    raise ValueError('Independent citation review pending: '+key)
    by_identity = {unit['urn']: unit for unit in readings['units'] if unit.get('map_root', True)}
    for unit in readings['units']:
        for lang, segments in unit['languages'].items():
            for segment in segments:
                if segment.get('transclude'):
                    witness = by_identity.get(segment['transclude'])
                    text = ' '.join(fragment['text'] for fragment in segment['fragments'])
                    if not witness or lang not in witness['languages'] or text.split() != unit_text(witness, lang).split():
                        raise ValueError('Documentary transclusion review is stale: '+segment['transclude'])
    for name, navigation in readings.get('navigation', {}).items():
        for lang in navigation['scan']:
            key = 'navigation/'+name+'/'+lang
            if not review_is_current(reviews.get(key, {}), navigation['raw']):
                raise ValueError(f'Independent navigation review pending or stale: {key}')
    for name, instruction in readings.get('documentary_instructions', {}).items():
        key = 'instruction/'+name
        if not review_is_current(reviews.get(key, {}), instruction_review_text(instruction)):
            raise ValueError('Independent instruction review pending or stale: '+key)


def documentary_order(div, order, readings, by_stem, lang, project):
    """Preserve source sections without attaching service headings to reusable prayers."""
    for occurrence in order:
        if 'section' in occurrence:
            if lang not in occurrence.get('witnesses', PROJECTS):
                continue
            if occurrence.get('file'):
                element(div, 'j:transclude', type='external', target=occurrence['corresp']+'@'+project)
                continue
            section = element(div, 'div')
            if occurrence.get('corresp'):
                section.set('corresp', occurrence['corresp'])
            conditions = occurrence.get('conditions', [])
            if conditions:
                identifier = 'documentary_'+occurrence['section']+'_'+lang
                rubric_key = occurrence.get('condition_instruction', {}).get(lang)
                rubric = readings['documentary_instructions'].get(rubric_key, {})
                page_start = rubric.get('page_start', False)
                if page_start.get(lang, False) if isinstance(page_start, dict) else page_start:
                    attributes = {'ed': '1965', 'facs': page_image_url(
                        IDENTIFIER, int(rubric['scan'][1:])-1, size='')}
                    if rubric.get('printed_page') is not None:
                        attributes['n'] = rubric['printed_page']
                    element(section, 'pb', **attributes)
                condition = element(section, 'j:conditional')
                condition.set(XML+'id', identifier)
                if rubric_key:
                    note = element(condition, 'note', type='instruction')
                    note.set(XML+'lang', rubric['language'])
                    rubric_words(note, rubric, rubric['language'])
                feature_structures(element(condition, 'j:all'), conditions)
            key = occurrence['heading']
            if isinstance(key, dict):
                key = key.get(lang)
            heading = readings['documentary_instructions'].get(key)
            if heading and lang in heading['witnesses']:
                if heading.get('page_start', True):
                    attributes = {'ed': '1965'}
                    if heading.get('printed_page') is not None:
                        attributes['n'] = heading['printed_page']
                    attributes['facs'] = page_image_url(
                        IDENTIFIER, int(heading['scan'][1:])-1, size='')
                    element(section, 'pb', **attributes)
                element(section, 'head', heading['text']).set(XML+'lang', heading['language'])
            documentary_order(section, occurrence['order'], readings, by_stem, lang, project)
            if conditions:
                element(section, 'j:endConditional', target='#'+identifier)
            if not len(section) or all(child.tag in (f'{{{J}}}conditional', f'{{{J}}}endConditional')
                                       for child in section):
                div.remove(section)
            for editorial in readings.get('documentary_notes', []):
                if (editorial['after_section'] == occurrence['section'] and
                        editorial['language'] == lang):
                    anchor = element(div, 'anchor')
                    anchor.set(XML+'id', editorial['anchor'])
                    notes = element(div.getroottree().getroot(), 'standOff', type='notes')
                    note = element(notes, 'note', type='commentary',
                                   target='#'+editorial['anchor'], resp=editorial['resp'])
                    note.set(XML+'lang', lang)
                    words(element(note, 'p'), editorial['text'], lang)
        elif 'instruction' in occurrence:
            instruction = readings['documentary_instructions'][occurrence['instruction']]
            if lang in instruction['witnesses']:
                facs = page_image_url(IDENTIFIER, int(instruction['scan'][1:])-1, size='')
                page_start = instruction.get('page_start', True)
                if page_start.get(lang, False) if isinstance(page_start, dict) else page_start:
                    element(div, 'pb', ed='1965', n=instruction['printed_page'], facs=facs)
                note = element(div, 'note', type=instruction.get('type', 'instruction'), facs=facs)
                note.set(XML+'lang', instruction['language'])
                rubric_words(note, instruction, instruction['language'])
        elif 'navigation' in occurrence:
            navigation = readings['navigation'][occurrence['navigation']]
            scan = navigation['scan'][lang]
            if navigation.get('page_start', True):
                element(div, 'pb', ed='1965', n=navigation['printed_page'],
                        facs=page_image_url(IDENTIFIER, int(scan[1:])-1, size=''))
            clauses = deepcopy(navigation['clauses'])
            for clause in clauses:
                if 'target' in clause:
                    clause['target'] = clause['target'].format(project=project)
            first_new_child = len(div)
            append_instruction(div, clauses)
            for child in list(div)[first_new_child:]:
                if child.tag == f'{{{TEI}}}note':
                    child.set('facs', page_image_url(
                        IDENTIFIER, int(scan[1:])-1, size=''))
        elif 'reference' in occurrence:
            # A partial translation may need separate ranges around an absent
            # verse while its source file retains the printed chapter structure.
            if lang not in occurrence.get('witnesses', PROJECTS):
                continue
            attributes = dict(occurrence['reference'])
            # The end point inherits the start point's project.
            if '@' not in attributes['target']:
                attributes['target'] += '@'+project
            element(div, 'j:transclude', type='external', **attributes)
        else:
            unit = by_stem[occurrence['unit']]
            if lang in unit['languages']:
                transclude_unit(div, unit, readings, project=project, documentary=True)


def build(source, project_directory, *, draft=False):
    readings = json.loads((source/'readings.json').read_text())
    validate_occurrences(readings)
    realization_payloads = {key: payload for key, payload, _ in review_payloads(readings)}
    reviews_path = source/'reviews.json'
    reviews = json.loads(reviews_path.read_text()) if reviews_path.exists() else {}
    front_path = source/'front.json'
    front_pages = json.loads(front_path.read_text())['pages'] if front_path.exists() else []
    if not draft:
        require_review(readings, reviews)
        for page in front_pages:
            if page['kind'] in FRONT_KINDS:
                if not review_is_current(reviews.get('front/'+page['scan'], {}), front_text(page)):
                    raise ValueError('Independent front-matter review pending: '+page['scan'])
    registry, problems = load_registry()
    if problems:
        raise ValueError('URN registry cannot be loaded cleanly')
    for unit in readings['units']:
        identities = [unit['urn']] + [s[key] for segments in unit['languages'].values()
                                     for s in segments for key in ('corresp', 'source', 'source_reference',
                                         'source_reference_corresp', 'chapter_corresp', 'transclude', 'repeat') if s.get(key)]
        for segments in unit['languages'].values():
            for segment in segments:
                identities.extend(segment[key] for key in ('canonical', 'canonical_end') if segment.get(key))
        identities.extend(unit[key] for key in ('canonical_whole', 'text_corresp') if unit.get(key))
        identities.extend(unit.get('canonical_home', {})[key] for key in ('urn','text_corresp') if unit.get('canonical_home', {}).get(key))
        if unit.get('publication_context'):
            identities.append(unit['publication_context'])
        identities.extend(unit.get('reuse', {}).values())
        identities += [citation['target'] for citations in unit.get('citations', {}).values()
                       for citation in citations if citation.get('target', '').startswith('urn:x-opensiddur:')]
        identities += [segment['repeat_cue']['corresp']
                       for segments in unit['languages'].values() for segment in segments
                       if segment.get('repeat_cue', {}).get('corresp')]
        identities += [segment['source_reference_part']['corresp']
                       for segments in unit['languages'].values() for segment in segments
                       if segment.get('source_reference_part')]
        quotations = [quotation for segments in unit['languages'].values()
                      for segment in segments for fragment in segment['fragments']
                      for owner in [fragment]+[reading for alternative in fragment.get('alternatives', [])
                                               for reading in alternative['readings'] if isinstance(reading, dict)]
                      for quotation in owner.get('quotations', [])]
        identities += [quotation[key] for quotation in quotations
                       for key in ('source_reference', 'chapter_corresp', 'source_reference_corresp')
                       if quotation.get(key)]
        identities += [quotation['source_reference_part']['corresp'] for quotation in quotations
                       if quotation.get('source_reference_part')]
        for urn in identities:
            # Numeric scripture descendants can be implicit in the registered book.
            if registry.resolve(urn) != urn:
                raise ValueError(f'Use the existing canonical URN, not its alias: {urn}')
            parsed = parse_urn(urn)
            if parsed.governed and urn not in registry.records and str(parsed.without_numeric_tail()) not in registry.records:
                raise ValueError(f'Unregistered identity: {urn}')
    def urn_strings(value):
        if isinstance(value, dict):
            for key, child in value.items():
                if key.startswith('urn:x-opensiddur:'):
                    yield key
                yield from urn_strings(child)
        elif isinstance(value, list):
            for child in value:
                yield from urn_strings(child)
        elif isinstance(value, str) and value.startswith('urn:x-opensiddur:'):
            from opensiddur.exporter.urn import split_range
            start, end = split_range(value.partition('@')[0]) or (value.partition('@')[0], None)
            yield start
            if end:
                yield end
    for urn in set(urn_strings(readings.get('wording_variants', []))) | set(urn_strings(readings.get('source_order', []))) | set(urn_strings(readings.get('expanded_order', []))) | {
            urn for unit in readings['units'] for key in ('wording_selection','conditions','citations')
            for urn in urn_strings(unit.get(key, []))}:
        parsed = parse_urn(urn)
        if registry.resolve(urn) != urn:
            raise ValueError('Use canonical identity: '+urn)
        if parsed.governed and urn not in registry.records and str(parsed.without_numeric_tail()) not in registry.records:
            raise ValueError('Unregistered realization identity: '+urn)
    documents = []
    def service_sections(order):
        for occurrence in order:
            if 'section' in occurrence:
                if occurrence.get('file'):
                    yield occurrence
                yield from service_sections(occurrence['order'])

    for lang, project in PROJECTS.items():
        root, body = document(lang, project, 'Prayerbook for the New Year — first day', ROOT_URN,
                              index=True, draft=draft)
        if front_pages:
            add_front(root, front_pages)
        div = element(body, 'div', corresp=ROOT_URN)
        by_stem = {unit['stem']: unit for unit in readings['units']}
        for section in service_sections(readings.get('source_order', [])):
            if lang not in section.get('witnesses', PROJECTS):
                continue
            heading_key = section.get('heading')
            if isinstance(heading_key, dict):
                heading_key = heading_key.get(lang)
            title = (section['titles'][lang] if section.get('titles') else
                     readings['documentary_instructions'][heading_key]['text'])
            service_root, service_body = document(lang, project, title, section['corresp'], draft=draft)
            inline_section = deepcopy(section)
            inline_section.pop('file')
            documentary_order(service_body, [inline_section], readings, by_stem, lang, project)
            documents.append((project_directory/project/(section['file']+'.xml'), service_root))
        documentary_order(div, readings.get('source_order', [{'unit': unit['stem']} for unit in readings['units']]),
                          readings, by_stem, lang, project)
        for unit in readings['units']:
            if lang in unit['languages']:
                pending = not review_is_current(reviews.get(unit['stem']+'/'+lang, {}),
                                                unit_review_text(unit, lang))
                realization_key = 'realization/'+unit['stem']+'/'+lang
                if realization_key in realization_payloads:
                    pending = pending or any(not review_is_current(reviews.get(key, {}), payload) for key, payload in realization_payloads.items())
                context_unit, home_unit = prepare_documents(unit, readings)
                documents.append((project_directory/project/(unit['stem']+'.xml'),
                                  unit_document(context_unit, lang, draft and pending)))
                if home_unit is not None:
                    documents.append((project_directory/project/(unit['canonical_home']['file']+'.xml'),
                                      unit_document(home_unit, lang, draft and pending)))
        documents.append((project_directory/project/'index.xml', root))
    root, body = document('he', EXPANDED, 'Expanded Ashkenazi Mahzor', EXPANDED_URN, index=True, draft=draft)
    for dependency in readings.get('dependencies', []):
        source_description = root.find(f'.//{{{TEI}}}sourceDesc')
        bibliography = element(source_description, 'bibl')
        element(bibliography, 'ptr', target='/'+dependency['project']+'/index#project_source_bibl')
        element(bibliography, 'note', dependency['reason'])
    if readings.get('expanded_coverage_note'):
        bibliography = root.find(f'.//{{{TEI}}}sourceDesc/{{{TEI}}}bibl')
        element(bibliography, 'note', readings['expanded_coverage_note'], type='encoding')
    add_front(root, [], expanded=True)
    div = element(body, 'div', corresp=EXPANDED_URN)
    element(div, 'head', 'מחזור אשכנז מורחב').set(XML+'lang', 'he')
    element(div, 'head', 'Expanded Ashkenazi Mahzor').set(XML+'lang', 'en')
    # The same structural sequence drives Hebrew and any English counterparts.
    order = readings.get('expanded_order', [{'unit': unit['stem']} for unit in readings['units']])
    by_stem = {unit['stem']: unit for unit in readings['units']}
    expanded_order(div, order, readings, by_stem)
    documents.append((project_directory/EXPANDED/'index.xml', root))
    corrections = source/'corrections.json'
    if corrections.exists():
        by_path = {f'{path.parent.name}/{path.name}': root for path, root in documents}
        correction_items = json.loads(corrections.read_text())['corrections']
        guarded_stems = {key.split('/')[1] for key in realization_payloads}
        guarded_stems.update(u['canonical_home']['file'] for u in readings['units'] if u.get('canonical_home'))
        if any(Path(c['file']).stem in guarded_stems for c in correction_items):
            raise ValueError('Canonical realization corrections must be part of its reviewed source data')
        apply_corrections(by_path, correction_items)
    # A language witness removed from the readings must not remain discoverable
    # through refdb merely because an earlier build wrote its file.
    obsolete = [project_directory/project/(unit['stem']+'.xml')
                for lang, project in PROJECTS.items() for unit in readings['units']
                if lang not in unit['languages']]
    obsolete += [project_directory/project/(section['file']+'.xml')
                 for lang, project in PROJECTS.items()
                 for section in service_sections(readings.get('source_order', []))
                 if lang not in section.get('witnesses', PROJECTS)]
    from .realizations import validate_generated
    validate_generated(documents, readings)
    paths_to_write = [path for path, _ in documents]
    if len(paths_to_write) != len(set(paths_to_write)):
        raise ValueError('Generated canonical home collides with another project file')
    home_manifest = source/'canonical_homes_manifest.json'
    current_homes = sorted(str((project_directory/project/(unit['canonical_home']['file']+'.xml')).relative_to(project_directory))
                           for project in PROJECTS.values() for unit in readings['units']
                           if unit.get('canonical_home') and project.rsplit('-',1)[-1] in unit['languages'])
    previous_homes = json.loads(home_manifest.read_text()) if home_manifest.exists() else []
    for relative in previous_homes:
        path = Path(relative)
        if len(path.parts) != 2 or path.parts[0] not in PROJECTS.values() or not re.fullmatch(r'[a-z0-9_]+\.xml',path.name) or path.name == 'index.xml':
            raise ValueError('Invalid prior canonical home path')
        candidate = project_directory/path
        if candidate not in paths_to_write:
            obsolete.append(candidate)
    paths = write_documents(documents, validator=validate, obsolete_paths=obsolete)
    write_if_changed(home_manifest, json.dumps(current_homes, indent=2)+'\n')
    settings_directory = project_directory.parent/'settings'
    for project, variant, parallel in [(PROJECTS['he'], 'documentary', False),
                                       (PROJECTS['he'], 'with_translation', True),
                                       (EXPANDED, 'undated', True)]:
        settings = {'description': 'First-day Rosh ha-Shanah mahzor; digitization in progress.',
                    'requires_processor': '>=0.8.0.dev0',
                    'book': {'project': project, 'file_name': 'index.xml', 'title': 'Prayerbook for the New Year — first day'},
                    'annotations': list(PROJECTS.values()) if parallel else [PROJECTS['he']],
                    'priority': {'transclusion': [project]+[p for p in PROJECTS.values() if p != project],
                                 'instructions': [project]+[p for p in PROJECTS.values() if p != project]},
                    'typography': {'instructions': {'from': 'both'}, 'line_numbers': {'enabled': False}}}
        if parallel:
            settings['parallel'] = {'projects': [PROJECTS['en']]}
        if project != EXPANDED:
            settings['electronic'] = {'day': 'none'}
        if project == EXPANDED:
            settings['readings'] = {'abbreviations': 'expanded'}
            for dependency in readings.get('dependencies', []):
                for kind in ('transclusion', 'instructions'):
                    # Hebrew dependencies precede translations even when a
                    # future English witness acquires the same prayer URN.
                    settings['priority'][kind].insert(-1, dependency['project'])
        destination = settings_directory/project/(variant+'.yaml')
        destination.parent.mkdir(parents=True, exist_ok=True)
        write_if_changed(destination, yaml.safe_dump(settings, allow_unicode=True, sort_keys=False))
    print(f'{len(paths)} validated JLPTEI files; ' + ('DRAFT review status' if draft else 'reviewed installment'))
    return paths


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root', type=Path, default=SOURCETEXTS_ROOT)
    parser.add_argument('--project-directory', type=Path, default=PROJECT_DIRECTORY)
    parser.add_argument('--draft', action='store_true')
    args = parser.parse_args(argv)
    build(args.source_root/BOOK, args.project_directory, draft=args.draft)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
