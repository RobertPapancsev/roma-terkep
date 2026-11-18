# v74: „Róma népessége – becslések és ókori számadatok” kártya: idővonal (modern becslések sávosan + ókori jogosulti számok külön jellel), táblázatok, módszertani megjegyzések.
# Nincs folytonos görbe: csak a szerzők saját becslései és az ókori számok szerepelnek.
import shutil
p='body_v60pre.html';b=open(p,encoding='utf8').read();cp='style_v60pre.css';c=open(cp,encoding='utf8').read()
assert 'popcard' not in b
shutil.copy(p,'src/body_v60pre_before_v74.html');shutil.copy(cp,'src/style_v60pre_before_v74.css')
def rep(s,a,x,n=1):
    assert s.count(a)==n,(a[:60],s.count(a));return s.replace(a,x)
E=[ # id, Időpont, Becslés, Kutató, Megjegyzés
("beard","Kr. e. 510 körül, a királyság végén","20 000–30 000","M. Beard 2015",""),
("hop09","Kr. e. 225","kb. 150 000","K. Hopkins 2009",""),
("man1","Kr. e. 225 körül","kb. 200 000","M. J. Mandich 2016","„városi skálázás”: a város népessége és mérete közti, más városokon megfigyelt összefüggésből"),
("sch","Kr. e. 28","800 000–1 000 000","W. Scheidel 2007",""),
("hop78","Kr. e. 1. század vége","800 000–1 000 000","K. Hopkins 1978",""),
("brunt","Augustus kora","kb. 750 000","P. A. Brunt 1971",""),
("mor","Augustus kora","kb. 1 000 000","N. Morley 1996",""),
("man2","Kr. e. 2","kb. 1 000 000 (alacsony változat: 750 000)","M. J. Mandich 2016",""),
("sto","Császárkor","kb. 450 000","G. R. Storey 1997","a népsűrűségből: Pompeji és Ostia feltárt háztömbjeinek lakósűrűségét vetíti Rómára"),
("sal1","4. század eleje","700 000–1 000 000","M. R. Salzman 2021",""),
("lan1","4. század","700 000–900 000","B. Lançon 2000",""),
("kra1","400 körül","kb. 800 000","R. Krautheimer 1980",""),
("lan2","408, a gót ostromok előtt","kb. 800 000","B. Lançon 2000",""),
("lan3","419","kb. 500 000","B. Lançon 2000",""),
("rus","419 körül","kb. 58 000","J. C. Russell 1958","a többi becsléstől nagyon eltér"),
("dur1","5. század","kb. 350 000","J. Durliat 1990",""),
("kra2","452","kb. 500 000","R. Krautheimer 1980",""),
("sal2","5. század közepe","300 000–500 000","M. R. Salzman 2021",""),
("kra3","500 körül","kb. 100 000","R. Krautheimer 1980",""),
("dur2","6. század","kb. 60 000","J. Durliat 1990",""),
("kra4","552 után","kb. 30 000","R. Krautheimer 1980",""),
]
A=[ # id, Időpont, Szám, Mit számol, Forrás
("suet","Kr. e. 46","320 000 → 150 000","az ingyenes gabonára jogosultak Caesar felülvizsgálata előtt és után","Suetonius, <i>Divus Iulius</i> 41.3"),
("rg1","Kr. e. 12","legalább 250 000","Augustus pénzajándékát (<i>congiarium</i>) kapott polgárok","<i>Res gestae</i> 15"),
("rg2","Kr. e. 5","320 000","a városi plebs, amely Augustus pénzajándékát kapta","<i>Res gestae</i> 15"),
("rg3","Kr. e. 2","valamivel több mint 200 000","az állami gabonát kapó polgárok","<i>Res gestae</i> 15"),
("dio","Kr. u. 202","kb. 200 000","a gabonajogosultak és a praetoriánusok együtt: Septimius Severus fejenként 10 aureust adott, összesen 50 millió dénárt, a fejszám ebből számolható","Cassius Dio 76(77).1"),
("jon","5. század közepe","kb. 120 000","ingyenes kenyérre és sertéshúsra jogosultak, többnyire családfők","A. H. M. Jones 1966"),
("pro1","546","legfeljebb 500","ennyi ember maradt a városban, amikor Totila bevonult","Prokopiosz, <i>A gót háború</i> (<i>Hist.</i> 7.20.19)"),
("pro2","547","0","Totila elvonulásakor a város lakatlanul maradt","Prokopiosz, <i>Hist.</i> 7.22.19"),
]
def rows(L,anc=False):
    o=[]
    for r in L:
        if anc:o.append(f'          <tr data-p="{r[0]}"><td>{r[1]}</td><td class="pn">{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td></tr>')
        else:o.append(f'          <tr data-p="{r[0]}"><td>{r[1]}</td><td class="pn">{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td></tr>')
    return '\n'.join(o)
card='''    <section class="card" id="popcard">
      <h2>Róma népessége</h2>
      <p class="hint">Róma lakosságáról nem maradt fenn népszámlálási adat. Az ókori források csak egyes csoportokat számolnak meg, főleg az ingyenes gabonára vagy pénzajándékra jogosult felnőtt férfi polgárokat. A teljes népességet a modern kutatók ezekből és más közvetett jelekből becsülik, ezért az alábbi számok becslések, nem adatok. Ugyanarra az időszakra is akár kétszeres különbség van közöttük.</p>
      <div class="seg popsel" role="group" aria-label="Skála"><button data-s="lin" aria-pressed="true">Lineáris skála</button><button data-s="log" aria-pressed="false">Logaritmikus skála</button></div>
      <div class="popchart" id="popchart"></div>
      <p class="hint popleg"><span class="pk e"></span> modern becslés (pont: egy szám, függőleges sáv: tartomány) · <span class="pk a"></span> ókori számadat egy csoportról, nem a teljes népesség · <span class="pk y"></span> a térkép évcsúszkáján beállított év</p>
      <p class="hint popinfo" id="popinfo">Vidd az egeret egy jelre, vagy kattints egy táblázatsorra.</p>
      <p class="hint">A pontokat szándékosan nem köti össze vonal: a becslések közötti évekre nincs adat, egy görbe ezt kitalálná. A két legnagyobb bizonytalanság: mekkora volt a város a köztársaság közepén, és milyen gyorsan fogyott az 5–6. században.</p>
      <h3 class="aqh">Modern becslések</h3>
      <div class="regwrap"><table class="regtab poptab">
        <thead><tr><th>Időpont</th><th>Becslés (lakos)</th><th>Kutató</th><th>Megjegyzés</th></tr></thead>
        <tbody>
'''+rows(E)+'''
        </tbody>
      </table></div>
      <h3 class="aqh">Ókori számadatok</h3>
      <div class="regwrap"><table class="regtab poptab">
        <thead><tr><th>Időpont</th><th>Szám</th><th>Kiket számol</th><th>Forrás</th></tr></thead>
        <tbody>
'''+rows(A,True)+'''
        </tbody>
      </table></div>
      <h3 class="aqh">Miért térnek el a becslések?</h3>
      <p class="hint"><b>A gabonaosztás szorzója.</b> A jogosultak száma (Augustus alatt kb. 200 000) csak a felnőtt férfi polgárokat számolja. A teljes népességhez hozzá kell számolni a nőket, a gyerekeket, a rabszolgákat, a nem polgár idegeneket, a katonákat és az előkelőket. Ezek arányára nincs ókori adat, ezért már a szorzó megválasztása is százezres eltéréseket okoz. Ebből az útból adódik a gyakran idézett, kb. egymilliós szám.</p>
      <p class="hint"><b>A népsűrűség.</b> Storey (1997) szerint egymillió lakos az ókori város 13,86 km²-es területén négyzetkilométerenként 72 150 főt jelentene, ami a mai Hongkong legsűrűbb részeihez hasonló. Pompeji és Ostia feltárt háztömbjeinek sűrűségéből jóval kisebb, kb. 450 000-es népesség adódik.</p>
      <p class="hint"><b>Az épületszám.</b> A 4. századi kerületjegyzék 46 602 bérházat (<i>insula</i>) és 1790 családi házat (<i>domus</i>) sorol fel (lásd „A 14 kerület számokban”). Ha az <i>insula</i> egész épületet jelent, az nagy népességre utal; ha csak lakást vagy telekegységet, akkor sokkal kisebbre. A szó jelentése vitatott, ezért a számból nem lehet lakosságot számolni.</p>
      <p class="hint"><b>A késő ókor.</b> Az 5. század ostromai (410, 455, 472) és a 6. századi gót háború idején a becslések között a legnagyobb a szórás: a kutatók ugyanazt a néhány adatot (a hús- és kenyérosztás jogosultjait, Prokopiosz leírását) eltérő módon értelmezik.</p>
    </section>
'''
b=rep(b,'    <details class="notwrap" id="notwrap">',card+'    <details class="notwrap" id="notwrap">')
js='''/* v74: Róma népessége. POP: modern becslések (lo–hi), POPA: ókori számadatok (v, v2 = érték változás után). Az x a diagramon elhelyezés éve (évszázados dátumoknál a század közepe). */
const POP=[{i:"beard",g:"beard",a:"Beard 2015",x:-510,lo:20000,hi:30000},{i:"hop09",g:"hop09",a:"Hopkins 2009",x:-232,lo:150000},{i:"man1",g:"man",a:"Mandich 2016",x:-218,lo:200000},
 {i:"sch",g:"sch",a:"Scheidel 2007",x:-28,lo:800000,hi:1000000},{i:"hop78",g:"hop78",a:"Hopkins 1978",x:-18,lo:800000,hi:1000000},{i:"brunt",g:"brunt",a:"Brunt 1971",x:-10,lo:750000},
 {i:"mor",g:"mor",a:"Morley 1996",x:-6,lo:1000000},{i:"man2",g:"man",a:"Mandich 2016",x:2,lo:1000000},{i:"sto",g:"sto",a:"Storey 1997",x:150,lo:450000},
 {i:"sal1",g:"sal",a:"Salzman 2021",x:315,lo:700000,hi:1000000},{i:"lan1",g:"lan",a:"Lançon 2000",x:350,lo:700000,hi:900000},{i:"kra1",g:"kra",a:"Krautheimer 1980",x:400,lo:800000},
 {i:"lan2",g:"lan",a:"Lançon 2000",x:408,lo:800000},{i:"lan3",g:"lan",a:"Lançon 2000",x:419,lo:500000},{i:"rus",g:"rus",a:"Russell 1958",x:421,lo:58000},
 {i:"dur1",g:"dur",a:"Durliat 1990",x:440,lo:350000},{i:"kra2",g:"kra",a:"Krautheimer 1980",x:452,lo:500000},{i:"sal2",g:"sal",a:"Salzman 2021",x:460,lo:300000,hi:500000},
 {i:"kra3",g:"kra",a:"Krautheimer 1980",x:500,lo:100000},{i:"dur2",g:"dur",a:"Durliat 1990",x:545,lo:60000},{i:"kra4",g:"kra",a:"Krautheimer 1980",x:560,lo:30000}];
const POPA=[{i:"suet",x:-46,v:320000,v2:150000},{i:"rg1",x:-12,v:250000},{i:"rg2",x:-5,v:320000},{i:"rg3",x:-2,v:200000},{i:"dio",x:202,v:200000},{i:"jon",x:450,v:120000},{i:"pro1",x:546,v:500},{i:"pro2",x:547,v:0}];
var popYear=null;
(function(){const box=document.getElementById("popchart");if(!box)return;const NS="http://www.w3.org/2000/svg",loc=document.documentElement.lang==="en"?"en-US":"hu-HU";
  let W=660,H=300;const L=62,R=34,T=12,B=30,X0=-600,X1=600;let mode="lin",yv=null,sel=null,lastW=0;
  const sx=x=>L+(x-X0)/(X1-X0)*(W-L-R);
  const sy=v=>{if(mode==="lin")return T+(1-v/1100000)*(H-T-B);const lv=Math.log10(Math.max(v,100));return T+(1-(lv-2)/(Math.log10(2000000)-2))*(H-T-B);};
  const mk=(n,a,p)=>{const e=document.createElementNS(NS,n);for(const k in a)e.setAttribute(k,a[k]);if(p)p.appendChild(e);return e;};
  const info=document.getElementById("popinfo"),rows={};document.querySelectorAll(".poptab tr[data-p]").forEach(r=>rows[r.dataset.p]=r);
  function show(id){sel=id;Object.values(rows).forEach(r=>r.classList.toggle("on",r.dataset.p===id));box.querySelectorAll("[data-p]").forEach(e=>e.classList.toggle("on",e.dataset.p===id));
    const r=rows[id];if(r&&info){const c=r.cells;info.textContent=c[2].textContent+": "+c[1].textContent+" ("+c[0].textContent+")";}}
  function draw(){W=Math.max(320,Math.min(900,box.clientWidth||660));H=W<520?240:300;box.innerHTML="";const s=mk("svg",{viewBox:`0 0 ${W} ${H}`,width:W,height:H,class:"popsvg",role:"img"},box);
    const ticks=mode==="lin"?[0,200000,400000,600000,800000,1000000]:[100,1000,10000,100000,1000000];
    ticks.forEach(v=>{const y=sy(v);mk("line",{x1:L,x2:W-R,y1:y,y2:y,class:"pg"},s);const t=mk("text",{x:L-6,y:y+4,"text-anchor":"end",class:"pt"},s);t.textContent=v.toLocaleString(loc);});
    for(let x=X0;x<=X1;x+=(W<520?400:200)){const xx=sx(x);mk("line",{x1:xx,x2:xx,y1:T,y2:H-B,class:"pg"},s);const t=mk("text",{x:xx,y:H-B+16,"text-anchor":"middle",class:"pt"},s);t.textContent=x===0?"0":fmtY(x);}
    mk("line",{x1:L,x2:W-R,y1:H-B,y2:H-B,class:"pax"},s);
    POPA.forEach(p=>{const g=mk("g",{class:"pa","data-p":p.i},s),x=sx(p.x),y=sy(p.v);
      if(p.v2!=null){const y2=sy(p.v2);mk("line",{x1:x,x2:x,y1:y+5,y2:y2-6,class:"parr"},g);mk("path",{d:`M${x-3.5},${y2-8}L${x},${y2-3}L${x+3.5},${y2-8}`,class:"parr"},g);mk("path",{d:`M${x},${y2-5}l5,5l-5,5l-5,-5z`,class:"pd"},g);}
      mk("path",{d:`M${x},${y-5}l5,5l-5,5l-5,-5z`,class:"pd"},g);});
    POP.forEach(p=>{const g=mk("g",{class:"pe","data-p":p.i},s),x=sx(p.x);
      if(p.hi){const y1=sy(p.hi),y2=sy(p.lo);mk("rect",{x:x-3,y:y1,width:6,height:Math.max(6,y2-y1),rx:3,class:"pb"},g);}
      else mk("circle",{cx:x,cy:sy(p.lo),r:4,class:"pc"},g);});
    const yl=mk("line",{class:"py",y1:T,y2:H-B,x1:0,x2:0},s);yl.style.display="none";s._yl=yl;
    s.querySelectorAll("[data-p]").forEach(e=>{e.addEventListener("mouseenter",()=>show(e.dataset.p));e.addEventListener("click",()=>show(e.dataset.p));});
    if(sel)show(sel);popYear(yv);}
  popYear=function(y){yv=y;const s=box.querySelector("svg");if(!s||!s._yl)return;const yl=s._yl;if(y==null||y==="all"||y<X0||y>X1){yl.style.display="none";return;}
    const x=sx(+y);yl.setAttribute("x1",x);yl.setAttribute("x2",x);yl.style.display="";};
  Object.values(rows).forEach(r=>r.addEventListener("click",()=>show(r.dataset.p)));
  const bs=[...document.querySelectorAll(".popsel button")];bs.forEach(bt=>bt.addEventListener("click",()=>{mode=bt.dataset.s;bs.forEach(x=>x.setAttribute("aria-pressed",String(x===bt)));draw();}));
  draw();popYear(state.year);if(window.ResizeObserver)new ResizeObserver(()=>{const w=box.clientWidth;if(w&&Math.abs(w-lastW)>4){lastW=w;draw();}}).observe(box);})();
'''
b=rep(b,'/* Ugrás: legördülő menü a (rejtett) gombokból */',js+'/* Ugrás: legördülő menü a (rejtett) gombokból */')
b=rep(b,'if(y!=="all")yr.value=y;apply();}','if(y!=="all")yr.value=y;apply();if(popYear)popYear(y);}')
b=rep(b,'"A 14 kerület számokban":"bérházak','"Róma népessége":"becslések Kr. e. 510-től a 6. századig, 12 kutatótól, és az ókori számadatok","A 14 kerület számokban":"bérházak')
src='''      <li><b>Róma népessége.</b> Modern becslések: M. Beard, <i>SPQR: A History of Ancient Rome</i>, London 2015; K. Hopkins, „The political economy of the Roman empire”, in: I. Morris – W. Scheidel (szerk.), <i>The Dynamics of Ancient Empires</i>, Oxford 2009; M. J. Mandich, „Urban Scaling and the Growth of Rome”, <i>TRAC 2015</i> (2016); W. Scheidel, „Demography”, in: <i>The Cambridge Economic History of the Greco-Roman World</i>, Cambridge 2007; K. Hopkins, <i>Conquerors and Slaves</i>, Cambridge 1978; P. A. Brunt, <i>Italian Manpower 225 B.C.–A.D. 14</i>, Oxford 1971; N. Morley, <i>Metropolis and Hinterland</i>, Cambridge 1996, 182. o.; G. R. Storey, „The population of ancient Rome”, <i>Antiquity</i> 71 (1997) 966–978; B. Lançon, <i>Rome in Late Antiquity</i>, Edinburgh 2000; R. Krautheimer, <i>Rome: Profile of a City, 312–1308</i>, Princeton 1980; J. Durliat, <i>De la ville antique à la ville byzantine: le problème des subsistances</i>, Róma 1990; J. C. Russell, <i>Late Ancient and Medieval Population</i>, Philadelphia 1958; M. R. Salzman, <i>The Falls of Rome</i>, Cambridge 2021; A. H. M. Jones, <i>The Decline of the Ancient World</i>, London 1966. Ókori adatok: Suetonius, <i>Divus Iulius</i> 41.3; <i>Res gestae divi Augusti</i> 15; Cassius Dio 76(77).1; Prokopiosz, <i>Hist.</i> 7.20.19 és 7.22.19.</li>
      <li><b>A séták vonala.</b>'''
b=rep(b,'      <li><b>A séták vonala.</b>',src)
c=rep(c,'</style>','''/* v74: Róma népessége */
#popcard{--pe:#1f5fa8;--pa:#b5651d;--py:#c0392b}
:root[data-theme="dark"] #popcard{--pe:#79aec6;--pa:#e0a060;--py:#e57c86}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) #popcard{--pe:#79aec6;--pa:#e0a060;--py:#e57c86}}
#popcard.open{grid-column:1/-1}
.popchart{margin:8px 0}
.popsvg{width:100%;height:auto;display:block;font-family:var(--font-mono,monospace);overflow:visible}
.popsvg .pg{stroke:var(--line);stroke-width:.6;stroke-dasharray:2 3}
.popsvg .pax{stroke:var(--muted);stroke-width:1}
.popsvg .pt{fill:var(--muted);font-size:11px}
.popsvg .pl{fill:none;stroke:var(--pe);stroke-opacity:.3;stroke-width:1}
.popsvg .pb{fill:var(--pe);fill-opacity:.55;stroke:var(--pe);stroke-width:1}
.popsvg .pc{fill:var(--pe);stroke:var(--sheet,#fff);stroke-width:1}
.popsvg .pd{fill:var(--sheet,#fff);stroke:var(--pa);stroke-width:1.8}
.popsvg .parr{fill:none;stroke:var(--pa);stroke-width:1.2}
.popsvg .py{stroke:var(--py);stroke-width:1.5;stroke-dasharray:4 3}
.popsvg [data-p]{cursor:pointer}
.popsvg .pe.on .pb,.popsvg .pe.on .pc{stroke:var(--ink);stroke-width:2.5}
.popsvg .pa.on .pd{fill:var(--pa)}
.popleg .pk{display:inline-block;width:10px;height:10px;margin:0 3px 0 6px;vertical-align:middle}
.popleg .pk.e{background:var(--pe);border-radius:50%}
.popleg .pk.a{border:1.8px solid var(--pa);transform:rotate(45deg) scale(.8)}
.popleg .pk.y{width:2px;height:12px;background:var(--py)}
.popinfo{min-height:1.4em;font-weight:600;color:var(--ink)}
.poptab td{white-space:normal;text-align:left;vertical-align:top}
.poptab td.pn{white-space:nowrap;text-align:right}
.poptab th{text-align:left}
.poptab tr[data-p]{cursor:pointer}
.poptab tr.on{background:rgba(31,95,168,.12)}
</style>''')
open(p,'w',encoding='utf8').write(b);open(cp,'w',encoding='utf8').write(c);print('ok')
