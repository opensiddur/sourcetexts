from pathlib import Path
import json,re,copy
p=Path('/tmp/mahzor-s238/iteration3');rows=json.loads((p.parent/'candidate-round6.json').read_text())['blocks'];new=[]
PO='urn:x-opensiddur:text:poem:';P='urn:x-opensiddur:text:prayer:'
roles={'ק׳':'קהל','ח׳':'חזן','קו״ח':'קהל וחזן'}
def get(n,k):return next(b['text']for b in rows if b['scan']==f's{n}'and b['key']==k)
def frag(n,k,text=None):return dict(scan=f's{n}',printed_page=str((n-20)//2),text=get(n,k)if text is None else text,page_start=False)
def segment(n,k,par,identity=None,text=None):
 f=frag(n,k,text);s=dict(paragraph=par,fragments=[f])
 for a,e in roles.items():
  if f['text'].startswith(a+' '):
   f['text']=f['text'][len(a)+1:];s['speaker']=dict(abbr=a,expan=e);s['speaker_before_reference']=True;break
 if identity:s.update(corresp=identity,reference_unit='stanza')
 return s
def unit(stem,urn,he,en):
 z=dict(stem='musaf_'+stem,urn=urn,title={'he':he,'en':en},languages={});new.append(z);return z
def add(z,lang,entries):
 z['languages'][lang]=[]
 for n,k,par,part in entries:z['languages'][lang].append(segment(n,k,par,z['urn']+'/'+part if part else None))
 z['languages'][lang][-1]['end_reference']=True
z=unit('vechayyot_asher_hennah',PO+'vechayyot_asher_hennah','וחיות אשר הנה','The living creatures by the throne')
add(z,'he',[(238,'vechayot_asher',1,'vechayyot'),(238,'chashot_beratzo',2,'chashot'),(240,'kaf_regel',3,'kaf_regel'),(240,'levilti_lenabel',4,'levilti'),(240,'rahem_metsukim',5,'rachem_metzuqim')]);add(z,'en',[(241,'rachem',1,'rachem_metzuqim')]);z['instructions']=[dict(text=get(238,'rubric_alef_bet_elazar'),language='he',type='description',witnesses=['he'])]
z['languages']['he'][0]['speaker']=dict(abbr='ק׳',expan='קהל');z['languages']['he'][0]['speaker_before_reference']=True
z['languages']['he'][1]['speaker']=dict(abbr='ח׳',expan='חזן');z['languages']['he'][1]['speaker_before_reference']=True
z['partial_translation_note']='The English source prints only the concluding Rachem Metzuqim stanza; the preceding Hebrew stanzas have no English counterpart.'
z=unit('veammekha_teluyim',PO+'veammekha_teluyim','ועמך תלואים','Thy people trust in repentance')
add(z,'he',[(240,'veamkha_teluim',1,'veammekha'),(242,'kol_shofar_kafuf',2,None),(242,'semukhim_betzidkat',3,None),(242,'lehizakher_lamo',4,'lehizakher'),(242,'im_yashkit',5,None),(242,'od_yizakher',6,'od_yizzakher')]);add(z,'en',[(241,'amekha',1,'veammekha'),(243,'amekha',1,None),(243,'lehaver',2,'lehizakher'),(243,'od_yizkor',3,'od_yizzakher')]);z['instructions']=[dict(text=get(240,'rubric_tashraq'),language='he',type='description',witnesses=['he'])]
z['languages']['he'][-1]['speaker']=dict(label='קהל וחזן',role='reader_and_congregation',language='he');z['languages']['he'][-1]['speaker_before_reference']=True
z=unit('veattah_ezon_qol',PO+'veattah_ezon_qol','ואתה אזון קול','Listen to the voice of those who glorify Thee')
add(z,'he',[(244,'veatah_azon_kol',1,'veattah'),(244,'sam_halikhot',2,None),(244,'yisu_ayin',3,'yissau')]);add(z,'en',[(245,'veattah',1,'veattah'),(245,'yissau',2,'yissau')]);z['instructions']=[dict(text=get(244,'acrostic_rubric'),language='he',type='description',witnesses=['he'])]
for s,a in zip(z['languages']['he'],['ק׳','ח׳','קו״ח']):s.update(speaker=dict(abbr=a,expan=roles[a]),speaker_before_reference=True)
z=unit('tehillot_kevodkha',PO+'tehillot_kevodkha','תהלות כבודך','The fame of Thine honour')
add(z,'he',[(246,'tehillot_kevodecha',1,'tehillot'),(246,'lehitvada_ulehigalot',2,'lehitvadda')]);add(z,'en',[(247,'tehillot',1,'tehillot'),(247,'lehodiya',2,'lehitvadda')])
z=unit('ki_maqdishekha',P+'amidah/ki_maqdishekha','כי מקדישיך','For those who sanctify Thee')
add(z,'he',[(246,'ki_makdishecha',1,'ki_maqdishekha'),(248,'elohenu_al_yisrael_cont',1,None),(248,'od_yizkor_lanu',2,'od_yizkor')]);add(z,'en',[(247,'ki_maqdish',1,'ki_maqdishekha')])
# The facing translation prints its continuation and the next Hebrew paragraph as one paragraph.
t=get(249,'ki_maqdish');before,after=t.split('Our Lord will yet remember',1);z['languages']['en'][0]['fragments'].append(frag(249,'ki_maqdish',before));z['languages']['en'][0].pop('end_reference',None);z['languages']['en'].append(segment(249,'ki_maqdish',1,z['urn']+'/od_yizkor','Our Lord will yet remember'+after));z['languages']['en'][-1]['end_reference']=True
z=unit('haochez_beyad_middat_mishpat',PO+'haochez_beyad_middat_mishpat','האוחז ביד מדת משפט','In His hand He holds the attribute of judgment')
hkeys=['haochez_beyad','haboḥen','hagoel','hadan','hehagui','havadai','hazocher','hachotech','hatov','hayodea','hakol_yochal','halan','hamamlich','hanoheg','hasovel','haelyon','hapoteach_petach','hatsofeh_larasha','hakatsar_bezaam','harachum_umakdim','hashaveh_umashveh','hatam_umitamem']
add(z,'he',[(248 if i<=16 else 250,k,i,str(i))for i,k in enumerate(hkeys,1)]);add(z,'en',[(249 if i<=16 else 251,'haochez_'+str(i),i,str(i))for i in range(1,23)])
# Source abbreviations are documentary; expanded settings already choose abbr/expan expansion.
for s in z['languages']['he'][1:]:
 f=s['fragments'][0];m=re.search(r'ו[\u0591-\u05c7]*[״]מ[\u0591-\u05c7]*|ו[\u0591-\u05c7]*מ[\u0591-\u05c7]*[״]',f['text']);assert m,f['text'];f['abbreviations']=[dict(abbr=m.group(),expan='וְכֹל מַאֲמִינִים')]
z['instructions']=[dict(text='ע״ס א״ב כפול.',language='he',type='description',witnesses=['he'])]
z=unit('veyeetayu',P+'veyeetayu','ויאתיו','All will come to serve Thee')
add(z,'he',[(250,'veyeetayu_kol',1,'veyeetayu'),(252,'lekha_et_zivheihem_continuation',1,None)]);add(z,'en',[(251,'veyetayu',1,'veyeetayu'),(253,'veyetayu',1,None)])
(p/'draft-poem-units.json').write_text(json.dumps(dict(status='DRAFT only. Not installed or approved. Literal audit, precise alignment/role scopes, variants, regional conditions, source page starts and parenthetical interpretations still require closure.',units=new),ensure_ascii=False,indent=2)+'\n');print(len(new),'draft works assembled')
