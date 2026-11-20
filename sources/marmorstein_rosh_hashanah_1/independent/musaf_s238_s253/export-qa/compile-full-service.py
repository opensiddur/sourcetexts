from pathlib import Path
import json,yaml,copy,shutil
from lxml import etree
from opensiddur.exporter.refdb import ReferenceDatabase
from opensiddur.exporter.external_compiler import ExternalCompilerProcessor
from opensiddur.exporter.linear import LinearData
from opensiddur.exporter.settings import load_settings
from opensiddur.exporter.compiler import drop_empty_scopes,close_up_whitespace,join_split_paragraphs,merge_credits,check_pairing
p=Path('/tmp/mahzor-s238/integration-v1');qa=p/'qa';projects=p/'project-final';db=ReferenceDatabase(qa/'full-reference.db');moved=[]
try:
 for project in projects.iterdir():
  f=project/'batch_review.xml'
  if f.exists():dest=qa/(project.name+'-batch.xml');shutil.move(f,dest);moved.append((dest,f))
 for project in projects.iterdir():
  if project.is_dir():db.sync_project(project.name,projects)
 reports=[]
 for kind in ['documentary','expanded']:
  cfg=yaml.safe_load((qa/(kind+'-unknown-unknown.yaml')).read_text());cfg['book']['file_name']='index.xml';settings=qa/(kind+'-full.yaml');settings.write_text(yaml.safe_dump(cfg,allow_unicode=True,sort_keys=False));data=load_settings(settings,linear_data=LinearData(),project_directory=projects);data.xml_cache.base_path=projects
  root=ExternalCompilerProcessor(cfg['book']['project'],'index.xml',linear_data=data,reference_database=db).process()[0]
  drop_empty_scopes(root);close_up_whitespace(root);join_split_paragraphs(root);merge_credits(root,data);problems=list(check_pairing(root));assert not problems,problems
  words=''.join(root.itertext());assert 'All will come to serve Thee'in words;assert 'Holy art Thou and awe-inspiring'in words
  f=qa/(kind+'-full-print.xml');f.write_bytes(etree.tostring(root,encoding='utf-8',pretty_print=True));reports.append(dict(kind=kind,pairing_problems=problems,full_book_reaches_end_of_new_musaf_batch=True,bytes=f.stat().st_size));print(kind,'whole book compiled',flush=True)
 # Morning selection must continue through Torah service and Musaf on both days.
 for shabbat in [False,True]:
  for frankfurt in [False,True]:
   cfg=yaml.safe_load((qa/'expanded-full.yaml').read_text());d=cfg['declarations'];d['opensiddur:service-time']={k:k=='shaharit'for k in ['shaharit','minha','maariv','musaf','neila','slihot']};d['opensiddur:holiday']={'rosh-hashana':1};d['opensiddur:holiday-aggregate']={'shabbat':shabbat};d['opensiddur:quorum']={'minyan':True};d['opensiddur:rite']={'frankfurt_am_main':frankfurt,'metz':False,'fuerth':False};d.setdefault('opensiddur:variant',{}).update({'urn:x-opensiddur:condition:prayer:berikh_shemeh/torah_opening':True,'urn:x-opensiddur:condition:prayer:amidah/tisgav_levaddekha/recite':True,'urn:x-opensiddur:condition:poem:v_yeetayu_kol_leavdekha/recite':True})
   settings=qa/('morning-shabbat'+str(shabbat)+'-frankfurt'+str(frankfurt)+'.yaml');settings.write_text(yaml.safe_dump(cfg,allow_unicode=True));data=load_settings(settings,linear_data=LinearData(),project_directory=projects);data.xml_cache.base_path=projects
   root=ExternalCompilerProcessor(cfg['book']['project'],'index.xml',linear_data=data,reference_database=db).process()[0];problems=list(check_pairing(root));assert not problems,problems;text=''.join(root.itertext());assert 'Holy art Thou and awe-inspiring'in text;assert 'All believe'in text;assert ('All will come to serve Thee'in text)==(not frankfurt);ns={'p':'http://jewishliturgy.org/ns/processing'};attah=bool(root.xpath('//p:transclude[starts-with(@target,"urn:x-opensiddur:text:poem:attah_hu_eloheinu")]',namespaces=ns));berikh=bool(root.xpath('//p:transclude[starts-with(@target,"urn:x-opensiddur:text:prayer:berikh_shemeh")]',namespaces=ns));assert attah==(not frankfurt),(shabbat,frankfurt,'AttahHu',attah);assert berikh==(not frankfurt),(shabbat,frankfurt,'Berikh',berikh);(qa/('morning-shabbat'+str(shabbat)+'-frankfurt'+str(frankfurt)+'.xml')).write_bytes(etree.tostring(root,encoding='utf-8',pretty_print=True));reports.append(dict(morning_selected=True,shabbat=shabbat,frankfurt_am_main=frankfurt,compiled_to_end_of_new_Musaf=True,regional_omission_correct=True,shacharit_attah_hu_and_berikh_unchanged=True,pairing_problems=problems));print('Morning',shabbat,frankfurt,'passes through Musaf',flush=True)
 (qa/'full-service-report.json').write_text(json.dumps(reports,indent=2)+'\n')
finally:
 for a,b in moved:shutil.move(a,b)
