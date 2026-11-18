/* Kimutatások: kártyák + térképrétegek (v166). Adat: imp_stats.json, szöveg: window.STX */
(function(){
const X=window.STX;if(!X)return;const HU=X.lang==="hu";
const loc=HU?"hu-HU":"en-GB",fmt=n=>Math.round(n).toLocaleString(loc);
const esc=s=>String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const css=document.createElement("style");css.textContent=`
:root{--stc:#1f5fa8;--stc2:#9db8d6}@media (prefers-color-scheme: dark){:root{--stc:#7fb0e8;--stc2:#3d5876}}
#map .gst circle{r:calc(var(--v) * var(--rk,1) * 1px);fill:var(--stc);fill-opacity:.55;stroke:var(--sheet);stroke-width:calc(var(--rk,1) * .8px);cursor:pointer}
#map .gst circle.c0{fill:#c6dbef;fill-opacity:.95}#map .gst circle.c1{fill:#9ecae1;fill-opacity:.95}#map .gst circle.c2{fill:#6baed6;fill-opacity:.95}#map .gst circle.c3{fill:#3182bd;fill-opacity:.95}#map .gst circle.c4{fill:#08519c;fill-opacity:.95}
.stp .stleg i.c0{background:#c6dbef;opacity:1}.stp .stleg i.c1{background:#9ecae1;opacity:1}.stp .stleg i.c2{background:#6baed6;opacity:1}.stp .stleg i.c3{background:#3182bd;opacity:1}.stp .stleg i.c4{background:#08519c;opacity:1}
#map .gst circle.u{fill:none;stroke:var(--stc);stroke-opacity:.7;stroke-width:calc(var(--rk,1) * 1px)}
#map .gst circle.on{fill-opacity:.95;stroke:var(--ink);stroke-width:calc(var(--rk,1) * 1.6px)}
#map .gst text{font:600 calc(var(--rk,1) * 11px) var(--font-body,sans-serif);fill:var(--ink);stroke:var(--sheet);stroke-width:calc(var(--rk,1) * 3px);paint-order:stroke;text-anchor:middle;pointer-events:none}
.stcard .stch{width:100%;max-width:760px;height:auto;display:block;margin:8px 0}
.stcard .stch .b{fill:var(--stc2)}.stcard .stch .b.on{fill:var(--stc)}.stcard .stch .ax{stroke:var(--line);stroke-width:1}
.stcard .stch text{font-size:11px;fill:var(--muted)}.stcard .stch text.v{fill:var(--ink)}
.stcard .stsrc{font-size:.82rem;color:var(--muted)}.stcard .sttop{columns:2;font-size:.9rem;padding-left:18px}@media(max-width:600px){.stcard .sttop{columns:1}}
.stp .stv{display:flex;flex-wrap:wrap;gap:6px;margin:8px 0}.stp .stv button{font:inherit;font-size:.85rem;padding:3px 10px;border-radius:14px;border:1px solid var(--line);background:var(--sheet);color:var(--ink);cursor:pointer}
.stp .stv button[aria-pressed=true]{background:var(--stc);border-color:var(--stc);color:#fff}
.stp .stleg{display:flex;align-items:flex-end;gap:14px;margin:8px 0;flex-wrap:wrap}.stp .stleg span{display:flex;flex-direction:column;align-items:center;font-size:.8rem;color:var(--muted)}
.stp .stleg i{display:block;border-radius:50%;background:var(--stc);opacity:.6;margin-bottom:3px}.stp .stleg i.u{background:none;border:1.5px solid var(--stc)}
.stp #stinfo{min-height:1.4em;margin:8px 0;padding:6px 8px;border-left:3px solid var(--stc);background:var(--paper)}
svg.ston .gpt,svg.ston .grome{opacity:.18}svg.ston .gr,svg.ston .grd,svg.ston .glim{opacity:.4}.stp .wknav{flex-wrap:wrap;gap:6px 10px;align-items:flex-start}.stcard .stbtn{font:inherit;padding:5px 14px;border-radius:16px;border:1px solid var(--stc);background:var(--stc);color:#fff;cursor:pointer}
:root{--aw:#b8336a;--ao:#b07d00;--ag:#2a78d6;--ax:#8a8a85}@media (prefers-color-scheme: dark){:root{--aw:#d55181;--ao:#c98500;--ag:#3987e5;--ax:#8b918f}}
#map .gst circle.a0{fill:var(--aw);fill-opacity:.8}#map .gst circle.a1{fill:var(--ao);fill-opacity:.8}#map .gst circle.a2{fill:var(--ag);fill-opacity:.8}#map .gst circle.a3{fill:var(--ax);fill-opacity:.8}
.stp .stleg i.a0,.stk i.a0{background:var(--aw);opacity:1}.stp .stleg i.a1,.stk i.a1{background:var(--ao);opacity:1}.stp .stleg i.a2,.stk i.a2{background:var(--ag);opacity:1}.stp .stleg i.a3,.stk i.a3{background:var(--ax);opacity:1}.stp .stleg i.ax{background:var(--muted);opacity:.5}
.stcard .stch .s0{fill:var(--aw)}.stcard .stch .s1{fill:var(--ao)}.stcard .stch .s2{fill:var(--ag)}.stcard .stch .s3{fill:var(--ax)}.stcard .stch text.sv{fill:#fff;font-weight:600}
.stk{display:flex;flex-wrap:wrap;gap:4px 14px;font-size:.82rem;color:var(--muted);margin:6px 0 0}.stk span{display:flex;align-items:center;gap:5px}.stk i{display:inline-block;width:11px;height:11px;border-radius:3px}
:root{--tm:#d4561f;--ts:#2a78d6;--tv:#138a60}@media (prefers-color-scheme: dark){:root{--tm:#d95926;--ts:#3987e5;--tv:#199e70}}
#map .gst circle.t0{fill:var(--tm);fill-opacity:.8}#map .gst circle.t1{fill:var(--ts);fill-opacity:.8}#map .gst circle.t2{fill:var(--tv);fill-opacity:.8}
.stp .stleg i.t0{background:var(--tm);opacity:1}.stp .stleg i.t1{background:var(--ts);opacity:1}.stp .stleg i.t2{background:var(--tv);opacity:1}
.stcard .stch .hc{fill:var(--stc)}.stcard .stch text.hv{font-size:10.5px;fill:var(--ink)}.stcard .stch text.hv.w{fill:#fff;font-weight:600}.stinfo2{font-size:.9em}.stcard .stch text.bvl{font-size:10px}
.stcard .stch .ln{fill:none;stroke:var(--stc);stroke-width:2}.stcard .stch .la{fill:none;stroke:var(--stc2);stroke-width:.6;opacity:.8}.stcard .stch .z{stroke:var(--line);stroke-dasharray:3 3}.stcard .stch .ev{stroke:var(--muted);stroke-width:1;stroke-dasharray:2 3}
.stkpi{display:flex;flex-wrap:wrap;gap:8px;margin:.5em 0 .9em}.stkpi div{border:1px solid var(--line);border-radius:8px;padding:7px 13px;background:var(--paper);font-size:.82rem;color:var(--muted);min-width:110px}.stkpi b{display:block;font-size:1.3rem;font-weight:600;color:var(--ink);line-height:1.25}
.stcard .stch .p0{fill:var(--stc2)}.stcard .stch .p1{fill:var(--stc)}.stk i.p0{background:var(--stc2)}.stk i.p1{background:var(--stc)}.stcard .stch .mkl{stroke:var(--muted);stroke-width:1}.stcard .stch text.mkt{font-size:10.5px;font-weight:600}
.stcard .stch rect,.stcard .stch circle{cursor:default}.stcard .stch rect:hover{filter:brightness(.88)}.stcard .stchw2{margin-top:6px}
.sttip{position:absolute;z-index:50;background:var(--ink);color:var(--sheet);font-size:.8rem;padding:4px 9px;border-radius:6px;pointer-events:none;max-width:260px;box-shadow:0 2px 8px rgba(0,0,0,.25)}
.stcard .stch .dl{stroke:var(--stc2);stroke-width:3;stroke-linecap:round}.stcard .stch .dd{fill:var(--stc)}.stcard .stch .gl{stroke:var(--line);stroke-width:1;opacity:.6}
.stcard .stch .q0{fill:#9ecae1}.stcard .stch .q1{fill:#2171b5}.stk i.q0{background:#9ecae1}.stk i.q1{background:#2171b5}.stcard .stch text.sv.q{fill:#08306b}
:root{--b0:#c2417a;--b1:#d4561f;--b2:#2a78d6;--b3:#6250d6;--b4:#b07d00;--b5:#138a60}@media (prefers-color-scheme: dark){:root{--b0:#d55181;--b1:#d95926;--b2:#3987e5;--b3:#9085e9;--b4:#c98500;--b5:#199e70}}
#map .gst circle.b0{fill:var(--b0);fill-opacity:.85}#map .gst circle.b1{fill:var(--b1);fill-opacity:.85}#map .gst circle.b2{fill:var(--b2);fill-opacity:.85}#map .gst circle.b3{fill:var(--b3);fill-opacity:.85}#map .gst circle.b4{fill:var(--b4);fill-opacity:.85}#map .gst circle.b5{fill:var(--b5);fill-opacity:.7}
.stp .stleg i.b0,.stk i.b0{background:var(--b0);opacity:1}.stp .stleg i.b1,.stk i.b1{background:var(--b1);opacity:1}.stp .stleg i.b2,.stk i.b2{background:var(--b2);opacity:1}.stp .stleg i.b3,.stk i.b3{background:var(--b3);opacity:1}.stp .stleg i.b4,.stk i.b4{background:var(--b4);opacity:1}.stp .stleg i.b5,.stk i.b5{background:var(--b5);opacity:1}
.stcard .stch .b0{fill:var(--b0)}.stcard .stch .b1{fill:var(--b1)}.stcard .stch .b2{fill:var(--b2)}.stcard .stch .b3{fill:var(--b3)}.stcard .stch .b4{fill:var(--b4)}.stcard .stch .b5{fill:var(--b5)}`;
document.head.appendChild(css);
const gS=el("g",{class:"gst"},null);svg.insertBefore(gS,svg.querySelector(".glbl")||null);
let DATA=null,cur=null,view=null;
const KEYS={cities:["cities"],leg:["leg23","leg220"],orbis:["orbis"],wreck:["wrecks"],mines:["mines"],clim:["clim"],epi:["epi"],pap:["pap"],hoard:["hoards"],insc:["insc"],nic:["nic"],ports:["ports"],amph:["amph"],raad:["raad"],son:["sonata"],iso:["iso"],quar:["quarries"],rrs:["rrs"]};
const BUN=new Set(["leg23", "leg220", "nic", "sonata", "epi", "pap", "raad", "iso", "amph", "orbis", "insc", "wrecks", "clim2", "clim"]);let BP=null;const getB=()=>BP||(BP=fetch("imp_st/b.json").then(r=>r.json()));
const getK=k=>BUN.has(k)?getB().then(b=>b[k]):fetch("imp_st/"+k+".json").then(r=>r.json());
const load=id=>{DATA=DATA||{};return Promise.all((KEYS[id]||[]).filter(k=>!(k in DATA)).map(k=>getK(k).then(d=>{DATA[k]=d;})));};
const rk=()=>gS.style.setProperty("--rk",(1/(pxk||1)).toFixed(4));
window.onVBc=rk;
/* kis oszlop/sáv diagram */
function bars(rows,opt){ // rows:[label,value,key?]
  const W=760,lh=opt.h?22:0,n=rows.length,max=Math.max(...rows.map(r=>r[1]))||1;
  if(opt.h){const H=n*lh+6,lw=opt.lw||170;let s=`<svg class="stch" viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(opt.t)}">`;
    rows.forEach((r,i)=>{const w=(W-lw-70)*r[1]/max,y=i*lh+3;s+=`<text x="${lw-6}" y="${y+14}" text-anchor="end">${esc(r[0])}</text><rect class="b${r[2]&&r[2]===opt.on?" on":""}" x="${lw}" y="${y+2}" width="${Math.max(1,w).toFixed(1)}" height="${lh-6}" rx="3"><title>${esc(r[0])}: ${fmt(r[1])}</title></rect><text class="v" x="${lw+w+5}" y="${y+14}">${fmt(r[1])}</text>`;});
    return s+"</svg>";}
  const mk=opt.marks||[],b=24,tp=mk.length?34:18,H=176+(mk.length?16:0),fv=v=>opt.int||Number.isInteger(v)||v>=100?fmt(v):v.toLocaleString(loc,{maximumFractionDigits:1}),
    stp=(()=>{const raw=max/5,m=Math.pow(10,Math.floor(Math.log10(raw||1)));return [1,2,2.5,5,10].map(k=>k*m).find(k=>k>=raw)||10*m;})(),tl=Array.from({length:Math.floor(max/stp)},(_,i)=>(i+1)*stp),
    l=Math.max(30,...tl.map(t=>fv(t).length*6+10)),cw=(W-l-8)/n,showV=cw>=24&&rows.every(r=>fv(r[1]).length*5.6<=cw+2),ph=H-b-tp,
    era=t=>{const y=+String(t).replace("−","-");if(t===""||isNaN(y))return t;return y<0?(HU?"Kr. e. "+(-y):(-y)+" BC"):y===0?(HU?"Kr. u. 1":"AD 1"):String(y);};
  let s=`<svg class="stch" viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(opt.t)}">`;
  tl.forEach(t=>{const y=(H-b-ph*t/max).toFixed(1);s+=`<line class="gl" x1="${l}" x2="${W-8}" y1="${y}" y2="${y}"/><text x="${l-4}" y="${(+y+4).toFixed(1)}" text-anchor="end">${fv(t)}</text>`;});
  s+=`<text x="${l-4}" y="${H-b+4}" text-anchor="end">0</text><line class="ax" x1="${l}" x2="${W-8}" y1="${H-b}" y2="${H-b}"/>`;
  rows.forEach((r,i)=>{const h=ph*r[1]/max,x=l+i*cw;const on=opt.on&&r[2]&&(Array.isArray(opt.on)?opt.on.includes(r[2]):r[2]===opt.on);
    s+=`<rect class="b${on?" on":""}" x="${(x+1).toFixed(1)}" y="${(H-b-h).toFixed(1)}" width="${Math.max(1,cw-2).toFixed(1)}" height="${Math.max(.5,h).toFixed(1)}" rx="2"><title>${esc(r[0])}: ${fv(r[1])}</title></rect>`;
    if(r[3])s+=`<line class="ax" x1="${x.toFixed(1)}" x2="${x.toFixed(1)}" y1="${H-b}" y2="${H-b+4}"/><text x="${(x+2).toFixed(1)}" y="${H-b+15}">${esc(era(r[3]))}</text>`;
    if(showV&&r[1])s+=`<text class="v bvl" x="${(x+cw/2).toFixed(1)}" y="${(H-b-h-3).toFixed(1)}" text-anchor="middle">${fv(r[1])}</text>`;});
  mk.forEach(m=>{const r=rows[m[0]];if(!r)return;const x=l+m[0]*cw+cw/2,y=H-b-ph*r[1]/max-(showV?14:4),right=x>W*.7;s+=`<line class="mkl" x1="${x.toFixed(1)}" x2="${x.toFixed(1)}" y1="${y.toFixed(1)}" y2="${(y-9).toFixed(1)}"/><text class="v mkt" x="${(x+(right?4:-4)).toFixed(1)}" y="${(y-12).toFixed(1)}" text-anchor="${right?"end":"start"}">${esc(m[1])}</text>`;});
  if(opt.maxl)s+=`<text class="v" x="${W-8}" y="12" text-anchor="end">${esc(opt.maxl)}</text>`;
  return s+"</svg>";}
/* páros vízszintes sávok: rows:[címke,a,b], keys:[ka,kb] */
function pair(ch,t){const W=760,lw=ch.lw||190,lh=34,n=ch.rows.length,H=n*lh+4,max=Math.max(...ch.rows.flatMap(r=>[r[1],r[2]]))||1,fv=v=>v.toLocaleString(loc,{maximumFractionDigits:1});
  let s=`<div class="stk"><span><i class="p0"></i>${esc(ch.keys[0])}</span><span><i class="p1"></i>${esc(ch.keys[1])}</span></div><svg class="stch" viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(t)}">`;
  ch.rows.forEach((r,i)=>{const y=i*lh+3;s+=`<text x="${lw-6}" y="${y+18}" text-anchor="end">${esc(r[0])}</text>`;
    [1,2].forEach(k=>{const w=(W-lw-70)*r[k]/max,yy=y+(k-1)*13+2;s+=`<rect class="p${k-1}" x="${lw}" y="${yy}" width="${Math.max(r[k]?1.5:0,w).toFixed(1)}" height="11" rx="2.5"><title>${esc(r[0])} · ${esc(ch.keys[k-1])}: ${fv(r[k])}</title></rect><text class="v bvl" x="${(lw+w+5).toFixed(1)}" y="${yy+9.5}">${fv(r[k])}</text>`;});});
  return s+"</svg>";}
/* 100%-os halmozott sávok: rows:[címke,[értékek]], keys:[nevek] */
function stack(ch,t){const W=760,lh=26,lw=ch.lw||190,n=ch.rows.length,H=n*lh+4,pc=v=>v.toLocaleString(loc,{maximumFractionDigits:0})+" %";
  let s=`<div class="stk">${ch.keys.map((k,i)=>`<span><i class="${ch.cls?ch.cls[i]:ch.sc?ch.sc+i:"a"+i}"></i>${esc(k)}</span>`).join("")}</div><svg class="stch" viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(t)}">`;
  const mx=Math.max(...ch.rows.map(r=>r[1].reduce((a,b)=>a+b,0)))||1,aw=ch.abs?W-lw-70:W-lw-4;
  ch.rows.forEach((r,j)=>{const y=j*lh+2,tt=r[1].reduce((a,b)=>a+b,0),tot=tt||1,sc=ch.abs?aw*tt/mx:aw;let x=lw;s+=`<text x="${lw-6}" y="${y+16}" text-anchor="end">${esc(r[0])}</text>`;
    r[1].forEach((v,i)=>{if(!v)return;const w=sc*v/tot,p=100*v/tot;s+=`<rect class="${ch.cls?ch.cls[i]:(ch.sc||"s")+i}" x="${(x+1).toFixed(1)}" y="${y+3}" width="${Math.max(.5,w-2).toFixed(1)}" height="${lh-8}" rx="3"><title>${esc(r[0])} · ${esc(ch.keys[i])}: ${pc(p)}</title></rect>`;
      if(w>40)s+=`<text class="sv${ch.sc==="q"&&i===0?" q":""}" x="${(x+w/2).toFixed(1)}" y="${y+16}" text-anchor="middle">${pc(p)}</text>`;x+=w;});if(ch.abs)s+=`<text class="v" x="${(x+5).toFixed(1)}" y="${y+16}">${fmt(tt)}</text>`;});
  return s+"</svg>";}
/* hőtérkép: rows:[címke,[értékek]], cols:[oszlopcímkék] */
function heat(ch,t){const W=760,lw=ch.lw||170,lh=26,n=ch.rows.length,m=ch.cols.length,cw=(W-lw-4)/m,H=n*lh+22,mx=Math.max(...ch.rows.flatMap(r=>r[1]))||1;
  let s=`<svg class="stch" viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(t)}">`;
  ch.rows.forEach((r,j)=>{const y=j*lh;s+=`<text x="${lw-6}" y="${y+17}" text-anchor="end">${esc(r[0])}</text>`;
    r[1].forEach((v,i)=>{const x=lw+i*cw,o=v?.1+.85*v/mx:0;s+=`<rect class="hc" x="${(x+1).toFixed(1)}" y="${y+2}" width="${(cw-2).toFixed(1)}" height="${lh-4}" rx="3" fill-opacity="${o.toFixed(2)}"><title>${esc(r[0])} · ${esc(ch.cols[i])}: ${v}</title></rect>`;
      if(v)s+=`<text class="hv${o>.55?" w":""}" x="${(x+cw/2).toFixed(1)}" y="${y+17}" text-anchor="middle">${v}</text>`;});});
  ch.cols.forEach((c,i)=>{if(ch.ct&&!ch.ct[i])return;s+=`<text x="${(lw+i*cw+cw/2).toFixed(1)}" y="${n*lh+15}" text-anchor="middle">${esc(c)}</text>`;});
  return s+"</svg>";}
/* idősor: d={y0,y1,t,ts,p,ps}, ch.panels=[{k,ks,lo,hi,t,u,ticks}], ch.ev=[[év,címke]] */
function line(d,ch,t){const W=760,l=46,r=26,ph=150,gap=26,np=ch.panels.length,H=np*(ph+gap)+20,X=y=>l+(W-l-r)*(y-d.y0)/(d.y1-d.y0);
  let s=`<svg class="stch" viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(t)}">`;
  ch.panels.forEach((P,k)=>{const top=k*(ph+gap)+14,Y=v=>top+ph*(P.hi-v)/(P.hi-P.lo),path=a=>{let o="",pen=0;a.forEach((v,i)=>{if(v==null){pen=0;return;}o+=(pen?"L":"M")+X(d.y0+i).toFixed(1)+","+Y(Math.max(P.lo,Math.min(P.hi,v))).toFixed(1);pen=1;});return o;};
    s+=`<text x="${l}" y="${top-4}" class="v">${esc(P.t)}</text>`;
    (P.ticks||[]).forEach(v=>{s+=`<line class="gl" x1="${l}" x2="${W-r}" y1="${Y(v).toFixed(1)}" y2="${Y(v).toFixed(1)}"/><text x="${l-4}" y="${(Y(v)+4).toFixed(1)}" text-anchor="end">${v}</text>`;});
    if(P.zero!=null)s+=`<line class="z" x1="${l}" x2="${W-r}" y1="${Y(P.zero).toFixed(1)}" y2="${Y(P.zero).toFixed(1)}"/>`;
    (ch.ev||[]).forEach((e,i)=>{s+=`<line class="ev" x1="${X(e[0]).toFixed(1)}" x2="${X(e[0]).toFixed(1)}" y1="${top}" y2="${top+ph}"/>`;if(k===0)s+=`<text x="${(X(e[0])+3).toFixed(1)}" y="${top+10+(i%2)*13}">${esc(e[1])}</text>`;});
    s+=`<path class="la" d="${path(d[P.k])}"/><path class="ln" d="${path(d[P.ks])}"/>`;});
  for(let y=Math.ceil(d.y0/100)*100;y<=d.y1;y+=100){const x=X(y);s+=`<line class="gl" x1="${x.toFixed(1)}" x2="${x.toFixed(1)}" y1="${H-22}" y2="${H-17}"/>`;if(y%200===0)s+=`<text x="${x.toFixed(1)}" y="${H-4}" text-anchor="middle">${y<0?(HU?"Kr. e. "+(-y):(-y)+" BC"):y===0?"0":(HU?"Kr. u. "+y:"AD "+y)}</text>`;}
  return s+"</svg>";}
/* pontdiagram: ch.cols=[{t,lo,hi,ticks}], ch.rows=[[címke,[[átlag,szórás],…],n]] */
function dots(ch,t){const W=760,lw=ch.lw||200,nc=ch.cols.length,cw=(W-lw-10)/nc,lh=24,n=ch.rows.length,H=n*lh+40;
  let s=`<svg class="stch" viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(t)}">`;
  ch.cols.forEach((C,j)=>{const x0=lw+j*cw+10,x1=lw+(j+1)*cw-10,X=v=>x0+(x1-x0)*(v-C.lo)/(C.hi-C.lo);s+=`<text x="${((x0+x1)/2).toFixed(1)}" y="12" text-anchor="middle" class="v">${esc(C.t)}</text>`;
    C.ticks.forEach(v=>{s+=`<line class="gl" x1="${X(v).toFixed(1)}" x2="${X(v).toFixed(1)}" y1="20" y2="${n*lh+22}"/><text x="${X(v).toFixed(1)}" y="${n*lh+36}" text-anchor="middle">${v}</text>`;});
    ch.rows.forEach((r,i)=>{const y=22+i*lh+lh/2,[m,sd]=r[1][j],a=X(Math.max(C.lo,m-sd)),b=X(Math.min(C.hi,m+sd));s+=`<line class="dl" x1="${a.toFixed(1)}" x2="${b.toFixed(1)}" y1="${y}" y2="${y}"/><circle class="dd" cx="${X(m).toFixed(1)}" cy="${y}" r="4.5"><title>${esc(r[0])} · ${esc(C.t)}: ${m.toLocaleString(loc,{maximumFractionDigits:2})} ± ${sd.toLocaleString(loc,{maximumFractionDigits:2})}</title></circle>`;});});
  ch.rows.forEach((r,i)=>{s+=`<text x="${lw-6}" y="${22+i*lh+lh/2+4}" text-anchor="end">${esc(r[0])} (${r[2]})</text>`;});
  return s+"</svg>";}
/* kártyák */
const box=document.getElementById("stcards");if(!box)return;
X.cards.forEach(c=>{const sec=document.createElement("section");sec.className="card fold stcard";sec.id="st-"+c.id;
  sec.innerHTML=`<h2>${esc(c.h)}<span class="foldsub">${esc(c.s)}</span></h2>${c.kpi?`<div class="stkpi">${c.kpi.map(k=>`<div><b>${esc(k[0])}</b>${esc(k[1])}</div>`).join("")}</div>`:""}${c.p.map(p=>`<p>${p}</p>`).join("")}<div class="stchw"></div><div class="stchw2"></div>${c.top?`<ol class="sttop">${c.top.map(t=>`<li>${esc(t)}</li>`).join("")}</ol>`:""}${c.nomap?"":`<p><button class="stbtn" type="button">${esc(X.ui.show)}</button></p>`}<p class="stsrc">${c.src}</p>`;
  box.appendChild(sec);
  if(!c.nomap)sec.querySelector(".stbtn").onclick=()=>{open(c.id);};chart(c,sec.querySelector(".stchw"));draw1(c.ch2,sec.querySelector(".stchw2"),c.h);});
function draw1(ch,w,t,on){if(!ch||!w)return;const cap=ch.cap?`<p class="hint">${esc(ch.cap)}</p>`:"";
  if(ch.line){w.innerHTML=cap+`<p class="hint">${esc(X.ui.loading)}</p>`;getK(ch.line).then(d=>{w.innerHTML=cap+line(d,ch,t);});return;}
  w.innerHTML=cap+(ch.dots?dots(ch,t):ch.heat?heat(ch,t):ch.stack?stack(ch,t):ch.pair?pair(ch,t):bars(ch.rows,{h:ch.h,t:t,on:on,lw:ch.lw,maxl:ch.maxl,int:ch.int,marks:ch.marks}));}
function chart(c,w,on){draw1(c.ch,w,c.h,on);}
/* buborék a diagramokhoz (egér és érintés) */
const tipEl=document.createElement("div");tipEl.className="sttip";tipEl.hidden=true;document.body.appendChild(tipEl);
function tipShow(e){const t=e.target.closest&&e.target.closest(".stch rect,.stch circle");if(!t){tipEl.hidden=true;return;}const ti=t.querySelector("title");if(ti){t.dataset.tip=ti.textContent;ti.remove();}if(!t.dataset.tip){tipEl.hidden=true;return;}
  tipEl.textContent=t.dataset.tip;tipEl.hidden=false;const r=t.getBoundingClientRect(),w=tipEl.offsetWidth;tipEl.style.left=Math.max(6,Math.min(innerWidth-w-6,r.left+r.width/2-w/2))+scrollX+"px";tipEl.style.top=r.top+scrollY-tipEl.offsetHeight-6+"px";}
box.addEventListener("mouseover",tipShow);box.addEventListener("click",tipShow);box.addEventListener("mouseleave",()=>{tipEl.hidden=true;});
/* réteg */
const Vdef={ports:"all",pap:"all",orbis:"tj",clim:"all",epi:"all",mines:"all",cities:"all",leg:"220",wreck:"all",hoard:"all",insc:"all",nic:"all",amph:"all",raad:"all",son:"all",iso:"n",quar:"all",rrs:"all"};
function sel(id,v){const D=DATA,P=[];
  if(id==="cities")for(const c of D.cities){if(v==="big"&&!(c[2]>=100))continue;P.push({x:c[0],y:c[1],r:c[2]?1.6+Math.sqrt(c[2])/2.6:2.2,u:!c[2],i:`<b>${esc(c[3])}</b> · ${esc(c[4])}<br>${c[2]?fmt(c[2])+" ha":X.ui.noarea}${c[5]!==null?` · ${X.ui.from} ${c[5]<0?(-c[5])+(HU?" Kr. e.":" BC"):(HU?"Kr. u. ":"AD ")+c[5]}`:""}`});}
  if(id==="leg"){if(v==="23")for(const l of D.leg23)P.push({x:l[0],y:l[1],r:5+l[2]*3,i:`<b>${esc(l[3])}</b>: ${l[2]} ${X.ui.legs}`,t:String(l[2])});
    else{const by={};for(const l of D.leg220){const k=l[0]+"_"+l[1];(by[k]=by[k]||{x:l[0],y:l[1],n:[],p:l[3],s:l[4]}).n.push(l[2]);}
      for(const k in by){const b=by[k];P.push({x:b.x,y:b.y,r:5+b.n.length*2.5,i:`<b>${esc(b.n.join(", "))}</b><br>${esc(b.p)} · ${esc(b.s)}`,t:b.n.length>1?String(b.n.length):""});}}}
  if(id==="wreck"){const R={w1:[-1e4,-200],w2:[-200,0],w3:[0,200],w4:[200,400],w5:[400,1e4],all:[-1e4,1e4]}[v];
    for(const w of D.wrecks)if(w[3]>=R[0]&&w[2]<R[1])P.push({x:w[0],y:w[1],r:2.6,i:`${X.ui.wreck}: ${yr(w[2])} – ${yr(w[3])}`});}
  if(id==="hoard"){const R={h1:[-1e4,69],h2:[69,193],h3:[193,260],h4:[260,285],h5:[285,1e4],all:[-1e4,1e4]}[v];
    for(const h of D.hoards)if(h[2]>=R[0]&&h[2]<R[1])P.push({x:h[0],y:h[1],r:2.4,i:`${X.ui.hoard}: ${X.ui.closing} ${yr(h[2])}${h[3]?` · ${fmt(h[3])} ${X.ui.coins}`:""}`});}
  if(id==="insc")for(const g of D.insc[v])P.push({x:g[0],y:g[1],r:Math.min(26,1.6+Math.sqrt(g[2])/5),i:`${fmt(g[2])} ${X.ui.insc} · ${X.ui.cell}`});
  if(id==="mines"){const b={all:-1,au:0,ag:1,pb:2,cu:3,sn:4,fe:5}[v];for(const m of D.mines){if(b>=0&&!(m[2]>>b&1))continue;const mt=X.ui.met.filter((_,i)=>m[2]>>i&1).join(", ");P.push({x:m[0],y:m[1],r:2.6,i:`<b>${esc(m[3])}</b>${m[5]?` (${esc(m[5])})`:""} · ${esc(m[4])}<br>${mt||X.ui.nomet}`});}}
  if(id==="clim"){for(const c of D.clim){if(v!=="all"&&c[4]!==v)continue;P.push({x:c[0],y:c[1],r:3,i:`<b>${c[2]===c[3]?yr(c[2]):yr(c[2])+" – "+yr(c[3])}</b> · ${esc(X.ui.ct[c[4]]||c[4])}<br>${esc(c[5])}${!HU&&c[6]?" · "+esc(c[6]):""}`});}}
  if(id==="epi"){const T2={pla:0,ep:3,fa:4,shortage:4},G={};for(const e of D.epi){if(v==="pre"&&e[2]>=541)continue;if(v==="pla"&&e[4]!=="pla")continue;if(v==="ep"&&e[4]!=="ep")continue;if(v==="fa"&&!(e[4]==="fa"||e[4]==="shortage"))continue;const k=e[0]+"_"+e[1];(G[k]=G[k]||{x:e[0],y:e[1],l:[]}).l.push(e);}
    for(const k in G){const g=G[k],cnt={};g.l.sort((a,b)=>a[2]-b[2]);g.l.forEach(e=>{const t=T2[e[4]]??2;cnt[t]=(cnt[t]||0)+1;});const dom=+Object.keys(cnt).sort((a,b)=>cnt[b]-cnt[a])[0],n=g.l.length;
      P.push({x:g.x,y:g.y,r:4.5+Math.sqrt(n)*2.4,cl:"b"+dom,t:n>1?String(n):"",i:`<b>${esc(g.l[0][5])}</b>${n>1?` · ${n} ${X.ui.erec}`:""}<br>`+g.l.slice(0,14).map(e=>`${e[2]===e[3]?yr(e[2]):yr(e[2])+" – "+yr(e[3])}: ${esc(X.ui.et[e[4]]||e[4])}`).join("<br>")+(n>14?"<br>…":"")});}}
  if(id==="orbis"){const j={tj:3,tn:4,fj:5}[v],bd=d=>d<5?0:d<10?1:d<20?2:d<30?3:4,nf=d=>d==null?"–":d.toLocaleString(loc,{maximumFractionDigits:1});for(const o of D.orbis){const d=o[j];if(d==null)continue;P.push({x:o[0],y:o[1],r:3.6,c:bd(d),i:`<b>${esc(o[2])}</b><br>${X.ui.otj}: ${nf(o[3])} · ${X.ui.otn}: ${nf(o[4])} · ${X.ui.ofj}: ${nf(o[5])} ${X.ui.days}`});}P.sort((a,b)=>a.c-b.c);}
  if(id==="pap"){const j={all:3,pt:4,er:5,lr:6,ar:7}[v];for(const a of D.pap){const n=a[j];if(!n)continue;P.push({x:a[0],y:a[1],r:Math.min(30,2+Math.sqrt(n)/1.6),i:`<b>${esc(a[2])}</b><br>${fmt(a[3])} ${X.ui.docs}${X.ui.pper.map((t,i)=>a[4+i]?` · ${t}: ${fmt(a[4+i])}`:"").join("")}`});}}
  if(id==="ports"){const F={all:0,a:1,re:2,bw:8|16,fp:64,vm:128,ph:32,si:256}[v];for(const o of D.ports){if(F&&!(o[4]&F))continue;const ft=X.ui.pf.filter((_,i)=>o[4]>>i&1&&X.ui.pf[i]).join(", ");P.push({x:o[0],y:o[1],r:2.4,i:`<b>${esc(o[2]||o[3])}</b>${o[2]&&o[3]?" · "+esc(o[3]):""}${ft?"<br>"+esc(ft):""}`});}}
  if(id==="nic")for(const n of D.nic)P.push({x:n[0],y:n[1],r:4+Math.sqrt(n[2])*3.2,i:`<b>${esc(n[3])}</b>: ${n[2]} ${X.ui.bish}`,t:n[2]>=4?String(n[2]):""});
  if(id==="amph"){const k={all:-1,w:0,o:1,g:2}[v],nm=X.ui.ac,lg=d=>2+2.1*Math.log10(Math.max(1,d));for(const a of D.amph){const by=a[4],tot=by.reduce((x,y)=>x+y,0),val=k<0?tot:by[k];if(!val)continue;
    P.push({x:a[0],y:a[1],r:lg(val),cl:"a"+(k<0?a[5]:k),i:`<b>${esc(a[2])}</b> · ${esc(a[3])}<br>${X.ui.dens}: ${fmt(tot)} cg/m²${by.map((b,i)=>b?` · ${nm[i]} ${Math.round(100*b/tot)} %`:"").join("")}<br>${a[6]} ${X.ui.atypes}: ${esc(a[7].join(", "))}${a[6]>4?" …":""}`});}}
  if(id==="raad"){const o={all:-1,o0:0,o1:1,o2:2,o3:3,o4:4,o5:5}[v],U=X.ui;for(const l of D.raad){const val=o<0?l[3]:l[4][o];if(!val)continue;
    const as=l[5].map(a=>`<b>${esc(a[0])}</b>${a[1]?` (${esc(a[1])})`:""} · ${esc(U.rst[a[2]]||a[2])} · ${esc(U.rpr[a[3]]||a[3])} · ${yr(a[4][0])} – ${yr(a[4][1])}<br>${a[6]} ${U.atypes} · ${fmt(a[7])} ${esc(U.rq[a[5]]||a[5])}${a[8].map((p,i)=>p?` · ${U.ac[i]} ${p} %`:"").join("")}`).join("<br>");
    P.push({x:l[0],y:l[1],r:2.5+Math.sqrt(val)*1.35,cl:"t"+l[2],i:`${as}<br><span class="stinfo2">${U.rorg}: ${l[4].map((n,i)=>n?`${U.rog[i]} ${n}`:"").filter(Boolean).join(", ")}</span>`});}}
  if(id==="son"){const k={all:-1,w:0,o:1,g:2}[v],U=X.ui,lg=d=>2+3*Math.log10(Math.max(1,d));for(const a of D.sonata){const by=a[4],tot=by.reduce((x,y)=>x+y,0),val=k<0?tot:by[k];if(!val)continue;
    P.push({x:a[0],y:a[1],r:lg(val),cl:"a"+(k<0?a[5]:k),i:`<b>${esc(a[2])}</b> · ${esc(U.reg[a[3]]||a[3])}<br>${fmt(tot)} ${U.frag}${by.map((b,i)=>b?` · ${U.ac[i]} ${Math.round(100*b/tot)} %`:"").join("")}<br>${a[6]} ${U.exc} · ${a[7]} ${U.atypes} · ${yr(a[8][0])} – ${yr(a[8][1])}`});}}
  if(id==="iso"){const U=X.ui,cls=v==="n"?(x=>x<9?0:x<10?1:x<11?2:x<12?3:4):(x=>x<-20?0:x<-19?1:x<-18?2:x<-17?3:4);for(const a of D.iso){const val=v==="n"?a[6]:a[5];
    P.push({x:a[0],y:a[1],r:2.5+Math.sqrt(a[4])*1.1,c:cls(val),i:`<b>${esc(a[2])}</b>${a[3]?` · ${esc(U.ipr[a[3]]||a[3])}`:""}<br>${a[4]} ${U.indv} · δ¹³C ${a[5].toLocaleString(loc)}‰${a[7]!=null?` (±${a[7].toLocaleString(loc)})`:""} · δ¹⁵N ${a[6].toLocaleString(loc)}‰${a[8]!=null?` (±${a[8].toLocaleString(loc)})`:""}<br>${U.idat}: ${a[9][0]===a[9][1]?yr(a[9][0]):yr(a[9][0])+" – "+yr(a[9][1])}<br><span class="stinfo2">${esc(a[10])}</span>`});}P.sort((a,b)=>b.r-a.r);}
  if(id==="quar"){const U=X.ui,k={all:-1,w:0,cm:1,ls:2,ss:3,ig:4,al:5,ex:-2}[v];for(const q of D.quarries){if(k>=0&&q[5]!==k)continue;if(k===-2&&!q[6])continue;
    P.push({x:q[0],y:q[1],r:q[6]?3.6:2.6,c:q[6]?4:1,i:`<b>${esc(q[2])}</b> · ${esc(q[3])} (${esc(U.qcn[q[4]]||q[4])})<br>${esc(U.qcat[q[5]])} · ${esc(U.qre[q[6]])}<br><span class="stinfo2">${esc(U.qbib)}: ${esc(q[7])}</span>`});}P.sort((a,b)=>a.r-b.r);}
  if(id==="rrs"){const U=X.ui,k={all:-1,v:0,m:1,n:2,r:3,i:4,f:5}[v];for(const o of D.rrs){if(k>=0&&o[4]!==k)continue;const fl=o[9];
    P.push({x:o[0],y:o[1],r:o[4]===0?3.4:o[4]===5?2.2:2.8,cl:"b"+o[4],i:`<b>${esc(o[2])}</b> · ${esc(o[3])}${o[11]>=0?` · ${esc(U.rrg[o[11]])}`:""}<br>${esc(U.rcat[o[4]])}${o[10].length?` (${o[10].map(t=>esc(U.rty[t])).join(", ")})`:""}<br>${o[5]!=null&&o[6]!=null?yr(o[5])+" – "+yr(o[6]):U.rnd}${o[7]?" · "+esc(U.rsz[o[7]]):""}${o[8]?" · "+esc(U.rfm[o[8]]):""}${[2,4,8].filter(b=>fl&b).map(b=>"<br>"+esc(U.rfl[b])).join("")}`});}
    P.sort((a,b)=>(a.cl==="b5")-(b.cl==="b5")||0);P.reverse();}
  return P;}
const yr=y=>y<0?(HU?`Kr. e. ${-y}`:`${-y} BC`):(HU?`Kr. u. ${y}`:`AD ${y}`);
function draw(){gS.innerHTML="";rk();const P=sel(cur,view);if(cur!=="orbis"&&cur!=="quar"&&cur!=="rrs")P.sort((a,b)=>b.r-a.r);
  for(const p of P){const c=el("circle",{cx:p.x,cy:-p.y,class:p.u?"u":p.cl?p.cl:p.c!=null?"c"+p.c:"",style:`--v:${p.r.toFixed(2)}`},gS);c.addEventListener("click",ev=>{ev.stopPropagation();gS.querySelectorAll(".on").forEach(e=>e.classList.remove("on"));c.classList.add("on");const f=document.getElementById("stinfo");if(f)f.innerHTML=p.i;});
    if(p.t){const t=el("text",{x:p.x,y:-p.y,dy:"0.35em"},gS);t.textContent=p.t;}}
  const n=document.getElementById("stn");if(n)n.textContent=X.ui.shown.replace("{n}",fmt(P.length));return P;}
function fitData(P){if(!P.length)return fitFull();const q=(a,f)=>a[Math.min(a.length-1,Math.max(0,Math.round(f*(a.length-1))))];const xs=P.map(p=>p.x).sort((a,b)=>a-b),ys=P.map(p=>-p.y).sort((a,b)=>a-b),f=P.length>60?.01:0;
  let x0=q(xs,f),x1=q(xs,1-f),y0=q(ys,f),y1=q(ys,1-f);const pad=Math.max(80,(x1-x0)*.06,(y1-y0)*.06);x0-=pad;x1+=pad;y0-=pad;y1+=pad;
  const r=(svg.clientWidth||1)/(svg.clientHeight||1);let w=Math.max(x1-x0,800),h=Math.max(y1-y0,800/r);if(w/h<r)w=h*r;else h=w/r;return[(x0+x1)/2-w/2,(y0+y1)/2-h/2,w,h];}
function pane(){const c=X.cards.find(c=>c.id===cur);
  return `<div class="stp"><div class="wknav"><b style="flex:1">${esc(c.h)}</b><button class="wk-x st-x" type="button">${esc(X.ui.close)}</button></div>`+
  (c.views?`<div class="stv">${c.views.map(v=>`<button type="button" data-v="${v[0]}" aria-pressed="${v[0]===view}">${esc(v[1])}</button>`).join("")}</div>`:"")+
  `<p class="hint" id="stn"></p>${c.leg?`<div class="stleg">${c.leg.map(l=>`<span><i class="${l.u?"u":l.cl?l.cl:l.c!=null?"c"+l.c:""}" style="width:${2*l.r}px;height:${2*l.r}px"></i>${esc(l.t)}</span>`).join("")}</div>`:""}`+
  `<div id="stinfo">${esc(X.ui.click)}</div>${c.pn.map(p=>`<p>${p}</p>`).join("")}</div>`;}
function wire(){panel.querySelectorAll(".stv button").forEach(b=>b.onclick=()=>{view=b.dataset.v;panel.innerHTML=pane();wire();draw();const c=X.cards.find(c=>c.id===cur);const w=document.querySelector("#st-"+cur+" .stchw");if(w&&c.ch&&c.ch.vk)chart(c,w,c.ch.vk[view]);});
  const x=panel.querySelector(".st-x");if(x)x.onclick=close;}
function close(){cur=null;svg.classList.remove("ston");gS.innerHTML="";window.stPanel=null;panel.innerHTML=panel0;}
async function open(id){svg.classList.add("ston");{const m=document.getElementById("map");if(m){const r=m.getBoundingClientRect();if(r.top<-40||r.top>innerHeight*.4)m.scrollIntoView({behavior:"smooth",block:"start"});}}if(typeof walk!=="undefined"&&walk&&typeof stop==="function")stop();cur=id;view=Vdef[id];panel.innerHTML=`<p class="hint">${esc(X.ui.loading)}</p>`;
  document.querySelector(".main").scrollIntoView({behavior:"smooth",block:"start"});await load(id);if(cur!==id)return;panel.innerHTML=pane();wire();setVBnow(fitData(draw()));window.stPanel=()=>{const h=pane();setTimeout(()=>{wire();draw();},0);return h;};}
document.addEventListener("click",e=>{const b=e.target.closest&&e.target.closest(".walksel2 button");if(b&&cur)close();},true);
})();
