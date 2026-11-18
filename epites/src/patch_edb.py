# v89: „Keresztény feliratok (3–8. század)” kártya. Adat: edb/calc.py -> edb/data.json; szöveg: src/edb_card.py
import json,shutil,sys
sys.path.insert(0,'src');import edb_card as EC
p='body_v60pre.html';b=open(p,encoding='utf8').read();cp='style_v60pre.css';c=open(cp,encoding='utf8').read()
assert 'edbcard' not in b and 'milcard' in b
shutil.copy(p,'src/body_v60pre_before_v89.html');shutil.copy(cp,'src/style_v60pre_before_v89.css')
def rep(s,a,x,n=1):
    assert s.count(a)==n,(a[:60],s.count(a));return s.replace(a,x)
D=EC.D
card,src,sub=EC.build('hu')
b=rep(b,'    <section class="card" id="bldcard">',card+'    <section class="card" id="bldcard">')
js='''/* v89: keresztény feliratok (edb/data.json) */
const EDBD='''+json.dumps({"bins":D['bins'],"w":D['w'],"time":D['time']},separators=(',',':'))+''';
var edbYear=null;
(function(){const card=document.getElementById("edbcard"),box=document.getElementById("edbchart");if(!card||!box)return;const NS="http://www.w3.org/2000/svg",loc=document.documentElement.lang==="en"?"en-US":"hu-HU";
  const mk=(n,a,p)=>{const e=document.createElementNS(NS,n);for(const k in a)e.setAttribute(k,a[k]);if(p)p.appendChild(e);return e;};
  const info=document.getElementById("edbinfo"),labs=[...card.querySelectorAll("#edbleg .il")].map(e=>e.textContent),ks=box.dataset.k.split(","),B=EDBD.bins,W=EDBD.w,TT=EDBD.time;let yv=null;
  const idx=B.map((_,i)=>i).filter(i=>TT.all[i]>=30),X0=B[idx[0]],X1=B[idx[idx.length-1]]+W,sh=(k,i)=>100*TT[k][i]/TT.all[i],f1=v=>v.toLocaleString(loc,{maximumFractionDigits:v<10?1:0});
  const mark=()=>{const s=box.querySelector("svg");if(!s||!s._yl)return;const y=yv;if(y==null||y==="all"||y<X0||y>X1){s._yl.style.display="none";return;}const x=s._xs(+y);s._yl.setAttribute("x1",x);s._yl.setAttribute("x2",x);s._yl.style.display="";};
  edbYear=function(y){yv=y;mark();};
  function draw(){box.innerHTML="";const Wd=Math.max(320,Math.min(1600,box.clientWidth||660)),H=Wd<520?190:Math.min(400,Math.max(220,Math.round(Wd*0.27))),L=40,R=12,Tp=8,Bt=26;
    const s=mk("svg",{viewBox:`0 0 ${Wd} ${H}`,width:Wd,height:H,class:"bldsvg edbsvg"},box);
    const mx=Math.max(...ks.map(k=>Math.max(...idx.map(i=>sh(k,i)))))*1.08,sy=v=>Tp+(1-v/mx)*(H-Tp-Bt),xs=x=>L+(x-X0)/(X1-X0)*(Wd-L-R),step=[5,10,20].find(x=>mx/x<=6)||25;
    for(let v=0;v<=mx;v+=step){const y=sy(v);mk("line",{x1:L,x2:Wd-R,y1:y,y2:y,class:"pg"},s);const t=mk("text",{x:L-5,y:y+4,"text-anchor":"end",class:"pt"},s);t.textContent=v+"%";}
    (Wd<520?[200,400,600]:[200,300,400,500,600,700]).forEach(x=>{const t=mk("text",{x:xs(x),y:H-Bt+16,"text-anchor":x===200?"start":"middle",class:"pt"},s);t.textContent=fmtY(x);});
    mk("line",{x1:L,x2:Wd-R,y1:H-Bt,y2:H-Bt,class:"pax"},s);
    ks.forEach(k=>{mk("path",{d:idx.map((i,j)=>(j?"L":"M")+xs(B[i]+W/2).toFixed(1)+","+sy(sh(k,i)).toFixed(1)).join(""),class:"edbl e"+k},s);});
    const dots=mk("g",{},s);
    idx.forEach(i=>{const x=B[i],g0=mk("g",{class:"bb"},s);mk("rect",{x:xs(x),y:Tp,width:xs(x+W)-xs(x),height:H-Tp-Bt,class:"bhit"},g0);
      const show=()=>{s.querySelectorAll(".bb.on").forEach(e=>e.classList.remove("on"));g0.classList.add("on");dots.innerHTML="";ks.forEach(k=>mk("circle",{cx:xs(x+W/2),cy:sy(sh(k,i)),r:3.5,class:"edbd e"+k},dots));
        info.textContent=fmtY(x)+"–"+(x+W)+" · "+Math.round(TT.all[i]).toLocaleString(loc)+" · "+ks.map((k,j)=>labs[j]+": "+f1(sh(k,i))+"%").join("; ");};
      g0.addEventListener("mouseenter",show);g0.addEventListener("click",()=>{show();if(typeof setYear==="function")setYear(Math.max(-1000,Math.min(650,x+Math.round(W/2))));});});
    const yl=mk("line",{class:"py",y1:Tp,y2:H-Bt,x1:0,x2:0},s);yl.style.display="none";s._yl=yl;s._xs=xs;mark();}
  draw();let lw=0;if(window.ResizeObserver)new ResizeObserver(()=>{const w=box.clientWidth;if(w&&Math.abs(w-lw)>4){lw=w;draw();}}).observe(box);
  card.querySelectorAll("[data-goto]").forEach(a=>a.addEventListener("click",e=>{e.preventDefault();goTo(a.dataset.goto);}));
  edbYear(state.year);})();
'''
b=rep(b,'/* v79: építkezések időrendben (bld/data.json) */',js+'/* v79: építkezések időrendben (bld/data.json) */')
b=rep(b,'if(milYear)milYear(y);','if(milYear)milYear(y);if(edbYear)edbYear(y);')
b=rep(b,'"Építkezések időrendben":"az','"Keresztény feliratok (3–8. század)":"'+sub+'","Építkezések időrendben":"az')
b=rep(b,'      <li><b>Építkezések időrendben.</b>',src+'\n      <li><b>Építkezések időrendben.</b>')
c=rep(c,'</style>','''/* v89: keresztény feliratok */
#edbcard{--egrc:#2f7fb8;--echr:#c0392b;--ecrs:#6b3fa0;--esy:#8a5a44;--erd:#3d7f6e;--emo:#e08a1e;--efo:#6b3fa0}
#edbcard.open{grid-column:1/-1}
#edbcard .egrc{background:var(--egrc);stroke:var(--egrc);fill:var(--egrc)}#edbcard .echr{background:var(--echr);stroke:var(--echr);fill:var(--echr)}#edbcard .ecrs{background:var(--ecrs);stroke:var(--ecrs);fill:var(--ecrs)}
#edbcard .edbsvg path.edbl{fill:none;stroke-width:2.2;stroke-linejoin:round;stroke-linecap:round}#edbcard .edbsvg circle.edbd{stroke:var(--sheet);stroke-width:1.5}
#edbcard .edbbars .fe{grid-template-columns:minmax(0,1.2fr) minmax(80px,1.3fr) 3.6em}#edbcard .edbbars .fev{text-align:right}
#edbcard .edbbars .feb span.esy{background:var(--esy)}#edbcard .edbbars .feb span.erd{background:var(--erd)}#edbcard .edbbars .feb span.emo{background:var(--emo)}#edbcard .edbbars .feb span.efo{background:var(--efo)}
#edbcard .edbmon .fe{grid-template-columns:7em minmax(80px,1fr) 3em}
</style>''')
open(p,'w',encoding='utf8').write(b);open(cp,'w',encoding='utf8').write(c);print('ok')
