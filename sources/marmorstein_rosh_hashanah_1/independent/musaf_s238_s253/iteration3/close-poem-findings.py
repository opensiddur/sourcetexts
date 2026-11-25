from pathlib import Path
import json,copy,re,unicodedata
p=Path('/tmp/mahzor-s238/iteration3');d=json.loads((p/'draft-poem-units-v2.json').read_text());N=lambda s:unicodedata.normalize('NFKD',s)
by={u['stem']:u for u in d['units']};decisions=[]
# Printed paragraphs do not follow the role or alignment boundaries.
u=by['musaf_vechayyot_asher_hennah']
for s,n in zip(u['languages']['he'],[1,1,2,3,4]):s['paragraph']=n
u['source_notes']={'en':[dict(language='en',text='This edition translates only the concluding Rachem Metzuqim stanza. The preceding Hebrew stanzas have no printed English translation.') ]}
u.pop('partial_translation_note',None)
decisions.append('Vechayyot/Chashot share the printed paragraph on238. KafRegel on240 is a new source strophe, evidenced by the preceding colon and its new congregation cue; its identity is not derived from the page turn.')
u=by['musaf_veammekha_teluyim']
for s,n in zip(u['languages']['he'],[1,1,1,2,2,3]):s['paragraph']=n
for lang,ss in u['languages'].items():
 for s in ss:
  if s.get('corresp','').endswith('/kol_shofar'):s.pop('corresp');s.pop('reference_unit')
decisions.append('Vammecha continues across240242 without a paragraph or reference boundary at QolShofar. Semukhim remains an independently identified speaker stanza within the same printed paragraph.')
u=by['musaf_veattah_ezon_qol']
for s,n in zip(u['languages']['he'],[1,1,2]):s['paragraph']=n
u['languages']['he'][1].update(corresp=u['urn']+'/sam',reference_unit='stanza')
s=u['languages']['en'][0];f=s['fragments'][0];at='The paths of the world';before,after=f['text'].split(at,1);f['text']=before
new=copy.deepcopy(s);new['fragments'][0]['text']=at+after;new['corresp']=u['urn']+'/sam';new['reference_unit']='stanza';s.pop('end_reference',None);u['languages']['en'].insert(1,new)
# Incipit names follow the source and the general transliteration table.
renames={'veammekha_teluyim':'veammekha_teluim','tehillot_kevodkha':'tehillot_kevodekha','/lehizakher':'/lehizzakher','/yissau':'/yisu','/od_yizkor':'/od_yizkar'}
def rename(v):
 if isinstance(v,str):
  for old,new in renames.items():v=v.replace(old,new)
  return N(v)
 if isinstance(v,list):return[rename(x)for x in v]
 if isinstance(v,dict):return{k:rename(x)for k,x in v.items()}
 return v
d=rename(d);by={u['stem']:u for u in d['units']}
# Ki Maqdishekha and Od Yizkar retain separate canonical identities, independent of their shared source paragraph.
u=by['musaf_ki_maqdishekha'];old=u['urn'];ki='urn:x-opensiddur:text:prayer:amidah/ki_maqdishekha';od='urn:x-opensiddur:text:prayer:od_yizkar_lanu';u.update(stem='musaf_qedushah_conclusion_parts',urn='urn:x-opensiddur:text:siddur:rosh_hashanah/musaf/qedushah_conclusion_parts',map_root=False)
for lang,ss in u['languages'].items():
 for s in ss:
  s['paragraph']=1
  if s.get('corresp'):s['corresp']=od if s['corresp'].endswith('/od_yizkar')else ki;s['reference_unit']='prayer'
# Role descriptions are related to their stanza, and start inside that scope.
for u in d['units']:
 for ss in u['languages'].values():
  for s in ss:s.pop('speaker_before_reference',None)
# Preserve every printed variant siglum as an apparatus annotation; name each reading independently.
for u in d['units']:
 u['citations']=u.get('citations',{})
 serial=0
 for lang,ss in u['languages'].items():
  for s in ss:
   for f in s['fragments']:
    if N('אָיוֹם (נ״א היום)')in f['text']and not f.get('alternatives'):
     f['alternatives']=[dict(printed=N('אָיוֹם (נ״א היום)'),readings=[N('אָיוֹם'),'היום'])]
    for alt in f.get('alternatives',[]):
     serial+=1;identifier=u['stem']+'_source_variant_'+str(serial);alt['xml_id']=identifier
     alt['readings']=[dict(text=t,corresp='urn:x-opensiddur:condition:'+u['urn'].partition(':text:')[2]+'/source_variant_'+str(serial)+'/'+str(i))for i,t in enumerate(alt['readings'],1)]
     u['citations'].setdefault(lang,[]).append(dict(scan=f['scan'],language='he',note_type='annotation',target='#'+identifier,text='נ״א',abbreviations=[dict(abbr='נ״א',expan='נוסח אחר')]))
# Ha-ohez: one stable incipit stanza per source row; its printed column labels govern every row.
u=next(u for u in d['units']if u['stem']=='musaf_haochez_beyad_middat_mishpat');u['join_source_fragments']=True
incipits=['haochez','habochen','hagoel','hadan','hehagui','havaddai','hazokher','hachotekh','hatov','hayodea','hakol','halan','hamamlikh','hanoheg','hasovel','haelyon','hapoteach','hatzofeh','haqetzar','harachum','hashaveh','hatam']
condition='urn:x-opensiddur:condition:poem:haochez_beyad_middat_mishpat/hehagui/vehoveh'
for lang,ss in list(u['languages'].items()):
 out=[]
 for i,s in enumerate(ss):
  s['corresp']=u['urn']+'/'+incipits[i]
  if lang=='he':
   f=s['fragments'][0];call,response=f['text'].split(':',1);f['text']=call+':'
   response_frag=copy.deepcopy(f);response_frag['text']=response
   # The abbreviation belongs only to the response, never to the reader's hemistich.
   f.pop('abbreviations',None)
   resp=dict(paragraph=s['paragraph'],fragments=[response_frag])
   if i==0:
    s['speaker']=dict(label='חזן.',language='he',role='reader');resp['speaker']=dict(label='קהל.',language='he',role='congregation')
   if s.get('end_reference'):s.pop('end_reference');resp['end_reference']=True
   out.extend([s,resp])
  else:out.append(s)
 # Split the optional word without giving its condition ownership of the stanza boundary.
 idx=next(j for j,s in enumerate(out)if N('(וְהֹוֶה)')in s['fragments'][0]['text'])if lang=='he'else 4
 s=out[idx];f=s['fragments'][0];needle=N('(וְהֹוֶה)')if lang=='he'else', is';before,after=f['text'].split(needle,1);f['text']=before
 optional=copy.deepcopy(f);optional['text']=needle;optional.pop('abbreviations',None)
 tail=copy.deepcopy(f);tail['text']=after;tail.pop('abbreviations',None)
 if lang=='en':f['join_next']=True
 opt=dict(paragraph=s['paragraph'],conditions=[dict(type='opensiddur:variant',features={condition:True})],fragments=[optional])
 if lang=='he':opt['marked']=True
 suffix=dict(paragraph=s['paragraph'],fragments=[tail])
 out[idx+1:idx+1]=[opt,suffix];u['languages'][lang]=out
# Exact source directives will sit in source/expanded order outside the prayer-word work.
d['integration_directives']={'before_haochez':dict(scan='s248',text='פותחים הארון.',language='he',witnesses=['he']),'after_haochez':dict(scan='s250',text='סוגרים הארון.',language='he',witnesses=['he'])}
d['encoding_decisions']=decisions+['Speaker descriptions follow each stanza milestone; source row/column headings in Haochez are preserved once, not invented afresh on every row.','קו״ח continues the already accepted project mapping to reader_and_congregation, meaning both participants. No sequential timing is inferred from the order of the abbreviation letters.','The partial English witness is explicitly documented in sourceDesc, following the general partial-witness policy.','The project currently marks the unambiguous Tetragrammaton and its abbreviated forms; other divine epithets remain literal pending a separate context-sensitive annotation policy. This is consistent with earlier accepted material.','New canonical units/conditions/names remain provisional until registry and full-service integration checks pass.']
d['status']='Revised draft after independent encoding audit; source human362+ and final closure/integration/export still pending.'
(p/'poem-units-revised.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');print('Refined7modules: paragraph/role scopes,8canonical works, named apparatus, bilingual optional-word condition')
