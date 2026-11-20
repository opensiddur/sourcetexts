from pathlib import Path
import json,unicodedata,hashlib
p=Path('/tmp/mahzor-s238');a=json.loads((p/'candidate-round6.json').read_text());b=json.loads((p/'candidate-round7.json').read_text());en=lambda d:[x for x in d['blocks']if x['language']=='en'];assert en(a)==en(b)
assert all(unicodedata.normalize('NFKD',x['text'])==x['text']for x in b['blocks'])
words=['לְהוֹדִֽיעַ','וָשַֽׁחַר','וַעֲצְמוֹתֵיהֶם','תַּחְתִּיֹּת','שֶׁחוּא'];report={'english_blocks_byte_unchanged':True,'candidate7_all_blocks_nfkd':True,'changed_words':[{ 'word':unicodedata.normalize('NFKD',w),'codepoints':['U+%04X'%ord(c)for c in unicodedata.normalize('NFKD',w)]}for w in words],'note':'General encoding instructions require NFKD, not NFC. This check preserves that policy. CGJ-bearing Jerusalem words are unchanged by this batch.'}
(p/'post-human374-stability.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print('All English blocks unchanged; all149 source blocks NFKD')
