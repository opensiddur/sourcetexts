import {spawn} from 'node:child_process';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
const root='/home/efeins/src/opensiddur-repos/output/marmorstein_rosh_hashanah_2/morning_s25_s45/exports';
const cache=await fs.mkdtemp(path.join(os.tmpdir(),'day2-html-review-'));
const server=spawn('/usr/bin/python3',['-m','http.server','8927','--bind','127.0.0.1','--directory',root],{stdio:'ignore'});
const chrome=spawn('/usr/bin/google-chrome',['--headless','--no-sandbox','--disable-gpu','--disable-dev-shm-usage','--remote-debugging-port=8928','--user-data-dir='+cache,'about:blank'],{stdio:'ignore'});
const delay=ms=>new Promise(r=>setTimeout(r,ms));let ws;
try {
 let target;
 for(let i=0;i<100;i++){try{target=await(await fetch('http://127.0.0.1:8928/json/new?about:blank',{method:'PUT'})).json();break;}catch{await delay(100);}}
 if(!target)throw Error('Chrome did not start');
 ws=new WebSocket(target.webSocketDebuggerUrl);await new Promise((r,j)=>{ws.onopen=r;ws.onerror=j;});
 let sequence=0;const pending=new Map(),errors=[];
 ws.onmessage=event=>{const value=JSON.parse(event.data);if(value.id){const item=pending.get(value.id);if(item){pending.delete(value.id);value.error?item.reject(Error(JSON.stringify(value.error))):item.resolve(value.result);}}else if(value.method==='Runtime.exceptionThrown'){errors.push(value.params.exceptionDetails.text);}};
 function rpc(method,params={}){return new Promise((resolve,reject)=>{const id=++sequence;pending.set(id,{resolve,reject});ws.send(JSON.stringify({id,method,params}));});}
 async function evaluate(expression){const r=await rpc('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});if(r.exceptionDetails)throw Error(JSON.stringify(r.exceptionDetails));return r.result.value;}
 await rpc('Page.enable');await rpc('Runtime.enable');
 async function navigate(name,width=1280){await rpc('Emulation.setDeviceMetricsOverride',{width,height:1000,deviceScaleFactor:1,mobile:width<500});await rpc('Page.navigate',{url:'http://127.0.0.1:8927/'+name+'/book.html'});for(let i=0;i<100;i++){await delay(80);if(await evaluate("document.readyState==='complete'&&!!document.getElementById('os-book')"))break;}await delay(250);}
 async function screenshot(file,needle){if(needle)await evaluate(`(()=>{const n=[...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].find(n=>n.textContent.trim()===${JSON.stringify(needle)});if(n)window.scrollTo(0,n.getBoundingClientRect().top+window.scrollY-65);return !!n;})()`);await delay(150);const r=await rpc('Page.captureScreenshot',{format:'png',captureBeyondViewport:false});await fs.writeFile(file,Buffer.from(r.data,'base64'));}
 const report={profiles:{},matrix:[],errors};
 for(const name of ['documentary_hebrew','documentary_parallel','expanded','night_expanded']){
  await navigate(name);const details=await evaluate(`(()=>{const ids=[...document.querySelectorAll('[id]')].map(n=>n.id);const missing=[...document.querySelectorAll('a[href^="#"]')].map(n=>n.getAttribute('href').slice(1)).filter(id=>id&&!document.getElementById(id));return {title:document.title,duplicateIds:ids.filter((id,i)=>ids.indexOf(id)!==i),missingFragmentLinks:missing,scanLinks:document.querySelectorAll('a.scan-link').length,horizontalOverflow:document.documentElement.scrollWidth>innerWidth+1,headings:[...document.querySelectorAll('main h1,main h2,main h3,main h4')].map(n=>n.textContent.trim())};})()`);
  if(details.duplicateIds.length||details.missingFragmentLinks.length)throw Error(name+' bad anchors '+JSON.stringify(details));
  await screenshot(root+'/'+name+'/browser-wide.png',name==='night_expanded'?'Evening Prayer for the New Year':name==='documentary_hebrew'?'תְּפִלּוֹת.':'Prayers');
  const scan=await evaluate(`(()=>{const link=[...document.querySelectorAll('a.scan-link[data-scan-view]')].find(n=>n.getClientRects().length);if(!link)return null;const href=link.href;link.click();const state=window.OSScanViewer.state();window.OSScanViewer.close();return {href,state};})()`);
  details.scanViewer=scan;
  const note=await evaluate(`(()=>{const button=[...document.querySelectorAll('main button.note-ref')].at(-1);if(!button)return null;button.scrollIntoView({block:'center'});return button.getAttribute('popovertarget');})()`);
  if(note){await delay(250);await evaluate(`document.querySelector('button[popovertarget="'+${JSON.stringify(note)}+'"]')?.click()`);await delay(150);details.citationPopover=await evaluate(`(()=>{const n=document.getElementById(${JSON.stringify(note)}),r=n.getBoundingClientRect();return {opened:n.matches(':popover-open'),text:n.textContent.trim(),inViewport:r.top>=0&&r.bottom<=innerHeight};})()`);if(!details.citationPopover.opened||!details.citationPopover.inViewport)throw Error(name+' citation popover');await screenshot(root+'/'+name+'/browser-note-wide.png');await evaluate(`document.getElementById(${JSON.stringify(note)}).hidePopover()`);}
  const ref=await evaluate(`(()=>{const n=document.querySelector('main a.page-ref');if(!n)return null;n.scrollIntoView({block:'center'});n.click();return n.getAttribute('href').slice(1);})()`);
  if(ref){await delay(350);details.pageReference=await evaluate(`(()=>{const n=document.getElementById(${JSON.stringify(ref)}),r=n.getBoundingClientRect();return {hash:location.hash,targetExists:!!n,inViewport:r.top>=0&&r.top<innerHeight};})()`);if(!details.pageReference.targetExists||!details.pageReference.inViewport)throw Error(name+' page reference');}
  await navigate(name,390);await screenshot(root+'/'+name+'/browser-mobile.png',name==='night_expanded'?'Evening Prayer for the New Year':name==='documentary_hebrew'?'תְּפִלּוֹת.':'Prayers');details.mobileHorizontalOverflow=await evaluate('document.documentElement.scrollWidth>innerWidth+1');report.profiles[name]=details;
 }
 await navigate('expanded');
 const id=await evaluate("JSON.parse(document.getElementById('os-book').textContent).id");
 for(const german of [false,true,null])for(const gender of ['male','female',null])for(const shabbat of [false,true,null]){
  const settings={'opensiddur:rite':{german},'opensiddur:person':{gender},'opensiddur:holiday-aggregate':{shabbat}};
  await evaluate(`localStorage.setItem(${JSON.stringify('opensiddur:'+id+':settings')},${JSON.stringify(JSON.stringify(settings))})`);
  await rpc('Page.reload');await delay(400);
  const result=await evaluate(`(()=>{const walker=document.createTreeWalker(document.querySelector('main'),NodeFilter.SHOW_TEXT);let n,pieces=[];while(n=walker.nextNode()){let shown=true;for(let e=n.parentElement;e&&e.tagName!=='BODY';e=e.parentElement){const c=getComputedStyle(e);if(c.display==='none'||c.visibility==='hidden'){shown=false;break;}}if(shown)pieces.push(n.data);}const t=pieces.join(' ').replace(/\\s+/g,' ');return {text:t,hiddenLabels:[...document.querySelectorAll('.conditional-note')].filter(n=>n.getClientRects().length).map(n=>n.innerText)};})()`);
  const count=needle=>result.text.split(needle).length-1;
  const row={german,gender,shabbat,torahBlessings:count('who has chosen us from all peoples'),female:count('who made me according to His will'),barukhShem:count('Blessed be His glorious royal Name for ever and ever.')};
  if(row.torahBlessings!==(german===null?2:1)||row.female!==(gender==='male'?0:1)||row.barukhShem!==1)throw Error('Client matrix '+JSON.stringify(row));
  report.matrix.push(row);
 }
 await navigate('expanded',1280);await evaluate(`localStorage.setItem(${JSON.stringify('opensiddur:'+id+':settings')},${JSON.stringify(JSON.stringify({'opensiddur:rite':{german:true},'opensiddur:person':{gender:'female'},'opensiddur:holiday-aggregate':{shabbat:true}}))})`);await rpc('Page.reload');await delay(500);await screenshot(root+'/expanded/browser-known-shabbat-german-female.png','Morning Prayer');
 await fs.writeFile(root+'/browser_qa.json',JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({profiles:Object.keys(report.profiles),matrix:report.matrix.length,errors,overflow:Object.fromEntries(Object.entries(report.profiles).map(([k,v])=>[k,[v.horizontalOverflow,v.mobileHorizontalOverflow]]))}));
}finally{if(ws)ws.close();chrome.kill('SIGTERM');server.kill('SIGTERM');await delay(300);await fs.rm(cache,{recursive:true,force:true});}
