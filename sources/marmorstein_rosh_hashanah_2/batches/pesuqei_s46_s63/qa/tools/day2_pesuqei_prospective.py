from pathlib import Path
import json,hashlib,shutil
from opensiddur.importer.marmorstein_rosh_hashanah_2.pesuqei import build_documents
from opensiddur.importer.scan.authoring import normalized_xml
from opensiddur.importer.util.validation import validate
S=Path('/home/efeins/.codex/worktrees/marmorstein-day-two-sources/master/sources/marmorstein_rosh_hashanah_2');B=S/'batches/pesuqei_s46_s63';project=Path('/home/efeins/.codex/worktrees/marmorstein-day-two-projects/master');out=Path('/tmp/day2-pesuqei-prospective');out.mkdir(exist_ok=True)
recipe=json.loads((B/'pesuqei_units.json').read_text());units={u['stem']:u for u in json.loads((B/'working/readings.json').read_text())['units']};docs=build_documents(recipe,units)
if not (out/'project').exists():shutil.copytree(project/'project',out/'project');shutil.copytree(project/'settings',out/'settings')
rows=[]
for rel,root in docs:
 p=out/'project'/rel;p.parent.mkdir(exist_ok=True);p.write_text(normalized_xml(root),encoding='utf-8');ok,errors=validate(p);rows.append({'path':rel,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'valid':ok,'errors':list(map(str,errors))})
assert all(x['valid']for x in rows),[x for x in rows if not x['valid']]
D=B/'qa';D.mkdir(exist_ok=True);(D/'prospective_schema.json').write_text(json.dumps({'status':'passed_prospective_xml_only','question1023_pending':True,'recipe_sha256':hashlib.sha256((B/'pesuqei_units.json').read_bytes()).hexdigest(),'documents':rows},indent=2)+'\n')
for src,dest in [('/tmp/day2-pesuqei-source-v4-closure.json',S/'independent/pesuqei_s46_s63/source_v4_closure.json'),('/tmp/day2-pesuqei-final-source-46-51-closure.json',S/'independent/pesuqei_s46_s63/source46_51_sol_final/closure.json')]:shutil.copyfile(src,dest)
print('All',len(rows),'prospective documents valid; no actual project files changed')
