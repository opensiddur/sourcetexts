from pathlib import Path
from collections import Counter
from lxml import etree
import json
p=Path('/tmp/mahzor-s276/compile-qa-v4');ns={'t':'http://www.tei-c.org/ns/1.0','p':'http://jewishliturgy.org/ns/processing'};pages=[];responses=[]
for f in sorted(p.glob('*-print.xml')):
 if f.name.endswith('-full-print.xml'):continue
 root=etree.parse(str(f))
 for lang in ['he','en']:
  pbs=root.xpath('//p:parallelItem[@xml:lang=$lang]//t:pb[@ed="1965"]',namespaces=ns,lang=lang)
  counts=Counter(pb.get('facs')for pb in pbs);assert max(counts.values(),default=0)<=1,(f.name,lang,counts)
  if f.name.startswith('documentary-'):
   assert sum(pb.get('n')=='128'for pb in pbs)==1,(f.name,lang,'primary128')
   assert sum(pb.get('n')=='136'for pb in pbs)==1,(f.name,lang,'primary136')
  pages.append(dict(file=f.name,language=lang,primary_page_markers=len(pbs),all_primary_scan_sources_unique=True))
expected={'shabbat_omit_both':(0,0),'shabbat_hayom_only':(1,0),'shabbat_both_no_cantor_repeat':(1,1),'shabbat_both_cantor_hayom':(2,1),'shabbat_both_cantor_repeat':(2,2),'shabbat_frankfurt':(2,2),'shabbat_hayom_only_repeat':(2,0),'weekday_areshet_no_repeat':(2,1),'weekday_areshet_repeat':(2,2)}
for profile,expected_counts in expected.items():
 for kind in ['documentary','expanded']:
  f=p/(kind+'-'+profile+'-print.xml');root=etree.parse(str(f))
  for lang in ['he','en']:
   counts=tuple(len(root.xpath('//p:parallelItem[@xml:lang=$lang]//'+('t:milestone[@corresp=$identity]' if kind=='expanded' else 'p:transclude[substring-before(@target,"@")=$identity]'),namespaces=ns,lang=lang,identity='urn:x-opensiddur:text:prayer:'+part))for part in ['hayom_harat_olam','areshet_sefatenu/opening'])
   expected_here=expected_counts if kind=='expanded'else tuple(int(x>0)for x in expected_counts)
   assert counts==expected_here,(f.name,lang,expected_here,counts)
   responses.append(dict(file=f.name,language=lang,hayom_occurrences=counts[0],areshet_occurrences=counts[1],matches_selected_custom=True))
# A known circumcision preserves the action after its condition-rubric is suppressed.
f=p/'documentary-weekday_brit_true-print.xml';root=etree.parse(str(f));assert root.xpath('//t:note[@type="instruction" and contains(.,"פותחים ארון הקודש")]',namespaces=ns)
(p/'response-page-marker-assertions.json').write_text(json.dumps(dict(status='passed',primary_page_marker_checks=pages,response_count_checks=responses,known_brit_retains_ark_instruction=True),ensure_ascii=False,indent=2)+'\n');print(len(pages),'per-language primary page-marker checks;',len(responses),'exact response occurrence checks; known circumcision keeps Ark action.')
