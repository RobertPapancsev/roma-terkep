# v82: „Feliratok” kártya – az EDR római feliratai: időgörbe típusonként (aoristikus), a legnagyobb lelőhelyek táblázata, sírfeliratok az utak mentén. Adat: insc/calc.py -> insc/data.json
import json,shutil
p='body_v60pre.html';b=open(p,encoding='utf8').read();cp='style_v60pre.css';c=open(cp,encoding='utf8').read()
assert 'insccard' not in b
shutil.copy(p,'src/body_v60pre_before_v82.html');shutil.copy(cp,'src/style_v60pre_before_v82.css')
def rep(s,a,x,n=1):
    assert s.count(a)==n,(a[:60],s.count(a));return s.replace(a,x)
D=json.load(open('insc/data.json'))
fmt=lambda n:f'{n:,}'.replace(',',' ')
def yr(y):
    if y is None:return '–'
    return f'Kr. e. {-y}' if y<0 else f'Kr. u. {y}'
TL=[('tomb','sírfeliratok'),('sacred','vallási feliratok'),('honor','tiszteletbeli feliratok'),('build','építési feliratok'),('other','egyéb és ismeretlen')]
leg=' · '.join(f'<span class="ik i{k}"></span> <span class="il">{t}</span>' for k,t in TL)
CXN={'salario':('A Salaria-temető','a via Salaria és a via Pinciana között; több lelőhely-leírás összevonva'),
 'codini':('A Vigna Codini kolumbáriumai','via Appia'),
 'forum':('Forum Romanum',''),
 'spaolo':('San Paolo fuori le mura és környéke','via Ostiensis'),
 'pamphilj':('Villa Pamphilj temetői','via Aurelia'),
 'liviae':('Livia szolgáinak és felszabadítottjainak kolumbáriuma (Monumentum Liviae)','via Appia'),
 'jrand':('A Vigna Randanini zsidó katakombája','via Appia'),
 'statili':('A Statiliusok kolumbáriuma','a Porta Maior mellett'),
 'vatican':('A vatikáni nekropolisz és a via Triumphalis menti temető',''),
 'colosseum':('Colosseum','főleg az aréna mellvédjének (podium) töredékei'),
 'carmel':("A Corso d'Italia, a karmelita templom környéke",'a Salaria-temető része'),
 'callisto':('Callistus katakombái','via Appia'),
 'jmonte':('A monteverdei zsidó katakomba','via Portuensis'),
 'equites':('A császári lovastestőrség (equites singulares) temetője','via Labicana, a SS. Marcellino e Pietro katakombánál'),
 'volusii':('A Volusiusok síremléke','via Appia'),
 'paedag':('Paedagogium','falfirkák az épület falain'),
 'domitilla':('Domitilla katakombái','via Ardeatina'),
 'pretestato':('Praetextatus katakombái','via Appia'),
 'priscilla':('Priscilla katakombái','via Salaria'),
 'foraug':('Augustus fóruma',''),
 'jtorl':('A Villa Torlonia zsidó katakombái','via Nomentana'),
 'pacis':('Templum Pacis',''),
 'fortra':('Traianus fóruma',''),
 'argentina':('A Largo Argentina szent körzete','')}
tn=dict(TL)
rows=[]
for k,v in sorted(D['cx'].items(),key=lambda x:-x[1]['n']):
    nm,sub=CXN[k];tt=max(v['t'],key=lambda t:v['t'][t]);sh=round(100*v['t'][tt]/v['n'])
    import math
    lo=math.floor(v['q1']/25)*25;hi=math.ceil(v['q3']/25)*25
    if hi==lo:hi+=25
    per=f'{yr(lo)} – {yr(hi)}'
    name=f'<a href="#" data-goto="{v["e"]}">{nm}</a>' if v['e'] else nm
    sb=('<span class="sub">'+sub+'</span>') if sub else ''
    rows.append(f'          <tr><td>{name}{sb}</td><td class="pn">{fmt(v["n"])}</td><td>{per}</td><td><span class="ik i{tt}"></span> {tn[tt]} ({sh}%)</td></tr>')
RN={'appia':'Via Appia','salaria':'Via Salaria (és a Pinciana felé)','praenestina':'Via Praenestina (Porta Maior)','labicana':'Via Labicana','latina':'Via Latina','ostiensis':'Via Ostiensis','nomentana':'Via Nomentana','aurelia':'Via Aurelia','portuensis':'Via Portuensis','vaticana':'Vatikán (via Triumphalis, via Cornelia)','tiburtina':'Via Tiburtina','ardeatina':'Via Ardeatina','flaminia':'Via Flaminia','cassia':'Via Cassia'}
RO=sorted(D['roads'].items(),key=lambda x:-x[1]['tomb'])
mx=max(v['tomb'] for k,v in RO)
rr='\n'.join(f'        <div class="fe"><span class="fen">{RN[k]}</span><span class="feb"><span class="itomb" style="width:{100*v["tomb"]/mx:.1f}%"></span></span><span class="fev">{fmt(v["tomb"])}</span></div>' for k,v in RO)
card='''    <section class="card" id="insccard">
      <h2>Feliratok</h2>
      <p class="hint">Az Epigraphic Database Roma (EDR) nyílt adatállománya '''+fmt(D['n'])+''' Rómában előkerült feliratot tartalmaz. Ebből '''+fmt(D['loc'])+''' feliratnál ismert a lelőhely (szöveges leírással), '''+fmt(D['dated'])+''' feliratnak van keltezése. Típus szerint: '''+fmt(D['types']['tomb'])+''' sírfelirat, '''+fmt(D['types']['sacred'])+''' vallási, '''+fmt(D['types']['honor'])+''' tiszteletbeli és '''+fmt(D['types']['build'])+''' építési felirat, a többi egyéb vagy ismeretlen (falfirkák, ülésfeliratok, töredékek).</p>
      <h3 class="aqh">A feliratok időben</h3>
      <p class="hint">A keltezés többnyire időszak („Kr. u. 1–2. század”); a felirat súlya egyenletesen oszlik el az időszak 25 éves sávjai között, ahogy az „Építkezések időrendben” kártyán. A „pontosabban keltezett” nézet csak azokat a feliratokat mutatja, amelyeknek a keltezése legfeljebb 100 évet fog át.</p>
      <div class="seg inscsel" role="group" aria-label="Keltezés pontossága"><button data-m="all" aria-pressed="true">Minden keltezett felirat ('''+fmt(D['time']['nAll'])+''')</button><button data-m="tight" aria-pressed="false" title="Csak azok, amelyeknek a keltezése legfeljebb 100 évet fog át (pl. Kr. u. 50–150). A tágabb, például „Kr. u. 1–3. század” keltezések kimaradnak.">Csak a pontosabban keltezett feliratok ('''+fmt(D['time']['nTight'])+''')</button><button data-m="notomb" aria-pressed="false">Sírfeliratok nélkül</button></div>
      <div class="bldchart" id="inscchart"></div>
      <p class="hint bldleg">'''+leg+'''</p>
      <p class="hint popinfo" id="inscinfo">Vidd az egeret egy oszlopra; kattintásra a térkép évcsúszkája arra az időre áll.</p>
      <p class="hint">A feliratok több mint négyötöde sírfelirat, és ezek a Kr. u. 1. század első felében a legsűrűbbek. Ekkor épült a legtöbb nagy kolumbárium; némelyikbe, mint Liviáéba és a Statiliusokéba, egy-egy előkelő háztartás rabszolgáit és felszabadítottjait temették. A tiszteletbeli, vallási és építési feliratok csúcsa későbbi, a Kr. u. 2. század második fele és a 3. század eleje. A görbék a feliratállítás szokását mutatják, nem a népességet; a 3. század közepétől a feliratok száma erősen csökken.</p>
      <h3 class="aqh">A legnagyobb lelőhelyek</h3>
      <div class="regwrap"><table class="regtab insctab">
        <thead><tr><th>Lelőhely</th><th>Felirat</th><th>Fő időszak</th><th>Leggyakoribb típus</th></tr></thead>
        <tbody>
'''+'\n'.join(rows)+'''
        </tbody>
      </table></div>
      <p class="hint">A „fő időszak” a feliratok keltezésének középső fele (az időszakok középpontjai alapján, 25 évre kerekítve). Egy-egy lelőhelyhez az EDR lelőhely-leírásaiból soroltuk a feliratokat (például minden „Vigna Codini” kezdetű leírás egy sorba került). A linkként jelölt nevekre kattintva a térkép odaugrik.</p>
      <h3 class="aqh">Sírfeliratok az utak mentén</h3>
      <p class="hint">Rómában a városon belül nem temetkeztek, ezért a sírok a kivezető utak mentén sorakoztak. A lelőhely leírásában szereplő út-, kapu- és katakombanevek alapján '''+fmt(D['nroad'])+''' felirat sorolható egy-egy úthoz; a sáv a sírfeliratok számát mutatja.</p>
      <div class="foodest roadest">
'''+rr+'''
      </div>
    </section>
'''
b=rep(b,'    <section class="card" id="bldcard">',card+'    <section class="card" id="bldcard">')
js='''/* v82: feliratok (insc/data.json) */
const INSC='''+json.dumps({"bins":D['bins'],"w":D['w'],"time":{k:D['time'][k] for k in ('all','tight')}},separators=(',',':'))+''';
var inscYear=null;
(function(){const box=document.getElementById("inscchart");if(!box)return;const NS="http://www.w3.org/2000/svg",loc=document.documentElement.lang==="en"?"en-US":"hu-HU";
  const T=["tomb","sacred","honor","build","other"],B=INSC.bins,W=INSC.w;let mode="all",yv=null;
  const labs=[...document.querySelectorAll("#insccard .bldleg .il")].map(e=>e.textContent);
  const mk=(n,a,p)=>{const e=document.createElementNS(NS,n);for(const k in a)e.setAttribute(k,a[k]);if(p)p.appendChild(e);return e;};
  const info=document.getElementById("inscinfo"),f0=v=>Math.round(v).toLocaleString(loc);
  function draw(){const S=INSC.time[mode==="tight"?"tight":"all"],G=mode==="notomb"?T.slice(1):T;box.innerHTML="";
    const Wd=Math.max(320,Math.min(1600,box.clientWidth||660)),H=Wd<520?180:Math.min(420,Math.max(220,Math.round(Wd*0.28))),L=46,R=10,Tp=8,Bt=26;
    const s=mk("svg",{viewBox:`0 0 ${Wd} ${H}`,width:Wd,height:H,class:"bldsvg"},box);const n=B.length,bw=(Wd-L-R)/n;
    const tot=B.map((_,k)=>G.reduce((a,g)=>a+S[g][k],0)),mx=Math.max(...tot)*1.05||1,sy=v=>Tp+(1-v/mx)*(H-Tp-Bt);
    const st=[1,2,5,10,20,50,100,200,500,1000,2000];const step=st.find(x=>mx/x<=6)||5000;
    for(let v=0;v<=mx;v+=step){const y=sy(v);mk("line",{x1:L,x2:Wd-R,y1:y,y2:y,class:"pg"},s);const t=mk("text",{x:L-5,y:y+4,"text-anchor":"end",class:"pt"},s);t.textContent=v.toLocaleString(loc);}
    const xs=x=>L+(x-B[0])/W*bw;(Wd>900?[-200,-100,0,100,200,300,400,500,600,700]:[-200,0,200,400,600]).forEach(x=>{const t=mk("text",{x:Math.min(Wd-R,Math.max(L,xs(x))),y:H-Bt+16,"text-anchor":x===-200?"start":x===700?"end":"middle",class:"pt"},s);t.textContent=x===0?"0":fmtY(x);});
    mk("line",{x1:L,x2:Wd-R,y1:H-Bt,y2:H-Bt,class:"pax"},s);
    B.forEach((x,k)=>{const g0=mk("g",{class:"bb"},s);let acc=0;G.forEach(g=>{const v=S[g][k];if(v<=0)return;const y1=sy(acc+v),y0=sy(acc);mk("rect",{x:xs(x)+0.5,y:y1,width:Math.max(1,bw-1),height:Math.max(0,y0-y1),class:"ik i"+g},g0);acc+=v;});
      mk("rect",{x:xs(x),y:Tp,width:bw,height:H-Tp-Bt,class:"bhit"},g0);
      const show=()=>{s.querySelectorAll(".bb.on").forEach(e=>e.classList.remove("on"));g0.classList.add("on");if(info)info.textContent=fmtY(x)+"–"+fmtY(x+W)+" · "+f0(tot[k])+" ("+G.filter(g=>S[g][k]>=0.5).map(g=>labs[T.indexOf(g)]+": "+f0(S[g][k])).join("; ")+")";};
      g0.addEventListener("mouseenter",show);g0.addEventListener("click",()=>{show();if(typeof setYear==="function")setYear(Math.max(-1000,Math.min(650,x+Math.round(W/2))));});});
    const yl=mk("line",{class:"py",y1:Tp,y2:H-Bt,x1:0,x2:0},s);yl.style.display="none";s._yl=yl;s._xs=xs;inscYear(yv);}
  inscYear=function(y){yv=y;const s=box.querySelector("svg");if(!s||!s._yl)return;if(y==null||y==="all"||y<B[0]||y>B[B.length-1]+W){s._yl.style.display="none";return;}const x=s._xs(+y);s._yl.setAttribute("x1",x);s._yl.setAttribute("x2",x);s._yl.style.display="";};
  const bs=[...document.querySelectorAll(".inscsel button")];bs.forEach(bt=>bt.addEventListener("click",()=>{mode=bt.dataset.m;bs.forEach(x=>x.setAttribute("aria-pressed",String(x===bt)));draw();}));
  document.querySelectorAll("#insccard [data-goto]").forEach(a=>a.addEventListener("click",e=>{e.preventDefault();goTo(a.dataset.goto);}));
  draw();inscYear(state.year);let lw=0;if(window.ResizeObserver)new ResizeObserver(()=>{const w=box.clientWidth;if(w&&Math.abs(w-lw)>4){lw=w;draw();}}).observe(box);})();
'''
b=rep(b,'/* v79: építkezések időrendben (bld/data.json) */',js+'/* v79: építkezések időrendben (bld/data.json) */')
b=rep(b,'if(popYear)popYear(y);if(bldYear)bldYear(y);}','if(popYear)popYear(y);if(bldYear)bldYear(y);if(inscYear)inscYear(y);}')
b=rep(b,'"Építkezések időrendben":"az','"Feliratok":"az EDR '+fmt(D['n'])+' római felirata: időben, lelőhelyek, sírok az utak mentén","Építkezések időrendben":"az')
src='''      <li><b>Feliratok.</b> Epigraphic Database Roma (EDR), EpiDoc-fájlok, 12. változat (Sapienza Università di Roma – Università di Napoli L’Orientale – Università di Firenze – Università di Foggia; S. Panciera, G. Camodeca, G. A. Cecconi, S. Orlandi, L. Fabriani, S. Evangelisti), Zenodo 2026, <a href="https://doi.org/10.5281/zenodo.18468635">10.5281/zenodo.18468635</a>, CC BY 4.0. Az összesítés saját: a Rómában előkerült feliratok (lelőhely: Roma), típus az EDR besorolása szerint, keltezés az EDR „notBefore–notAfter” adataiból, a lelőhelyek és az utak a lelőhely-leírás kulcsszavai alapján (insc/calc.py).</li>
      <li><b>Építkezések időrendben.</b>'''
b=rep(b,'      <li><b>Építkezések időrendben.</b>',src)
c=rep(c,'</style>','''/* v82: feliratok */
#insccard{--it:#8a5a44;--is:#7a4e9c;--ih:#c9a227;--ib:#2f7fb8;--io:#b9c0c4}
#insccard.open{grid-column:1/-1}
.ik.itomb{fill:var(--it);background:var(--it)}.ik.isacred{fill:var(--is);background:var(--is)}.ik.ihonor{fill:var(--ih);background:var(--ih)}.ik.ibuild{fill:var(--ib);background:var(--ib)}.ik.iother{fill:var(--io);background:var(--io)}
span.ik{display:inline-block;width:11px;height:11px;border-radius:2px;vertical-align:middle;margin-left:4px}
.insctab td{white-space:normal;text-align:left;vertical-align:top}.insctab td.pn{text-align:right;white-space:nowrap}
.insctab td .sub{display:block;color:var(--muted);font-size:12px}
.insctab th{text-align:left}
.roadest .feb span.itomb{background:var(--it)}
</style>''')
open(p,'w',encoding='utf8').write(b);open(cp,'w',encoding='utf8').write(c);print('ok')
