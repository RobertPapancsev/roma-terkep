# v85: „Jogállás és császári nevek időben” kártya. Adat: nm/calc.py -> nm/data.json; szöveg: src/nm_card.py
import json,shutil,sys
sys.path.insert(0,'src');import nm_card as NC
p='body_v60pre.html';b=open(p,encoding='utf8').read();cp='style_v60pre.css';c=open(cp,encoding='utf8').read()
assert 'nmcard' not in b and 'occcard' in b
shutil.copy(p,'src/body_v60pre_before_v85.html');shutil.copy(cp,'src/style_v60pre_before_v85.css')
def rep(s,a,x,n=1):
    assert s.count(a)==n,(a[:60],s.count(a));return s.replace(a,x)
D=NC.D
card,src,sub=NC.build('hu')
b=rep(b,'    <section class="card" id="bldcard">',card+'    <section class="card" id="bldcard">')
keys=[k for k,_,_ in NC.ST]+[k for k,_ in NC.NM]
js='''/* v85: jogállás és császári nevek időben (nm/data.json) */
const NMD='''+json.dumps({"bins":D['bins'],"w":D['w'],"tot":D['tot'],"time":{k:D['time'][k] for k in keys}},separators=(',',':'))+''';
var nmYear=null;
(function(){const card=document.getElementById("nmcard");if(!card)return;const NS="http://www.w3.org/2000/svg",loc=document.documentElement.lang==="en"?"en-US":"hu-HU";
  const B=NMD.bins,W=NMD.w,idx=B.map((_,i)=>i).filter(i=>NMD.tot[i]>=40&&B[i]>=-100&&B[i]<500),X0=B[idx[0]],X1=B[idx[idx.length-1]]+W;let yv=null;const charts=[];
  const mk=(n,a,p)=>{const e=document.createElementNS(NS,n);for(const k in a)e.setAttribute(k,a[k]);if(p)p.appendChild(e);return e;};
  const f1=v=>v.toLocaleString(loc,{maximumFractionDigits:v<10?1:0});
  card.querySelectorAll(".nmchart").forEach(box=>{const ks=box.dataset.k.split(","),cl=box.dataset.c,info=box.parentNode.querySelector("#"+box.id.replace("chart","info")),labs=[...box.parentNode.querySelectorAll("#"+box.id.replace("chart","leg")+" .il")].map(e=>e.textContent.replace(/ \\(.*\\)/,""));
    const sh=(k,i)=>100*NMD.time[k][i]/NMD.tot[i];
    function draw(){box.innerHTML="";const Wd=Math.max(320,Math.min(1600,box.clientWidth||660)),H=Wd<520?190:Math.min(400,Math.max(220,Math.round(Wd*0.27))),L=40,R=12,Tp=8,Bt=26;
      const s=mk("svg",{viewBox:`0 0 ${Wd} ${H}`,width:Wd,height:H,class:"bldsvg nmsvg"},box);
      const mx=Math.max(...ks.map(k=>Math.max(...idx.map(i=>sh(k,i)))))*1.08,sy=v=>Tp+(1-v/mx)*(H-Tp-Bt),xs=x=>L+(x-X0)/(X1-X0)*(Wd-L-R),step=[1,2,5,10,20].find(x=>mx/x<=6)||25;
      for(let v=0;v<=mx;v+=step){const y=sy(v);mk("line",{x1:L,x2:Wd-R,y1:y,y2:y,class:"pg"},s);const t=mk("text",{x:L-5,y:y+4,"text-anchor":"end",class:"pt"},s);t.textContent=v+"%";}
      (Wd<520?[-100,100,300,500]:[-100,0,100,200,300,400,500]).forEach(x=>{const t=mk("text",{x:xs(x),y:H-Bt+16,"text-anchor":x===-100?"start":x===500?"end":"middle",class:"pt"},s);t.textContent=x===0?"0":fmtY(x);});
      mk("line",{x1:L,x2:Wd-R,y1:H-Bt,y2:H-Bt,class:"pax"},s);
      ks.forEach(k=>{mk("path",{d:idx.map((i,j)=>(j?"L":"M")+xs(B[i]+W/2).toFixed(1)+","+sy(sh(k,i)).toFixed(1)).join(""),class:"nml "+cl+k},s);});
      const dots=mk("g",{},s);
      idx.forEach(i=>{const x=B[i],g0=mk("g",{class:"bb"},s);mk("rect",{x:xs(x),y:Tp,width:xs(x+W)-xs(x),height:H-Tp-Bt,class:"bhit"},g0);
        const show=()=>{s.querySelectorAll(".bb.on").forEach(e=>e.classList.remove("on"));g0.classList.add("on");dots.innerHTML="";ks.forEach(k=>mk("circle",{cx:xs(x+W/2),cy:sy(sh(k,i)),r:3.5,class:"nmd "+cl+k},dots));
          if(info)info.textContent=fmtY(x)+"–"+fmtY(x+W)+" · "+ks.map((k,j)=>labs[j]+": "+f1(sh(k,i))+"%").join("; ");};
        g0.addEventListener("mouseenter",show);g0.addEventListener("click",()=>{show();if(typeof setYear==="function")setYear(Math.max(-1000,Math.min(650,x+Math.round(W/2))));});});
      const yl=mk("line",{class:"py",y1:Tp,y2:H-Bt,x1:0,x2:0},s);yl.style.display="none";s._yl=yl;s._xs=xs;mark();}
    function mark(){const s=box.querySelector("svg");if(!s||!s._yl)return;const y=yv;if(y==null||y==="all"||y<X0||y>X1){s._yl.style.display="none";return;}const x=s._xs(+y);s._yl.setAttribute("x1",x);s._yl.setAttribute("x2",x);s._yl.style.display="";}
    charts.push(mark);draw();let lw=0;if(window.ResizeObserver)new ResizeObserver(()=>{const w=box.clientWidth;if(w&&Math.abs(w-lw)>4){lw=w;draw();}}).observe(box);});
  nmYear=function(y){yv=y;charts.forEach(f=>f());};
  card.querySelectorAll("[data-goto]").forEach(a=>a.addEventListener("click",e=>{e.preventDefault();goTo(a.dataset.goto);}));
  nmYear(state.year);})();
'''
b=rep(b,'/* v84: foglalkozások a feliratokon (occ/data.json) */',js+'/* v84: foglalkozások a feliratokon (occ/data.json) */')
b=rep(b,'if(occYear)occYear(y);}','if(occYear)occYear(y);if(nmYear)nmYear(y);}')
b=rep(b,'"Építkezések időrendben":"az','"Jogállás és császári nevek időben":"'+sub+'","Építkezések időrendben":"az')
b=rep(b,'      <li><b>Építkezések időrendben.</b>',src+'\n      <li><b>Építkezések időrendben.</b>')
c=rep(c,'</style>','''/* v85: jogállás és császári nevek időben */
#nmcard{--slib:#2f7fb8;--sser:#8a5a44;--sfil:#c9a227;--silib:#6b3fa0;--siser:#b79ad6;--niuli:#c0392b;--nclaudi:#e08a1e;--nflavi:#9a8f00;--nulpi:#3d7f6e;--naeli:#2f7fb8;--naureli:#6b3fa0;--ncoccei:#8c8c8c;--nseptimi:#5a5a5a}
#nmcard.open{grid-column:1/-1}
#nmcard .slib{background:var(--slib);stroke:var(--slib);fill:var(--slib)}#nmcard .sser{background:var(--sser);stroke:var(--sser);fill:var(--sser)}#nmcard .sfil{background:var(--sfil);stroke:var(--sfil);fill:var(--sfil)}#nmcard .silib{background:var(--silib);stroke:var(--silib);fill:var(--silib)}#nmcard .siser{background:var(--siser);stroke:var(--siser);fill:var(--siser)}
#nmcard .niuli{background:var(--niuli);stroke:var(--niuli);fill:var(--niuli)}#nmcard .nclaudi{background:var(--nclaudi);stroke:var(--nclaudi);fill:var(--nclaudi)}#nmcard .nflavi{background:var(--nflavi);stroke:var(--nflavi);fill:var(--nflavi)}#nmcard .nulpi{background:var(--nulpi);stroke:var(--nulpi);fill:var(--nulpi)}#nmcard .naeli{background:var(--naeli);stroke:var(--naeli);fill:var(--naeli)}#nmcard .naureli{background:var(--naureli);stroke:var(--naureli);fill:var(--naureli)}#nmcard .ncoccei{background:var(--ncoccei)}#nmcard .nseptimi{background:var(--nseptimi)}
#nmcard .nmsvg path.nml{fill:none;stroke-width:2.2;stroke-linejoin:round;stroke-linecap:round}
#nmcard .nmsvg circle.nmd{stroke:var(--sheet);stroke-width:1.5}
.nmtab td .ik{margin-left:0;margin-right:4px}
</style>''')
open(p,'w',encoding='utf8').write(b);open(cp,'w',encoding='utf8').write(c);print('ok')
