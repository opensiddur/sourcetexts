Exact /home/efeins/.codex/worktrees/marmorstein-processor/master/schema/JLPTEI-3.md lines262–323
262: 
263: The two cantillations divide the Decalogue differently. Ta'am tachton merges the four short commandments into a
264: single verse — they are too short to stand alone — and reads אנכי together with לא יהיה לך. Ta'am elyon does the
265: reverse: one verse per commandment, so the four short ones are four verses, while the first two commandments
266: each run long. Neither division is a refinement of the other, but their union is finer than both, and every
267: edition's division is a coarsening of that union. An edition verse is therefore always a whole number of
268: consecutive canonical verses, which is what makes a mapping possible at all.
269: 
270: The canonical division is the one the Leningrad Codex numbers, so `tanakh-wlc-he` needs no mapping. Exodus 20 has **26**
271: canonical verses and Deuteronomy 5 has **33**:
272: 
273: | canonical | text | MAM (ta'am tachton) | JPS 1917 (common) |
274: |---|---|---|---|
275: | `exodus/20/2` | אנכי | 20:2 | 20:2 |
276: | `exodus/20/3` | לא יהיה לך | 20:2 | 20:3 |
277: | `exodus/20/13` | לא תרצח | 20:12 | 20:13 |
278: | `exodus/20/14` | לא תנאף | 20:12 | 20:13 |
279: | `exodus/20/15` | לא תגנב | 20:12 | 20:13 |
280: | `exodus/20/16` | לא תענה | 20:12 | 20:13 |
281: | `exodus/20/17` | לא תחמד | 20:13 | 20:14 |
282: | `exodus/20/26` | ולא תעלה במעלת | 20:22 | 20:23 |
283: 
284: A handful of chapters diverge for reasons unrelated to cantillation — a chapter boundary one verse further on,
285: a verse a witness does not contain. Those are recorded in `opensiddur/common/versification.py`, which is the
286: single place any edition's numbering is stated.
287: 
288: ### Recording an edition's own numbering
289: 
290: Two milestone units carry the two numberings, and they must not be confused:
291: 
292: | unit | `@corresp` | `@n` | role |
293: |---|---|---|---|
294: | `verse` | required, canonical URN | canonical number | identity, alignment, transclusion |
295: | `edition-verse` | **never** | the edition's own number | display only |
296: 
297: ```xml
298: <!-- Miqra al pi ha-Masorah, Exodus 20. One MAM verse, four canonical verses. -->
299: <tei:milestone unit="edition-verse" n="12"/>
300: <tei:p><tei:milestone unit="verse" n="13" corresp="urn:x-opensiddur:text:bible:exodus/20/13"/>לֹא תִרְצָח</tei:p>
301: <tei:p><tei:milestone unit="verse" n="14" corresp="urn:x-opensiddur:text:bible:exodus/20/14"/>לֹא תִנְאָף</tei:p>
302: <tei:p><tei:milestone unit="verse" n="15" corresp="urn:x-opensiddur:text:bible:exodus/20/15"/>לֹא תִגְנֹב</tei:p>
303: <tei:p><tei:milestone unit="verse" n="16" corresp="urn:x-opensiddur:text:bible:exodus/20/16"/>לֹא תַעֲנֶה</tei:p>
304: <tei:milestone unit="edition-verse" n="13"/>
305: <tei:milestone unit="verse" n="17" corresp="urn:x-opensiddur:text:bible:exodus/20/17"/>לֹא תַחְמֹד
306: ```
307: 
308: Because `edition-verse` carries no `@corresp`, the reference database and the parallel compiler — which look
309: only at `@corresp` — ignore it entirely. Canonical verse-number visibility is a rendering choice:
310: `typography.markers.verse_numbers` selects `shown` or `hidden`. Keep canonical `@n` values
311: when hiding numbers; edition-number labels remain separate display markers.
312: 
313: ### Rules
314: 
315: - **One milestone per canonical verse, exactly once per project.** A verse split across paragraphs by a
316:   parashah break in the middle of it is still one verse and keeps one milestone; its scope runs to the next
317:   verse milestone regardless of paragraph boundaries. Repeating the milestone gives the verse two identical
318:   `@corresp` values. Both the reference database and the parallel compiler keep only the first, drop the rest,
319:   and warn. A source may legitimately print the same text twice, even with different wording, so this is not an
320:   error; but only the first copy can be reached by its URN.
321: - **Never renumber to paper over a disagreement.** If an edition's verse count does not match the canonical
322:   one and the reason is not in the versification table, that is a defect in the importer or an unrecorded
323:   divergence, not something to be shifted into alignment.
