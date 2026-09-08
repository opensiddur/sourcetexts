# The 1949 printing, read off its scan

What the page says, written down page by page from the Internet Archive scan. The reading
is the evidence behind `project/birnbaum_ashkenaz_{he,en}_1949/` in the opensiddur-projects
repository: the TEI was authored from these files, not from any existing transcription.

```
readings/{printed}.md        what the page was read to say, in full
hebrew/{printed}.txt         the Hebrew lifted out of that reading
transcription/{printed}.txt  the Wikisource text for the same page, for comparison
```

`{printed}` is the printed page number, not the scan leaf. The mapping to leaves, and the
images themselves, live outside every repository — a leaf is re-fetchable from the Archive
and the enlarged bands are derived from it, so neither is worth keeping in git. See
`opensiddur/importer/birnbaum_scan/pages.py` in the opensiddur-ai repository.

`hebrew/` against `transcription/` is the diff that `specs/birnbaum_scan/accuracy.md`
reports, with `specs/birnbaum_scan/verdicts/` recording which side each difference was
decided for. Keeping the compared slice here is what lets that measurement be rechecked;
`transcription/` is Wikisource text and carries its licence, while the reading is ours. See
`../LICENSE.md`, sections 2 and 4.
