from pathlib import Path
import json,copy,yaml
from lxml import etree
from opensiddur.exporter.refdb import ReferenceDatabase
from opensiddur.exporter.external_compiler import ExternalCompilerProcessor
from opensiddur.exporter.linear import LinearData
from opensiddur.exporter.settings import load_settings
from opensiddur.exporter.constants import PROCESSING_NAMESPACE
from opensiddur.exporter.compiler import drop_empty_scopes,close_up_whitespace,join_split_paragraphs,merge_credits,check_pairing
p=Path('/tmp/mahzor-s238/iteration3');qa=p/'qa-projects';db=ReferenceDatabase(p/'reference.db')
for project in qa.iterdir():
 if project.is_dir():db.sync_project(project.name,qa)
reports=[]
for state in ['unknown','included','omitted']:
 for dest in ['print','electronic']:
  data=LinearData(defer_reader_settings=dest=='electronic');data=load_settings(p/(state+'.yaml'),linear_data=data,project_directory=qa);data.xml_cache.base_path=qa
  project='prayerbook_for_the_new_year-heidenheim-1965-he';result=ExternalCompilerProcessor(project,'index.xml',linear_data=data,reference_database=db).process()[0]
  drop_empty_scopes(result);close_up_whitespace(result);join_split_paragraphs(result);merge_credits(result,data)
  if dest=='electronic':result.set(f'{{{PROCESSING_NAMESPACE}}}destination','electronic')
  problems=list(check_pairing(result));out=p/f'compiled-{state}-{dest}.xml';out.write_bytes(etree.tostring(result,encoding='utf-8',pretty_print=True));reports.append(dict(state=state,destination=dest,file=str(out),pairing_problems=problems));print(state,dest,'compiled; pairing problems',len(problems),flush=True)
(p/'compiler-qa.json').write_text(json.dumps(dict(scope='Isolated seven-module test, not full-service acceptance',results=reports),indent=2)+'\n')
