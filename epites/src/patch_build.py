# v79: „Építkezések időrendben” kártya – az építési aktivitás a térkép saját adataiból: (1) a SITAR ásatási egységek építési fázisai (aoristikus összegzés, 25 éves sávok), (2) a térkép elemeinek építési éve. Adat: bld/calc.py -> bld/data.json
import json,shutil
p='body_v60pre.html';b=open(p,encoding='utf8').read();cp='style_v60pre.css';c=open(cp,encoding='utf8').read()
assert 'bldcard' not in b
shutil.copy(p,'src/body_v60pre_before_v79.html');shutil.copy(cp,'src/style_v60pre_before_v79.css')
def rep(s,a,x,n=1):
    assert s.count(a)==n,(a[:60],s.count(a));return s.replace(a,x)
D=json.load(open('bld/data.json'))
S=D['sitar'];M=D['map']
G1=[('house','lakóépületek'),('water','vízvezeték, csatorna, kút'),('cult','szentélyek, templomok'),('tomb','sírok'),('public','középületek, szórakozóhelyek'),('trade','műhelyek, raktárak, kikötő'),('infra','utak, falak, katonai építmények'),('other','azonosítatlan funkció')]
G2=[('temple','templomok, szentélyek'),('church','keresztény templomok'),('house','lakóházak, paloták'),('bath','fürdők'),('aqua','vízvezetékek, kutak'),('gate','kapuk, falak'),('tomb','sírok'),('other','egyéb (fórumok, bazilikák, színházak, utak stb.)')]
leg=lambda G,cls:' · '.join(f'<span class="bk {cls}{k}" data-g="{k}"></span> <span class="bl" data-g="{k}">{t}</span>' for k,t in G)
card='''    <section class="card" id="bldcard">
      <h2>Építkezések időrendben</h2>
      <p class="hint">Mikor építkeztek a legtöbbet Rómában? Pontos kimutatás erről nincs, de a térkép két saját adatsorából közelítőleg kiolvasható. Egyik sem teljes: csak azt mutatják, amit feltártak, illetve amit a térképre felvettünk.</p>
      <h3 class="aqh">1. Az ásatások építési fázisai</h3>
      <p class="hint">A római régészeti nyilvántartás (SITAR) a térkép területén '''+f'{S["nEntries"]}'+''' olyan építési fázist rögzít, amelynek az ásatók megadták a keltezését (fal, alapozás, padló; a modern rétegek nélkül); ebből '''+f'{S["nAll"]}'+''' esik Kr. e. 800 és Kr. u. 800 közé. A keltezés legtöbbször időszak, például „Kr. u. 1. század”. Ilyenkor az egység súlyát egyenletesen elosztjuk az időszak 25 éves sávjai között; így minden egység összesen egyet számít (aoristikus módszer). A „pontosabban keltezett” nézet csak azokat mutatja, amelyeknek a keltezése legfeljebb 100 évet fog át.</p>
      <div class="seg bldsel" role="group" aria-label="Keltezés pontossága"><button data-m="all" aria-pressed="true">Minden keltezett fázis ('''+f'{S["nAll"]}'+''')</button><button data-m="tight" aria-pressed="false" title="Csak azok, amelyeknek a keltezése legfeljebb 100 évet fog át (pl. Kr. u. 50–150). A tágabb, például „Kr. u. 1–3. század” keltezések kimaradnak.">Csak a pontosabban keltezett fázisok ('''+f'{S["nTight"]}'+''')</button></div>
      <div class="bldchart" id="bldchart1"></div>
      <p class="hint bldleg">'''+leg(G1,'s')+'''</p>
      <h3 class="aqh">2. A térkép épületei</h3>
      <p class="hint">A térkép '''+f'{M["n"]}'+''' elemének építési éve (az első építés, nem az újjáépítések), 25 éves sávokban, a térkép funkció-szűrőjének csoportjai szerint.</p>
      <div class="bldchart" id="bldchart2"></div>
      <p class="hint bldleg">'''+leg(G2,'m')+'''</p>
      <p class="hint popinfo" id="bldinfo">Vidd az egeret egy oszlopra; kattintásra a térkép évcsúszkája arra az időre áll.</p>
      <p class="hint">Mindkét adatsorban a Kr. u. 50 és 125 közötti időszak a legerősebb: az ásatási adatokban a Kr. u. 75–100 közötti sáv a legmagasabb, a térkép épületeinél a Kr. u. 100–125 közötti, közvetlenül utána a 75–100 közötti. A második csúcs mindkettőben Augustus kora (Kr. e. 50 – Kr. u. 1). Az ásatási adatokban a 2. század is erős, a 3. század közepétől erősen csökkennek. A térkép épületeinél kisebb csúcsok jelzik a Severus-kort (Kr. u. 200–225) és a 3–4. század fordulóját (Aurelianus-fal, Diocletianus fürdői, Constantinus építkezései).</p>
      <p class="hint"><b>Korlátok.</b> Az ásatási adatok ott sűrűek, ahol sokat ástak (a Fórumon, a Palatinuson, a mai építkezések helyén), és a rétegek keltezése sokszor csak évszázadnyi pontosságú. A nagy császárkori épületek alapozásai a korábbi rétegeket gyakran elpusztították, ezért a korai korszakok alulreprezentáltak. A térkép elemeit mi válogattuk: kb. a felük az ókori forrásokban említett, nevesített épület, ami a középületeknek kedvez. A számok tehát arányokat és csúcsokat mutatnak, nem az összes építkezést.</p>
    </section>
'''
b=rep(b,'    <section class="card" id="popcard">',card+'    <section class="card" id="popcard">')
js='''/* v79: építkezések időrendben (bld/data.json) */
const BLD='''+json.dumps(D,separators=(',',':'))+''';
var bldYear=null;
(function(){const b1=document.getElementById("bldchart1"),b2=document.getElementById("bldchart2");if(!b1)return;const NS="http://www.w3.org/2000/svg",loc=document.documentElement.lang==="en"?"en-US":"hu-HU";
  const G1=["house","water","cult","tomb","public","trade","infra","other"],G2=["temple","church","house","bath","aqua","gate","tomb","other"],B=BLD.bins,W=BLD.w;let mode="all",yv=null;
  const lab=(cls,g)=>{const e=document.querySelector("#bldcard .bldleg .bk."+cls+g);return e&&e.nextElementSibling?e.nextElementSibling.textContent:g;};
  const mk=(n,a,p)=>{const e=document.createElementNS(NS,n);for(const k in a)e.setAttribute(k,a[k]);if(p)p.appendChild(e);return e;};
  const info=document.getElementById("bldinfo"),f1=v=>v.toLocaleString(loc,{maximumFractionDigits:1});
  function draw(box,S,G,cls,dec){box.innerHTML="";const Wd=Math.max(320,Math.min(900,box.clientWidth||660)),H=Wd<520?180:220,L=40,R=10,T=8,Bt=26;
    const s=mk("svg",{viewBox:`0 0 ${Wd} ${H}`,width:Wd,height:H,class:"bldsvg"},box);const n=B.length,bw=(Wd-L-R)/n;
    const tot=B.map((_,k)=>G.reduce((a,g)=>a+S[g][k],0)),mx=Math.max(...tot)*1.05||1;const sy=v=>T+(1-v/mx)*(H-T-Bt);
    const step=mx>80?20:mx>40?10:5;for(let v=0;v<=mx;v+=step){const y=sy(v);mk("line",{x1:L,x2:Wd-R,y1:y,y2:y,class:"pg"},s);const t=mk("text",{x:L-5,y:y+4,"text-anchor":"end",class:"pt"},s);t.textContent=v.toLocaleString(loc);}
    const xs=x=>L+(x-B[0])/W*bw;(Wd>900?[-800,-600,-400,-200,0,200,400,600,800]:[-800,-400,0,400,800]).forEach(x=>{if(Wd<520&&(x===-400||x===400))return;const t=mk("text",{x:Math.min(Wd-R,Math.max(L,xs(x))),y:H-Bt+16,"text-anchor":x===-800?"start":x===800?"end":"middle",class:"pt"},s);t.textContent=x===0?"0":fmtY(x);});
    mk("line",{x1:L,x2:Wd-R,y1:H-Bt,y2:H-Bt,class:"pax"},s);
    B.forEach((x,k)=>{const g0=mk("g",{class:"bb","data-k":k},s);let acc=0;G.forEach(g=>{const v=S[g][k];if(v<=0)return;const y1=sy(acc+v),y0=sy(acc);mk("rect",{x:xs(x)+0.5,y:y1,width:Math.max(1,bw-1),height:Math.max(0,y0-y1),class:"bk "+cls+g},g0);acc+=v;});
      mk("rect",{x:xs(x),y:T,width:bw,height:H-T-Bt,class:"bhit"},g0);
      const show=()=>{s.querySelectorAll(".bb.on").forEach(e=>e.classList.remove("on"));g0.classList.add("on");if(!info)return;const parts=G.filter(g=>S[g][k]>0.05).map(g=>lab(cls,g)+": "+(dec?f1(S[g][k]):S[g][k]));info.textContent=(x<0&&x+W>0?fmtY(x)+"–"+fmtY(x+W):fmtY(x)+"–"+fmtY(x+W))+" · "+(dec?f1(tot[k]):tot[k])+(parts.length?" ("+parts.join("; ")+")":"");};
      g0.addEventListener("mouseenter",show);g0.addEventListener("click",()=>{show();const y=Math.max(-1000,Math.min(650,x+Math.round(W/2)));if(typeof setYear==="function")setYear(y);});});
    const yl=mk("line",{class:"py",y1:T,y2:H-Bt,x1:0,x2:0},s);yl.style.display="none";s._yl=yl;s._xs=xs;}
  function drawAll(){draw(b1,BLD.sitar[mode],G1,"s",true);draw(b2,BLD.map.c,G2,"m",false);bldYear(yv);}
  bldYear=function(y){yv=y;[b1,b2].forEach(bx=>{const s=bx.querySelector("svg");if(!s||!s._yl)return;if(y==null||y==="all"||y<B[0]||y>B[B.length-1]+W){s._yl.style.display="none";return;}const x=s._xs(+y);s._yl.setAttribute("x1",x);s._yl.setAttribute("x2",x);s._yl.style.display="";});};
  const bs=[...document.querySelectorAll(".bldsel button")];bs.forEach(bt=>bt.addEventListener("click",()=>{mode=bt.dataset.m;bs.forEach(x=>x.setAttribute("aria-pressed",String(x===bt)));drawAll();}));
  drawAll();bldYear(state.year);let lw=0;if(window.ResizeObserver)new ResizeObserver(()=>{const w=b1.clientWidth;if(w&&Math.abs(w-lw)>4){lw=w;drawAll();}}).observe(b1);})();
'''
b=rep(b,'/* Ugrás: legördülő menü a (rejtett) gombokból */',js+'/* Ugrás: legördülő menü a (rejtett) gombokból */')
b=rep(b,'if(popYear)popYear(y);}','if(popYear)popYear(y);if(bldYear)bldYear(y);}')
b=rep(b,'"Róma élelmezése":"gabona','"Építkezések időrendben":"az ásatások építési fázisai és a térkép épületei 25 éves sávokban","Róma élelmezése":"gabona')
src='''      <li><b>Építkezések időrendben.</b> A térkép saját adatai: a SITAR ásatási egységeinek „cronologia di impianto/fondazione” bejegyzései (SITAR – Sistema Informativo Territoriale Archeologico di Roma, <a href="https://www.archeositarproject.it/">archeositarproject.it</a>), valamint a térkép elemeinek építési éve. Az időszakra keltezett egységek elosztása az aoristikus módszert követi (J. H. Ratcliffe, „Aoristic analysis: the spatial interpretation of unspecific temporal events”, <i>International Journal of Geographical Information Science</i> 14 (2000) 669–679).</li>
      <li><b>Róma élelmezése.</b>'''
b=rep(b,'      <li><b>Róma élelmezése.</b>',src)
c=rep(c,'</style>','''/* v79: építkezések időrendben */
#bldcard{--b1:#b5651d;--b2:#2f7fb8;--b3:#7a4e9c;--b4:#5b5b5b;--b5:#c9a227;--b6:#6d7f2a;--b7:#a23b3b;--b8:#b9c0c4;--b9:#d07aa8;--b10:#2aa198}
#bldcard.open{grid-column:1/-1}
.bldchart{margin:6px 0}
.bldsvg{width:100%;height:auto;display:block;font-family:var(--font-mono,monospace)}
.bldsvg .pg{stroke:var(--line);stroke-width:.6;stroke-dasharray:2 3}.bldsvg .pax{stroke:var(--muted);stroke-width:1}.bldsvg .pt{fill:var(--muted);font-size:10px}
.bldsvg .bhit{fill:transparent;cursor:pointer}.bldsvg .bb.on .bhit{fill:rgba(0,0,0,.06)}
.bldsvg .py{stroke:#c0392b;stroke-width:1.5;stroke-dasharray:4 3;pointer-events:none}
.bk.shouse,.bk.mhouse{fill:var(--b1);background:var(--b1)}.bk.swater,.bk.maqua{fill:var(--b2);background:var(--b2)}.bk.scult,.bk.mtemple{fill:var(--b3);background:var(--b3)}
.bk.stomb,.bk.mtomb{fill:var(--b4);background:var(--b4)}.bk.spublic{fill:var(--b5);background:var(--b5)}.bk.strade{fill:var(--b6);background:var(--b6)}
.bk.sinfra,.bk.mgate{fill:var(--b7);background:var(--b7)}.bk.sother,.bk.mother{fill:var(--b8);background:var(--b8)}.bk.mchurch{fill:var(--b9);background:var(--b9)}.bk.mbath{fill:var(--b10);background:var(--b10)}
.bldleg span.bk{display:inline-block;width:11px;height:11px;border-radius:2px;vertical-align:middle;margin-left:4px}
</style>''')
open(p,'w',encoding='utf8').write(b);open(cp,'w',encoding='utf8').write(c);print('ok')
