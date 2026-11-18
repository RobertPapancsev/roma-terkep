# v78: „Róma élelmezése” kártya: gabona (ókori számadatok, osztás, hajók), olaj és a Monte Testaccio (méret, összetétel, amforaszám-becslések, feliratok), későbbi osztások; a térképen lévő kikötő- és raktárhelyek listája és kiemelése.
import shutil
p='body_v60pre.html';b=open(p,encoding='utf8').read();cp='style_v60pre.css';c=open(cp,encoding='utf8').read()
assert 'foodcard' not in b
shutil.copy(p,'src/body_v60pre_before_v78.html');shutil.copy(cp,'src/style_v60pre_before_v78.css')
def rep(s,a,x,n=1):
    assert s.count(a)==n,(a[:60],s.count(a));return s.replace(a,x)
PL=[("emporium","Emporium","a tiberisi kikötő rakpartja, Kr. e. 193-tól"),
("porticusaemilia","Porticus Aemilia","nagy raktárcsarnok a kikötő mellett (más értelmezés szerint hajódokk)"),
("horreagalbae","Horrea Galbae","gabona-, olaj- és borraktárak három udvar körül"),
("horrealolliana","Horrea Lolliana","raktárak a kikötőnegyedben"),
("monstestaceus","Monte Testaccio","a kiürített olajos amforák dombja"),
("statioannonae","Statio Annonae (?)","a gabonaellátás hivatala a Forum Boariumon; az azonosítás vitatott"),
("minucia","Porticus Minucia Frumentaria (?)","az ingyenes gabonaosztás helye; az azonosítás vitatott"),
("horrea","Horrea Agrippiana","raktár a Fórum és a Palatinus között"),
("horreapiper","Horrea Piperataria","a fűszerraktárak"),
("macellumliviae","Macellum Liviae","élelmiszerpiac az Esquilinuson")]
lis='\n'.join(f'        <li><span class="n">·</span><span><strong><a href="#" data-goto="{i}">{n}</a></strong><span class="sub">{s}</span></span></li>' for i,n,s in PL)
card='''    <section class="card" id="foodcard">
      <h2>Róma élelmezése</h2>
      <p class="hint">A milliós város élelmének nagy részét tengeren hozták. Josephus szerint Africa nyolc hónapig, Egyiptom négy hónapig etette Rómát (A zsidó háború 2.383, 2.386). Az <i>Epitome de Caesaribus</i> szerint Augustus idején évente húszmillió egység gabona érkezett Egyiptomból (1.6); a szöveg nem nevezi meg a mértékegységet, a kutatás általában modiusnak érti.</p>
      <h3 class="aqh">Gabona</h3>
      <p class="hint">Gaius Gracchus törvénye (Kr. e. 123) óta a jogosult polgárok kedvezményes áron, Clodius törvénye (Kr. e. 58) óta ingyen kapták a gabonát, fejenként havi öt modiust, kb. 33 kg-ot (P. Garnsey – D. Rathbone 1985). Augustus alatt valamivel több mint 200 000 polgár kapott állami gabonát (<i>Res gestae</i> 15; lásd „Róma népessége”). A gabonaellátást Augustus kora végétől a <i>praefectus annonae</i> felügyelte (Tacitus, <i>Annales</i> 1.7).</p>
      <p class="hint">A szállítást magánhajósok végezték, ezért a császárok kedvezményekkel ösztönözték őket. Claudius vállalta a viharban elveszett rakomány kárát, és kiváltságokat adott annak, aki gabonaszállító hajót épített (Suetonius, <i>Claudius</i> 18–19). Gaius jogtudós szerint az a latin jogú ember, aki legalább 10 000 modius befogadóképességű hajót épített, és hat évig gabonát szállított vele Rómába, római polgárjogot kapott (<i>Institutiones</i> 1.32c). A 2. században az 50 000 modiusos hajó tulajdonosát mentesítették a közterhek alól (<i>Digesta</i> 50.5.3).</p>
      <p class="hint">A <i>Historia Augusta</i> szerint Septimius Severus halálakor hétévi gabonakészletet hagyott hátra, napi 75 000 modius kiosztásával számolva (Severus 23.2).</p>
      <h3 class="aqh">Olaj: a Monte Testaccio</h3>
      <p class="hint">A Tiberis-parti kikötő, az Emporium mögött áll Róma legnagyobb régészeti „adatbázisa”: egy mesterséges domb, amely szinte csak összetört olajos amforákból áll. Az olajtól átitatott cserepeket nem lehetett újra felhasználni. A domb nem rendezetlen szemétlerakó: a fenék nélküli amforákat cseréppel töltötték meg, és lépcsőzetes támfalakat építettek belőlük; mögéjük öntötték a többi cserepet, a rothadó olaj szagát pedig mésszel fedték el (J. A. Lobell 2009, J. Remesal ásatásáról).</p>
      <div class="regwrap"><table class="regtab foodtab">
        <tbody>
          <tr><td>Alapterület</td><td>kb. 2 ha</td><td>Claridge; Peña</td></tr>
          <tr><td>Térfogat</td><td>kb. 580 000 m³</td><td>Claridge; Peña</td></tr>
          <tr><td>Magasság</td><td>kb. 35 m; más összegzések 40–50 m-t adnak a környező talaj fölött</td><td>Claridge; Peña; Broekaert</td></tr>
          <tr><td>Kerület</td><td>majdnem 1 km</td><td>Claridge; Peña</td></tr>
          <tr><td>Használat</td><td>Augustustól a 3. század közepéig; a legkésőbbi eddig talált consuli dátum Kr. u. 265</td><td>Dressel; Lobell 2009</td></tr>
        </tbody>
      </table></div>
      <h4 class="aqh4">Miből áll?</h4>
      <div class="foodbar"><span class="fb1" style="width:80%">kb. 80%</span><span class="fb2" style="width:15%">15–17%</span><span class="fb3" style="width:5%"></span></div>
      <p class="hint aqleg"><span class="sw f1"></span> dél-hispániai (baeticai) olajos amfora, Dressel 20 típus · <span class="sw f2"></span> észak-africai (tripolitaniai és tunéziai) amforák · <span class="sw f3"></span> kb. 5% hispániai és galliai bor- és halszószos edény (W. Broekaert 2011). Egy másik összegzés szerint a baeticai amforák aránya 85% fölötti (Lobell 2009).</p>
      <h4 class="aqh4">Hány amfora? Három becslés</h4>
      <div class="foodest">
        <div class="fe"><span class="fen">E. Rodríguez Almeida 1984</span><span class="feb"><span style="width:37.7%"></span></span><span class="fev">kb. 20 millió</span></div>
        <div class="fe"><span class="fen">J. Remesal (Lobell 2009)</span><span class="feb"><span style="width:47.2%"></span></span><span class="fev">kb. 25 millió</span></div>
        <div class="fe"><span class="fen">B. Ward-Perkins 2005</span><span class="feb"><span style="width:100%"></span></span><span class="fev">kb. 53 millió</span></div>
      </div>
      <p class="hint">A becslések a domb térfogatából és az ásatott szelvények sűrűségéből indulnak ki, ezért ennyire eltérnek. Egy Dressel 20 amfora kb. 70 liter olajat fogadott be (P. Tyers szerint 7–8 modius, 61–70 liter); üresen kb. 30, tele kb. 100 kg volt. Broekaert számítása szerint ez Augustustól Aurelianusig 1,4–1,75 milliárd liter olajat, évente kb. 74 000–92 600 amforát, azaz 5,2–6,5 millió litert jelent, évente 100–150 hajórakományt (Broekaert 2011). Ward-Perkins nagyobb amforaszáma kb. 6 milliárd literrel számol.</p>
      <h4 class="aqh4">A feliratok</h4>
      <p class="hint">Sok amforán égetés után festett felirat (<i>titulus pictus</i>) van; a kutatás a sorokat görög betűkkel jelöli. Az α sor az üres edény súlya, a β a szállító kereskedő neve, a γ az olaj súlya, a δ az ellenőrzés bejegyzése: a hispániai ellenőrző hely, a consuli év és a tisztviselők neve. Egy amforán például az üres edény 82 római font, az olaj 216 római font (Lobell 2009). A fülekre nyomott bélyegek a fazekasműhelyhez vagy a birtokhoz kötődő neveket őrzik. A consuli dátumok miatt a domb rétegei évre pontosan keltezhetők; ezeket 1872-ben Heinrich Dressel kezdte gyűjteni; az 1980-as évektől E. Rodríguez Almeida, majd J. M. Blázquez és J. Remesal ásatásai folytatják (CEIPAC, Barcelonai Egyetem).</p>
      <p class="hint">A <i>Historia Augusta</i> szerint Septimius Severus a római népnek ingyenes napi olajosztást adott örök időkre (Severus 18.3). Broekaert szerint a bélyegek és a feliratok azt mutatják, hogy a behozatal már az Antoninusok alatt tetőzött; Severus intézkedése inkább a szállítás átszervezése volt. Ekkor kerültek a lefoglalt hispániai olajbirtokok a császárhoz: a bélyegeken az AVGGGNNN rövidítés Severust és két fiát jelöli (Broekaert 2011).</p>
      <h3 class="aqh">A 3. század végén</h3>
      <p class="hint">Aurelianus (270–275) idejére a gabona helyett már kenyeret osztottak: a <i>Historia Augusta</i> szerint egy unciával növelte a cipók súlyát az egyiptomi bevételből (Aurelianus 47.1), és sertéshúst is osztatott (35.2). Az ingyenes olaj, kenyér és sertéshús mellé ingyenes bort is tervezett: Etruriában szőlőt akart telepíttetni, de ez nem valósult meg; a császári bort a Sol-templom csarnokaiban árulták (48.1–4).</p>
      <h3 class="aqh">A térképen</h3>
      <p class="hint"><button class="chip" id="foodbtn" aria-pressed="false">A helyek kiemelése a térképen</button> A nevekre kattintva a térkép odaugrik. Az ostiai és a portusi kikötő a térképen kívül esik.</p>
      <ol class="itin chlist foodlist">
'''+lis+'''
      </ol>
    </section>
'''
b=rep(b,'    <section class="card" id="popcard">',card+'    <section class="card" id="popcard">')
js='''/* v78: Róma élelmezése – a helyek a térképen */
(function(){const ids=[...document.querySelectorAll("#foodcard [data-goto]")].map(a=>a.dataset.goto),fb=document.getElementById("foodbtn");if(!fb)return;
  document.querySelectorAll("#foodcard [data-goto]").forEach(a=>a.addEventListener("click",e=>{e.preventDefault();goTo(a.dataset.goto);}));
  fb.addEventListener("click",()=>{const on=fb.getAttribute("aria-pressed")!=="true";fb.setAttribute("aria-pressed",String(on));
    ids.forEach(id=>{const n=nodes[id];if(n)n.g.classList.toggle("foodhl",on);});
    if(on){const P=ids.map(id=>nodes[id]&&nodes[id].m._c).filter(c=>c&&isFinite(c[0])&&isFinite(c[1]));if(P.length){
      const x0=Math.min(...P.map(c=>c[0])),x1=Math.max(...P.map(c=>c[0])),y0=Math.min(...P.map(c=>-c[1])),y1=Math.max(...P.map(c=>-c[1]));
      let w=(x1-x0)*1.25+120,h=(y1-y0)*1.25+120;const r=vb[3]/vb[2];if(h/w>r)w=h/r;else h=w*r;setVB([(x0+x1)/2-w/2,(y0+y1)/2-h/2,w,h]);}}});})();
'''
b=rep(b,'/* Ugrás: legördülő menü a (rejtett) gombokból */',js+'/* Ugrás: legördülő menü a (rejtett) gombokból */')
b=rep(b,'"Róma népessége":"becslések','"Róma élelmezése":"gabona, olaj és a Monte Testaccio: ókori adatok és régészeti becslések","Róma népessége":"becslések')
src='''      <li><b>Róma élelmezése.</b> Josephus, <i>A zsidó háború</i> 2.383, 2.386; <i>Epitome de Caesaribus</i> 1.6; <i>Res gestae</i> 15; Tacitus, <i>Annales</i> 1.7; Suetonius, <i>Claudius</i> 18–19; Gaius, <i>Institutiones</i> 1.32c; <i>Digesta</i> 50.5.3; <i>Historia Augusta</i>, Severus 18.3, 23.2, Aurelianus 35.2, 47.1, 48.1–4. P. Garnsey – D. Rathbone, „The Background to the Grain Law of Gaius Gracchus”, <i>Journal of Roman Studies</i> 75 (1985) 20–25. Monte Testaccio: H. Dressel, <i>Ricerche sul Monte Testaccio</i>, Róma 1878; E. Rodríguez Almeida, <i>Il Monte Testaccio: ambiente, storia, materiali</i>, Róma 1984; J. M. Blázquez Martínez – J. Remesal Rodríguez (szerk.), <i>Estudios sobre el Monte Testaccio (Roma)</i> I–IV, Barcelona 1999–2007; W. Broekaert, „Oil for Rome during the Second and Third Century AD: a Confrontation of Archaeological Records and the Historia Augusta”, <i>Mnemosyne</i> 64 (2011) 591–623; J. A. Lobell, „Trash Talk”, <i>Archaeology</i> 62/2 (2009); B. Ward-Perkins, <i>The Fall of Rome and the End of Civilization</i>, Oxford 2005; A. Claridge, <i>Rome</i> (Oxford Archaeological Guides), 2. kiad., Oxford 2010; J. T. Peña, <i>Roman Pottery in the Archaeological Record</i>, Cambridge 2007; „Dressel 20”, in: P. Tyers, <i>Roman Amphoras in Britain</i>, <i>Internet Archaeology</i> 1 (1996).</li>
      <li><b>Róma népessége.</b>'''
b=rep(b,'      <li><b>Róma népessége.</b>',src)
c=rep(c,'</style>','''/* v78: Róma élelmezése */
#foodcard{--fo1:#6d7f2a;--fo2:#b5651d;--fo3:#9aa5a7}
#foodcard.open{grid-column:1/-1}
.regtab.foodtab{min-width:0;width:100%}
.foodtab td{white-space:normal;text-align:left;vertical-align:top}
.foodtab td:last-child{color:var(--muted);font-size:12px}
.foodbar{display:flex;height:22px;border-radius:3px;overflow:hidden;margin:6px 0;font:600 11px var(--font-body);color:#fff}
.foodbar span{display:flex;align-items:center;padding:0 6px;white-space:nowrap;overflow:hidden}
.foodbar .fb1{background:var(--fo1)}.foodbar .fb2{background:var(--fo2)}.foodbar .fb3{background:var(--fo3)}
.aqleg .sw.f1{background:var(--fo1)}.aqleg .sw.f2{background:var(--fo2)}.aqleg .sw.f3{background:var(--fo3)}
.foodest{display:grid;gap:5px;margin:6px 0}
.foodest .fe{display:grid;grid-template-columns:minmax(0,1.4fr) minmax(60px,1fr) auto;gap:8px;align-items:center;font-size:13px}
.foodest .feb{height:12px;background:rgba(0,0,0,.05);border-radius:2px}
.foodest .feb span{display:block;height:100%;background:var(--fo2);border-radius:2px}
.foodest .fev{font-family:var(--font-mono,monospace);font-size:12px;white-space:nowrap}
.m.foodhl .s{stroke:#b5651d!important;stroke-width:3px!important;vector-effect:non-scaling-stroke}
</style>''')
open(p,'w',encoding='utf8').write(b);open(cp,'w',encoding='utf8').write(c);print('ok')
