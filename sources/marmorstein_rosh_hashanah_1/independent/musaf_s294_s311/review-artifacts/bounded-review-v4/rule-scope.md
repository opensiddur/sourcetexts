Exact /home/efeins/.codex/worktrees/marmorstein-processor/master/schema/JLPTEI-3.md lines208–260
208: 
209: Use `verse` for biblical verses and a descriptive unit such as `prayer-part` or
210: `petition` for the repeated liturgical unit. Adjacent units of the same kind
211: share a boundary. Explicitly terminate the sequence before unrelated prose,
212: speaker rubrics, source-only repetitions, or a switch of unit type; a paragraph
213: or division closing tag is not a milestone terminator. Preserve the former
214: wrapper's scope when converting existing encodings, and verify resolved URN
215: ranges as well as parallel rendering.
216: 
217: A `tei:seg` remains appropriate for a bounded quotation carrying `source`, a
218: language change, or other inline semantics. If that passage also needs a
219: correspondence, normally place its milestone before the semantic span. A short quotation
220: inside a larger aligned liturgical part may instead keep its own **quote-context** chapter
221: and verse milestones inside `tei:seg type="quotation"`: this keeps the inline phrase together
222: in the parallel row. Keep the enclosing liturgical correspondence outside the span, retain
223: canonical chapter/verse `@n` values, and close both inner scopes before the span ends. The
224: quotation's contextual URNs identify only its bounded extent; they must not advertise a
225: partial quotation as the canonical whole verse. Verify exact quoted-range resolution as
226: well as both-language rendering. Do not duplicate a canonical URN merely because the text
227: is printed again elsewhere.
228: 
229: ### Terminating a scope
230: 
231: Rule 2 runs a scope to the end of the file when nothing of the same unit follows, which
232: over-claims wherever a division ends partway through a file with no sibling after it — a
233: page of shared liturgy whose last paragraph belongs to no named prayer, for instance. The
234: terminator in rule 3 closes such a scope explicitly:
235: 
236: ```xml
237: <tei:milestone unit="prayer" n="1" corresp="urn:x-opensiddur:text:prayer:amidah/avot"/>
238: ...
239: <tei:milestone unit="prayer"/>   <!-- ends avot; starts nothing -->
240: ```
241: 
242: A terminator is not indexed, because only elements carrying `corresp` are, so it adds no
243: URN mapping and cannot be referenced.
244: 
245: This also applies to `half-verse` and `verse-part`. Their bare terminators have
246: neither `corresp` nor `n`; a numbered or named subdivision still requires its
247: canonical correspondence. A bare `verse` or `chapter` milestone cannot substitute
248: for a subverse terminator, because bare milestones close only their own unit.
249: 
250: **The unit must match exactly.** A bare milestone of some *other* unit does not terminate
251: anything, which is what keeps `unit="edition-verse"` — which carries `n` and never
252: `corresp` — from closing every verse it follows.
253: 
254: ## Versification
255: 
256: Editions of the Tanakh do not all divide the text into verses the same way, but a verse URN has to denote the
257: same words everywhere or nothing can be joined to anything. The URN space therefore has one **canonical** verse
258: division, and every project maps its own numbering onto it.
259: 
260: > **A canonical verse boundary is any point that is a verse boundary under _either_ ta'am elyon or ta'am
