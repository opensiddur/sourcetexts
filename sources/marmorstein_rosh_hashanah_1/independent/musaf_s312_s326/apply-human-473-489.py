from pathlib import Path
import json,copy
p=Path('/tmp/mahzor-s312');d=json.load(open(p/'spine-draft.json'));before=copy.deepcopy(d)
replacements=[('כלל שלום הרבון','אצל שלום הרבון'),('אֲנִי שֶׁלָּךְ וַחֲלוֹמוֹתַי שֶׁלָּךְ','אֲנִי שֶׁלָּךְ וַחֲלוֹמוֹתַי שֶׁלָּךְ'),('לַיהוָה֙','לְיהֹוָה֙'),('יְסֹ֣בְבֶ֔נְהוּ','יְסֹֽבְבֶ֙נְהוּ֙')]
def patch(x):
 if isinstance(x,dict):
  for k,v in x.items():
   if isinstance(v,str) and k=='text':
    for a,b in replacements:v=v.replace(a,b)
    x[k]=v
   else:patch(v)
 elif isinstance(x,list):
  for v in x:patch(v)
patch(d)
by={u['stem']:u for u in d['units']}
f=by['rh_minchah_ashrei']['languages']['he'][0]['fragments'][0];assert 'סֶֽלָה' in f['text'];f['text']=f['text'].replace('סֶֽלָה','סֶּֽלָה')
# The other confirmed marks already match the staged source; retain them unchanged.
answers={473:'no dagesh',474:'no meteg',475:'lamed dagesh present',476:'no kaf dagesh',477:'אין series: all initial kafs have dagesh; מי series: none',478:'samekh dagesh and lamed dagesh present',479:'בשערי ציון כתוב שלא יאמר אצל שלום הרבון רק יאמר זה:',480:'אֲנִי שֶׁלָּךְ וַחֲלוֹמוֹתַי שֶׁלָּךְ',481:'הַ לְיהֹוָה (pashta); star above enlarged ה',482:'pashta on second bet and shuruq; meteg on samekh',483:'second lamed meteg present',484:'mem meteg',485:'mem meteg present',486:'first mem meteg',487:'he meteg present',488:'tsadi meteg',489:'ayin meteg'}
ledger=json.load(open(p/'human-473-478.json'))
for q in ledger:q['answer']=answers[q['number']];q['adjudication_source']='explicit user reading, 2026-11-23'
(p/'human-473-478.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n')
# Keep the frozen primary untouched; update only the current candidate and structured source blocks.
c=json.load(open(p/'candidate-v3.json'));patch(c)
for seq in [c['blocks'],d['source_blocks']]:
 for block in seq:
  if block.get('scan')=='s323' and block.get('key')=='ashrei_intro' and 'text' in block:block['text']=block['text'].replace('סֶֽלָה','סֶּֽלָה')
c['human_adjudications']=ledger;c['status']='Human473–489 applied; independent source closure pending';(p/'candidate-v4.json').write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')
d['human_adjudications']=ledger;(p/'spine-draft.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
w=json.load(open(p/'work.json'));w['human_pending']=[];w['status']='human_readings_resolved_independent_closure_pending';(p/'work.json').write_text(json.dumps(w,ensure_ascii=False,indent=2)+'\n')
(p/'human-473-489-resolution.json').write_text(json.dumps(dict(status='All17 human decisions recorded; not overall acceptance',answers=answers,large_he_star='Existing haazinu_large_he footnote anchor preserves printed star semantics; not a Hebrew accent.',pashta_interpretation='User lists second bet and final shuruq as pashta hosts; samekh has meteg.',changed_units=[u['stem'] for u,v in zip(d['units'],before['units']) if u!=v]),ensure_ascii=False,indent=2)+'\n')
print('Applied17 human decisions; frozen primary unchanged.')
