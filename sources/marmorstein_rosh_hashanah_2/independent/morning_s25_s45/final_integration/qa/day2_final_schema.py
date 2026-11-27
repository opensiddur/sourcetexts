from pathlib import Path
import json, hashlib
from opensiddur.importer.util.validation import validate
p=Path('/home/efeins/.codex/worktrees/marmorstein-day-two-projects/master/project')
paths=sorted((p/'prayerbook_for_the_new_year_second_day-heidenheim-1965-he').glob('*.xml'))+sorted((p/'prayerbook_for_the_new_year_second_day-marmorstein-1965-en').glob('*.xml'))+[p/'machzor_expanded-opensiddur-he/second_day_morning.xml',p/'machzor_expanded-opensiddur-he/second_night.xml']
rows=[]
for f in paths:
 ok,errors=validate(f);rows.append({'file':str(f.relative_to(p)),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'valid':ok,'errors':list(map(str,errors))})
 if not ok:print(f,errors,flush=True)
Path('/tmp/day2-final-schema.json').write_text(json.dumps({'status':'passed'if all(r['valid'] for r in rows)else'failed','documents':rows},indent=2)+'\n');print(len(rows),'documents',sum(not r['valid'] for r in rows),'failures')
