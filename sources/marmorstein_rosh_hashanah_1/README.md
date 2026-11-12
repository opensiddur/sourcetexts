# Heidenheim–Marmorstein: first day of Rosh ha-Shanah, 1965

**Status: 57 of 355 leaves accepted, through physical scan51 plus six later pilot leaves. German-rite and audience conditions are verified; no source questions remain in accepted installments. Full-volume digitization remains in progress.** This contribution belongs to
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
  reader's answer was opened. Each file states its scope; raw readings alone do not certify complete page coverage.
- `independent/pilot.json`, `independent/navigation.json`: Claude Opus 5.5 with CLI configured for medium
  effort (actual model self-reports are retained separately), using read-only image access, with no primary transcription or OCR
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
The complete opening תפלה page and all printed Minchah material through s12
are now independently reviewed, including the guideline audit. The accepted pilot stays complete.

`opening_comparison.json` retains comparisons for the raw eight-leaf batch.
The additional enlarged-image readings and `opening_encoding_resolutions.json`
record the accepted excerpts' audit. A tight image crop corrected the initial
adjudication of the bet dagesh and maqaf in Mah Tovu; the superseded decision is
preserved in `primary/opening_superseded_adjudication.json`.

The expanded spine separates weekday Minchah from the first-day Rosh ha-Shanah
morning service and keeps the daily psalm in a named appendix. Existing service
and holiday settings delimit each section locally. The work-in-progress status is recorded in the gated editorial front and
editionStmt. The printed weekday Amidah, Kedushah, both Modim columns,
closing prayers and repetition directions are complete. The expanded service
inserts canonical Kaddish references and the reader repetition locally;
material from s13 onward still requires adjudication and assembly.

Secondary review now includes the general encoding guidelines, the ODD and the URN scheme, as well as blind image reading, alignment and recitation order. Findings and follow-up are preserved in `independent/opening_minchah_guidelines*.json`. Both Modim witnesses deliberately preserve their own page-6 break at the same Archive leaf: the print has parallel columns whose continuations are separate source streams. Untranslated-page English directions are retained once, in their printed position in the Hebrew documentary project, rather than duplicated as a whole-book English parallel. Chapter numbers on excerpts provide context only; whole-chapter correspondences require a complete chapter. The opening collection has a distinct structural identity; its prayer and verse identities are reused.

Printed Rashi script is recorded as `source_script` evidence when identifying rubrics. Instructions and speaker notes have no `rend` attribute: their presentation follows reader-selected styles (user directive, 2026-11-09). Historical independent reviews retain their original file hashes; `guideline_adherence_resolutions.json` records this subsequent presentation correction.

The Birnbaum Kedushah comparison (user-approved follow-up, 2026-11-09) adds a repetition-and-minyan guard to the reusable witness and declares minyan locally in the expanded repetition. The preparatory Minchah spine is specifically Elul29 (Hebrew month6), with matching local date and ordinary-season declarations. The printed האל הקדוש remains unchanged; no unprinted Ten Days variant is inserted. `qedushah_condition_verification.json` records nine actual compiler cases, including known afternoon time/location for calendar resolution.
The structural follow-up and its guideline adherence passed independent Claude Opus 5.5 review at medium effort; see `independent/qedushah_conditions.json`. Case settings and compiled-output hashes are preserved with the runtime verification.

Kedushah speaker correction (2026-11-09): the three response labels mean **קהל וחזן**, not congregation alone. They are encoded as `קו״ח` in `abbr`, `קהל וחזן` in `expan`, and existing `instruction:role/reader_and_congregation`. The user supplied the decisive correction; the blind secondary reread still misread these tiny labels and is preserved honestly as a failed reading. Enlarged-image adjudication, superseded data and the separate markup audit are linked from `qedushah_speaker_resolutions.json`. This is a transcription correction, without sic/corr. Speaker abbreviations and expansions now both participate in the review hash, so either change requires renewed review.

## Continued opening sequence

The opening entrance prayers and weekday Minchah are complete through s12.
The next accepted batch, s13–s17 (Archive n12–n16, printed pp. 7–11), contains
bilingual eruv tavshilin and festival lights and complete Hebrew Kabbalat Shabbat.
The user confirms this edition retains both the opening Psalms and Lekhah Dodi
on RH-Shabbat, with inclusion controlled in the expanded structural spine.
Ten literal refrain cues expand to eleven complete refrains, including the
opening congregational response. Missing English remains absent.

Blind readings, enlarged adjudications, superseded decisions, frozen-file
guideline/alignment/order review and actual compiler settings checks are
recorded in the preparations_kabbalat evidence files. All eight Psalm chapters
have verified verse counts and order. There are now 23 fully transcribed and
reviewed leaves, 32 independently read leaves, and 355 leaves in total.
Continue in scan order at s18 (Archive n17, printed page 12); full-volume
acceptance remains false.

## First-night Maariv (s18–s23)

Barekhu through Ga’al Yisrael is accepted in 19 Hebrew/English files.
The edition’s Shema cantillation, enlarged letters, Yiddish role labels,
Rashi-script rubrics, citation notes and page continuations are preserved.
Existing prayer and Biblical URNs are reused. Missing English remains absent.
The shared expanded order has local quorum/service settings and no required
navigation. Exact excerpt publication URNs do not claim entire chapters.

Two frozen-file independent guideline/alignment/order audits, enlarged source
readings and the user’s source adjudications are retained. The first audit’s
incorrect intrinsic/occurrence minyan finding was withdrawn; the entire
canonical Barekhu meditation retains its existing shared extent. Single/double
pashta distinctions and meteg positions follow this print. Our inserted vav
in Chronicles16:9 has been removed as a transcription correction, with the
prior accepted hash retained. Printed page8 at s52 is confirmed directly.
Cross-module source paragraph continuity is recorded separately.

The accepted build validates 81 XML files;99 importer tests / 41 subtests and the
separate exporter character fix’s 360 tests / 199 subtests pass. Quorum/service
checks, excerpt checks and integrated PDF/HTML previews pass. Exporter fix
PR 298 is separate; merge it before dependent digitization changes.

There are 29 fully accepted leaves and 40 independent image readings out of 355.
This earlier installment is followed by the accepted s24–s25 batch below.


## Hashkivenu through Half Kaddish (s24–s25)

Seven units in Hebrew and English cover printed p.15. Existing canonical URNs
and exact Bible verse scopes are reused. Shabbat Veshamru and minyan Kaddish
are scoped in service order; the fixed Ten Days witness cannot substitute its
English into preparatory Elul29 Minchah. Birnbaum dependencies self-bind their
components, preserving their existing calendar variants. The literal חזן role
is outside the reusable first prayer-part scope. Missing translations remain absent.

Blind readings, enlarged/word crops, the human-confirmed segol in בכסה and
two independent source/guideline/alignment/order audits are retained. Final
reviewer-requested documentary no-day settings were corrected in the generator,
regression-tested and checked in serialized HTML locally. The subsequently
authorized independent settings/code review passed with no required changes;
reviewed file hashes stayed unchanged. See hashkivenu_resolutions.json.

The accepted build validates 95 XML files;102 focused tests and 41subtests pass.
Eight runtime cases and four Bible excerpt scope checks pass. There are now
31 fully accepted leaves and40independent readings out of 355. Continue at
s26 (Archive n25); whole-volume and whole-service acceptance remain false.


## Full evening Amidah (s26–s33)

The complete silent evening Amidah is accepted through the Temple prayer on
printed p.19. Fifteen modules in each language reuse existing festival composite
and prayer-part identities, keeping the earlier ordinary Minchah witnesses intact.
The shared expanded spine includes the sequence once, with local silent and
no-repetition settings. No evening Kedushah or substitute translation is supplied.

Source-parenthesized Sabbath phrases use marked conditionals within the printed
paragraphs. Their raw parentheses remain in readings.json; generated text uses
the standard conditional delimiters, and selected clauses have none. The optional
seal vav joins Israel. Rashi אם שבת. labels are instruction notes without rend.
The unspecified (מלכנו) remains literal, with no supplied English. Six full
scriptural quotations have chapter/verse milestones outside their source spans
and explicit terminators; neither an excerpt nor a repeated verse claims a new
canonical identity. Psalm 19:15 keeps its existing reference mapping and both
printed occurrences remain aligned.

Blind readings, enlarged and word-crop adjudications, human confirmations and
two frozen-file independent source/guideline/alignment/order audits are retained.
The original English “Thou has created” is encoded with sic/corr has/hast.
Human-confirmed marks include the bet dagesh in באפו, no sheva in לַייָ, and
dalet dagesh/holam plus first-nun meteg in וּפִקְדֹּנֵֽנוּ, with no fe/qof dagesh.
The reviewer’s initial low effort self-label is retained alongside the actual
medium CLI invocation; it has not been silently rewritten.

The guarded build validates 125 XML files. 104 focused tests and 41subtests,
names/features/registry/reference checks, seven new Amidah compiler cases and
six bilingual quotation-scope checks pass. The earlier eight compiler cases
also pass. All 92 earlier language files retain the same printed words and
correspondence sequence after quotation-marker placement is corrected. Final
acceptance changes only metadata in the frozen independently reviewed XML.

There are now 39 fully accepted leaves, 48 independent readings and 48 verified
page labels out of 355. Continue at scan page 34 (Archive n33). This is the full
evening Amidah, not the complete evening service or the complete volume.


A selected-day follow-up verifies every Sabbath insertion in Hebrew and English:
definite weekday removes its words and markers; definite Shabbat includes its
words without brackets or when-rubrics; an undecided setting retains the standard
markers. Fresh print compilation and the actual documentary/expanded HTML
JavaScript payloads pass, as do 208 exporter tests and 122 subtests. This is
recorded in shabbat_resolution_verification.json; no exporter or source-word
changes were needed, and no new browser/PDF visual review is claimed.

## Evening conclusion and home customs (s34–s38)

Fourteen reusable units (21 language files) cover the evening conclusion,
Sabbath passages, Mishnah Shabbat 2, study passages, Kiddush and home customs,
greetings and Aleinu. The documentary Kiddush arrangement has two separate
service files, keeping both headings together after Hebrew-only material.
The expanded order has a named home appendix and preserves the Frankfurt
custom, shared recitation and calendar/quorum choices. No absent translations
are supplied. Birnbaum supplements retain credits and licences.

Physical PDF page 35 (Archive n34) is printed p.20 and precedes physical page 34
(printed p.21) in recitation order. The 355-page PDF was recounted; all 54 cached
images match their ordinal PDF page by nearest-image comparison. Focal pages
34–36 were rendered and visually checked. Archive recompression prevents
exact RGB-byte equality. Unique Archive URLs remain the documentary anchors.

Three independent source/guideline/alignment/order audits and all human
adjudications are retained. Frankfurt’s pataḥ-alef, pointed small-type titles,
all five disputed dageshes and the final pointed שבת are confirmed. The
Mishnah pointing typo has sic/corr; raw readings preserve the print. Actual
blind differences and superseded ambiguities remain available. CLI model
metadata confirms Claude Opus 5.5; the medium invocation and differing effort
self-reports remain recorded without claiming an observable internal setting.

Accepted: 44 of 355 leaves; 53 independently read; 51 with excerpts; no pending
unit reviews. Whole-volume/service acceptance remains false. Continue at
scan 39 (Archive n38), the beginning of morning preparations.

Validation: 148 XML files, 112 importer tests / 41 subtests, naming/features/registry/
references; eight actual expanded print cases; exact selected Kiddush words
in both languages and both occurrences for weekday/Shabbat; 20 documentary
and 28 expanded marked Sabbath scopes for false/true/undecided states under
production JavaScript. The documentary headings share one aligned row.

## Morning preliminaries (s39–s43, accepted)

Nine units (sixteen language files) and four documentary service files cover
wrapping in the tallit, entrance prayers, Shaḥar Avaqeshkha, the preparatory
Psalm anthology and Yigdal. The tallit page has actual partial English
translations on the same physical leaf; its untranslated intention and final
petition stay Hebrew-only. The English linkage words are omitted from prayer
words. Source typos “Lister” and “מסדורים” retain separate sic/corr readings.

Existing canonical identities are reused; five new records are structural
contexts only. Identical Hebrew Mah Tovu reuses the earlier witness inline,
with a new documentary context/facsimile and the actual first English witness.
The second Psalm 17:6 is encoded directly with a unique occurrence milestone,
preserving “I called” beside the source Hebrew. Actual compiled rows match all
eighteen Psalm occurrences and complete Mah Tovu to their own source words.
There are no duplicate-alignment warnings or parallel-compilation failures.
The expanded sequence repeats the existing canonical Bible witness where
required; earlier s7 pointing remains its intentional canonical lookup.

Three independent source/guideline/alignment/order audits, enlarged and micro
readings, actual blind differences/hashes and all human decisions are retained.
The final audit approves the compiled row evidence. `morning_review_provenance.json`
records actual model identifiers, the medium invocation and separate effort
self-reports. No hidden effective effort is inferred. Attribution/metre,
Divine Name pointing, smudges, metegs, dalet dagesh and shuruq are settled.

Accepted: 49 of 355 leaves; 58 independently read; 58 verified labels; 56
with excerpts; no pending unit reviews. Whole-volume/service acceptance is
false. Continue at physical scan 44 (Archive n43), printed p.4.

Validation: 168 schema-valid XML files; 115 importer tests and 41 subtests;
feature/naming/registry/reference checks; nine compiled service/calendar/quorum
and original/corrected-reading cases; production JavaScript checks of marked
Sabbath scopes and morning-entry selection. All 23 final review targets differ
only in acceptance metadata; all 145 prior non-index XML files are unchanged.

Final exports: 42-page documentary PDF and 43-page expanded PDF, with matching
HTML. Fourteen affected/credit pages rendered and visually inspected. Columns,
verse/stanza alignment, complete repeated passages and credits are retained;
internal HTML anchors and final PDF references resolve. No new live-browser
review is claimed. Scan39–43 images match their physical pages in the original
355-page PDF. See `morning_*verification.json` and `morning_pdf_page_identity.json`.

## Opening morning blessings (s44–s47: documentary accepted)

Six new reusable units (twelve language files) and paired service-order files
complete printed pp.4–5: Adon Olam, washing the hands, Asher Yatzar, the three
existing Torah blessings, Numbers 6:24–26, Elu Devarim and Elohai Neshamah.
All prayer/poem/Bible identities already existed; one new service context is
structural only. Hebrew Adon Olam has ten couplets; English has twelve source
paragraphs within those same ten stanza scopes. Hebrew Elu Devarim remains
one paragraph and its English keeps two. The existing Torah words stay intact;
only the false mid-page opening pb in Laasoq is removed.

Primary/blind full-page readings, enlarged/micro/tight checks and two independent
documentary source/guideline/alignment/order audits approve the source. Raw
hashes and initial differences remain. The user confirms וְהָרַאְיוֹן with pataḥ
under resh and sheva under alef; it is preserved literally. Tight crops settle
the gimel/final-kaf/initial-bet dageshes. Actual model identifiers, medium CLI
configuration and differing effort self-reports are recorded separately.

Accepted documentary coverage: 53 of 355 leaves; 58 independently read and
image-verified labels; 56 leaves with excerpts; no pending source-unit reviews.
Whole-volume/service acceptance remains false. The next source page is scan 48.

**Expanded integration is approved.** The explicit `opensiddur:rite/german`
condition selects the order. German rite places Elohai Neshamah immediately
after Asher Yatzar and relocates the whole block of three Torah blessings,
Numbers 6:24–26 and Elu Devarim to the later p.8 insertion. Every other rite
keeps that full block between Asher Yatzar and Elohai Neshamah. Known rites
get each passage exactly once; undefined rite retains bilingual labeled
alternatives. The user supplied the exact rule. Broad Ashkenaz is independent
of the regional German feature; no generic variant switch is used.

Validation: 182 XML files pass the guarded schema build; 116 importer tests
and 41 subtests pass; naming/features/registry checks and documentary links
pass. Seventeen paired rows match exact source words, including all ten stanzas
and three Numbers verses. Both page directions link to the correct-language
Elohai Neshamah. The accepted documentary PDF is 44 pages; new pages 34–36
are rendered and visually checked, and pixel-identical to the reviewed draft.
HTML anchors and final PDF references resolve. Twenty documentary Sabbath
scopes still behave correctly under production JavaScript. All 22 review files
differ only in acceptance metadata; 163 prior non-index files are unchanged,
and the two Laasoq files change only their false initial pb. No new browser
review is claimed. Subsequent expanded-order evidence is recorded below.

## German-rite relocation in the expanded edition

Two independent expanded-order reviews approve the implementation and actual
compiled evidence. The review improvements add bilingual conditional labels
and a coverage note in the expanded source bibliography. Source words and
all 181 other XML files remain unchanged. The expanded index matches its
final independent snapshot exactly. Reviewer limitations are preserved in the
raw reports; no source/order ambiguity remains.

Eight real compiler cases verify definite German/non-German choices,
undefined rite and negative leakage into other services. Each complete
five-unit block, Elohai Neshamah, all ten Adon Olam stanzas and all three
Numbers verses are accounted for in both languages. Three production
JavaScript DOM/CSS cases check actual visibility and order, including
false-branch hiding, known-condition label hiding and undecided alternatives.
The Shabbat and broad-rite cases establish independence of the German flag;
they do not claim new Shabbat content. The Rosh-ha-Shanah Minchah case is
a negative scope test, not a new test of the Elul29 service.

211 targeted tests and 629 subtests pass; schema/features/names/references
pass. The expanded PDF is now 46 pages with matching HTML. Physical pages
34–38 and 45 were rendered and inspected for complete blocks, column layout,
bilingual labels and coverage/credits; anchors and final PDF references
resolve. The documentary 44-page PDF is unchanged. The undated expanded PDF
shows labeled alternatives; explicit rite settings select one recitation order.
No new live-browser review is claimed. Material on scans48–59 remains partial,
including gaps around the p.8 anchor. Continue source transcription at scan48.


### Accepted continuation: physical scan pages 48–51

Printed pages6–7 through Aval Anachnu are accepted. Twenty new bilingual
modules reuse existing canonical identities. All human source-image questions
are resolved and independently verified; raw initial readings and disagreements
remain in the comparison/evidence record. Original English errors use sic/corr.

The source's continuous cross-page petition preserves the existing separate
shetargilenu and gomel_chasadim extents. Audience alternatives use person/gender
symbols; the expanded spine preserves the accepted German-rite relocation.
All21new paired rows and six actual conditional/service cases pass. All222XML
files validate, and names/features/registry/references pass. Final PDF/HTML
exports are inspected and recorded in hashachar_export_verification.json.
The isolated exporter fix remains PR299, outside the digitization branch.

Accepted coverage is57of355leaves. Continue at physical scan52 (Archive n51).
The whole volume and full service are still incomplete.


### Accepted continuation: physical PDF scans52–55

Printed p8 is bilingual; pp9–10 contain Hebrew-only offerings. Five bilingual
and six Hebrew-only modules reuse existing canonical identities. The morning
Shema structural occurrence prevents substitution of the evening pointing.
Numbers28:4 crosses the source page boundary; source citations are notes.

All source questions are resolved, including the human-confirmed p8 dageshes
and Numbers accents/meteg. Independent guideline, alignment and order review,
four compiled service/rite cases, eight paired rows and electronic-link checks
pass. The239accepted XML text trees match the reviewed draft exactly.
Final accepted exports and hashes are in morning8_export_verification.json.
Coverage is61of355leaves; continue at physical PDF scan56 (Archive n55).
The whole volume and full service remain incomplete.


### Draft continuation: physical PDF scans56–59

Thirteen new Hebrew-only units fill the preparatory offerings/study sequence
through printed p14. No English is invented. Ana’s source attribution and
side-column acrostics are commentary. All eight Mishnah labels follow their
own canonical milestones so the first label survives range transclusion.

The generated252XML files validate.218targeted tests and636subtests pass.
Independent guideline, alignment and order review is approved; all human Hebrew
corrections have been independently verified. Three Shabbat branches, exact words
for all13units, labels/acrostics and actual HTML conditions/links pass. Refreshed
documentary draft PDF contains51pages and passes visual inspection after the
human corrections. The54-page expanded PDF also passes fresh visual and coordinate checks.
The earlier top-margin diagnosis was a preview-reading mistake and is retracted;
no exporter change was needed. See qorbanot_draft_export_verification.json.

Scans56,58,59 and all13recited/study modules are accepted, bringing coverage
to64of355. Scan57 remains source-glyph-uncertain solely for the German
instruction’s final glyph in פֿאָלגענדע־. Tentative ז is encoded as tei:c
cert="low"; the human-confirmed samekh in איינגעסאַלטעט is retained. There
are no unanswered human questions. Raw disagreements and superseded erroneous
proposals remain archived. Stable accepted PDFs/HTML were not overwritten.
Prior pilot scans60–65 already cover the continuation; next new primary scan66.
Whole-volume and complete-service acceptance remain false.
