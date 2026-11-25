from pathlib import Path
import json
p=Path('/tmp/mahzor-s238/iteration3/poem-units-revised.json');d=json.loads(p.read_text())
notes={
'musaf_vechayyot_asher_hennah':'The printed English follows the main Hebrew reading with Hayyah before Cherub. No English translation of the reversed Hebrew alternative is printed.',
'musaf_tehillot_kevodekha':'The printed English follows the main Hebrew readings rendered as “roared” and “Make straight, clear the way.” This edition prints no English alternatives for the corresponding Hebrew variants.',
'musaf_qedushah_conclusion_parts':'The printed English follows the main Hebrew readings rendered as “with Thy holiness” and “Awe-inspiring One.” This edition prints no English alternatives for the corresponding Hebrew variants.'}
for u in d['units']:
 if u['stem'] in notes:
  seq=u.setdefault('source_notes',{}).setdefault('en',[])
  if not any(n['text']==notes[u['stem']]for n in seq):seq.append(dict(language='en',text=notes[u['stem']]))
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
