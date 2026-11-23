Exact /home/efeins/.codex/worktrees/marmorstein-processor/master/schema/JLPTEI-3.md lines1933–1965
1933: 
1934: In the first way, the processor is initialized with settings attributes without adding any XML markup. That way, a processor could produce a text that is valid (for example) for a given date/time combination. The processing model does not define how to initialize the processor, as that is defined by the processor itself (configuration files, command line parameters, looking up a calendar, etc).
1935: 
1936: Settings are declared in XML using the `j:declare` element. The part of the text where the setting's scope ends is at the matching `j:endDeclare` element, as shown here: 
1937: ```xml
1938: <tei:text>
1939:    ...
1940:    <j:declare xml:id="setting_start">
1941:       <tei:fs type="some_setting" xml:id="setting_one">
1942:          ...
1943:       </tei:fs>
1944:    </j:declare>
1945:    <!-- This is the scope of the declaration -->
1946:    <j:endDeclare target="#setting_start"/>
1947:    ....
1948: </tei:text>
1949: ```
1950: The `j:declare` element declares a set of `tei:fs` settings as in-scope.
1951: It must have an `xml:id` attribute that is referenced by 
1952: the `j:endDeclare` element. Every `j:declare` element must be matched with a `j:endDeclare` element that follows it as its sibling, so that every element that begins between the two also ends between them. If one were inside an element and the other outside it, leaving that element out (for a false condition, or outside a transcluded range) would separate the declaration from its end. The `j:declare` holds only `tei:fs` elements, each with a `@type` and at least one `tei:f`. It gives values, not alternatives: `tei:vAlt` and `tei:vNot` are for conditions. The schema enforces all of these.
1953: 
1954: Declaration blocks may be nested and declaration blocks may also cross each other's boundaries.
1955: 
1956: Within the JLPTEI processing model, if any attribute setting is changed and it has a downstream effect (for example, the current date is changed has a downstream effect on what holidays it might be), the downstream effects are recalculated at the point of the setting. If a set attribute goes out of scope, and that change had downstream effects, the downstream effects must also be recalculated using the previous scope.
1957: 
1958: #### Declaring conditions
1959: 
1960: The scope of a condition is started by the `j:conditional` element and closed by the `j:endConditional` element. The condition itself is specified within the `j:conditional` element.
1961: 
1962: The same condition syntax is used by `j:condition`, which decides whether a standoff note is set at all (see
1963: [Conditional notes](#conditional-notes)).
1964: 
1965: `j:conditional` elements must have an `xml:id` attribute, that `j:endConditional` elements reference in their `target` attribute to end the conditional scope.
