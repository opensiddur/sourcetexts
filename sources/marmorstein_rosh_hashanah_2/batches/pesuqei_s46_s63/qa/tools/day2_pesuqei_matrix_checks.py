from pathlib import Path
import json,hashlib
from lxml import etree
base=Path('/home/efeins/src/opensiddur-repos/output/marmorstein_rosh_hashanah_2/pesuqei_s46_s63');P='{http://jewishliturgy.org/ns/processing}';T='{http://www.tei-c.org/ns/1.0}';rows=[]
for path in sorted((base/'matrix').glob('*.xml')):
 if path.name=='references.xml':continue
 root=etree.parse(str(path));body=root.find('.//'+T+'body');calls=list(body.iter(P+'transclude'));repeat=[x for x in calls if x.get('target')=='urn:x-opensiddur:text:bible:psalms/91/16'];gap=[x for x in calls if x.get('target')=='urn:x-opensiddur:text:bible:psalms/136/25'];assert len(repeat)==len(gap)==1,(path,len(repeat),len(gap))
 assert not repeat[0].xpath('.//*[@role="parallel"]')
 assert not gap[0].xpath('.//*[@role="parallel"]')
 for number in (24,26):
  markers=body.xpath('.//tei:milestone[@corresp=$urn]',namespaces={'tei':T[1:-1]},urn='urn:x-opensiddur:text:bible:psalms/136/'+str(number));assert len(markers)==2,(path,number,len(markers))
 rows.append({'case':path.stem,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'psalm91_repeat_hebrew_only':True,'psalm136_25_hebrew_only':True,'neighboring_24_26_bilingual':True})
assert len(rows)==27,len(rows)
S=Path('/home/efeins/.codex/worktrees/marmorstein-day-two-sources/master/sources/marmorstein_rosh_hashanah_2/batches/pesuqei_s46_s63/qa');(S/'pesuqei_condition_matrix.json').write_text(json.dumps({'status':'passed_prospective_only','case_count':len(rows),'cases':rows},indent=2)+'\n');print('All27actualcompiledcases preservebothHebrewonlyoccurrences andneighboringbilingualalignment')
