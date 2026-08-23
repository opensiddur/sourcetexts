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

Everything in this directory was retrieved from Hebrew Wikisource, whose text is licensed
[Creative Commons Attribution-ShareAlike 4.0 International][ccbysa] (CC BY-SA 4.0). That is the
license the site itself reports through its API (`meta=siteinfo&siprop=rightsinfo`), and it is
the license contributors agree to under the [Wikimedia Terms of Use][tou].

This layer is not a formality. **The Wikisource edition is not a faithful reproduction of the
1949 printing.** Its index page states that the edition renders Birnbaum's English rubrics into
Hebrew, adds Eretz Yisrael customs, and makes textual corrections. Those are original editorial
contributions by identifiable people, and they are what CC BY-SA covers — so the sections in
`source/` and `external/` carry rights that the underlying 1949 text does not.

## What this means downstream

- **Attribute the contributors.** The `credits/` files next to each page list the named
  Wikisource accounts who edited it. Those names are the attribution CC BY-SA requires, and
  they belong in the TEI header as `tei:respStmt` entries.
- **Share alike.** Work derived from this material must be released under CC BY-SA 4.0 or a
  compatible license.
- **Do not describe the result as "Birnbaum 1949."** It is the Wikisource edition of Birnbaum,
  which is a different text.
- **Do not assume worldwide public domain.** Only the 1949 layer is public domain, and only in
  the United States.

## Provenance

| | |
|---|---|
| Work | `Philip Birnbaum - ha-Siddur ha-Shalem (The Daily Prayer Book,1949).pdf` |
| Retrieved from | `he.wikisource.org` |
| Scan hosted at | Wikimedia Commons, digitised from the Internet Archive and the Open Siddur Project |
| Author | Philip (Paltiel) Birnbaum, 1904–1988 |
| Publisher | Hebrew Publishing Company, New York, 1949 |

`manifest.json` records the exact revision of every page retrieved, so any claim here can be
checked against the wiki as it stood at download time.

This file records what the sources say about licensing; it is not legal advice.

[commons]: https://commons.wikimedia.org/wiki/File:Philip_Birnbaum_-_ha-Siddur_ha-Shalem_(The_Daily_Prayer_Book,1949).pdf
[ccbysa]: https://creativecommons.org/licenses/by-sa/4.0/
[tou]: https://foundation.wikimedia.org/wiki/Policy:Terms_of_Use
