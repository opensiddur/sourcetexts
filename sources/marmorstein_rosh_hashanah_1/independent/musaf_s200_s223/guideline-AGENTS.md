This file provides guidance to coding agents when working with code in this repository.

## Project Overview

The project derives from 3 repositories:
opensiddur-processor https://github.com/opensiddur/opensiddur-processor (this repository)
sourcetexts https://github.com/opensiddur/sourcetexts (submodule at sourcetexts/, content in sourcetexts/sources/)
opensiddur-projects https://github.com/opensiddur/opensiddur-projects (submodule at opensiddur-projects/, content in opensiddur-projects/project/)

The other two repositories are git submodules of this one, so a release tag pins the exact
source and project commits it was built against. See `RELEASE_PROCEDURE.md`.

**Paired PRs.** opensiddur-projects PRs are validated by this repository's validators
(`.github/workflows/validate-projects.yml`). When project XML depends on an unmerged change here
(registry entries, schema, validators), give both PRs the same branch name: the projects check
then validates against that opensiddur-processor branch instead of main, and warns that it did. Merge
the opensiddur-processor PR first, re-run the projects check (it falls back to main once the branch is
deleted), then merge the projects PR.

This repository has 3 parts: 
(1) schema documentation for the Jewish Liturgy Project TEI extension (`JLPTEI-3.md`) and formal RelaxNG and Schematron schemas (schema/ subdirectory)
(2) importers (opensiddur/importer/ subdirectory) that 
 (a) download raw data and put them into the sourcetexts/sources/ submodule and 
 (b) convert the raw data into JLPTEI XML format and save them as projects (opensiddur-projects/project/ submodule)
(3) exporters (opensiddur/exporter/ subdirectory) that 
 (a) compile JLPTEI projects containing multiple JLPTEI files and/or reference multiple projects into a compiled intermediate format and 
 (b) export the intermediate format into finalized consumable forms (currently PDF via LuaLaTeX).

Any specifications for agents to build code should be stored in the specs/ directory.
Specifications and plans for bug fixes are temporary working artifacts and must not be committed.

## Commands

**Set up a fresh checkout or worktree** — run all three before trusting a test run:
```bash
git submodule update --init
uv sync --all-groups
bash scripts/build-schema.sh
```
A new worktree starts with empty submodule directories, so the importers and exporters find
no sources or projects until `git submodule update --init` has run.
The compiled schema artifacts are gitignored, so a new worktree has none. Without them
~47 validation tests fail in a way that looks like a real regression rather than missing
setup.

**Run code:**
```bash
uv run python <script.py>
```

**Run all tests:**
```bash
uv run pytest
```

**Run a single test file:**
```bash
uv run pytest opensiddur/tests/exporter/test_compiler.py
```

**Run with coverage:**
```bash
uv run coverage run -m unittest discover -s opensiddur/tests -v
uv run coverage report -m
```

**Install dependencies:**
```bash
uv sync --all-groups
```

**Compile JLPTEI schema** (requires podman):
```bash
bash scripts/build-schema.sh
```

**Validate a JLPTEI file** (requires `jing`: `apt install jing`):
```bash
uv run python -m opensiddur.importer.util.validation opensiddur-projects/project/tanakh-wlc-he/ruth.xml
```

**Download Feinstein/Heidenheim haggadah sources** (OSP compilation + HebrewBooks PDF):
```bash
uv run python -m opensiddur.importer.feinstein_haggadah.download
```

**Align page breaks** from the 1822 PDF facsimile (writes `page_breaks.json`):
```bash
uv run python -m opensiddur.importer.feinstein_haggadah.align_page_breaks
```

**Convert haggadah sources to JLPTEI projects** (each output file is validated against RelaxNG + Schematron before write):
```bash
uv run python -m opensiddur.importer.feinstein_haggadah.convert
```

**Import prayers from opensiddur.org** (see `specs/OPENSIDDUR_ORG_IMPORT.md`). The site's monthly GitHub export
is cloned beside the repositories, at `opensiddur-repos/opensiddur.org/` (`$OPENSIDDUR_ORG_UPSTREAM` overrides).
```bash
uv run python -m opensiddur.importer.opensiddur_org.download --category 183   # copy in-scope posts; no-op when unchanged
uv run python -m opensiddur.importer.opensiddur_org.survey                    # output/opensiddur_org_triage.{json,md}
uv run python -m opensiddur.importer.opensiddur_org.match                     # URN decisions, recorded at once; the evidence in output/
uv run python -m opensiddur.importer.opensiddur_org.convert --register        # standard posts -> <title>-<author>-<date>-<lang> projects
uv run python -m opensiddur.importer.opensiddur_org.update [--prune]          # monthly: all of the above for what the new export changed; report in output/
```
Licence decisions live in `opensiddur/importer/opensiddur_org/licence_decisions.yaml`; a licence or post not
decided there is asked about, then recorded. A decision about one post lapses when a later export updates or
relicenses it. Decisions about single posts that the spec's rules get wrong or leave open (out of scope, a column's
language, what a post's colours mean, essays, where a post outside the site's tables keeps its text) live in `post_decisions.yaml`. `convert --emit-contributor-candidates` writes lines for
unregistered contributors to `output/` for review; they are never registered automatically.

**Download the Birnbaum siddur** — three sources for one book, all writing into
`sourcetexts/sources/birnbaum_siddur/` keyed by the same scan page number. Needs
`--contact-email` or `$OPENSIDDUR_CONTACT_EMAIL`; the Archive additionally asks that AI
agents name their model, via `--agent-model` or `$OPENSIDDUR_AGENT_MODEL`.
```bash
# All four stages in dependency order -- this is the one to run
uv run python -m opensiddur.importer.birnbaum_siddur.download

# ...or individually. The first three fetch; the fourth reconciles and must run last.
uv run python -m opensiddur.importer.birnbaum_siddur.wikisource         # text/ source/ external/
uv run python -m opensiddur.importer.birnbaum_siddur.en_wikisource      # en/
uv run python -m opensiddur.importer.birnbaum_siddur.internet_archive   # ia/
uv run python -m opensiddur.importer.birnbaum_siddur.correspondence     # pages.json
```
Every stage is a no-op when its source has not changed, down to leaving manifests
unwritten so an unchanged run produces no diff at all.
`pages.json` is the artifact every later stage reads: for each of the 815 leaves it gives the
IA leaf, the printed page number, which side of the opening it is, its facsimile URL, the
facing page, and which of the three sources its English text should come from. It is derived —
regenerate it, never hand-edit it. `correspondence.py --check` exits non-zero if any page
number could not be settled, for CI.

The Archive item and the Commons file Wikisource transcribes are the same scan (identical
SHA-1), which is what lets the two be paired: **IA leaf `n` is scan page `n + 1`**. Nothing
on disk is named by leaf number. Add `--with-djvu` for the 20 MB word-coordinate file the
segmentation stage needs, or `--fetch-pdf` to put the 488 MB scan in `output/` for reading
alongside; neither is committed. Note that `ia/ocr/` on a Hebrew page mixes Birnbaum's real
English footnotes with Hebrew that OCR misread as Latin, and is not usable prose until
segmentation has run.

**Sync reference database** after adding or updating projects:
```bash
uv run python -m opensiddur.exporter.refdb
```

## Architecture

### Data Flow

```
sources/          →  importer/  →  project/       →  exporter/  →  PDF
(raw source texts)   (→ JLPTEI)    (JLPTEI files)    (linear XML)
```

### Key Packages

**`opensiddur/exporter/`** — Compiles JLPTEI to linear intermediate XML for export.

- `compiler.py`, `external_compiler.py`, `inline_compiler.py`: Three processor classes handle the transclusion/annotation pipeline:
  - `CompilerProcessor` — base, processes full documents
  - `ExternalCompilerProcessor` — handles external transclusions (preserves element structure)
  - `InlineCompilerProcessor` — handles inline transclusions (extracts text only)
- `linear.py`: `LinearData` singleton (via `get_linear_data()`) holds shared processing state (XML cache, conditional settings stack, context stack, project priorities)
- `conditional_settings.py`, `condition_eval.py`, `derived_settings.py`: evaluate `j:conditional` scopes and derive calendar-related settings from declared feature values
- `calendar/compute.py`: computes Hebrew/Gregorian calendar, holiday, and Torah-reading feature values used by condition evaluation
- `urn.py` / `refdb.py`: `UrnResolver` and `ReferenceDatabase` resolve `urn:x-opensiddur:` URIs to files via SQLite
- `tex/latex.py`, `pdf/pdf.py`: LuaLaTeX/PDF output stages (driven by `tex/reledmac.xslt`; uses `reledmac` + `reledpar` for critical-edition apparatus and parallel-text alignment)
- `html/html.py`: the electronic-book output stage, one self-contained HTML file (driven by `html/html.xslt`). Compile with `--destination electronic` first. The undecided conditions are resolved on the reader's device, against the reader's settings and the device's clock, by `html/assets/condition.js`, a port of `condition_eval.py`/`client_settings.py` that is tested against them under Node (`$OPENSIDDUR_NODE`, or `node` on the PATH). `html/assets/calendar.js` ports the calendar derivations (`calendar/`, `derivation_graph.py`, `derived_settings.py`) the same way: a change to one needs the same change in the other
- `metadata.py`: the colophon model (licences, credits, and the sources from each project's `index.xml`), shared by the output stages, each of which only serialises the colophon (`build_colophon`)
- `cli_common.py`: what the output stages share — `-s/--settings` and `--project-directory`, the settings loader (`load_output_settings`: an unreadable or invalid file is an error; the projects it names are not checked) and the preparation of the compiled tree (`prepare_compiled_tree`)

The compiler uses a **processing context state machine** — see `specs/COMPILER_SPECIFICATION.md` for the full spec. Each context on the stack has a `command` field (`COPY_AND_RECURSE`, `COPY_ELEMENT_AND_RECURSE`, `RECURSE`, `SKIP`, `COPY_TEXT_AND_RECURSE`) controlling element handling.

**`opensiddur/importer/`** — Converts source texts to JLPTEI.

- `jps1917/`: JPS 1917 Bible translation from Wikisource (MediaWiki → JLPTEI)
- `birnbaum_siddur/`: Birnbaum ha-Siddur ha-Shalem, 1949, from three sources over one scan — Hebrew Wikisource (`wikisource.py`), English Wikisource (`en_wikisource.py`) and the Internet Archive's OCR (`internet_archive.py`), reconciled into `pages.json` by `correspondence.py` and sequenced by `download.py`
- `wlc/`: Westminster Leningrad Codex (structured data → JLPTEI via XSLT)
- `miqra_al_pi_hamasorah/`: Miqra al pi ha-Masorah (TSV/Wikidata → JLPTEI via XSLT)

- `util/wikisource.py`, `util/wikisource_book.py`, `util/internet_archive.py`: shared, book-agnostic clients for the Action API and archive.org, and the per-page download/manifest loop above them. Both clients honour `Retry-After`, back off exponentially, pace serially and identify themselves with a reachable address.

**`opensiddur/common/`** — Saxon-based XSLT 3.0 processing (`xslt.py`), shared constants.

### Schema

`schema/jlptei.odd.xml` is the source ODD (One Document Does it all). `build-schema.sh` compiles it to RelaxNG (`jlptei.odd.xml.relaxng`), Schematron (`jlptei.odd.xml.schematron`), and a Schematron XSLT stylesheet (`jlptei.odd.xml.schematron.xslt`). These compiled artifacts are gitignored; run `bash scripts/build-schema.sh` before validating. Validation uses RelaxNG plus Schematron (via the compiled XSLT).

`schema/JLPTEI-3.md` is prose authoring guidance. When it disagrees with `jlptei.odd.xml`, trust the ODD and run the validator.

### JLPTEI Authoring

**`j:` elements defined in the schema** (namespace `http://jewishliturgy.org/ns/jlptei/2`, prefix `j:`):
- `j:transclude` — include content from another file; `target` required, optional `targetEnd`, `type` optional (`external`|`inline`, default `external`)
- `j:divineName` — inline divine name for special downstream handling
- `j:read` / `j:written` — kri/ktiv pair inside `tei:choice`
- `j:declare` / `j:endDeclare` — scoped setting declarations; every `j:declare` must have `xml:id`, and matching `j:endDeclare` uses required `target`
- `j:conditional` / `j:endConditional` — conditional text blocks; `j:conditional` must have `xml:id` when closed by `j:endConditional`, which uses required `target`
- `j:condition` — first child of a standoff note (not an instruction); a condition deciding whether the whole note is set, evaluated where it would be set. Not a scope (no end marker); conditional words *inside* a note still use `j:conditional`
- `j:all` / `j:any` / `j:none` / `j:one` — boolean operators for conditions

**Settings registry.** Every `opensiddur:*` feature structure type, its features and the kind
of value each takes are listed in `opensiddur/exporter/features.yaml`. An unregistered type or
feature, or a value of the wrong kind, is an error in a `j:declare`, `j:conditional`,
`j:condition` or a settings file's `declarations`. A new setting is added to the registry first
(and, for a common type the exporter reasons about, to `schema/JLPTEI-3.md`). Check a project with
`uv run python -m opensiddur.exporter.validate_features [project ...]`. Tests whose feature names
are made up switch the check off with `registry_helpers.unchecked_registry()`.

Contributor credits are **not** a `j:` element. They belong in the TEI header as `tei:respStmt` entries with contributor URNs on `tei:name/@ref` (see `schema/JLPTEI-3.md`).
The shape `urn:x-opensiddur:contributor:<namespace>/<identifier>` is enforced by Schematron, and
every `opensiddur.org` identifier must have a line in `specs/urn_registry/contributor.jsonl` —
an unregistered one is a typo, and a typo credits a different person.

**Content-model and Schematron rules** (violations produce cryptic jing errors):
- `tei:TEI` must have `@xml:lang`
- `tei:revisionDesc` is excluded from the module includes — omit it
- `tei:head` must be a direct child of `tei:div`, never inside `tei:p`
- `tei:milestone` is allowed inside `tei:p` (it belongs to `tei_model.global`)
- `tei:standOff[@type]` only accepts `notes`, `settings`, or `conditions`
- `tei:p[@type]` only accepts `open-1`, `closed-1`, or `open-3`
- `tei:title[@type]` only accepts `main`, `sub`, `alt`, or `alt-sub`
- `tei:titlePage` goes in `tei:front`; `tei:titlePart[@type]` is a *different*, open list (`main`, `sub`, `alt`, `short`, `desc`) from `tei:title[@type]`
- `tei:imprimatur` takes inline content only — a `tei:p` inside it is invalid (`tei:epigraph` does take `tei:p`)

**Prefer milestone correspondences.** For repeated reference units (verses, prayer
parts, petitions, or stanzas), put the URN on `tei:milestone/@corresp` with a
consistent `@unit`, following the Tanach encodings. Keep the printed paragraph
and line structure independent of these boundaries. Higher-level `tei:div`
correspondences are appropriate for whole prayers and sections. Use `tei:seg`
for bounded quotations or other inline semantics, not merely to wrap each
repeating unit. When replacing a wrapper, preserve its exact reference scope:
terminate the milestone before unrelated text, rubrics, or a different unit
sequence using a same-unit milestone with no `corresp`. Retain `source` and
other semantic markup on the quoted span, and verify both transclusion ranges
and Hebrew/English alignment after regeneration.

**URN/`corresp` scoping**: A `corresp` on a `tei:milestone` scopes from that milestone to the next same-unit milestone, or end of file. This is the basis for parallel-text alignment: two documents share an alignment segment when they carry identical `corresp` values on their milestones.

**Project layout**: Every `project/<name>/` directory must have `index.xml` as its entry point. Individual text files refer back to the index via `tei:sourceDesc/tei:p/tei:ref` or a `tei:bibl/tei:ptr`.

**Naming** (`specs/NAMING_SCHEME.md`):
- A project is named `<title>-<author>-<date>-<lang>`, lowercase ASCII, with `-` between fields
  and `_` between the words of a field: `hasiddur_hashalem-birnbaum-1949-he`. The last field is
  the `xml:lang` of its `index.xml`. A translation shares its original's title. A source that
  romanizes its own name keeps that romanization as its title (Asher's *Selichoth* is
  `selichoth`), folded to lowercase ASCII.
- A book's settings live at `settings/<book.project>/<variant>.yaml`, so its release files are
  named after its project: `<project>-<variant>-<tag>.pdf`.
- File stems and URN path components are lowercase ASCII words joined by `_`. Hebrew words in
  any of these follow the transliteration table in `schema/JLPTEI-3.md` (het `ch`, khaf `kh`,
  qof `q`, tzadi `tz`, dagesh hazak doubled, final heh written), unless they have a common
  spelling listed in `specs/naming/spellings.yaml`. A file and a URN for the same text spell
  its words the same way.
- When you settle a spelling the table did not decide, add it to `spellings.yaml`. Check with
  `uv run python -m opensiddur.common.validate_names [project ...]`; pull requests to
  opensiddur-projects must pass it. A new variant in `spellings.yaml` makes the projects that
  still use the old spelling fail, so regenerate them in a paired PR with the same branch name.

### Testing Conventions

- Tests live in `opensiddur/tests/`, mirroring the package structure.
- Write tests in `unittest` style.
- Mock external calls (network APIs, file I/O where appropriate).
- The CI runs `unittest discover`, but `uv run pytest` also works locally.
- A pile of validation failures in a new worktree usually means the schema has not been
  compiled yet — see the setup step at the top of Commands.
