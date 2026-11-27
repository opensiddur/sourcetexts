from pathlib import Path
import json,hashlib,shutil
S=Path('/home/efeins/.codex/worktrees/marmorstein-day-two-sources/master/sources/marmorstein_rosh_hashanah_2');B=S/'batches/pesuqei_s46_s63';p=B/'working/adjudicated_pages.json'
def write(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
d=json.loads(p.read_text());before=sha(p);archive=B/'reconciliation/rejected_composition_v3.json';assert not archive.exists();shutil.copyfile(p,archive)
changes=[(54,0,3,'עַצְמוֹתָיו','עַצְמֹתָיו','s54-atzmotav'),(54,0,5,'פּוֹדֶה','פֹּדֶה','s54-podeh'),(56,2,7,'אֹתוֹת','אוֹתֹת','s56-otot'),(60,2,0,'רַנְּנוּ','רַנֲנוּ','s60-rannenu'),(56,2,0,'הַלְלוּיָהּ','הַלֲלוּיָהּ','s56-halleluyah-first'),(56,2,0,'הַלְלוּ','הַלֲלוּ','s56-hallelu-second'),(56,2,1,'הַלְלוּיָהּ','הַלֲלוּיָהּ','s56-hallelu-fourth'),(58,0,7,'הַלְלוּיָהּ','הַלֲלוּיָהּ','s58-halleluyah-last')]
ledger=[]
for scan,bi,li,old,new,e in changes:
 page=next(x for x in d['pages']if x['scan']==scan);b=page['blocks'][bi];line=b['lines'][li];n=line.count(old);assert n in (1,2),(scan,old,n);b['lines'][li]=line.replace(old,new);ledger.append({'scan':scan,'block':bi,'line':li,'before':line,'after':b['lines'][li],'count':n,'evidence':'dedicated_readers/final/pesuqei-q-'+e+'.json'})
for page in d['pages']:
 for b in page['blocks']:
  if page['language']=='he':b['text']='\n'.join(b['lines'])
 body=[x for x in page['blocks']if x['kind']!='citation'];page['first_line']=body[0]['lines'][0];page['last_line']=body[-1]['lines'][-1]
d['status']='corrected_source_composition_v4; awaiting bounded amendment closure and question1023';write(p,d)
for src in Path('/tmp').glob('pesuqei-q-*.json'):
 dest=B/'dedicated_readers/final'/src.name
 if not dest.exists():shutil.copyfile(src,dest)
cache=Path('/home/efeins/src/opensiddur-repos/output/marmorstein_rosh_hashanah_2/psuqei_s46_s63/adjudication_final');cache.mkdir(parents=True,exist_ok=True)
for src in Path('/tmp').glob('pesuqei-q-*-crop.png'):shutil.copyfile(src,cache/src.name)
for lo in (46,52,58):
 scope=B/f'scoped_sources/v4/pages_{lo}_{lo+5}.json';write(scope,{'status':'corrected scoped source for independent approval; not batch acceptance','scans':list(range(lo,lo+6)),'pages':[x for x in d['pages']if lo<=x['scan']<=lo+5]})
write(B/'reconciliation/source_composition_v4.json',{'status':'bounded corrections awaiting closure','before_sha256':before,'after_sha256':sha(p),'changes':ledger,'method':'Differences suggested checks; every changed reading independently read from this scan in an enlarged crop. Other-edition words never copied as evidence.'})
print('Applied',sum(x['count'] for x in ledger),'individual word corrections',sha(p))
