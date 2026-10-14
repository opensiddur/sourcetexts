# David Asher, Selichoth, 1912: scan edition

Source: https://archive.org/details/selichothdavidasher1912
Issue: https://github.com/opensiddur/opensiddur-ai/issues/207

Vallentine & Sons, London, 1912–5672 reprint of David Asher's translation, first
published in 1866. The scan is the source; OCR and independent readings are checks.
Archive metadata records its supplied scan under CC BY-SA 4.0. This encoding is
also distributed under CC BY-SA 4.0. AI-assisted reading and encoding are credited
to Codex, rather than attributed to the source translator or an OCR provider.

## Coverage and evidence

The current documentary and expanded entrypoints cover both title pages, the first seven days, Erev Rosh Hashanah, Tzom Gedaliah, penitential days two through five, Erev Yom Kippur, the Monday fast, Thursday fast, the last Monday fast, Tenth of Tevet, Fast of Esther, Seventeenth of Tammuz, Yom Kippur Katan, and the final circumcision poem through n410 (printed204), the last page. Independent Hebrew proofreading remains pending.

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
superscripts remain unresolved printed note markers with no identified targets.
Explanatory notes are not presumed to exist. OCR differences are recorded as findings, never silently adopted.

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

## Tzom Gedaliah (n183–n208, printed 91–103)

The complete service starts at the large heading below Erev's conclusion on
n183/n184 and ends with the conclusion cue at the bottom of n207/n208.
`scan_reading/tzom-gedaliah.json` lists its 38 reading units in printed order.
`initial/` retains staged first captures, some ending mid-poem;
`assembled-first-pass/` preserves the full scan-first assembly before English OCR.
Working readings, OCR comparison, image adjudication and SHA-256 provenance remain
separate. Same-reader crop reviews are not independent Hebrew proofreading; pointing
review remains pending. Scan labels and verified language pairing are recorded
separately from Archive's candidate labels.

Each new independent piyyut is a reusable module with a source-independent incipit
URN: Az terem nimtehu, Et Adonai behimamtseo, Avelah nafshi, Amanta meaz,
Elohim ein biltekha, Tashuv terahamenu shuv, Horita derekh teshuvah,
Im afes rova haqen and Torah haqedoshah. The invocation remains body verse.
New scriptural prayer modules use their incipits; reprints of previously encoded
prayers remain at their printed service positions without duplicate canonical
identities. Hebrew is verse, English its printed prose. Cross-page words and verses
retain their facsimile breaks; discretionary line-end hyphenation is normalized.

Horita has eight shared stanza units and seven `abbr/expan` choices per language.
Each expansion uses its full opening refrain from printed 99. The English cue
between Reuben and Judah remains there; Hebrew places its cue after both examples.
There is no added concluding opening-stanza repetition. Its Hebrew-only פזמון
heading sits below the service heading, and both appear in the generated contents.

Expanded instructions transclude verified Asher ranges and disappear when fulfilled:

- Opening: Ashrei through Shomea tefillah’s final “for it is great” on page 7,
  including the Kaddish preface and Half Kaddish. The following printed Selah
  lanu is included once. The abbreviated Hebrew כי רבו citation is ambiguous;
  this editorial boundary follows the explicit English cue and adjacent reprint.
- Preliminary pair: Ki al rahamekha, El erekh apayim, preliminary Vayaavor.
  The seven later pairs use El melekh yoshev and Vayaavor.
- Four repeat cues: Hebrew includes the introductory page-52 petitions and their
  bounded ranges; English cites the earlier page-9/10 ranges. Each unequal list
  forms one shared paired prose block with inline transclusions.
- Closing repetition: Zekhor rahamekha on 16 through Mahi umasi's final
  גמירא בשביא on 23, including printed Ashamnu repetitions and intervening prayers.
- Final continuation: Makhnise rahamim through the first-day closing prayers,
  followed by Full Kaddish from Birnbaum, selected by the default export settings.
  Its scoped settings are first_day=false and Ten Days of Repentance=true;
  the caller's context is restored afterward. This supplied Kaddish is editorial,
  not text printed on the Gedaliah leaves.

The service index gate uses `opensiddur:holiday/tzom-gedalia`, with no visible
instruction for an undecided occasion. The incomplete book stays outside releases.

English printed 103 has a marginal Hebrew note, עשרה הרוגי מלכות, with no visible
matching body marker. It is retained as a commentary note attached editorially to
the final cue, and carried into the expanded view. Its original target is unknown.
The printed “Horeb” footnote says “Zion”; preserve that wording without silently
correcting it. English printed 92 has תשובה in its body and שתית in a note; both
receive explicit Hebrew language spans.

The 26 Tamid superscripts in the preceding Erev poem are unresolved printed note
markers with no identified targets. They are not established references, and no
explanatory notes are presumed to exist.

Gedaliah's `standOff` supplies an explicitly empty editorial instruction override
for `instruction:aseret_yemei_teshuvah/add`. The secondary Full Kaddish already
contains the selected Ten Days doubling, so its “During the Ten Days … add”
rubric is fulfilled and omitted. This does not remove the Reader performance cue
or change Birnbaum's source encoding. Compiler PR #232 makes instruction selection
apply to a rubric whose enclosing conditional has resolved true.

## Second penitential day: n209–n232, printed 104–115

The contiguous encoding now reaches the final conclusion cue on printed 115.
`scan_reading/penitential-second-day.json` orders 40 bilingual units; its directory
retains immutable initial captures and complete pre-OCR assemblies separately
from working readings. Comparison, adjudication and proofreading records identify
English Archive OCR provenance and hashes. Independent Hebrew proofreading is
pending, particularly rare vocabulary and damaged pointing; same-reader crop
review does not replace it. The 24 new page-map corrections record visible labels,
languages and image-verified translation pairing independently of Archive metadata.

Independent poems use these source-independent identities and matching XML stems:

| Reading ID | XML stem / `poem:` identity |
|---|---|
| shiharnukha | shiharnukha_biqshanukha_yotser_harim |
| elohai_boshti | elohai_boshti_venikhlamti_leharim_panai |
| ashem_baalei | ashem_baalei_ashmah_haqarta_miqedem |
| anahnu_hahomer | anahnu_hahomer_veatah_yotserenu |
| orkha_vaamitkha | orkha_vaamitkha_shelah |
| tohelet_yisrael | tohelet_yisrael_hesed_lo_neezav |
| bein_keseh | bein_keseh_leasor |
| el_har | el_har_hamor_givat_horiyah |
| shaarei_shamayim | shaarei_shamayim_belulei_esh_umayim |

The genuine service assembly is `penitential_second_day.xml`, identified by
`siddur:selichot/penitential_second_day`. Its repeated prayer paragraphs retain
their actual page breaks inline, without introducing duplicate canonical prayer
modules. The invocation אלהינו ואלהי אבותינו belongs to its poem's verse body.

The expanded opening supplies Ashrei, the Selichot Kaddish preface, Half Kaddish,
Lekha Adonai hatsedaqah and Shomea tefillah. As with Gedaliah, the ambiguous Hebrew
כי רבו endpoint is bounded by the explicit English “for it is great” and the
following Selah lanu reprint: supply that following prayer once. The preliminary
pair uses Ki al rahamekha, El erekh apayim and preliminary Vayaavor; seven later
pairs use El melekh and Vayaavor. All four petition cues cite page 52 in both
languages; their expansions use its bounded Rahamekha rabbim, Keraham av and
Ki lo al tsidqotenu modules, paired inline at a shared milestone.

The closing repetition supplies Zekhor rahamekha through Mahi umasi (גמירא בשביא,
printed 23). The final continuation supplies Makhnise rahamim onward and Full
Kaddish, without repeating Mahi. The unprinted Full Kaddish uses the configured
Birnbaum fallback under first_day=false / Ten Days=true, restoring caller context
afterward. Fulfilled “say,” “repeat,” and secondary “add” instructions are omitted.

Bein keseh le'asor has seven shared units and its opening spans printed 111–112.
Its complete opening is the verified refrain expansion. Seven Hebrew and six
English abbreviation choices preserve the Hebrew-only internal cue between the
surety and supplication passages. The final Hebrew cue includes וכו׳. Shaarei
shamayim is verse with terminal ותעל תפלתם refrains; its English explanatory note
calls the gates seven although the text enumerates eight. Preserve that edition
wording and all 21 English notes, including explicit Hebrew spans in the body and
apparatus. Dots and terminal stops use the documented nonbreaking normalization.

### Half Kaddish during the Ten Days

The printed page-3 Half Kaddish (Archive n7, scan s8) has one לְעֵלָּא; its
scan-first reading remains unchanged. Following the user's 2026-10-09 correction,
the shared module supplies a second לְעֵלָּא conditionally during the Ten Days of
Repentance. This is a documented editorial seasonal addition, not text printed
on that leaf. The existing מִן כָּל wording is retained. Earlier services explicitly
use Ten Days=false; Gedaliah and the second penitential day's expanded openings
use Ten Days=true. Scope endings restore the caller's settings. Documentary
verification excludes this addition while checking the original printed reading.

### Third penitential day (n233–n258)

The third day occupies printed 116–128, ending above the fourth-day heading on
n257/n258. Nine independent poems use source-independent incipit URNs and files;
אלהינו ואלהי אבותינו remains part of each introducing poem, where printed.
The two service entrypoints share those modules and retain the top-level day
heading above the pizmon heading.

The opening repeats Ashrei through Shomea tefillah, before the following printed
Selah lanu. Four petition cues repeat the bounded passages on printed 52 in both
languages. Closing repetition includes Mahi umasi, then the separately printed
Shevat hakisse; final continuation begins Makhnise rahamim. Expanded output omits
fulfilled instructions and supplies Full Kaddish from the configured secondary
edition, with first_day=false and Ten Days=true. The opening Half Kaddish also
selects the documented seasonal addition.

Shemaenu selihati has six shared semantic alignment units. Hebrew prints a cue
between the lily and dove stanzas that English joins without a cue. It also ends
with a cue to repeat the entire opening, absent in English. Hebrew therefore has
six abbreviation choices, English four; full printed refrains remain full.
Expansions use this edition's own opening and refrain. English printed citations
“Gen. xxxviii. 17” and “Gen. ix. 9” remain documentary readings.

`penitential-third-day*` records scan-first captures, a complete pre-OCR snapshot,
English OCR candidates, provenance, hashes and adjudication. Independent Hebrew
proofreading remains pending, particularly for pointing and rare vocabulary.

### Fourth penitential day

The complete service occupies n257–n282 (printed 128–140), beginning below the
third-day conclusion and ending before the fifth-day body heading. Independent
piyyutim use incipit filenames and canonical poem URNs: eshet_neurim_haahuvah,
atah_elohai_malki_miqqedem, adonai_elohei_yisrael_atah_tsaddiq,
eleikha_adonai_shivaati, elohim_adonai_heli_yotseri_umeholeli,
amarnu_nigzarnu_lanu_veein_doresh, yoshev_beseter_elyon_magenni_vetsinnati,
ezrahi_meever_hannahar, and melekh_melakhim_veram_al_ramim.

Yoshev beseter pairs eight semantic stanzas. Six short cues in each language
expand the opening's verified full refrain; the final cue in each language
repeats the complete opening. The final full English refrain's distinct “given
to me” wording and exclamation remain printed text. The printed-130 repeat
starts with Enter not into judgment: the nested prayer range
`selichot/rahamekha_rabbim/al_tavo` excludes the mercy verse already printed
there. Remaining petition cues use the full printed-52 ranges. Opening,
closing repetition and conclusion limits match the third penitential day;
both supplied Kaddishes use scoped Ten Days context. Fulfilled cues are omitted
in the expanded view. The secondary Full Kaddish remains attributed to Birnbaum.

Immutable first captures, complete pre-OCR snapshots, independent English OCR
candidates and image adjudication accompany the readings. Hebrew awaits an
independent reader. English printed 133 ends “ardent pass” and printed 134 begins
“Support my soul”; no completion is visible. Preserve this apparent printing
truncation in the documentary text and record its uncertainty separately.

### Fifth penitential day

Complete from the large heading on n281/n282 (printed 140) through the conclusion
cue on n307/n308 (printed 153 upper). The Erev Yom Kippur heading and following
text are outside this service. The ten independent poem modules use incipit
filenames and canonical poem URNs: am_adonai_hizqu_venithazzaqah,
atah_haroeh_beelbon_neelamim, oznekha_hatteh_vehaqshev_leheqer_ranen,
teshuvah_hashuvah_qedumah_meaz_lehetiv, atah_helqi_vetsur_levavi,
omets_yosif_tahor_yadayim, azon_tehin_vehasqat_atirah,
ezkerah_elohim_veehemayah, ahavat_oz_vetoqef_hafekh, and
miqveh_yisrael_moshio_beet_tsarah.

Ezkerah has five shared semantic units. Its thirteen-attributes opening continues
across printed 149–150, ending with “take us for thy heritage” / ונחלתנו. The
single final cue in each language expands this complete opening. There are no
other refrain choices and no printed repetition instruction. Keep the full
printed opening as text and the Hebrew-only פזמון as a subordinate heading.
Five paired petition expansions refer to the complete bounded printed-52 mercy,
judgment, father and Daniel passages. Opening and conclusion boundaries follow
the preceding penitential days; both supplied Kaddishes use scoped Ten Days
context and the Birnbaum Full Kaddish fallback. Fulfilled cues disappear in the
expanded view. The closing repetition ends at Mahi umasi before Miqveh Yisrael;
the final continuation begins Makhnise rahamim.

Source evidence retains immutable first captures and complete pre-OCR snapshots.
English Archive OCR provides independent comparison candidates. Image adjudication
retains the apparent “recited has thirteen attributes” printing error on 147,
and its prayer-pair citation 12, 11. Mixed Hebrew/English footnotes retain their
language direction. Independent Hebrew proofreading remains pending.

## Erev Yom Kippur — n307–n320

Complete bilingual scan readings cover printed 153 lower through 159 upper,
ending at the Reader’s Kaddish before the Second Fast body heading. The later
running header on the closing page belongs to the following service. Evidence is
in `scan_reading/erev-yom-kippur.json`, its named unit files, immutable `initial/`
captures and complete `assembled-preocr/` snapshots. `erev-yom-kippur-proofreading.json`
records hashes; `erev-yom-kippur-ocr-comparison.json` and
`erev-yom-kippur-adjudication.json` record English OCR provenance and image review.
Independent Hebrew proofreading remains pending.

| Reading | Independent module / canonical identity |
|---|---|
| adon_befaqdekha | `adon_befaqdekha_enosh_labbeqarim.xml`, `poem:adon_befaqdekha_enosh_labbeqarim` |
| adon_din | `adon_din_im_yeduqdaq.xml`, `poem:adon_din_im_yeduqdaq` |
| yertseh_tsom | `yertseh_tsom_ammekha.xml`, `poem:yertseh_tsom_ammekha` |

The `erev_yom_kippur.xml` service assembles these modules and the edition’s
reprinted prayers. Yertseh has seven shared stanza units and full printed refrains;
preserve their “this”/“that” and Hebrew orthographic variants. Only the final cue
expands its complete first stanza. The Hebrew-only פזמון stays subordinate to the
bilingual day heading. Common prayers retain their existing canonical identities
when referenced; reprints retain their own source positions within the service.

The opening instructions conflict: Hebrew specifies Ashrei through Shomea tefillah,
while English starts “for thou hearest prayer,” citing page 2, and ends “for it is
great,” citing page 7. The first phrase actually occurs at the end of Lekha Adonai
on printed 4. Expanded output editorially follows the complete Hebrew preliminary
range through Shomea tefillah, excluding the immediately following Selah lanu
reprint. Both documentary cues remain; the unexplained raised mark after English
7 is retained as `ᶜ` pending clarification. This resolution is editorial, not a
claim that both cues prescribe identical ranges.

Three normal prayer-pair cues transclude El melekh and Vayaavor; one petition cue
uses the bounded printed-52 mercy/judgment, father/mercy and Daniel ranges. The
preliminary pair and closing confession/petitions are printed here in full. The
final cue supplies only canonical `prayer:kaddish/shalem` from Birnbaum via default
settings, with first_day=false and Ten Days=true, retaining the Reader role.
Fulfilled instructions disappear; no unrequested Makhnise rahamim conclusion is
inserted. The opening Half Kaddish also uses the seasonal doubled leela editorial
reading. Discretionary page-spanning English Par-/don and trans-/gression are joined;
immutable captures retain the visible hyphens.

## Monday fast (printed “Second Fast”) — n319–n336

The large body heading on printed159 begins the Monday fast, Hebrew לשני;
it is the first service of the Monday–Thursday–Monday series. English Second
Fast names the weekday, not a penitential-day ordinal. The service ends above
the Thursday/Fifth Fast body heading on printed167. Its final Ezekiel footnote
belongs to Monday even though it is printed below Thursday's opening text.

The bilingual service `monday_fast.xml` directly references three independent
piyyutim with source-independent canonical poem URNs and matching filenames:
`yisrael_ammekha_tehinnah_orkhim`, `elohim_beyisrael_gadol_nodata`, and
`malakhei_rahamim_meshartei_elyon`. Hebrew is verse; English keeps printed prose.
Malakhei rahamim has eight shared stanza units. Six short Hebrew אולי יחום cues
and six English “Perchance, &c.” cues expand the verified opening refrain.
Only Hebrew prints the final full refrain and a מלאכי opening-repeat cue.
Do not supply unprinted English counterparts. Keep the printed פזמון below
the service heading, and omit the fulfilled repetition instruction in expansion.

Three prayer-pair cues expand El melekh and Vayaavor from this edition. The
petition cue after Nissa levavenu follows Hebrew's printed-52 father/Daniel
ranges, while English explicitly cites earlier pages9/10 and uses their bounded
`adonai_boqer_tishma_qoli/repeat` and `hateh_elohai_oznekha/repeat` targets.
The opening and concluding weekday Amidah/usual-service/Torah instructions remain
in both views because those prescribed services are not supplied. There is no
immediate Full Kaddish Titkabel expansion at this ending. The printed Reader
label before Veal yeakkev has explicit English direction.

The running-order gate combines native Monday (`hebrew-day=2`) with an explicit
`asher:occasion/monday_fast=true` selector. This selector means the first Monday
of the book's Monday–Thursday–Monday fast series; the calendar does not yet derive
that series. Unknown occasion settings keep the section available in the book.

Evidence is in `scan_reading/monday-fast.json`, immutable initial captures and
assembled pre-OCR snapshots, and the Monday proofreading, OCR-comparison and
adjudication records. Fifteen English notes retain their printed anchors and
citations, including the apparent Isaiah vi.7 error for the quotation of56:7.
English OCR is independent comparison evidence; Hebrew independent proofreading
remains pending. Page-spanning omni-/potent and congre-/gation are joined.

The conclusion has blank Hebrew Torah/haftarah page fields. English claims the
readings occur at volume end, but image inspection of s408–s411 shows the volume
ends with the circumcision pizmon, printed204, and contains no such final reading.
Preserve the documentary claim and record it as unresolved; no dangling target
URN is introduced for an absent passage.

### Thursday fast, n335–n342

The Fifth Fast is Hebrew לחמישי, Thursday of the Monday–Thursday–Monday series.
Its body starts below Monday's concluding rubric on printed167 and ends before
Last of the Three Fasts on printed171. Fifteen bilingual units preserve three
independent poems: `taanit_tsibbur_qaveu`, `anshei_amanah_avadu`, and the reprinted
`yisrael_nosha_fast_day_recension`, canonically a variant of `poem:yisrael_nosha`.
The pizmon has six shared stanzas and five choices per language (four short
refrains and one complete-opening repeat); full printed hyphenation differs.

Expanded opening supplies Monday's Selah lanu, El erekh and Vayaavor reprints.
Three prayer-pair cues supply the edition's El melekh/Vayaavor; the petition cue
uses printed52 Hebrew targets and printed9/10 English targets. The conclusion
supplies Monday's ten bounded closing units, including its retained weekday,
Torah and haftarah performance rubric. Its fourteen notes join the two Thursday
notes in expanded output. No Full Kaddish is added. Both weekday Amidah rubrics
remain because a whole Amidah is not supplied. The documentary final pair cue's
“pp. 1, 12.” and the apparent “repeated y” printing are preserved.

Evidence: `thursday-fast-proofreading.json`, frozen English OCR comparison,
immutable first/assembled readings and image adjudications. The petition reading
was renamed to `verses_after_hoshiah`; immutable evidence keeps its original
identifier and bytes. Independent Hebrew proofreading remains pending. Occasion:
`asher:occasion/thursday_fast=true` together with native Hebrew weekday5.


## Last Monday fast, n343–n350

The Last of the Three Fasts is the final Monday of BeHaB, gated on the explicit
last_monday_fast occasion and native weekday two. Its three independent poems
are Afafunu mayim, Ozon tahan vehasket atirah, and the fast-day recension of
Ezkerah elohim veehemayah. The latter has a prose Thirteen Attributes opening
and four verse stanza units, including a Hebrew verse crossing printed173/174.
Only its concluding opening cue expands; no extra repeat instruction is printed.
The Hebrew petition-repeat cue on printed172 has no English counterpart. Its
expanded correspondence is paired with an empty English unit, preserving this
asymmetry without adding unprinted English text. Opening and closing ranges
repeat Monday; unsupplied weekday-service instructions remain, with no Full
Kaddish insertion. Documentary English has one note; expanded English inherits
fourteen additional Monday notes. Immutable captures, assembled pre-OCR snapshots,
frozen English OCR inputs and image corrections accompany all fourteen units.
Independent Hebrew proofreading remains pending.


## Tenth of Tevet, n349–n358

The service begins below the final Monday on printed174 and ends above the Fast
of Esther on printed178. Its index gate uses the native asara-btevet holiday.
Three independent poems are Ezkerah matsoq asher qeraani, Even haroshah leiyyim
veleharishah, and Avotai ki vatehu beshem elohei tsuri. Avotai has fourteen shared
stanza units, thirteen Hebrew short cues and twelve English short cues. Each
cue expands its complete opening, as this edition instructs. No English cue is
added to the last stanza. Internal source breaks are retained, including the
English to-/wards word join. Ten English notes retain their anchors; expanded
output inherits fourteen closing notes from Monday. The opening and conclusion
repeat bounded Monday ranges; unsupplied weekday-service instructions remain,
without adding Full Kaddish. Fifteen scan readings retain immutable first captures,
assembled pre-OCR snapshots, frozen English OCR comparison inputs and image
adjudication. Independent Hebrew proofreading remains pending.


## Fast of Esther, n357–n368

Complete from printed178 lower through183 upper, with native taanit-esther gate.
Fourteen units include three independent poems: Adam bequm aleinu, Attah hael
oseh felaot, and Bematei mispar hillinu fanekha. Bematei has eight shared stanza
units; its seven Hebrew cues expand the complete opening. The English rubric
mentions repetition but the English body prints no cues: expanded English retains
one opening and receives no invented refrains. The languages cross source pages
at different places; empty counterpart fragments must not rewind facsimile order.
Only two El melekh/Vayaavor pairs are printed, after Adam and Attah. No pair is
inserted after Bematei. Opening and conclusion repeat Monday ranges; unsupplied
performance instructions remain and no Full Kaddish is added. Nineteen English
notes retain exact anchors, including two mixed Hebrew/English notes. The gallows
note's inconsistent feet/yards figures and apparent citations remain as printed.
Expanded English inherits fourteen Monday conclusion notes. Immutable initial
and assembled pre-OCR captures, frozen English OCR inputs, corrections and hashes
are retained. Independent Hebrew proofreading remains pending.


## Seventeenth of Tammuz, n367–n376

Complete from printed183 lower through187, with native tzom-tammuz gate. Fourteen
bilingual units include Atanu lekhah yotser ruhot, Amar bekhi mippenei yad sheluhah,
and Sheeh neessar as independent poems. Sheeh has four shared stanza units, a
Hebrew final full-opening cue and one English short refrain cue. Preserve full
refrain variants; there is no repetition rubric. English hea-/ven spans a page
break and is joined without an editorial space. Opening and conclusion reuse
bounded Monday ranges, retaining unsupplied weekday instructions without Full
Kaddish. Expanded English inherits fourteen Monday notes in addition to thirteen
actual Tammuz notes.

English printed184 apparently interchanges superscripts2/3: the image-in-temple
sentence bears3, the city-broken-up sentence2. The encoding follows the printed
associations to apparatus3/2, despite their unexpected subject matter. Printed185
has three markers (1 tongues,2 seventh heaven,3 for Tammuz) but no apparatus text.
Preserve these as superscript markers, with no invented note targets. Provisional
note guesses in the immutable first captures were removed from working readings;
the adjudication explicitly documents that error. Esther's full-page OCR comparison
incidentally exposed the Tammuz introductory text on183 before its capture. New
poem captures and assembled snapshots precede their English OCR comparisons;
independent Hebrew proofreading remains pending.


## Yom Kippur Katan, n377–n408

The monthly service covers printed188–203 upper, before the circumcision heading.
Its occasion is selected explicitly with asher:occasion/yom_kippur_katan; no
weekday or monthly date is inferred from the inconsistent printed Psalm rubrics.
Psalm102, Psalm20, Psalm8 and the independent prayers and poems have reusable
source-independent identities and modules. Yom zeh has five shared stanza units,
Bat ammi six, and Rahmana ten. The first two have four abbreviation choices per
language; Rahmana has eight English cues and nine fully printed Hebrew responses.
The bracketed responses in Masat kappai and Samar are full verse, including the
response crossing printed193/194. The invocation is body text, never a heading.

On printed193 Hebrew places the father/Daniel repeat cue before Samar. English
interrupts the poem after “Remember the” and before “bull” on the next page.
Preserve that interleaved rubric in its independent poem module; expand its
bounded page9/10 targets at the same position. The Hebrew cue remains in service
order. First Ashamnu repeat: Hebrew uses the page200 reprint; English explicitly
cites18 and uses the original Ashamnu. The second repeat uses the reprint in both.
The two English words divided by facsimile breaks, sup-/plications and Par-/don,
are joined editorially while page evidence and frozen captures retain their breaks.

Supply the opening unnamed Kaddish as Half Kaddish, retaining Reader. The closing
Reader Kaddish cue is printed only in Hebrew; the expanded English counterpart
is editorial. Supply Full Kaddish with first_day=false and Ten Days=false.
Aleinu and Mourner Kaddish come from the Birnbaum fallback defaults, using its
existing Aleinu service identity and the canonical Mourner Kaddish identity.
Retain the Mourner role. Expanded views omit fulfilled inclusion instructions,
but retain repetitions once/twice/seven times, Ark actions, Psalm-order choices,
and unsupplied Torah/Haftara/Amidah instructions. The print claims Torah/Haftara
readings at volume end, but the last leaves contain only the circumcision poem.

Nine English notes retain printed anchors and wording. Enlarged s399 confirms
“Jer. iii. 2.” despite the quoted verse normally being numbered3; preserve that
citation. Enlarged s387 confirms “diminished from me”; initial “form” was a capture
error. Initial and assembled pre-OCR readings, English OCR input hashes and image
adjudication remain evidence. All Hebrew native-resolution bands were reviewed
by the same reader; independent Hebrew proofreading remains pending. English
full-page OCR s409 incidentally exposed the circumcision opening before its
separate first capture; record that exposure in the final section's provenance.

## Final circumcision recension, printed203 lower–204

The final heading on n407/n408 starts a separate circumcision section, ending at
n409/n410, the final printed page. Its reusable poem uses
`urn:x-opensiddur:text:poem:zekhor_berit_avraham/circumcision_recension`; the
common incipit already identifies the longer Erev Rosh Hashanah recension.
Five paired stanza units retain Hebrew verse and English printed prose. Hebrew
והשב and ושוב each expand to their different full refrain in this same recension.
English prints neither short cue; its two omissions remain omissions. Only the
fulfilled repetition rubric disappears in the expanded view. The circumcision
performance instruction remains. The English top-level display title is an
editorial label from the final-page running heading, not another printed body
heading. An explicit circumcision selector supplies its calendar gate.

The English superscript1 after flesh has no corresponding note on either final
page. Preserve it without a target or invented apparatus. The Hebrew words after the small והשב cue at the bottom of203 begin the next
stanza: `מִפִּי אוֹהֲבֶיךָ עֵד בֵּינְךָ וּבֵין`, continuing on204 with
`יְדִידֶיךָ ·`. They belong to one verse across the page break. A user correction
prompted image proofreading: the earlier working reading misread אוהביך/עד,
omitted the opening and invented דם before ידידיך. The corrected working reading
and XML restore the verse; immutable first/pre-OCR captures retain the error
for provenance. The English translation’s “blood” remains as printed.
The final pages contain no Torah/haftarah appendix requested by earlier rubrics.

First captures and pre-OCR snapshots are immutable. English s409 OCR had already
been exposed during the monthly-service comparison; this incidental exposure is
recorded. s411 was image-read before its OCR comparison. Native Hebrew rereading
by the same agent is not independent proofreading; independent proof remains
pending. Comparison findings and adjudication are committed alongside readings.


## Transcription proofreading pass

[Proofreading coverage](proofreading/README.md) records the image-only second
pass, frozen captures, comparison hashes and adjudications. Hebrew batches001–028
reach the final Hebrew page, s410/n409, with rare words and comprehensive pointing
still pending. English batches001–020 cover the title and services through Seventeenth of Tammuz, s369 lower–377 (n368–376), printed 183 lower–187; subsequent English services are pending.
These are same-model second readings with prior exposure, not independent-person
proofreading. See each ledger for exact coverage and unresolved findings.

Tammuz image proofreading corrects the reusable poem identities to `etonen_lekha_yotser_ruhot` (אתאונן לך יוצר רוחות) and `amerer_bivekhi_mippenei_yad_shalehah` (אמרר בבכי מפני יד שלחה). Historical reading IDs and immutable capture filenames remain unchanged for evidence traceability; current XML filenames and publication/alignment URNs use the corrected incipits.
