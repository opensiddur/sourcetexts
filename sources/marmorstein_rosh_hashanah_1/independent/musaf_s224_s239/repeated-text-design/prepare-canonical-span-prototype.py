from pathlib import Path
import json
p=Path('/tmp/mahzor-s224');r=json.loads((p/'ready.json').read_text());u={v['stem']:v for v in r['units']};out=[]
def text(s):return ' '.join(f['text']for f in s['fragments'])
def entry(urn,old_stem,old_index,new_stem,new_parts):
 item=dict(urn=urn,canonical_owner=dict(stem=old_stem,segment=old_index),occurrence=new_stem,languages={})
 for lang,parts in new_parts.items():
  old=u[old_stem]['languages'][lang][old_index];item['languages'][lang]=dict(old=text(old),new=parts,identical=text(old)==parts,old_scan=old['fragments'][0]['scan'],new_scan=u[new_stem]['languages'][lang][0]['fragments'][0]['scan'])
 out.append(item)
G='urn:x-opensiddur:text:prayer:amidah/gevurot/'
for stem,offset,boundary in [('musaf_repetition_gevurot_open',0,'מְכַלְכֵּל'),('musaf_repetition_gevurot_close',2,'וְנֶאֱמָן')]:
 he=text(u[stem]['languages']['he'][0]);before,sep,after=he.partition(boundary);assert sep
 he_parts=[before.rstrip(),sep+after]
 if offset==0:en_parts=[text(s)for s in u[stem]['languages']['en']]
 else:
  en=text(u[stem]['languages']['en'][0]);before,sep,after=en.partition('; and ');assert sep;en_parts=[before+';','and '+after]
 assert ' '.join(he_parts)==he
 assert ' '.join(en_parts)==' '.join(text(s)for s in u[stem]['languages']['en'])
 for i in range(2):
  old=u['rh_gevurot']['languages']['he'][offset+i];entry(old['corresp'],'rh_gevurot',offset+i,stem,dict(he=he_parts[i],en=en_parts[i]))
for urn,old,new,index in [('urn:x-opensiddur:text:bible:psalms/146/10','rh_vetimlokh','musaf_repetition_yimlokh',1),('urn:x-opensiddur:text:bible:psalms/22/4','repetition_veattah_qadosh','musaf_repetition_veattah_qadosh',0),('urn:x-opensiddur:text:prayer:uvekhen_lekha_taaleh_qedushah/text','uvekhen_lekha_taaleh_qedushah','musaf_uvekhen_lekha_taaleh_qedushah',0)]:
 entry(urn,old,index,new,{lang:text(ss[0])for lang,ss in u[new]['languages'].items()})
(p/'canonical-span-prototype.json').write_text(json.dumps(dict(status='Design evidence only, not accepted or installed',parts=out),ensure_ascii=False,indent=2)+'\n')
print('Seven canonical parts,14 language realizations; each proposed split exactly reconstructs the original source paragraph.')
for item in out: print(item['urn'].rsplit(':',1)[-1],{lang:v['identical']for lang,v in item['languages'].items()})
