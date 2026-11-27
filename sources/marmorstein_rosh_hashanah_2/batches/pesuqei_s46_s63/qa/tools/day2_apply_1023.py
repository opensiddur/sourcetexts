from pathlib import Path
import json,hashlib,shutil
from datetime import datetime,timezone
S=Path('/home/efeins/.codex/worktrees/marmorstein-day-two-sources/master/sources/marmorstein_rosh_hashanah_2');B=S/'batches/pesuqei_s46_s63'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=B/'working/adjudicated_pages.json';source=json.loads(p.read_text(encoding='utf-8'));page=next(x for x in source['pages']if x['scan']==62);line=page['blocks'][2]['lines'][5];assert line.endswith('כְּמוֹ־');assert page['blocks'][2]['lines'][6].startswith('עֵֽשֶׂב')
r=B/'working/readings.json';units=json.loads(r.read_text(encoding='utf-8'))['units'];unit=next(x for x in units if x['stem']=='psalm_92');v=next(x for x in unit['languages']['he']if x.get('corresp')=='urn:x-opensiddur:text:bible:psalms/92/8');assert 'כְּמוֹ־עֵֽשֶׂב' in ' '.join(x['text']for x in v['fragments'])
record={'question':1023,'scan':62,'reference':'urn:x-opensiddur:text:bible:psalms/92/8','user_answer':'Printed maqaf','duplicate_answer':'Both pending question cards received the same answer.','resolved_utc':datetime.now(timezone.utc).isoformat(),'decision':'Retain U+05BE joining כְּמוֹ to עֵֽשֶׂב across the printed line break.','source_before_sha256':sha(p),'source_after_sha256':sha(p),'working_readings_before_sha256':sha(r),'working_readings_after_sha256':sha(r),'text_changed':False,'explanation':'The reviewed provisional reading already encoded the confirmed maqaf. Only its unresolved status changes. No source text, boundaries, recipe, generated XML or rendered artifact changes.','source_context':[line,page['blocks'][2]['lines'][6]],'evidence_image':json.loads((B/'questions_1023.json').read_text())['questions'][0]['image']};write(B/'human_answer_1023.json',record)
q=json.loads((B/'questions_1023.json').read_text());q['questions'][0].update(status='resolved_by_user',answer='Printed maqaf',application='human_answer_1023.json');write(B/'questions_1023.json',q)
print('Confirmed existing maqaf; source and literal recipe hashes unchanged',sha(p),sha(r))
