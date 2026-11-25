from pathlib import Path
import json,copy
p=Path('/tmp/mahzor-s312');d=json.load(open(p/'spine-draft.json'));c=json.load(open(p/'candidate-v4.json'))
# These are local word-specific adjudications, confirmed from enlarged source crops.
changes=[('וְיוֹסִֽיפוּ לְּךָ','וְיוֹסִֽיפוּ לְךָ'),('יְהוָ֖ה','יְהֹוָ֖ה'),('וְיִתְרוֹמַם','וְיִתְרֹמַם')]
def patch(x):
 if isinstance(x,dict):
  for k,v in x.items():
   if k=='text' and isinstance(v,str):
    for a,b in changes:v=v.replace(a,b)
    x[k]=v
   else:patch(v)
 elif isinstance(x,list):
  for v in x:patch(v)
patch(d);patch(c)
history=[]
for b in c['blocks']:
 notes={k:b.pop(k) for k in ['uncertainties','changes_from_primary'] if k in b}
 if notes:history.append(dict(scan=b['scan'],key=b['key'],historical_notes=notes,status='Historical candidate-v3 observations superseded by word audits, meteg closures, human473–489 and final source closure. Not current unresolved flags.'))
(p/'candidate-historical-notes.json').write_text(json.dumps(history,ensure_ascii=False,indent=2)+'\n')
c['status']='Adjudicated candidate-v5; final independent source closure pending';c['final_source_evidence']=['source-last-crops-review.json','closure-three-dots-review.json','human-473-489-resolution.json'];(p/'candidate-v5.json').write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n');(p/'spine-draft.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
ledger=json.load(open(p/'source-difference-audit-ledger.json'))
for e in ledger:
 if e['id'] in [2,72,115]:e.update(choice='custom',literal={2:'כָּל',72:'בּוֹנָֽיִךְ',115:'בֵּית'}[e['id']],reason='Final enlarged native image adjudication; see closure-three-dots-review.json or source-last-crops-review.json.',uncertainty='Closed by agreement of primary image adjudication and independent enlarged crop reading; no unresolved contrary reading.')
 if e['id']==100:e.update(choice='A',literal='חזן',reason='Final nun visible; primary and final-source-322-review agree. Earlier חז reading superseded.',uncertainty='closed')
 if e['id']==11:e.update(choice='human',literal='בשערי ציון כתוב שלא יאמר אצל שלום הרבון רק יאמר זה:',reason='User479',uncertainty='closed')
(p/'source-difference-audit-ledger-final.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n')
proof=dict(status='Primary adjudication with independent enlarged source evidence, pending full scope closure',retained_dots=[490,492,497],fixed_no_lamed_dagesh=491,restored_holam=[493,494,495],corrected_defective_vayitromam=496,source_difference_ids_closed=[2,72,115],human_all_resolved=True,historical_notes_archived='candidate-historical-notes.json')
(p/'source-final-dispositions.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n');print('Applied crop-verified final source fixes; historical notes archived, not silently discarded.')
