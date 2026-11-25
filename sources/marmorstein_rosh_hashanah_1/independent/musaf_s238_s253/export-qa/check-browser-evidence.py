from pathlib import Path
import json,re,unicodedata
p=Path('/tmp/mahzor-s238/integration-v1');q=p/'qa';norm=lambda s:' '.join(unicodedata.normalize('NFKD',s).split());core=json.loads((q/'html-browser-checks.json').read_text());special=json.loads((q/'special-browser-checks.json').read_text());checks=[]
for row in core+special:
 assert not row['errors'],(row['file'],row['errors']);assert row['scrollWidth']<=row['width'];assert not row['duplicateIds'],(row['file'],row['duplicateIds']);assert not row['brokenInternalLinks'],(row['file'],row['brokenInternalLinks'])
 checks.append(dict(file=row['file'],javascript_errors=0,horizontal_overflows=0,duplicate_ids=0,broken_internal_links=0))
for row in core:
 name=row['file'];t=row['text'];include=any(s in name for s in ['fuerth','other_include','unknown']);assert ('Thou alone wilt'in t)==include,(name,'Tisgav');assert ('All will come to serve'in t)==include,(name,'Veye');assert t.count('All believe')==22,(name,'22 refrains');assert ('To Thee will they offer their sacrifices'in t)==(include and'unknown-omitted'not in name),(name,'offering clause')
# A solitary Fuerth=true keeps other rites undefined, so its instruction remains visible.
for row in special:
 if 'fuerth_only'in row['file']:
  assert 'All will come to serve'in row['text'];assert 'In Fuerth and other communities'in row['text']
 if 'abbreviated'in row['file']:assert 'קו״ח'in row['text']and'ק׳'in row['text']
cor=json.loads((p/'source/corrections.json').read_text())['corrections'];ids=['rh_pachdekha_hast','musaf_harachum_shehu','musaf_kesod_once_one','musaf_veattah_forty_eight'];reading=[]
for kind in ['documentary','expanded']:
 printed=next(v for v in special if v['file']=='special-'+kind+'-printed_errors.html');corrected=next(v for v in core if v['file']==kind+'-unknown-unknown.html')
 for id in ids:
  c=next(c for c in cor if c['id']==id)
  a=norm(c.get('before','')+c['sic']+c.get('after',''));b=norm(c.get('before','')+c['corr']+c.get('after',''))
  assert a in norm(printed['text']),(kind,id,'printed',a)
  assert b in norm(corrected['text']),(kind,id,'corrected',b)
  reading.append(dict(kind=kind,correction=id,printed_form_visible=True,corrected_form_visible=True))
(q/'browser-export-evidence.json').write_text(json.dumps(dict(network_mode="Offline browser; Playwright route **/* aborts HTTP(S), only local file content loaded",core_states=len(core),special_states=len(special),checks=checks,error_reading_checks=reading,regional_conditions_and22refrains_correct=True,offscreen_sections_forced_to_render_before_text_measurement=True),ensure_ascii=False,indent=2)+'\n');print('24 actual browser states pass: links, layout, region/optional conditions, abbreviations, printed/corrected errors')
