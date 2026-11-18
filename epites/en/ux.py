# v63: asztali használhatóság – összecsukható szűrők, a séta szövege az adatlap-panelben, teljes képernyő (mindkét nyelvre)
def ux(body,cur):
    T={"hu":{"f":"Szűrők és rétegek","a":"aktív","fs":"Teljes képernyő","ex":"Kilépés a teljes képernyőből","x":"Kilépés","wc":"Séta bezárása ✕"},
       "en":{"f":"Filters and layers","a":"active","fs":"Full screen","ex":"Exit full screen","x":"Exit","wc":"Close walk ✕"}}[cur]
    def rp1(a,b):
        nonlocal body
        assert body.count(a)==1,(a[:50],body.count(a));body=body.replace(a,b)
    i=body.index('<div class="search">');j=body.index('</div>',body.index('</ul>',i))+6
    body=body[:j]+'\n    <button class="fbtn" id="fbtn" aria-expanded="false"><span class="fbl">'+T["f"]+'</span><span class="fbn" id="fbn"></span> <span class="fba">▾</span></button>'+body[j:]
    rp1('<button id="z-all">','<button id="z-fs" aria-label="'+T["fs"]+'" title="'+T["fs"]+'">'+T["fs"]+'</button>\n          <button id="z-all">')
    rp1('select(st.id);drawWalk();}','select(st.id);walkPanel(k);drawWalk();}')
    rp1('if(!on){walk=null;drawWalk();','if(!on){walk=null;drawWalk();document.querySelectorAll(".walkpanel").forEach(x=>x.remove());if(cur&&nodes[cur])nodes[cur].g.classList.remove("sel");cur=null;intro();')
    rp1('let walkAuto=[];',r'''let walkAuto=[];
/* a séta megállója az adatlap-panel tetején jelenik meg, a térkép mellett (a gombfeliratok a séta-kártya gombjaiból jönnek, így nyelvfüggetlen) */
function walkPanel(k){if(!walk)return;const st=walk.s[k],n=walk.s.length,d=document.createElement("div");d.className="walkpanel";
  d.innerHTML=`<div class="wptop"><div class="wpname">${esc(walk.t)}</div><button class="wp-close">@@WC@@</button></div><div class="walknav"><button class="wp-prev"${k===0?" disabled":""}>${esc(document.getElementById("wprev").textContent)}</button><span>${k+1} / ${n}</span><button class="wp-next"${k===n-1?" disabled":""}>${esc(document.getElementById("wnext").textContent)}</button></div><h2>${k+1}. ${esc(st.h)}</h2><p class="wptext"></p>`;
  d.querySelector(".wptext").textContent=st.x;panel.insertBefore(d,panel.firstChild);panel.scrollTop=0;
  const r=document.querySelector(".mapbox").getBoundingClientRect();if(r.top<-40||r.top>innerHeight*0.5)document.querySelector(".main").scrollIntoView({block:"start"});}
panel.addEventListener("click",e=>{if(!walk||!e.target.closest)return;if(e.target.closest(".wp-close")){const b=document.querySelector(".walksel button[aria-pressed=true]");if(b)b.click();return;}if(e.target.closest(".wp-prev")&&wi>0)showStop(wi-1);else if(e.target.closest(".wp-next")&&wi<walk.s.length-1)showStop(wi+1);});'''.replace("@@WC@@",T["wc"]))
    js=r'''/* összecsukható szűrők: a keresés és az évcsúszka mindig látszik, a többi sor a gombbal nyitható */
(function(){const c=document.querySelector(".controls"),b=document.getElementById("fbtn"),nEl=document.getElementById("fbn"),DEF={"t-paus":"true","t-arch":"true","t-hypo":"true","t-det":"true"};
  const count=()=>{let n=0;const f=document.querySelector(".fnseg button[aria-pressed=true]");if(f&&f.dataset.fn!=="all")n++;if(document.getElementById("cb-period").getAttribute("aria-pressed")!=="true")n++;
    n+=document.querySelectorAll("#periodchips .chip[aria-pressed=false]").length;
    c.querySelectorAll(".chip[id^=t-]").forEach(x=>{if(["t-nolli","t-depth","t-route"].includes(x.id))return;if(x.getAttribute("aria-pressed")!==(DEF[x.id]||"false"))n++;});
    nEl.textContent=n?" · "+n+" @@A@@":"";};
  const set=o=>{c.classList.toggle("collapsed",!o);b.setAttribute("aria-expanded",String(o));b.querySelector(".fba").textContent=o?"▴":"▾";};
  const o=false;/* v125: oldalbetöltéskor mindig összezárva (korábban a böngésző megjegyezte a nyitott állapotot) */
  set(o);b.addEventListener("click",e=>{e.stopPropagation();set(c.classList.contains("collapsed"));});c.addEventListener("click",()=>setTimeout(count,30));document.addEventListener("click",()=>setTimeout(count,60));setTimeout(count,60);})();
/* teljes képernyő: a térkép és az adatlap együtt */
(function(){const b=document.getElementById("z-fs"),m=document.querySelector(".main");if(!m.requestFullscreen){b.hidden=true;return;}
  b.addEventListener("click",()=>{if(document.fullscreenElement)document.exitFullscreen();else m.requestFullscreen().catch(()=>{});});
  document.addEventListener("fullscreenchange",()=>{const f=!!document.fullscreenElement;b.setAttribute("aria-label",f?"@@EX@@":"@@FS@@");b.title=b.getAttribute("aria-label");b.textContent=f?"@@X@@":"@@FS@@";if(typeof syncPanel==="function")setTimeout(syncPanel,80);});})();
/* funkció szerinti szűrő */'''.replace('@@A@@',T["a"]).replace('@@X@@',T["x"]).replace('@@EX@@',T["ex"]).replace('@@FS@@',T["fs"])
    rp1('/* funkció szerinti szűrő */',js)
    # v64: telefon – kétujjas nagyítás, a nézet a térkép tényleges arányához igazodik
    rp1('function setVB(v){vb=v;','function setVB(v){const r0=svg.getBoundingClientRect();if(r0.width>50&&r0.height>50){const hh=v[2]*r0.height/r0.width;v=[v[0],v[1]+(v[3]-hh)/2,v[2],hh];}vb=v;')
    rp1('window.addEventListener("resize",viewChanged);','window.addEventListener("resize",()=>{setVB(vb.slice());});')
    rp1('svg.addEventListener("pointerdown",e=>{drag={x:e.clientX,y:e.clientY,vb:vb.slice(),moved:false};});',"""const tps=new Map();let pinch=null;
svg.addEventListener("pointerdown",e=>{tps.set(e.pointerId,[e.clientX,e.clientY]);
  if(tps.size===2){const [a,b]=[...tps.values()],r=svg.getBoundingClientRect(),mx=(a[0]+b[0])/2,my=(a[1]+b[1])/2;
    pinch={d:Math.hypot(a[0]-b[0],a[1]-b[1])||1,vb:vb.slice(),sx:vb[0]+(mx-r.left)/r.width*vb[2],sy:vb[1]+(my-r.top)/r.height*vb[3],moved:false};drag=null;return;}
  if(tps.size===1)drag={x:e.clientX,y:e.clientY,vb:vb.slice(),moved:false};});
/* kétujjas nagyítás: a két ujj közti pont a helyén marad */
window.addEventListener("pointermove",e=>{if(!tps.has(e.pointerId))return;tps.set(e.pointerId,[e.clientX,e.clientY]);if(!pinch||tps.size<2)return;
  const [a,b]=[...tps.values()],r=svg.getBoundingClientRect(),d=Math.hypot(a[0]-b[0],a[1]-b[1])||1,mx=(a[0]+b[0])/2,my=(a[1]+b[1])/2;
  const w=Math.max(40,Math.min(6600,pinch.vb[2]*pinch.d/d)),h=w*pinch.vb[3]/pinch.vb[2];pinch.moved=true;
  setVB([pinch.sx-(mx-r.left)/r.width*w,pinch.sy-(my-r.top)/r.height*h,w,h]);});
const tpEnd=e=>{tps.delete(e.pointerId);if(pinch&&tps.size<2){if(pinch.moved)svg.addEventListener("click",stopOnce,true);pinch=null;drag=null;}};
window.addEventListener("pointerup",tpEnd);window.addEventListener("pointercancel",tpEnd);""")
    rp1('/* megosztható link:','setTimeout(()=>setVB(vb.slice()),0);\n/* megosztható link:')
    return body
CSS='''/* v63: összecsukható szűrők, séta a panelben, teljes képernyő */
.controls.collapsed>.legend-row,.controls.collapsed>.chips{display:none!important}
.fbtn{font:500 13px var(--font-body);padding:7px 14px;border:1px solid var(--ink);border-radius:999px;background:var(--sheet);color:var(--ink);cursor:pointer;white-space:nowrap}
.fbtn[aria-expanded=true]{background:var(--ink);color:var(--sheet)}
.fbtn .fbn{font-weight:600}
.controls .search{width:auto;flex:1 1 320px}
#walkstop{display:none!important}
.walkpanel{border-left:3px solid #b23a2a;padding:2px 0 12px 12px;margin:0 0 16px;border-bottom:1px solid var(--line)}
.walkpanel .wpname{font:600 11px var(--font-body);letter-spacing:.06em;text-transform:uppercase;color:#b23a2a;margin-bottom:6px}
.walkpanel .wptop{display:flex;align-items:flex-start;justify-content:space-between;gap:8px}
.walkpanel .wp-close{flex:none;font:500 12px var(--font-body);padding:4px 10px;border:1px solid var(--line);border-radius:999px;background:var(--sheet);color:var(--ink);cursor:pointer;white-space:nowrap}
.walkpanel .wp-close:hover{border-color:#b23a2a;color:#b23a2a}
.walkpanel h2{margin:.5em 0 .4em;font-size:1.25rem}
.walkpanel .wptext{white-space:pre-line;line-height:1.55;margin:0}
.walkpanel .walknav span{font:500 13px var(--font-mono);color:var(--muted)}
.main:fullscreen{background:var(--paper);padding:12px;box-sizing:border-box;width:100vw;height:100vh;overflow:auto}
.main:fullscreen #map{height:calc(100vh - 120px);width:100%}
.main:fullscreen .side{max-height:calc(100vh - 24px)!important}
/* v64: telefon */
@media (max-width:700px){
  .wrap{padding:12px 12px 36px}
  header.top{grid-template-columns:minmax(0,1fr);gap:6px}
  .plate{display:none}
  h1{font-size:26px;line-height:1.12;text-wrap:pretty}
  .districts{margin-top:6px}
  #navsel{flex:1 1 auto;min-width:0;width:100%;max-width:340px;font-size:15px;padding:8px 28px 8px 12px}
  .controls{gap:8px 10px;padding:10px 0}
  .controls .search{flex:1 1 100%;max-width:none}
  .search input{font-size:16px}
  .fbtn{font-size:14px;padding:9px 14px}
  .seg{flex-wrap:wrap;border-radius:14px}
  .year{gap:6px 8px}
  .year input[type=range]{width:100%;flex:1 1 160px}
  .year button{padding:6px 8px}
  #map{aspect-ratio:1/1;max-height:62vh}
  .zoom{top:6px;right:6px}
  .zoom button{min-width:40px;min-height:36px;font-size:12px;padding:4px 8px}
  #z-fs,#z-altis{display:none}
  .year button[data-y]:not([data-y="all"]){display:none}
  .caption span:first-child{display:none}
  .caption{font-size:11px}
  aside.panel{padding:14px 14px}
  .walknav button{padding:8px 14px;font-size:15px}
  .chip{padding-top:7px;padding-bottom:7px}
  .langsw a{padding:7px 14px;font-size:13px}
}
</style>'''

# v65: minden szűrő törlése, megosztható nézet, betöltésjelző, billentyűzet
def ux2(body,cur):
    T={"hu":{"r":"Minden szűrő törlése","rs":"Alaphelyzet","ld":"Betöltés…","kb":"Billentyűzet: nyilak (mozgatás, ha a térkép fölött vagy), + és − (nagyítás), Esc (bezárás)."},
       "en":{"r":"Reset all filters","rs":"Reset view","ld":"Loading…","kb":"Keyboard: arrow keys (pan, with the pointer over the map), + and − (zoom), Esc (close)."}}[cur]
    def rp1(a,b):
        nonlocal body
        assert body.count(a)==1,(a[:60],body.count(a));body=body.replace(a,b)
    rp1('<span class="fba">▾</span></button>','<span class="fba">▾</span></button><button class="rbtn" id="rbtn" hidden>'+T["r"]+'</button>')
    rp1('<button id="z-all">','<button id="z-reset" title="'+T["rs"]+'">'+T["rs"]+'</button>\n          <button id="z-all">')
    rp1('<div class="tip" id="tip"></div>','<div class="tip" id="tip"></div>\n        <div class="loadind" id="loadind" hidden><span class="spin"></span>'+T["ld"]+'</div>')
    rp1('nEl.textContent=n?','document.getElementById("rbtn").hidden=!n;nEl.textContent=n?')
    rp1('try{if(location.hash!=="#"+id)location.hash=id;}catch(e){}','schedHash();')
    rp1('function viewChanged(){','function viewChanged(){schedHash();')
    rp1('function apply(){','function apply(){schedHash();')
    rp1('function drawWalk(){','function drawWalk(){schedHash();')
    rp1('intro();setColorBy(true);setYear("all");fromHash();viewChanged();','intro();setColorBy(true);setYear("all");fromHash();viewChanged();setTimeout(()=>{window.__hashReady=true;},600);')
    old_fh='function fromHash(){let h="";try{h=decodeURIComponent(location.hash.slice(1));}catch(e){}if(h&&nodes[h]&&h!==cur)goTo(h);}'
    new_fh=r'''/* a cím #-jele utáni rész a teljes nézetet őrzi: e = kiválasztott elem, v = látott terület, on/off = rétegek, fn = funkció, np = kikapcsolt korszakok, y = év, c = színezés, w = séta és megálló.
   A régi, csak elemazonosítót tartalmazó linkek továbbra is működnek. */
const LDEF={"t-paus":1,"t-arch":1,"t-hypo":1,"t-det":1},LAY=["t-paus","t-arch","t-hypo","t-det","t-sitar","t-fur","t-aq","t-rd","t-ch","t-relief","t-lanc","t-nolli","t-route","t-depth"];
function hashStr(){const p=[];if(cur&&nodes[cur])p.push("e="+cur);p.push("v="+vb.map(x=>Math.round(x)).join(","));
  const on=[],off=[];LAY.forEach(id=>{const b=document.getElementById(id);if(!b)return;const pr=b.getAttribute("aria-pressed")==="true";if(pr&&!LDEF[id])on.push(id.slice(2));if(!pr&&LDEF[id])off.push(id.slice(2));});
  if(on.length)p.push("on="+on.join("."));if(off.length)p.push("off="+off.join("."));if(state.fn!=="all")p.push("fn="+state.fn);
  const np=Object.keys(state.periods).filter(k=>!state.periods[k]);if(np.length)p.push("np="+np.join("."));if(state.year!=="all")p.push("y="+state.year);
  const c=document.getElementById("cb-today").getAttribute("aria-pressed")==="true"?"t":(state.byPeriod?"":"s");if(c)p.push("c="+c);
  if(walk)p.push("w="+walk.id+"."+(wi+1));return p.join("&");}
var hashT=null;function schedHash(){if(!window.__hashReady)return;clearTimeout(hashT);hashT=setTimeout(()=>{try{history.replaceState(null,"",location.pathname+location.search+"#"+hashStr());}catch(e){}},250);}
function fromHash(){let h="";try{h=decodeURIComponent(location.hash.slice(1));}catch(e){}if(!h)return;
  if(h.indexOf("=")<0){if(nodes[h]&&h!==cur)goTo(h);return;}
  const P={};h.split("&").forEach(kv=>{const i=kv.indexOf("=");if(i>0)P[kv.slice(0,i)]=kv.slice(i+1);});
  const was=window.__hashReady;window.__hashReady=false;const pressed=b=>b.getAttribute("aria-pressed")==="true";
  try{
  if(P.c==="s")document.getElementById("cb-source").click();else if(P.c==="t")document.getElementById("cb-today").click();else document.getElementById("cb-period").click();
  const fb=document.querySelector('.fnseg button[data-fn="'+(P.fn||"all")+'"]');if(fb&&!pressed(fb))fb.click();
  const np=(P.np||"").split(".").filter(Boolean);document.querySelectorAll("#periodchips [data-p]").forEach(b=>{if(pressed(b)!==!np.includes(b.dataset.p))b.click();});
  const on=(P.on||"").split(".").filter(Boolean),off=(P.off||"").split(".").filter(Boolean);
  LAY.forEach(id=>{const b=document.getElementById(id);if(!b)return;const k=id.slice(2),want=LDEF[id]?!off.includes(k):on.includes(k);if(pressed(b)!==want)b.click();});
  if(P.y&&isFinite(+P.y))setYear(+P.y);else if(state.year!=="all")setYear("all");
  if(P.w){const q=P.w.split("."),b=document.querySelector('.walksel button[data-w="'+q[0]+'"]');if(b){if(!(walk&&walk.id===q[0]))b.click();if(walk)showStop(Math.max(0,Math.min(walk.s.length-1,(+q[1]||1)-1)));}}
  else if(walk){const b=document.querySelector(".walksel button[aria-pressed=true]");if(b)b.click();}
  if(P.e&&nodes[P.e]&&P.e!==cur)select(P.e);
  if(P.v){const v=P.v.split(",").map(Number);if(v.length===4&&v.every(isFinite)&&v[2]>0&&v[3]>0)setVB(v);}
  }finally{window.__hashReady=was;}}'''
    rp1(old_fh,new_fh)
    js=r'''/* minden szűrő törlése: színezés, funkció, korszakok, rétegek és év vissza alapra (a séta és a kiválasztás megmarad) */
document.getElementById("rbtn").addEventListener("click",e=>{e.stopPropagation();const pr=b=>b.getAttribute("aria-pressed")==="true",DEF={"t-paus":1,"t-arch":1,"t-hypo":1,"t-det":1};
  const cp=document.getElementById("cb-period");if(!pr(cp)||pr(document.getElementById("cb-today")))cp.click();
  const fa=document.querySelector('.fnseg button[data-fn="all"]');if(!pr(fa))fa.click();
  document.querySelectorAll("#periodchips [data-p]").forEach(b=>{if(!pr(b))b.click();});
  document.querySelectorAll('.controls .chip[id^="t-"]').forEach(b=>{if(pr(b)!==!!DEF[b.id])b.click();});
  const ya=document.querySelector('.presets button[data-y="all"]');if(ya)ya.click();
  document.dispatchEvent(new Event("click"));});
/* v72: alaphelyzet a térkép gombjai között: séta bezárása, szűrők törlése, kiválasztás megszüntetése, kiinduló nézet */
document.getElementById("z-reset").addEventListener("click",()=>{if(walk){const b=document.querySelector(".walksel button[aria-pressed=true]");if(b)b.click();}
  document.querySelectorAll(".regsel button[aria-pressed=true],#aqflow[aria-pressed=true],#foodbtn[aria-pressed=true]").forEach(x=>x.click());
  if(typeof undockCard==="function")undockCard();
  document.getElementById("rbtn").click();if(cur&&nodes[cur])nodes[cur].g.classList.remove("sel");cur=null;intro();setVB(ROM.slice());schedHash();});
/* betöltésjelző: futó adatletöltések (ásatási csempék, domborzat) és a térképre kerülő képek (régi térképek) */
(function(){const ind=document.getElementById("loadind");let n=0,t=null;const upd=()=>{clearTimeout(t);if(n>0)t=setTimeout(()=>{ind.hidden=n<=0;},180);else ind.hidden=true;};
  const inc=()=>{n++;upd();},dec=()=>{n=Math.max(0,n-1);upd();};
  if(window.fetch){const f0=window.fetch.bind(window);window.fetch=(...a)=>{inc();return f0(...a).finally(dec);};}
  /* a fetch akkor tér vissza, amikor a válasz feje megjött; a törzs letöltését a json()/text() hívás várja ki, ezt is számoljuk */
  if(window.Response){["json","text","blob"].forEach(k=>{const o=Response.prototype[k];Response.prototype[k]=function(){inc();return o.apply(this,arguments).finally(dec);};});}
  new MutationObserver(ms=>ms.forEach(m=>m.addedNodes.forEach(nd=>{const ims=nd.nodeName==="image"?[nd]:(nd.querySelectorAll?[...nd.querySelectorAll("image")]:[]);
    ims.forEach(im=>{if(im.dataset.ld)return;im.dataset.ld="1";inc();let done=false;const fin=()=>{if(done)return;done=true;dec();};im.addEventListener("load",fin);im.addEventListener("error",fin);setTimeout(fin,20000);});}))).observe(svg,{childList:true,subtree:true});})();
/* billentyűzet: nyilak mozgatnak (ha az egér a térkép fölött van vagy a térképen van a fókusz), + és − nagyít, Esc bezárja az adatlapot és a sétát */
(function(){let over=false;svg.setAttribute("tabindex","0");svg.addEventListener("pointerenter",()=>{over=true;});svg.addEventListener("pointerleave",()=>{over=false;});
  const cap=document.querySelector(".caption span");if(cap)cap.textContent+=" @@KB@@";
  document.addEventListener("keydown",e=>{if(e.ctrlKey||e.metaKey||e.altKey)return;const t=e.target,tag=(t&&t.tagName)||"";if(/^(INPUT|SELECT|TEXTAREA)$/.test(tag)||(t&&t.isContentEditable))return;
    const k=e.key;
    if(k==="+"||k==="="){zoom(1/1.25);e.preventDefault();return;}
    if(k==="-"||k==="_"){zoom(1.25);e.preventDefault();return;}
    if(k==="Escape"){const qr=document.getElementById("qres");if(qr&&!qr.classList.contains("hidden")){qr.classList.add("hidden");return;}
      if(walk){const b=document.querySelector(".walksel button[aria-pressed=true]");if(b)b.click();}
      if(cur&&nodes[cur])nodes[cur].g.classList.remove("sel");cur=null;intro();schedHash();return;}
    const D={ArrowLeft:[-1,0],ArrowRight:[1,0],ArrowUp:[0,-1],ArrowDown:[0,1]}[k];
    if(D&&(over||document.activeElement===svg)){const s=e.shiftKey?0.35:0.12;setVB([vb[0]+D[0]*vb[2]*s,vb[1]+D[1]*vb[3]*s,vb[2],vb[3]]);e.preventDefault();}});})();
/* funkció szerinti szűrő */'''.replace("@@KB@@",T["kb"])
    rp1('/* funkció szerinti szűrő */',js)
    return body
CSS2='''/* v65: szűrők törlése, betöltésjelző */
.rbtn{font:500 13px var(--font-body);padding:7px 14px;border:1px solid var(--line);border-radius:999px;background:none;color:var(--accent);cursor:pointer;white-space:nowrap}
.rbtn:hover{border-color:var(--accent)}
.loadind{position:absolute;left:10px;top:10px;display:inline-flex;align-items:center;gap:8px;font:500 12px var(--font-body);background:var(--sheet);border:1px solid var(--line);border-radius:999px;padding:5px 12px 5px 9px;box-shadow:0 1px 4px rgba(0,0,0,.08);pointer-events:none}
.loadind[hidden]{display:none}
.loadind .spin{width:12px;height:12px;border:2px solid var(--line);border-top-color:var(--accent);border-radius:50%;animation:rspin .8s linear infinite}
@keyframes rspin{to{transform:rotate(360deg)}}
@media (prefers-reduced-motion: reduce){.loadind .spin{animation:none}}
#map:focus-visible{outline:2px solid var(--accent);outline-offset:-2px}
</style>'''
