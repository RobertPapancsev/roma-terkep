# v88: „Sírtelkek mérete” és „Katonák Róma sírfeliratain” kártya. Adat: plot/calc.py, mil/calc.py; szöveg: src/mp_card.py
import json,shutil,sys
sys.path.insert(0,'src');import mp_card as MC
p='body_v60pre.html';b=open(p,encoding='utf8').read();cp='style_v60pre.css';c=open(cp,encoding='utf8').read()
assert 'milcard' not in b and 'agecard' in b
shutil.copy(p,'src/body_v60pre_before_v88.html');shutil.copy(cp,'src/style_v60pre_before_v88.css')
def rep(s,a,x,n=1):
    assert s.count(a)==n,(a[:60],s.count(a));return s.replace(a,x)
M=MC.M
card,src,subs=MC.build('hu')
b=rep(b,'    <section class="card" id="bldcard">',card+'    <section class="card" id="bldcard">')
keys=[k for k,_,_ in MC.LN]
js='''/* v88: katonák Róma sírfeliratain (mil/data.json) */
const MILD='''+json.dumps({"bins":M['bins'],"w":M['w'],"time":{k:M['time'][k] for k in keys}},separators=(',',':'))+''';
var milYear=null;
(function(){const card=document.getElementById("milcard"),box=document.getElementById("milchart");if(!card||!box)return;const NS="http://www.w3.org/2000/svg",loc=document.documentElement.lang==="en"?"en-US":"hu-HU";
  const mk=(n,a,p)=>{const e=document.createElementNS(NS,n);for(const k in a)e.setAttribute(k,a[k]);if(p)p.appendChild(e);return e;};
  const info=document.getElementById("milinfo"),labs=[...card.querySelectorAll("#milleg .il")].map(e=>e.textContent),ks=box.dataset.k.split(","),B=MILD.bins,W=MILD.w;let yv=null;
  const idx=B.map((_,i)=>i).filter(i=>B[i]>=-50&&B[i]<400),X0=B[idx[0]],X1=B[idx[idx.length-1]]+W,f1=v=>v.toLocaleString(loc,{maximumFractionDigits:v<10?1:0});
  const mark=()=>{const s=box.querySelector("svg");if(!s||!s._yl)return;const y=yv;if(y==null||y==="all"||y<X0||y>X1){s._yl.style.display="none";return;}const x=s._xs(+y);s._yl.setAttribute("x1",x);s._yl.setAttribute("x2",x);s._yl.style.display="";};
  milYear=function(y){yv=y;mark();};
  function draw(){box.innerHTML="";const Wd=Math.max(320,Math.min(1600,box.clientWidth||660)),H=Wd<520?190:Math.min(400,Math.max(220,Math.round(Wd*0.27))),L=40,R=12,Tp=8,Bt=26;
    const s=mk("svg",{viewBox:`0 0 ${Wd} ${H}`,width:Wd,height:H,class:"bldsvg milsvg"},box);
    const mx=Math.max(...ks.map(k=>Math.max(...idx.map(i=>MILD.time[k][i]))))*1.08,sy=v=>Tp+(1-v/mx)*(H-Tp-Bt),xs=x=>L+(x-X0)/(X1-X0)*(Wd-L-R),step=[5,10,20,25,50].find(x=>mx/x<=6)||100;
    for(let v=0;v<=mx;v+=step){const y=sy(v);mk("line",{x1:L,x2:Wd-R,y1:y,y2:y,class:"pg"},s);const t=mk("text",{x:L-5,y:y+4,"text-anchor":"end",class:"pt"},s);t.textContent=v;}
    (Wd<520?[0,200,400]:[0,100,200,300,400]).forEach(x=>{const t=mk("text",{x:xs(x),y:H-Bt+16,"text-anchor":x===400?"end":"middle",class:"pt"},s);t.textContent=x===0?"0":fmtY(x);});
    mk("line",{x1:L,x2:Wd-R,y1:H-Bt,y2:H-Bt,class:"pax"},s);
    ks.forEach(k=>{mk("path",{d:idx.map((i,j)=>(j?"L":"M")+xs(B[i]+W/2).toFixed(1)+","+sy(MILD.time[k][i]).toFixed(1)).join(""),class:"mill u"+k},s);});
    const dots=mk("g",{},s);
    idx.forEach(i=>{const x=B[i],g0=mk("g",{class:"bb"},s);mk("rect",{x:xs(x),y:Tp,width:xs(x+W)-xs(x),height:H-Tp-Bt,class:"bhit"},g0);
      const show=()=>{s.querySelectorAll(".bb.on").forEach(e=>e.classList.remove("on"));g0.classList.add("on");dots.innerHTML="";ks.forEach(k=>mk("circle",{cx:xs(x+W/2),cy:sy(MILD.time[k][i]),r:3.5,class:"mild u"+k},dots));
        info.textContent=fmtY(x)+"–"+fmtY(x+W)+" · "+ks.map((k,j)=>labs[j]+": "+f1(MILD.time[k][i])).join("; ");};
      g0.addEventListener("mouseenter",show);g0.addEventListener("click",()=>{show();if(typeof setYear==="function")setYear(Math.max(-1000,Math.min(650,x+Math.round(W/2))));});});
    const yl=mk("line",{class:"py",y1:Tp,y2:H-Bt,x1:0,x2:0},s);yl.style.display="none";s._yl=yl;s._xs=xs;mark();}
  draw();let lw=0;if(window.ResizeObserver)new ResizeObserver(()=>{const w=box.clientWidth;if(w&&Math.abs(w-lw)>4){lw=w;draw();}}).observe(box);
  card.querySelectorAll("[data-goto]").forEach(a=>a.addEventListener("click",e=>{e.preventDefault();goTo(a.dataset.goto);}));
  milYear(state.year);})();
'''
b=rep(b,'/* v86: életkor és család a sírfeliratokon (age/data.json) */',js+'/* v86: életkor és család a sírfeliratokon (age/data.json) */')
b=rep(b,'if(ageYear)ageYear(y);}','if(ageYear)ageYear(y);if(milYear)milYear(y);}')
b=rep(b,'"Építkezések időrendben":"az',''.join('"'+k+'":"'+v+'",' for k,v in subs.items())+'"Építkezések időrendben":"az')
b=rep(b,'      <li><b>Építkezések időrendben.</b>','\n'.join(src)+'\n      <li><b>Építkezések időrendben.</b>')
c=rep(c,'</style>','''/* v88: sírtelkek, katonák */
#plotcard.open,#milcard.open{grid-column:1/-1}
#plotcard .plotbars .fe{grid-template-columns:minmax(0,1.3fr) minmax(80px,1.2fr) 3em}#plotcard .plotbars .feb span{background:#8a5a44}#plotcard .plotbars .fev{text-align:right}
.numtab th:not(:first-child),.cohtab th:not(:first-child){text-align:right}.cohtab td,.cohtab th{white-space:nowrap}
#milcard{--upraet:#c0392b;--ueqs:#2f7fb8;--uurb:#e08a1e;--ucla:#3d7f6e}
#milcard .upraet{background:var(--upraet);stroke:var(--upraet);fill:var(--upraet)}#milcard .ueqs{background:var(--ueqs);stroke:var(--ueqs);fill:var(--ueqs)}#milcard .uurb{background:var(--uurb);stroke:var(--uurb);fill:var(--uurb)}#milcard .ucla{background:var(--ucla);stroke:var(--ucla);fill:var(--ucla)}
#milcard .milsvg path.mill{fill:none;stroke-width:2.2;stroke-linejoin:round;stroke-linecap:round}#milcard .milsvg circle.mild{stroke:var(--sheet);stroke-width:1.5}
.miltab .sm{color:var(--muted);font-size:12px}.miltab td.pn{white-space:nowrap}
</style>''')
open(p,'w',encoding='utf8').write(b);open(cp,'w',encoding='utf8').write(c);print('ok')
