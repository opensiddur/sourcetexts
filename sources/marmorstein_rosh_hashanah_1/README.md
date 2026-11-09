# Heidenheim–Marmorstein: first day of Rosh ha-Shanah, 1965

**Status: pilot review complete; the full-volume digitization remains in progress.** This contribution belongs to
[opensiddur-processor issue 214](https://github.com/opensiddur/opensiddur-processor/issues/214).
The complete source is [this 355-leaf Archive item](https://archive.org/details/mahzor-lyom-rishon-shel-rosh-hashanah-day-one-jenny-marmorstein-1965),
[also described by Open Siddur](https://opensiddur.org/?p=69112).

The book was arranged by Wolf Heidenheim and translated by Jenny Marmorstein,
published by Victor Goldschmidt, Basle, in 1965. Aharon N. Varady prepared the
scan from the HUC-JIR Klau Library copy in Cincinnati. The Archive and Open Siddur
identify their shared source as CC0 1.0 Universal; preserve those source records.

## Evidence and status

- `ia/metadata.json`, `ia/scandata.xml`, `ia/page_numbers.json`: downloaded metadata
  and machine pagination candidates. These are not image-verified page labels.
- `ia/ocr/sN.txt`: all 355 per-leaf OCR candidates, **unverified**. Never feed these
  directly to the JLPTEI builder as accepted transcription.
- `page_corrections.json`: image-verified labels, language assignments and reciprocal
  translation pairs. `pages.json` is derived; regenerate it rather than editing it.
- `primary/*.json`: immutable initial Codex image readings, before the second
  reader's answer was opened. Each file covers selected passages, not whole pages.
- `independent/pilot.json`, `independent/navigation.json`: Claude Opus 5.5 at medium
  effort, using read-only image access, with no primary transcription or OCR
  supplied. Preserve the reader's uncertainty statements. The reader sometimes
  mistakes chapter labels for pagination; those are not promoted to verified labels.
- `independent/selections.json`: the independently read spans corresponding to the
  encoded excerpts, selected from those raw readings. Running page/chapter labels
  are excluded from the prayer words. The Hodu selection ends at I Chronicles 16:36.
- `comparison.json`: differences between immutable first readings and independent
  selected readings, separating consonants/words, pointing, and whitespace.
- `adjudications.json`: decisions with reading hashes and scan evidence. Agreement
  between readers does not resolve a mark either reader explicitly found uncertain.
- `readings.json`: current image-adjudicated source for the builder, including
  explicit canonical URNs, page boundaries, source order and expanded order. Printed
  Hebrew linkage cues are excluded from accepted English prayer words; shared
  canonical milestones provide alignment. Immutable readings retain the printed cues.
  Biblical citations are separate metadata emitted as standoff citation notes.
- `reviews.json`: per-witness review records bound to the current text hash.
  Editorial exclusions record the five removed linkage cues, scan locations and
  before/after hashes without changing the independent reading evidence.
- `progress.json`: generated coverage report. An excerpt is never a completed leaf.

All images, enlarged bands, full coordinate OCR, raw process logs and generated
PDF/HTML previews remain outside Git in `output/marmorstein_rosh_hashanah_1/`.
The decoder preserves printed Divine Name spellings and their logical points.

## Pilot coverage

The pilot contains the three Torah blessings (printed pp. 4–5), Barukh She-amar
(p. 15), I Chronicles 16:8–36 from Hodu (pp. 15–16), and Psalm 24 from the
unpaginated Hebrew-only daily-psalm appendix. It also encodes the page-8 direction
to insert the Torah blessings from page 4. The English title page, copyright page, translator’s preface, and following blank
leaf have also been independently read and accounted for. The cover emblem and
Hebrew title-page signature are now resolved by the user’s exact reading:
וואלף ב"ר שמשון ז"ל איש היידנהיים. The Hodu continuation and Psalm 19
are now also encoded in both languages. Psalm 34 and the other services remain
to be transcribed.

English is present only where printed; Psalm 24 has no generated English file.
Preserve misprints such as English “convenant” in `tei:sic`, paired with the
editorial correction in `tei:corr`; never replace the printed reading silently.
Reuse existing canonical prayer and scripture URNs; edition-specific spelling or
pointing does not create a new identity.

On 2026-11-08 the user confirmed the dagesh in הבריות, no extra mark in ליראיו
(Archive n59), and the mappiq in the small parenthetical לשמה (Archive n45).
These were encoded in the first reading; the second reader had flagged uncertainty.
The confirmations are recorded in `reviews.json`. All pilot witnesses now pass
independent review with image adjudication and these human confirmations.
Six front leaves, s1–s6, are complete, including both title pages and the verified blank leaf.
Six prayer leaves, s60–s65 (the facing Hebrew/English pages 15–17), are also
complete after independent coverage checks. The other prayer witnesses remain
excerpts; images read or OCR available do not imply complete page coverage.

## Page directions and expansion

The raw instruction remains “In most communities of the German rite the benedictions
of the Torah (page 4) are inserted here.” Both language pages print it in English.
Generated documentary TEI replaces its number with an edition-qualified URN page
reference. PDF supplies the newly typeset page number; HTML supplies a link.

The expanded mahzor inserts the three blessings at that point through canonical
URNs and retains the German-rite qualification. It omits their earlier occurrence
from this pilot's expanded sequence. This demonstrates the mechanism; it is not a
complete service arrangement. No source text is copied into the expanded project.

## Reproduction

Use the companion processor branch `feat/marmorstein-rosh-hashanah-1`. Its
`specs/MARMORSTEIN_ROSH_HASHANAH_1.md` records the specification and commands.
Pass this repository's `sources/` as `--source-root` and the projects worktree's
`project/` as `--project-directory`.

`download` uses the shared paced Archive client with contact address and agent model,
checks downloaded derivative size/hash, and writes unchanged metadata/OCR only when
necessary. `download --regenerate` needs no network. `build` validates all XML before writing and requires current independent reviews
for all encoded witnesses. `--draft` is available for explicitly unreviewed work. `verify --check`
continues to fail until the whole volume is completely transcribed and reviewed.

## Hodu and Psalm 19 continuation

Romemu, Vehu Raḥum and Hoshiah et ammekha reuse the existing modules and their
22 canonical segment identities; Psalm 19 adds 15 shared verse correspondences.
Liturgical excerpt identities retain scripture sources separately. Both expanded
and documentary sequences include the new material in its printed order.

The same independent reader’s original s62–s65 image readings cover Hodu; new
blind readings of s66–s67 complete Psalm 19. Alignment/order audits and their
adjudications are in `independent/hodu_alignment.json` and
`independent/psalm_19_alignment.json`. First readings and raw comparison snapshots
remain immutable evidence, not the accepted build input.

Image adjudication records printed English “withold” and “whem”, Hebrew defective
עֹמֶדֶת, and the visible pointing of the full Divine Name. The audit reopened an
earlier Chronicles 16:35 punctuation decision: the enlarged scan shows a comma
after “salvation”; the revised decision and its history are recorded. Psalm 19’s
Hebrew chapter label and English reference are citation notes, outside prayer words.

## Obvious source errors

`corrections.json` records five located occurrences: “convenant” → “covenant”
(Chronicles 16:15 and 16:17), “withold” → “withhold” (Psalm 40:12), and
“whem” → “whom” (Psalm 144:15), and “paeons” → “paeans” (Barukh She-amar). The builder uses the shared correction utility
to emit `tei:choice/tei:sic` and `tei:corr` before schema validation. Unique
textual context prevents a correction from silently moving to another occurrence.

Accepted source words and review hashes retain exactly what the images show.
Normal exports select the corrected form by the repository default
`readings.errors: corrected`; `readings.errors: printed` selects the source form.
The defective printed Hebrew עֹמֶדֶת, archaic English and translation choices are
retained without treating them as typographic errors.

The pilot closeout also independently verifies full coverage of s60/s61 in
`independent/pilot_pages_15_coverage.json`. The Hebrew Chronicles 16:16
continuation stays in the same reference scope across s60/s62. Enlarged cover
and title-page signature readings are preserved in `primary/calligraphy.json`
and `independent/calligraphy.json`; the exact reading is now settled in
`human_pilot_confirmation.json`, including the previously unread ז"ל.

## Pilot closeout status

`pilot_acceptance.json` records completed prayer reviews, exact human adjudication
of the calligraphic signature, and the user’s successful browser visual/interactive
check. No human review gates remain. Final front-matter generation is revalidated
automatically, with each CI result recorded against its actual commit. The final processor CI passes
4,440 tests (93 skipped), with 93.55% coverage and a successful coverage upload.
The independent enlarged-image reader could confidently identify only וואלף;
that original uncertainty is retained as evidence alongside the subsequent exact
human reading. No guesses were promoted to accepted transcription.

All pilot gates are complete. Both final CI checks passed; the user resolved the
calligraphic signature and confirmed electronic layout and links. The complete
355-leaf volume remains in progress.


## Full-volume work from the beginning

The next batch starts at s7 (Archive n6, printed p. 1), after the completed six
front leaves. First image readings and blind independent readings now cover
s7–s14 (printed pp. 1–8): entrance prayers, weekday Minchah, eruv tavshilin,
festival candle lighting, and the start of Kabbalat Shabbat. See
`full_volume_work.json` for the exact intake and adjudication state. These
opening pages are sequential; they are not Hebrew/English facing counterparts.

Mah Tovu and Ashrei are accepted Hebrew-only excerpts using existing canonical
identities. No English prayer words have been supplied. Ashrei's marginal קמה
is a citation note anchored at Psalm 145:1, following its introductory verses.
The remaining s7 prayers and the s8 Half Kaddish direction remain in intake;
neither opening leaf is certified complete. The accepted pilot stays complete.

`opening_comparison.json` retains comparisons for the raw eight-leaf batch.
The additional enlarged-image readings and `opening_encoding_resolutions.json`
record the accepted excerpts' audit. A tight image crop corrected the initial
adjudication of the bet dagesh and maqaf in Mah Tovu; the superseded decision is
preserved in `primary/opening_superseded_adjudication.json`.

The expanded spine separates weekday Minchah from the first-day Rosh ha-Shanah
morning service and keeps the daily psalm in a named appendix. Existing service
and holiday settings delimit each section locally. Editorial rubrics explicitly
label the gaps. The Kaddish/Amidah, speaker alternatives, page continuations and
remaining entrance verses still need adjudication and assembly before these
sections can be accepted as complete.
