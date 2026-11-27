from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,subprocess
root=Path('/home/efeins/src/opensiddur-repos/output/marmorstein_rosh_hashanah_2/morning_s25_s45/exports')
manifest=json.loads((root/'render_manifest.json').read_text());rows={}
for name,row in manifest.items():
 paths=[Path(row[k])for k in ['settings','print','electronic','pdf','html']if row.get(k)]
 paths+=sorted((root/name).glob('page-*.png'))+sorted((root/name).glob('browser-*.png'))+[root/name/'contact.jpg']
 rows[name]={str(p):hashlib.sha256(p.read_bytes()).hexdigest()for p in paths}
out={'status':'frozen_for_independent_presentation_review','created_utc':datetime.now(timezone.utc).isoformat(),'profiles':rows,'reports':{n:hashlib.sha256((root/n).read_bytes()).hexdigest()for n in ['pdf_qa.json','browser_qa.json','compile_manifest.json','render_manifest.json']}}
(root/'frozen_manifest.json').write_text(json.dumps(out,indent=2)+'\n');print('Frozen',len(rows),'profiles')
