# David Asher, Selichoth, 1912: scan edition

Source: https://archive.org/details/selichothdavidasher1912
Issue: https://github.com/opensiddur/opensiddur-ai/issues/207

Vallentine & Sons, London, 1912–5672 reprint of David Asher's translation, first
published in 1866. The scan is the source; OCR and independent readings are checks.
Archive metadata records its supplied scan under CC BY-SA 4.0. This encoding is
also distributed under CC BY-SA 4.0. AI-assisted reading and encoding are credited
to Codex, rather than attributed to the source translator or an OCR provider.

## Coverage and evidence

The current documentary and expanded entrypoints cover both title pages and the first seven complete days, through n99/n100, before the day-before-New-Year body heading.

The first-day documentary encoding covers both title pages (n1/n2) and the entire
first day: Hebrew n5–n51 and English n6–n52, ending at the midpage Kaddish rubric. The second day continues from the large heading on n51/n52 through the closing instruction in the middle of n59/n60, before the third-day heading. The third day continues through n67/n68, ending before the fourth-day section heading.
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
from expanded output. The third day follows in the same entrypoints.


## Third day (Archive n59–n68)

The third day covers verified printed pages 29–33. Two Archive openings are
swapped: printed 31 is n65/n66, while printed 32 is n63/n64. The logical
Hebrew order is s60, s62, s66, s64, s68; English is s61, s63, s67, s65, s69.
`third-day-scope.json` records the image-verified ordering and exact boundaries.
The fourth-day running header on the final opening does not belong to the
third-day body. Page corrections preserve real scan identities, verified
printed labels and reciprocal translation pairs independently.

`scan_reading/third-day-initial.json` is the immutable first image reading;
`scan_reading/third-day.json` supplies the adjudicated text. The separate
`third-day-proofreading.json` records the English OCR comparison and subsequent
image corrections. This is a same-assistant image review; independent Hebrew
consonant and pointing proofreading remains pending. Apparent unusual Hebrew
wording is retained without conjectural emendation. Physical English wrapping
is joined, including nine- / parts across printed 31–32.

Three independent piyyutim have shared canonical URNs and separate modules:

| File | Canonical URN |
|---|---|
| eqra_beshimkha_lehahaziq_bekha.xml | urn:x-opensiddur:text:poem:eqra_beshimkha_lehahaziq_bekha |
| taarog_eilekha_kaayal.xml | urn:x-opensiddur:text:poem:taarog_eilekha_kaayal |
| shahar_qamti.xml | urn:x-opensiddur:text:poem:shahar_qamti |

The invocation remains body text. Shahar qamti has six named stanza milestones,
four abbreviated refrains and a final cue supplying the complete opening with
its refrain. Printed Hebrew verses and English prose remain distinct. Eight
English footnotes occur at their verified anchors; the Palestine note follows
“thy poor people.” The small repeated-verse rubric on printed 31 is Hebrew-only.

`third_day.xml` is the service assembly, with a top-level day heading above
its pizmon heading. The expanded view supplies the same bounded opening,
repeated verses, three prayer pairs and concluding prayers described for day
two, omitting fulfilled instructions. Its Full Kaddish comes from Birnbaum,
selected by default settings; the scoped declaration sets `first_day=false`
and `aseret-ymei-tshuva=false`, then restores caller context. These supplied
passages are editorial additions, not readings of n59–n68.

`heading-adjudication.json` corrects the first pizmon's English running header:
“PROPITIATORY PRAYERS FOR THE FIRST DAY.” remains documentary metadata rather
than a body heading or TOC caption. The actual Hebrew פזמון remains the heading.

## Fourth day

Complete from Archive n67/n68 to n75/n76, before the next day’s body heading. Paired images establish printed order; `fourth-day-scope.json` records it. `scan_reading/fourth-day-initial.json` is immutable scan-first evidence; `fourth-day-proofreading.json` records the comparison and adjudications. This day preserves 8 English footnotes. Independent Hebrew proofreading remains pending.

- `ayeh_kol_nifleotekha.xml`: `urn:x-opensiddur:text:poem:ayeh_kol_nifleotekha`.
- `aryeh_bayaar_damiti.xml`: `urn:x-opensiddur:text:poem:aryeh_bayaar_damiti`.
- `beashmoret_haboqer.xml`: `urn:x-opensiddur:text:poem:beashmoret_haboqer`.

The expanded service replaces fulfilled opening, repeated-verse, prayer-pair and closing cues with verified Asher ranges; it supplies the unprinted Full Kaddish from the Birnbaum default projects under a day-specific false first-day/Ten-Days scope. Short refrain choices expand only this edition’s printed full refrain; the final incipit cue supplies the verified first stanza and refrain. Documentary output retains each printed cue.

## Fifth day

Complete from Archive n75/n76 to n83/n84, before the next day’s body heading. Paired images establish printed order; `fifth-day-scope.json` records it. `scan_reading/fifth-day-initial.json` is immutable scan-first evidence; `fifth-day-proofreading.json` records the comparison and adjudications. This day preserves 8 English footnotes. Independent Hebrew proofreading remains pending.

- `ein_kemidat_basar_midotekha.xml`: `urn:x-opensiddur:text:poem:ein_kemidat_basar_midotekha`.
- `im_amri_eshkeha_mar_sihi.xml`: `urn:x-opensiddur:text:poem:im_amri_eshkeha_mar_sihi`.
- `yehabbienu_tsel_yado.xml`: `urn:x-opensiddur:text:poem:yehabbienu_tsel_yado`.

The expanded service replaces fulfilled opening, repeated-verse, prayer-pair and closing cues with verified Asher ranges; it supplies the unprinted Full Kaddish from the Birnbaum default projects under a day-specific false first-day/Ten-Days scope. Short refrain choices expand only this edition’s printed full refrain; the final incipit cue supplies the verified first stanza and refrain. Documentary output retains each printed cue.

Day five prints two El Melekh/Vayaavor cues, after its first poem and after its
pizmon. No third prayer pair is supplied. Yehabbienu tsel yado retains eight
stanza alignments and the English extend-thy-grace sentence follows the ocean stanza’s short cue,
unlike its Hebrew counterpart. Each language retains its printed cue position. The mixed קרן הפוך apparatus note on
English page 38 has explicit Hebrew/English language boundaries. Physical
`sacri-` / `fices` across pages 39–40 is joined with its source-page break intact.

Hebrew poetic phrase dots retain the printed gap using a nonbreaking space; the dot stays with the preceding word when a semantic verse line wraps. Sof pasuq remains attached directly to its word. This spacing normalization leaves documentary words and punctuation unchanged.

## Sixth day

Complete from Archive n83/n84 to n91/n92, before the next day’s body heading. Paired images establish printed order; `sixth-day-scope.json` records it. `scan_reading/sixth-day-initial.json` is immutable scan-first evidence; `sixth-day-proofreading.json` records the comparison and adjudications. This day preserves 6 English footnotes. Independent Hebrew proofreading remains pending.

- `ani_yom_ira_eilekha_eqra.xml`: `urn:x-opensiddur:text:poem:ani_yom_ira_eilekha_eqra`.
- `betulat_bat_yehudah.xml`: `urn:x-opensiddur:text:poem:betulat_bat_yehudah`.
- `hoqer_hakol_vesoqer.xml`: `urn:x-opensiddur:text:poem:hoqer_hakol_vesoqer`.

The expanded service replaces fulfilled opening, repeated-verse, prayer-pair and closing cues with verified Asher ranges; it supplies the unprinted Full Kaddish from the Birnbaum default projects under a day-specific false first-day/Ten-Days scope. Short refrain choices expand only this edition’s printed full refrain; the final incipit cue supplies the verified first stanza and refrain. Documentary output retains each printed cue.

The sixth-day final Hebrew `חוקר וכו׳` repeats its first stanza and full refrain in expanded output. The English prints no corresponding opening cue: neither documentary nor expanded English invents that repetition. Following common prayers remain aligned at their shared markers.

## Seventh day

Complete from Archive n91/n92 to n99/n100, before the next day’s body heading. Paired images establish printed order; `seventh-day-scope.json` records it. `scan_reading/seventh-day-initial.json` is immutable scan-first evidence; `seventh-day-proofreading.json` records the comparison and adjudications. This day preserves 8 English footnotes. Independent Hebrew proofreading remains pending.

- `ein_teliyah_lerosh.xml`: `urn:x-opensiddur:text:poem:ein_teliyah_lerosh`.
- `al_yimat_lefanekha.xml`: `urn:x-opensiddur:text:poem:al_yimat_lefanekha`.
- `honenu_adonai_honenu.xml`: `urn:x-opensiddur:text:poem:honenu_adonai_honenu`.

The expanded service replaces fulfilled opening, repeated-verse, prayer-pair and closing cues with verified Asher ranges; it supplies the unprinted Full Kaddish from the Birnbaum default projects under a day-specific false first-day/Ten-Days scope. Short refrain choices expand only this edition’s printed full refrain; the final incipit cue supplies the verified first stanza and refrain. Documentary output retains each printed cue.

The seventh-day Hebrew repetition rubric names the refrain limits in reverse order (from נשענו till עזרנו). Documentary output retains that wording; the expanded choice uses the verified complete refrain עזרנו ... נשענו. English also prints `(Help us, &c.)` immediately after the opening full refrain: both its cue and its expansion remain at that printed position, with no corresponding Hebrew cue invented. The English printed page-47 numeral is not visible and remains unknown; page 47 and its Hebrew pairing are established separately. Both editions stop at the concluding Reader’s Kaddish cue before the large Erev Rosh Hashanah heading on n99/n100.

## Erev Rosh Hashanah (Archive n99–n184)

The complete service runs from the large body heading on printed 49 through the
Reader’s Kaddish cue on printed 91, before the Fast of Gedaliah. Both book views
now include it. Its 113 scan-reading units retain immutable initial readings,
English OCR comparisons, targeted image adjudications, and hashes of the working
readings. Independent Hebrew proofreading remains pending; the Tamid poem’s 26
numbered references remain printed markers because no explanatory text was located
in this scan. OCR differences are recorded as findings, never silently adopted.

Independent piyyutim use canonical incipit files/URNs listed in text-modules.json.
The extended El rahum wording has its own variant module and preserves the shorter
first-day reading. Hebrew poetry/litanies use verse lines and marked responses;
English prose retains the edition’s structure. The common invocation is body text.

Expanded instructions use each language’s printed target limits. Hebrew repeat
cues add the printed-52 רחמיך רבים / אל תבוא range before the verified printed-9/10 repeats; most English cues explicitly cite
those earlier ranges. The English printed-58 cue
explicitly begins at “Thy mercy is great” on 52. After the first pizmon the Hebrew
cue stops before the Daniel verses, which are printed in full on 71; English
retains its own explicit repeat of those verses. Ark opening/closing instructions
remain at their independently printed positions, including between El melekh and
Vayaavor. Fulfilled repetition instructions disappear only in the expanded view.
The two alternating Zekhor berit refrains and both final opening-stanza repetitions
are supplied from this edition’s full printed occurrences.

The final unprinted Full Kaddish uses the existing Birnbaum default fallback,
scoped with first_day=false and Ten Days of Repentance=false. Supplied passages
are editorial expansions, not printing on the cue’s source page. No Gedaliah
service, release integration, or publication is included.

The page-52 repetitions have bounded canonical prayer identities `prayer:keraham_av`
and `prayer:selichot/ki_lo_al_tsidqotenu`. The latter begins at “for we do not
presume” / כי לא על and ends at the Daniel petition’s end. The explicit English page-58 reference and its paired Hebrew cue use these
reprinted readings. Other unpaginated Hebrew cues use the verified earlier
ranges, matching the explicit English page-9/10 references.
English cues that cite pages 9/10 retain those earlier readings: page 52 prints
“Happy”, “Selah!”, and “thy own sake”, with different punctuation before “and
grant”. These differences are not silently harmonized.

Expanded repeat cues can list different petitions in Hebrew and English. Set
them as one paired prose paragraph with inline transclusions and a shared
alignment milestone for the cue; retain bounded prayer targets in the source
modules. Separate external blocks for unequal target lists can shift later
translations. Verify the compiled pairings and the page-52 translation wording
before rendering, in addition to checking passage starts in the PDF.

The poem identity and filename use `el_eloah_dalefah_eini`: אלוהַּ is
transliterated eloah. The initial-capture file was renamed without changing
its bytes; its historical internal label records the earlier naming mistake.
