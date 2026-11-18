// Légiómozgás-kalkulátor – a Birodalmi térkép panelje (v146).
// Hálózat: imp_net.json (Itiner-e utak + ORBIS vízi élek), útgeometria: imp_roads1.json, helynevek: imp_search.json.
(function(){
"use strict";
const HU=(document.documentElement.lang||"hu").startsWith("hu");
const T=HU?{
 btn:"⚔ Légiómozgás",title:"Légiómozgás-kalkulátor",close:"Bezárás",via:"Útközben (nem kötelező)",phv:"köztes hely, pl. hágó vagy város…",dated:"Csak az indulás évében már meglévő utak (ahol az Itiner-e keltezi az utat)",xh:"Átkelés ismert híd nélkül (óra)",xBr:"átkelés: {r}, ismert római híd: {b}",xNo:"átkelés: {r}, ismert híd nélkül (+{h} óra)",xH:"Folyóátkelések",xP:"{n} átkelés nagyobb folyón, ebből {b} ismert római hídon (Wikidata). A többinél {h} óra késéssel számoltam (komp, hajóhíd vagy gázló); a hídlista hiányos, ezért ez inkább felső becslés.",wDatedFb:"Kr. u. {y}-ban még meglévő utakon nem volt útvonal, ezért a később épült utakat is használtam.",wDatedL:"A Kr. u. {y} után épült utakat kihagytam; emiatt az útvonal kb. {k} km-rel hosszabb.",seaR:"Hajón kedvező széllel kb. {a}, kedvezőtlennel kb. {b} nap (a számítás {n} nap; Casson 1951 alapján); érkezés így kb. {d1} – {d2}",prof:"Magassági profil: a csomópontok magassága és a szakaszok legmagasabb pontja; a tengeri szakasz 0 m.",mini:"Panel összecsukása",maxi:"Panel kinyitása",from:"Kiindulás",to:"Célállomás",ph:"hely neve…",
 start:"Indulás",era:"korszak",ad:"Kr. u.",bc:"Kr. e.",year:"év",month:"hónap",day:"nap",inf:"Gyalogság (fő)",cav:"Lovasság (fő)",mules:"Málhás öszvérek",wag:"Ökrös szekerek",
 pace:"Tempó",p0:"normál katonai lépés (Vegetius: 20 mérföld / 5 óra)",p1:"teljes lépés (24 mérföld / 5 óra)",p2:"erőltetett menet (teljes lépés, 7 óra)",
 rest:"Pihenőnap minden … menetnap után (0 = nincs)",water:"Hajó és folyami szállítás",winter:"Hajózás a téli zárt időszakban is (Nov. 11 – Márc. 10)",
 hypo:"Feltételezett (hipotetikus) utak kerülése",port:"Behajózás/kirakodás (nap)",own:"A katonák saját élelme (nap)",adv:"További beállítások",
 grain:"Gabona (kg/fő/nap)",wat:"Víz (l/fő/nap)",hfod:"Ló takarmánya (kg/nap)",mfod:"Öszvér takarmánya (kg/nap)",mcap:"Öszvér teherbírása (kg)",wcap:"Szekér teherbírása (kg)",
 width:"Gyalogos sorok szélessége (fő)",seaS:"Tengeri sebesség (km/nap)",seas:"Évszakhatások (hó, sár, hőség, legelő, szél, folyók)",snowZ:"Hóval zárt hágó (m felett, dec.–ápr.)",mud:"Sár: lassulás nem biztos úton (%)",heat:"Hőségben napi menetidő (%)",hotW:"Víz hőségben (szorzó)",hg:"Ló szemes takarmánya legelőn (kg)",mg:"Öszvér szemes takarmánya legelőn (kg)",seasH:"Évszak",seasP:"Sáros időszakban {w} menetnap, hőségben {h} nap (rövidebb menet, több víz), legeltetéssel {g} nap a(z) {n}-ból; a {s} m feletti hágók decembertől áprilisig zárva.",wRivIce:"Folyami szakasz jégzajlás idején ({d}).",wEtes:"Nyáron a Földközi-tenger keleti részén északi szél (etéziák): észak, illetve nyugat felé lassabb a hajózás.",wSnowDet:"A rövidebb, {k2} km-es út egy kb. {z} m-es hágón vinne át, amelyet ilyenkor hó zár; ezért a számítás a {k1} km-es kerülőutat választotta. Ha mégis át akarsz kelni, emeld meg a hóhatárt a beállításoknál, vagy kapcsold ki az évszakhatásokat.",wSnowIn:"Hóval zárt hágó ({z} m) az útvonalon ({d}); másik út nem volt.",calc:"Számítás",loading:"Hálózat betöltése…",
 noPlace:"Válassz kiindulást és célállomást a listából.",noRoute:"Nem találtam útvonalat a hálózaton (például a tenger a téli időszakban zárva van).",
 sum:"Összesítés",dist:"Táv",road:"úton",ship:"hajón",river:"folyón",mdays:"menetnap",rdays:"pihenőnap",sdays:"hajón töltött nap",
 dep:"Indulás",arr:"Érkezés",total:"Összesen",cal:"naptári nap",col:"Menetoszlop",colL:"hossza kb.",pass:"áthaladási ideje egy ponton",
 camp:"Minden este menettábor (castra): az oszlop végének is napnyugta előtt be kell érnie",campH:"Táborépítés ideje (óra)",campS:"{n} napon rövid a nappal: a menetnek korábban kell véget érnie, hogy napnyugtáig az oszlop vége is beérjen, és felépüljön a tábor ({c} óra; a táborépítés az oszlop elejének érkezésekor kezdődik)",campOK:"A tábor ({c} óra) és az oszlop beérkezése egyik napon sem rövidíti a menetet",tailS:"{n} napon rövid a nappal: a menetnek korábban kell véget érnie, hogy napnyugtáig az oszlop vége is beérjen",tailOK:"Az oszlop vége minden nap napnyugta előtt beér",
 tailW:"A menetoszlop vége a menetidő után még {h} órát halad: rövid nappalon sötétedés után ér táborba.",
 log:"Ellátás",perday:"naponta",trip:"az út alatt",grainT:"gabona (katonák)",fodT:"takarmány (állatok)",waterT:"víz",carry:"A málha és a katonák saját élelme kb. {d} napra elég; ennél hosszabb úton útközbeni ellátás (raktárak, rekvirálás) kell.",
 days:"Napi szakaszok",dcol:["Nap","Dátum","km","↑ m","Táborhely közelében","Megjegyzés"],restN:"pihenőnap",shipN:"hajón",embN:"behajózás/kirakodás",arrN:"megérkezés",
 warn:"Figyelmeztetések",wSea:"Tengeri szakasz a téli zárt időszakban ({d}).",wSeaU:"Tengeri szakasz a bizonytalan hajózási időszakban ({d}).",
 wHyp:"Az útvonal {p}%-a feltételezett (hipotetikus) úton halad.",wSnap:"{w} kb. {k} km-re van a legközelebbi úttól; ezt a szakaszt légvonalban számoltam.",
 wUp:"Folyón felfelé ({k} km): vontatás, lassú.",relief:"Szintkülönbség: összesen kb. {u} m emelkedés és {d} m lejtés; legmagasabb pont kb. {z} m.",wPass:"Hegyi átkelő kb. {z} m magasan ({d}): télen és kora tavasszal hó, a hágó járhatatlan lehet.",wClosed:"A tengeri útvonalakat a téli zárt hajózási időszak miatt kihagytam; a „Hajózás a téli zárt időszakban is” beállítással bekapcsolhatók.",
 assume:"Becslés a megadott feltevésekkel: menetsebesség {v} km/óra sík terepen, napi menetidő {h} nyári óra (Vegetius; Róma szélességén kb. 1¼ mai óra egy nyári óra), de rövid nappalon csak annyi, hogy napnyugtáig az oszlop vége beérjen és felépüljön a tábor, irányfüggő lassulás a domborzat szerint (Tobler-függvény, felfelé lassabb), az út bizonyossága szerinti lassulás. Évszakhatások (becsült szorzók, a beállításoknál módosíthatók): hó a hágókon, sár, hőség, legelő, etéziás szél, folyami jég és vízállás. A magasságok az Itiner-e nyomvonalból, illetve kb. 200–300 m-es domborzati rácsból származnak; a pontatlan nyomvonal miatt hegyvidéken túlbecsülhetők.",
 km:"km",h:"óra",t:"t",m3:"m³",none:"–",ex:"pl."
}:{
 btn:"⚔ Legion march",title:"Legion march calculator",close:"Close",via:"Via (optional)",phv:"intermediate place, e.g. a pass or town…",dated:"Only roads that already existed in the departure year (where Itiner-e dates the road)",xh:"River crossing without a known bridge (hours)",xBr:"crossing: {r}, known Roman bridge: {b}",xNo:"crossing: {r}, no known bridge (+{h} h)",xH:"River crossings",xP:"{n} crossings of larger rivers, {b} of them on a known Roman bridge (Wikidata). For the others I added a delay of {h} hours (ferry, pontoon bridge or ford); the bridge list is incomplete, so this is rather an upper estimate.",wDatedFb:"There was no route on roads existing in AD {y}, so roads built later were used too.",wDatedL:"Roads built after AD {y} were left out; because of this the route is about {k} km longer.",seaR:"At sea about {a} days with favourable winds and {b} with unfavourable ones (calculated: {n} days; after Casson 1951); arrival therefore about {d1} – {d2}",prof:"Elevation profile: node elevations and the highest point of each segment; sea legs at 0 m.",mini:"Collapse panel",maxi:"Expand panel",from:"Start",to:"Destination",ph:"place name…",
 start:"Departure",era:"era",ad:"AD",bc:"BC",year:"year",month:"month",day:"day",inf:"Infantry (men)",cav:"Cavalry (men)",mules:"Pack mules",wag:"Ox wagons",
 pace:"Pace",p0:"normal military step (Vegetius: 20 miles / 5 hours)",p1:"full step (24 miles / 5 hours)",p2:"forced march (full step, 7 hours)",
 rest:"Rest day after every … marching days (0 = none)",water:"Ship and river transport",winter:"Sail also in the closed winter season (11 Nov – 10 Mar)",
 hypo:"Avoid hypothetical roads",port:"Embarking/landing (days)",own:"Soldiers' own rations (days)",adv:"More settings",
 grain:"Grain (kg/man/day)",wat:"Water (l/man/day)",hfod:"Horse fodder (kg/day)",mfod:"Mule fodder (kg/day)",mcap:"Mule load (kg)",wcap:"Wagon load (kg)",
 width:"Infantry ranks width (men)",seaS:"Sea speed (km/day)",seas:"Seasonal effects (snow, mud, heat, grazing, wind, rivers)",snowZ:"Snow-closed passes (above m, Dec–Apr)",mud:"Mud: slowing on uncertain roads (%)",heat:"Daily marching time in heat (%)",hotW:"Water in heat (multiplier)",hg:"Horse hard feed when grazing (kg)",mg:"Mule hard feed when grazing (kg)",seasH:"Season",seasP:"{w} marching days in the muddy season, {h} days in heat (shorter march, more water), grazing on {g} of {n} days; passes above {s} m closed from December to April.",wRivIce:"River leg during ice ({d}).",wEtes:"In summer the eastern Mediterranean has northerly winds (Etesians): sailing north or west is slower.",wSnowDet:"The shorter {k2} km route crosses a pass of about {z} m that snow closes at this time of year, so the calculation chose the {k1} km detour. To cross anyway, raise the snow limit in the settings or turn off seasonal effects.",wSnowIn:"Snow-closed pass ({z} m) on the route ({d}); there was no other way.",calc:"Calculate",loading:"Loading network…",
 noPlace:"Choose a start and a destination from the list.",noRoute:"No route found on the network (for example, the sea is closed in winter).",
 sum:"Summary",dist:"Distance",road:"by road",ship:"by sea",river:"by river",mdays:"marching days",rdays:"rest days",sdays:"days at sea",
 dep:"Departure",arr:"Arrival",total:"Total",cal:"calendar days",col:"Marching column",colL:"length c.",pass:"time to pass a point",
 camp:"Marching camp (castra) every evening: the tail of the column must also arrive before sunset",campH:"Camp building time (hours)",campS:"On {n} days daylight is short: the march must end earlier so that the tail of the column arrives and the camp is built by sunset ({c} hours; building starts when the head of the column arrives)",campOK:"The camp ({c} hours) and the arrival of the column shorten the march on no day",tailS:"On {n} days daylight is short: the march must end earlier so that the tail of the column arrives by sunset",tailOK:"The tail of the column arrives before sunset every day",
 tailW:"The tail of the column marches {h} hours after the head stops: on short days it reaches camp after dark.",
 log:"Supply",perday:"per day",trip:"for the journey",grainT:"grain (soldiers)",fodT:"fodder (animals)",waterT:"water",carry:"Baggage and the soldiers' own rations last c. {d} days; longer journeys need supply on the way (depots, requisition).",
 days:"Daily stages",dcol:["Day","Date","km","↑ m","Camp near","Note"],restN:"rest day",shipN:"at sea",embN:"embarking/landing",arrN:"arrival",
 warn:"Warnings",wSea:"Sea leg in the closed winter season ({d}).",wSeaU:"Sea leg in the uncertain sailing season ({d}).",
 wHyp:"{p}% of the route follows hypothetical roads.",wSnap:"{w} is c. {k} km from the nearest road; this leg is counted in a straight line.",
 wUp:"Upstream on a river ({k} km): towing, slow.",relief:"Relief: c. {u} m of ascent and {d} m of descent in total; highest point c. {z} m.",wPass:"Mountain crossing at c. {z} m ({d}): snow in winter and early spring, the pass may be impassable.",wClosed:"Sea routes were left out because of the closed winter sailing season; they can be switched on with “Sail also in the closed winter season”.",
 assume:"Estimate with these assumptions: marching speed {v} km/h on level ground, daily marching time {h} summer hours (Vegetius; one summer hour is about 1¼ modern hours at the latitude of Rome), but on short days only as long as lets the tail of the column arrive and the camp be built by sunset, direction-dependent slowing by relief (Tobler's function, uphill slower), slowing by road certainty. Seasonal effects (estimated multipliers, adjustable in the settings): snow on passes, mud, heat, grazing, Etesian winds, river ice and water level. Elevations come from the Itiner-e tracks or a c. 200–300 m terrain grid; because the tracks are approximate they may be overestimated in mountains.",
 km:"km",h:"h",t:"t",m3:"m³",none:"–",ex:"e.g."
};
const MON_HU=["január","február","március","április","május","június","július","augusztus","szeptember","október","november","december"];
const MON_EN=["January","February","March","April","May","June","July","August","September","October","November","December"];
const MON_LA=["Ian.","Feb.","Mart.","Apr.","Mai.","Iun.","Iul.","Aug.","Sept.","Oct.","Nov.","Dec."];
const MON=HU?MON_HU:MON_EN;
const esc=s=>String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const fmt=(x,d=0)=>Number(x).toLocaleString(HU?"hu-HU":"en-GB",{maximumFractionDigits:d,minimumFractionDigits:d});
// ---- Julián naptár ----
const leap=y=>y%4===0;const mlen=(y,m)=>[31,leap(y)?29:28,31,30,31,30,31,31,30,31,30,31][m];
function jd(y,m,d){const a=Math.floor((14-(m+1))/12),yy=y+4800-a,mm=(m+1)+12*a-3;return d+Math.floor((153*mm+2)/5)+365*yy+Math.floor(yy/4)-32083;}
function fromJd(J){const c=J+32082,d=Math.floor((4*c+3)/1461),e=c-Math.floor(1461*d/4),m=Math.floor((5*e+2)/153);const day=e-Math.floor((153*m+2)/5)+1,mon=m+3-12*Math.floor(m/10),y=d-4800+Math.floor(m/10);return [y,mon-1,day];}
const ROMN=n=>{const v=[[10,"X"],[9,"IX"],[5,"V"],[4,"IV"],[1,"I"]];let s="";for(const[a,b]of v)while(n>=a){s+=b;n-=a;}return s;};
function romanDate(y,m,d){const non=[2,4,6,9].includes(m)?7:5,ide=non+8;
 if(d===1)return "Kal. "+MON_LA[m];if(d===non)return "Non. "+MON_LA[m];if(d===ide)return "Id. "+MON_LA[m];
 if(d<non)return (d===non-1?"pridie ":"a. d. "+ROMN(non-d+1)+" ")+"Non. "+MON_LA[m];
 if(d<ide)return (d===ide-1?"pridie ":"a. d. "+ROMN(ide-d+1)+" ")+"Id. "+MON_LA[m];
 const nm=(m+1)%12,n=mlen(y,m)-d+2;return (n===2?"pridie ":"a. d. "+ROMN(n)+" ")+"Kal. "+MON_LA[nm];}
const dstr=J=>{const[y,m,d]=fromJd(J);return y<=0?(HU?`Kr. e. ${1-y}. ${MON[m]} ${d}.`:`${d} ${MON[m]} ${1-y} BC`):(HU?`${y}. ${MON[m]} ${d}.`:`${d} ${MON[m]} ${y}`);};
const doy=J=>{const[y]=fromJd(J);return J-jd(y,0,1)+1;};
function daylight(latDeg,J){const dec=23.44*Math.sin(2*Math.PI*(284+doy(J))/365)*Math.PI/180,lat=latDeg*Math.PI/180;
 const c=-Math.tan(lat)*Math.tan(dec);return c>=1?0:c<=-1?24:2*Math.acos(c)*180/Math.PI/15;}
const latOf=y=>40+y/111.2;
function seaSeason(J){const[ y,m,d]=fromJd(J),md=m*100+d; // 0 nyitott, 1 bizonytalan, 2 zárt (Vegetius IV.39)
 if(md>=1011||md<211)return 2; if(md<427||md>=814)return 1; return 0;}
// ---- adatok ----
let NET=null,IDX=null,RG=null,ADJ=null,load=null;
function getData(){return load||(load=Promise.all([fetch("imp_net.json").then(r=>r.json()),fetch("imp_search.json").then(r=>r.json()),fetch("imp_roads1.json").then(r=>r.json())]).then(([n,s,r])=>{
 NET=n;IDX=s;RG={};for(const[i,mt,ce,str]of r)RG[i]=str;
 const N=n.n.length;ADJ=Array.from({length:N},()=>[]);
 n.e.forEach((e,k)=>{ADJ[e[0]].push([k,1]);if(e[3]!==5&&e[3]!==6)ADJ[e[1]].push([k,-1]);});
 NET._dt=new Map((n.dt||[]).map(([k,lo,hi])=>[k,[lo,hi]]));NET._xc=new Map();for(const[k,rv,br]of n.xc||[])(NET._xc.get(k)||NET._xc.set(k,[]).get(k)).push([rv,br]);}));}
const roadOK=(k,y)=>{const d=NET._dt.get(k);return !d||((d[0]==null||d[0]<=y)&&(d[1]==null||d[1]>=y));};
const nUnb=k=>{const x=NET._xc.get(k);return x?x.filter(c=>c[1]<0).length:0;};
const rvName=i=>{const r=NET.rv[i];return r[0]&&r[1]&&r[0]!==r[1]?`${r[0]} (${r[1]})`:(r[0]||r[1]);};
const nrm=s=>s.normalize("NFD").replace(/[̀-ͯ]/g,"").toLowerCase();
// ---- felület ----
const box=document.querySelector(".mapbox");if(!box)return;
const css=document.createElement("style");css.textContent=`
.mvbtn{position:absolute;z-index:6;left:8px;top:8px;font:inherit;padding:5px 12px;border:1px solid var(--line);border-radius:14px;background:var(--sheet);color:var(--ink);cursor:pointer;box-shadow:0 1px 4px rgba(0,0,0,.15)}
.mvp{position:absolute;z-index:7;left:8px;top:8px;bottom:8px;width:min(380px,calc(100% - 16px));overflow:auto;background:var(--sheet);border:1px solid var(--line);border-radius:6px;box-shadow:0 4px 18px rgba(0,0,0,.22);padding:10px 12px;font-size:14px}
.mvp h3{margin:0 0 6px;font-size:16px}.mvp .x{position:absolute;right:8px;top:6px;border:0;background:none;font-size:20px;cursor:pointer;color:var(--ink)}
.mvp label{display:block;margin:6px 0 2px}.mvp input,.mvp select{font:inherit;padding:3px 6px;border:1px solid var(--line);border-radius:4px;background:var(--paper);color:var(--ink);max-width:100%}
.mvp .row{display:flex;gap:6px;flex-wrap:wrap}.mvp .row>*{flex:1 1 0;min-width:0}.mvp input[type=number]{width:100%}
.mvp .ck{display:flex;gap:6px;align-items:flex-start;margin:4px 0}.mvp .ck input{margin-top:3px}
.mvp .ac{position:relative}.mvp .ac ul{position:absolute;z-index:9;left:0;right:0;top:100%;margin:0;padding:0;list-style:none;background:var(--sheet);border:1px solid var(--line);max-height:220px;overflow:auto}
.mvp .ac li{padding:4px 8px;cursor:pointer}.mvp .ac li:hover,.mvp .ac li.on{background:rgba(31,95,168,.12)}
.mvp .go{margin:10px 0 4px;font:inherit;padding:5px 16px;border-radius:14px;border:1px solid var(--ink);background:var(--ink);color:var(--paper);cursor:pointer}
.mvp table{border-collapse:collapse;width:100%;font-size:13px}.mvp td,.mvp th{border-bottom:1px solid var(--line);padding:2px 4px;text-align:left;vertical-align:top}
.mvp .res h4{margin:10px 0 4px;font-size:14px}.mvp .warn{color:#9b2d39}.mvp .hint{color:var(--muted);font-size:12px}
#map .mvl{fill:none;stroke:#b0122a;stroke-width:3.2px;vector-effect:non-scaling-stroke;stroke-linecap:round;stroke-linejoin:round;opacity:.9}
#map .mvw{fill:none;stroke:#1f5fa8;stroke-width:3px;vector-effect:non-scaling-stroke;stroke-dasharray:7 5;opacity:.9}
#map .mvc{fill:#fff;stroke:#b0122a;stroke-width:2px;vector-effect:non-scaling-stroke;cursor:pointer}#map .gmv{pointer-events:auto}
.mvp tr.hl td{background:rgba(176,18,42,.14)}.mvp .prof{width:100%;height:90px;display:block;margin:4px 0}.mvp .prof text{font-size:10px;fill:var(--muted)}
.mvp .mn{position:absolute;right:34px;top:6px;border:0;background:none;font-size:18px;cursor:pointer;color:var(--ink)}
.mvp .sl{display:none;margin:2px 0 0;font-size:13px;cursor:pointer}
.mvp.mini{bottom:auto;height:auto;overflow:hidden}.mvp.mini>*:not(h3):not(.x):not(.mn):not(.sl){display:none}.mvp.mini .sl{display:block}
@media (max-width:640px){.mvp{top:auto;height:58%;left:4px;right:4px;width:auto;bottom:4px}.mvp.mini{top:auto;bottom:4px;height:auto}.mvp input,.mvp select{font-size:16px}}`;document.head.appendChild(css);
const btn=document.createElement("button");btn.className="mvbtn";btn.type="button";btn.textContent=T.btn;box.appendChild(btn);
const P=document.createElement("div");P.className="mvp";P.hidden=true;box.appendChild(P);
const yNow=117;
P.innerHTML=`<button class="x" type="button" aria-label="${T.close}">×</button><button class="mn" type="button" aria-label="${T.mini}" aria-expanded="true">▾</button><h3>${T.title}</h3><p class="sl"></p>
<div class="ac"><label for="mvf">${T.from}</label><input id="mvf" placeholder="${T.ph}" autocomplete="off"><ul hidden></ul></div>
<div class="ac"><label for="mvt">${T.to}</label><input id="mvt" placeholder="${T.ph}" autocomplete="off"><ul hidden></ul></div>
<div class="ac"><label for="mvv">${T.via}</label><input id="mvv" placeholder="${T.phv}" autocomplete="off"><ul hidden></ul></div>
<label>${T.start}</label><div class="row"><select id="mve" aria-label="${T.era}"><option value="1">${T.ad}</option><option value="-1">${T.bc}</option></select><input id="mvy" type="number" min="1" max="700" value="${yNow}" aria-label="${T.year}"><select id="mvm" aria-label="${T.month}">${MON.map((m,i)=>`<option value="${i}"${i===4?" selected":""}>${m}</option>`).join("")}</select><input id="mvd" type="number" min="1" max="31" value="1" aria-label="${T.day}"></div>
<div class="row"><div><label for="mvi">${T.inf}</label><input id="mvi" type="number" min="0" step="100" value="5000"></div><div><label for="mvc">${T.cav}</label><input id="mvc" type="number" min="0" step="10" value="120"></div></div>
<div class="row"><div><label for="mvmu">${T.mules}</label><input id="mvmu" type="number" min="0" step="10" value="640"></div><div><label for="mvw">${T.wag}</label><input id="mvw" type="number" min="0" value="0"></div></div>
<label for="mvpace">${T.pace}</label><select id="mvpace"><option value="0">${T.p0}</option><option value="1">${T.p1}</option><option value="2">${T.p2}</option></select>
<label for="mvr">${T.rest}</label><input id="mvr" type="number" min="0" max="14" value="4">
<div class="ck"><input id="mvwa" type="checkbox" checked><label for="mvwa">${T.water}</label></div>
<div class="ck"><input id="mvwi" type="checkbox"><label for="mvwi">${T.winter}</label></div>
<div class="ck"><input id="mvh" type="checkbox"><label for="mvh">${T.hypo}</label></div>
<div class="ck"><input id="mvcp" type="checkbox" checked><label for="mvcp">${T.camp}</label></div>
<div class="ck"><input id="mvdt" type="checkbox" checked><label for="mvdt">${T.dated}</label></div>
<div class="ck"><input id="mvse" type="checkbox" checked><label for="mvse">${T.seas}</label></div>
<details><summary>${T.adv}</summary>
<div class="row"><div><label for="mvpo">${T.port}</label><input id="mvpo" type="number" min="0" step="0.5" value="1"></div><div><label for="mvo">${T.own}</label><input id="mvo" type="number" min="0" value="3"></div></div>
<div class="row"><div><label for="mvg">${T.grain}</label><input id="mvg" type="number" min="0" step="0.05" value="0.85"></div><div><label for="mvwt">${T.wat}</label><input id="mvwt" type="number" min="0" step="0.5" value="3"></div></div>
<div class="row"><div><label for="mvhf">${T.hfod}</label><input id="mvhf" type="number" min="0" value="11"></div><div><label for="mvmf">${T.mfod}</label><input id="mvmf" type="number" min="0" value="8"></div></div>
<div class="row"><div><label for="mvmc">${T.mcap}</label><input id="mvmc" type="number" min="0" value="90"></div><div><label for="mvwc">${T.wcap}</label><input id="mvwc" type="number" min="0" value="450"></div></div>
<div class="row"><div><label for="mvch">${T.campH}</label><input id="mvch" type="number" min="0" max="8" step="0.5" value="3"></div><div><label for="mvxh">${T.xh}</label><input id="mvxh" type="number" min="0" max="24" step="0.5" value="2"></div></div>
<div class="row"><div><label for="mvsz">${T.snowZ}</label><input id="mvsz" type="number" min="500" step="100" value="1500"></div><div><label for="mvmd">${T.mud}</label><input id="mvmd" type="number" min="0" max="60" value="15"></div></div>
<div class="row"><div><label for="mvht">${T.heat}</label><input id="mvht" type="number" min="30" max="100" value="80"></div><div><label for="mvhw">${T.hotW}</label><input id="mvhw" type="number" min="1" step="0.1" value="1.7"></div></div>
<div class="row"><div><label for="mvhg">${T.hg}</label><input id="mvhg" type="number" min="0" value="4"></div><div><label for="mvmg">${T.mg}</label><input id="mvmg" type="number" min="0" step="0.5" value="2.5"></div></div>
<div class="row"><div><label for="mvwd">${T.width}</label><input id="mvwd" type="number" min="1" value="6"></div><div><label for="mvss">${T.seaS}</label><input id="mvss" type="number" min="20" value="160"></div></div>
</details>
<button class="go" type="button">${T.calc}</button><div class="res" aria-live="polite"></div>`;
const $=id=>P.querySelector("#"+id);const RES=P.querySelector(".res");
btn.onclick=()=>{P.hidden=false;btn.hidden=true;getData();};
P.querySelector(".x").onclick=()=>{P.hidden=true;btn.hidden=false;};
const MN=P.querySelector(".mn"),SL=P.querySelector(".sl");const setMini=m=>{P.classList.toggle("mini",m);MN.textContent=m?"▴":"▾";MN.setAttribute("aria-label",m?T.maxi:T.mini);MN.setAttribute("aria-expanded",String(!m));};
MN.onclick=()=>setMini(!P.classList.contains("mini"));SL.onclick=()=>setMini(false);
const narrow=()=>window.matchMedia("(max-width:640px)").matches;
$("mvi").addEventListener("change",()=>{$("mvmu").value=Math.round((+$("mvi").value||0)/8);});
const SEL={mvf:null,mvt:null,mvv:null};
for(const id of ["mvf","mvt","mvv"]){const inp=$(id),ul=inp.parentNode.querySelector("ul");let res=[];
 inp.addEventListener("input",async()=>{SEL[id]=null;await getData();const q=nrm(inp.value.trim());if(q.length<2){ul.hidden=true;return;}
  res=[];for(const e of IDX){const ks=[e[0],e[1],...(e[3]||"").split("|")].filter(Boolean).map(nrm);let sc=-1;for(const k of ks){if(k===q){sc=3;break;}if(k.startsWith(q))sc=Math.max(sc,2);else if(k.includes(q))sc=Math.max(sc,1);}
   if(sc>0)res.push([sc,e]);}
  res.sort((a,b)=>b[0]-a[0]||a[1][0].length-b[1][0].length);res=res.slice(0,8).map(r=>r[1]);
  ul.innerHTML=res.map((e,i)=>`<li data-i="${i}">${esc(e[0]||e[1])}${e[1]&&e[0]?` <span class="hint">(${esc(e[1])})</span>`:""}</li>`).join("");ul.hidden=!res.length;});
 ul.addEventListener("mousedown",ev=>{const li=ev.target.closest("li");if(!li)return;ev.preventDefault();const e=res[+li.dataset.i];SEL[id]=e;inp.value=e[0]||e[1];ul.hidden=true;});
 inp.addEventListener("blur",()=>setTimeout(()=>ul.hidden=true,150));}
const gMv=el("g",{class:"gmv"});svg.insertBefore(gMv,gSet);
// ---- útvonalkeresés ----
const PACE=[[4.7,5],[5.7,5],[5.7,7]];
function prm(){const p={inf:+$("mvi").value||0,cav:+$("mvc").value||0,mules:+$("mvmu").value||0,wag:+$("mvw").value||0,pace:+$("mvpace").value,rest:+$("mvr").value||0,
 water:$("mvwa").checked,winter:$("mvwi").checked,hypo:$("mvh").checked,port:+$("mvpo").value||0,own:+$("mvo").value||0,grain:+$("mvg").value||0,wat:+$("mvwt").value||0,
 hf:+$("mvhf").value||0,mf:+$("mvmf").value||0,mc:+$("mvmc").value||0,wc:+$("mvwc").value||0,wd:Math.max(1,+$("mvwd").value||6),sea:Math.max(20,+$("mvss").value||160),
 seas:$("mvse").checked,snowZ:+$("mvsz").value||1500,mud:Math.min(60,Math.max(0,+$("mvmd").value||0))/100,heat:Math.min(100,Math.max(30,+$("mvht").value||80))/100,hotW:Math.max(1,+$("mvhw").value||1.7),
 hg:+$("mvhg").value||0,mg:+$("mvmg").value||0,camp:$("mvcp").checked,campH:Math.max(0,+$("mvch").value||0),dated:$("mvdt").checked,year:(+$("mve").value<0?1-(+$("mvy").value||1):(+$("mvy").value||117)),xh:Math.max(0,+$("mvxh").value||0)};
 let[v,h]=PACE[p.pace];if(p.inf===0&&p.cav>0)v=7;if(p.wag>0)v=Math.min(v,3.5);p.v=v;p.rh=h;
 p.colM=p.inf/p.wd*1.5+p.cav/4*3+p.mules/2*3+p.wag*10;p.passH=p.colM/1000/p.v;return p;}
const slopeF=s=>Math.max(.45,Math.exp(-3.5*Math.tan(Math.min(30,s)*Math.PI/180)));
const certF=[1,.95,.85];
const rel=(e,dir)=>e[3]===0&&e.length>8?(dir===-1?e[9]:e[8]):1;
// ---- évszakhatások (v149; becsült szabályok, a panelen állíthatók) ----
const monOf=t=>fromJd(Math.floor(t))[1];
const lonOf=(x,y)=>15+x/(111.2*Math.cos(latOf(y)*Math.PI/180));
const isHot=(lat,m)=>(m>=5&&m<=7&&lat<38)||((m===4||m===8)&&lat<33);
const isWet=(lat,m)=>lat>=45?[9,10,11,0,1,2,3].includes(m):lat>=37?[10,11,0,1,2].includes(m):[11,0,1].includes(m);
const isGraze=(lat,m)=>lat>=42?(m>=3&&m<=9):lat>=34?((m>=2&&m<=5)||m===9||m===10):(m<=3);
const snowShut=(p,z,m)=>p.seas&&z>=p.snowZ&&(m===11||m<=3);
function mudF(p,ce,lat,m){if(!p.seas||!isWet(lat,m))return 1;return 1-p.mud*[1/3,1,5/3][ce];}
// Vegetius „nyári órái”: Róma szélességén nyár közepén egy római óra kb. 1,25 mai óra (5 nyári óra ≈ 6¼ óra)
const SUMH=1.25;
function hoursOf(p,lat,J){const m=monOf(J);return p.rh*SUMH*(p.seas&&isHot(lat,m)?p.heat:1);}
// menettábor és oszlophossz: az oszlop végének is be kell érnie, és napnyugtáig tábort kell verni
function capOf(p,lat,J){return daylight(lat,J)-(p.camp?Math.max(p.passH,p.campH):p.passH);}
function dayHours(p,lat,J){return Math.max(.5,Math.min(hoursOf(p,lat,J),capOf(p,lat,J)));}
function riverF(p,k,lat,lon,m){if(!p.seas)return 1;const nile=lat<31.6&&lon>29&&lon<34;
 if(nile){if(m>=7&&m<=9)return k===5?1.3:1;if(m>=3&&m<=5)return .8;return 1;}
 if(lat>=44&&(m===11||m<=1))return 0; if(lat>=40&&(m===7||m===8))return .8; return 1;}
function seaF(p,lon,dx,dy,J){const ss=seaSeason(J);if(ss===2&&!p.winter)return 0;let f=ss===2?.7:ss===1?.9:1;
 const m=monOf(J);if(p.seas&&m>=4&&m<=8&&lon>10){const L=Math.hypot(dx,dy)||1;f*=1+.3*((dx*.34-dy*.94)/L);}return p.seas||ss===2?f:(ss===2?.7:1);}
function edgeDays(e,p,dir,t,ei){const k=e[3],km=e[2],a=NET.n[dir===1?e[0]:e[1]],b=NET.n[dir===1?e[1]:e[0]];const lat=latOf(a[1]),m=monOf(t);
 if(k===0||k===1){if(k===0&&e.length>8&&snowShut(p,e[12],m))return Infinity;let d=km/(p.v*rel(e,dir)*certF[e[6]]*mudF(p,e[6],lat,m))/dayHours(p,lat,t);if(p.hypo&&e[6]===2)d*=3;if(k===0&&ei!=null&&p.xh>0){const u=nUnb(ei);if(u)d+=u*p.xh/dayHours(p,lat,t);}return d;}
 if(k===2)return km/(p.v*dayHours(p,lat,t))+p.port/2;
 if(k===3||k===4){const f=seaF(p,lonOf(a[0],a[1]),b[0]-a[0],b[1]-a[1],t);return f>0?km/(p.sea*f):Infinity;}
 if(k===5||k===6){const f=riverF(p,k,lat,lonOf(a[0],a[1]),m);return f>0?km/((k===5?65:15)*f):Infinity;}
 if(k===7)return km/75+.1;}
function nearestNode(x,y){let b=-1,bd=1e18;const n=NET.n;for(let i=0;i<NET.nr;i++){const dx=n[i][0]-x,dy=n[i][1]-y,d=dx*dx+dy*dy;if(d<bd){bd=d;b=i;}}return [b,Math.sqrt(bd)];}
function dijkstra(s,t,p,J0){const N=NET.n.length,D=new Float64Array(N).fill(Infinity),PE=new Int32Array(N).fill(-1),PD=new Int8Array(N);const rr=p.rest>0?1+1/p.rest:1;
 const H=[];const push=(d,v)=>{H.push([d,v]);let i=H.length-1;while(i){const j=(i-1)>>1;if(H[j][0]<=H[i][0])break;[H[i],H[j]]=[H[j],H[i]];i=j;}};
 const pop=()=>{const r=H[0],l=H.pop();if(H.length){H[0]=l;let i=0;for(;;){const a=2*i+1,b=a+1;let m=i;if(a<H.length&&H[a][0]<H[m][0])m=a;if(b<H.length&&H[b][0]<H[m][0])m=b;if(m===i)break;[H[i],H[m]]=[H[m],H[i]];i=m;}}return r;};
 D[s]=0;push(0,s);
 while(H.length){const[d,u]=pop();if(d>D[u])continue;if(u===t)break;
  for(const[k,dir]of ADJ[u]){const e=NET.e[k],kd=e[3];if(kd>=2&&!p.water)continue;if(kd===0&&p.dated&&!roadOK(k,p.year))continue;
   const c=edgeDays(e,p,dir,J0+d*rr,k);if(!(c<Infinity))continue;const v=dir===1?e[1]:e[0],nd=d+c;if(nd<D[v]){D[v]=nd;PE[v]=k;PD[v]=dir;push(nd,v);}}}
 if(D[t]===Infinity)return null;const path=[];let v=t;while(v!==s){const k=PE[v];path.push([k,PD[v]]);const e=NET.e[k];v=PD[v]===1?e[0]:e[1];}return path.reverse();}
const pts=s=>s.trim().split(" ").map(q=>q.split(",").map(Number));
function geom(k,dir){const e=NET.e[k];const A=NET.n[e[0]],B=NET.n[e[1]];let g;
 if(e[3]===0&&RG[e[4]])g=pts(RG[e[4]]);else if(e[3]>=3)g=pts(NET.w[e[4]]);else g=[A.slice(),B.slice()];
 const d0=Math.hypot(g[0][0]-A[0],g[0][1]-A[1]),d1=Math.hypot(g[g.length-1][0]-A[0],g[g.length-1][1]-A[1]);if(d1<d0)g.reverse();
 g[0]=A.slice();g[g.length-1]=B.slice();if(dir===-1)g.reverse();return g;}
function along(g,f){let L=0;const s=[0];for(let i=1;i<g.length;i++){L+=Math.hypot(g[i][0]-g[i-1][0],g[i][1]-g[i-1][1]);s.push(L);}const t=f*L;
 for(let i=1;i<g.length;i++)if(s[i]>=t){const r=(t-s[i-1])/((s[i]-s[i-1])||1);return [g[i-1][0]+(g[i][0]-g[i-1][0])*r,g[i-1][1]+(g[i][1]-g[i-1][1])*r];}return g[g.length-1];}
let GRID=null;function nearPlace(x,y,max=12){if(!GRID){GRID=new Map();IDX.forEach(e=>{const k=Math.floor(e[4]/20)+"_"+Math.floor(e[5]/20);(GRID.get(k)||GRID.set(k,[]).get(k)).push(e);});}
 let b=null,bd=max;const gx=Math.floor(x/20),gy=Math.floor(y/20);for(let i=-1;i<=1;i++)for(let j=-1;j<=1;j++)for(const e of GRID.get((gx+i)+"_"+(gy+j))||[]){const d=Math.hypot(e[4]-x,e[5]-y);const w=e[7]==="city"||e[7]==="leg"||e[7]==="civ"?.6:e[7]==="fort"?.8:e[7]==="camp"||e[7]==="fortlet"?1.5:1;if(d*w<bd){bd=d*w;b=e;}}return b;}
// ---- számítás ----
P.querySelector(".go").onclick=async()=>{RES.innerHTML=`<p class="hint">${T.loading}</p>`;await getData();const p=prm();
 const A=SEL.mvf,B=SEL.mvt;if(!A||!B){RES.innerHTML=`<p class="warn">${T.noPlace}</p>`;return;}
 const yIn=Math.max(1,+$("mvy").value||117),y=+$("mve").value<0?1-yIn:yIn,m=+$("mvm").value,d=Math.min(Math.max(1,+$("mvd").value||1),mlen(y,m));const J0=jd(y,m,d);
 const lat0=latOf(A[5]);const ss=seaSeason(J0),seaOK=p.water&&(ss<2||p.winter);
 const[sa,da]=nearestNode(A[4],A[5]),[sb,db]=nearestNode(B[4],B[5]);
 const V=SEL.mvv;const sv=V?nearestNode(V[4],V[5])[0]:-1;
 const run=pp=>{if(sv<0)return dijkstra(sa,sb,pp,J0);const p1=dijkstra(sa,sv,pp,J0);if(!p1)return null;let t=J0;for(const[k,dir]of p1)t+=edgeDays(NET.e[k],pp,dir,t,k);const p2=dijkstra(sv,sb,pp,t);return p2?p1.concat(p2):null;};
 const kmOf=x=>x.reduce((t,[k])=>t+NET.e[k][2],0);
 let path=run(p),dateFb=false,dateLong=0;if(!path&&p.dated){path=run(Object.assign({},p,{dated:false}));dateFb=!!path;}
 else if(path&&p.dated){const q=run(Object.assign({},p,{dated:false}));if(q){const a1=kmOf(path),a2=kmOf(q);if(a1>a2*1.03+5)dateLong=a1-a2;}}
 let det=null;if(path&&p.seas){const m0=monOf(J0);if(m0===11||m0<=4){const p2=Object.assign({},p,{snowZ:1e9}),q=run(p2);if(q){const km=x=>x.reduce((t,[k])=>t+NET.e[k][2],0),k1=km(path),k2=km(q);let zx=0;for(const[k]of q){const e=NET.e[k];if(e[3]===0&&e.length>8)zx=Math.max(zx,e[12]);}if(k2<.85*k1&&zx>=p.snowZ)det={k1,k2,zx};}}}if(!path){RES.innerHTML=`<p class="warn">${T.noRoute}</p>`;return;}
 // szakaszok
 const legs=[];if(da>0.3)legs.push({k:1,km:da,g:[[A[4],A[5]],NET.n[sa]],sl:0,ce:1,snap:A,nb:sa});
 for(const[k,dir]of path){const e=NET.e[k];legs.push({ei:k,na:dir===1?e[0]:e[1],nb:dir===1?e[1]:e[0],k:e[3],km:e[2],g:geom(k,dir),sl:e[5],ce:e[6],rf:rel(e,dir),up:e[3]===0&&e.length>8?(dir===-1?e[11]:e[10]):0,dn:e[3]===0&&e.length>8?(dir===-1?e[10]:e[11]):0,zx:e[3]===0&&e.length>8?e[12]:0});}
 if(db>0.3)legs.push({k:1,km:db,g:[NET.n[sb],[B[4],B[5]]],sl:0,ce:1,snap:B,na:sb});
 // idővonal
 let J=J0,march=0,rests=0,sea=0,DAYS=[],cur={km:0,note:[]},hLeft=null,mdCount=0;const kmT={road:0,ship:0,river:0,hyp:0,up:0};const W=[];
 let curXY=[A[4],A[5]];const SE={hot:0,wet:0,graze:0};let seaN=0,seaLo=0,seaHi=0;const XL=[];
 let nShort=0;const newDay=()=>{const la=latOf(curXY[1]);hLeft=dayHours(p,la,J);cur.short=capOf(p,la,J)<hoursOf(p,la,J);};
 const closeDay=(note,pos)=>{const P2=pos||curXY,lat=latOf(P2[1]),mm=monOf(J);DAYS.push({J,km:cur.km,up:cur.up||0,dn:cur.dn||0,zx:cur.zx||0,pos:P2,note:[...cur.note,...(note?[note]:[])],
   short:!!cur.short&&cur.km>0,hot:p.seas&&isHot(lat,mm),wet:p.seas&&isWet(lat,mm),graze:p.seas&&isGraze(lat,mm)});cur={km:0,note:[]};J++;};
 newDay();let marchedToday=false;
 for(const L of legs){const isW=L.k>=3;
  if(isW){ if(marchedToday){closeDay("",curXY);mdCount++;marchedToday=false;newDay();}
   const ssn=seaSeason(J);if(L.k===3||L.k===4){if(ssn===2)W.push(T.wSea.replace("{d}",dstr(J)));else if(ssn===1)W.push(T.wSeaU.replace("{d}",dstr(J)));kmT.ship+=L.km;}else{kmT.river+=L.km;if(L.k===6)kmT.up+=L.km;}
   const a=L.g[0],b=L.g[L.g.length-1],lat=latOf(a[1]),lon=lonOf(a[0],a[1]),mm=monOf(J);
   let f=L.k===3||L.k===4?seaF(p,lon,b[0]-a[0],b[1]-a[1],J):L.k===7?1:riverF(p,L.k,lat,lon,mm);if(!(f>0)){f=.5;W.push(T.wRivIce.replace("{d}",dstr(J)));}
   if(p.seas&&(L.k===3||L.k===4)&&mm>=4&&mm<=8&&lon>10&&f<.95)W.push(T.wEtes);
   const dd=L.k===3||L.k===4?L.km/(p.sea*f):L.k===5?L.km/(65*f):L.k===6?L.km/(15*f):L.km/75+.1;const n=Math.max(1,Math.ceil(dd-1e-9));if(L.k===3||L.k===4){seaN+=n;seaLo+=Math.max(1,Math.ceil(dd/1.4-1e-9));seaHi+=Math.ceil(dd/.55-1e-9);}
   for(let i=0;i<n;i++){cur.km=L.km/n;curXY=along(L.g,(i+1)/n);cur.note.push(T.shipN);closeDay("",curXY);sea++;}
   newDay();continue;}
  if(L.k===2&&p.port>0){ // kikötői átszállás: behajózás / kirakodás
   if(marchedToday){closeDay("",curXY);mdCount++;marchedToday=false;}
   const n=Math.ceil(p.port/2-1e-9);for(let i=0;i<n;i++){cur.note.push(T.embN);closeDay("",curXY);sea++;}newDay();
   kmT.road+=L.km;curXY=along(L.g,1);continue;}
  if(L.k<=2){kmT.road+=L.km;if(L.ce===2)kmT.hyp+=L.km;if(L.snap&&L.km>=1)W.push(T.wSnap.replace("{w}",esc(L.snap[0])).replace("{k}",fmt(L.km)));}
  if(L.zx&&snowShut(p,L.zx,monOf(J)))W.push(T.wSnowIn.replace("{z}",fmt(Math.round(L.zx/50)*50)).replace("{d}",dstr(J)));
  if(L.ei!=null&&NET._xc.has(L.ei)){for(const[ri,bi]of NET._xc.get(L.ei)){XL.push([ri,bi]);cur.note.push(bi>=0?T.xBr.replace("{r}",rvName(ri)).replace("{b}",NET.br[bi][0]):T.xNo.replace("{r}",rvName(ri)).replace("{h}",fmt(p.xh,1)));
   if(bi<0&&p.xh>0){let need=p.xh;while(need>1e-6){if(hLeft>=need){hLeft-=need;need=0;}else{need-=hLeft;hLeft=0;closeDay("",curXY);mdCount++;march++;marchedToday=false;if(p.rest>0&&march%p.rest===0){cur.note.push(T.restN);closeDay("",curXY);rests++;}newDay();}}marchedToday=true;}}}
  let rem=L.km,done=0;const addR=x=>{if(!L.km)return;cur.up=(cur.up||0)+(L.up||0)*x/L.km;cur.dn=(cur.dn||0)+(L.dn||0)*x/L.km;if(L.zx)cur.zx=Math.max(cur.zx||0,L.zx);};
  kmT.up2=(kmT.up2||0)+(L.up||0);kmT.dn2=(kmT.dn2||0)+(L.dn||0);if(L.zx>(kmT.zx||0))kmT.zx=L.zx;
  while(rem>1e-6){const v=p.v*(L.rf||1)*certF[L.ce]*mudF(p,L.ce,latOf(curXY[1]),monOf(J));const can=hLeft*v;
   if(can>=rem-1e-6){hLeft-=rem/v;cur.km+=rem;addR(rem);done+=rem;rem=0;curXY=along(L.g,1);marchedToday=true;}
   else{cur.km+=can;addR(can);done+=can;rem-=can;curXY=along(L.g,done/L.km);marchedToday=true;closeDay("",curXY);mdCount++;march++;marchedToday=false;
    if(p.rest>0&&march%p.rest===0){cur.note.push(T.restN);closeDay("",curXY);rests++;}newDay();}}}
 if(marchedToday||!DAYS.length){closeDay(T.arrN,curXY);march++;}else DAYS[DAYS.length-1].note.push(T.arrN);
 const Jend=DAYS[DAYS.length-1].J;
 for(const D of DAYS){if(D.short)nShort++;if(D.hot)SE.hot++;if(D.wet&&D.km>0&&!D.note.includes(T.shipN))SE.wet++;if(D.graze)SE.graze++;}
 // oszlop és ellátás
 const colM=p.colM,passH=p.passH;

 if(p.water&&!seaOK)W.unshift(T.wClosed);if(dateFb)W.unshift(T.wDatedFb.replace("{y}",p.year));if(dateLong)W.push(T.wDatedL.replace("{y}",p.year).replace("{k}",fmt(dateLong)));if(det)W.unshift(T.wSnowDet.replace("{k2}",fmt(det.k2)).replace("{z}",fmt(Math.round(det.zx/50)*50)).replace("{k1}",fmt(det.k1)));for(const D of DAYS){const mm=fromJd(D.J)[1];if(D.zx>=1200&&(mm>=10||mm<=3)){W.push(T.wPass.replace("{z}",fmt(Math.round(D.zx/50)*50)).replace("{d}",dstr(D.J)));break;}}if(kmT.hyp>0)W.push(T.wHyp.replace("{p}",fmt(100*kmT.hyp/Math.max(1,kmT.road))));if(kmT.up>0)W.push(T.wUp.replace("{k}",fmt(kmT.up)));
 const men=p.inf+p.cav,gD=men*p.grain,nd=DAYS.length;
 const fFull=p.cav*p.hf+p.mules*p.mf+p.wag*2*15,fGraze=p.cav*p.hg+p.mules*p.mg+p.wag*2*3,wBase=men*p.wat+(p.cav+p.mules)*25+p.wag*2*40;
 let fTot=0,wTot=0;for(const D of DAYS){fTot+=D.graze?fGraze:fFull;wTot+=D.hot?wBase*p.hotW:wBase;}
 const fD=fTot/nd,wD=wTot/nd;
 const loadKg=p.mules*p.mc+p.wag*p.wc,needD=gD+fD,carryD=p.own+(needD>0?loadKg/needD:0);
 // mobilon az eredmény után összecsukjuk a panelt, hogy az útvonal látsszon
 SL.textContent=`${A[0]||A[1]} → ${B[0]||B[1]}: ${fmt(Jend-J0+1)} ${T.cal}, ${T.arr.toLowerCase()} ${dstr(Jend)} ▴`;if(narrow())setMini(true);
 // rajz
 gMv.innerHTML="";let bb=[1e9,1e9,-1e9,-1e9];
 for(const L of legs){const dd="M"+L.g.map(q=>q[0].toFixed(2)+" "+(-q[1]).toFixed(2)).join("L");el("path",{class:L.k>=3?"mvw":"mvl",d:dd},gMv);for(const q of L.g){bb[0]=Math.min(bb[0],q[0]);bb[1]=Math.min(bb[1],q[1]);bb[2]=Math.max(bb[2],q[0]);bb[3]=Math.max(bb[3],q[1]);}}
 DAYS.forEach((D,i)=>{const c=el("circle",{class:"mvc",cx:D.pos[0],cy:-D.pos[1],r:Math.max(1.5,(bb[2]-bb[0])/300)},gMv);const t=el("title",{},c);t.textContent=`${i+1}. ${dstr(D.J)} – ${fmt(D.km)} km`;
  c.addEventListener("click",ev=>{ev.stopPropagation();setMini(false);const tr=RES.querySelector(`tr[data-d="${i}"]`);if(tr){RES.querySelectorAll("tr.hl").forEach(x=>x.classList.remove("hl"));tr.classList.add("hl");tr.scrollIntoView({block:"center",behavior:"smooth"});}});});
 {const r=svg.getBoundingClientRect(),pr=P.getBoundingClientRect(),asp=(r.height||1)/(r.width||1);let w=Math.max(60,(bb[2]-bb[0])*1.3),h=Math.max(60,(bb[3]-bb[1])*1.3);
 const side=pr.bottom>=r.bottom-16&&pr.top>r.top+20&&pr.width>r.width*.6?"b":"l";const f=side==="l"?Math.min(.7,Math.max(0,(pr.right-r.left)/r.width)):Math.min(.7,Math.max(0,(r.bottom-pr.top)/r.height));
 if(side==="l"){w=Math.max(w,h/asp)/(1-f);h=w*asp;const x0=bb[2]+(bb[2]-bb[0])*.15-w;setVBnow([x0,-(bb[1]+bb[3])/2-h/2,w,h]);}
 else{h=Math.max(h,w*asp)/(1-f);w=h/asp;setVBnow([(bb[0]+bb[2])/2-w/2,-(bb[1]+bb[3])/2-h*(1-f)/2,w,h]);}}
 // magassági profil: csomópont-magasságok és a szakaszok legmagasabb pontja; tengeri szakasz 0 m
 const PR=[];{let cum=0;const zn=i=>i==null?null:i<NET.nr?NET.z?.[i]??null:0;
  for(const L of legs){const za=zn(L.na),zb=zn(L.nb);if(!PR.length&&za!=null)PR.push([0,za]);
   if(L.k>=3){if(!PR.length)PR.push([cum,0]);PR.push([cum+L.km,0]);cum+=L.km;continue;}
   if(L.zx&&za!=null&&zb!=null&&L.zx>Math.max(za,zb)+50)PR.push([cum+L.km/2,L.zx]);cum+=L.km;if(zb!=null)PR.push([cum,zb]);}}
 let PROF="";if(PR.length>2){const X=PR[PR.length-1][0]||1,Zm=Math.max(100,...PR.map(q=>q[1])),w=300,h=80,sx=x=>(x/X*(w-30)+28).toFixed(1),sy=z=>(h-12-z/Zm*(h-22)).toFixed(1);
  const pl=PR.map(q=>sx(q[0])+","+sy(q[1])).join(" ");const im=PR.reduce((a,q,i)=>q[1]>PR[a][1]?i:a,0);
  PROF=`<svg class="prof" viewBox="0 0 ${w} ${h}" preserveAspectRatio="none" role="img" aria-label="${T.prof}"><polygon points="${sx(0)},${sy(0)} ${pl} ${sx(X)},${sy(0)}" fill="rgba(176,18,42,.15)"/><polyline points="${pl}" fill="none" stroke="#b0122a" stroke-width="1.2" vector-effect="non-scaling-stroke"/><line x1="28" x2="${w}" y1="${sy(0)}" y2="${sy(0)}" stroke="currentColor" stroke-opacity=".3"/><text x="0" y="${+sy(Zm)+3}">${fmt(Math.round(Zm/10)*10)} m</text><text x="0" y="${sy(0)}">0 m</text><text x="${w-2}" y="${h-1}" text-anchor="end">${fmt(X)} km</text><text x="28" y="${h-1}">0</text></svg><p class="hint">${T.prof}</p>`;}
 // eredmény
 const tot=kmT.road+kmT.ship+kmT.river;
 let H=`<h4>${T.sum}</h4><p><b>${esc(A[0]||A[1])} → ${esc(B[0]||B[1])}</b><br>${T.dist}: <b>${fmt(tot)} km</b> (${T.road} ${fmt(kmT.road)}${kmT.ship?`, ${T.ship} ${fmt(kmT.ship)}`:""}${kmT.river?`, ${T.river} ${fmt(kmT.river)}`:""} km)<br>
 ${fmt(march)} ${T.mdays}, ${fmt(rests)} ${T.rdays}${sea?`, ${fmt(sea)} ${T.sdays}`:""}<br>
 ${sea&&seaN?`<span class="hint">${T.seaR.replace("{a}",seaLo).replace("{b}",seaHi).replace("{n}",seaN).replace("{d1}",dstr(Jend+seaLo-seaN)).replace("{d2}",dstr(Jend+seaHi-seaN))}</span><br>`:""}
 ${T.dep}: ${dstr(J0)} <span class="hint">(${romanDate(...fromJd(J0))})</span><br>${T.arr}: <b>${dstr(Jend)}</b> <span class="hint">(${romanDate(...fromJd(Jend))})</span><br>${T.total}: ${fmt(Jend-J0+1)} ${T.cal}</p>
${PROF} ${kmT.up2?`<p>${T.relief.replace("{u}",fmt(Math.round(kmT.up2/10)*10)).replace("{d}",fmt(Math.round(kmT.dn2/10)*10)).replace("{z}",fmt(Math.round((kmT.zx||0)/50)*50))}</p>`:""}<h4>${T.col}</h4><p>${T.colL} ${fmt(colM/1000,1)} km; ${T.pass} ${fmt(passH,1)} ${T.h}. ${(nShort?(p.camp?T.campS:T.tailS).replace("{n}",nShort):(p.camp?T.campOK:T.tailOK)).replace("{c}",fmt(p.campH,1))}</p>
 <h4>${T.log}</h4><table><tr><th></th><th>${T.perday}</th><th>${T.trip}</th></tr>
 <tr><td>${T.grainT}</td><td>${fmt(gD/1000,1)} ${T.t}</td><td>${fmt(gD*nd/1000)} ${T.t}</td></tr>
 <tr><td>${T.fodT}</td><td>${fmt(fD/1000,1)} ${T.t}</td><td>${fmt(fTot/1000)} ${T.t}</td></tr>
 <tr><td>${T.waterT}</td><td>${fmt(wD/1000,1)} ${T.m3}</td><td>${fmt(wTot/1000)} ${T.m3}</td></tr></table>
 <p>${T.carry.replace("{d}",fmt(carryD,1))}</p>`+(p.seas?`<h4>${T.seasH}</h4><p>${T.seasP.replace("{w}",SE.wet).replace("{h}",SE.hot).replace("{g}",SE.graze).replace("{n}",nd).replace("{s}",fmt(p.snowZ))}</p>`:"");
 if(XL.length){const nb=XL.filter(x=>x[1]>=0).length;H+=`<h4>${T.xH}</h4><p>${T.xP.replace("{n}",XL.length).replace("{b}",nb).replace("{h}",fmt(p.xh,1))}</p>`;}
 if(W.length)H+=`<h4>${T.warn}</h4><ul>${[...new Set(W)].map(x=>`<li class="warn">${x}</li>`).join("")}</ul>`;
 H+=`<h4>${T.days}</h4><table><tr>${T.dcol.map(c=>`<th>${c}</th>`).join("")}</tr>`+DAYS.map((D,i)=>{const pl=nearPlace(D.pos[0],D.pos[1]);
  return `<tr data-d="${i}"><td>${i+1}</td><td>${dstr(D.J)}</td><td>${D.km>0?fmt(D.km):""}</td><td>${D.up>=10?fmt(D.up):""}</td><td>${pl?esc(pl[0]||pl[1]):T.none}</td><td>${[...new Set(D.note)].map(esc).join(", ")}</td></tr>`;}).join("")+`</table>`;
 H+=`<p class="hint">${T.assume.replace("{v}",fmt(p.v,1)).replace("{h}",p.rh)}</p>`;RES.innerHTML=H;};
// ---- külső hozzáférés (Caesar-séták) ----
window.MV={ready:()=>getData(),
 route(ax,ay,bx,by,water){const p=prm();p.water=!!water;p.dated=false;p.seas=false;p.hypo=false;p.winter=true;const[sa]=nearestNode(ax,ay),[sb]=nearestNode(bx,by);
  const path=dijkstra(sa,sb,p,jd(117,5,1));if(!path)return [[[ax,ay],[bx,by]]];const g=[[[ax,ay],NET.n[sa].slice()]];for(const[k,dir]of path)g.push(geom(k,dir));g.push([NET.n[sb].slice(),[bx,by]]);return g;},
 async calc(c){btn.click();await getData();setMini(false);SEL.mvf=c.f;$("mvf").value=c.f[0];SEL.mvt=c.to;$("mvt").value=c.to[0];SEL.mvv=null;$("mvv").value="";
  const[y,m,d]=c.J;$("mve").value=y<=0?"-1":"1";$("mvy").value=y<=0?1-y:y;$("mvm").value=m;$("mvd").value=d;
  const nInf=c.inf!=null?c.inf:c.leg*5000,k=nInf/5000;$("mvi").value=nInf;$("mvc").value=c.cav!=null?c.cav:Math.round(k*120);$("mvmu").value=c.mules!=null?c.mules:Math.round(k*640);if(c.pace!=null)$("mvpace").value=c.pace;$("mvw").value=0;$("mvwa").checked=!!c.sea;$("mvdt").checked=false;
  P.querySelector(".go").click();P.scrollTop=0;}};
})();
