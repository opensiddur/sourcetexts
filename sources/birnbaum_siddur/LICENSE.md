# Licensing of the Birnbaum ha-Siddur ha-Shalem sources

Two separate rights apply to the files in this directory, and they are not the same.
Anything derived from these files has to satisfy both.

## 1. The 1949 printed text — public domain in the United States

*ha-Siddur ha-Shalem* (The Daily Prayer Book), edited and translated by Philip (Paltiel)
Birnbaum, published 1949 by the Hebrew Publishing Company, New York.

The scanned source is hosted on Wikimedia Commons, which records it as public domain under
[`{{PD-US-not renewed}}`][commons]: a work published in the United States between 1929 and
1963 whose copyright was not renewed in its 28th year, as US law then required.

**This is public domain by non-renewal, not by expiration**, and the Commons file also carries
`{{Not-PD-US-expired-min-year}}` to say so. The distinction matters outside the United States:
non-renewal is a quirk of US law and has no effect elsewhere. Birnbaum died in 1988, so in
countries applying a life-plus-70 term the work is expected to remain in copyright until the
end of **2058**.

## 2. The Wikisource additions — CC BY-SA 4.0 International

This covers `text/`, `credits/`, `source/`, `external/` and `en/` — everything retrieved
from a Wikisource, Hebrew or English — and `scan_reading/transcription/`, which is a slice
of `source/` kept beside the reading it was compared against (section 4). It does **not** cover `ia/`, which has no wiki layer;
see section 3.

Everything so retrieved comes from Wikisource, whose text is licensed
[Creative Commons Attribution-ShareAlike 4.0 International][ccbysa] (CC BY-SA 4.0). That is the
license the site itself reports through its API (`meta=siteinfo&siprop=rightsinfo`), and it is
the license contributors agree to under the [Wikimedia Terms of Use][tou].

This layer is not a formality. **The Wikisource edition is not a faithful reproduction of the
1949 printing.** Its index page states that the edition renders Birnbaum's English rubrics into
Hebrew, adds Eretz Yisrael customs, and makes textual corrections. Those are original editorial
contributions by identifiable people, and they are what CC BY-SA covers — so the sections in
`source/` and `external/` carry rights that the underlying 1949 text does not.

## 3. The Internet Archive scan and its OCR — no additional rights

`ia/` holds material from the Internet Archive item
[`PhilipBirnbaumHaSiddurHaShalemTheDailyPrayerBook1949`][ia]: whole-book OCR derivatives
under `ia/derivatives/`, the per-page text sliced out of them under `ia/ocr/`, and the
item's own metadata in `ia/metadata.json`.

**It is the same scan as the Commons file in section 1** — not a similar one. The Archive
and Commons report the identical SHA-1 for the PDF,
`4208e06b5b212b5dc1631a4f096c660e95119d48`, at 488,138,938 bytes. That identity is the
whole basis for laying the Archive's OCR against the Wikisource transcription leaf by
leaf, so it is recorded here rather than left as an assumption; `ia/metadata.json`
preserves the Archive's own file list so the claim stays checkable.

Two consequences:

- **The 1949 layer is exactly as in section 1** — public domain in the United States by
  non-renewal, and only there. The Archive states the same reason in its own `rights`
  field, preserved in `ia/metadata.json`.
- **The OCR adds nothing.** It is machine-generated from those page images, and the
  Archive asserts no separate rights over it. There is no CC BY-SA layer on `ia/`, and no
  contributors to attribute — which is precisely why `en/` exists alongside it.

### What `ia/ocr/` actually contains

Worth stating plainly, because the files look more finished than they are:

- The OCR reads Hebrew as **Latin gibberish**. On a Hebrew page, what it produces is not
  Hebrew in any usable sense.
- Birnbaum set his English commentary as footnotes at the bottom of the Hebrew pages, and
  that English *is* read correctly — but it arrives interleaved with the gibberish in OCR
  reading order, with nothing marking where one ends and the other begins.
- So an `ia/ocr/NNN.txt` file for a Hebrew page is a **provenance record, not prose**.
  Separating the running head, body and footnote regions is a later stage's work, and
  nothing should quote these files as text until it has run.

## 4. The reading made off the scan — section 1 text, our transcription

`scan_reading/` holds what the printed page was read to say, page by page:
`readings/{printed}.md` is the reading itself, and `hebrew/{printed}.txt` is the Hebrew
lifted out of it. Both are transcriptions of the 1949 printing described in section 1, made
by reading the scan rather than by copying any existing transcription of it, so the
underlying text carries section 1's terms and nothing further attaches from section 2.

`scan_reading/transcription/{printed}.txt` is the exception and is **not** ours: it is a
slice of the Hebrew Wikisource text in `source/`, kept here so that the accuracy
measurement in the opensiddur-ai repository can be rechecked against exactly the words it
compared. It carries section 2's CC BY-SA 4.0 terms like the rest of `source/`.

The distinction matters because the two are meant to be laid side by side. A reader
comparing them is comparing a public-domain printing with a CC BY-SA edition of it, and the
obligations differ across that line.

## What this means downstream

- **Attribute the contributors.** The `credits/` files next to each page list the named
  Wikisource accounts who edited it. Those names are the attribution CC BY-SA requires, and
  they belong in the TEI header as `tei:respStmt` entries.
- **Share alike.** Work derived from this material must be released under CC BY-SA 4.0 or a
  compatible license.
- **Do not describe work built on the Wikisource layers as "Birnbaum 1949."** `source/`,
  `external/` and `text/` are the Wikisource edition of Birnbaum, which is a different text.
  `scan_reading/readings/` and `scan_reading/hebrew/` are the exception: they were read off
  the 1949 page itself and do describe that printing, which is the whole reason they were
  made.
- **Do not assume worldwide public domain.** Only the 1949 layer is public domain, and only in
  the United States.
- **Attribute the English contributors too.** `en/credits/NNN.txt` carries the same
  obligation for the English Wikisource pages that `credits/` carries for the Hebrew.
- **Do not quote `ia/ocr/` as text.** See section 3: on Hebrew pages it is unsegmented
  OCR mixing real English footnotes with Hebrew misread as Latin.

## Provenance

| | |
|---|---|
| Work | `Philip Birnbaum - ha-Siddur ha-Shalem (The Daily Prayer Book,1949).pdf` |
| Retrieved from | `he.wikisource.org` |
| Scan hosted at | Wikimedia Commons, digitised from the Internet Archive and the Open Siddur Project |
| Scan SHA-1 | `4208e06b5b212b5dc1631a4f096c660e95119d48` (488,138,938 bytes), identical on Commons and the Internet Archive |
| English pages retrieved from | `en.wikisource.org`, same file, `Page:` namespace |
| OCR retrieved from | `archive.org`, item `PhilipBirnbaumHaSiddurHaShalemTheDailyPrayerBook1949` |
| Author | Philip (Paltiel) Birnbaum, 1904–1988 |
| Publisher | Hebrew Publishing Company, New York, 1949 |

`manifest.json`, `en/manifest.json` and `ia/manifest.json` record the exact revision or
checksum of everything retrieved, so any claim here can be checked against the sources as
they stood at download time.

This file records what the sources say about licensing; it is not legal advice.

[ia]: https://archive.org/details/PhilipBirnbaumHaSiddurHaShalemTheDailyPrayerBook1949
[commons]: https://commons.wikimedia.org/wiki/File:Philip_Birnbaum_-_ha-Siddur_ha-Shalem_(The_Daily_Prayer_Book,1949).pdf
[ccbysa]: https://creativecommons.org/licenses/by-sa/4.0/
[tou]: https://foundation.wikimedia.org/wiki/Policy:Terms_of_Use
