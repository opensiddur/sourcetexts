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

## Page 6 (faces 5)

### Running head

    6        Preliminary Morning Service

**Italic**, where the Hebrew side sets its running head in plain type, and the page number
sits at the outer *left* because this is a verso. Page 5 puts its number at the outer
right. Neither side carries a running head on the page that opens the section.

### The rubrics, again italic

    When putting on the tallith:
    Meditation before putting on the tefillin

The second carries **no terminal colon**, matching the facing Hebrew page exactly. Whatever
else inverts between the two sides, the wording does not: his rubric is the same words and
the same punctuation on both pages, and only the type changes.

### The source citation uses a colon here and a comma there

    Psalm 36:8-11

Centred above the passage with the book name in italic, and separating chapter from verse
with a **colon**. Page 5 sets the same citation as `תהלים לו, ח–יא`, with a **comma**. The
separator is a property of the language the citation is set in, not of the book, and both
are his. An en dash joins the range on both sides.

## Footnote apparatus: both blocks again

As on page 4, and for the same reason — a commentary has run over from the facing Hebrew
page — the foot carries two blocks divided by their own rule.

### Upper block — commentary continued from page 5, and one new note

The long tefillin note begun on page 5 finishes here. A second note follows it, keyed by
the catchword הנני מכון, naming the meditation's source as the Siddur of Rabbi Isaiah
Horowitz (1555–1630), the של"ה.

**One sentence of that commentary decides an encoding question**: it says the tefillin are
not worn on Sabbaths and festivals, and gives the reason. That is the only place in this
unit where the restriction is stated — there is **no rubric** on pages 5–11 conditioning
the tefillin passages on the day.

So no `j:conditional` is owed for them. The passages stand unconditional, and the fact
lives in the apparatus, which is where he put it. Encoding a condition here would be a
claim the print does not make, and the reader of a compiled weekday service would not be
able to tell the difference between what Birnbaum printed and what we inferred.

### Lower block — the numbered citations

    1 Deuteronomy 6:8.   2 Deuteronomy 6:4–9; 11:13–21; Exodus 13:1–10; 11–16.

Two this page, run together on one line, book names italic, numerals superscript, and the
series restarting from 1 as it does on every page.

**Every numeric range here takes an en dash, including the one with no chapter.** Checked at
7×: `13:1–10; 11–16.`, and in the commentary block above it `Rabbi Isaiah Horowitz
(1555–1630)`. So the rule is any number, dash, number — not verse ranges only — and it holds
in the apparatus as it does in the running text. The transcription sets a hyphen throughout.

## Page 8 (faces 7)

### Running head and opening

    8        Preliminary Morning Service

Opens **mid-sentence**, continuing the tefillin meditation begun on page 6, exactly as the
facing Hebrew page 7 opens mid-sentence continuing from page 5. The two sides break at the
same place, so the page turn is one event on both and the `tei:pb` sits inside the same
`tei:p` on each side.

### The rubrics, italic as always on this side

    When placing the tefillin on the left arm:
    When placing the tefillin on the forehead:
    When winding the retsuah three times round the middle finger:

Word for word the rubrics of page 7, which sets them roman. `tefillin` and `retsuah` are
italic within these already-italic rubrics, so — as with `tallith` on pages 4 and 6 — the
term is indistinguishable here and stands out on the Hebrew page. Both sides mark it
`tei:foreign` and leave the realisation to typography.

### No heading

Neither page of this opening carries a heading: the tefillin section was headed on pages 5
and 6, and this opening is its continuation. So the unit's headings do not fall on every
opening, and a reader of the compiled text meets them where the print puts them.

## Footnote apparatus: both blocks, and a short rule between them

One commentary note, keyed `קני המנורה`, glossing the seven branches as the continents of
the earth — self-contained, no run across the opening.

Below it, **under a rule of its own that is visibly shorter than the block rule above it**,
the numbered citations:

    1 Psalm 145:16.   2 Hosea 2:21-22.

That short rule is the arrangement page 4 and page 6 also show, and it is worth stating
once: the commentary and the citations are two apparatuses, and the print separates them
typographically rather than merely by position. Two `tei:note` types, as encoded.

## Page 10 (faces 9)

Running head, number at the outer left. No heading — this opening continues the tefillin
parashiyoth begun on page 9.

**The two Torah portions are parted the same way on both sides.** Page 9's reading flagged
this as an open question, because the Wikisource text carries an editorial note observing
that Birnbaum's English divides the portions where his Hebrew does not. On the page it is
not so: the second portion begins here as a new indented paragraph with an opening
quotation mark, **no heading and no blank line** — and page 9 sets its two portions as two
paragraphs in exactly the same way.

So there is no asymmetry to encode here, and nothing like Mah Tovu's. Both sides paragraph
at the same point, and the parting needs no URN of its own to keep the columns together.

The English also paragraphs the passage at its speech boundaries, which the Hebrew does
too. The editorial note was about a different edition's practice, or about a distinction
finer than the page shows.

## Page 12 (faces 11)

### The poems are headed here and not on the facing page

    ADON OLAM
    YIGDAL

Centred, roman, letterspaced caps. **Page 11 heads neither.** The poems simply begin there,
the first word doing the work.

This is the sharpest form of the asymmetry running through the unit. Pages 3/4 and 5/6
head their sections in *different languages*; here one side heads them and the other does
not head them at all. A `tei:head` on the English side with no counterpart on the Hebrew —
which the schema permits, and which the compiled Hebrew column will simply not show.

### The poem has the same structure on both sides, set two different ways

The Hebrew page sets each line of verse as two hemistichs side by side in two columns. This
page sets each line as **two stacked lines in a single column**: twenty printed lines for
Adon Olam's ten lines of verse, and the pairs correspond one for one.

So the structure is not in dispute between the sides — Birnbaum's footnote says ten lines,
and both sides give ten lines. What differs is only how each is set: two columns there, two
stacked lines here.

That settles the encoding: a `tei:lg` of ten `tei:l` on **both** sides, each `tei:l`
holding the whole line. Splitting on the Hebrew page's column, or on this page's line
break, would give twenty lines on one side and contradict the book about itself.

## Verifying the English body text against the page

The English of the tallith and tefillin sections was authored into TEI from the
en.wikisource transcription. That is the wrong way round for this project — the page is
the evidence and a transcription is a check — so the text was verified afterwards, and
this records how, because an unverified claim is worth nothing.

**A second witness, independent of Wikisource.** The Internet Archive OCR is generated
from these page images and has no wiki layer. `LICENSE.md` §3 warns it is unusable on
*Hebrew* pages, where it reads Hebrew as Latin gibberish; on English pages it reads
correctly, so for this side it is exactly the independent check the Hebrew side gets from
the Wikisource text.

1,198 authored words were diffed against the OCR of scan pages 29-37. **966 matched
directly (80.6%).** The rest split into three kinds, and none of them turned out to be an
authoring error:

- **OCR garbling a single word** — `tlioir` for *their*, `soil` for *God*, `faculfic` for
  *faculties*, `arc` for *are*, `ful filled` for *fulfilled*. These confirm the authored
  text rather than impeaching it.
- **The alignment slipping.** One run matched the parashiyoth against page 12's
  *footnotes* — the note on Adon Olam and Yigdal — because the OCR stream carries the
  apparatus inline with the body. A diff artifact, not a difference.
- **Long runs the OCR simply failed on.** Four of these, 15 to 85 words, and they are the
  only ones that could have hidden a real error.

**Every long run was checked on the image**, and all four are on the page as authored:

| run | where | band |
|---|---|---|
| the *Supreme God* passage, 42 words | printed 8 | `8_2` |
| the betrothal verses, 37 words | printed 8 | `8_3` |
| Exodus 13:11-15, 15 and 85 words | printed 10 | `10_3` |
| the passage's last sentence | printed 12 | `12_0` |

Band `12_0` also confirms the slice boundary: ADON OLAM begins immediately after the
sentence the parashiyoth end on, so nothing was taken from the next section.

**What this does not establish.** The check is word-level and catches a wrong or missing
word. It does not catch what a reading catches — where a rubric is italic and where roman,
what the apparatus does, where a paragraph parts. Those were read off the images
separately and are recorded above, page by page.
