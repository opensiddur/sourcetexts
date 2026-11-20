from pathlib import Path
import json,copy,unicodedata
def N(s):return unicodedata.normalize("NFKD",s)
p=Path('/tmp/mahzor-s238/iteration3');d=json.loads((p/'draft-poem-units.json').read_text());by={u['stem']:u for u in d['units']}
def split(u,lang,index,at,part,role=None):
 at=N(at);s=u['languages'][lang][index];assert len(s['fragments'])==1
 f=s['fragments'][0];before,after=f['text'].split(at,1);f['text']=before
 tail=copy.deepcopy(s);tail['fragments'][0]['text']=at+after;tail['corresp']=u['urn']+'/'+part;tail['reference_unit']='stanza'
 tail.pop('speaker',None);tail.pop('speaker_before_reference',None)
 if 'end_reference'in s:s.pop('end_reference')
 if role:tail.update(speaker=dict(abbr=role,expan={'ח׳':'חזן','קו״ח':'קהל וחזן'}[role]),speaker_before_reference=True)
 u['languages'][lang].insert(index+1,tail);return tail
u=by['musaf_veammekha_teluyim']
# Preserve the facing English paragraph while aligning its interior to the source stanzas.
split(u,'en',0,'let the voice of the bent Shofar','kol_shofar')
u['languages']['he'][1].update(corresp=u['urn']+'/kol_shofar',reference_unit='stanza')
split(u,'en',2,'relying on the piety','semukhim')
u['languages']['he'][2].update(corresp=u['urn']+'/semukhim',reference_unit='stanza')
idx=next(i for i,s in enumerate(u['languages']['en'])if s.get('corresp')==u['urn']+'/lehizakher')
split(u,'en',idx,'If He is patient','im_yashqit')
u['languages']['he'][4].update(corresp=u['urn']+'/im_yashqit',reference_unit='stanza')
u=by['musaf_tehillot_kevodkha'];s=split(u,'he',0,'ח׳ סֹלּוּ','sollu_pannu','ח׳');s['fragments'][0]['text']=s['fragments'][0]['text'][3:]
split(u,'en',0,'‘Make straight','sollu_pannu')
# Each variant explicitly retains its literal printed words; the abbreviation belongs in an apparatus note.
for u in d['units']:
 for lang,ss in u['languages'].items():
  if lang!='he':continue
  for s in ss:
   for f in s['fragments']:
    for printed,main,alt in [
      ('מֵרְעִישׁוֹת (נ״א מַרְעִישׁוֹת)','מֵרְעִישׁוֹת','מַרְעִישׁוֹת'),
      ('גָּעֲשׁוּ (נ״א גֵּעַשׁ)','גָּעֲשׁוּ','גֵּעַשׁ'),
      ('סֹלּוּ פַּנּוּ (נ״א סוּרוּ מִנִּי)','סֹלּוּ פַּנּוּ','סוּרוּ מִנִּי'),
      ('בִּקְדֻשָּׁתְךָ (נ״א כערכך)','בִּקְדֻשָּׁתְךָ','כערכך'),
      ('אָיוֹם (כ״א היום)','אָיוֹם','היום')]:
     if N(printed) in f['text']:f.setdefault('alternatives',[]).append(dict(printed=N(printed),readings=[N(main),N(alt)]))
# The Rahem variant is a printed additional block that must not be omitted from documentary evidence.
u=by['musaf_vechayyot_asher_hennah'];f=u['languages']['he'][-1]['fragments'][0]
main=N('וְחַיָּה לְחַיָּה וּכְרוּב לִכְרוּב');printed=main+N(' (נ״א וּכְרוּב לִכְרוּב וְחַיָּה לְחַיָּה)');assert main in f['text'];f['text']=f['text'].replace(main,printed);f['alternatives']=[dict(printed=printed,readings=[main,'וּכְרוּב לִכְרוּב וְחַיָּה לְחַיָּה'])]
# Explicitly terminate stanza scopes before independently printed speaker labels.
for u in d['units']:
 for ss in u['languages'].values():
  for i,s in enumerate(ss):
   if i and s.get('speaker'):ss[i-1]['end_reference']=True
(p/'draft-poem-units-refined.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');print('Draft alignment and source variant markup refined; unapproved')
