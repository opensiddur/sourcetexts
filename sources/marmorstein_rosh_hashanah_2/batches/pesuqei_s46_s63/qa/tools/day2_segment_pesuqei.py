"""Build draft boundary recipes from independently read volume-two words.

The first-day witness supplies only boundary anchors and registered identities.
Every emitted prayer word comes from adjudicated volume-two source pages.
The coverage proof and independent alignment review must close before approval.
"""
from pathlib import Path
import json,re,unicodedata,hashlib,difflib,copy
S=Path('/home/efeins/.codex/worktrees/marmorstein-day-two-sources/master/sources');B=S/'marmorstein_rosh_hashanah_2/batches/pesuqei_s46_s63';D=Path('/tmp/day2-pesuqei-recipe-draft');D.mkdir(exist_ok=True)
ROOT='urn:x-opensiddur:text:siddur:rosh_hashanah/day_two';BIBLE='urn:x-opensiddur:text:bible:'
STEMS=['barukh_sheamar','chronicles_1_16_8_to_36','romemu','vehu_rachum','hoshiah_et_ammekha','psalm_19','psalm_34','psalm_90','psalm_91','psalm_91_repeat','psalm_135','psalm_136','psalm_33','morning_psalm_92','morning_psalm_93']
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def nrm(t):return re.sub(r'[^\w]','',re.sub('[\u0591-\u05c7\u034f]','',unicodedata.normalize('NFC',t))).lower()
def tokens(t):return re.findall(r'\S+',t)
def join(ts):return ' '.join(ts).replace('־ ','־')
old=json.loads((S/'marmorstein_rosh_hashanah_1/readings.json').read_text(encoding='utf-8'));refs={u['stem']:u for u in old['units']};source=json.loads((B/'working/adjudicated_pages.json').read_text(encoding='utf-8'));pages=source['pages'];units=[]
for stem in STEMS:
 r=refs[stem];u={k:copy.deepcopy(r[k])for k in ['stem','urn','title','poetry','start','end','map_root','translation_omissions','edition_layout']if k in r};u['languages']={}
 if stem.startswith('morning_psalm_'):
  number=stem.rsplit('_',1)[-1];u['stem']='psalm_'+number;u['urn']=BIBLE+'psalms/'+number
 if stem=='psalm_91_repeat':u['urn']=ROOT+'/morning_occurrences/psalm_91_repeat';u['map_root']=True
 units.append(u)
report={'status':'draft_boundary_mapping_not_source_approval','input_page_sha256':sha(B/'working/adjudicated_pages.json'),'boundary_reference_sha256':sha(S/'marmorstein_rosh_hashanah_1/readings.json'),'languages':{},'all_words_from_new_source':True,'ambiguous_boundaries':[]}
for lang in ['he','en']:
 src=[]
 for page in pages:
  if page['language']!=lang:continue
  for bi,block in enumerate(page['blocks']):
   if block['kind']=='citation':continue
   text=block['text']
   for ti,t in enumerate(tokens(text)):
    src.append({'word':t,'scan':'s'+str(page['scan']),'printed_page':page['printed_page'],'block':bi,'word_index':ti})
 reference=[];segments=[]
 for ui,stem in enumerate(STEMS):
  for pi,part in enumerate(refs[stem]['languages'].get(lang,[])):
   start=len(reference)
   for f in part['fragments']:reference.extend(tokens(f['text']))
   segments.append((ui,pi,start,len(reference),part))
 matcher=difflib.SequenceMatcher(a=[nrm(t)for t in reference],b=[nrm(t['word'])for t in src],autojunk=False)
 bounds={0:0,len(reference):len(src)};ops=matcher.get_opcodes()
 for tag,a,z,b,c in ops:
  if tag=='equal':
   for i in range(z-a+1):bounds[a+i]=b+i
  else:
   bounds.setdefault(a,b);bounds[z]=c
 differences=[{'kind':tag,'reference_tokens':reference[a:z],'source_tokens':[t['word']for t in src[b:c]],'source_positions':src[max(0,b-2):min(len(src),c+2)]}for tag,a,z,b,c in ops if tag!='equal']
 seen=[];mapping=[]
 for ui,pi,a,z,part in segments:
  if a not in bounds or z not in bounds:
   report['ambiguous_boundaries'].append({'language':lang,'unit':STEMS[ui],'part':pi,'old_start':a,'old_end':z})
   continue
  b,c=bounds[a],bounds[z];assert b<=c
  selected=src[b:c]
  if not selected:raise ValueError(('Empty mapped source part',lang,STEMS[ui],pi))
  seen.extend(range(b,c));newpart={k:copy.deepcopy(v)for k,v in part.items()if k not in ['fragments','canonical','canonical_end','transclude','repeat','conditions','condition_end_corresp','marked','wording_selection']}
  if part.get('canonical'):newpart['corresp']=part['canonical']
  fragments=[]
  cursor=a
  for original_fragment in part['fragments']:
   stop=cursor+len(tokens(original_fragment['text']))
   if cursor not in bounds or stop not in bounds:raise ValueError(('Ambiguous semantic fragment',lang,STEMS[ui],pi))
   fragment_start,fragment_end=bounds[cursor],bounds[stop]
   for offset,t in enumerate(src[fragment_start:fragment_end]):
    absolute=fragment_start+offset
    if offset==0 or fragments[-1]['scan']!=t['scan']:
     fragment={'scan':t['scan'],'printed_page':t['printed_page'],'words':[],
               'page_start':absolute==0 or src[absolute-1]['scan']!=t['scan']}
     if original_fragment.get('text_type'):fragment['text_type']=original_fragment['text_type']
     fragments.append(fragment)
    fragments[-1]['words'].append(t['word'])
   cursor=stop
  for fi,f in enumerate(fragments):
   f['text']=join(f.pop('words'))
   if fi+1<len(fragments)and f['text'].endswith('־'):f['join_next']=True
  newpart['fragments']=fragments
  u=units[ui]
  if STEMS[ui] in ['morning_psalm_92','morning_psalm_93']:
   newpart['corresp']=newpart.pop('source');newpart.pop('reference_unit',None)
  if STEMS[ui]=='psalm_91_repeat':
   newpart.update(corresp=u['urn']+'/quote/psalms/91/16',source=BIBLE+'psalms/91/16',reference_unit='verse',chapter_corresp=u['urn']+'/quote/psalms/91')
  overlaps={BIBLE+'psalms/'+i for i in ['19/15','20/10','25/6','46/8','84/13']}
  if newpart.get('corresp')in overlaps:
   canonical=newpart['corresp'];bookpath=canonical.rsplit(':',1)[-1]
   newpart.update(corresp=ROOT+'/morning_occurrences/'+u['stem']+'/quote/'+bookpath,source=canonical,reference_unit='verse')
  if newpart.get('source','').startswith(BIBLE) and not newpart.get('corresp','').startswith(BIBLE):newpart['reference_unit']='verse'
  u['languages'].setdefault(lang,[]).append(newpart)
  mapping.append({'unit':u['stem'],'part':pi,'reference_bounds':[a,z],'source_bounds':[b,c],'source_first':selected[0],'source_last':selected[-1]})
 assert sorted(seen)==list(range(len(src))),('Words not covered exactly once',lang,len(src),len(seen),report['ambiguous_boundaries'])
 report['languages'][lang]={'source_token_count':len(src),'reference_token_count':len(reference),'alignment_ratio':matcher.ratio(),'differences':differences,'mappings':mapping,'all_source_tokens_covered_once':True}
# New source-attested citations; source labels are retained verbatim except display parentheses removal by renderer.
for u in units:
 citations={}
 for lang,parts in u['languages'].items():
  opening=parts[0]['fragments'][0];pg=next(p for p in pages if 's'+str(p['scan'])==opening['scan'])
  oldstem=next(st for st in STEMS if ('psalm_'+st.rsplit('_',1)[-1] if st.startswith('morning_psalm_')else st)==u['stem'])
  if refs[oldstem].get('citations',{}).get(lang):
   # Locate the source citation preceding this unit, verified subsequently against source layout.
   cs=[x for x in pg['blocks']if x['kind']=='citation']
   expected=refs[oldstem]['citations'][lang][0]['text']
   matches=[x for x in cs if x['text'].strip()==expected.strip()]
   if not matches:raise ValueError(('Citation not verified on new sourcepage',u['stem'],lang,expected))
   text=matches[0]['text'];target=parts[0]['corresp'];ref=u['urn']
   if u['stem']=='chronicles_1_16_8_to_36':text=text.replace('16, 8','16:8');ref=BIBLE+'chronicles_1/16/8'
   citations[lang]=[{'scan':opening['scan'],'printed_page':opening['printed_page'],'text':text,'target':target,'reference':ref}]
 if citations:u['citations']=citations
write(D/'readings.json',{'status':'draft_after_source_adjudication; independent source/boundary approval pending','units':units})
write(D/'segmentation_proof.json',report)
print('Mapped',len(units),'units;',[(k,v['source_token_count'],v['alignment_ratio'])for k,v in report['languages'].items()],'ambiguous',len(report['ambiguous_boundaries']))
