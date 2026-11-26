from pathlib import Path
import sys,json,unicodedata,hashlib
from lxml import etree
ns={'j':'http://jewishliturgy.org/ns/jlptei/2'}
results={}
for path in Path(sys.argv[1]).glob('prayerbook_for_the_new_year_second_day-*/*.xml'):
 tree=etree.parse(str(path));tokens=[]
 for name in tree.xpath('//j:divineName',namespaces=ns):
  token=''.join(name.itertext());bare=''.join(c for c in token if '\u05d0'<=c<='\u05ea')
  assert bare in ['יי','יהוה'],(path,token)
  preceding=name.getprevious().tail if name.getprevious() is not None else name.getparent().text
  if preceding:assert not ('\u05d0'<=preceding[-1]<='\u05ea' or unicodedata.combining(preceding[-1])),(path,'starts inside word')
  if name.tail:assert not ('\u05d0'<=name.tail[0]<='\u05ea' or unicodedata.combining(name.tail[0])),(path,'ends inside word')
  tokens.append(token)
 results[str(path)]={'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'divine_name_tokens':tokens}
print(json.dumps({'status':'passed','scope':'Current daytwo files; exact yy/YHWH forms and wholeword or maqaf boundaries','files':results},ensure_ascii=False,indent=2))
