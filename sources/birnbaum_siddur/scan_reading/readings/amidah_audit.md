# Amidah and Havineinu scan audit

Checked 2026-09-18 against the Internet Archive images n105–n121
(printed 81–97), with n122 (printed 98) for the facing English completion.
Scope starts at Adonai sefatai and ends after Havineinu. Avinu Malkenu,
which begins below Havineinu on printed 97–98, is outside this unit.

Compared the Hebrew and English prayer bodies, printed instructions, and
footnotes with the birnbaum_scan importer and the generated Birnbaum XML.
The main prayer paragraphs and seasonal insertions were present. The
Havineinu commentary was present in the reading for 97 but had never been
included in the importer or generated apparatus.

## Coverage by opening

| Printed pages | IA leaves | Prayer text and instructions checked |
| --- | --- | --- |
| 81–82 | n105–n106 | Silent devotion and repetition rubrics; Adonai sefatai; opening of Avot |
| 83–84 | n107–n108 | Zokhrenu; Avot ending; Gevurot, rain and Ten Days additions; Kedushah through Yimlokh; Reader labels |
| 85–86 | n109–n110 | Kedushah ending and seasonal seal; Atah qadosh and seasonal seal; knowledge, repentance, forgiveness, redemption; Reader's fast-day Aneinu |
| 87–88 | n111–n112 | Healing; years and both rain-season alternatives; ingathering; justice and seasonal seal; slanderers; righteous, continuing onto 89–90 |
| 89–90 | n113–n114 | Righteous ending; Jerusalem; David; hearing prayer; Retzeh; Yaaleh veyavo with all three occasion alternatives |
| 91–92 | n115–n116 | Yaaleh veyavo ending; Modim derabbanan and its rubric; Modim; Hanukkah insertion continuing onto 93–94 |
| 93–94 | n117–n118 | Hanukkah ending; Purim insertion; Veal kulam; Ukhtov and rubric; thanksgiving seal; priestly blessing and Reader rubric |
| 95–96 | n119–n120 | Priestly blessing completion; Sim shalom and Ten Days alternative; Elohai netzor with meditation rubric; Yehi ratzon, continuing onto 97–98 |
| 97–98 | n121–n122 | Yehi ratzon ending; Hallel cross-reference (565 Hebrew / 566 English); Abridged Shemoneh Esreh heading and instruction; complete Havineinu |

## Apparatus inventory

There are 23 notes: 15 commentaries and 8 numbered scriptural citations.
Notes extending across pages are counted once.

| Printed page(s) | Note |
| --- | --- |
| 81–82 | שמונה עשרה: origin, standing posture, and list of nineteen blessings |
| 82 | Psalm 51:17 (printed citation 3) |
| 82 | אבות |
| 83 | זכרנו |
| 83 | גבורות |
| 83–84 | משיב הרוח |
| 84–85 | קדושה |
| 84 | Isaiah 6:3 (1); Ezekiel 3:12 (2); Psalm 146:10 (3) |
| 86 | אתה חונן |
| 86 | Isaiah 65:24 (1), attached to Aneinu |
| 88 | גרי הצדק |
| 89–90 | רצה |
| 90 | יעלה ויבוא |
| 92 | מודים |
| 92 | מודים דרבנן |
| 93 | ברכה המשולשת |
| 95 | אלהי נצור |
| 96 | Numbers 6:24–26 (1); Psalms 60:7; 19:15 (2) |
| 97 | הביננו: Rabbi Samuel, Berakhoth 29a, thirteen petitions, and the three opening/closing blessings |
| 98 | Malachi 3:4 (1) |

## Corrections supported by the images

- Printed 87 reads **מִטּוּבָהּ**, not מִטּוּבֶֽךָ. Corrected the Hebrew
  reading and importer. The English reads “thy goodness” and is retained.
- Printed 97's commentary catchword and later quotation read **הביננו**,
  not הבינינו. Corrected the reading and restored the complete note to
  the apparatus, including its Hebrew quotations and italic titles.
- The Shemoneh Esreh commentary reads “direction of Rabban” and “reasons
  for the number”; removed a duplicated “of” and restored the missing “r”.
  Restored the punctuation between entries 10–13 of its blessing list.
- The Retzeh commentary reads “was daily recited”; restored “daily”.
- Restored citation periods and quotation punctuation in the commentary.
- Narrowed note targets to their existing passage URNs: Avot, Zokhrenu,
  Atah gibor, Mashiv haruach, the three Kedushah verses, Aneinu, Retzeh,
  Yaaleh veyavo, Modim, and Modim derabbanan. This keeps notes on optional
  passages attached to those passages rather than entire blessings.
- The apparatus source span now ends at printed 98, where its final
  Malachi citation is printed.

The XML prayer bodies were regenerated from the importer: only the Hebrew
years blessing changed among the prayer bodies. The English apparatus was regenerated with all
23 notes. The Hallel cross-reference was inside an empty conditional, which the
compiler discarded. It is now a standalone instruction, retaining the
printed occasions and the different Hebrew/English page references.
All other rubrics and alternative prayer texts were retained.

Validation: all 59 prayer/apparatus/wrapper XML files pass schema validation; the
59 build/apparatus tests (plus 298 subtests) pass. All 23 complete note
texts survive parallel compilation exactly once.
All encoded instruction texts also survive the undecided parallel compile,
including both Hallel page references.
