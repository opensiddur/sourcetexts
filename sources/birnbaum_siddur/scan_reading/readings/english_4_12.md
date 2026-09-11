# Printed pages 4, 6, 8, 10, 12 (English; facing 3, 5, 7, 9, 11)

The English side of the first five openings of Birkhoth ha-Shaḥar. Taken from the
en.wikisource page-by-page transcription of **this** scan — a human transcription, page
scoped, of the same file — and checked against the page images. That is a different
relationship from the Hebrew side, where the available transcription is a reconstructed
text rather than a witness to this book. `pages.json` records every one of these pages as
`usable` at quality 4.

What follows is what was verified on the image rather than taken on trust.

## Page 4 (faces 3)

### Headings, and that they are not in the same language as the facing page

    PRELIMINARY MORNING SERVICE
    PUTTING ON THE TALLITH

Both centred, roman, letterspaced caps. The facing Hebrew page heads the same two sections
בִּרְכוֹת הַשַּֽׁחַר and סֵֽדֶר עֲטִיפַת טַלִּית. **The two sides head this section in
different languages**, as Shaḥarith li-Yladim does and unlike the Amidah, where SHEMONEH
ESREH stands in English on both sides of the opening.

That is the configuration that once produced `NERDLIHC ROF REYARP GNINROM`, so both of
these must be measured in the rendered PDF from the glyphs' own x coordinates. `pdftotext`
reading order will show a reversed Latin heading as correct.

### The rubrics are italic here and roman there

    Upon entering the synagogue:
    Before putting on the tallith:

Word for word the rubrics of the facing page, and set **italic** where page 3 sets them
roman — the inversion already recorded for pages 1 and 2.

`tallith` is italic within the second, which is to say indistinguishable inside an
already-italic rubric. Page 3 sets that same word italic against its roman rubric, where
it does stand out. Same intent, two realisations; both sides encode it `tei:foreign` and
leave it to the typography.

### Mah Tovu is one paragraph on the Hebrew page and two on this one

This page sets Numbers 24:5 as a line of its own, and begins a new indented paragraph at
*By thy abundant grace I enter thy house*. Page 3 runs the whole catena together with no
break and no indentation.

**This matters for alignment and not only for the reading.** The two columns join on exact
URN equality, so the two sides pair here only if the parting the English makes is named on
both — the verse from Numbers under one URN and the Psalms catena under another. Left as
one block on one side and two on the other, the columns pair at the top of the passage and
drift for the rest of it.

The catena itself is Numbers 24:5, then Psalms 5:8, 26:8, 95:6, 69:14 — which is the
footnote's own list, not an identification made here.

### The numbered citations begin on this page

Superscript `1` after *answer me with thy saving truth*, `2` after *thou spreadest the
heavens like a curtain*, `3` in the paragraph beginning *I am enwrapping myself*. The
Hebrew page carries none: the numbered series is English-side only, which is Birnbaum's
own statement in his introduction and holds on every page read so far.

## Footnote apparatus: two blocks, each under its own rule

The foot of this page carries **both** apparatuses, stacked, and separated from each other
by a second rule. This is the first page that shows the arrangement, because it is the
first page where the commentary runs over.

### Upper block — the commentary continued from page 3

The ציצית note begun at the foot of page 3 finishes here, closing at *(Nedarim 25a)*. It
carries no catchword of its own: the catchword is on page 3, where the note began.

So a single note is set under two facing pages, and the reader follows it across the
opening. Where it broke is the 1949 compositor's measure; a rendered PDF sets to a
different measure, so the break is recorded here and is not encoded.

### Lower block — the numbered scripture citations

    1 Numbers 24:5; Psalms 5:8; 26:8; 95:6; 69:14.   2 Psalm 104:1-2.   3 Numbers 15:38.

Run together on one line rather than one per line, with the book names in italic and the
numerals superscript. Chapter and verse take a colon.

The series restarts at `1` on every page. That is a fact about the printed page, recorded
in `@n`; a PDF repaginates, so the renderer draws its own series and does not try to
reproduce the numbering.
