from pathlib import Path
import json,copy,yaml
from lxml import etree
from opensiddur.importer.scan.authoring import apply_corrections
from opensiddur.importer.marmorstein_rosh_hashanah_1.build import unit_document,document,element,PROJECTS,ROOT_URN,unit_urn,validate
p=Path('/tmp/mahzor-s238/iteration3');qa=p/'qa-projects';units=json.loads((p/'poem-units-revised.json').read_text())['units'];reports=[]
for lang,project in PROJECTS.items():
 dest=qa/project;dest.mkdir(parents=True,exist_ok=True)
 root,body=document(lang,project,'DRAFT: seven-module alignment check only',ROOT_URN,index=True,draft=True);div=element(body,'div',corresp=ROOT_URN)
 for u in units:
  if u['stem']=='musaf_haochez_beyad_middat_mishpat'and lang=='he':element(div,'note','פותחים הארון.',type='instruction')
  doc=unit_document(u,lang,True)
  file=project+'/'+u['stem']+'.xml'
  corrections=[c for c in json.loads((p/'pending-corrections.json').read_text())['corrections']if c['file']==file]
  if corrections:apply_corrections({file:doc},corrections)
  text=etree.tostring(doc,encoding='unicode');f=dest/(u['stem']+'.xml');f.write_text(text);ok,errors=validate(text);reports.append(dict(file=str(f),valid=ok,errors=errors))
  element(div,'j:transclude',type='external',target=unit_urn(u)+'@'+project)
  if u['stem']=='musaf_haochez_beyad_middat_mishpat'and lang=='he':element(div,'note','סוגרים הארון.',type='instruction')
 (dest/'index.xml').write_text(etree.tostring(root,encoding='unicode'))
base=yaml.safe_load(Path('/home/efeins/.codex/worktrees/marmorstein-projects/master/settings/prayerbook_for_the_new_year-heidenheim-1965-he/with_translation.yaml').read_text());base['description']='DRAFT isolated seven-module alignment test, not the complete service.';base['book']['title']='DRAFT poem alignment only'
for state in ['unknown','included','omitted']:
 cfg=copy.deepcopy(base)
 if state!='unknown':
  cfg['declarations']={'opensiddur:variant':{'urn:x-opensiddur:condition:poem:haochez_beyad_middat_mishpat/hehagui/vehoveh':state=='included','urn:x-opensiddur:condition:poem:v_yeetayu_kol_leavdekha/veyizbechu':state=='included'}}
 cfg['readings']={'abbreviations':'expanded'}
 (p/(state+'.yaml')).write_text(yaml.safe_dump(cfg,allow_unicode=True,sort_keys=False))
(p/'schema-revised.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2)+'\n');print(sum(x['valid']for x in reports),'/',len(reports),'schema-valid revised source witnesses')
