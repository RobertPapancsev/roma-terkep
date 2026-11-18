# v85: „Jogállás és császári nevek időben” kártya – közös generátor (hu/en). Adat: nm/calc.py -> nm/data.json
import json
D=json.load(open('nm/data.json'))
B=D['bins'];T=D['time'];TOT=D['tot']
ST=[('lib','felszabadított (libertus, liberta)','freed (libertus, liberta)'),('ser','rabszolga (servus, serva, verna)','slave (servus, serva, verna)'),('fil','apanév (szabad születés)','father’s name (free birth)'),('ilib','császári felszabadított (Augusti libertus)','imperial freedman/woman (Augusti libertus)'),('iser','császári rabszolga (Caesaris servus)','imperial slave (Caesaris servus)')]
NM=[('iuli','Iulius'),('claudi','Claudius'),('flavi','Flavius'),('ulpi','Ulpius'),('aeli','Aelius'),('aureli','Aurelius')]
EMP=[('iuli','Iulius','Augustus, Tiberius, Caligula','Kr. e. 27 – Kr. u. 41','27 BC – AD 41',67),('claudi','Claudius','Claudius, Nero','Kr. u. 41–68','AD 41–68',27),('flavi','Flavius','Vespasianus, Titus, Domitianus','Kr. u. 69–96','AD 69–96',27),
 ('coccei','Cocceius','Nerva','Kr. u. 96–98','AD 96–98',2),('ulpi','Ulpius','Traianus','Kr. u. 98–117','AD 98–117',19),('aeli','Aelius','Hadrianus, Antoninus Pius','Kr. u. 117–161','AD 117–161',44),
 ('aureli','Aurelius','Marcus Aurelius, Lucius Verus, Commodus; Caracalla, Elagabalus, Severus Alexander','Kr. u. 161–192 és 211–235','AD 161–192 and 211–235',55),('septimi','Septimius','Septimius Severus','Kr. u. 193–211','AD 193–211',18)]
EMPEN={'Vespasianus, Titus, Domitianus':'Vespasian, Titus, Domitian','Traianus':'Trajan','Hadrianus, Antoninus Pius':'Hadrian, Antoninus Pius'}
CXN={'liviae':('Livia szolgáinak és felszabadítottjainak kolumbáriuma (Monumentum Liviae)','The columbarium of Livia’s slaves and freedmen (Monumentum Liviae)'),'statili':('A Statiliusok kolumbáriuma','The columbarium of the Statilii'),
 'volusii':('A Volusiusok síremléke','The tomb of the Volusii'),'codini':('A Vigna Codini kolumbáriumai','The columbaria of the Vigna Codini'),'salario':('A Salaria-temető','The Salarian cemetery'),
 'spaolo':('San Paolo fuori le mura és környéke','San Paolo fuori le mura and surroundings'),'vatican':('A vatikáni nekropolisz és a via Triumphalis menti temető','The Vatican necropolis and the cemetery along the Via Triumphalis'),
 'pamphilj':('Villa Pamphilj temetői','The cemeteries of the Villa Pamphilj'),'equites':('A császári lovastestőrség (equites singulares) temetője','The cemetery of the imperial horse guard (equites singulares)'),
 'callisto':('Callistus katakombái','The catacombs of Callixtus'),'domitilla':('Domitilla katakombái','The catacombs of Domitilla'),'priscilla':('Priscilla katakombái','The catacombs of Priscilla'),'pretestato':('Praetextatus katakombái','The catacombs of Praetextatus')}
NAME={k:n for k,n,*_ in EMP}
def share(k,lo,hi):
    a=sum(T[k][i] for i,x in enumerate(B) if lo<=x<hi);b=sum(TOT[i] for i,x in enumerate(B) if lo<=x<hi);return 100*a/b
def peak(k):
    ok=[i for i in range(len(B)) if TOT[i]>=200];i=max(ok,key=lambda i:T[k][i]/TOT[i]);return B[i],100*T[k][i]/TOT[i]
def build(lang):
    hu=lang=='hu';t=lambda a,b:a if hu else b
    fmt=(lambda n:f'{n:,}'.replace(',',' ')) if hu else (lambda n:f'{n:,}')
    pc=lambda x:(f'{x:.0f}' if x>=10 else (f'{x:.1f}'.replace('.',',') if hu else f'{x:.1f}'))
    yr=lambda y:(f'Kr. e. {-y}' if y<0 else f'Kr. u. {y}') if hu else (f'{-y} BC' if y<0 else f'AD {y}')
    C=D['cnt'];L=[]
    leg1=' · '.join(f'<span class="ik s{k}"></span> <span class="il">{h if hu else e}</span>' for k,h,e in ST)
    leg2=' · '.join(f'<span class="ik n{k}"></span> <span class="il">{n}</span>' for k,n in NM)
    L.append('    <section class="card" id="nmcard">')
    L.append('      <h2>'+t('Jogállás és császári nevek időben','Legal status and imperial names over time')+'</h2>')
    L.append('      <p class="hint">'+t(f'Az EDR {fmt(D["ntext"])} olvasható szövegű római feliratából {fmt(C["lib"])} feliraton áll felszabadított-jelölés (libertus, liberta), {fmt(C["ser"])} feliraton rabszolga-jelölés (servus, serva, verna), {fmt(C["fil"])} feliraton apanév („Marci filius”), ami szabad születést jelez. Császári felszabadított (Augusti libertus) {fmt(C["ilib"])}, császári rabszolga (Caesaris servus) {fmt(C["iser"])} feliraton szerepel. A görbék azt mutatják, hogy egy-egy korszak keltezett feliratainak hány százalékán áll az adott jelölés vagy név.',
      f'Of the {fmt(D["ntext"])} inscriptions from Rome with a readable text in EDR, {fmt(C["lib"])} carry a freed-status marker (libertus, liberta), {fmt(C["ser"])} a slave marker (servus, serva, verna), and {fmt(C["fil"])} a father’s name (“Marci filius”), the sign of free birth. An imperial freedman or freedwoman (Augusti libertus) appears in {fmt(C["ilib"])} inscriptions, an imperial slave (Caesaris servus) in {fmt(C["iser"])}. The curves show on what percentage of the dated inscriptions of each period a given marker or name appears.')+'</p>')
    L.append('      <h3 class="aqh">'+t('Jogállás-jelölések','Status markers')+'</h3>')
    L.append('      <div class="bldchart nmchart" id="nmchart1" data-k="'+','.join(k for k,_,_ in ST)+'" data-c="s"></div>')
    L.append('      <p class="hint bldleg nmleg" id="nmleg1">'+leg1+'</p>')
    L.append('      <p class="hint popinfo" id="nminfo1">'+t('Vidd az egeret a görbére; kattintásra a térkép évcsúszkája arra az időre áll.','Hover over the curve; click to set the map’s year slider to that time.')+'</p>')
    L.append('      <p class="hint">'+t(f'A felszabadított-jelölés a Kr. u. 1. század első felében a feliratok {pc(share("lib",0,50))}%-án szerepel, a 2. század első felében {pc(share("lib",100,150))}%-án, a 3. század második felében {pc(share("lib",250,300))}%-án. Az apanév már korábban ritkul: a Kr. e. 1. század első felében még {pc(share("fil",-100,-50))}%, a Kr. u. 1. században {pc(share("fil",0,100))}%. Ez a jelölés kiírásának szokását mutatja; arra, hogy hány felszabadított vagy rabszolga élt a városban, ebből nem lehet következtetni. A császári felszabadítottak aránya a Kr. u. 1. század közepétől a 2. század végéig egyenletes ({pc(share("ilib",50,200))}%).',
      f'The freed-status marker appears on {pc(share("lib",0,50))}% of inscriptions in the first half of the 1st century AD, on {pc(share("lib",100,150))}% in the first half of the 2nd century and on {pc(share("lib",250,300))}% in the second half of the 3rd. The father’s name becomes rare even earlier: still {pc(share("fil",-100,-50))}% in the first half of the 1st century BC, {pc(share("fil",0,100))}% in the 1st century AD. This shows the habit of writing the marker out; it does not allow conclusions about how many freed people or slaves lived in the city. The share of imperial freedmen is steady from the mid-1st to the end of the 2nd century AD ({pc(share("ilib",50,200))}%).')+'</p>')
    L.append('      <h3 class="aqh">'+t('Császári családnevek','Imperial family names')+'</h3>')
    L.append('      <p class="hint">'+t('Aki római polgárjogot kapott, vagy akit a császár felszabadított, a császár családnevét vette fel, és a név öröklődött. Ezért minden dinasztia után megnő a nevét viselők száma.','Anyone who received Roman citizenship, or was freed by the emperor, took the emperor’s family name, and the name was inherited. So after each dynasty the number of people bearing its name grows.')+'</p>')
    L.append('      <div class="bldchart nmchart" id="nmchart2" data-k="'+','.join(k for k,_ in NM)+'" data-c="n"></div>')
    L.append('      <p class="hint bldleg nmleg" id="nmleg2">'+leg2+'</p>')
    L.append('      <p class="hint popinfo" id="nminfo2">'+t('Vidd az egeret a görbére.','Hover over the curve.')+'</p>')
    pk={k:peak(k) for k,_ in NM}
    L.append('      <p class="hint">'+t(f'A hullámok sorban követik egymást: a Claudius név a Kr. u. 1. század második felében a leggyakoribb ({pc(pk["claudi"][1])}%), az Ulpius és az Aelius a 2. században. Az Aurelius a 2. század végétől nő meg, és a 3. században a leggyakoribb ({pc(pk["aureli"][1])}%). Ebben része van a Constitutio Antoninianának: Kr. u. 212-ben Caracalla (hivatalos nevén Marcus Aurelius Antoninus) a birodalom szinte minden szabad lakosának polgárjogot adott. A 4–5. században a Flavius név újra megnő; ekkor már nem családnév, hanem a hivatalnokok és katonák rangjelző neve Constantinus dinasztiája után.',
      f'The waves follow one another: the name Claudius is most frequent in the second half of the 1st century AD ({pc(pk["claudi"][1])}%), Ulpius and Aelius in the 2nd century. Aurelius grows from the end of the 2nd century and is the most frequent in the 3rd ({pc(pk["aureli"][1])}%). The Constitutio Antoniniana played a part in this: in AD 212 Caracalla (officially Marcus Aurelius Antoninus) gave citizenship to almost every free inhabitant of the empire. In the 4th–5th centuries the name Flavius rises again; by then it is no longer a family name but a status name of officials and soldiers, after the dynasty of Constantine.')+'</p>')
    L.append('      <p class="hint">'+t('Fontos korlát: a feliratok keltezése részben éppen a neveken alapul (egy Aurelius feliratát a kiadók Marcus Aurelius uralkodása utánra teszik), ezért a hullámok kezdete részben a keltezés módszeréből következik. A császárok saját nevét, a légiók és épületek nevét (legio VII Claudia, basilica Iulia) és a szavazókerületeket nem számoltuk.',
      'An important limit: the dating of the inscriptions is partly based on these very names (the editors place the inscription of an Aurelius after the reign of Marcus Aurelius), so the start of each wave partly follows from the dating method. The emperors’ own names, the names of legions and buildings (legio VII Claudia, basilica Iulia) and the voting tribes were not counted.')+'</p>')
    L.append('      <h3 class="aqh">'+t('Melyik császár szabadította fel?','Which emperor freed them?')+'</h3>')
    L.append('      <p class="hint">'+t('A császári felszabadított a gazdája családnevét kapta, így a névből tudható, melyik császár (vagy dinasztia) szabadította fel. A táblázat azokat a feliratokat számolja, amelyeken a családnév és az „Augusti libertus” együtt áll.','An imperial freedman received his master’s family name, so the name shows which emperor (or dynasty) freed him. The table counts the inscriptions where the family name and “Augusti libertus” stand together.')+'</p>')
    L.append('      <div class="regwrap"><table class="regtab insctab nmtab">')
    L.append('        <thead><tr><th>'+t('Családnév','Family name')+'</th><th>'+t('Császárok','Emperors')+'</th><th>'+t('Uralkodás','Reign')+'</th><th>'+t('Felirat','Inscriptions')+'</th><th>'+t('Felirat uralkodási évenként','Inscriptions per regnal year')+'</th></tr></thead>')
    L.append('        <tbody>')
    for k,n,em,rh,re_,yrs in EMP:
        v=D['al'].get(k,0);r=v/yrs
        L.append(f'          <tr><td><span class="ik n{k}"></span> {n}</td><td>{em if hu else EMPEN.get(em,em)}</td><td>{rh if hu else re_}</td><td class="pn">{v}</td><td class="pn">{(f"{r:.1f}".replace(".",",") if hu else f"{r:.1f}")}</td></tr>')
    L.append('        </tbody>')
    L.append('      </table></div>')
    L.append('      <p class="hint">'+t('Az évenkénti érték csak nagyságrendet mutat: a felszabadítottak a császárukat túlélték, és a feliratuk később is készülhetett.','The per-year value only shows the order of magnitude: freedmen outlived their emperor, and their inscription could be made later.')+'</p>')
    L.append('      <h3 class="aqh">'+t('Lelőhelyek szerint','By findspot')+'</h3>')
    L.append('      <div class="regwrap"><table class="regtab insctab nmtab">')
    L.append('        <thead><tr><th>'+t('Lelőhely','Findspot')+'</th><th>'+t('Felirat szöveggel','Inscriptions with text')+'</th><th>'+t('Felszabadított-jelölés','Freed marker')+'</th><th>'+t('Rabszolga-jelölés','Slave marker')+'</th><th>'+t('Leggyakoribb császári név','Most frequent imperial name')+'</th></tr></thead>')
    L.append('        <tbody>')
    for k,v in sorted(D['cx'].items(),key=lambda x:-x[1]['n']):
        nm=CXN[k][0 if hu else 1];name=f'<a href="#" data-goto="{v["e"]}">{nm}</a>' if v['e'] else nm
        top=max(NAME,key=lambda x:v['c'][x]);tv=100*v['c'][top]/v['n']
        tops=f'<span class="ik n{top}"></span> {NAME[top]} ({pc(tv)}%)' if v['c'][top]>=5 else '–'
        L.append(f'          <tr><td>{name}</td><td class="pn">{fmt(v["n"])}</td><td class="pn">{pc(100*v["c"]["lib"]/v["n"])}%</td><td class="pn">{pc(100*v["c"]["ser"]/v["n"])}%</td><td>{tops}</td></tr>')
    L.append('        </tbody>')
    L.append('      </table></div>')
    eq=D['cx']['equites'];st=D['cx']['statili']
    L.append('      <p class="hint">'+t(f'A korai kolumbáriumokban sok a felszabadított- és a rabszolga-jelölés, császári név alig van (a Statiliusoknál a feliratok {pc(100*st["c"]["lib"]/st["n"])}%-án áll felszabadított-, {pc(100*st["c"]["ser"]/st["n"])}%-án rabszolga-jelölés). A császári lovastestőrség 2–3. századi temetőjében fordítva: jelölés alig van, a katonák viszont a császáruk nevét viselik (Aurelius: {pc(100*eq["c"]["aureli"]/eq["n"])}%, Ulpius: {pc(100*eq["c"]["ulpi"]/eq["n"])}%, Aelius: {pc(100*eq["c"]["aeli"]/eq["n"])}%).',
      f'In the early columbaria freed and slave markers are frequent and imperial names almost absent (among the Statilii {pc(100*st["c"]["lib"]/st["n"])}% of inscriptions carry a freed marker, {pc(100*st["c"]["ser"]/st["n"])}% a slave marker). In the 2nd–3rd-century cemetery of the imperial horse guard it is the reverse: markers are rare, but the soldiers bear their emperor’s name (Aurelius: {pc(100*eq["c"]["aureli"]/eq["n"])}%, Ulpius: {pc(100*eq["c"]["ulpi"]/eq["n"])}%, Aelius: {pc(100*eq["c"]["aeli"]/eq["n"])}%).')+'</p>')
    L.append('      <p class="hint">'+t(f'A számítás feliratonként egyszer számol egy jelölést vagy nevet, akárhányszor fordul elő. Az időbeli megoszlás 25 éves sávokban készült, mint a „Feliratok” kártyán ({fmt(D["ndated"])} keltezett felirat); a 40-nél kevesebb feliratot tartalmazó sávok nem látszanak.',
      f'Each marker or name is counted once per inscription, however often it occurs. The distribution over time uses 25-year bands, as on the “Inscriptions” card ({fmt(D["ndated"])} dated inscriptions); bands with fewer than 40 inscriptions are not shown.')+'</p>')
    L.append('    </section>')
    src='      <li><b>'+t('Jogállás és császári nevek időben.','Legal status and imperial names over time.')+'</b> '+t('Adat: EDR (lásd „Feliratok”). A kimutatás saját: a jelölések és a nyolc császári családnév keresése a feliratok szövegében, feliratonként egyszer számolva, a több EDR-számon ismétlődő feliratok másodpéldányai nélkül; a császárok saját neve, a légió-, épület- és kerületnevek kiszűrve (nm/calc.py). A császárok uralkodási évei a szokásos kronológia szerint.','Data: EDR (see “Inscriptions”). The summary is our own: a search for the markers and for eight imperial family names in the texts of the inscriptions, counted once per inscription, without the second copies of inscriptions repeated under several EDR numbers; the emperors’ own names and the names of legions, buildings and tribes filtered out (nm/calc.py). Regnal years follow the standard chronology.')+'</li>'
    sub=t('felszabadított- és rabszolga-jelölések, Iuliusok, Claudiusok, Aureliusok hullámai, császári felszabadítottak','freed and slave markers, the waves of Iulii, Claudii and Aurelii, imperial freedmen')
    return '\n'.join(L)+'\n',src,sub
if __name__=='__main__':
    for l in ('hu','en'):
        c,s,sub=build(l);print(len(c.split('\n')));print([p for p in c.split('\n') if 'A hullámok' in p or 'A felszabadított-jelölés' in p or 'korai kolumb' in p])
    print({k:peak(k) for k,_ in NM})
