# David Asher, Selichoth, 1912: scan edition

Source: https://archive.org/details/selichothdavidasher1912
Issue: https://github.com/opensiddur/opensiddur-ai/issues/207

Vallentine & Sons, London, 1912–5672 reprint of David Asher's translation, first
published in 1866. The scan is the source; OCR and independent readings are checks.
Archive metadata records its supplied scan under CC BY-SA 4.0. This encoding is
also distributed under CC BY-SA 4.0. AI-assisted reading and encoding are credited
to Codex, rather than attributed to the source translator or an OCR provider.

## Coverage and evidence

The current documentary entrypoint covers both title pages (n1/n2) and the entire
first day: Hebrew n5–n51 and English n6–n52, ending at the midpage Kaddish rubric. The second day continues from the large heading on n51/n52 through the closing instruction in the middle of n59/n60, before the third-day heading.
The following table records the refrain poem and referenced prayer ranges,
which occur at their source positions in the complete entrypoint.

| IA leaf | Scan identity | Printed label | Content |
|---|---|---|---|
| 2 | s3 | unnumbered | English title and imprint metadata |
| 23 / 24 | s24 / s25 | יא / 11 | אל מלך יושב; beginning of ויעבור |
| 25 / 26 | s26 / s27 | יב / 12 | ויעבור continuation through לכל קראיך / “call on thee” |
| 31 / 32 | s32 / s33 | טו / 15 | במוצאי מנוחה, translation, rubrics and footnote |

`ia/` retains metadata, scandata, machine page candidates and English OCR for the
encoded pages. `page_corrections.json` records image-verified labels and reciprocal
translation pairing; `pages.json` is derived from those and Archive scandata.
Unverified printed labels and languages remain null. Leaf 30 is separately verified
as English page 14 to demonstrate correction of Archive's mistaken page-1 label.
Never use a printed label as a unique key: both languages share page numbers.

Images, overlapping bands and large OCR derivatives live outside git under
`output/asher_selichot/`. All links in the page map identify the exact source leaf.

`scan_reading/` retains initial readings, the blind independent Hebrew reading,
image adjudications, corrected structured reading (`refrain-and-prayers.json`), documentary
streams, English OCR comparisons and accuracy limits. English initial errors in
“sitteth”, “unto” and a comma were corrected after returning to crops. The initial
reading is retained so corrections do not disappear from the record.

## Editorial decisions and expansions

The piyyut's Hebrew raised dots/two-dot stops delimit verse phrases, encoded as
lines within stanzas. Physical page wrapping crosses these phrases; the image is
retained as the authority for physical wrapping. English is prose and is divided
into corresponding semantic stanza slices for alignment. Running headings are not
inserted into dependency prayer text. Original word order, spelling and pointing
are retained, including תֶּרֶף, וְאַל־לַחֲטָאוֹת and defectively spelled שְׁלֹשׁ.
Points too small for full confidence are discussed in `scan_reading/accuracy.md`.

Printed refrain cues are preserved in `tei:choice/tei:abbr`. The `tei:expan`
branch supplies text verified in this same source:

- Hebrew לשמוע after stanzas 2–7 expands to the refrain printed in stanza 1:
  לִשְׁמֹעַ אֶל־הָרִנָּה וְאֶל־הַתְּפִלָּה.
- English “(Hearken, &c.)” after stanzas 3–7 expands to “to hearken unto our hymns
  of praise, and unto our supplication.” English stanza 2 prints no such cue;
  none is invented, even though the Hebrew side has one.
- The concluding במוצאי וכו׳ / “(On the outgoing, &c.)” expands to the whole
  opening stanza, as its opening words specify. The full refrain already printed
  before the Hebrew concluding cue remains printed text, not an editorial addition.
- The documentary entrypoint preserves the final “Say …” instruction. The expanded
  entrypoint replaces it with external transclusions of `el_melekh_yoshev` and
  `vayaavor`, without copying their text into the poem. The source modules retain the printed
  instruction; the expanded view omits it because the requested prayers are present.

The dependency starts precisely at אֵל מֶלֶךְ / “Omnipotent King” on page 11.
`vayaavor` starts at וַיַּעֲבֹר / “And the Eternal passed” on the same page and ends
at לְכָל־קֹרְאֶיךָ / “on thee” on page 12. It includes the source's attached
forgiveness petitions. It excludes the preceding piyyut, the following מקוה ישראל /
“The hope of Israel”, and page 12's further cross-references. No recursive expansion
of that out-of-scope material is claimed.

The page-15 English footnote “i.e. Appease thy anger and pardon our sins.” stays
attached to “mighty deed” and must render once. Mixed-language Hebrew-page rubrics
keep English text and explicit Hebrew foreign runs. Source verse stops are represented
by middle dot / U+05C3 sof pasuq (׃); typographical word spacing is normalized. Prose line-end
hyphenation is joined; lexical “long-suffering” is retained. Double-yod divine names
remain יְיָ; no substitution of the tetragrammaton is performed.

## Regeneration and checking

From the matching opensiddur-ai worktree, pass this repository's `sources` directory
and the companion opensiddur-projects worktree's `project` directory explicitly:

```bash
python -m opensiddur.importer.asher_selichot.download --source-root <sources> --contact-email <reachable-address>
python -m opensiddur.importer.asher_selichot.build --source-root <sources> --project-directory <projects>
python -m opensiddur.importer.asher_selichot.verify --source-root <sources> --project-directory <projects>
```

`download --regenerate` rebuilds the page map from cached metadata and corrections
without network requests. Export settings are in the code repository under
`specs/asher_selichot/`, outside automatic release settings. Both PDFs cover the complete first day; the rest of the volume remains pending.

Book entrypoints use the original title-page readings; no experimental heading is
added to the service. Verse lines represent printed phrases and stops rather than
physical wraps of narrow scan lines. Display typography is reset for the edition.
Expanded phrases are selected from choices, and transcluded prayers retain their
own source-page links. See `scan_reading/accuracy.md` for pointing that still needs
independent review.

In expanded output, the opening instruction to repeat the refrain is also omitted:
the refrain text is supplied in full. `asher:expansions/refrains_present` and
`asher:expansions/prayers_present` separately govern the visibility of these printed
instructions. Documentary settings declare both false; expanded settings declare
both true. Other rubrics are retained.

## Complete first-day section through n52

`first-day-scope.json` records the verified section limits: Hebrew n5–n51 and
English n6–n52, stopping after the Reader’s Kaddish instruction before the second-day
heading in the middle of the final pages. The running heading on n51 is already
“second day”; it must not be used to discard the first-day conclusion.

Both title pages (n1/n2) and the complete first day are encoded. The `index.xml`
book entrypoints include the titles and transclude `first_day.xml`, which directly
references every independent prayer and piyyut in source order and retains printed
rubrics. The named texts include Ashrei, Half Kaddish, El Melekh, Vayaavor, the
first-day selichot, Bemotzaei Menuhah, and concluding prayers.
Independent text modules occur at their original positions; there are no gaps.
The final first-day rubric is retained, without importing second-day material from
the lower half of n51/n52. The full book remains a work in progress.

`scan_reading/first-day/` preserves 66 primary reading units committed before English
OCR comparison. `first-day-continuation.json` groups complete bilingual prayers,
retaining each fragment’s original facsimile. Page-crossing paragraphs stay together;
physical English page hyphenation is joined. Hebrew poems preserve verse stops and
phrase dots, with prose English translations. `first-day-corrections.json` records
image rechecks without overwriting the initial readings. Pointing still needs an
independent Hebrew reading, especially the unusual piyyut and Aramaic vocabulary.

The continuation retains the printed footnotes, including the Eve of New Year
addition, Reader-alone direction, biblical references, and explanatory notes. The
printed “Exod. xxiii. 19.” citation on page 8 is retained as printed. English OCR and
its unresolved differences are saved separately; OCR is not evidence for Hebrew.
The final page’s OCR includes the second day, which is excluded from authored text.
No additional service expansion or editorial prayer text has been inserted into the
complete documentary entrypoint. The expanded book entrypoint shares the same text modules.

Primary readings were committed before English OCR was consulted; the immutable
`*-first-pass.json` files preserve them. `first-day-opening.json` records six
image-adjudicated English corrections. `opening-ocr-comparison.json` preserves the
initial discrepancy report, including findings still marked unresolved. The Hebrew
opening is a primary scan reading; independent checking of pointing remains pending.
`opening-documentary-streams.json` derives expected streams directly from these
readings, independently of generated XML. Mixed-language rubrics retain their
language boundaries. Psalm 145:9 crosses its facsimile page break inside the same
printed prose paragraph. Shared verse URNs provide alignment without importing
another edition’s words.

The title-page readings include Asher’s author/translator credentials and the full
imprints. The English scan appears to omit the closing quote after “Way of Faith.”;
no closing quote has been supplied. Physical prose wrapping and quotation glyph shapes
are normalized. First-page printed numbers remain unknown; the contents and a later
cross-reference disagree and neither supplies a visible printed numeral.

Use `specs/asher_selichot/first-day.yaml` in the code worktree to render this complete first-day
bilingual edition. This setting remains outside automatic release builds.

Hebrew closing punctuation in the opening is attached to the preceding word in
the normalized authoring readings and XML. Ordinary spaces before the verse-ending
marks allowed TeX to wrap them onto a separate line. The initial scan readings
retain the original spacing; this correction changes typography only.

The Hebrew two-dot verse stop is encoded as U+05C3 HEBREW PUNCTUATION SOF
PASUQ (׃), attached to its preceding word, throughout the opening and existing
reusable text modules, including expanded refrains. U+003A COLON (:) remains in English
punctuation and title-imprint punctuation. Earlier first-pass evidence is retained
unchanged, including its provisional colon representation.

## Piyyut invocations and identification

The recurring אלהינו ואלהי אבותינו and “Our God and the God of our fathers”
belong to each piyyut’s opening text, rather than headings. The Hebrew invocation
is an introductory line within the verse group; the English invocation remains
in its translated prose paragraph. The three affected poems are identified by
the distinctive incipits אין מי יקרא בצדק, אם עונינו רבו להגדיל, and
תבא לפניך שועת חנון, recorded as `incipit_he` in the continuation metadata.
These are incipit identifiers, not independently established formal titles or
added printed headings. Piyyut URNs and filenames use these distinctive incipits independently of this edition. This structural
interpretation follows the user’s correction; the primary readings and their
words remain unchanged.

## Expanded complete first day

`expanded.xml` in each project includes the title pages and transcludes the same
`first_day.xml` used by the documentary book. The poem module supplies its concluding
prayers in a conditional branch alongside the printed cue, so a separate expanded
first-day assembly is unnecessary. Compile with the code companion’s
`specs/asher_selichot/default.yaml`: it expands abbreviations and sets
`asher:expansions` flags for supplied refrains, prayers and repetitions. These
settings remain outside automatic release builds.

The following editorial transclusions replace the corresponding printed cues:

| Instruction identity | Supplied range |
|---|---|
| `after_first_selihah_rubric`, `after_second_selihah_verses` | `prayer:adonai_boqer_tishma_qoli/repeat`: כרחם אב / “Like a father hath compassion” through ביום קראנו / “when we call”; then `prayer:hateh_elohai_oznekha/repeat`: כי לא על צדקתינו / “for we do not presume” through the end of the Daniel petition, including אדני שמעה / “O Lord! hear” |
| `after_second_selihah_prayers`, `after_third_selihah_prayers` | Complete Asher `prayer:el_melekh_yoshev` and `prayer:vayaavor` |
| Piyyut conclusion on n31/n32 | The same two prayers, after the poem |
| `ashamnu_repeat`, `ashamnu_repeat_2` | Complete Asher `prayer:ashamnu`, ending ואנחנו הרשענו / “but we have done wickedly” |
| `reader_kaddish` on n51/n52 | `prayer:kaddish/shalem`, from the secondary Birnbaum 1949 projects |

The two bounded scriptural ranges start within their original prose paragraphs;
matching closing milestones prevent them from including unrelated text. The
`repeat_start` fields record bilingual range starts without altering scan readings.
The expanded view omits every fulfilled instruction while retaining general service
rubrics. The documentary view retains all printed cues and omits supplied repetitions.

Asher’s first-day leaves contain only the final Kaddish instruction, not the full
prayer. The secondary-source Full Kaddish is an editorial addition, not an Asher
reading. `default.yaml` prioritizes Asher, then Birnbaum Hebrew; the parallel column
prioritizes Asher English, then Birnbaum English. The reusable Birnbaum wrapper
includes Yitgadal, Yehe Shmeh, Yitbarakh, Titkabel, Yehe Shlama and Oseh Shalom,
using existing Birnbaum text modules, with the complete-prayer source range on
printed pages 135/136. Its internal references retain the Birnbaum edition even
when a caller prioritizes another edition. No secondary wording is copied into
Asher’s primary reading evidence.

The final Full Kaddish transclusion is scoped explicitly to first-day Selichot:
`asher:selichot/first_day=true` and
`opensiddur:holiday-aggregate/aseret-ymei-tshuva=false`. The first day is never
during the Ten Days of Repentance. This scope excludes Birnbaum’s date-dependent
extra לעילא and its explanatory rubric, even if the caller’s settings conflict.
The declaration ends after the prayer and restores the caller’s context; it does
not change Birnbaum’s reusable source text or Asher’s documentary readings.


## Text identities and book assemblies

This encoding is the foundation for the final book. `index.xml` is the documentary
book entrypoint and `expanded.xml` the expanded entrypoint. Both contain the two
title pages and reference the same first- and second-day assemblies by URN. Coverage and pending
proofreading are edition metadata, rather than part of a text's identity.

Each independent text has its own module, with the same filename and canonical
URN in both language projects. Source attribution is retained in the publication
URN's `@asher_selichot_he_1912` / `@asher_selichot_en_1912` suffix, header metadata
and facsimile links. `first_day.xml` holds the actual printed service order and rubrics; its direct
transclusions use the source-independent canonical URNs. The opening, preface,
before-piyyut and closing subdivisions were authoring batches, not printed service
divisions, and their grouping files and URNs are removed. The generator also
removes those obsolete files on regeneration after replacement XML validates.

| File | Canonical identity (after `urn:x-opensiddur:text:`) |
|---|---|
| `ashrei.xml` | `prayer:ashrei` |
| `kaddish_chatzi.xml` | `prayer:kaddish/chatzi` |
| `ein_mi_yiqra_betsedeq.xml` | `poem:ein_mi_yiqra_betsedeq` |
| `im_avoneinu_rabu_lehagdil.xml` | `poem:im_avoneinu_rabu_lehagdil` |
| `tavo_lefanekha_shavat_hinnun.xml` | `poem:tavo_lefanekha_shavat_hinnun` |
| `bemotzaei_menuhah.xml` | `poem:bemotzaei_menuhah` |
| `ashamnu.xml` | `prayer:ashamnu` |
| `shema_qolenu.xml` | `prayer:shema_qolenu` |
| `el_melekh_yoshev.xml` | `prayer:el_melekh_yoshev` |
| `vayaavor.xml` | `prayer:vayaavor` |
| `avinu_malkenu_chonenu.xml` | `prayer:avinu_malkenu/chonenu` (the single printed petition) |

[text-modules.json](text-modules.json) records the complete mapping from existing
reading IDs to the extracted modules. Existing registry names are reused for
common prayers and their parts; other names are distinctive incipits, without
asserting unverified formal titles. The preliminary Vayaavor is separately scoped
as `prayer:vayaavor/selichot_preliminary` because its attached petitions differ
from the later printed range. Biblical Psalm 6 uses `bible:psalms/6`.

The old isolated excerpt entrypoints are replaced by the book entrypoints.
`refrain-and-prayers.json` is the renamed active structured reading; immutable
first-pass evidence remains intact. Splitting modules changes neither printed
words nor the documentary/expanded decisions. Reverse verification follows the
single service assembly in source-page order and compares each module with its reading unit.

### Hebrew poetic structure

`poetry-structure.json` records a separate image-based markup adjudication for
12 previously paragraph-encoded poems and litanies: Ki al rahamekha, El erekh
apayim, Ashamnu mikol am, Leenenu, El rahum, Anenu, Mi Sheanah, Rahmana,
Mahi umasi, Makhnise rahamim, and the two Maran divishmaya poems. The source
readings and English paragraph/litany forms remain unchanged. The specified
printed phrase or verse stops delimit semantic poetic lines; this does not
interpret every raised dot throughout the service as a verse break.

Mi Sheanah (s46 / Archive n45, printed 22) has 20 lines, each with one terminal
הוא יעננו refrain. Anenu has 35 terminal עננו refrains; Rahmana has four ענינא
refrains before its changing petitions. XML uses `tei:lg`/`tei:l`, with responses
marked `tei:seg type="refrain"` inside the line, preserving their printed pointing
and attached sof pasuq. A line spanning two source pages remains one verse with
an internal facsimile page break (e.g. גלה ממנו משוש in Ashamnu mikol am).
The metadata records scan provenance, verse counts and refrain counts, so a
word-identical paragraph or a missing/displaced refrain fails verification.


## Second day (Archive n51–n60)

`second-day-scope.json` records the exact boundaries. Printed pages 25–29 pair
Hebrew n51,53,55,57,59 with English n52,54,56,58,60. The running third-day
heading on the final opening does not establish the service boundary.
`scan_reading/second-day-initial.json` retains the first image reading;
`scan_reading/second-day.json` is the adjudicated reading. The separate
`second-day-proofreading.json` records image-pass corrections and Archive English
OCR comparison provenance. Hebrew pointing still needs independent proofreading.
The English singular “God of our Father!” is retained as printed.

Four additional independent modules are shared by both language projects:
`eiyyeh_qinatkha_ugevurotekha.xml`, `ein_qore_beshimkha.xml`,
`avvitikha_qivitikha_meerets_merhaqim.xml`, and `yisrael_nosha.xml`. Each has a
source-independent incipit URN. The invocation remains body text. Hebrew verse
and English prose retain their separate structures. Israel Nosha has six named
stanza milestones, four short refrain choices, and a final choice expanding the
entire first stanza with its refrain. Seven English notes are encoded once each,
including the two separate notes printed “The three patriarchs.”

`second_day.xml` is the actual service assembly. Its printed day heading is above
the Hebrew printed פזמון heading; no unprinted English pizmon heading is invented.
The export settings generate a contents page through heading level two.
Documentary output retains all instructions. Expanded output replaces them:

- Opening: Ashrei, the Selichot Kaddish preface, Half Kaddish, Lekha Adonai,
  Shomea tefillah and Selah lanu avinu (through כי רבו עוונינו), followed by
  El erekh apayim and the preliminary Vayaavor ending ורב חסד לכל קראיך.
- The repeated verses after the first piyyut use the bounded Keraham-av repeat
  (`adonai_boqer_tishma_qoli/repeat`) and Daniel petition repeat
  (`hateh_elohai_oznekha/repeat`), not adjacent material outside those ranges.
- Three printed prayer-pair cues supply El Melekh yoshev and Vayaavor.
- The conclusion supplies the existing first-day closing prayers from Zekhor
  rahamekha, including its bounded Ashamnu repetitions, then the Full Kaddish
  selected from Birnbaum by the default expanded settings. It declares
  `first_day=false` and `aseret-ymei-tshuva=false` around that Kaddish instead of
  copying the first-day calendar declaration. The declaration closes afterward.

Supplied text is editorial expansion, not attributed to printing on n51–n60.
Fulfilled instruction text and the now-unneeded refrain instruction are omitted
from expanded output. The third day is not encoded in these entrypoints.
