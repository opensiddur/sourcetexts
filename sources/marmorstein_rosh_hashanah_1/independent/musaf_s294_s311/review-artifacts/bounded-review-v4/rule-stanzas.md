Exact /home/efeins/.codex/worktrees/marmorstein-processor/master/schema/JLPTEI-3.md lines95–176
95: source's spelling (see [NAMING_SCHEME.md](../specs/NAMING_SCHEME.md)); the common spellings, and the known misspellings of other words, are listed in [`specs/naming/spellings.yaml`](../specs/naming/spellings.yaml). Otherwise:
96: 
97: | Letter/Vowel | Transliteration    |
98: |--------------|--------------------|
99: | Aleph        | not transliterated |
100: | Bet          | b                  |
101: | Vet          | v                  |
102: | Gimel        | g                  |
103: | Dalet        | d                  |
104: | Heh          | h                  |
105: | Vav          | v                  |
106: | Zayin        | z                  |
107: | Het          | ch                 |
108: | Tet          | t                  |
109: | Yod          | y                  |
110: | Kaf          | k                  |
111: | Khaf         | kh                 |
112: | Lamed        | l                  |
113: | Mem          | m                  |
114: | Nun          | n                  |
115: | Samekh       | s                  |
116: | Ayin         | not transliterated |
117: | Peh          | p                  |
118: | Feh          | f                  |
119: | Tzadi        | tz                 |
120: | Quf          | q                  |
121: | Resh         | r                  |
122: | Shin         | sh                 |
123: | Sin          | s                  |
124: | Tav          | t                  |
125: | Patah        | a                  |
126: | Qamatz       | a                  |
127: | Qamatz qatan | o                  |
128: | Hiriq        | i                  |
129: | Segol        | e                  |
130: | Tsere        | e                  |
131: | Holam        | o                  |
132: | Shuruq, Qubutz | u                |
133: | Hataf patah, Hataf segol, Hataf qamatz | a, e, o |
134: | Sheva na     | e                  |
135: | Sheva nach   | Not transliterated |
136: | Patah/Qamatz + yod | ai           |
137: | Tsere/Segol + yod | ei            |
138: 
139: And:
140: 
141: - **Dagesh hazak doubles** its letter within a word: `tefillah`, `ahavah_rabbah`, `attah`,
142:   `chayyim`, `kammah`. The dagesh a prefix brings to the next letter does not: `hasiddur`,
143:   `hamasorah`, `birkat_hamazon`, `mikol`, `bameh`. A letter written with two characters (`sh`,
144:   `ch`, `kh`, `tz`) is never doubled: `mitratzeh`, not `mitratztzeh`.
145: - **A shva is sounded** (`e`) under a word's first letter, under a doubled letter, as the
146:   second of two, and after a long vowel (qamatz, tsere, holam, shuruq, hiriq + yod): `berit`,
147:   `peri`, `malkhutekha`, `yotzerenu`, `virtzonekha`, and after the conjunction וּ: `uvemaqhalot`,
148:   `ukhetov`. After a short vowel it is silent: `lemaankha`, `miqdash`; so it is after a qamatz
149:   qatan, which is short (`zokhrenu`, `qorbanot`), and before a letter that takes a light dagesh
150:   (`ushpizin`).
151: - **The yod of the suffix ֶיךָ is not written**: segol + yod is `ei` (`vetechezeinah`), but
152:   before this suffix it is `e`, as it is said: `lefanekha`, `rachamekha`, `elekha`. Tsere + yod
153:   is always `ei`: `eloheinu`, `aleinu`.
154: - **A final heh is written** after its vowel: `minchah`, `retzeh`, `mosheh`. So is a mappiq heh.
155: - **Prefixes join their word**: the article and the prepositions (`ha`, `ve`/`u`, `be`, `le`,
156:   `ke`, `mi`, `she`) are written as part of the word they precede, with nothing between:
157:   `hashalem`, `bekhol`, `leleil`.
158: - **Nothing marks a dropped aleph or ayin**, not `_` and not an apostrophe: `vaanachnu`,
159:   `haaretz`, `asher_gealanu`.
160: 
161: 
162: For poems that aren't part of a prayer service (including _piyyutim_ and _z'mirot_), 
163: use the `poem` namespace. It uses the same transliteration rules as the `prayer` namespace above.
164: 
165: Passover haggadah projects use a dedicated `haggadah` namespace for seder-specific sections,
166: while reusing `prayer` for shared liturgy (kiddush, birkat hamazon) and `bible` for scriptural
167: quotations. See [HAGGADAH_URN_SCHEME.md](../specs/HAGGADAH_URN_SCHEME.md) for the hybrid scheme.
168: 
169: The Metsudah linear siddurim align their Hebrew and English phrase by phrase with the `metsudah`
170: namespace, `urn:x-opensiddur:text:metsudah:<text path>/<n>`: the *n*th phrase, as Metsudah divides it,
171: of the `prayer`, `poem` or `bible` text whose path it carries. See
172: [SIDDUR_URN_SCHEME.md](../specs/SIDDUR_URN_SCHEME.md#metsudah--the-phrases-of-the-metsudah-linear-layout).
173: 
174: To add URNs to reference parts of poems and prayers that don't have natural line divisions or have alternative numbers of lines, use the transliterated first word (or phrase, if the word is ambiguous) as the name of the division. For example `urn:x-opensiddur:text:poem:yonah_matzah/hayom` for the stanza in the song `יונה מצאה` that begins `היום אשר נא כצאן`.
175: 
176: ## URN scope
