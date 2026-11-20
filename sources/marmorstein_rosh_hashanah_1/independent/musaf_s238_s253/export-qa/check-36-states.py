from pathlib import Path
import json,yaml,copy
from lxml import etree
from opensiddur.exporter.refdb import ReferenceDatabase
from opensiddur.exporter.external_compiler import ExternalCompilerProcessor
from opensiddur.exporter.linear import LinearData
from opensiddur.exporter.settings import load_settings
from opensiddur.exporter.compiler import check_pairing
q=Path('/tmp/mahzor-s238/integration-v1/qa');projects=q.parent/'project-final';db=ReferenceDatabase(q/'reference.db');ns={'p':'http://jewishliturgy.org/ns/processing','t':'http://www.tei-c.org/ns/1.0','j':'http://jewishliturgy.org/ns/jlptei/2'};P='urn:x-opensiddur:text:prayer:amidah/';V='urn:x-opensiddur:text:poem:v_yeetayu_kol_leavdekha';C='urn:x-opensiddur:condition:';rows=[];breaks=[]
for kind in ['documentary','expanded']:
 for rite in ['unknown','frankfurt','metz','fuerth_alone','other_include','other_omit']:
  for optional in ['unknown','included','omitted']:
   cfg=yaml.safe_load((q/(kind+'-unknown-unknown.yaml')).read_text());rf={}if rite=='unknown'else({'fuerth':True}if rite=='fuerth_alone'else dict(frankfurt_am_main=rite=='frankfurt',metz=rite=='metz',fuerth=False));vf={}
   if rite in ['other_include','other_omit']:vf.update({C+'prayer:amidah/tisgav_levaddekha/recite':rite=='other_include',C+'poem:v_yeetayu_kol_leavdekha/recite':rite=='other_include'})
   if optional!='unknown':vf.update({C+'poem:haochez_beyad_middat_mishpat/hehagui/vehoveh':optional=='included',C+'poem:v_yeetayu_kol_leavdekha/veyizbechu':optional=='included'})
   cfg['declarations']={'opensiddur:rite':rf,'opensiddur:variant':vf};path=q/'matrix-setting.yaml';path.write_text(yaml.safe_dump(cfg,allow_unicode=True));data=load_settings(path,linear_data=LinearData(),project_directory=projects);data.xml_cache.base_path=projects;root=ExternalCompilerProcessor(cfg['book']['project'],'batch_review.xml',linear_data=data,reference_database=db).process()[0];assert not list(check_pairing(root));targets=[v.partition('@')[0]for v in root.xpath('//p:transclude/@target',namespaces=ns)]
   if kind=='expanded':first=P+'addir_adiraynu'in targets;repeat=P+'addir_adiraynu/addir'in targets
   else:first=any(v.endswith('/qedushah/addir_first')for v in targets);repeat=any(v.endswith('/qedushah/addir_repeat')for v in targets)
   tis=P+'tisgav_levaddekha'in targets;veye=V in targets;assert first==(rite!='frankfurt');assert repeat;assert tis==(rite not in ['frankfurt','metz','other_omit']);assert veye==(rite not in ['frankfurt','metz','other_omit'])
   text=''.join(root.itertext());direction='In Fuerth and other communities'in text;assert rite!='fuerth_alone'or direction
   rows.append(dict(veyeetayu_instruction_in_compiled_text=direction,view=kind,rite=rite,optional=optional,first_adir=first,repeated_adir=repeat,tisgav=tis,veyeetayu=veye,pairing_problems=[]))
   if rite=='other_include':
    pbs=root.xpath('//t:pb[contains(@facs,"/n251.") or contains(@facs,"/n252.")]',namespaces=ns);assert len(pbs)==2,(kind,optional,len(pbs))
    for pb in pbs:
     scan=252 if '/n251.'in pb.get('facs')else 253
     # Physical boundary must survive optional-clause removal and stay outside that scope.
     optional_anc=pb.xpath('ancestor::j:conditional[.//t:f[@name=$u]]',namespaces=ns,u=C+'poem:v_yeetayu_kol_leavdekha/veyizbechu');assert not optional_anc
     before=[];after=[];seen=False
     for event,node in etree.iterwalk(root,events=('start','end')):
      if event=='start':
       if node is pb:seen=True
       if node.text:(after if seen else before).append(node.text)
      elif node.tail:(after if seen else before).append(node.tail)
     before=' '.join(before);after=' '.join(after)
     if scan==252:
      assert 'וְיִזְנְחוּ'in after
      assert ('זִבְחֵיהֶם'in before)==(optional!='omitted'),(kind,optional,'offering')
     breaks.append(dict(view=kind,optional=optional,scan_page=scan,n=pb.get('n'),facs=pb.get('facs'),outside_optional_clause=True,preceding_excerpt=before[-180:],following_excerpt=after[:180],nearest_paragraph=etree.tostring(pb.getparent(),encoding='unicode')[:500]))
(q/'matrix-36-states.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n');(q/'page-boundaries-condition-states.json').write_text(json.dumps(breaks,ensure_ascii=False,indent=2)+'\n');print('36print condition states and12physical page-boundary checks pass')
