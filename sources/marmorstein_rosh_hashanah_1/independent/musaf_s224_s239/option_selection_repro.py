from pathlib import Path
import tempfile
from lxml import etree
from opensiddur.exporter.external_compiler import ExternalCompilerProcessor
from opensiddur.exporter.inline_compiler import InlineCompilerProcessor
from opensiddur.exporter.linear import reset_linear_data,get_linear_data
from opensiddur.exporter.refdb import ReferenceDatabase
T='http://www.tei-c.org/ns/1.0';J='http://jewishliturgy.org/ns/jlptei/2';C='urn:x-opensiddur:condition:prayer:example/'
with tempfile.TemporaryDirectory()as tmp:
 pr=Path(tmp);(pr/'example').mkdir();root=etree.Element(('{'+T+'}')+'TEI',nsmap={'tei':T,'j':J});root.set('{http://www.w3.org/XML/1998/namespace}lang','en');div=etree.SubElement(etree.SubElement(etree.SubElement(root,('{'+T+'}')+'text'),('{'+T+'}')+'body'),('{'+T+'}')+'div');div.set('corresp','urn:x-opensiddur:text:prayer:example');declare=etree.SubElement(div,('{'+J+'}')+'declare');declare.set('{http://www.w3.org/XML/1998/namespace}id','selection');fs=etree.SubElement(declare,('{'+T+'}')+'fs',type='opensiddur:variant')
 for name,value in [('first','false'),('second','true')]:etree.SubElement(etree.SubElement(fs,('{'+T+'}')+'f',name=C+name),('{'+T+'}')+'binary',value=value)
 para=etree.SubElement(div,('{'+T+'}')+'p');choice=etree.SubElement(para,('{'+T+'}')+'choice')
 for name in ['first','second']:etree.SubElement(choice,('{'+J+'}')+'option',corresp=C+name).text=name
 etree.SubElement(div,('{'+J+'}')+'endDeclare',target='#selection');path=pr/'example/example.xml';path.write_bytes(etree.tostring(root));db=ReferenceDatabase(pr/'reference.db')
 for cls in [ExternalCompilerProcessor,InlineCompilerProcessor]:
  reset_linear_data();ld=get_linear_data();ld.xml_cache.base_path=pr;span=root.getroottree().getpath(div);proc=cls('example','example.xml',span,span,linear_data=ld,reference_database=db);out=proc.process();nodes=out if isinstance(out,list)else[out];text=''.join(''.join(n.itertext())for n in nodes if n is not None);print(cls.__name__,repr(text))
