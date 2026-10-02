# Hanukkah, Megillat Hashmonaim and Purim

Source: Birnbaum, *ha-Siddur ha-Shalem* (1949), printed 709–730,
[Internet Archive n733–n754](https://archive.org/details/PhilipBirnbaumHaSiddurHaShalemTheDailyPrayerBook1949/page/n733/mode/2up).

The 22 scans were read before comparing the saved Wikisource transcriptions.
`initial_reading.json`, `hashmonaim_initial.json`, `purim_initial.json`,
`notes_initial.json`, and `rubrics.json` preserve that first reading.
`readings.json` is the corrected derivative used by the importer.
Page-turn markers inside passages retain physical boundaries independently of
verse, stanza and paragraph divisions. `page` and `en_page` are printed numbers.

`comparison_initial.json` records 224 Hebrew differences. `adjudication.json`
records the enlarged-scan decisions: 121 retained initial readings and 103
corrections (including 11 requiring a third reading). Counts by difference,
not by the number of changed combining marks:

| Difference | Initial reading retained | Reading corrected |
|---|---:|---:|
| Consonants | 9 | 32 |
| Pointing/punctuation | 112 | 71 |

Qamats/qatan-only differences follow the project’s U+05B8 convention. The
remaining decisions were checked against enlarged page images, not accepted
by similarity to familiar liturgical wording. The full comparison slices are
saved separately in `../transcription/709.txt` through `729.txt` (odd pages).
`english_comparison.json` records seven punctuation disagreements: the scan
corrects “Opposite it,” to “Opposite it” on 714 and supports the initial reading
in the other six cases. Curly quotes, Ḥ/ḥ, line wrapping, and markup were folded
for that secondary comparison.

## Structural and textual decisions

- Maoz Tzur has six Hebrew stanzas but only five English translations. The
  untranslated sixth stanza has an empty English alignment anchor, on the
  facing page 712; it is not supplied from another edition. Preserve Birnbaum’s
  wording: וקרב יום הישועה; נקם נקמת עבדיך; כי ארכה השעה;
  ואין קץ לימי רעה; והקם רועים שבעה. Both initial reading and comparison
  supplied לנו in the final line; the scan does not.
- Megillat Hashmonaim has 76 numbered Hebrew verses and an unnumbered English
  translation. Margin numbers identify verses beginning partway through a
  printed line: verse 1 includes ותקיף בממשלתו … ישמעו לו; verse 2 begins
  הוא כבש. The English boundary follows the corresponding clauses. Hebrew
  paragraphs start at 1, 6, 11, 17, 28, 37, 43, 50, 59, 65, 68, 74, 75;
  English paragraphs at 1, 6, 11, 17, 22, 28, 37, 43, 50, 59, 65, 68, 73, 75.
- This is a liturgical reading, not a biblical book: its 76 milestone URNs are
  `prayer:megillat_hashmonaim/1` through `/76`. Bounded quotations in verse 39
  carry Exodus 20:9 and 34:21 source URNs. Bracketed [לא] in verse 44 is printed
  text, not an optional recitation.
- The blessings before and after the Megillah are present; Esther itself is
  not printed on these leaves. Asher Heni’s twenty alphabetic lines are omitted
  in the morning. Shoshanat Yaakov, Arur Haman and Harvonah remain in both
  morning and evening. “On Purim morning:” is the printed starting-point
  instruction, not a morning-only condition on the following poem. Printed
  [מגנה] remains text, not a conditional.
- Seven commentary notes are retained. The Hashmonaim note beginning on 713
  continues on 714 and is joined once. Hebrew catchwords have explicit Hebrew
  language markup. The scan’s Sofrim 14:6 citation is retained rather than the
  comparison transcription’s 4:16.
- The unchanged Shehecheyanu blessing is shared with the existing festival
  text. Sheasah Nissim is shared between Hanukkah and Purim. Additional printings
  are recorded in the bibliographic scopes.

The importer sources are `build/hanukkah_purim.py`, `hanukkah_purim_data.py`, and
`notes_hanukkah_purim.py` in opensiddur-ai. Both XML projects are generated from
those sources. The book’s index continues with `siddur:chanukah` and
`siddur:purim`; the reusable Hashmonaim and poem files remain independently
addressable.
