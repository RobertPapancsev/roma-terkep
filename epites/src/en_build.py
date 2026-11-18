# v60: angol oldal építése. Bemenet: body_v60pre.html, en/units.json, en/out_NN.json  ->  body_en.html, en.html
import json,re,glob,sys
S=open('body_v60pre.html',encoding='utf8').read()
D=json.load(open('en/units.json',encoding='utf8'));U={u["id"]:u for u in D["units"]}
E={}
for f in sorted(glob.glob('en/out_*.json')):
    for r in json.load(open(f,encoding='utf8')): E[r["id"]]=r["e"]
for f in sorted(glob.glob('en/fix_*.json')):
    for r in json.load(open(f,encoding='utf8')): E[r["id"]]=r["e"]
miss=[i for i in U if i not in E or not str(E[i]).strip()];assert not miss,miss[:10]
# --- ellenőrzés: HTML-egységek címkesora
def tags(h):
    t=re.findall(r'<[^>]+>',h)
    return [re.sub(r'\s(aria-label|placeholder|title|alt)="[^"]*"','',x) for x in t]
bad=[]
for i,u in U.items():
    if u["kind"]=="html":
        if tags(u["t"])!=tags(E[i]) or '`' in E[i] or '${' in E[i]: bad.append(i)
        if len(u["t"])-len(u["t"].lstrip())!=len(E[i])-len(E[i].lstrip()): E[i]=u["t"][:len(u["t"])-len(u["t"].lstrip())]+E[i].lstrip()
print('html-eltérés:',bad)
# --- behelyettesítés hátulról
for s,e,uid,mode in sorted(D["occ"],key=lambda o:-o[0]):
    S=S[:s]+(json.dumps(E[uid],ensure_ascii=False) if mode=='js' else E[uid])+S[e:]
def rp(a,b,n=None):
    global S
    c=S.count(a)
    assert c>=1 and (n is None or c==n),(a[:70],c)
    S=S.replace(a,b)
rp('<html lang="hu">','<html lang="en">',1);rp('toLocaleString("hu-HU")','toLocaleString("en-US")');rp('<title>Az ókori Róma térképe</title>','<title>Map of Ancient Rome</title>',1)
rp('"100 római láb = 29,6 m"','"100 Roman feet = 29.6 m"',1);rp('"1 actus = 120 láb = 35,5 m"','"1 actus = 120 feet = 35.5 m"',1);rp('n.textContent="É";','n.textContent="N";',1)
rp('const TDL={A:"áll",R:"rom",U:"föld alatt / zárt térben látogatható",N:"nem látható (nyoma sincs vagy nem hozzáférhető)"};','const TDL={A:"standing",R:"ruin",U:"underground / indoors, can be visited",N:"not visible (no trace, or not accessible)"};',1)
rp('const PERIODS={k1:"Vaskor és királykor",k2:"Köztársaság",k3:"Korai császárkor",k4:"Késő császárkor",k5:"Kora középkor"};','const PERIODS={k1:"Iron Age and Regal period",k2:"Republic",k3:"Early Empire",k4:"Late Empire",k5:"Early Middle Ages"};',1)
rp('y<0?`Kr. e. ${-y}`:`Kr. u. ${y}`','y<0?`${-y} BC`:`AD ${y}`',2)
rp('`<span class="pill ruinp">használatban kb. ${fmtY(m.to)}-ig</span>`','`<span class="pill ruinp">in use until c. ${fmtY(m.to)}</span>`',1)
rp('" · betöltés…"','" · loading…"',1);rp('"Vatikánváros területére a SITAR nem tartalmaz adatot"','"SITAR has no data for Vatican City"',1)
rp('return"latiumi kultúra, "+s.slice(16)+" periódus";','return"Latial culture, period "+s.slice(16);',1)
rp('const era=x=>x==="a"?"Kr. e. ":"Kr. u. ";','const era=x=>x==="a"?" BC":" AD";const rn=r=>{const v={I:1,V:5,X:10};let n=0;for(let i=0;i<r.length;i++){const a=v[r[i]],b=v[r[i+1]]||0;n+=a<b?-a:a;}return n+(n%10===1&&n!==11?"st":n%10===2&&n!==12?"nd":n%10===3&&n!==13?"rd":"th");};',1)
rp('if(m)return era(m[3])+m[2]+". század "+({"Fine":"vége","Inizio":"eleje","Metà":"közepe","Prima metà":"első fele","Seconda metà":"második fele","Primo quarto":"első negyede","Secondo quarto":"második negyede","Terzo quarto":"harmadik negyede"})[m[1]];',
   'if(m)return ({"Fine":"late","Inizio":"early","Metà":"mid","Prima metà":"first half of the","Seconda metà":"second half of the","Primo quarto":"first quarter of the","Secondo quarto":"second quarter of the","Terzo quarto":"third quarter of the"})[m[1]]+" "+rn(m[2])+" century"+era(m[3]);',1)
rp('if(m)return era(m[2])+m[1]+". század";return s;}','if(m)return rn(m[1])+" century"+era(m[2]);return s;}',1)
rp('const m1=v=>v.toFixed(1).replace(".",",");','const m1=v=>v.toFixed(1);',1)
rp('`a legmagasabb mért pontja kb. ${m1(-d)} m-rel a mai felszín fölött van (álló rom, vagy a környezete feltárt, mélyített terület)`','`its highest measured point is c. ${m1(-d)} m above today\'s ground level (a standing ruin, or the surrounding area has been excavated and lowered)`',1)
rp('"nagyjából a mai felszín szintjén"','"roughly at today\'s ground level"',1)
rp('`a legmagasabb mért pontja kb. ${m1(d)} m-rel a mai felszín alatt`','`its highest measured point is c. ${m1(d)} m below today\'s ground level`',1)
rp('<h3>Magasság és mélység</h3><dl class="facts"><dt>Mért magasság</dt><dd>${q} m a tengerszint felett</dd><dt>A mai felszín itt</dt><dd>kb. ${m1(p.zg)} m a tengerszint felett</dd><dt>Mélység</dt><dd>${t}</dd></dl><p class="hint">A mért magasságok a SITAR adatai; a mai felszín a Lazio régió 5 m-es domborzatmodelljéből való (1–2 m-es bizonytalansággal), ezért a mélység tájékoztató érték.</p>',
   '<h3>Elevation and depth</h3><dl class="facts"><dt>Measured elevation</dt><dd>${q} m above sea level</dd><dt>Today\'s ground level here</dt><dd>c. ${m1(p.zg)} m above sea level</dd><dt>Depth</dt><dd>${t}</dd></dl><p class="hint">The measured elevations are SITAR data; today\'s ground level comes from the 5 m terrain model of the Lazio Region (uncertainty 1–2 m), so the depth is indicative only.</p>',1)
rp('||e[0]||"keltezés")','||e[0]||"dating")',1);rp('a keltezés alapja: ','basis of the dating: ',1);rp('<h3>A keltezés részletei</h3>','<h3>Dating details</h3>',1)
for a,b in [("tervszerű, nagy felületű ásatás","planned open-area excavation"),("kisebb ásatás: szonda, árok, kutatóakna","small excavation: test pit, trench, sounding"),("álló épület vizsgálata","study of a standing structure"),("fúrásból ismert","known from core drilling"),("helyszíni megfigyelés, ásatás nélkül","on-site observation, no excavation"),("nem saját ásatás: szakirodalmi vagy levéltári adat","no excavation of its own: data from publications or archives")]: rp('"'+a+'"','"'+b+'"',1)
rp('"Régészeti egység"','"Archaeological unit"',1);rp('SITAR ásatási adat · ${esc(p.id)}. sz. egység','SITAR excavation record · unit no. ${esc(p.id)}',1)
for a,b in [("Meghatározás","Definition"),("Csoport","Group"),("Jelleg","Type"),("Helymeghatározás","Positioning"),("Állapot","Condition"),("Módszer","Method"),("Időpont","Date"),("Hely","Place"),("Felelős (Soprintendenza)","Responsible (Soprintendenza)"),("A kutatás módja","Method of investigation")]: rp('row("'+a+'",','row("'+b+'",',1)
rp('<h3>A kutatás</h3>','<h3>The investigation</h3>',1);rp('a kutatás régészeti leletet nem talált','the investigation found no archaeological remains',1)
rp('${o.hu?`<h3>A kutatás leírása</h3><p>${esc(o.hu)}</p>`:""}','${o.en?`<h3>Description of the investigation</h3><p>${esc(o.en)}</p>`:""}',1)
rp('data-l="${o.hu?"Eredeti olasz szöveg":"A kutatás leírása (olaszul)"}">${o.hu?"Eredeti olasz szöveg":"A kutatás leírása (olaszul)"} ▾','data-l="${o.en?"Italian original":"Description of the investigation (in Italian)"}">${o.en?"Italian original":"Description of the investigation (in Italian)"} ▾',1)
rp('${p.dh?`<h3>Leírás <span class="hint">(a SITAR adatbázisából, magyarul)</span></h3><p>${esc(p.dh)}</p>','${p.de?`<h3>Description <span class="hint">(from the SITAR database, translated from Italian)</span></h3><p>${esc(p.de)}</p>',1)
rp('Eredeti olasz szöveg','Italian original');rp('"A kutatás leírása (olaszul)"','"Description of the investigation (in Italian)"',1)
rp('<h3>Leírás <span class="hint">(olaszul, a SITAR adatbázisából)</span></h3>','<h3>Description <span class="hint">(in Italian, from the SITAR database)</span></h3>',1)
rp('Forrás: SITAR – Sistema Informativo Territoriale Archeologico di Roma, Soprintendenza Speciale di Roma, CC BY-SA 4.0. A rekonstrukciók (szaggatott vonal) a feltárók értelmezései.','Source: SITAR – Sistema Informativo Territoriale Archeologico di Roma, Soprintendenza Speciale di Roma, CC BY-SA 4.0. The reconstructions (dashed line) are the excavators\' interpretations.',1)
rp('const oiDate=d=>d?d.slice(0,10).replace(/-/g,". ")+".":"";','const oiDate=d=>d?d.slice(0,10):"";',1)
rp('const catLabel={paus:"Forrásból és feltárásból ismert",arch:"Főleg régészetből ismert",hypo:"Helye bizonytalan"};','const catLabel={paus:"Known from sources and excavation",arch:"Known mainly from archaeology",hypo:"Location uncertain"};',1)
rp('">Ma: ${TDL[','">Today: ${TDL[',1)
rp('Notitia VIII. ker. ${notI+1}.','Notitia, Region VIII, no. ${notI+1}',1)
S=re.sub(r'Notitia ([IVX]+)\. ker\.',r'Notitia, Region \1',S)
rp('<h3>Mit mondanak az ókori források</h3>','<h3>What the ancient sources say</h3>',2);rp('Ókori szerző nem írja le; régészeti lelet.','Not described by any ancient author; known from archaeology.',1)
rp('"Bővebben a forrásokról"','"More on the sources"',1);rp('<h3>Mit mutatnak az ásatások</h3>','<h3>What the excavations show</h3>',1);rp('"Bővebben az ásatásokról"','"More on the excavations"',1)
rp('panel.innerHTML=`<h2>Kezdd itt</h2>','panel.innerHTML=`<h2>Start here</h2>',1)
rp('a térképen nem ábrázolt','not shown on the map',1);rp('"keltezetlen"','"undated"');rp('sub:"helye nem ismert"','sub:"location unknown"');rp('"– válassz területet –"','"– choose an area –"',1)
rp('n+" elem látszik (a többi szűrő is érvényes)"','n+" elements shown (the other filters also apply)"',1)
rp('Nincs találat a térkép elemei között.','No match among the map elements.',1);rp('y==="all"?"minden korszak":','y==="all"?"all periods":',1)
# CARDSUB: a kulcsok az angol h2-címek
hu_h2=re.findall(r'<h2>([^<$]+)</h2>',open('body_v60pre.html',encoding='utf8').read());en_h2=re.findall(r'<h2>([^<$]+)</h2>',S)
assert len(hu_h2)==len(en_h2),(len(hu_h2),len(en_h2));H=dict(zip(hu_h2,en_h2))
subs={"Éremkincsek: mikor rejtettek el pénzt":"13,349 hoards from the empire, 18 from Rome: crisis, sieges, debasement","Róma a birodalom feliratai között":"Rome and the provinces: 525,870 Latin inscriptions, formulae, the freed, soldiers, age","Keresztény feliratok (3–8. század)":"40,175 inscriptions from the catacombs: language, symbols, cemeteries, month of burial, church offices","Sírtelkek mérete":"the size of 1,345 plots in feet and metres, by road and period","Katonák Róma sírfeliratain":"Praetorians, horse guard, urban cohorts, fleets: age, service, origin, findspot","Életkor és család a sírfeliratokon":"8,941 ages, age-rounding, length of marriage, for whom the tomb was set up","Jogállás és császári nevek időben":"freed and slave markers, the waves of Iulii, Claudii and Aurelii, imperial freedmen","Foglalkozások a feliratokon":"2,338 inscriptions naming physicians, cooks, goldsmiths: sectors, legal status, workshop addresses","Feliratok":"44,796 EDR inscriptions from Rome: over time, findspots, tombs along the roads","Építkezések időrendben":"construction phases from excavations and the map’s buildings in 25-year bands","Róma élelmezése":"grain, oil and Monte Testaccio: ancient figures and archaeological estimates","Róma népessége":"estimates by 12 scholars from 510 BC to the 6th century, and the ancient figures","A 14 kerület számokban":"apartment blocks, houses, warehouses, baths, fountains, bakeries in the 4th-century catalogue","Séták":"eleven historical walks from Catiline to the Gothic sieges, following ancient authors, and walks from novels","Róma vízvezetékei":"the 11 aqueducts according to Frontinus, baths, end points, supply and distribution","A fő utak kapuról kapura":"ten roads from the gates of the Servian Wall to the Aurelian Wall","Korai keresztény Róma (4–6. század)":"tituli, basilicas, catacombs","Hogyan olvasd a térképet":"sources, excavations, symbols","Források":"data and literature used"}
m=re.search(r'^const CARDSUB=\{.*\};$',S,re.M);assert m
S=S[:m.start()]+'const CARDSUB='+json.dumps({H[k]:v for k,v in subs.items()},ensure_ascii=False)+';'+S[m.end():]
rp('gr:"Domus Augustana – hivatalos szárny"','gr:"Domus Augustana – state wing"',1);rp('gr:"Porticus Octaviae (korábban Porticus Metelli)"','gr:"Porticus Octaviae (formerly Porticus Metelli)"',1)
# --- nyelvválasztó mindkét oldalra
HU=open('body_v60pre.html',encoding='utf8').read();C=open('style_v60pre.css',encoding='utf8').read()
def lang(body,cur):
    sw='    <nav class="langsw" aria-label="Nyelv / Language"><a href="index.html" lang="hu" hreflang="hu"'+(' class="on" aria-current="true"' if cur=="hu" else '')+'>Magyar</a><a href="en.html" lang="en" hreflang="en"'+(' class="on" aria-current="true"' if cur=="en" else '')+'>English</a></nav>\n'
    i=body.index('    <h1>');assert body.count('    <h1>')==1
    body=body[:i]+sw+body[i:]
    js='/* nyelvválasztó: a kiválasztott elem (a cím #-jele utáni rész) megmarad a másik nyelvű oldalon is */\ndocument.querySelectorAll(".langsw a").forEach(a=>a.addEventListener("click",e=>{if(a.classList.contains("on")){e.preventDefault();return;}a.href=a.getAttribute("href").split("#")[0]+location.hash;}));\n/* funkció szerinti szűrő */'
    assert body.count('/* funkció szerinti szűrő */')==1
    # v61: "Forrás szerint" színezésnél a három forráskategória-gomb (jelmagyarázat) közvetlenül a színezés sora alá kerül
    anc='    </div>\n    <div class="chips hidden" id="depthkey"';assert body.count(anc)==1
    body=body.replace(anc,'      <div class="chips hidden" id="srcchips" role="group"></div>\n'+anc)
    js+='''\n/* forrás szerinti színezésnél a jelmagyarázat (a három kategóriagomb) a színezés sorába kerül, különben a rétegsor elején marad */
(function(){const box=document.getElementById("srcchips"),low=document.getElementById("t-det").parentNode,three=["t-paus","t-arch","t-hypo"].map(id=>document.getElementById(id));
  const place=()=>{const src=document.getElementById("cb-source").getAttribute("aria-pressed")==="true";
    if(src)three.forEach(b=>box.appendChild(b));else three.slice().reverse().forEach(b=>low.insertBefore(b,low.firstChild));box.classList.toggle("hidden",!src);};
  ["cb-source","cb-period","cb-today"].forEach(id=>document.getElementById(id).addEventListener("click",()=>setTimeout(place,0)));setTimeout(place,0);})();'''
    return body.replace('/* funkció szerinti szűrő */',js)
css='''/* v60: nyelvválasztó */
.langsw{grid-column:1/-1;justify-self:end;display:inline-flex;border:1px solid var(--line);border-radius:999px;overflow:hidden;margin-bottom:.3em}
.langsw a{font:500 12px var(--font-body);padding:4px 12px;color:var(--ink);text-decoration:none}
.langsw a.on{background:var(--ink);color:var(--sheet);cursor:default}
</style>'''
assert C.count('</style>')==1;C=C.replace('</style>',css)
import sys,os;sys.path.insert(0,'en');from ux import ux,ux2,CSS as UXCSS,CSS2 as UXCSS2
HU=lang(HU,'hu');S=lang(S,'en');HU=ux(HU,'hu');S=ux(S,'en');HU=ux2(HU,'hu');S=ux2(S,'en');C=C.replace('</style>',UXCSS);C=C.replace('</style>',UXCSS2)
open('body.html','w',encoding='utf8').write(HU);open('style.css','w',encoding='utf8').write(C)
open('body_en.html','w',encoding='utf8').write(S)
open('index.html','w',encoding='utf8').write(HU.replace('{{STYLE}}',C));open('en.html','w',encoding='utf8').write(S.replace('{{STYLE}}',C))
# maradék magyar szöveg keresése (megjegyzéseken kívül)
hu=re.compile(r'[őűŐŰ]|\b(és|az|egy|nem|vagy|kb\.|Kr\. [eu]\.)\b')
left=[]
for i,l in enumerate(S.split('\n'),1):
    c=re.sub(r'/\*.*?\*/','',l);c=re.sub(r'(^|[;{}\s])//.*$','',c)
    if c.strip().startswith(('/*','*','//')) or 410<=i<=428: continue
    for mm in hu.finditer(c): left.append((i,c[max(0,mm.start()-50):mm.end()+50]));break
print('maradék gyanús sor:',len(left))
for x in left[:60]: print(x)
