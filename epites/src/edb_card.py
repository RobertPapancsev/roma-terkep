# v89: „Keresztény feliratok (3–8. század)” kártya – közös generátor (hu/en). Adat: edb/calc.py -> edb/data.json
import json,math
D=json.load(open('edb/data.json'));B=D['bins'];T=D['time']
RN={'appia':('Via Appia','Via Appia'),'ardeatina':('Via Ardeatina','Via Ardeatina'),'appard':('a Via Appia és a Via Ardeatina között','between the Via Appia and the Via Ardeatina'),'ostiensis':('Via Ostiensis','Via Ostiensis'),'portuensis':('Via Portuensis','Via Portuensis'),
 'aurelia':('Via Aurelia','Via Aurelia'),'vaticana':('Vaticanus (Szent Péter)','Vatican (St Peter’s)'),'flaminia':('Via Flaminia','Via Flaminia'),'salaria':('Via Salaria','Via Salaria'),'nomentana':('Via Nomentana','Via Nomentana'),
 'tiburtina':('Via Tiburtina','Via Tiburtina'),'labicana':('Via Labicana','Via Labicana'),'latina':('Via Latina','Via Latina')}
LN=[('grc','görög nyelvű','in Greek'),('chr','Krisztus-monogrammal','with a Christogram'),('crs','kereszttel','with a cross')]
SY=[('chr','Krisztus-monogram (chi-rho)','Christogram (chi-rho)'),('bird','madár, galamb','bird, dove'),('palm','pálmaág','palm branch'),('crs','kereszt','cross'),('anchor','horgony','anchor'),('vessel','edény','vessel'),('wreath','koszorú','wreath'),('orans','imádkozó alak (orans)','praying figure (orans)'),('tree','fa','tree'),('fish','hal','fish'),('shepherd','pásztor','shepherd'),('sheep','bárány','sheep'),('ship','hajó','ship')]
TI=[('presb','presbyter (pap)','presbyter (priest)'),('mart','vértanú említése (martyr)','mention of a martyr'),('neof','neofitus (frissen megkeresztelt)','neophyte (newly baptised)'),('foss','fossor (sírásó, a katakomba munkása)','fossor (gravedigger, catacomb worker)'),('episc','püspök vagy pápa említése (episcopus, papa)','mention of a bishop or pope (episcopus, papa)'),
 ('lect','lector (felolvasó)','lector (reader)'),('diac','diaconus','deacon'),('virgo','Istennek szentelt szűz (virgo sacra, ancilla Dei)','consecrated virgin (virgo sacra, ancilla Dei)'),('exor','exorcista','exorcist'),('acol','acolitus','acolyte'),('subd','subdiaconus','subdeacon')]
FO=[('pace','„in pace” (békében)','“in pace” (in peace)'),('dep','„depositus, deposita” (eltemetve) a temetés napjával','“depositus, deposita” (buried), with the day of burial'),('bm','„bene merenti” (jól megérdemelten)','“bene merenti” (well deserving)'),('locus','„locus” (sírhely megnevezése)','“locus” (naming the burial place)'),('dm','„Dis Manibus” (a pogány sírfeliratok kezdete)','“Dis Manibus” (the opening of pagan epitaphs)'),('vivo','„se vivo” (még életében)','“se vivo” (in his or her lifetime)'),('emit','„emit, comparavit” (sírhely vásárlása)','“emit, comparavit” (purchase of a burial place)')]
MH=['január','február','március','április','május','június','július','augusztus','szeptember','október','november','december'];ME=['January','February','March','April','May','June','July','August','September','October','November','December']
LINK={'Coem. Pontiani':'cponziano','Coem. Octavillae ad s.Pancratium':'spancrazio','Coem. Nicomedis':'cnicomede','Basilica S.Petri apostoli':'oldstpeter'}
def build(lang):
    hu=lang=='hu';t=lambda a,b:a if hu else b
    fmt=(lambda n:f'{n:,}'.replace(',',' ')) if hu else (lambda n:f'{n:,}')
    d1=lambda x:(f'{x:.1f}'.replace('.',',') if hu else f'{x:.1f}')
    pc=lambda x:(f'{x:.0f}' if x>=10 else d1(x))
    yr=lambda y:(f'Kr. u. {y}' if hu else f'AD {y}')
    def sh(k,lo,hi):
        a=sum(T[k][i] for i,x in enumerate(B) if lo<=x<hi);b=sum(T['all'][i] for i,x in enumerate(B) if lo<=x<hi);return 100*a/b
    n=D['n'];Lg=D['lang'];grc=Lg.get('grc',0);bi=Lg.get('la, grc',0);ex=D['ex'];notinc=ex.get('Pictus',0)+ex.get('Scariphatus',0)+ex.get('Exaratus',0)+ex.get('Carbone scriptus',0)
    tot=sum(T['all']);c4=100*sum(v for v,x in zip(T['all'],B) if 300<=x<400)/tot
    L=[]
    L.append('    <section class="card" id="edbcard">')
    L.append('      <h2>'+t('Keresztény feliratok (3–8. század)','Christian inscriptions (3rd–8th century)')+'</h2>')
    L.append('      <p class="hint">'+t(f'A bari egyetem adatbázisa, az Epigraphic Database Bari (EDB) a római keresztények feliratait gyűjti. A nyílt adatállomány {fmt(D["n0"])} feliratot tartalmaz, szinte mind a városfalon kívüli katakombákból és temetőkből; több felirat két-három rekordban is szerepel (ugyanaz a kő a gyűjtemény régebbi és újabb kötetében), ezek másodpéldányai ({fmt(D["ndup"])}) nélkül {fmt(n)} feliratot számoltunk. Ebből {fmt(D["dated"])} keltezett, {fmt(grc)} görög nyelvű ({pc(100*grc/n)}%), {fmt(bi)} kétnyelvű. A feliratok {pc(100*notinc/n)}%-át nem vésték, hanem a sírt lezáró vakolatba karcolták vagy ráfestették; {fmt(D["metr"])} felirat verses.',
      f'The database of the University of Bari, the Epigraphic Database Bari (EDB), collects the inscriptions of the Christians of Rome. The open data set contains {fmt(D["n0"])} inscriptions, almost all from the catacombs and cemeteries outside the city walls; a number of inscriptions appear in two or three records (the same stone in an older and a newer volume of the corpus); without these second copies ({fmt(D["ndup"])}) we counted {fmt(n)}. Of these {fmt(D["dated"])} are dated, {fmt(grc)} are in Greek ({pc(100*grc/n)}%) and {fmt(bi)} bilingual. {pc(100*notinc/n)}% of the inscriptions were not carved but scratched into, or painted on, the plaster closing the tomb; {fmt(D["metr"])} are in verse.')+'</p>')
    L.append('      <h3 class="aqh">'+t('Nyelv és jelképek időben','Language and symbols over time')+'</h3>')
    L.append('      <div class="bldchart" id="edbchart" data-k="'+','.join(k for k,_,_ in LN)+'"></div>')
    L.append('      <p class="hint bldleg" id="edbleg">'+' · '.join(f'<span class="ik e{k}"></span> <span class="il">{h if hu else e}</span>' for k,h,e in LN)+'</p>')
    L.append('      <p class="hint popinfo" id="edbinfo">'+t('Vidd az egeret a görbére; kattintásra a térkép évcsúszkája arra az időre áll.','Hover over the curve; click to set the map’s year slider to that time.')+'</p>')
    L.append('      <p class="hint">'+t(f'A görbe azt mutatja, hogy egy-egy korszak feliratainak hány százaléka görög nyelvű, illetve hányon áll Krisztus-monogram vagy kereszt. A 3. században a feliratok {pc(sh("grc",200,300))}%-a görög, a 4. század második felében {pc(sh("grc",350,400))}%-a. A Krisztus-monogram a 4. század elejéig alig fordul elő ({pc(sh("chr",200,300))}%), a század második felében a feliratok {pc(sh("chr",350,400))}%-án áll. A kereszt később terjed el: az 5. század első felében {pc(sh("crs",400,450))}%, a 6. században {pc(sh("crs",500,600))}%. A keltezett feliratok {pc(c4)}%-a a 4. századra esik; a 6–7. századból sávonként csak 30–100 felirat maradt, ott a görbe bizonytalan.',
      f'The curve shows what percentage of the inscriptions of each period are in Greek, and how many carry a Christogram or a cross. In the 3rd century {pc(sh("grc",200,300))}% of the inscriptions are Greek, in the second half of the 4th century {pc(sh("grc",350,400))}%. The Christogram hardly occurs before the early 4th century ({pc(sh("chr",200,300))}%); in the second half of that century it stands on {pc(sh("chr",350,400))}% of the inscriptions. The cross spreads later: {pc(sh("crs",400,450))}% in the first half of the 5th century, {pc(sh("crs",500,600))}% in the 6th. {pc(c4)}% of the dated inscriptions fall in the 4th century; from the 6th–7th centuries only 30–100 inscriptions per band survive, so the curve is uncertain there.')+'</p>')
    L.append('      <h3 class="aqh">'+t('Jelképek a feliratokon','Symbols on the inscriptions')+'</h3>')
    sv={'chr':D['chr'],'crs':D['crs'],**D['sg']};mx=max(sv[k] for k,_,_ in SY)
    L.append('      <div class="foodest edbbars">')
    for k,h,e in sorted(SY,key=lambda x:-sv[x[0]]):
        L.append(f'        <div class="fe"><span class="fen">{h if hu else e}</span><span class="feb"><span class="esy" style="width:{100*sv[k]/mx:.1f}%"></span></span><span class="fev">{fmt(sv[k])}</span></div>')
    L.append('      </div>')
    L.append('      <h3 class="aqh">'+t('Temetők és utak','Cemeteries and roads')+'</h3>')
    L.append('      <p class="hint">'+t(f'Az EDB {D["ncem"]} temetőhöz és lelőhelyhez sorolja a feliratokat. A nagy katakombák a térkép szélén túl, az utak mentén fekszenek; a linkként jelölt temetők a térképen is szerepelnek.',
      f'EDB assigns the inscriptions to {D["ncem"]} cemeteries and findspots. The great catacombs lie beyond the edge of the map, along the roads; the cemeteries shown as links are also on the map.')+'</p>')
    rmx=max(D['road'].values())
    L.append('      <div class="foodest edbbars">')
    for k,v in sorted(D['road'].items(),key=lambda x:-x[1]):
        L.append(f'        <div class="fe"><span class="fen">{RN[k][0 if hu else 1]}</span><span class="feb"><span class="erd" style="width:{100*v/rmx:.1f}%"></span></span><span class="fev">{fmt(v)}</span></div>')
    L.append('      </div>')
    L.append('      <div class="regwrap"><table class="regtab insctab agetab edbtab">')
    L.append('        <thead><tr><th>'+t('Temető (az EDB megnevezése)','Cemetery (as named in EDB)')+'</th><th>'+t('Út','Road')+'</th><th>'+t('Felirat','Inscriptions')+'</th><th>'+t('Fő időszak','Main period')+'</th><th>'+t('Görög','Greek')+'</th><th>'+t('Krisztus-monogram','Christogram')+'</th><th>'+t('Karcolt vagy festett','Scratched or painted')+'</th></tr></thead>')
    L.append('        <tbody>')
    rows=D['cem'][:24]+[c for c in D['cem'][24:] if c['c'] in LINK]
    for c in rows:
        nm=f'<i lang="la">{c["c"]}</i>';nm=f'<a href="#" data-goto="{LINK[c["c"]]}">{nm}</a>' if c['c'] in LINK else nm
        lo=math.floor(c['q1']/25)*25;hi=math.ceil(c['q3']/25)*25
        if hi==lo:hi+=25
        rd=RN[c['road']][0 if hu else 1] if c['road'] else '–'
        L.append(f'          <tr><td>{nm}</td><td>{rd}</td><td class="pn">{fmt(c["n"])}</td><td class="pn">{yr(lo)}–{hi}</td><td class="pn">{pc(100*c["grc"]/c["n"])}%</td><td class="pn">{pc(100*c["chr"]/c["n"])}%</td><td class="pn">{pc(100*c["pict"]/c["n"])}%</td></tr>')
    L.append('        </tbody>')
    L.append('      </table></div>')
    L.append('      <p class="hint">'+t(f'A „fő időszak” a keltezések középső fele, 25 évre kerekítve. {fmt(D["noroad"])} felirat lelőhelye nem sorolható úthoz. A Memoria Apostolorum (a Via Appián, a mai San Sebastiano alatt) feliratai mind karcolt vagy festett falfirkák: a zarándokok Péter és Pál apostolhoz szóló fohászai.',
      f'“Main period” is the middle half of the dates, rounded to 25 years. {fmt(D["noroad"])} inscriptions have a findspot that cannot be assigned to a road. The inscriptions of the Memoria Apostolorum (on the Via Appia, under today’s San Sebastiano) are all scratched or painted graffiti: pilgrims’ invocations of the apostles Peter and Paul.')+'</p>')
    A=D['age'];E=D['edr'];mo=D['months'];mt=sum(mo);mmx=max(mo)
    L.append('      <h3 class="aqh">'+t('A temetés hónapja','The month of burial')+'</h3>')
    L.append('      <p class="hint">'+t(f'A keresztény sírfeliratok gyakran közlik a temetés napját („deposita III Kalendas Septembres”). {fmt(mt)} feliraton olvasható a teljes dátum ({fmt(D["mla"])} latin, {D["mgr"]} görög). A római naptár szerinti napot átszámoltuk: a „harmadik nap szeptember Kalendae-ja előtt” augusztus 30.',
      f'Christian epitaphs often give the day of burial (“deposita III Kalendas Septembres”). The full date can be read in {fmt(mt)} inscriptions ({fmt(D["mla"])} Latin, {D["mgr"]} Greek). The day in the Roman calendar was converted: “the third day before the Kalends of September” is 30 August.')+'</p>')
    L.append('      <div class="foodest edbbars edbmon">')
    for i,v in enumerate(mo):
        L.append(f'        <div class="fe"><span class="fen">{(MH if hu else ME)[i]}</span><span class="feb"><span class="emo" style="width:{100*v/mmx:.1f}%"></span></span><span class="fev">{v}</span></div>')
    L.append('      </div>')
    L.append('      <p class="hint">'+t(f'A temetések {pc(100*(mo[7]+mo[8])/mt)}%-a augusztusra és szeptemberre esik; ha egyenletesen oszlanának el, ez 17% lenne. A késő nyári csúcs a római halandóság ismert sajátossága, a maláriával és a nyári fertőzésekkel hozzák összefüggésbe.',
      f'{pc(100*(mo[7]+mo[8])/mt)}% of the burials fall in August and September; if they were evenly spread this would be 17%. The late-summer peak is a known feature of mortality in Rome, linked to malaria and summer infections.')+'</p>')
    L.append('      <h3 class="aqh">'+t('Életkor: keresztény és korábbi sírfeliratok','Age: Christian and earlier epitaphs')+'</h3>')
    L.append('      <div class="regwrap"><table class="regtab insctab agetab">')
    L.append('        <thead><tr><th></th><th>'+t('Keresztény feliratok (EDB)','Christian inscriptions (EDB)')+'</th><th>'+t('Sírfeliratok az EDR-ben','Epitaphs in EDR')+'</th></tr></thead>')
    L.append('        <tbody>')
    for lab,a,b in [(t('Életkor-adat','Ages given'),fmt(A['n']),fmt(E['n'])),(t('Középérték','Median'),t(f'{A["med"]} év',f'{A["med"]} years'),t(f'{E["med"]} év',f'{E["med"]} years')),(t('10 év alatti','Under 10'),pc(100*A['u10']/A['n'])+'%',pc(100*E['u10'])+'%'),(t('60 év fölötti','Over 60'),pc(100*A['o60']/A['n'])+'%',pc(100*E['o60'])+'%'),(t('Whipple-index (kerekítés)','Whipple index (rounding)'),str(A['whipple']),str(E['whipple']))]:
        L.append(f'          <tr><td>{lab}</td><td class="pn">{a}</td><td class="pn">{b}</td></tr>')
    L.append('        </tbody>')
    L.append('      </table></div>')
    L.append('      <p class="hint">'+t(f'A két adatbázis életkorai hasonlóan oszlanak el. A keresztény latin feliratokon az életkor {pc(100*A["pm"]/A["nla"])}%-a mellett ott áll a „plus minus” (körülbelül). A keresztény életkorok közül {fmt(A["nla"])} latin, {A["ngr"]} görög feliratból származik; a görög feliratok betűkkel írt számait (κε = 25) átszámoltuk.',
      f'The ages in the two databases are distributed similarly. In the Christian Latin inscriptions {pc(100*A["pm"]/A["nla"])}% of the ages are qualified by “plus minus” (about). Of the Christian ages {fmt(A["nla"])} come from Latin and {A["ngr"]} from Greek inscriptions; the numerals written with letters in the Greek inscriptions (κε = 25) were converted.')+'</p>')
    L.append('      <h3 class="aqh">'+t('Egyházi tisztségek és megnevezések','Church offices and terms')+'</h3>')
    L.append('      <div class="regwrap"><table class="regtab insctab agetab">')
    L.append('        <thead><tr><th>'+t('Megnevezés','Term')+'</th><th>'+t('Felirat','Inscriptions')+'</th></tr></thead>')
    L.append('        <tbody>')
    for k,h,e in sorted(TI,key=lambda x:-D['tit'][x[0]]):
        L.append(f'          <tr><td>{h if hu else e}</td><td class="pn">{D["tit"][k]}</td></tr>')
    L.append('        </tbody>')
    L.append('      </table></div>')
    L.append('      <h3 class="aqh">'+t('Formulák','Formulae')+'</h3>')
    fmx=max(D['form'].values())
    L.append('      <div class="foodest edbbars">')
    for k,h,e in sorted(FO,key=lambda x:-D['form'][x[0]]):
        L.append(f'        <div class="fe"><span class="fen">{h if hu else e}</span><span class="feb"><span class="efo" style="width:{100*D["form"][k]/fmx:.1f}%"></span></span><span class="fev">{fmt(D["form"][k])}</span></div>')
    L.append('      </div>')
    L.append('      <p class="hint">'+t(f'A formulákat és a tisztségeket a {fmt(D["ntxt"])} olvasható szövegű feliraton számoltuk ({fmt(D["nlat"])} latin vagy kétnyelvű, {fmt(D["ngrc"])} görög szövegrésszel), feliratonként egyszer, a görög megfelelőkkel együtt (πρεσβύτερος, ἐν εἰρήνῃ, κατάθεσις). Az „in pace” vagy görög megfelelője a feliratok {pc(100*D["form"]["pace"]/D["ntxt"])}%-án áll; a pogány „Dis Manibus” {D["form"]["dm"]} keresztény feliraton is megmaradt. A töredékes számok és az ismétlődő feliratok másodpéldányai itt sem számítanak. A tisztségek találatait és a görög életkorokat egyenként átolvastuk: kimaradt az olvasó megszólítása („lector”), a Martyrius-féle személynév és a házasság hossza.',
      f'Formulae and offices were counted in the {fmt(D["ntxt"])} inscriptions with a readable text ({fmt(D["nlat"])} with a Latin and {fmt(D["ngrc"])} with a Greek part), once per inscription, together with their Greek equivalents (πρεσβύτερος, ἐν εἰρήνῃ, κατάθεσις). “In pace” or its Greek equivalent stands on {pc(100*D["form"]["pace"]/D["ntxt"])}% of the inscriptions; the pagan “Dis Manibus” survives on {D["form"]["dm"]} Christian inscriptions. Fragmentary numerals and second copies of repeated inscriptions are not counted here either. The office hits and the Greek ages were read one by one: addresses to the reader (“lector”), personal names such as Martyrius and lengths of marriage were left out.')+'</p>')
    L.append('    </section>')
    src='      <li><b>'+t('Keresztény feliratok (3–8. század).','Christian inscriptions (3rd–8th century).')+'</b> '+t('Epigraphic Database Bari (EDB) – Inscriptions by Christians in Rome (3rd–8th cent. CE), EpiDoc-fájlok (C. Carletti, A. E. Felle, A. Rocco; Università di Bari), Zenodo 2019, <a href="https://doi.org/10.5281/zenodo.3575485">10.5281/zenodo.3575485</a>; a fájlok licence CC BY-NC-SA 3.0 (nem kereskedelmi felhasználás). Az összesítés saját: nyelv, jelképek, technika és temető az EDB mezőiből; a temetők utakhoz sorolása, a temetés hónapja, az életkor, a tisztségek és a formulák a feliratok latin és görög szövegéből (edb/parse.py, edb/calc.py, edb/greek.py, edb/dup.py). A halálozás évszakairól: B. D. Shaw, <i>Seasons of Death: Aspects of Mortality in Imperial Rome</i>, Journal of Roman Studies 86 (1996).',
      'Epigraphic Database Bari (EDB) – Inscriptions by Christians in Rome (3rd–8th cent. CE), EpiDoc files (C. Carletti, A. E. Felle, A. Rocco; Università di Bari), Zenodo 2019, <a href="https://doi.org/10.5281/zenodo.3575485">10.5281/zenodo.3575485</a>; the files are licensed CC BY-NC-SA 3.0 (non-commercial use). The summary is our own: language, symbols, technique and cemetery from the EDB fields; the assignment of cemeteries to roads, month of burial, age, offices and formulae from the Latin and Greek texts of the inscriptions (edb/parse.py, edb/calc.py, edb/greek.py, edb/dup.py). On the seasons of death: B. D. Shaw, <i>Seasons of Death: Aspects of Mortality in Imperial Rome</i>, Journal of Roman Studies 86 (1996).')+'</li>'
    sub=t(f'{fmt(n)} felirat a katakombákból: nyelv, jelképek, temetők, a temetés hónapja, egyházi tisztségek',f'{fmt(n)} inscriptions from the catacombs: language, symbols, cemeteries, month of burial, church offices')
    return '\n'.join(L)+'\n',src,sub
if __name__=='__main__':
    for l in ('hu','en'):
        c,s,sub=build(l);print(len(c.split('\n')),sub)
    import re;print(re.sub(r'<[^>]+>','',' '.join(x for x in build('hu')[0].split('\n') if 'class="hint"' in x))[:2600])
