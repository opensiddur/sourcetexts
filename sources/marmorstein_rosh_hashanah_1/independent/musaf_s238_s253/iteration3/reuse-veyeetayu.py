from pathlib import Path
import json,copy,unicodedata
def N(s):return unicodedata.normalize("NFKD",s)
p=Path('/tmp/mahzor-s238/iteration3');d=json.loads((p/'draft-poem-units-refined.json').read_text());u=next(u for u in d['units']if u['stem']=='musaf_veyeetayu');old=u['urn'];new='urn:x-opensiddur:text:poem:v_yeetayu_kol_leavdekha';u['urn']=new;u['stem']='musaf_v_yeetayu_kol_leavdekha'
starts={'he':['וְיֶאֱתָיוּ','וְיִדְרְשׁוּךָ','(וְיִזְבְּחוּ','וְיִירָאוּךָ','וִימַלְּלוּ','וִיסַלְּדוּ','וְיִפְצְחוּ','וְיִשְׁמְעוּ'],'en':['All will come','Peoples that','(To Thee','At sunrise','talk of Thy might','Trembling will','so that the mountains','those far away']}
for lang,ss in list(u['languages'].items()):
 fragments=[copy.deepcopy(f)for s in ss for f in s['fragments']];alltext='';positions=[]
 for f in fragments:
  if alltext and not alltext[-1].isspace():alltext+=' '
  a=len(alltext);alltext+=f['text'];positions.append((a,len(alltext),f))
 boundaries=[alltext.index(N(t))for t in starts[lang]]+[len(alltext)];out=[]
 for n,(a,b)in enumerate(zip(boundaries,boundaries[1:]),1):
  fs=[]
  for left,right,f in positions:
   if max(left,a)<min(right,b):
    ff=copy.deepcopy(f);ff['text']=alltext[max(left,a):min(right,b)];fs.append(ff)
  assert fs,(lang,n)
  out.append(dict(paragraph=1,corresp=new+'/'+str(n),reference_unit='stanza',fragments=fs))
 out[-1]['end_reference']=True;u['languages'][lang]=out
# The parenthetical offering clause is preserved as an explicitly named, unresolved optional reading.
condition='urn:x-opensiddur:condition:poem:v_yeetayu_kol_leavdekha/veyizbechu'
for lang,ss in u['languages'].items():
 s=ss[2];fs=s['fragments'];joined=' '.join(f['text']for f in fs);close=joined.index(')')+1
 optional=[];rest=[];remaining=close
 for f in fs:
  t=f['text'];ff=copy.deepcopy(f)
  if remaining>=len(t):optional.append(ff);remaining-=len(t)+1
  elif remaining>0:
   ff['text']=t[:remaining];optional.append(ff);tail=copy.deepcopy(f);tail['text']=t[remaining:];rest.append(tail);remaining=0
  else:rest.append(ff)
 assert optional[0]['text'].startswith('(')and optional[-1]['text'].endswith(')'),(lang,optional)
 marker=copy.deepcopy(optional[0]);marker['text']=''
 boundary=dict(paragraph=1,corresp=new+'/3',reference_unit='stanza',fragments=[marker])
 opt=dict(paragraph=1,conditions=[dict(type='opensiddur:variant',features={condition:True})],marked=True,fragments=optional)
 continuation=dict(paragraph=1,fragments=rest)
 ss[2:3]=[boundary,opt,continuation]
(p/'draft-poem-units-v2.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
(p/'veyeetayu-identity-decision.json').write_text(json.dumps(dict(status='Existing identity reused; source/guideline approval still pending',canonical=new,stanzas=[new+'/'+str(i)for i in range(1,9)],registry='specs/urn_registry/poem.jsonl',discovery='identity-search.json',source='Existing Hebrew project v_yeetayu_kol_lavdekha-300-he confirms exact8stanza extents. Only its identities are reused; this edition retains its own words and Marmorstein English. No Zangwill translation supplied.',discarded_unregistered_draft_identity=old,optional_parenthetical_condition=condition),ensure_ascii=False,indent=2)+'\n');print('Reused existing root and8stanza identities; preserved page-independent alignment and optional clause')
