from pathlib import Path
import json,re
from lxml import etree
p=Path('/tmp/mahzor-s238/integration-v1/qa');ns={'t':'http://www.tei-c.org/ns/1.0','p':'http://jewishliturgy.org/ns/processing'};role='urn:x-opensiddur:instruction:role/';checks=[]
reports=json.loads((p/'compiler-report.json').read_text());core=[v for v in reports if re.fullmatch(r'(documentary|expanded)-(frankfurt|fuerth|metz|other_include|other_omit|unknown)-(included|omitted|unknown)\.yaml',v['settings'])];extra=[v for v in reports if v not in core];assert len(core)==32,len(core)
(p/'compiler-report.json').write_text(json.dumps(core,indent=2)+'\n');(p/'additional-compile-report.json').write_text(json.dumps(extra,indent=2)+'\n')
for report in core:
 assert not report['pairing_problems'];r=etree.parse(str(p/report['file']));targets=r.xpath('//p:transclude/@target',namespaces=ns);targets={v.partition('@')[0]for v in targets};name=report['settings'];kind=name.split('-')[0]
 if kind=='expanded':
  for uri in ['urn:x-opensiddur:text:prayer:amidah/qedushah/ani','urn:x-opensiddur:text:bible:deuteronomy/6/4']:
   nodes=r.xpath('//p:transclude[@target=$u]',namespaces=ns,u=uri);assert len(nodes)==1,(name,uri,len(nodes));word=nodes[0];assert not word.xpath('.//t:note[@type="description"]',namespaces=ns);previous=word.getprevious();assert previous is not None
   actors=previous.xpath('.//t:note[@corresp=$u]',namespaces=ns,u=role+'reader_and_congregation');assert len(actors)==1,(name,uri,len(actors))
  k=r.xpath('//p:transclude[@target="urn:x-opensiddur:text:prayer:amidah/naaritzekha_venaqdishkha_kesod"]',namespaces=ns);assert len(k)==1;assert len(k[0].xpath('.//t:note[@corresp=$u]',namespaces=ns,u=role+'reader'))==2
  veye='urn:x-opensiddur:text:poem:v_yeetayu_kol_leavdekha'in targets;editorial=r.xpath('//t:note[@corresp=$u][@resp="urn:x-opensiddur:contributor:opensiddur.org/codex"]',namespaces=ns,u=role+'reader')
  if veye:
   target=r.xpath('//p:transclude[@target="urn:x-opensiddur:text:poem:v_yeetayu_kol_leavdekha"]',namespaces=ns)[0];assert len(target.getprevious().xpath('.//t:note[@corresp=$u]',namespaces=ns,u=role+'reader'))==1
 if kind=='documentary':
  documentary_cues=[]
  for namepart,expected in [('kevodo_first','congregation'),('mimeqomo_first','congregation'),('shema','reader_and_congregation'),('ani','reader_and_congregation')]:
   wrappers=r.xpath('//p:transclude[contains(@target,$piece)]',namespaces=ns,piece='urn:x-opensiddur:text:siddur:rosh_hashanah/musaf/repetition/qedushah/'+namepart+'@')
   assert len(wrappers)==1,(name,namepart,len(wrappers))
   node=wrappers[0];assert not node.xpath('.//t:note[starts-with(@corresp,$role)]',namespaces=ns,role=role)
   previous=node.getprevious();actors=previous.xpath('.//t:note[starts-with(@corresp,$role)]',namespaces=ns,role=role);assert len(actors)==1 and actors[0].get('corresp')==role+expected,(name,namepart,[v.get('corresp')for v in actors]);documentary_cues.append(dict(part=namepart,role=expected,count=1))
  assert not r.xpath('//p:parallelItem[@xml:lang="en"]//t:note[starts-with(@corresp,$role)]',namespaces=ns,role=role)
 checks.append(dict(settings=name,destination=report['destination'],pairing_problems=0,expanded_actor_scopes_correct=True if kind=='expanded'else None,documentary_actor_scopes_correct=documentary_cues if kind=='documentary'else None))
(p/'final-compiled-checks.json').write_text(json.dumps(checks,indent=2)+'\n');print('32 final core compiler states verified; expanded Ani/Shema cues once, Kesod two cues in their two rows, Veye editorial cue once per included or deferred occurrence')
