"""Read-only checks for the independent closure reviewer; prints evidence only."""
from pathlib import Path
import hashlib,json,unicodedata
from lxml import etree
s=Path('/home/efeins/.codex/worktrees/marmorstein-day-two-sources/master/sources/marmorstein_rosh_hashanah_2');b=s/'batches/maariv_s5_s24';p=Path('/home/efeins/.codex/worktrees/marmorstein-day-two-projects/master/project');ns={'t':'http://www.tei-c.org/ns/1.0'};summary={}
profile=json.loads((b/'evening_sequence.json').read_text());bindings=0
for name in profile['prayer_recipes']:
 r=json.loads((s/name).read_text())
 for rel,digest in r['input_sha256'].items():assert hashlib.sha256((s/rel).read_bytes()).hexdigest()==digest,(name,rel);bindings+=1
summary['current_prayer_input_hashes_verified']=bindings
old=json.loads((s/'independent/veahavta_range_encoding_rebinding/previous_recipe.json').read_text());new=json.loads((b/'scripture_ranges.json').read_text());assert old['units']==new['units'];assert set(k for k in old if old[k]!=new[k])=={'input_sha256'};summary['veahavta_only_source_hash_bindings_changed']=True
proof=json.loads((s/'independent/veahavta_range_encoding_rebinding/equivalence.json').read_text())
metadata=json.loads((s/'independent/evening_metadata_equivalence/proof.json').read_text())
def without_edition(raw):
 root=etree.fromstring(raw)
 for n in root.xpath('//*[local-name()="editionStmt"]/*[local-name()="edition"]'):n.text='EDITION STATUS'
 return etree.tostring(root)
for path,digest in proof['module_hashes'].items():
 path=Path(path);relative=str(path.relative_to(p));record=metadata['files'][relative];current=hashlib.sha256(path.read_bytes()).hexdigest();assert digest==record['before_sha256'];assert current==record['after_sha256'];oldxml=Path(metadata['previous_xml_cache'])/relative;assert without_edition(oldxml.read_bytes())==without_edition(path.read_bytes())
summary['veahavta_approved_words_structure_other_metadata_unchanged']=True
allunits=[u for name in profile['prayer_recipes'] for u in json.loads((s/name).read_text())['units']];assert len({u['file'] for u in allunits})==len(allunits);summary['unique_module_owners']=len(allunits)
for project in ['prayerbook_for_the_new_year_second_day-heidenheim-1965-he','prayerbook_for_the_new_year_second_day-marmorstein-1965-en']:
 maps={}
 for path in (p/project).glob('*.xml'):
  tree=etree.parse(str(path))
  for urn in tree.xpath('//t:body//@corresp',namespaces=ns):
   if ':text:bible:' in urn:maps.setdefault(urn,[]).append(path.name)
 duplicates={k:v for k,v in maps.items() if len(v)>1};assert not duplicates,duplicates;summary[project+'_duplicate_bible_keys']=duplicates
 for path in (p/project).glob('*.xml'):
  tree=etree.parse(str(path))
  for node in tree.xpath('//*[local-name()="divineName"]'):
   value=''.join(node.itertext());letters=''.join(c for c in value if '\u05d0'<=c<='\u05ea');assert letters in ['יי','יהוה'],(path.name,value)
   if letters=='יהוה':assert '\u05b9'in value,(path.name,value)
summary['all_literal_tetragrammatons_follow_recorded_holam_convention']=True
source=p/'prayerbook_for_the_new_year-heidenheim-1965-he/morning_full_kaddish.xml';assert hashlib.sha256(source.read_bytes()).hexdigest()==profile['titqabbal_source_sha256'];donor=etree.parse(str(source));derived=etree.parse(str(p/'machzor_expanded-opensiddur-he/kaddish_titqabbal.xml'));urn='urn:x-opensiddur:text:prayer:kaddish/titqabbal/text';a=donor.xpath('//t:seg[@source=$u]',namespaces=ns,u=urn)[0];c=derived.xpath('//t:seg[@source=$u]',namespaces=ns,u=urn)[0];assert unicodedata.normalize('NFKD',''.join(a.itertext()))==''.join(c.itertext());summary['titqabbal_exact_first_day_source_words']=True
print(json.dumps(summary,ensure_ascii=False,indent=2))
import sys
sys.path.insert(0,'/home/efeins/.codex/worktrees/marmorstein-day-two-processor/master')
from opensiddur.exporter.refdb import milestone_terminates
rooturn='urn:x-opensiddur:text:siddur:chol/shacharit/conclusion/aleinu'
current=etree.parse(str(p/'prayerbook_for_the_new_year_second_day-heidenheim-1965-he/aleinu.xml'))
assert current.xpath('count(//t:body//t:div[@corresp=$u])',namespaces=ns,u=rooturn)==1
assert not current.xpath('//t:milestone[starts-with(@corresp,$u)]',namespaces=ns,u=rooturn+'/')
previous=etree.parse(str(s/'independent/concluding_modules_encoding/before_whole_aleinu.xml'))
words=lambda tree:[''.join(n.itertext()) for n in tree.xpath('//t:body//t:p',namespaces=ns)]
assert words(current)==words(previous)
print(json.dumps({'whole_aleinu_root_once':True,'no_incompatible_child_mapping_claimed':True,'both_aleinu_paragraphs_exactly_unchanged':True},indent=2))
