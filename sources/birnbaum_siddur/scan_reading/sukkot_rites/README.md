# Sukkot rites: IA n699–732, printed 675–708

The initial readings precede consultation of the mechanical transcription slices.
They intentionally retain errors; the corrected derivatives are the authoring inputs.

- `initial-hebrew-first.json`: Ushpizin, Lulav and Hoshanot 675–689.
- `initial-parent-reading.json`: Hoshanot 690–696.
- `initial-hebrew-last.json`: Geshem and Hakafot 697–707.
- `initial-english-reading.json`: English texts, rubrics and notes across all 34 pages.
- `sukkot-hebrew-first-corrected.json`, `sukkot-parent-corrected.json`, and
  `sukkot-hebrew-last-corrected.json`: corrected readings after individual scan checks.
- `sukkot-first-verdicts.json`, `sukkot-parent-verdicts.json`, and
  `sukkot-hebrew-last-verdicts.json`: individual differences and decisions.
- `final_reading.json`: 149 assembled text units, 47 notes and the printed rubrics.
  Cross-page text and note continuations are joined, preserving page-break markers.

References to `/tmp/` in reader reports identify the working artifacts at the time
of adjudication; their preserved equivalents are listed above. Images are the cached
IA leaves identified in `pages.json`; enlarged evidence crops are local working files.
Mechanical secondary slices are in the adjacent `transcription/` directory.

The user's first-use decision is implemented as `opensiddur:practice/lulav-first-use`,
a personal boolean with no default. Unspecified means MAYBE. Hoshanot has Hebrew body
text and English explanatory notes, not a printed English translation.

The importer is `opensiddur.importer.birnbaum_scan.build.sukkot_rites` in the matching
opensiddur-ai worktree. Build both projects with `build.build_he` and `build.build_en`;
compile `sukkot_rites.xml` using `settings_sukkot_rites.yaml` for the bilingual proof.
