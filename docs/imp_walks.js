/* Caesar hadjáratai – séták a birodalmi térképen (v152).
   Adat: imp_walks_hu.json / imp_walks_en.json (data/build_walks.py). A megállók közötti vonal a légiókalkulátor
   úthálózatán (Itiner-e, tengeren ORBIS) keresett legrövidebb út; ez közelítés, nem Caesar ismert útvonala. */
(function(){
const HU=(document.documentElement.lang||"hu").startsWith("hu");
const GRP=HU?{caesar:["⚔ Caesar hadjáratai – séták","Évenként egy séta Caesar saját beszámolói (A gall háború, A polgárháború) nyomán. Válassz egyet:"],hadj:["⚔ Hadjáratok – séták","Más hadvezérek és császárok hadjáratai kortárs leírások nyomán."],utak:["🧭 Ókori utazások – séták","Ókori utazások a résztvevők vagy kortársak leírása nyomán. Válassz egyet:"]}
 :{caesar:["⚔ Caesar’s campaigns – walks","One walk per year, following Caesar’s own accounts (Gallic War, Civil War). Choose one:"],hadj:["⚔ Campaigns – walks","Campaigns of other generals and emperors after contemporary accounts."],utak:["🧭 Ancient journeys – walks","Ancient journeys after the accounts of travellers or contemporaries. Choose one:"]};
const T=HU?{mp:"A szöveg szerint {n} római mérföld (kb. {km} km; 1 mérföld ≈ 1,48 km) {f} és e hely között; a térkép úthálózatán keresett út {r} km.",
  close:"Séta bezárása ✕",prev:"‹ Előző",next:"Következő ›",calc:"Menetidő a kalkulátorral",legsG:"A kalkulátor alapértékei szerinti teljes létszámú légiókkal ({n} légió) számol; a forrás nem adja meg a sereg pontos létszámát.",party:"Kis csoporttal számol ({m} fő, málhásállat nélkül); tengeren a hajó sebessége, a szél és az évszak számít (Vegetius és Casson alapján).",calcH:"Összevetés a forrással",loading:"Betöltés…",
  legs:"A kalkulátor alapértékei szerinti teljes létszámú légiókkal ({n} légió) számol; Caesar légiói valószínűleg kisebbek voltak.",men:"{m} gyalogossal számol (Caesar adata); a lovasok és málhás állatok száma a kalkulátor arányai szerint.",cav:"Csak lovassággal ({m} lovas) számol; a létszámot Caesar nem adja meg.",route:"A vonal a későbbi római úthálózaton keresett útvonal, nem Caesar ismert útja."}
 :{mp:"According to the text {n} Roman miles (about {km} km; 1 mile ≈ 1.48 km) between {f} and this place; the route found on the map’s road network is {r} km.",
  close:"Close walk ✕",prev:"‹ Previous",next:"Next ›",calc:"Travel time with the calculator",legsG:"Uses full-strength legions with the calculator’s default values ({n} legions); the source does not give the exact size of the army.",party:"Uses a small party ({m} people, no pack animals); at sea the ship’s speed, the wind and the season count (after Vegetius and Casson).",calcH:"Comparison with the source",loading:"Loading…",
  legs:"Uses full-strength legions with the calculator’s default values ({n} legions); Caesar’s legions were probably smaller.",men:"Uses {m} infantry (Caesar’s figure); cavalry and pack animals in the calculator’s proportions.",cav:"Uses cavalry only ({m} horsemen); Caesar does not give the number.",route:"The line is a route found on the later Roman road network, not Caesar’s known route."};
const esc=s=>String(s??"").replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const css=document.createElement("style");css.textContent=`
details.walks{margin:6px 0 10px}details.walks>summary{cursor:pointer;font-weight:600}
.walksel2{display:flex;flex-wrap:wrap;gap:6px;margin-top:6px}.walksel2 button{font:inherit;font-size:13px;padding:4px 10px;border:1px solid var(--line);border-radius:14px;background:var(--sheet);color:var(--ink);cursor:pointer}
.walksel2 button[aria-pressed=true]{background:#7a1020;border-color:#7a1020;color:#fff}
#map .wkl{fill:none;stroke:#7a1020;stroke-width:3px;vector-effect:non-scaling-stroke;stroke-linecap:round;stroke-linejoin:round;opacity:.85}
#map .wkl.sea{stroke-dasharray:6 5}#map .wkl.on{stroke-width:5px;opacity:1}
#map .wkm circle{fill:#7a1020;stroke:#fff;stroke-width:2px;vector-effect:non-scaling-stroke;cursor:pointer}#map .wkm.on circle{fill:#d4a017}
#map .wkm text{fill:#fff;font-weight:700;text-anchor:middle;dominant-baseline:central;pointer-events:none;font-family:system-ui,sans-serif}
.wkp .wknav{display:flex;align-items:center;gap:8px;margin:8px 0}.wkp .wknav button{font:inherit;padding:3px 10px;border:1px solid var(--line);border-radius:12px;background:var(--sheet);color:var(--ink);cursor:pointer}
.wkp .wknav button:disabled{opacity:.4;cursor:default}.wkp .wkd{color:var(--muted);font-size:13px;margin:2px 0 6px}.wkp .wkx{margin:4px 0 8px}
.wkp .wkcalc{margin:10px 0;padding:8px 10px;border:1px solid var(--line);border-radius:6px}.wkp .wkcalc button{font:inherit;padding:4px 12px;border-radius:14px;border:1px solid var(--ink);background:var(--ink);color:var(--paper);cursor:pointer}
.wkp figure.wkim{margin:8px 0 10px}.wkp figure.wkim img{display:block;max-width:100%;height:auto;min-height:60px;border-radius:4px;background:var(--paper)}.wkp figure.wkim figcaption{font-size:13px;margin-top:4px}.wkp figure.wkim .cr{display:block;font-size:11px;color:var(--muted);margin-top:2px}.wkp figure.wkim .kd{font-weight:600}.wkp details.wkin{margin:6px 0}.wkp details.wkin summary{cursor:pointer;color:var(--muted)}`;document.head.appendChild(css);
const ctr=document.querySelector(".controls");if(!ctr||!window.MV)return;
const goMap=()=>{const m=document.querySelector(".main");if(m){const r=m.getBoundingClientRect();if(r.top<-40||r.top>window.innerHeight*.5)m.scrollIntoView({behavior:"smooth",block:"start"});}};
const BOX={};let after=ctr;for(const gk of ["caesar","hadj","utak"]){const ex=document.getElementById("wk-"+gk);if(ex){BOX[gk]=ex;continue;}const b=document.createElement("details");b.className="walks";b.innerHTML=`<summary>${GRP[gk][0]}</summary><p class="hint">${GRP[gk][1]}</p><div class="walksel2"></div>`;after.insertAdjacentElement("afterend",b);after=b;BOX[gk]=b;}
const WIC={};const wfill=()=>panel.querySelectorAll("figure.wkim img[data-id]").forEach(im=>{const g=im.dataset.g;(WIC[g]=WIC[g]||fetch("imp_wimg_"+g+".json").then(r=>r.json())).then(d=>{if(d[im.dataset.id])im.src="data:image/webp;base64,"+d[im.dataset.id];}).catch(()=>{});});
const KD=HU?{coin:"Érem",insc:"Felirat",site:"Helyszín",obj:"Tárgy"}:{coin:"Coin",insc:"Inscription",site:"Site",obj:"Object"};
const wimg=m=>`<figure class="wkim"><img data-g="${m.g}" data-id="${m.id}" width="${m.w}" height="${m.h}" alt="${esc(m.c)}"><figcaption><span class="kd">${KD[m.k]||""}:</span> ${esc(m.c)}<span class="cr">${HU?"Kép":"Image"}: ${esc(m.a)} · ${m.lu?`<a href="${esc(m.lu)}" target="_blank" rel="noopener">${esc(m.l)}</a>`:esc(m.l)} · <a href="${esc(m.p)}" target="_blank" rel="noopener">Wikimedia Commons</a></span></figcaption></figure>`;
const allSel=()=>document.querySelectorAll(".walksel2 button");
let W=null,walk=null,wi=0,G=null,legsG=[];
const gW=el("g",{class:"gwk"});svg.insertBefore(gW,gSet);
function load(){return W||(W=fetch(HU?"imp_walks_hu.json":"imp_walks_en.json").then(r=>r.json()));} /* v305: a teljes sétaadat csak az első megnyitáskor töltődik le */
async function openW(id){panel.innerHTML=`<p class="hint">${T.loading}</p>`;const d=await load();const w=d.find(x=>x.id===id);if(w)start(w);}
fetch(HU?"imp_walks_idx_hu.json":"imp_walks_idx_en.json").then(r=>r.json()).then(d=>{for(const gk in BOX)if(!d.some(w=>(w.g||"caesar")===gk))BOX[gk].hidden=true;d.forEach(w=>{const sel=BOX[w.g||"caesar"].querySelector(".walksel2");const b=document.createElement("button");b.type="button";b.textContent=w.y;b.title=w.t;b.dataset.w=w.id;b.setAttribute("aria-pressed","false");
  b.onclick=()=>{if(walk&&walk.id===w.id)stop();else{openW(w.id);goMap();}};sel.appendChild(b);});});
function stop(){walk=null;gW.innerHTML="";legsG=[];allSel().forEach(x=>x.setAttribute("aria-pressed","false"));if(typeof panel0!=="undefined")panel.innerHTML=panel0;}
async function start(w){walk=w;wi=0;allSel().forEach(x=>x.setAttribute("aria-pressed",String(x.dataset.w===w.id)));
  panel.innerHTML=`<p class="hint">${T.loading}</p>`;await MV.ready();if(walk!==w)return;draw();show(0);}
function draw(){gW.innerHTML="";legsG=[null];const s=walk.s;
  for(let i=1;i<s.length;i++){const o=s[i].rf||[s[i-1].x,s[i-1].y];const P=[o,...(s[i].via||[]),[s[i].x,s[i].y]];let g=[];if(s[i].ln)g=[P];else for(let k=1;k<P.length;k++)g=g.concat(MV.route(P[k-1][0],P[k-1][1],P[k][0],P[k][1],s[i].sea));legsG.push(g);
    for(const part of g){el("path",{class:"wkl"+(s[i].sea?" sea":""),"data-i":i,d:"M"+part.map(q=>q[0].toFixed(2)+" "+(-q[1]).toFixed(2)).join("L")},gW);}}
  const r=Math.max(6,Math.min(14,(vb[2]||1000)/150));s.forEach((st,i)=>{const g=el("g",{class:"wkm","data-i":i},gW);el("circle",{cx:st.x,cy:-st.y,r},g);const t=el("text",{x:st.x,y:-st.y,"font-size":r*1.1},g);t.textContent=i+1;
    const ti=el("title",{},g);ti.textContent=`${i+1}. ${st.n}`;g.addEventListener("click",ev=>{ev.stopPropagation();show(i);});});}
function resize(){const r=Math.max(.8,(vb[2]||1000)/55);gW.querySelectorAll(".wkm").forEach(g=>{const c=g.querySelector("circle"),t=g.querySelector("text");c.setAttribute("r",r);t.setAttribute("font-size",r*1.15);});}
function fit(i){const s=walk.s,pts=[[s[i].x,s[i].y]];if(i>0){pts.push(s[i].rf||[s[i-1].x,s[i-1].y]);for(const part of legsG[i]||[])for(const q of part)pts.push(q);}
  let x0=Math.min(...pts.map(q=>q[0])),x1=Math.max(...pts.map(q=>q[0])),y0=Math.min(...pts.map(q=>q[1])),y1=Math.max(...pts.map(q=>q[1]));
  const rc=svg.getBoundingClientRect(),asp=(rc.height||1)/(rc.width||1);let w=Math.max(160,(x1-x0)*1.35),h=Math.max(160,(y1-y0)*1.35);if(h/w>asp)w=h/asp;else h=w*asp;
  setVBnow([(x0+x1)/2-w/2,-(y0+y1)/2-h/2,w,h]);setTimeout(resize,60);}
function show(i){wi=i;const st=walk.s[i],n=walk.s.length;
  gW.querySelectorAll(".wkm").forEach(g=>g.classList.toggle("on",+g.dataset.i===i));gW.querySelectorAll(".wkl").forEach(p=>p.classList.toggle("on",+p.dataset.i===i));
  const P=t=>t.split(/\n\n+/).map(x=>`<p>${esc(x)}</p>`).join("");
  let h=`<div class="wkp"><div class="wknav"><b style="flex:1">${esc(walk.t)}</b><button class="wk-x" type="button">${T.close}</button></div>`;
  if(i===0)h+=`<details class="wkin" open><summary>${HU?"Bevezető":"Introduction"}</summary>${P(walk.intro)}${(walk.g||"caesar")==="caesar"?`<p class="hint">${T.route}</p>`:""}</details>`;
  h+=`<div class="wknav"><button class="wk-p" type="button"${i===0?" disabled":""}>${T.prev}</button><span>${i+1} / ${n}</span><button class="wk-n" type="button"${i===n-1?" disabled":""}>${T.next}</button></div>`;
  h+=`<h2>${i+1}. ${esc(st.h)}</h2><div class="wkd">${esc(st.d)} · ${esc(st.n)}</div>${st.img?wimg(st.img):""}<div class="wkx">${P(st.t)}</div>`;
  if(st.mp){let r=0;for(const part of MV.route(st.mp.f[0],st.mp.f[1],st.x,st.y,!!st.mp.s))for(let k=1;k<part.length;k++)r+=Math.hypot(part[k][0]-part[k-1][0],part[k][1]-part[k-1][1]);const loc=HU?"hu-HU":"en-GB";h+=`<p class="hint">${T.mp.replace("{n}",st.mp.n.toLocaleString(loc)).replace("{km}",Math.round(st.mp.n*1.48).toLocaleString(loc)).replace("{f}",esc(st.mp.fn)).replace("{r}",Math.round(r).toLocaleString(loc))}</p>`;}
  if(st.calc)h+=`<div class="wkcalc"><b>${T.calcH}</b><p>${esc(st.calc.src)}</p><button class="wk-c" type="button">${T.calc}</button><p class="hint">${st.calc.party?T.party.replace("{m}",st.calc.inf):st.calc.inf===0?T.cav.replace("{m}",(st.calc.cav||0).toLocaleString(HU?"hu-HU":"en-GB")):st.calc.inf?T.men.replace("{m}",st.calc.inf.toLocaleString(HU?"hu-HU":"en-GB")):((walk.g||"caesar")==="caesar"?T.legs:T.legsG).replace("{n}",st.calc.leg)}</p></div>`;
  h+=`<div class="wknav"><button class="wk-p" type="button"${i===0?" disabled":""}>${T.prev}</button><span>${i+1} / ${n}</span><button class="wk-n" type="button"${i===n-1?" disabled":""}>${T.next}</button></div></div>`;
  panel.innerHTML=h;panel.scrollTop=0;wfill();
  panel.querySelectorAll(".wk-p").forEach(b=>b.onclick=()=>show(wi-1));panel.querySelectorAll(".wk-n").forEach(b=>b.onclick=()=>show(wi+1));
  panel.querySelector(".wk-x").onclick=stop;const c=panel.querySelector(".wk-c");if(c)c.onclick=()=>MV.calc(st.calc);
  fit(i);const mb=document.querySelector(".mapbox");if(mb){const r=mb.getBoundingClientRect();if(r.top<-40||r.top>innerHeight*.5)mb.scrollIntoView({block:"start"});}}
})();
