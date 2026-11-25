Exact /home/efeins/.codex/worktrees/marmorstein-processor/master/schema/JLPTEI-3.md lines1991–2052
1991: ##### Kinds of rubric
1992: 
1993: A rubric is classified by what it does where it stands, not by its wording, and its kind decides
1994: how it is encoded:
1995: 
1996: - **A condition** says *when* the passage that follows is said: "On the Sabbath:", "With a
1997:   minyan:", "Between Rosh Hashanah and Yom Kippur add:". It is the `j:conditional`'s own
1998:   `tei:note type="instruction"`, and it means something only while the condition is unknown: it
1999:   is printed when the condition is `undefined`, and not at all when it is `true` or `false`.
2000: - **A directive** tells the reader to do or say something the text at that point does not
2001:   contain: "Mourners' Kaddish" where no kaddish follows, "The Ark is opened", "Stand". It is a
2002:   `tei:note type="instruction"` in the text, printed wherever its place is reached.
2003: - **A description** says *what* the passage printed after it is, who says it, or how: "Mourners'
2004:   Kaddish" before a transcluded kaddish (naming it, and implying all the instructions to
2005:   mourners), "Reader:", "In silent devotion:". It belongs to the passage. It is a
2006:   `tei:note type="description"` placed first inside the passage's scope, after the
2007:   `j:conditional`, and it is printed whenever the passage is: with it when the condition is
2008:   `true` or `undefined`, and left out with it when `false`.
2009: 
2010: The same words can be a directive in one edition and a description in another: an edition that
2011: prints only "Mourners' Kaddish" is telling the reader to say it, and one that transcludes the
2012: kaddish there is naming the text that follows. A rubric that says both when and what — "When the
2013: Reader repeats the Amidah, the following Kedushah is said:" — is a description, since leaving it
2014: out would lose the name of the passage.
2015: 
2016: ```xml
2017: <j:conditional xml:id="mourners_kaddish">
2018:    <tei:note type="instruction">With a minyan:</tei:note>
2019:    <tei:fs type="opensiddur:quorum">
2020:       <tei:f name="minyan"><tei:binary value="true"/></tei:f>
2021:    </tei:fs>
2022: </j:conditional>
2023: <tei:note type="description">Mourners' Kaddish.</tei:note>
2024: <j:transclude target="urn:x-opensiddur:text:prayer:kaddish/mourners"/>
2025: <j:endConditional target="#mourners_kaddish"/>
2026: ```
2027: 
2028: Descriptions and instructions are set alike: inline, as rubrics, with the edition's instruction
2029: priority choosing their wording.
2030: 
2031: ##### How an undecided scope is set off
2032: 
2033: A scope whose condition evaluates to `undefined` is kept, and how it is set off from the text
2034: around it follows the source:
2035: 
2036: - **`@type="marked"`**: the source itself marks the passage off, with brackets, parentheses or a
2037:   line. The standard delimiters are reproduced around it (brackets within running text, a rule
2038:   around blocks), with its instruction, if it has one.
2039: - **An instruction** and no `@type`: the instruction announces the passage, as the source's
2040:   rubric does, and a closing delimiter shows where it ends. The instruction may be the
2041:   conditional's own `tei:note`, or the `tei:note type="instruction"` or `type="description"`
2042:   the scope opens with.
2043: - **Neither**: the conditional is a direction to the processor, not to the reader, and the passage
2044:   is kept with no delimiters at all. The occasion conditions on a book's running order, around
2045:   the transclusion of each section that is said only on some days, are of this kind (see
2046:   [Conditions on a running order](#conditions-on-a-running-order)).
2047: 
2048: ##### Conditions on a running order
2049: 
2050: A section that is said only on some occasions -- the weekday services, the Sabbath services,
2051: Hallel, the festival services -- is conditioned at its transclusion in the running order: the
2052: outermost point at which the condition can be stated, so that one condition governs the whole
