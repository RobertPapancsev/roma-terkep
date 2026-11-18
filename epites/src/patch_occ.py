# v84: „Foglalkozások a feliratokon” kártya. Adat: occ/calc.py -> occ/data.json; szöveg: src/occ_card.py
import json,shutil,sys
sys.path.insert(0,'src');import occ_card as OC
p='body_v60pre.html';b=open(p,encoding='utf8').read();cp='style_v60pre.css';c=open(cp,encoding='utf8').read()
assert 'occcard' not in b
shutil.copy(p,'src/body_v60pre_before_v84.html');shutil.copy(cp,'src/style_v60pre_before_v84.css')
def rep(s,a,x,n=1):
    assert s.count(a)==n,(a[:60],s.count(a));return s.replace(a,x)
D=OC.D
card,src,sub=OC.build('hu')
b=rep(b,'    <section class="card" id="bldcard">',card+'    <section class="card" id="bldcard">')
js='''/* v84: foglalkozások a feliratokon (occ/data.json) */
const OCCD='''+json.dumps({"bins":D['bins'],"w":D['w'],"time":D['time']},separators=(',',':'))+''';
var occYear=null;
(function(){const card=document.getElementById("occcard"),box=document.getElementById("occchart");if(!card||!box)return;const NS="http://www.w3.org/2000/svg",loc=document.documentElement.lang==="en"?"en-US":"hu-HU";
  const labs=[...card.querySelectorAll(".occleg .il")].map(e=>e.textContent.replace(/ \\(.*\\)/,""));
  const secs=[...card.querySelectorAll(".occsec .fe")],rows=[...card.querySelectorAll(".occtab tbody tr")],more=document.getElementById("occmore");
  const info=document.getElementById("occinfo"),info0=info.textContent,tinfo=document.getElementById("occtinfo");let sel=null,yv=null;
  const B=OCCD.bins,W=OCCD.w,f0=v=>Math.round(v).toLocaleString(loc);
  const secInfo=fe=>{const st=fe.dataset.st.split(",").map(Number),tot=st.reduce((a,x)=>a+x,0);info.textContent=fe.querySelector(".fen").textContent+": "+(+fe.dataset.c).toLocaleString(loc)+" · "+st.map((v,i)=>v?labs[i]+": "+v+" ("+Math.round(100*v/tot)+"%)":"").filter(Boolean).join("; ");};
  const filt=()=>{const all=more.dataset.on==="1";rows.forEach(r=>{r.hidden=sel?r.dataset.s!==sel.dataset.s:!(all||r.classList.contains("otop"));});more.parentNode.hidden=!!sel;};
  secs.forEach(fe=>{fe.addEventListener("mouseenter",()=>secInfo(fe));fe.addEventListener("mouseleave",()=>{if(sel)secInfo(sel);else info.textContent=info0;});
    const tg=()=>{sel=sel===fe?null:fe;secs.forEach(x=>{x.classList.toggle("on",x===sel);x.classList.toggle("dim",!!sel&&x!==sel);x.setAttribute("aria-pressed",String(x===sel));});if(sel)secInfo(sel);else info.textContent=info0;filt();draw();};
    fe.addEventListener("click",tg);fe.addEventListener("keydown",e=>{if(e.key==="Enter"||e.key===" "){e.preventDefault();tg();}});});
  const ms=[...card.querySelectorAll(".occmode button")];ms.forEach(bt=>bt.addEventListener("click",()=>{ms.forEach(x=>x.setAttribute("aria-pressed",String(x===bt)));card.querySelectorAll(".occsec .ok").forEach(s=>{s.style.width=s.dataset[bt.dataset.m]+"%";});}));
  more.addEventListener("click",()=>{more.dataset.on=more.dataset.on==="1"?"0":"1";filt();});
  const mk=(n,a,p)=>{const e=document.createElementNS(NS,n);for(const k in a)e.setAttribute(k,a[k]);if(p)p.appendChild(e);return e;};
  function draw(){const ks=sel?[sel.dataset.s]:Object.keys(OCCD.time),tot=B.map((_,k)=>ks.reduce((a,g)=>a+OCCD.time[g][k],0));box.innerHTML="";
    const Wd=Math.max(320,Math.min(1600,box.clientWidth||660)),H=Wd<520?170:Math.min(380,Math.max(200,Math.round(Wd*0.25))),L=40,R=10,Tp=8,Bt=26;
    const s=mk("svg",{viewBox:`0 0 ${Wd} ${H}`,width:Wd,height:H,class:"bldsvg"},box);const n=B.length,bw=(Wd-L-R)/n;
    const mx=Math.max(...tot)*1.05||1,sy=v=>Tp+(1-v/mx)*(H-Tp-Bt);const st=[1,2,5,10,20,50,100,200,500];const step=st.find(x=>mx/x<=6)||1000;
    for(let v=0;v<=mx;v+=step){const y=sy(v);mk("line",{x1:L,x2:Wd-R,y1:y,y2:y,class:"pg"},s);const t=mk("text",{x:L-5,y:y+4,"text-anchor":"end",class:"pt"},s);t.textContent=v.toLocaleString(loc);}
    const xs=x=>L+(x-B[0])/W*bw;(Wd>900?[-200,-100,0,100,200,300,400,500,600,700]:Wd<520?[-200,200,600]:[-200,0,200,400,600]).forEach(x=>{const t=mk("text",{x:Math.min(Wd-R,Math.max(L,xs(x))),y:H-Bt+16,"text-anchor":x===-200?"start":x===700?"end":"middle",class:"pt"},s);t.textContent=x===0?"0":fmtY(x);});
    mk("line",{x1:L,x2:Wd-R,y1:H-Bt,y2:H-Bt,class:"pax"},s);const nm=sel?sel.querySelector(".fen").textContent+" · ":"";
    B.forEach((x,k)=>{const g0=mk("g",{class:"bb"},s),v=tot[k];if(v>0)mk("rect",{x:xs(x)+0.5,y:sy(v),width:Math.max(1,bw-1),height:Math.max(0,sy(0)-sy(v)),class:"occb"},g0);
      mk("rect",{x:xs(x),y:Tp,width:bw,height:H-Tp-Bt,class:"bhit"},g0);
      const show=()=>{s.querySelectorAll(".bb.on").forEach(e=>e.classList.remove("on"));g0.classList.add("on");if(tinfo)tinfo.textContent=nm+fmtY(x)+"–"+fmtY(x+W)+" · "+f0(v);};
      g0.addEventListener("mouseenter",show);g0.addEventListener("click",()=>{show();if(typeof setYear==="function")setYear(Math.max(-1000,Math.min(650,x+Math.round(W/2))));});});
    const yl=mk("line",{class:"py",y1:Tp,y2:H-Bt,x1:0,x2:0},s);yl.style.display="none";s._yl=yl;s._xs=xs;occYear(yv);}
  occYear=function(y){yv=y;const s=box.querySelector("svg");if(!s||!s._yl)return;if(y==null||y==="all"||y<B[0]||y>B[B.length-1]+W){s._yl.style.display="none";return;}const x=s._xs(+y);s._yl.setAttribute("x1",x);s._yl.setAttribute("x2",x);s._yl.style.display="";};
  card.querySelectorAll("[data-goto]").forEach(a=>a.addEventListener("click",e=>{e.preventDefault();if(a.dataset.at){const q=a.dataset.at.split(",").map(Number),w=Math.min(vb[2],320),h=w*vb[3]/vb[2];setVB([q[0]-w/2,-q[1]-h/2,w,h]);document.querySelector(".mapbox").scrollIntoView({behavior:"auto",block:"nearest"});}else goTo(a.dataset.goto);}));
  filt();draw();occYear(state.year);let lw=0;if(window.ResizeObserver)new ResizeObserver(()=>{const w=box.clientWidth;if(w&&Math.abs(w-lw)>4){lw=w;draw();}}).observe(box);})();
'''
b=rep(b,'/* v82: feliratok (insc/data.json) */',js+'/* v82: feliratok (insc/data.json) */')
b=rep(b,'if(inscYear)inscYear(y);}','if(inscYear)inscYear(y);if(occYear)occYear(y);}')
b=rep(b,'"Építkezések időrendben":"az','"Foglalkozások a feliratokon":"'+sub+'","Építkezések időrendben":"az')
b=rep(b,'      <li><b>Építkezések időrendben.</b>',src+'\n      <li><b>Építkezések időrendben.</b>')
c=rep(c,'</style>','''/* v84: foglalkozások a feliratokon */
#occcard{--oil:#6b3fa0;--ois:#b79ad6;--ol:#2f7fb8;--os:#8a5a44;--of:#c9a227;--ou:#c3c9cc;--oc:#3d7f6e}
#occcard.open{grid-column:1/-1}
#occcard .oil{background:var(--oil)}#occcard .ois{background:var(--ois)}#occcard .ol{background:var(--ol)}#occcard .os{background:var(--os)}#occcard .of{background:var(--of)}#occcard .ou{background:var(--ou)}
.occsec .fe{grid-template-columns:minmax(0,1fr) minmax(80px,1.6fr) 3.4em;cursor:pointer;border-radius:4px;padding:2px 4px}
.occsec .fe:hover,.occsec .fe.on{background:rgba(0,0,0,.05)}.occsec .fe.dim{opacity:.45}.occsec .fe.on .fen{font-weight:700}
.occsec .fe:focus-visible{outline:2px solid var(--ink);outline-offset:1px}
.occsec .feb{display:flex;overflow:hidden}.occsec .feb span.ok{display:block;flex:none;height:100%;border-radius:0;transition:width .25s}
.occsec .fev{text-align:right}
.omini{display:flex;width:110px;max-width:100%;height:10px;border-radius:2px;overflow:hidden;background:rgba(0,0,0,.05)}.omini .ok{display:block;flex:none;height:100%}
.occtab td:nth-child(5){vertical-align:middle}.occtab tr[hidden]{display:none}
.occmore{border:1px solid var(--line);background:transparent;color:var(--ink);font:500 13px var(--font-body);padding:5px 12px;border-radius:999px;cursor:pointer}
.occmore[data-on="0"] .om1,.occmore[data-on="1"] .om0{display:none}
.bldsvg .occb{fill:var(--oc)}
.insctab td[title]{cursor:help;text-decoration:underline dotted;text-underline-offset:3px}
@media (prefers-reduced-motion:reduce){.occsec .feb span.ok{transition:none}}
</style>''')
open(p,'w',encoding='utf8').write(b);open(cp,'w',encoding='utf8').write(c);print('ok')
