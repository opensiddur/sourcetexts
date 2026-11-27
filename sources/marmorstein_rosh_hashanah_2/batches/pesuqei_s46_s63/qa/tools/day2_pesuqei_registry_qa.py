from pathlib import Path
import json,hashlib
from lxml import etree
from opensiddur.exporter.refdb import ReferenceDatabase
from opensiddur.exporter.urn import UrnResolver
from opensiddur.importer.marmorstein_rosh_hashanah_2.pesuqei import build_documents
from opensiddur.importer.scan.authoring import normalized_xml
P=Path('/home/efeins/.codex/worktrees/marmorstein-day-two-processor/master');S=Path('/home/efeins/.codex/worktrees/marmorstein-day-two-sources/master/sources/marmorstein_rosh_hashanah_2');B=S/'batches/pesuqei_s46_s63';base=Path('/home/efeins/src/opensiddur-repos/output/marmorstein_rosh_hashanah_2/pesuqei_s46_s63/exports');project=Path('/tmp/day2-pesuqei-prospective/project');report={'scope':'prospective XML and actual isolated reference mappings, not source acceptance','findings':[]}
recipe=json.loads((B/'pesuqei_units.json').read_text());units={u['stem']:u for u in json.loads((B/'working/readings.json').read_text())['units']};docs=build_documents(recipe,units);review=json.loads(Path('/tmp/day2-pesuqei-recipe-final-review.json').read_text());expected=review['final_code_amendment']['generated_document_sha256']if 'final_code_amendment'in review else None
print('review keys',review.keys())
report['protected_files']=len(recipe['protected_files']);assert all(hashlib.sha256((project/path).read_bytes()).hexdigest()==sha for path,sha in recipe['protected_files'].items())
report['generated_files']={p:hashlib.sha256(normalized_xml(root).encode()).hexdigest()for p,root in docs};assert all(hashlib.sha256((project/p).read_bytes()).hexdigest()==sha for p,sha in report['generated_files'].items())
with ReferenceDatabase(base/'references.sqlite')as db:
 db.sync_project('hasiddur_hashalem-birnbaum-1949-he',project)
 resolver=UrnResolver(db);en='prayerbook_for_the_new_year_second_day-marmorstein-1965-en';he='prayerbook_for_the_new_year_second_day-heidenheim-1965-he'
 results={}
 for urn,n in [('urn:x-opensiddur:text:bible:psalms/91/16',1),('urn:x-opensiddur:text:bible:psalms/136/25',0)]:
  found=resolver.resolve(urn+'@'+en);assert len(found)==n,(urn,found);results[urn]={'expected_english_providers':n,'found':[x.model_dump()for x in found]}
 for unit in units.values():
  for lang,parts in unit['languages'].items():
   for part in parts:
    if part.get('corresp'):
     found=resolver.resolve(part['corresp']+'@'+(he if lang=='he'else en));assert len(found)==1,(lang,part['corresp'],found)
 report['provider_checks']=results
old=Path('/home/efeins/src/opensiddur-repos/output/marmorstein_rosh_hashanah_2/morning_s25_s45/exports/night_expanded');new=base/'night_expanded';report['night_regression']={}
for mode in ('print','electronic'):
 before=(old/(mode+'.xml')).read_bytes();after=(new/(mode+'.xml')).read_bytes();report['night_regression'][mode]={'before_sha256':hashlib.sha256(before).hexdigest(),'after_sha256':hashlib.sha256(after).hexdigest(),'byte_identical':before==after};assert before==after,mode
report['status']='passed_prospective_only';(B/'qa/registry_and_regression.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print('All canonicalproviders,786protectedfiles,34generatedoutputs,andNightregressions passed')
