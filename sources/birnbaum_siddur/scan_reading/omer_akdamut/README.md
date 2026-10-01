# Omer and Akdamut: printed 637–654 (Internet Archive n661–n678)

`pages.json` supplies the scan mapping. The page images were read first, with
independent Hebrew and English readers, before comparison with the mechanically
resolved Wikisource page slices. `primary_reading.md` records the initial parent
page inventory. The three `*-reading`/English files preserve the initial readings;
they are evidence of the process, not the final text. In particular, several
initial Akdamut “enlarged-crop follow-up” conclusions were overturned on review.

`final_reading.json` contains 56 Omer units (including all 49 daily formulas),
45 bilingual Akdamut pairs (90 lines), and all 16 printed apparatus notes.
Notes continued across a facing page are joined; the two Leviticus source notes
remain distinct occurrences. Introductory rubrics are encoded in callers.

The initial mechanical comparison is preserved in `omer-initial-diff.json`.
`omer-he-verdicts.json` and `akdamut-verdicts.json` preserve the second-reader
proposals with individual meteg/point decisions and crop coordinates. Their
claims were reviewed against enlarged page bands and focused crops by the parent;
they do not override the final readings. Notable parent corrections include full
בִּנְגִינוֹת, וְחַמֵּד, וְתַחֲפֵי and חֲיָל. Both candidates missed the holam in
לְתַלּוֹתֵי; the focused p649 crop (580,275,955,355), enlarged 5x, settles it.
The final comparison contains explicit remaining print/transcription differences,
including the five defective שמנה spellings. It strips numeric count labels on
both sides, not spoken words; labels are represented by daily selection rubrics.

Final Hebrew uses NFC and U+05B8 qamats, rather than importing the transcription's
qamats-qatan distinction. The comparison's built-in qamats-qatan rule alone settles
that class mechanically. Logical holam next to shin dots is retained, including
מֹשֶׁה. Each disputed meteg occurrence was inspected separately.

Both XML projects validate; the compiled proofs were read back against all 101
bilingual units. All 16 notes occur in the PDF, with the two identical source
citations counted at their separate occurrences. PDF glyph coordinates pass the
Hebrew-direction check, including its deliberately reversed control. Calendar
checks cover the Omer season and first day of Shavuot in Israel and diaspora.
The date checks uncovered and fixed the calendar adapter's use of the Omer day
within the week in place of its total day count.
