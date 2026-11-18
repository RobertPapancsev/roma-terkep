# v86: „Életkor és család a sírfeliratokon” kártya. Adat: age/calc.py -> age/data.json; szöveg: src/age_card.py
import json,shutil,sys
sys.path.insert(0,'src');import age_card as AC
p='body_v60pre.html';b=open(p,encoding='utf8').read();cp='style_v60pre.css';c=open(cp,encoding='utf8').read()
assert 'agecard' not in b and 'nmcard' in b
shutil.copy(p,'src/body_v60pre_before_v86.html');shutil.copy(cp,'src/style_v60pre_before_v86.css')
def rep(s,a,x,n=1):
    assert s.count(a)==n,(a[:60],s.count(a));return s.replace(a,x)
D=AC.D
card,src,sub=AC.build('hu')
b=rep(b,'    <section class="card" id="bldcard">',card+'    <section class="card" id="bldcard">')
keys=[k for k,_,_ in AC.LN]
js='''/* v86: életkor és család a sírfeliratokon (age/data.json) */
const AGED='''+json.dumps({"bins":D['bins'],"w":D['w'],"tot":D['tot'],"time":{k:D['time'][k] for k in keys},"hist":D['hist']},separators=(',',':'))+''';
var ageYear=null;
(function(){const card=document.getElementById("agecard");if(!card)return;const NS="http://www.w3.org/2000/svg",loc=document.documentElement.lang==="en"?"en-US":"hu-HU";
  const mk=(n,a,p)=>{const e=document.createElementNS(NS,n);for(const k in a)e.setAttribute(k,a[k]);if(p)p.appendChild(e);return e;};
  const f1=v=>v.toLocaleString(loc,{maximumFractionDigits:v<10?1:0}),lab=id=>[...card.querySelectorAll("#"+id+" .il")].map(e=>e.textContent.replace(/ \\(.*\\)/,""));
  const watch=(box,draw)=>{draw();let lw=0;if(window.ResizeObserver)new ResizeObserver(()=>{const w=box.clientWidth;if(w&&Math.abs(w-lw)>4){lw=w;draw();}}).observe(box);};
  {const box=document.getElementById("agechart"),info=document.getElementById("ageinfo"),labs=lab("ageleg"),S=["m","f","u"],H0=AGED.hist,n=H0.m.length;
   watch(box,()=>{box.innerHTML="";const Wd=Math.max(320,Math.min(1600,box.clientWidth||660)),H=Wd<520?180:Math.min(380,Math.max(210,Math.round(Wd*0.26))),L=44,R=10,Tp=8,Bt=26;
    const s=mk("svg",{viewBox:`0 0 ${Wd} ${H}`,width:Wd,height:H,class:"bldsvg"},box),bw=(Wd-L-R)/n,tot=H0.m.map((_,i)=>S.reduce((a,k)=>a+H0[k][i],0)),mx=Math.max(...tot)*1.05,sy=v=>Tp+(1-v/mx)*(H-Tp-Bt),step=[50,100,200,250,500].find(x=>mx/x<=6)||1000;
    for(let v=0;v<=mx;v+=step){const y=sy(v);mk("line",{x1:L,x2:Wd-R,y1:y,y2:y,class:"pg"},s);const t=mk("text",{x:L-5,y:y+4,"text-anchor":"end",class:"pt"},s);t.textContent=v.toLocaleString(loc);}
    mk("line",{x1:L,x2:Wd-R,y1:H-Bt,y2:H-Bt,class:"pax"},s);
    for(let i=0;i<n;i++){const x=L+i*bw,g0=mk("g",{class:"bb"},s);let acc=0;S.forEach(k=>{const v=H0[k][i];if(!v)return;mk("rect",{x:x+1,y:sy(acc+v),width:Math.max(1,bw-2),height:sy(acc)-sy(acc+v),class:"a"+k},g0);acc+=v;});
      mk("rect",{x:x,y:Tp,width:bw,height:H-Tp-Bt,class:"bhit"},g0);const nm=i===n-1?"80+":(i*5)+"–"+(i*5+4);
      if(Wd>=520||i%2===0||i===n-1){const t=mk("text",{x:x+bw/2,y:H-Bt+16,"text-anchor":"middle",class:"pt"},s);t.textContent=nm;}
      const show=()=>{s.querySelectorAll(".bb.on").forEach(e=>e.classList.remove("on"));g0.classList.add("on");info.textContent=nm+" · "+tot[i].toLocaleString(loc)+" ("+S.map((k,j)=>labs[j]+": "+H0[k][i].toLocaleString(loc)).join("; ")+")";};g0.addEventListener("mouseenter",show);g0.addEventListener("click",show);}});}
  {const box=document.getElementById("agechart2"),info=document.getElementById("ageinfo2"),labs=lab("ageleg2"),ks=box.dataset.k.split(","),B=AGED.bins,W=AGED.w;let yv=null;
   const idx=B.map((_,i)=>i).filter(i=>AGED.tot[i]>=40&&B[i]>=-100&&B[i]<400),X0=B[idx[0]],X1=B[idx[idx.length-1]]+W,sh=(k,i)=>100*AGED.time[k][i]/AGED.tot[i];
   const mark=()=>{const s=box.querySelector("svg");if(!s||!s._yl)return;const y=yv;if(y==null||y==="all"||y<X0||y>X1){s._yl.style.display="none";return;}const x=s._xs(+y);s._yl.setAttribute("x1",x);s._yl.setAttribute("x2",x);s._yl.style.display="";};
   ageYear=function(y){yv=y;mark();};
   watch(box,()=>{box.innerHTML="";const Wd=Math.max(320,Math.min(1600,box.clientWidth||660)),H=Wd<520?190:Math.min(400,Math.max(220,Math.round(Wd*0.27))),L=40,R=12,Tp=8,Bt=26;
    const s=mk("svg",{viewBox:`0 0 ${Wd} ${H}`,width:Wd,height:H,class:"bldsvg agesvg"},box);
    const mx=Math.max(...ks.map(k=>Math.max(...idx.map(i=>sh(k,i)))))*1.08,sy=v=>Tp+(1-v/mx)*(H-Tp-Bt),xs=x=>L+(x-X0)/(X1-X0)*(Wd-L-R),step=[1,2,5,10,20].find(x=>mx/x<=6)||25;
    for(let v=0;v<=mx;v+=step){const y=sy(v);mk("line",{x1:L,x2:Wd-R,y1:y,y2:y,class:"pg"},s);const t=mk("text",{x:L-5,y:y+4,"text-anchor":"end",class:"pt"},s);t.textContent=v+"%";}
    (Wd<520?[-100,100,300]:[-100,0,100,200,300,400]).forEach(x=>{const t=mk("text",{x:xs(x),y:H-Bt+16,"text-anchor":x===-100?"start":x===400?"end":"middle",class:"pt"},s);t.textContent=x===0?"0":fmtY(x);});
    mk("line",{x1:L,x2:Wd-R,y1:H-Bt,y2:H-Bt,class:"pax"},s);
    ks.forEach(k=>{mk("path",{d:idx.map((i,j)=>(j?"L":"M")+xs(B[i]+W/2).toFixed(1)+","+sy(sh(k,i)).toFixed(1)).join(""),class:"agel r"+k},s);});
    const dots=mk("g",{},s);
    idx.forEach(i=>{const x=B[i],g0=mk("g",{class:"bb"},s);mk("rect",{x:xs(x),y:Tp,width:xs(x+W)-xs(x),height:H-Tp-Bt,class:"bhit"},g0);
      const show=()=>{s.querySelectorAll(".bb.on").forEach(e=>e.classList.remove("on"));g0.classList.add("on");dots.innerHTML="";ks.forEach(k=>mk("circle",{cx:xs(x+W/2),cy:sy(sh(k,i)),r:3.5,class:"aged r"+k},dots));
        info.textContent=fmtY(x)+"–"+fmtY(x+W)+" · "+ks.map((k,j)=>labs[j]+": "+f1(sh(k,i))+"%").join("; ");};
      g0.addEventListener("mouseenter",show);g0.addEventListener("click",()=>{show();if(typeof setYear==="function")setYear(Math.max(-1000,Math.min(650,x+Math.round(W/2))));});});
    const yl=mk("line",{class:"py",y1:Tp,y2:H-Bt,x1:0,x2:0},s);yl.style.display="none";s._yl=yl;s._xs=xs;mark();});}
  card.querySelectorAll("[data-goto]").forEach(a=>a.addEventListener("click",e=>{e.preventDefault();goTo(a.dataset.goto);}));
  ageYear(state.year);})();
'''
b=rep(b,'/* v85: jogállás és császári nevek időben (nm/data.json) */',js+'/* v85: jogállás és császári nevek időben (nm/data.json) */')
b=rep(b,'if(nmYear)nmYear(y);}','if(nmYear)nmYear(y);if(ageYear)ageYear(y);}')
b=rep(b,'"Építkezések időrendben":"az','"Életkor és család a sírfeliratokon":"'+sub+'","Építkezések időrendben":"az')
b=rep(b,'      <li><b>Építkezések időrendben.</b>',src+'\n      <li><b>Építkezések időrendben.</b>')
c=rep(c,'</style>','''/* v86: életkor és család a sírfeliratokon */
#agecard{--am:#2f7fb8;--af:#c0392b;--au:#c3c9cc;--rspouse:#c0392b;--rchild:#e08a1e;--rparent:#3d7f6e;--rpatron:#6b3fa0;--rself:#8c8c8c;--gfam:#c0392b;--ghh:#6b3fa0;--gam:#3d7f6e;--gkin:#e08a1e}
#agecard.open{grid-column:1/-1}
#agecard .am{background:var(--am);fill:var(--am)}#agecard .af{background:var(--af);fill:var(--af)}#agecard .au{background:var(--au);fill:var(--au)}
#agecard .rspouse{background:var(--rspouse);stroke:var(--rspouse);fill:var(--rspouse)}#agecard .rchild{background:var(--rchild);stroke:var(--rchild);fill:var(--rchild)}#agecard .rparent{background:var(--rparent);stroke:var(--rparent);fill:var(--rparent)}#agecard .rpatron{background:var(--rpatron);stroke:var(--rpatron);fill:var(--rpatron)}#agecard .rself{background:var(--rself);stroke:var(--rself);fill:var(--rself)}
#agecard .agesvg path.agel{fill:none;stroke-width:2.2;stroke-linejoin:round;stroke-linecap:round}#agecard .agesvg circle.aged{stroke:var(--sheet);stroke-width:1.5}
#agecard .agerel .fe{grid-template-columns:minmax(0,1.3fr) minmax(80px,1.2fr) 3.6em}#agecard .agerel .fev{text-align:right}
#agecard .agerel .feb span.gfam{background:var(--gfam)}#agecard .agerel .feb span.ghh{background:var(--ghh)}#agecard .agerel .feb span.gam{background:var(--gam)}#agecard .agerel .feb span.gkin{background:var(--gkin)}
.agetab th:not(:first-child){text-align:right}
</style>''')
open(p,'w',encoding='utf8').write(b);open(cp,'w',encoding='utf8').write(c);print('ok')
