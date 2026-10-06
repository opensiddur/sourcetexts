# David Asher, Selichoth, 1912: scan-reading pilot

Source: https://archive.org/details/selichothdavidasher1912
Issue: https://github.com/opensiddur/opensiddur-ai/issues/207

Vallentine & Sons, London, 1912–5672 reprint of David Asher's translation, first
published in 1866. The scan is the source; OCR and independent readings are checks.
Archive metadata records its supplied scan under CC BY-SA 4.0. This encoding is
also distributed under CC BY-SA 4.0. AI-assisted reading and encoding are credited
to Codex, rather than attributed to the source translator or an OCR provider.

## Coverage and evidence

| IA leaf | Scan identity | Printed label | Pilot content |
|---|---|---|---|
| 2 | s3 | unnumbered | English title and imprint metadata |
| 23 / 24 | s24 / s25 | יא / 11 | אל מלך יושב; beginning of ויעבור |
| 25 / 26 | s26 / s27 | יב / 12 | ויעבור continuation through לכל קראיך / “call on thee” |
| 31 / 32 | s32 / s33 | טו / 15 | במוצאי מנוחה, translation, rubrics and footnote |

`ia/` retains metadata, scandata, machine page candidates and English OCR for the
pilot pages. `page_corrections.json` records image-verified labels and reciprocal
translation pairing; `pages.json` is derived from those and Archive scandata.
Unverified printed labels and languages remain null. Leaf 30 is separately verified
as English page 14 to demonstrate correction of Archive's mistaken page-1 label.
Never use a printed label as a unique key: both languages share page numbers.

Images, overlapping bands and large OCR derivatives live outside git under
`output/asher_selichot/`. All links in the page map identify the exact source leaf.

`scan_reading/` retains initial readings, the blind independent Hebrew reading,
image adjudications, corrected structured reading (`pilot.json`), documentary
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
  entrypoint follows it with external transclusions of `el_melekh_yoshev` and
  `vayaavor`, without copying their text into the poem or silently replacing the rubric.

The dependency starts precisely at אֵל מֶלֶךְ / “Omnipotent King” on page 11.
`vayaavor` starts at וַיַּעֲבֹר / “And the Eternal passed” on the same page and ends
at לְכָל־קֹרְאֶיךָ / “on thee” on page 12. It includes the source's attached
forgiveness petitions. It excludes the preceding piyyut, the following מקוה ישראל /
“The hope of Israel”, and page 12's further cross-references. No recursive expansion
of that out-of-scope material is claimed.

The page-15 English footnote “i.e. Appease thy anger and pardon our sins.” stays
attached to “mighty deed” and must render once. Mixed-language Hebrew-page rubrics
keep English text and explicit Hebrew foreign runs. Source verse stops are represented
by middle dot / colon; typographical word spacing is normalized. Prose line-end
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
without network requests. Pilot export settings are in the code repository under
`specs/asher_selichot/`, outside automatic release settings. Both PDFs are pilot
artifacts; this does not encode the whole volume.

The service heading “Asher Selichoth: first-day piyyut pilot” is editorial. Verse
lines represent the printed phrases and stops, rather than every physical wrap
of a narrow scan line. The title-page text is retained; its display typography is
reset for the pilot. Expanded phrases are selected from choices, and the added
prayers retain their own source-page links. See `scan_reading/accuracy.md` for
pointing that still deserves a stronger independent reading.
