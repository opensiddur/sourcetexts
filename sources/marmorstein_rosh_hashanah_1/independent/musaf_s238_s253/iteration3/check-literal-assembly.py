from pathlib import Path
import json,re,hashlib,unicodedata
from opensiddur.importer.marmorstein_rosh_hashanah_1.realizations import join_source_fragments
p=Path('/tmp/mahzor-s238');rows=json.loads((p/'candidate-round7.json').read_text())['blocks'];units=json.loads((p/'iteration3/poem-units-revised.json').read_text())['units'];by={u['stem']:u for u in units}
expected={
'vechayyot_asher_hennah':{'he':[(238,'vechayot_asher'),(238,'chashot_beratzo'),(240,'kaf_regel'),(240,'levilti_lenabel'),(240,'rahem_metsukim')],'en':[(241,'rachem')]},
'veammekha_teluim':{'he':[(240,'veamkha_teluim'),(242,'kol_shofar_kafuf'),(242,'semukhim_betzidkat'),(242,'lehizakher_lamo'),(242,'im_yashkit'),(242,'od_yizakher')],'en':[(241,'amekha'),(243,'amekha'),(243,'lehaver'),(243,'od_yizkor')]},
'veattah_ezon_qol':{'he':[(244,'veatah_azon_kol'),(244,'sam_halikhot'),(244,'yisu_ayin')],'en':[(245,'veattah'),(245,'yissau')]},
'tehillot_kevodekha':{'he':[(246,'tehillot_kevodecha'),(246,'lehitvada_ulehigalot')],'en':[(247,'tehillot'),(247,'lehodiya')]},
'qedushah_conclusion_parts':{'he':[(246,'ki_makdishecha'),(248,'elohenu_al_yisrael_cont'),(248,'od_yizkor_lanu')],'en':[(247,'ki_maqdish'),(249,'ki_maqdish')]},
'haochez_beyad_middat_mishpat':{'he':[(int(b['scan'][1:]),b['key'])for b in [b for b in rows if b['key']in ['haochez_beyad','haboḥen','hagoel','hadan','hehagui','havadai','hazocher','hachotech','hatov','hayodea','hakol_yochal','halan','hamamlich','hanoheg','hasovel','haelyon','hapoteach_petach','hatsofeh_larasha','hakatsar_bezaam','harachum_umakdim','hashaveh_umashveh','hatam_umitamem']]],'en':[(249 if i<=16 else 251,'haochez_'+str(i))for i in range(1,23)]},
'v_yeetayu_kol_leavdekha':{'he':[(250,'veyeetayu_kol'),(252,'lekha_et_zivheihem_continuation')],'en':[(251,'veyetayu'),(253,'veyetayu')]}}
def clean(t):
 t=unicodedata.normalize('NFKD',t)
 return ' '.join(re.sub(r'(?:קו״ח|קה״ח|קר״ס|ק׳|ח׳)\s+','',t).split())
checks=[]
for stem,langs in expected.items():
 u=by['musaf_'+stem]
 for lang,keys in langs.items():
  blocks=[next(b for b in rows if b['scan']==f's{n}'and b['key']==k)for n,k in keys];text=' '.join(b['text']for b in blocks)
  if stem=='vechayyot_asher_hennah'and lang=='he':
   main='וְחַיָּה לְחַיָּה וּכְרוּב לִכְרוּב';variant=next(b['text']for b in rows if b['key']=='variant_ka');text=unicodedata.normalize('NFKD',text).replace(unicodedata.normalize('NFKD',main),unicodedata.normalize('NFKD',main+' '+variant))
  rendered=''.join(f['text']for s in u['languages'][lang]for f in s['fragments'])
  # Distinct source paragraphs need a separator, while interior alignment splits preserve their original spaces.
  rendered=join_source_fragments([f for s in u['languages'][lang]for f in s['fragments']])
  left,right=clean(text),clean(rendered);ok=left==right;checks.append(dict(stem=stem,lang=lang,source_blocks=keys,candidate_sha256=hashlib.sha256(left.encode()).hexdigest(),encoded_literal_sha256=hashlib.sha256(right.encode()).hexdigest(),matches=ok))
  if not ok:
   import difflib
   print(stem,lang,' '.join(difflib.ndiff(left.split(),right.split())))
(p/'iteration3/literal-assembly-check.json').write_text(json.dumps(dict(status='Literal assembly coverage only; not source or guideline acceptance',checks=checks),ensure_ascii=False,indent=2)+'\n');print(sum(c['matches']for c in checks),'/',len(checks),'literal assembly comparisons match')
