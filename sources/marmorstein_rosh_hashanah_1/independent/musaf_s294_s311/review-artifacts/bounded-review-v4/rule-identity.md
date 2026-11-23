Exact /home/efeins/.codex/worktrees/marmorstein-processor/master/schema/JLPTEI-3.md lines1–85
1: # Jewish Liturgy TEI
2: 
3: This document provides a description of the [TEI](http://www.tei-c.org) variant used to encode Jewish liturgical
4: texts in the Open Siddur.
5: 
6: # About JLPTEI
7: 
8: JLPTEI XML is the Jewish Liturgy Project (subset of the) [Text Encoding Initiative](http://www.tei-c.org) XML.
9: 
10: ## XML Namespaces
11: 
12: Every JLPTEI document uses the following XML namespaces:
13: ```xml
14: <tei:TEI xmlns:tei="http://www.tei-c.org/ns/1.0"
15:          xmlns:j="http://jewishliturgy.org/ns/jlptei/2">
16:    ...
17: </tei:TEI>
18: ```
19: 
20: The `tei` namespace is used for TEI-defined elements. The `j` namespace is used for nonstandard JLPTEI extensions.
21: 
22: ## Attributes
23: When we refer to `ns:element[@attribute='value']`, it is shorthand for:
24: ```xml
25: <ns:element attribute="value">...</ns:element>
26: ```
27: 
28: ## Projects
29: 
30: Projects are the highest level organizing structure. All documents are contained within a project.
31: Projects may represent individual sources, or a combination of sources chosen for a particular purpose.
32: A project is a directory under the `projects/` directory in github.
33: 
34: Every project contains a document named `index.xml`. This is the default entry point of the project.
35: 
36: Projects must have globally unique names, of the form `<title>-<author>-<date>-<lang>` in lowercase ASCII (eg, `tanakh-jps-1917-en`, `hasiddur_hashalem-birnbaum-1949-he`). See [NAMING_SCHEME.md](../specs/NAMING_SCHEME.md).
37: 
38: ## URNs and linkages
39: 
40: URNs (Universal Resource Names) are a form of URI (universal resource identifier) that allow reference to specific sections, paragraphs, verses, or (sometimes) words within our liturgical or scriptural XML documents. We use our own custom URN namespace that begins `urn:x-opensiddur:` The remainder of the URN is hierarchical, beginning with the type of what is being identified (eg, `text`, `note`, `instruction`, `setting`, `condition`). A project identifier may follow, after an `@` sign, where a reference must name the project it is taken from; a `@corresp` never carries one.
41: 
42: An element's  urn is stored in the TEI-global `@corresp` attribute.
43: 
44: ### URNs versus file/fragment pointers
45: 
46: Not every cross-file reference is a URN. A URN names *a text* — content that may exist in
47: several variant representations, where the `@project` suffix selects one of those
48: possibilities. That covers most cross-references: alignment between editions, quotations of a
49: Biblical or liturgical passage, transclusion of shared text. Use a URN whenever the thing
50: referenced could plausibly be represented by more than one project.
51: 
52: Some references, though, point at one exact, unchanging position in one exact file, with no
53: notion of "which variant" — the reference names a specific document's specific content, not a
54: text that document happens to carry. The paradigm case is a document's citation of its own
55: project's source bibliography: a haggadah document's `tei:bibl` names one constant bibliographic
56: entry in its project's `index.xml`, never "one of several possible sources." For these, use a
57: plain, project-root-relative file/fragment pointer instead of a URN:
58: 
59: ```
60: /{PROJECT_ID}/{FILE_STEM}#{XML_ID}
61: ```
62: 
63: with no file extension (`.xml` is assumed). For example,
64: `/haggadah_leleil_shimmurim-heidenheim-1822-he/index#project_source_bibl` addresses the `tei:bibl` with that
65: `xml:id` in `haggadah_leleil_shimmurim-heidenheim-1822-he/index.xml`. `xml:id` is unique within a file, so resolving
66: this kind of pointer only requires opening the named file — no URN or reference-database lookup.
67: 
68: `condition` URNs name a condition that cannot be calculated — in practice a textual variant,
69: a wording some communities add and others do not. They are used as the feature names of the
70: `opensiddur:variant` feature structure (see [Setting attribute values](#setting-attribute-values)).
71: The path mirrors the text URN of the passage that varies, with the variant's name appended, and
72: carries **no** project identifier, because a variant belongs to the text rather than to any one
73: edition of it:
74: ```urn
75: urn:x-opensiddur:condition:haggadah:maggid/lefikhakh/shirah_chadashah
76: ```
77: 
78: An example complete Biblical URN is:
79: ```urn
80: urn:x-opensiddur:text:bible:genesis/1/1@tanakh-wlc-he
81: ```
82: which identifies the verse Genesis 1:1 in the WLC source.
83: The URN `urn:x-opensiddur:text:bible:genesis/1` identifies the chapter Genesis 1 in *every* source. A biblical
84: URN names a stretch of text, not one edition's way of numbering it, so every project must mean the same thing by
85: it — see [Versification](#versification).
