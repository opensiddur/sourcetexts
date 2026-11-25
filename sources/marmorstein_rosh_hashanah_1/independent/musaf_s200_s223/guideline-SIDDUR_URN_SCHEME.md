# Siddur canonical URN scheme

This document defines canonical reference URNs for siddurim in the Open Siddur JLPTEI
corpus. It supplements [JLPTEI-3.md](../schema/JLPTEI-3.md) and stands beside
[HAGGADAH_URN_SCHEME.md](HAGGADAH_URN_SCHEME.md), which it generalises.

A haggadah is one book with one running order, so naming its sections after that order
worked. A siddur is not: the same prayer appears in several services, several siddurim
order those services differently, and a translation has to align to all of it. The names
therefore have to say *what a text is*, independently of where any one book prints it.

## The rule everything else follows

> **A URN names a text. It does not name a book, a service, an occasion, a rite, or a
> position in any of them.**

Where a text sits is expressed by the book's own structure (`siddur:`) transcluding it.
When a text is said is a `j:conditional`. Which community says it is a condition too.
None of these belong in the path.

## Namespace overview

| Content | URN prefix | Example |
|---|---|---|
| A book's own running order | `urn:x-opensiddur:text:siddur:` | `…:chol/shacharit/amidah` |
| Shared liturgy | `urn:x-opensiddur:text:prayer:` | `…:amidah/avot` |
| Piyyutim and zemirot | `urn:x-opensiddur:text:poem:` | `…:adon_olam` |
| Scripture | `urn:x-opensiddur:text:bible:` | `…:psalms/145/1` |
| Mishnah | `urn:x-opensiddur:text:mishnah:` | `…:shabbat/2` |
| Talmud | `urn:x-opensiddur:text:talmud:` | `…:berakhot/11b/<incipit>` |
| Rubrics | `urn:x-opensiddur:instruction:` | `…:role/congregation` |

### Telling `siddur:` from `prayer:`

The two are easy to confuse, because a unit of a book's order is very often exactly one
prayer. The rule:

> **A `siddur:` URN names a place in a book's order. It holds no words of its own — only
> sequence, pagination, headings and transclusions.**
>
> **The test: remove every `j:transclude`. If no liturgy is left, the URN is `siddur:`.**

`prayer:` names a text that is said. `siddur:` is the one namespace where an occasion and
a service may appear, because a table of contents is exactly what they describe.

So `siddur:` reaches all the way down to the unit, and
`siddur:chol/shacharit/amidah` and `prayer:amidah` both exist and say different things —
*where this book puts it*, and *what is said there*. That is not a duplication to be
tidied away. The weekday and the Shabbat Amidah are different orderings of shared
berakhot; a project may map `prayer:amidah` only once, since `refdb` raises
`DuplicateUrnError` on a repeated text URN; so the two orderings have nowhere to live but
`siddur:`.

## `siddur:` — the book's running order

```
urn:x-opensiddur:text:siddur:<occasion>[/<service>][/<unit>]@<project>
```

This is the one namespace that *does* encode occasion and service, because that is
exactly what a siddur's table of contents is. It is the skeleton: `siddur:` files hold
headings, pagination and transclusions, and as little text of their own as possible.

```
urn:x-opensiddur:text:siddur:siddur@hasiddur_hashalem-birnbaum-1949-he
urn:x-opensiddur:text:siddur:chol@hasiddur_hashalem-birnbaum-1949-he
urn:x-opensiddur:text:siddur:chol/shacharit@hasiddur_hashalem-birnbaum-1949-he
urn:x-opensiddur:text:siddur:chol/shacharit/amidah@hasiddur_hashalem-birnbaum-1949-he
```

`<occasion>` and `<service>` come from closed lists, so two siddurim agree:

**occasion** — `all`, `chol`, `shabbat`, `rosh_chodesh`, `shalosh_regalim`, `pesach`,
`sukkot`, `shavuot`, `rosh_hashanah`, `yom_kippur`, `chanukah`, `purim`, `taanit`,
`berakhot`, `bayit`, `lifecycle`, `hosafot`.

`all` is for a unit said at its service **whatever the occasion** — not a unit said on
every occasion *in addition* to what the occasion calls for, which is `hosafot`. Prefer a
named occasion wherever the book confines a unit to one. Birnbaum's Shaḥarith li-Yladim is
the first of these — a child says it every morning, Sabbaths and festivals included, so
filing it under `chol` would say something the book does not.

**`all` is about which unit stands there, not about whether anything inside it varies.**
This once read "`all` is a claim that no occasion changes the unit, and it is wrong the
moment some occasion does", which is too strong and contradicts what this document says
three sections down about `prayer:`: *a passage said only on some occasion keeps its own
name and is wrapped in `j:conditional`*. If a conditional inside a unit disqualified `all`,
the conditional mechanism would have nothing to do.

The test is **replacement**: file a unit under a named occasion when the book puts a
*different* unit in its place on another occasion, as it does for the Amidah — the Sabbath
morning Amidah is another text, not this one with an insert. File it under `all` when the
same unit is said and the occasion only changes what is said *within* it.

Birkhoth ha-Shaḥar is the case that settled this, and the print settles it twice on its own
pages: `On Sabbath say:` stands inside the section, and the section ends *"On Sabbaths and
on major festivals the service is continued on page 299."* A unit that tells you what to add
on the Sabbath and where to go next afterwards is plainly said on the Sabbath.

The practical consequence is not cosmetic. Under `chol` the unit declared `shabbat: false`,
which resolved its own Sabbath rubric away in **every** compile, including the undecided one
— a conditional that could never be true, inside a unit whose rubric says when to say it.
Validation, the registry and the reference database all passed; only compiling it and
looking for the passage found it.

**service** — `arvit`, `shacharit`, `musaf`, `minchah`, `neilah`, `selichot`. Omitted for
occasions that are not services.

Two siddurim sharing a `siddur:` URN is correct and wanted: alignment joins on the URN
with `@project` stripped, so a translation of this book emits identical `siddur:` URNs
under its own project id and aligns unit for unit with no further work. Adding to the
closed lists is a change to this document, not a local decision.

## `prayer:` — shared liturgy

```
urn:x-opensiddur:text:prayer:<prayer>[/<part>]*
```

**Never contains an occasion, service or rite, except to distinguish a complete
wording variant as described below.** A passage said only on some occasion
keeps its own name and is wrapped in `j:conditional`:

```
urn:x-opensiddur:text:prayer:amidah/avot
urn:x-opensiddur:text:prayer:amidah/avot/zokhrenu
urn:x-opensiddur:text:prayer:amidah/gevurot/mashiv_haruach
urn:x-opensiddur:text:prayer:kaddish/yatom
urn:x-opensiddur:text:prayer:ashrei
urn:x-opensiddur:text:prayer:yaaleh_veyavo
```

A calendar name may distinguish a **complete wording variant** when the words
actually differ and selecting the undifferentiated identity would lose those
words. `prayer:hadlaqat_ner_yom_tov/shabbat` identifies the combined blessing
with של שבת ושל יום טוב, rather than the ordinary festival wording של יום טוב.
It is registered as `kind: variant`; the parent path denotes a wording variant,
not a smaller span or a new occasion identity. Reuse the conditional parent
where it already supplies both wordings. An edition printing only the ordinary
blessing cannot serve as the combined variant; an extraction of the complete wording in
an existing compatible witness may supply it without creating new prayer words.
Calendar names alone, changes of placement and differences of edition do not
justify new identities.

### Nest only what lives in one place

A `kind: variant` child is the documented complete-wording exception above;
the following nesting rule governs sub-parts.

> **A text is a sub-part of another only if that is the *only* place it appears.
> A text appearing in more than one parent is an independent unit that those parents
> quote.**

This is the same rule as "no occasion in the path", applied to containers. A path
component is a claim about where a text belongs, and a text belonging in two places
cannot be described by either one.

`prayer:amidah/avot` is correctly nested: the first berakhah of the Amidah appears
nowhere else, so the Amidah is genuinely part of what it is.

`prayer:ashrei` is correctly **not** nested. Ashrei is said in P'sukei D'zimra, at
Minchah, and at Ne'ilah. `prayer:pesuqei_dezimrah/ashrei` would name one of its homes and
lose the rest, and a Minchah service transcluding it would either have to use a URN that
says P'sukei D'zimra or invent a second one for the same text.

`prayer:yaaleh_veyavo` likewise. It appears canonically in the Amidah *and* in Birkat
HaMazon, so it is an independent unit quoted in both, not a part of either.
`prayer:amidah/avodah/yaaleh_veyavo` would be wrong for the same reason
`prayer:rosh_chodesh/yaaleh_veyavo` is: it names one context out of several.

The practical test when adding a name: *can I think of a second service or prayer in
which this text is said?* If yes, it is top-level. Depth is a claim, so do not
manufacture it.

### Name by incipit, not by ordinal

**Where a text has no settled name, use its opening words. Never number it.**

An ordinal records a position in one edition, and position is exactly what varies. The
zimmun and the Harachaman series differ between rites in both order and wording, so
`birkat_hamazon/17` names nothing that survives a change of edition, while
`birkat_hamazon/harachaman/yitbarakh` names the same text wherever it falls.

**A canonical incipit stands for the logically equivalent wordings of the same text.**
The zimmun opens with הב לן ונברך in one rite and רבותי נברך in another; these are one
text under one URN, and the differences are variants (`tei:choice`/`j:option`) or
conditions. Choosing one incipit and canonicalising it is better than either numbering
them or minting a URN per wording — the alternative is that no two editions of birkat
hamazon can be aligned at all.

**When two texts share an incipit, go further down.** Two Harachaman paragraphs both open
הרחמן הוא ינחילנו יום שכלו and then diverge, one for Shabbat and one for Yom Tov. They are
distinct texts, not one text with a variant ending, so they get distinct names:

```
urn:x-opensiddur:text:prayer:birkat_hamazon/harachaman/yanchilenu_shabbat
urn:x-opensiddur:text:prayer:birkat_hamazon/harachaman/yanchilenu_tov
```

Each then carries its own condition — in a haggadah only the Shabbat one is conditional,
since Pesach is a festival either way; in a siddur both are. Where a pair like this is
ordered, Shabbat conventionally precedes Yom Tov.

### The same text in several contexts

A text repeated verbatim in different places gets **one** URN for the text and keeps a
distinct URN for each context, because what differs between the contexts is usually not
the words but the rubrics around them.

Borei Pri Hagafen is the worked example: the same blessing over each of the seder's four
cups, over qiddush, and over havdalah. It is one `prayer:borei_peri_hagafen`. Each context
keeps its own URN, which holds whatever is particular to it — the instruction for that
cup, a note, a conditional — and reaches the shared words in one of two ways:

- **Transclude it.** `<j:transclude target="urn:x-opensiddur:text:prayer:borei_peri_hagafen"/>`
  inside the context's division. Right when the context adds nothing to the words.
- **Declare partial correspondence with milestones.** The outer division carries the
  context URN; milestones inside it identify the shared text independently of paragraphs. This is the pattern
  `haggadah_leleil_shimmurim-heidenheim-1822-he/psalm_126.xml` already uses, where a `tei:div` with the
  haggadah's URN contains milestones with canonical `bible:` URNs.

```xml
<tei:div corresp="urn:x-opensiddur:text:haggadah:barekh/kos_shlishi">
  <tei:note type="instruction" corresp="urn:x-opensiddur:instruction:…"/>
  <tei:p><tei:milestone unit="prayer" corresp="urn:x-opensiddur:text:prayer:borei_peri_hagafen"/>…
  <tei:milestone unit="prayer"/></tei:p>
</tei:div>
```

### One text, printed on several pages

A book prints a shared text more than once — Birnbaum's Avot is on printed page 81 at
Shacharit, 161 at Minchah, 201 at Arvit — and the file holding that text is one file. So
`tei:pb` has to say *which printing* each break belongs to. `@ed` is a list of tokens, and
that is the mechanism:

> **The first token is the edition. A second token is present only where that edition
> prints the same text more than once, and names which printing — by the `siddur:` path of
> the unit it belongs to.**

```xml
<tei:pb n="81"  ed="1949 chol/shacharit/amidah" facs="…"/>
<tei:pb n="161" ed="1949 chol/minchah/amidah"   facs="…"/>
```

A break falling at the same point in two printings names both:
`ed="1949 chol/shacharit/amidah chol/minchah/amidah"`.

**A text needs its own file per context only when the words differ.** Where they are
identical, the second unit transcludes the same URN, and its page breaks sit beside the
first unit's in the one text, each under its own sigil. `tei:biblScope unit="pages"` in
the file's `sourceDesc` carries one entry per printing for the same reason.

Note that `@corresp` holds **one** URN. `refdb.add_urn_mapping` indexes the attribute
whole and does not split on whitespace, so a space-separated list would be recorded as a
single nonexistent URN. Correspondence to two URNs at once is expressed by nesting, not
by listing.

### Where a shared text lives is revisited as the book grows

The first unit to print a text is not thereby its home. A name is chosen from what the
text *is*, and early in a conversion the only evidence available is the one place it has
been read so far — which is a fact about the reading order, not about the liturgy.

Birnbaum's Shema is the case that shows it. The two verses were first read inside the
run-on paragraph on printed page 1, in Shaḥarith li-Yladim, and so were first realised
there. They belong to Keriath Shema, which this conversion has not reached. When it is
reached, the realisation moves there and the children's page transcludes it; the URNs do
not change, but which file *realises* them does.

> **Expect to move the realisation of a shared text as later units are read. What may
> not change under it is the URN itself, because that is what two projects join on.**

This is not churn to be avoided. Leaving a text realised in the first unit that happened
to print it would make the running order of one conversion into a claim about the
liturgy, and every later unit would have to defer to an accident.

### Conditions belong to the context, not to the shared text

Conditioning a transclusion from outside it is the established convention, not something
this scheme introduces — see [Conditional text](../schema/JLPTEI-3.md#conditional-text),
the `Transclusion` scope in `feinstein_haggadah/conditionals.py`, and the existing usage
in `haggadah_leleil_shimmurim-heidenheim-1822-he/pre_seder.xml` and `chumash-opensiddur-he/parashat_chukat_balak.xml`.

It is restated here only because sharing depends on it. A Harachaman paragraph said on
Shabbat is the same words as one said any other day; what differs is whether it is said.
A shared text that carried its own condition would be bound to one occasion and useless
to every other context, and the next context needing it would have to copy the words
instead of transcluding them. The same reasoning keeps instructions in the context: the
rubric for the third cup differs from the second while the blessing does not.

## `front:` — a book's own front matter

```
urn:x-opensiddur:text:front:<part>[/<n>]
```

Front matter is the one thing in a book that is neither liturgy nor a place in the running
order. A title page is not said, so it is not `prayer:`; it holds words of its own, so it is
not `siddur:`, which by the rule above holds none. It gets a namespace.

**The parts are a closed list**, so that two books agree the way two siddurim agree on
`chol/shacharit`: `title_page`, `copyright`, `dedication`, `acknowledgements`, `preface`,
`introduction`, `contents`, `colophon`. Adding to it is a change to this document.

**No book or edition component.** The `@project` suffix already scopes the URN to an edition,
and leaving the book out of the path is exactly what lets a translation align: the Hebrew and
the English title leaves of one book are both `front:title_page`, and they pair with no
further work. So does a translation's introduction against the original's.

**A trailing numeric is the edition's own division**, under the same rule as
[Sub-division numbering](#sub-division-numbering). Birnbaum heads the parts of his
introduction I, II and III himself, so `front:introduction/1` records a division he made; it
does not claim that another edition's `/1` covers the same ground.

### One side may transclude what it does not realise

Front matter is routinely one-sided. Birnbaum wrote his introduction in English and the print
has no Hebrew counterpart to it at all.

> **An index may transclude a front-matter URN its own project does not realise.** The
> transclusion resolves to whichever project does, and that project issues the only
> `@corresp`.

Both compiles then carry the section, and neither carries a false alignment: a project is
never set in parallel against itself, so a transclusion resolving into the parallel project
falls back to a single column instead of pairing English against unrelated Hebrew. This needs
the other project named in `priority.transclusion`, after the primary — the priority list is a
filter, not a preference, and a URN in no listed project fails to resolve rather than
resolving anyway.

`tei:titlePage` cannot be transcluded, because it belongs to `model.frontPart` and a
transclusion arrives inside a `tei:div`. Two editions each write their own title leaf into
their own index and declare the correspondence by carrying the same URN. See
[Front matter](../schema/JLPTEI-3.md#front-matter).

## `poem:` — piyyutim and zemirot

Same rules and transliteration as `prayer:`. Used for poetry that is not itself part of
the fixed service order: zemirot, hoshanot, Adon Olam, Yigdal. Stanzas without a
canonical numbering are addressed by transliterated incipit, per JLPTEI-3:

```
urn:x-opensiddur:text:poem:yonah_matzah/hayom
```

## `bible:` — scripture

Unchanged from JLPTEI-3 and the haggadah scheme; see them for versification. A complete
scriptural unit inside the liturgy carries its `bible:` URN *in addition to* whatever
name the liturgy knows it by, on the enclosing division:

```xml
<tei:div corresp="urn:x-opensiddur:text:prayer:ashrei">
  <tei:milestone unit="chapter" n="145" corresp="urn:x-opensiddur:text:bible:psalms/145"/>
```

## `mishnah:` and `talmud:` — rabbinic sources

New here, and they behave differently from each other because liturgy quotes them
differently.

```
urn:x-opensiddur:text:mishnah:<tractate>/<chapter>[/<mishnah>]
urn:x-opensiddur:text:talmud:<tractate>/<daf><amud>[/<incipit>]
```

**Liturgy quotes whole mishnayot routinely** — a chapter of Mishnah recited entire is a
common liturgical unit. So a mishnah citation frequently needs no sub-part, and the
chapter-level URN is the exact unit.

**Liturgy almost never quotes a whole daf.** A talmudic passage in a siddur is a few
lines from one side of one folio, so a `talmud:` citation normally needs a sub-daf
component. A daf has no finer canonical division, so it is named by transliterated
incipit, exactly as `poem:` names a stanza.

**The absence of a trailing component is meaningful.** `mishnah:<tractate>/2` asserts the
whole chapter; `mishnah:<tractate>/2/1` asserts one mishnah within it. Do not add a
component to be safe — an unnecessary one makes a whole-unit quotation look partial and
breaks alignment against an edition that got it right.

Tractate names use the same transliteration rules as `prayer:`.

## Other cited works

`bible:`, `mishnah:` and `talmud:` are instances of a pattern rather than a closed set:
a work outside the liturgy, with its own canonical indexing scheme, that the liturgy
quotes. Others behave the same way — the Zohar is the obvious next one, with a canonical
citation scheme of its own and passages rather than whole sections quoted.

Two ways to handle such a work, and the choice turns on how often it is quoted:

- **A namespace of its own**, when the corpus quotes the work often enough that citations
  need to be comparable and resolvable against an edition of it. Follow the `talmud:`
  shape: the work's own canonical index, plus an incipit component where the quotation is
  a passage within an indexed unit rather than the whole of it.
- **A `prayer:` or `poem:` name from the siddur's own incipit**, when it is quoted a
  handful of times. A passage the liturgy knows by its opening words, such as
  `prayer:brich_shmei`, does not need a namespace stood up around it to be addressable,
  and inventing one for two or three citations costs more than it returns.

Either way the quotation carries a `tei:bibl`/`tei:ref` to the source. Standing up a new
namespace is a change to this document; using an incipit is not.

## `instruction:` — rubrics

Rubrics are not liturgy and do not belong in the text namespaces.

```
urn:x-opensiddur:instruction:<path>
```

Instruction sets live in their own projects, so a book's text can be read with its own
rubrics, with another edition's, with several, or with none. Two projects supplying the
same instruction URN are alternative rubrics for the same point; an instruction URN
present in one set and absent from another is normal and needs no special provision.

### Speaker roles — a controlled vocabulary

Who recites a passage is a rubric with only a few possible answers, so it gets standing
URNs rather than free text. Every siddur then marks these identically and a renderer can
style them:

```
urn:x-opensiddur:instruction:role/reader
urn:x-opensiddur:instruction:role/congregation
urn:x-opensiddur:instruction:role/reader_and_congregation
urn:x-opensiddur:instruction:role/reader_then_congregation
urn:x-opensiddur:instruction:role/congregation_then_reader
urn:x-opensiddur:instruction:role/kohanim
```

`role/kohanim` is not a fourth way of dividing reader from congregation: the priestly
blessing is said by the kohanim present and by nobody else, and a siddur that marked it
"congregation" would be telling the wrong people to say it.

Emitted as `tei:note type="instruction"` carrying the URN in `@corresp`.

## Partial witnesses are normal

**A project's realisation of a URN need not cover every conditional branch that text
has.** A partial witness is neither a defect nor a different text.

The haggadah's Ya'aleh v'yavo carries only the Pesach wording, because its source has
only that. A siddur's carries every occasion. Both are
`prayer:amidah/avodah/yaaleh_veyavo`, both are correct, and **neither has to change to
accommodate the other.**

Two consequences:

- Alignment on a URN does not imply the two sides have the same branches. A consumer
  selecting a branch some witness lacks gets nothing from that witness. That is the right
  answer, not an error.
- The registry records a URN's *known* branches. It never asserts that every project
  realising the URN implements them all. Validation checks that branches **used** are
  registered, never that registered branches are used.

This generalises what the corpus already relies on for translations, where an English
witness is routinely coarser than its Hebrew.

## Naming

Common spelling wins where a text has one in English: `aleinu`, `ashrei`, `kaddish`,
`yishtabach`, `birkat_hamazon`. Otherwise transliterate per the
[table in JLPTEI-3](../schema/JLPTEI-3.md#transliteration), spaces becoming `_`. The common
spellings, and known misspellings of other words, are listed in `specs/naming/spellings.yaml`
and checked by `validate_names`; see [NAMING_SCHEME.md](NAMING_SCHEME.md). The registry is the
tiebreaker and the record; the transliterator only seeds it.

Names are lowercase ASCII. A name may not contain `-`, which marks a range, nor `@`, `#`
or `:`, which delimit URN parts.

## Sub-division numbering

A trailing numeric component is **the transcribed edition's own division**, not a
canonical one:

```
urn:x-opensiddur:text:prayer:amidah/avot/1
```

A numbered URN aligns like any other: the compiler pairs identical URNs, and two texts that
both carry `prayer:amidah/avot/1` are set side by side there. That is what the haggadah's
`magid/ha_lachma_anya/1` relies on to align its Hebrew paragraphs with their translation.

**But a number is a poor alignment key, and a named subdivision is preferred.** The count is
the edition's own, so it can change between editions — a reprint that divides a paragraph
in two renumbers everything after it — and two editions that both call something `/1` have
only each divided it, not necessarily the same way. Use a number only where the texts that
share it were divided together, as a source and its translation are; name the subdivision
where it has a name. For the same reason a page turn in one printing must never become a
numbered division: it would claim an alignment with every other edition that does not
exist.

## Ending a scope: the unit-terminating milestone

A `@corresp` on a milestone scopes to the next milestone of the same unit *or the end of
the text* (see JLPTEI-3.md, "URN scope", for the full rule). That over-claims whenever a division ends partway through a file with nothing
of its kind after it — which a siddur hits constantly, because a page of shared text ends
with material belonging to no named prayer.

**A milestone with the same `@unit` and no `@corresp` closes the open scope without
opening one.**

```xml
<tei:milestone unit="prayer" n="1" corresp="urn:x-opensiddur:text:prayer:amidah/avot"/>
…
<tei:milestone unit="prayer"/>          <!-- ends avot; starts nothing -->
```

The terminator creates no mapping of its own, since only elements carrying `@corresp`
are indexed. There is precedent for a deliberately unindexed milestone in
`unit="edition-verse"`, which carries `@n` but never `@corresp`.

It did need a change to `refdb`, contrary to an earlier draft of this document.
`find_end_of_mapping` searched `following::tei:milestone[@corresp]`, so a terminator was
never considered as a candidate at all. Dropping that filter naively would have been
worse than doing nothing: under the path-depth fallback in `milestone_terminates`, an
`edition-verse` milestone would then have closed every canonical verse it follows,
truncating scopes across WLC, MAM and JPS. So a corresp-less milestone now terminates
only on an **exact** `@unit` match, which admits the terminator and excludes every other
bare milestone in the corpus — `citation`, `acrostic`, `parsha.annual` and
`edition-verse` among them. Verified inert: reindexing every project produces byte-identical
counts, and no bare milestone anywhere in the corpus follows an open scope of its own unit.

## The registry

The scheme is only useful if one text has exactly one URN across every work containing
it. That is recorded in `specs/urn_registry/`, as JSON Lines — one record per line, so a
diff shows one line per change:

```
specs/urn_registry/{prayer,poem,siddur,instruction,aliases}.jsonl
```

A canonical record names the URN, its parent, what kind of thing it is, and its labels:

```json
{"urn":"urn:x-opensiddur:text:prayer:amidah/avot","parent":"urn:x-opensiddur:text:prayer:amidah","kind":"berakhah","label_en":"Blessing of the Patriarchs","status":"canonical"}
```

From the first stable release, an alias record will bind a URN no longer in use to its
canonical name (until then a renamed URN is replaced outright; see `NAMING_SCHEME.md`):

```json
{"urn":"urn:x-opensiddur:text:haggadah:hallel/yishtabach","canonical":"urn:x-opensiddur:text:prayer:yishtabbach","status":"alias"}
```

A context record keeps a place-specific URN that reaches a shared text by transclusion
(see *Unification with the haggadah namespace*).

Registry URNs carry **no** `@project` and no `#fragment`: they name texts, not their
realisations. Where a URN resolves stays `refdb`'s job. The registry adds the three
things refdb structurally cannot hold — decomposition into parts, a human-readable label,
and the canonical/alias edge.

`python -m opensiddur.common.urn_registry --check` validates grammar, parentage,
uniqueness and alias resolution, and cross-checks against refdb that every `prayer:`,
`poem:`, `siddur:`, `mishnah:`, `talmud:` and `instruction:` URN a project emits is
registered.

## Unification with the haggadah namespace

`HAGGADAH_URN_SCHEME.md` says shared liturgy should use `prayer:`, and the Haggadah does: a
shared section or paragraph is named by its own URN (`feinstein_haggadah/sections.py`,
`SHARED_TEXTS` and `SHARED_PARAGRAPHS`).

| Section | URN |
|---|---|
| `maggid/psalm_113`, `/psalm_114`; `hallel/psalm_115` … `/psalm_118` | `prayer:hallel/psalm_113` … `/psalm_118` (+ `bible:psalms/*` milestones) |
| `hallel/yehalalukha` | `prayer:hallel/yehalelukha` |
| `hallel/psalm_136` | `prayer:hallel_hagadol` |
| `hallel/nishmat`, `/shokhen_ad`, `/hael_betaatzumot`, `/uvemaqhalot`, `/befi_yesharim`, `/yishtabbach` | `prayer:nishmat`, `prayer:shokhen_ad`, `prayer:hael_betaatzumot`, `prayer:uvemaqhalot`, `prayer:befi_yesharim`, `prayer:yishtabbach` |
| `barekh` paragraphs 1–28 | `prayer:birkat_hamazon/*`, by their opening words (`zimmun/hav_lan` … `yiru_et_adonai`), and `prayer:yaaleh_veyavo` |
| `barekh/psalm_126` | `prayer:birkat_hamazon/shir_hamaalot` |
| `qaddesh` paragraphs 1, 2, 3, 5 | `prayer:kiddush/vayekhulu`, `/savri`, `/asher_bachar_banu`; `prayer:shehecheyanu` |
| `nirtzah/al_hagefen` | `prayer:berakhah_acharonah/al_hagefen` |
| `nirtzah/sefirat_haomer` | `prayer:sefirat_haomer` |

A shared section is one paragraph, which its own URN names, so it has no paragraph URN.
**Ya'aleh v'yavo** is top-level, not under Birkat Hamazon: it is said in the Amidah too, and
that the Haggadah's copy carries only the Pesach wording is not a reason to re-encode it — see
*Partial witnesses are normal*. **The Nishmat-to-Yishtabbach block** is top-level for the same
reason: it concludes P'sukei D'zimra on Shabbat and festivals and is said at the seder too, so
it has two homes and no single parent. **`prayer:ashrei`** is top-level likewise.

Some places keep a `haggadah:` URN for what is particular to them, with a context record in
`specs/urn_registry/aliases.jsonl` that names the shared text they reach by transclusion
(`references`): the cups (`maggid/kos_sheni`, `barekh/29`, `nirtzah/kos_revii`, each
Borei peri hagafen), `rachatz` (Al netilat yadayim), `motzi_matzah` (Hamotzi and Al achilat
matzah) and `urechatz`, which has no blessing. Kiddush's Havdalah paragraph (`qaddesh/4`) and
Shefokh Chamatkha (`barekh/30`) stay `haggadah:` too.

What stays in `haggadah:` is what is genuinely seder-specific: the fifteen simanim as an
ordering, the Magid narrative, Shefokh Chamatkha, the Nirtzah songs, and the pre-Pesach
observances.

### Birnbaum's composite verse paragraphs

The Hodu-to-Ashrei installment explicitly assigns its ordered composite paragraphs
`siddur:chol/shacharit/pesuqei_dezimrah/{incipit}` URNs. This is a scoped extension of
the skeleton-only convention above: the paragraph records this book's arrangement
of verses, with the actual words in nested `bible:` segments. The liturgical joining
phrase “יְיָ מֶלֶךְ, יְיָ מָלָךְ” has its own `siddur:` subpart identity rather than
an invented biblical address. Its following clause is Exodus 15:18.

Each distinct verse is canonically mapped once. A repeated occurrence may carry its
biblical URN in `tei:seg/@source` when its pointing or punctuation differs, preserving
the printed occurrence without creating a duplicate canonical `corresp` mapping.
The enclosing paragraph's `siddur:` URN supplies bilingual alignment.
