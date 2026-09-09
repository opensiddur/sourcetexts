# The 1949 printing, read off its scan

What the page says, written down page by page from the Internet Archive scan. The reading
is the evidence behind `project/birnbaum_ashkenaz_{he,en}_1949/` in the opensiddur-projects
repository: the TEI was authored from these files, not from any existing transcription.

```
readings/{printed}.md        what the page was read to say, in full
hebrew/{printed}.txt         the Hebrew lifted out of that reading
transcription/{printed}.txt  the Wikisource text for the same page, for comparison
front/{section}.xml          the front matter, read straight into TEI
```

The front matter is read straight into TEI rather than into markdown first. For the body the
reading and the TEI are two artifacts, because the TEI is assembled from Python; in the front
matter the fragment *is* the reading, and the importer splices it in unchanged, so a parallel
prose copy would only drift away from it. The fragments cover scan leaves 1-25: the two title
leaves, the copyright page, the dedication, the acknowledgments and Birnbaum's introduction.
Both tables of contents are deferred.

`{printed}` is the printed page number, not the scan leaf. The mapping to leaves, and the
images themselves, live outside every repository — a leaf is re-fetchable from the Archive
and the enlarged bands are derived from it, so neither is worth keeping in git. See
`opensiddur/importer/birnbaum_scan/pages.py` in the opensiddur-ai repository.

`hebrew/` against `transcription/` is the diff that `specs/birnbaum_scan/accuracy.md`
reports in the opensiddur-ai repository, with `specs/birnbaum_scan/verdicts/` there
recording which side each difference was decided for. Keeping the compared slice here is what lets that measurement be rechecked;
`transcription/` is Wikisource text and carries its licence, while the reading is ours. See
`../LICENSE.md`, sections 2 and 4.
