from pathlib import Path
from itertools import product
import json,hashlib
from collections import Counter
from lxml import etree
import yaml
from opensiddur.exporter.linear import LinearData
from opensiddur.exporter.refdb import ReferenceDatabase
from opensiddur.exporter.settings import load_settings,read_settings
from opensiddur.exporter.external_compiler import ExternalCompilerProcessor
from opensiddur.exporter.compiler import drop_empty_scopes,close_up_whitespace,join_split_paragraphs,merge_credits
P='{http://jewishliturgy.org/ns/processing}';T='{http://www.tei-c.org/ns/1.0}';J='{http://jewishliturgy.org/ns/jlptei/2}'
project=Path('/home/efeins/.codex/worktrees/marmorstein-day-two-projects/master/project');settings=project.parent/'settings/machzor_expanded-opensiddur-he/second_day_morning.yaml';output=Path('/home/efeins/src/opensiddur-repos/output/marmorstein_rosh_hashanah_2/morning_s25_s45/matrix');output.mkdir(parents=True,exist_ok=True)
base=yaml.safe_load(settings.read_text());plan=json.load(open('/home/efeins/.codex/worktrees/marmorstein-day-two-sources/master/sources/marmorstein_rosh_hashanah_2/batches/morning_s25_s45/morning_order.json'));targets={r['key']:r.get('canonical_target')for r in plan['documentary_order']};torah=['birkhot_hatorah_laasoq','birkhot_hatorah_vehaarev','birkhot_hatorah_asher_bachar','numbers_6_24_to_26','ellu_devarim'];report={'scope':'Actual expanded morning compilation, all27 German/gender/Shabbat combinations','settings_sha256':hashlib.sha256(settings.read_bytes()).hexdigest(),'cases':[],'findings':[]}
with ReferenceDatabase(output/'references.sqlite')as db:
 for name in ['prayerbook_for_the_new_year_second_day-heidenheim-1965-he','prayerbook_for_the_new_year_second_day-marmorstein-1965-en','prayerbook_for_the_new_year-heidenheim-1965-he','machzor_expanded-opensiddur-he']:db.sync_project(name,project)
 for german,gender,shabbat in product([False,True,None],['male','female',None],[False,True,None]):
  name=f'german_{german}_gender_{gender}_shabbat_{shabbat}';configuration=json.loads(json.dumps(base));d=configuration.setdefault('declarations',{});d['opensiddur:rite']={'german':german};d['opensiddur:person']={'gender':gender};d.setdefault('opensiddur:holiday-aggregate',{})['shabbat']=shabbat
  path=output/(name+'.yaml');path.write_text(yaml.safe_dump(configuration,sort_keys=False,allow_unicode=True));ld=LinearData();load_settings(path,linear_data=ld,project_directory=project);book=read_settings(path,project_directory=project,resolve_fonts=False).book
  result=ExternalCompilerProcessor(book.project,book.file_name,linear_data=ld,reference_database=db).process()[0];drop_empty_scopes(result);close_up_whitespace(result);join_split_paragraphs(result);merge_credits(result,ld);xml=output/(name+'.xml');xml.write_bytes(etree.tostring(result,pretty_print=True,encoding='utf-8'))
  body=result.find('.//'+T+'body');calls=[n.get('target').split('@',1)[0]for n in body.iter(P+'transclude')];counter=Counter(calls);issues=[]
  def check(value,message):
   if not value:issues.append(message)
  expected=2 if german is None else 1
  for key in torah:check(counter[targets[key]]==expected,'Torah block count: '+key)
  check(counter[targets['elohai_neshamah']]==1,'ElohaiNeshamah must occur once')
  positions=[i for i,v in enumerate(calls)if v==targets[torah[0]]];elohai=calls.index(targets['elohai_neshamah']);attah=calls.index(targets['attah_hu_bashamayim'])
  if german is True:check(positions[0]>attah>elohai,'German late block order')
  elif german is False:check(positions[0]<elohai<attah,'Other rites early block order')
  else:check(positions[0]<elohai<attah<positions[1],'Unresolved rite alternatives')
  check(counter[targets['birkhot_hashachar_shelo_asani_ishah']]==int(gender!='female'),'Male blessing selection')
  check(counter[targets['birkhot_hashachar_sheasani_kirtzono']]==int(gender!='male'),'Female blessing selection')
  check(counter[targets['qorbanot_musaf_shabbat']]==int(shabbat is not False),'Shabbat offering selection')
  check(counter[targets['eizehu_meqoman']]==1 and counter[targets['middot']]==1,'Study units must remain outsideShabbat gate')
  check(counter['urn:x-opensiddur:text:bible:psalms/17/6']==2,'Repeated Psalm17:6 extent')
  barukh=[n for n in body.iter(P+'transclude')if n.get('target')=='urn:x-opensiddur:text:prayer:shema/barukh_shem']
  check(len(barukh)==2,'Two BarukhShem recitations')
  if len(barukh)==2:
   check(any(n.get('role')=='parallel'for n in barukh[0].iter(P+'parallelItem')),'Morning BarukhShem translation missing')
   check(not any(n.get('role')=='parallel'for n in barukh[1].iter(P+'parallelItem')),'Korbanot BarukhShem must remain Hebrew-only')
  text=' '.join(''.join(body.itertext()).split())
  check(text.count('Blessed be His glorious royal Name for ever and ever.')==1,'Unprinted English BarukhShem leakage')
  check(not any(n.get('type')=='page'for n in body.iter(T+'ref')),'Expanded output contains required navigation')
  labels=[n for n in body.iter(J+'conditional')if n.find(T+'note')is not None]
  if gender is not None:check(not any('preceding benediction' in ''.join(n.itertext())for n in labels),'Resolved gender condition still labels the variant')
  if shabbat is not None:check(not any('On Shabbat' in ''.join(n.itertext())for n in labels),'ResolvedShabbat condition still labels the insertion')
  # The canonical first Psalm17:6 has distinct attested English printings at its two calls.
  psalms=[n for n in body.iter(P+'transclude')if n.get('target')=='urn:x-opensiddur:text:bible:psalms/17/6'];en=[]
  for n in psalms:
   en.append(' '.join(' '.join(''.join(p.itertext())for p in n.iter(P+'parallelItem')if p.get('role')=='parallel').split()))
  check(len(en)==2 and en[0]!=en[1] and all(en),'Distinct Psalm17:6 translations')
  row={'case':name,'settings':str(path),'compiled_xml':str(xml),'compiled_sha256':hashlib.sha256(xml.read_bytes()).hexdigest(),'german':german,'gender':gender,'shabbat':shabbat,'calls':len(calls),'psalm_17_6_english':en,'findings':issues};report['cases'].append(row);report['findings'] += [{'case':name,'finding':i}for i in issues];print(name,'OK'if not issues else issues,flush=True)
report['status']='passed'if not report['findings']else'failed';(output/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print('MATRIX',report['status'],len(report['cases']),len(report['findings']))
