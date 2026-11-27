from pathlib import Path
import json
from lxml import etree
from opensiddur.exporter.linear import LinearData
from opensiddur.exporter.refdb import ReferenceDatabase
from opensiddur.exporter.settings import load_settings,read_settings
from opensiddur.exporter.external_compiler import ExternalCompilerProcessor
from opensiddur.exporter.compiler import drop_empty_scopes,close_up_whitespace,join_split_paragraphs,merge_credits
project=Path('/home/efeins/.codex/worktrees/marmorstein-day-two-projects/master/project');base=Path('/home/efeins/src/opensiddur-repos/output/marmorstein_rosh_hashanah_2/morning_s25_s45/exports');base.mkdir(parents=True,exist_ok=True)
profiles={'documentary_hebrew':project.parent/'settings/prayerbook_for_the_new_year_second_day-heidenheim-1965-he/documentary_hebrew.yaml','documentary_parallel':project.parent/'settings/prayerbook_for_the_new_year_second_day-heidenheim-1965-he/documentary_parallel.yaml','expanded':project.parent/'settings/machzor_expanded-opensiddur-he/second_day_morning.yaml','night_expanded':project.parent/'settings/machzor_expanded-opensiddur-he/second_day_evening.yaml'}
manifest={}
with ReferenceDatabase(base/'references.sqlite')as db:
 for name in ['prayerbook_for_the_new_year_second_day-heidenheim-1965-he','prayerbook_for_the_new_year_second_day-marmorstein-1965-en','prayerbook_for_the_new_year-heidenheim-1965-he','machzor_expanded-opensiddur-he']:db.sync_project(name,project)
 for name,settings in profiles.items():
  folder=base/name;folder.mkdir(exist_ok=True);manifest[name]={'settings':str(settings)}
  for destination in ['print','electronic']:
   ld=LinearData(defer_reader_settings=destination=='electronic');load_settings(settings,linear_data=ld,project_directory=project);book=read_settings(settings,project_directory=project,resolve_fonts=False).book
   result=ExternalCompilerProcessor(book.project,book.file_name,linear_data=ld,reference_database=db).process()[0];drop_empty_scopes(result);close_up_whitespace(result);join_split_paragraphs(result);merge_credits(result,ld)
   if destination=='electronic':result.set('{http://jewishliturgy.org/ns/processing}destination','electronic')
   output=folder/(destination+'.xml');output.write_bytes(etree.tostring(result,pretty_print=True,encoding='utf-8'));manifest[name][destination]=str(output);print(output,flush=True)
(base/'compile_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
