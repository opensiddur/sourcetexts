from pathlib import Path
import json,unicodedata,copy
p=Path('/tmp/mahzor-s238');N=lambda s:unicodedata.normalize('NFKD',s);d=json.loads((p/'candidate-round6.json').read_text());m=json.loads((p/'iteration3/poem-units-revised.json').read_text());log=[]
patches=[(362,'s238','chashot_beratzo','מֵרְעִישׁוֹת','מֵרְעִישׁוֹת'),(363,'s240','kaf_regel','יְפַרְשֵׁז','יְפַרְשֵׁז'),(364,'s240','mimekomo','עֶרֶב','עֶֽרֶב'),(365,'s242','im_yashkit','לְהוֹדִיעַ','לְהוֹדִֽיעַ'),(366,'s242','od_yizakher','וָשַׁחַר','וָשַֽׁחַר'),(367,'s242','mimekomo','יִפֶן','יִֽפֶן'),(368,'s244','veatah_azon_kol','בְּקַרְסֻלֵּיהֶם','בְּקַרְסֻלֵּיהֶם'),(369,'s246','adir_adirenu_1','אַדִּיר','אַדִּיר'),(370,'s246','adir_adirenu_2','אַדִּיר','אַדִּיר'),(371,'s246','adir_adirenu_1','עַל','עַל'),(372,'s246','tehillot_kevodecha','תַּחְתִּיּוֹת','תַּחְתִּיֹּת'),(373,'s250','in_fuerth_veetayu_rubric','סאַלטעט','סאַלטעט'),(374,'s250','harachum_umakdim','שֶׁהוּא','שֶׁחוּא')]
# This unambiguous source correction was independently identified and is tracked separately from human answers.
patches.append(('source-round3-242','s244','sam_halikhot','וַעֲצָמוֹתֵיהֶם','וַעֲצְמוֹתֵיהֶם'))
for number,scan,key,old,new in patches:
 old,new=N(old),N(new);block=next(b for b in d['blocks']if(b['scan'],b['key'])==(scan,key));assert old in block['text'],(number,key,old)
 # For unchanged common words record their presence without altering other occurrences.
 block['text']=block['text'].replace(old,new);count=0
 for u in m['units']:
  for ss in u['languages'].values():
   for s in ss:
    for f in s['fragments']:
     if f['scan']!=scan:continue
     if number==374 and N(' רַךְ לִרְצוֹת')not in f['text']:continue
     if old==new:continue
     if old in f['text']:f['text']=f['text'].replace(old,new);count+=1
     for a in f.get('alternatives',[]):
      if old in a.get('printed',''):a['printed']=a['printed'].replace(old,new)
      for r in a.get('readings',[]):
       if isinstance(r,dict)and old in r['text']:r['text']=r['text'].replace(old,new)
 log.append(dict(number=number,scan=scan,key=key,old=old,new=new,encoded_fragment_applications=count,authority='User exact adjudication'if isinstance(number,int)else'Independent definite source correction'))
answers={362:'no mem meteg',363:'no pe dagesh',364:'yes ayin meteg',365:'yes dalet meteg',366:'patah+meteg',367:'yes yod meteg',368:'בְּקַרְסֻלֵּיהֶם',369:'alef patah and dalet dagesh',370:'alef patah and dalet dagesh',371:'ayin patah',372:'no vav after yod',373:'סאַלטעט',374:'chet; encode sic/corr'}
d['status']='Candidate after human readings through374. All currently asked questions answered; final independent source-closure verdict and encoding/integration/export acceptance remain pending.'
(p/'candidate-round7.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');(p/'human-362-374.json').write_text(json.dumps(dict(answers=answers,applications=log,notes=['373 supplied spelling is preserved exactly; no normalization to German schaltet.','374 printed chet is retained; correction to he is a separate sic/corr layer, never a silent source-text substitution.']),ensure_ascii=False,indent=2)+'\n')
m['status']='Draft revised only for human362–374 and definite source-round3 correction; encoding round2 approved earlier version. Targeted follow-up review required.'
(p/'iteration3/poem-units-revised.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
correction=dict(id='musaf_harachum_shehu',file='prayerbook_for_the_new_year-heidenheim-1965-he/musaf_haochez_beyad_middat_mishpat.xml',scan='s250',sic=N('שֶׁחוּא'),corr=N('שֶׁהוּא'),before='',after=N(' רַךְ לִרְצוֹת'),evidence='https://archive.org/download/mahzor-lyom-rishon-shel-rosh-hashanah-day-one-jenny-marmorstein-1965/page/n249.jpg',reason='Source prints closed chet in place of he. User confirmed reading374 and explicitly requested sic/corr.',authority='User reading374')
(p/'iteration3/pending-corrections.json').write_text(json.dumps({'policy':'Unapproved batch correction layer; not yet installed in accepted corrections.json','corrections':[correction]},ensure_ascii=False,indent=2)+'\n')
print('All13 human answers applied;',sum(x['old']!=x['new']for x in log),'changed source spans; sic/corr staged separately')
