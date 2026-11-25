General encoding guidelines, lines 275–370

### Recording an edition's own numbering

Two milestone units carry the two numberings, and they must not be confused:

| unit | `@corresp` | `@n` | role |
|---|---|---|---|
| `verse` | required, canonical URN | canonical number | identity, alignment, transclusion |
| `edition-verse` | **never** | the edition's own number | display only |

```xml
<!-- Miqra al pi ha-Masorah, Exodus 20. One MAM verse, four canonical verses. -->
<tei:milestone unit="edition-verse" n="12"/>
<tei:p><tei:milestone unit="verse" n="13" corresp="urn:x-opensiddur:text:bible:exodus/20/13"/>לֹא תִרְצָח</tei:p>
<tei:p><tei:milestone unit="verse" n="14" corresp="urn:x-opensiddur:text:bible:exodus/20/14"/>לֹא תִנְאָף</tei:p>
<tei:p><tei:milestone unit="verse" n="15" corresp="urn:x-opensiddur:text:bible:exodus/20/15"/>לֹא תִגְנֹב</tei:p>
<tei:p><tei:milestone unit="verse" n="16" corresp="urn:x-opensiddur:text:bible:exodus/20/16"/>לֹא תַעֲנֶה</tei:p>
<tei:milestone unit="edition-verse" n="13"/>
<tei:milestone unit="verse" n="17" corresp="urn:x-opensiddur:text:bible:exodus/20/17"/>לֹא תַחְמֹד
```

Because `edition-verse` carries no `@corresp`, the reference database and the parallel compiler — which look
only at `@corresp` — ignore it entirely. Which numbering a reader sees is a rendering choice, driven by the
`opensiddur:verse-numbering` setting.

### Rules

- **One milestone per canonical verse, exactly once per project.** A verse split across paragraphs by a
  parashah break in the middle of it is still one verse and keeps one milestone; its scope runs to the next
  verse milestone regardless of paragraph boundaries. Repeating the milestone gives the verse two identical
  `@corresp` values. Both the reference database and the parallel compiler keep only the first, drop the rest,
  and warn. A source may legitimately print the same text twice, even with different wording, so this is not an
  error; but only the first copy can be reached by its URN.
- **Never renumber to paper over a disagreement.** If an edition's verse count does not match the canonical
  one and the reason is not in the versification table, that is a defect in the importer or an unrecorded
  divergence, not something to be shifted into alignment.
- `opensiddur/exporter/validate_versification.py` checks both of these across the Tanakh projects.

### Sub-verse scope

Liturgy quotes less than a verse constantly. Kiddush opens on the second half of Genesis 1:31;
the third-year haftarah of Emor runs from Nachum 2:2b to 2:3a; the Thirteen Attributes begin
partway through Exodus 34:6 and stop partway through 34:7. A verse URN cannot say any of that,
and `tei:anchor` does not reach — anchored points have no canonical references.

Two milestone units divide a verse. Each hangs its URN one path component below the verse's, so
no new URN grammar is needed: `urn:x-opensiddur:text:bible:genesis/1/31/b` is an ordinary URN
one level deeper.

| unit | `@corresp` | `@n` | placed |
|---|---|---|---|
| `half-verse` | verse URN + `/a` or `/b` | `a` or `b` | from the accents, mechanically |
| `verse-part` | verse URN + `/<name>` | the name | from a declared table |

```xml
<tei:milestone unit="verse" n="31" corresp="urn:x-opensiddur:text:bible:genesis/1/31"/>
<tei:milestone unit="half-verse" n="a" corresp="urn:x-opensiddur:text:bible:genesis/1/31/a"/>
וַיַּרְא אֱלֹהִים אֵת כׇּל אֲשֶׁר עָשָׂה וְהִנֵּה טוֹב מְאֹ֑ד
<tei:milestone unit="half-verse" n="b" corresp="urn:x-opensiddur:text:bible:genesis/1/31/b"/>
וַיְהִי עֶרֶב וַיְהִי בֹקֶר
<tei:milestone unit="verse-part" n="yom_hashishi"
               corresp="urn:x-opensiddur:text:bible:genesis/1/31/yom_hashishi"/>
יוֹם הַשִּׁשִּׁי׃
```

**A half-verse is the accentual division of the verse**, at the etnachta: `a` from the head of
the verse to the accent inclusive, `b` from the next word to the end. This is what a citation
means by "2:2b", and because it is read off the text it needs no curation — every accented
Hebrew Tanakh project carries it on every verse that has one.

**A verse-part is any other break**, at a word boundary the accents do not mark. It is named by
the transliterated first word of the part, exactly as a division of a poem is
(`yonah_matzah/hayom` above), and the name **may not contain `-`**, which marks a range. Parts
cannot be derived, so they are declared in `opensiddur/common/subverse.py` and every Tanakh
importer places them. Because a part's scope runs to the next verse-part, verse or chapter milestone (a
half-verse milestone does not end it), a passage
that stops in the middle of a verse needs a part declared where the *remainder* begins too:
`exodus/34/7/lo_yenakeh` exists so that `exodus/34/7/venakeh` ends where the recitation does.

The two units are separate unit-spaces and neither ends the other's scope: the Thirteen
Attributes close one word past the etnachta of Exodus 34:7, so a named part really does straddle
the accentual boundary. Neither ends the verse containing it either.

#### What sub-verse URNs do not cover

- **A break inside a word or inside a maqqef-joined unit.** The words a maqqef joins are read as
  one, and nothing may be placed between them.
- **A break inside a `tei:choice`.** A ketiv and a qere are two readings of one word, not two
  words. A boundary at the *head* of a choice is fine — the milestone goes before the element.
- **A verse whose division differs by variant.** Exodus 20:2 has its etnachta in one place under
  ta'am tachton and another under ta'am elyon, so it has no one accentual division and gets no
  halves. A URN must denote the same words wherever it resolves.
- **A verse with no etnachta**, which simply has no halves. Declare a verse-part if such a verse
  ever needs a break.
- **Psalms, Proverbs and Job where ole-we-yored governs.** There the etnachta is not the primary
  division, so verses carrying an ole are left undivided rather than divided at the wrong point.

General encoding guidelines, lines 650–705

Chapter:
```xml
<tei:milestone unit="chapter" n="2" corresp="urn:cts:opensiddur:bible.numbers.wlc:2"/>
```

Verse:
```xml
<tei:milestone unit="verse" n="2" corresp="urn:cts:opensiddur:bible.numbers.wlc:2.2"/>```

To indicate the spacing in scrolls, if it is available in your text:
* `<tei:lb/>` indicates a start-of-line.
* `<tei:lb type="first"/>` indicates the start of a poetic line which is broken in the scroll. 
  * The type may be `first`, `middle` or `last` (such as in פרשת האזינו)
* `<tei:cb/>` indicates a column break.

To indicate a _kri/ktiv_ (read/written) section, use:
```xml
<tei:choice>
   <j:read>kri</j:read>
   <j:written>ktiv</j:written>
</tei:choice>
```
When there is a _kri_ without a corresponding _ktiv_, use `tei:choice` with an empty `j:written`.
When there is a _ktiv_ without a corresponding _kri_, use `tei:choice` with an empty `j:read`.

To preserve a printed abbreviation alongside its editorial expansion, use
`tei:choice` with `tei:abbr` and `tei:expan`. The exporter setting
`readings.abbreviations` selects `abbreviated` (default) or `expanded` before
inline transclusion flattens the text. This does not select between kri/ktiv or
`j:option` readings. Record the evidence for expansions in the source README.

```xml
<tei:choice><tei:abbr>Hearken, &amp;c.</tei:abbr><tei:expan>Hearken to our prayer.</tei:expan></tei:choice>
```

A clear misprint in the source edition -- a misspelled or garbled word, a wrong citation
number, an unmatched quotation mark -- keeps the printed form in `tei:sic` beside its
correction in `tei:corr`. The exporter setting `readings.errors` selects `corrected`
(default) or `printed`. Archaic spellings are not errors, and a problem of fact or wording
is not a misprint; leave both as printed. A misprint inside an abbreviation nests its
`tei:choice` inside the `tei:abbr`.

```xml
<tei:choice><tei:sic>oppessors</tei:sic><tei:corr>oppressors</tei:corr></tei:choice>
```

To indicate alternate wordings of the same text, exactly one of which is read, use `j:option`
inside a `tei:choice`. Use `xml:lang` where the alternates differ in language, and `corresp` to
carry a URN by which a setting may select one:
```xml
<tei:choice>
   <j:option xml:lang="he">הב לן ונברך</j:option>
   <j:option xml:lang="yi">רבותי וויר וואָללן בענטשן</j:option>
</tei:choice>
```

General encoding guidelines, lines 760–789
```xml
<tei:l><tei:seg type="acrostic">מָ</tei:seg>עוֹז צוּר יְשׁוּעָתִי</tei:l>
```

Other inline spans that are marked by what they are, often shown in a source by colour:

* `<tei:seg type="quotation">`: words quoted from another text, such as a verse a translation renders.
* `<tei:seg type="supplied" subtype="...">`: words not in the source, supplied to fill a gap. The
  `subtype` says who supplied them (`scholars`, `author`).
* `<tei:seg type="cantillation" subtype="...">`: words read in a different melody from the text
  around them. The `subtype` names it (`job`, `eikhah`).
* `<tei:seg xml:lang="...">`: words in another language from the text around them.

#### Front matter

Material that precedes the main text — a title page, a preface, a translator's note — goes in `tei:front`, a
sibling of `tei:body` inside `tei:text`. In a project, front matter belongs on the project's `index.xml`, because
that is the entry point the exporter compiles.

Front matter that is running prose is encoded like any other text, with `tei:div`, `tei:head` and `tei:p`.

`j:transclude` is permitted inside `tei:front`, and the front matter need not be written into the index
literally. This is how a project holds front matter its own language does not print: a bilingual edition
sets its author's introduction once, in the project whose language it is, and the other project's index
transcludes it without declaring a `corresp` of its own. That keeps the introduction present when either
side is compiled, and — because a project is never set in parallel against itself — stops it being paired
against text it does not translate.

None of it is prayer, and an edition may leave it out: each section of front matter, and
each title page, is gated on `opensiddur:paratext` (see *Setting attribute values*).

General encoding guidelines, lines 900–950

### Annotations

Two types of annotations are recognized: 
1. Rubrics that appear inline in a text: instructions (`type="instruction"`) and descriptions
   (`type="description"`). See [Kinds of rubric](#kinds-of-rubric) for which is which.
2. Commentary (such as explanations or editorial notes) that is typically out-of-line with the text.

#### Instructions

Instructions are annotated as `tei:note` with a `type` attribute of `instruction` at the point where the instruction
affects the reader's usage of the text. An instruction that governs a passage — "On Shabbat:" — is not a range on
its own note; it is the rubric of the `j:conditional` around the passage.

Instructions may also have canonical labels (`corresp` attributes) with `urn:x-opensiddur:instruction:` URNs. If present, instruction sets may be swapped dynamically. For example, if the same "On shabbat" instruction exists in the source `A` and `B`, and they are both declared with the same `corresp` attribute, a setting can be used to choose which source's instruction should be used.

If an instruction says when a text is read, it is the condition's own rubric: the `tei:note` child of the
`j:conditional` that controls the text, which is printed only while the condition is undecided. A rubric that says what
the text is, who says it or how is a description, and goes inside the text the conditional controls (see
[Kinds of rubric](#kinds-of-rubric) below).

The following shows an example instructional note, a directive with an instruction URN:
```xml
<tei:note type="instruction" corresp="urn:x-opensiddur:instruction:amidah/rise">Rise.</tei:note>
```

#### Comments and Notes

Commentary that is not an integral part of the text is annotated using standoff markup, as follows: Within the text,
a `tei:anchor` element indicates a location that can be targeted for commentary. 

External to the `tei:text`, a `tei:standOff` element with `type="notes"` is present. In that element, the `tei:note` elements directly 
reference what they comment on. A `target` attribute references the point in the text where the note applies. 
If it applies to a longer section of text, a `targetEnd` attribute pointing to a later `tei:anchor` may also be used.
A short section of quoted text may be used to label the note, enclosed in `tei:label`.

Editorial and commentary notes may also have a `corresp` attribute in the `urn:x-opensiddur:notes:` namespace.

#### Conditional notes

A standoff note is found by its target alone, so it is set wherever its target's text is, including every place that
text is transcluded. Some notes only make sense in some of those places: a note on the opening of the Amidah that
speaks of the eighteen weekday benedictions does not belong in the Sabbath Amidah, which transcludes the same
opening. Such a note begins with a `j:condition` element that holds a condition, written as for
[`j:conditional`](#declaring-conditions) (feature structures and the `j:all`, `j:any`, `j:none` and `j:one`
operators):

```xml
<tei:standOff type="notes">
   <tei:note type="commentary" target="urn:x-opensiddur:text:prayer:amidah/adonai_sefatai">
      <j:condition>

General encoding guidelines, lines 1875–1905
Shemini Atzeret, Rosh Hashanah, Yom Kippur and Rosh Hodesh.

`slihot` gives the time of day only: from nightfall until the end of the time for Shaharit. The
season is not tested, because a personal fast has its selichot at any time of year. A text
says which season it belongs to.

Any of the date, time or holiday features may also contain a special value, the equivalent of
`<tei:symbol value="undefined"/>`. Having this value means that the attribute may have any
of its values. While processing, it is therefore necessary to include all
possibilities (as if the value were true or false) and any instructions that indicate to the reader what they are supposed to do in each case. 

When associating texts, the undefined value is accessible also through the `<tei:default/>` value, which should be used preferentially to the `tei:symbol` variant.

Overrides that are undefined are equivalent to having a false value.

#### Declaring attribute settings in a text


Declaring settings with text is used to force texts that will always have certain conditions met to process that way. For example, if the text is a Rosh Hashana mahzor and it includes ברכת המזון, it will never need to include על הנסים. By setting the holiday settings, the conditions will be processed correctly and the correct inclusions will be made without unnecessary text or instructions.


There are two ways to declare settings attributes:
1. By initializing the processor with attribute values already set.
2. By declaring attribute values with a range of text with XML

In the first way, the processor is initialized with settings attributes without adding any XML markup. That way, a processor could produce a text that is valid (for example) for a given date/time combination. The processing model does not define how to initialize the processor, as that is defined by the processor itself (configuration files, command line parameters, looking up a calendar, etc).

Settings are declared in XML using the `j:declare` element. The part of the text where the setting's scope ends is at the matching `j:endDeclare` element, as shown here: 
```xml
<tei:text>
   ...

General encoding guidelines, lines 1960–2001
how it is encoded:

- **A condition** says *when* the passage that follows is said: "On the Sabbath:", "With a
  minyan:", "Between Rosh Hashanah and Yom Kippur add:". It is the `j:conditional`'s own
  `tei:note type="instruction"`, and it means something only while the condition is unknown: it
  is printed when the condition is `undefined`, and not at all when it is `true` or `false`.
- **A directive** tells the reader to do or say something the text at that point does not
  contain: "Mourners' Kaddish" where no kaddish follows, "The Ark is opened", "Stand". It is a
  `tei:note type="instruction"` in the text, printed wherever its place is reached.
- **A description** says *what* the passage printed after it is, who says it, or how: "Mourners'
  Kaddish" before a transcluded kaddish (naming it, and implying all the instructions to
  mourners), "Reader:", "In silent devotion:". It belongs to the passage. It is a
  `tei:note type="description"` placed first inside the passage's scope, after the
  `j:conditional`, and it is printed whenever the passage is: with it when the condition is
  `true` or `undefined`, and left out with it when `false`.

The same words can be a directive in one edition and a description in another: an edition that
prints only "Mourners' Kaddish" is telling the reader to say it, and one that transcludes the
kaddish there is naming the text that follows. A rubric that says both when and what — "When the
Reader repeats the Amidah, the following Kedushah is said:" — is a description, since leaving it
out would lose the name of the passage.

```xml
<j:conditional xml:id="mourners_kaddish">
   <tei:note type="instruction">With a minyan:</tei:note>
   <tei:fs type="opensiddur:quorum">
      <tei:f name="minyan"><tei:binary value="true"/></tei:f>
   </tei:fs>
</j:conditional>
<tei:note type="description">Mourners' Kaddish.</tei:note>
<j:transclude target="urn:x-opensiddur:text:prayer:kaddish/mourners"/>
<j:endConditional target="#mourners_kaddish"/>
```

Descriptions and instructions are set alike: inline, as rubrics, with the edition's instruction
priority choosing their wording.

##### How an undecided scope is set off

A scope whose condition evaluates to `undefined` is kept, and how it is set off from the text
around it follows the source:


General encoding guidelines, lines 2100–2155

### Alignment

Translation (or other alternate text) alignment can be performed if both texts declare their correspondence to common URNs using the `corresp` attribute. For example, if two Bibles declare that a verse corresponds to `urn:x-opensiddur:text:bible:song_of_songs/1/5`, then that segment of text can be aligned with each other. The alignment starts from the declared milestone and runs until the next URN that both texts mark.

The join is on exact URN equality and nothing else: the compiler has no notion of one edition's verse
corresponding to several of another's. Two texts therefore align correctly only if both number their verses
canonically — see [Versification](#versification) — and a `@corresp` repeated within a document breaks the join,
because only the first segment carrying a given URN is kept (with a warning).

Where the two texts divide differently, only the URNs *both* mark become alignment boundaries: a division one
side does not carry is set within the nearest preceding division both carry. So a Hebrew divided at its accents
into `…/31/a` and `…/31/b` aligns against a translation that marks only `…/31`, and an edition that marks the
parshiyot aligns against one that marks only chapters. Where the two share no URN at all — an original divided
by biblical chapter and verse beside a translation divided by paragraph — they align only at the correspondence
that contains them, and are set as a single row: one text beside the other, whole. That is usually not what was
wanted, and the compiler warns when it happens; the remedy is to give both sides a common `@corresp`.


### Page references in a generated edition

Use an empty `tei:ref` with `type="page"` and an edition-qualified text URN:

```xml
<tei:note type="instruction" xml:lang="en">
  <tei:seg type="optional-page-reference">Hallel (page
    <tei:ref type="page" target="urn:x-opensiddur:text:prayer:hallel/blessing@hasiddur_hashalem-birnbaum-1949-he"/>)
    is recited here on Rosh Ḥodesh, Ḥol ha-Mo‘ed and Ḥanukkah.</tei:seg>
</tei:note>
```

The PDF exporter locates the first surviving occurrence of the target correspondence
in the specified source project, inserts a label there, and renders the reference
with LaTeX `\pageref`. The final number is the page in the generated document,
including separate Hebrew and English pages in parallel editions. Normal LaTeX
reruns resolve forward references. Original `tei:pb/@n` remains source foliation.

The electronic book has no pages. The same label becomes an HTML anchor in the destination,
and the reference becomes a link to it, shown as a symbol (→) between the source's own words.

Wrap independently removable instruction text in
`tei:seg type="optional-page-reference"`. If any of that span's page destinations
is absent after compilation (including conditional filtering), the exporter omits
the span. Keep independent directions outside it, or in separate spans. A missing
page destination outside an optional span is an export error. Bibliographic
citations to other books retain their original numbers.
