from pathlib import Path
import json,hashlib,subprocess,copy
P=Path('/home/efeins/.codex/worktrees/marmorstein-day-two-processor/master');S=Path('/home/efeins/.codex/worktrees/marmorstein-day-two-sources/master/sources/marmorstein_rosh_hashanah_2');B=S/'batches/pesuqei_s46_s63';PROJECT=Path('/home/efeins/.codex/worktrees/marmorstein-day-two-projects/master/project');HE='prayerbook_for_the_new_year_second_day-heidenheim-1965-he';EN='prayerbook_for_the_new_year_second_day-marmorstein-1965-en';EXP='machzor_expanded-opensiddur-he';ROOT='urn:x-opensiddur:text:siddur:rosh_hashanah/day_two'
def write(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads(Path('/tmp/day2-pesuqei-recipe-draft/readings.json').read_text(encoding='utf-8'));next(u for u in r['units']if u['stem']=='psalm_136')['edition_layout']='Hebrew: lead and refrain on each verse line, separated as right/left columns. English: refrain on a following line except short same-line verses2/3/8/17/18. No speaker identity inferred.';r['status']='Source-bound literal unit recipe; current approvals and batch acceptance are separate records.';write(B/'working/readings.json',r)
write(B/'segmentation_proof.json',json.loads(Path('/tmp/day2-pesuqei-recipe-draft/segmentation_proof.json').read_text(encoding='utf-8')))
spines=[HE+'/morning_prayers_service.xml',EN+'/morning_prayers_service.xml',EXP+'/second_day_morning.xml'];commit=subprocess.check_output(['git','-C',str(PROJECT.parent),'rev-parse','HEAD'],text=True).strip()
protected={str(p.relative_to(PROJECT)):sha(p)for proj in [HE,EN,EXP,'prayerbook_for_the_new_year-heidenheim-1965-he']for p in (PROJECT/proj).glob('*.xml')if str(p.relative_to(PROJECT))not in spines}
order=[]
for u in r['units']:
 item={'key':u['stem'],'expanded_target':u.get('start',u['urn'])}
 if u.get('start'):
  item['expanded_target']=u['start']+'-/'+u['end'].rsplit(':',1)[-1].split('/',1)[-1];item['documentary_target']=item['expanded_target']
 if u['stem']=='psalm_91_repeat':item.update(expanded_target='urn:x-opensiddur:text:bible:psalms/91/16',hebrew_only_repeat=True)
 if u['stem']=='psalm_136':
  v='urn:x-opensiddur:text:bible:psalms/136/';item['ranges']=[{'target':v+'1-/136/24','witnesses':['he','en']},{'target':v+'25','witnesses':['he']},{'target':v+'26','witnesses':['he','en']}]
 order.append(item)
settings={p:sha(PROJECT.parent/'settings'/p)for p in [HE+'/documentary_parallel.yaml',EXP+'/second_day_morning.yaml']}
corrections=[{'id':'source_s47_convenant','file':EN+'/chronicles_1_16_8_to_36.xml','sic':'convenant','corr':'covenant','before':'Remember for ever His ','after':', the word'},
 {'id':'source_s49_convenant','file':EN+'/chronicles_1_16_8_to_36.xml','sic':'convenant','corr':'covenant','before':'for Israel as an eternal ','after':','},
 {'id':'source_s49_withold','file':EN+'/vehu_rachum.xml','sic':'withold','corr':'withhold','before':'dost not ','after':' Thy compassion'},
 {'id':'source_s51_whem','file':EN+'/hoshiah_et_ammekha.xml','sic':'whem','corr':'whom','before':'Fortunate the people to ','after':' the like of this happens'}]
recipe={'batch':'pesuqei_s46_s63','readings_sha256':sha(B/'working/readings.json'),'source_approval_sha256':None,'order':order,'protected_files':protected,'settings_sha256':settings,'spine_templates':[{'path':p,'xml':(PROJECT/p).read_text(encoding='utf-8'),'sha256':sha(PROJECT/p),'baseline_commit':commit}for p in spines],'corrections':corrections}
write(B/'pesuqei_units.json',recipe)
registry=P/'specs/urn_registry/siddur.jsonl';known={x['urn'] for x in map(json.loads,registry.read_text(encoding='utf-8').splitlines())};records=[]
def add(urn,parent,label,refs=()):
 if urn in known:return
 known.add(urn);records.append({'urn':urn,'status':'context','parent':parent,'label_en':label,'references':list(refs),'note':'Documentary arrangement or repeated printing; canonical prayer/Bible identities are reused, not redefined.'})
add(ROOT+'/shacharit/pesuqei_dezimrah',ROOT+'/shacharit','Second-day Pesuqei deZimrah: documentary source sequence')
for u in r['units']:
 context=ROOT+'/morning_occurrences/'+u['stem'];parts=[p for lang in u['languages'].values()for p in lang]
 if u['urn'].startswith(ROOT+'/morning_occurrences/'):
  add(u['urn'],ROOT+'/morning_occurrences','Second-day source occurrence '+u['stem'],['urn:x-opensiddur:text:bible:psalms/91/16'])
 for part in parts:
  for key in ['chapter_corresp','corresp']:
   urn=part.get(key,'')
   if urn.startswith(context+'/'):
    add(context,ROOT+'/morning_occurrences','Second-day repeated printing '+u['stem'])
    add(urn,context,'Second-day source-bound '+u['stem']+' '+key,[part['source']] if part.get('source')else[])
with registry.open('a',encoding='utf-8')as f:
 for rec in records:f.write(json.dumps(rec,ensure_ascii=False)+'\n')
previous=json.loads((B/'registry_decisions.json').read_text(encoding='utf-8'))['new_context_records'] if (B/'registry_decisions.json').exists() else []
all_records=list({r['urn']:r for r in previous+records}.values())
write(B/'registry_decisions.json',{'new_context_records':all_records,'registry_reference':str(registry),'canonical_identity_audit':'identity_audit.json','note':'No new canonical prayer/Bible identity. Source repeated verses keep canonical source attribution; existing canonical providers remain protected.'})
print('Prepared15 source units,',len(protected),'protected files,',len(records),'registered context records. Generation still gated on current source and recipe approval.')
