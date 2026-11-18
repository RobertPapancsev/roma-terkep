# v84: „Foglalkozások a feliratokon” kártya – közös generátor (hu/en). Adat: occ/calc.py -> occ/data.json
import json,math
D=json.load(open('occ/data.json'));I=json.load(open('insc/data.json'))
ST=['il','is','l','s','f','u']
STL={'hu':['császári felszabadított (Augusti libertus)','császári rabszolga (Caesaris servus)','felszabadított','rabszolga','szabadon született (apja nevével)','nincs kiírva'],
     'en':['imperial freedman/woman (Augusti libertus)','imperial slave (Caesaris servus)','freed','slave','freeborn (with father’s name)','not stated']}
SECT=[('build','Építőipar','Building'),('make','Kézművesség','Crafts and manufacture'),('sell','Kereskedelem','Trade'),('bank','Pénzügyek','Banking'),('prof','Tanult szakmák','Professions'),('serv','Szolgáltatás, szórakoztatás','Services and entertainment'),('dom','Háztartási szolgálat','Domestic service'),('trans','Szállítás','Transport'),('admin','Igazgatás, ügyintézés','Administration')]
SN={'hu':{k:h for k,h,e in SECT},'en':{k:e for k,h,e in SECT}}
CXN={'liviae':('Livia szolgáinak és felszabadítottjainak kolumbáriuma (Monumentum Liviae)','The columbarium of Livia’s slaves and freedmen (Monumentum Liviae)'),
 'statili':('A Statiliusok kolumbáriuma','The columbarium of the Statilii'),'volusii':('A Volusiusok síremléke','The tomb of the Volusii'),
 'codini':('A Vigna Codini kolumbáriumai','The columbaria of the Vigna Codini'),'salario':('A Salaria-temető','The Salarian cemetery'),
 'spaolo':('San Paolo fuori le mura és környéke','San Paolo fuori le mura and surroundings'),'forum':('Forum Romanum','Forum Romanum')}
# cím a feliraton: (kulcs, latin kifejezés, megjegyzés hu, en, térképelem, koordináta)
AD=[('sacravia','de Sacra via','','', None,'231.9,-93.1'),('subura','de Subura','','',None,None),('velabrum','de Velabro','','',None,None),
 ('vicustuscus','de vico Tusco; ad Vortumnum','Vortumnus szobra a Vicus Tuscuson állt','the statue of Vortumnus stood in the Vicus Tuscus',None,'4.1,-75.6'),
 ('compitum','a compito Aliario','','',None,None),('castor','post aedem Castoris','a Castor-templom mögött','behind the temple of Castor','castor',None),
 ('caputafr','a Caput Africae','a császári apródiskola (paedagogium) a Caeliuson','the imperial school for pages (paedagogium) on the Caelian',None,None),
 ('portusvin','a portu vinario','','',None,None),('lolliana','ex horreis Lollianis','','','horrealolliana',None),
 ('sexareae','ab sex areis','','',None,None),('galbae','de horreis Galbae','','','horreagalbae',None),('foresq','de foro Esquilino','','',None,None),
 ('fontinalis','a porta Fontinale','','','fontinalis',None),('marcelli','a theatro Marcelli','','','marcellus',None),('libitina','ab luco Libitinae','','',None,None),
 ('mercsobr','a Mercurio Sobrio','','',None,None),('forumvin','de foro vinario','','',None,None),('vicuslongus','de vico Longo','','',None,None),
 ('agrippiana','de horreis Agrippianis','','','horrea',None),('macliviae','de macello Liviae','','','macellumliviae',None),('basiulia','de basilica Iulia','','','julia',None),
 ('hercmus','ab Hercule Musarum','','','porticusphilippi',None),('cloaca','ab cloaca maxima','','','cloacamax',None),('trigemina','ab extra porta Trigemina','','','portatrigemina',None),
 ('iugarius','de vico Iugario','','',None,'-205,-112'),('sallust','ex hortis Sallustianis','','','hortisallustiani',None),
 ('circusmax','de circo maximo ante pulvinar','a Circus Maximusban, a díszpáholy előtt','in the Circus Maximus, in front of the pulvinar',None,None),
 ('viminalis','de colle Viminale','','',None,None),('transtib','a Transtiberim','','',None,None)]
OB={o['k']:o for o in D['occ']}
import sys
sys.path.insert(0,'occ');import lex
LX={k:(la,hu,en) for k,la,_,hu,en,_ in lex.L}
def short(k,lang):return LX[k][1 if lang=='hu' else 2].split(',')[0].split(' (')[0]
TOPN=25;MINN=5
def build(lang):
    hu=lang=='hu';t=lambda a,b:a if hu else b
    fmt=(lambda n:f'{n:,}'.replace(',',' ')) if hu else (lambda n:f'{n:,}')
    pc=lambda x:(f'{x:.1f}'.replace('.',',') if hu else f'{x:.1f}')
    S=D['sect'];mx=max(v['t'] for v in S.values())
    order=sorted(S,key=lambda k:-S[k]['n'])
    def segs(st,tot,base):
        return ''.join(f'<span class="ok o{ST[i]}" data-n="{100*st[i]/base:.2f}" data-p="{100*st[i]/tot:.2f}" style="width:{100*st[i]/base:.2f}%"></span>' for i in range(6) if st[i])
    bars='\n'.join(f'        <div class="fe" data-s="{k}" data-st="{",".join(map(str,S[k]["st"]))}" data-c="{S[k]["n"]}" tabindex="0" role="button" aria-pressed="false"><span class="fen">{SN[lang][k]}</span><span class="feb">{segs(S[k]["st"],S[k]["t"],mx)}</span><span class="fev">{fmt(S[k]["n"])}</span></div>' for k in order)
    leg=' · '.join(f'<span class="ik o{ST[i]}"></span> <span class="il">{STL[lang][i]}</span>' for i in range(6))
    rows=[]
    occs=[o for o in D['occ'] if o['n']>=MINN]
    for j,o in enumerate(occs):
        mini=''.join(f'<span class="ok o{ST[i]}" style="width:{100*o["st"][i]/o["n"]:.1f}%"></span>' for i in range(6) if o['st'][i])
        rows.append(f'          <tr data-s="{o["s"]}"{" class=\"otop\"" if j<TOPN else ""}><td><i lang="la">{o["la"]}</i></td><td>{o["hu"] if hu else o["en"]}</td><td>{SN[lang][o["s"]]}</td><td class="pn">{fmt(o["n"])}</td><td><span class="omini">{mini}</span></td></tr>')
    # háztartások
    rate=100*D['nocc']/D['ntext']
    cx=[]
    for k,v in sorted(D['cx'].items(),key=lambda x:-x[1]['o']/max(1,x[1]['n'])):
        if v['o']<30 or k not in CXN:continue
        nm=CXN[k][0 if hu else 1]
        name=f'<a href="#" data-goto="{v["e"]}">{nm}</a>' if v['e'] else nm
        top=', '.join(f'{short(x,lang)} ({n})' for x,n in v['top'][:4])
        cx.append(f'          <tr><td>{name}</td><td class="pn">{fmt(v["n"])}</td><td class="pn">{fmt(v["o"])} ({pc(100*v["o"]/v["n"])}%)</td><td>{top}</td></tr>')
    ad=[]
    for k,la,nh,ne,el,at in sorted(AD,key=lambda a:-D['addr'][a[0]]['n']):
        v=D['addr'][k]
        if v['n']==0:continue
        lab=f'<i lang="la">{la}</i>'
        if el:lab=f'<a href="#" data-goto="{el}">{lab}</a>'
        elif at:lab=f'<a href="#" data-goto="" data-at="{at}">{lab}</a>'
        note=nh if hu else ne
        sb=f'<span class="sub">{note}</span>' if note else ''
        ad.append(f'          <tr><td>{lab}{sb}</td><td class="pn" title="{", ".join(v["ids"])}">{v["n"]}</td><td>{", ".join(short(x,lang) for x in v["occ"])}</td></tr>')
    # megállapítások számai
    tot=sum(v['n'] for v in S.values())
    big=round(100*(S['admin']['n']+S['dom']['n'])/D['nocc'])
    imp=lambda k:round(100*(S[k]['st'][0]+S[k]['st'][1])/S[k]['t'])
    mk=lambda k:sum(S[k]['st'][:5])
    B=D['bins'];T=D['time'];tt=[sum(T[k][i] for k in T) for i in range(len(B))]
    c1=round(100*sum(tt[i] for i,x in enumerate(B) if 0<=x<100)/sum(tt))
    a=I['time']['all'];it=[sum(a[k][i] for k in a) for i in range(len(B))]
    r1=100*sum(tt[i] for i,x in enumerate(B) if 0<=x<50)/sum(it[i] for i,x in enumerate(B) if 0<=x<50)
    r3=100*sum(tt[i] for i,x in enumerate(B) if 200<=x<300)/sum(it[i] for i,x in enumerate(B) if 200<=x<300)
    nrow=len(occs)
    L=[]
    L.append('    <section class="card" id="occcard">')
    L.append('      <h2>'+t('Foglalkozások a feliratokon','Occupations in the inscriptions')+'</h2>')
    L.append('      <p class="hint">'+t(f'Az EDR {fmt(D["nrome"])} római feliratából {fmt(D["ntext"])} feliratnak van olvasható szövege az adatállományban. Egy {D["nlex"]} latin foglalkozásnévből álló szótárral {fmt(D["nocc"])} feliraton találtunk foglalkozást: orvost, szakácsot, aranyművest, könyvelőt. A katonák feliratai ({fmt(D["nmil"])}) ebből a kimutatásból kimaradtak, ahogy a papi, a szenátori és a lovagi tisztségek is. A találatokat egyenként átnéztük, és kihagytuk azokat, ahol a szó nem a személy foglalkozása: például a császárok „Medicus” győzelmi címét, a Mercator, Sutorius vagy Fullonius nevet, a „Bona Dea Nutrix” istennevet, a törvények és rendeletek szövegét. Az EDR még nem tartalmazza Róma összes feliratát, ezért a számok arányokat mutatnak, nem teljes létszámot.',
      f'Of the {fmt(D["nrome"])} inscriptions from Rome in EDR, {fmt(D["ntext"])} have a readable text in the data set. Using a dictionary of {D["nlex"]} Latin occupational titles we found an occupation in {fmt(D["nocc"])} inscriptions: physicians, cooks, goldsmiths, accountants. The inscriptions of soldiers ({fmt(D["nmil"])}) are left out of this summary, as are priesthoods and senatorial and equestrian offices. Every hit was checked by reading, and those where the word is not the person’s occupation were dropped: for example the emperors’ victory title “Medicus”, the names Mercator, Sutorius or Fullonius, the divine name “Bona Dea Nutrix”, and the texts of laws and decrees. EDR does not yet contain all the inscriptions of Rome, so the figures show proportions, not complete head counts.')+'</p>')
    L.append('      <h3 class="aqh">'+t('Ágazatok és jogállás','Sectors and legal status')+'</h3>')
    L.append('      <p class="hint">'+t('A sáv hossza a feliratok számát, a színek a foglalkozást viselő személy jogállását mutatják. Kattints egy ágazatra: az időgörbe és a foglalkozások táblázata arra szűkül; újabb kattintás visszaállítja.','The length of the bar shows the number of inscriptions, the colours the legal status of the person holding the occupation. Click a sector: the time curve and the table of occupations narrow to it; click again to reset.')+'</p>')
    L.append('      <div class="seg occmode" role="group" aria-label="'+t('A sávok tartalma','What the bars show')+'"><button data-m="n" aria-pressed="true">'+t('Feliratok száma','Number of inscriptions')+'</button><button data-m="p" aria-pressed="false">'+t('Jogállás aránya','Share by legal status')+'</button></div>')
    L.append('      <div class="foodest occsec">')
    L.append(bars)
    L.append('      </div>')
    L.append('      <p class="hint bldleg occleg">'+leg+'</p>')
    L.append('      <p class="hint popinfo" id="occinfo">'+t('Vidd az egeret egy ágazatra, vagy kattints rá.','Hover over a sector, or click it.')+'</p>')
    L.append('      <p class="hint">'+t(f'Az igazgatás és a háztartási szolgálat adja a foglalkozást megnevező feliratok {big}%-át. Ezekben a legmagasabb a császári háztartás aránya (igazgatás: {imp("admin")}%, háztartási szolgálat: {imp("dom")}%). A kereskedők feliratain egyetlen császári rabszolga vagy felszabadított sincs. A kézműveseknél és a kereskedőknél, ahol a jogállás ki van írva, többnyire felszabadított áll (kézművesség: {mk("make")} jelölt közül {S["make"]["st"][2]}, kereskedelem: {mk("sell")} közül {S["sell"]["st"][2]}).',
      f'Administration and domestic service account for {big}% of the inscriptions that name an occupation. They also have the highest share of the imperial household (administration: {imp("admin")}%, domestic service: {imp("dom")}%). Not a single imperial slave or freedman appears among the traders. Among craftsmen and traders, where a status is stated it is mostly “freed” (crafts: {S["make"]["st"][2]} of {mk("make")}, trade: {S["sell"]["st"][2]} of {mk("sell")}).')+'</p>')
    L.append('      <p class="hint">'+t('A jogállást a foglalkozásnévhez tartozó névben keressük, a tétel vagy a mondat határáig, és közvetlenül a foglalkozásnév után. Csak azt a jelölést fogadjuk el, amely nyelvtani esetben egyezik a foglalkozásnévvel (libertus, servus, verna, vicarius, vagy az apa neve: „Marci filius”); a kiadók által pótolt „servus” is számít. Császári az, akinél a jelölés előtt a császár vagy a császárné áll (Augusti libertus, Caesaris servus), vagy egynevű személy mellett csak ennyi: „Felix Caesaris dispensator”. Több személyt felsoroló feliratoknál így is előfordulhat téves hozzárendelés. A „nincs kiírva” nem jelent szabad születést: az egynevű személyeknél (például „Blandus structor”) a felirat a jogállást egyszerűen nem közli.',
      'Legal status is looked for in the name that belongs to the occupational title, back to the boundary of the entry or sentence, and directly after the title. Only a marker that agrees in grammatical case with the title is accepted (libertus, servus, verna, vicarius, or the father’s name: “Marci filius”); a “servus” supplied by the editors also counts. A person is imperial when the marker is preceded by the emperor or empress (Augusti libertus, Caesaris servus), or when a single-named person has only this: “Felix Caesaris dispensator”. In inscriptions listing several people a wrong assignment can still occur. “Not stated” does not mean freeborn: for people with a single name (for example “Blandus structor”) the inscription simply does not give the status.')+'</p>')
    L.append('      <h3 class="aqh">'+t('A foglalkozások időben','Occupations over time')+'</h3>')
    L.append('      <div class="bldchart" id="occchart"></div>')
    L.append('      <p class="hint popinfo" id="occtinfo">'+t('Vidd az egeret egy oszlopra; kattintásra a térkép évcsúszkája arra az időre áll.','Hover over a bar; click to set the map’s year slider to that time.')+'</p>')
    L.append('      <p class="hint">'+t(f'Az időgörbe ugyanúgy készült, mint a „Feliratok” kártyán (25 éves sávok, {fmt(D["ndated"])} keltezett felirat). A foglalkozást megnevező feliratok {c1}%-a a Kr. u. 1. századra esik, a nagy kolumbáriumok korára. Az összes keltezett felirathoz mérve is ekkor a leggyakoribbak: a Kr. u. 1. század első felében {pc(r1)}%, a 3. században {pc(r3)}%.',
      f'The time curve is built the same way as on the “Inscriptions” card (25-year bands, {fmt(D["ndated"])} dated inscriptions). {c1}% of the inscriptions naming an occupation fall in the 1st century AD, the age of the great columbaria. Measured against all dated inscriptions they are also most frequent then: {pc(r1)}% in the first half of the 1st century AD, {pc(r3)}% in the 3rd century.')+'</p>')
    L.append('      <h3 class="aqh">'+t('A leggyakoribb foglalkozások','The most frequent occupations')+'</h3>')
    L.append('      <div class="regwrap"><table class="regtab insctab occtab">')
    L.append('        <thead><tr><th>'+t('Latin név','Latin title')+'</th><th>'+t('Jelentése','Meaning')+'</th><th>'+t('Ágazat','Sector')+'</th><th>'+t('Felirat','Inscriptions')+'</th><th>'+t('Jogállás','Legal status')+'</th></tr></thead>')
    L.append('        <tbody>')
    L+=rows
    L.append('        </tbody>')
    L.append('      </table></div>')
    L.append('      <p class="hint"><button class="occmore" id="occmore" data-on="0"><span class="om0">'+t(f'Mind a {nrow} foglalkozás mutatása',f'Show all {nrow} occupations')+'</span><span class="om1">'+t(f'Csak a {TOPN} leggyakoribb',f'Only the {TOPN} most frequent')+'</span></button></p>')
    L.append('      <p class="hint">'+t(f'A táblázatban a legalább öt feliraton előforduló foglalkozások szerepelnek. Egy felirat több foglalkozást is megnevezhet, ezért a sorok együtt több feliratot adnak ki, mint ahány felirat van. Néhány név többértelmű: a structor kőműves és asztali tálaló is lehet, az argentarius bankár, a faber argentarius ezüstműves.',
      'The table lists the occupations found in at least five inscriptions. One inscription can name several occupations, so the rows add up to more than the number of inscriptions. Some titles are ambiguous: a structor can be a mason or a table-server, an argentarius is a banker, a faber argentarius a silversmith.')+'</p>')
    L.append('      <h3 class="aqh">'+t('Nagy háztartások sírkamrái','The tomb chambers of great households')+'</h3>')
    L.append('      <p class="hint">'+t(f'Átlagosan a feliratok {pc(rate)}%-a nevez meg foglalkozást. A nagy háztartások kolumbáriumaiban ennek a többszöröse: itt a rabszolgákat és a felszabadítottakat a háztartásban végzett feladatukkal azonosították.',
      f'On average {pc(rate)}% of the inscriptions name an occupation. In the columbaria of the great households the share is several times higher: here slaves and freedmen were identified by the job they did in the household.')+'</p>')
    L.append('      <div class="regwrap"><table class="regtab insctab">')
    L.append('        <thead><tr><th>'+t('Lelőhely','Findspot')+'</th><th>'+t('Felirat','Inscriptions')+'</th><th>'+t('Foglalkozással','With an occupation')+'</th><th>'+t('Leggyakoribb foglalkozások','Most frequent occupations')+'</th></tr></thead>')
    L.append('        <tbody>')
    L+=cx
    L.append('        </tbody>')
    L.append('      </table></div>')
    L.append('      <h3 class="aqh">'+t('Műhelyek és boltok címe','Addresses of workshops and shops')+'</h3>')
    L.append('      <p class="hint">'+t('Néhány felirat azt is megmondja, hol dolgozott az illető: „aurifex de Sacra via” (aranyműves a Sacra Viáról). A linkre kattintva a térkép odaugrik; a feliratok száma fölé vitt egérrel az EDR-azonosítók látszanak.',
      'Some inscriptions also say where the person worked: “aurifex de Sacra via” (goldsmith from the Sacra Via). Click a link to jump there on the map; hover over the number of inscriptions to see the EDR identifiers.')+'</p>')
    L.append('      <div class="regwrap"><table class="regtab insctab">')
    L.append('        <thead><tr><th>'+t('Hely a feliraton','Place as named in the inscription')+'</th><th>'+t('Felirat','Inscriptions')+'</th><th>'+t('Foglalkozások','Occupations')+'</th></tr></thead>')
    L.append('        <tbody>')
    L+=ad
    L.append('        </tbody>')
    L.append('      </table></div>')
    L.append('      <p class="hint">'+t(f'A Sacra Via {D["addr"]["sacravia"]["n"]} feliratán csak luxuscikkek készítői és árusai szerepelnek: gyöngyárusok, aranyművesek, ékkő- és ezüstműves, vésnök, illatszerkészítő, koszorúkötő és sípkészítő. A Vicus Tuscus és a compitum Aliarium feliratain ruhakészítők, a Castor-templom mögött bankárok és egy köpenykészítő állnak.',
      f'The {D["addr"]["sacravia"]["n"]} inscriptions from the Sacra Via name only makers and sellers of luxury goods: pearl-dealers, goldsmiths, a gem-cutter and a silversmith, an engraver, a perfumer, a garland-maker and a flute-maker. The inscriptions from the Vicus Tuscus and the compitum Aliarium name clothiers, those from behind the temple of Castor bankers and a cloak-maker.')+'</p>')
    L.append('    </section>')
    src='      <li><b>'+t('Foglalkozások a feliratokon.','Occupations in the inscriptions.')+'</b> '+t(f'Adat: EDR (lásd „Feliratok”). A kimutatás saját: {D["nlex"]} latin foglalkozásnév keresése a feliratok szövegében, kilenc ágazatba sorolva; a találatok kézi átnézésével (a kizárt tételek: occ/excl.py); a jogállás a foglalkozásnévhez tartozó név esetben egyező jelölései alapján; a katonai feliratok és az ismétlődő feliratok másodpéldányai nélkül; a címek a foglalkozásnév utáni helymegjelölésből (occ/lex.py, occ/calc.py). A téma alapműve: Sandra R. Joshel, <i>Work, Identity, and Legal Status at Rome. A Study of the Occupational Inscriptions</i>, Norman–London 1992.',
      f'Data: EDR (see “Inscriptions”). The summary is our own: a search for {D["nlex"]} Latin occupational titles in the texts of the inscriptions, grouped into nine sectors; every hit checked by reading (excluded items: occ/excl.py); legal status from case-agreeing markers in the name belonging to the title; military inscriptions and second copies of repeated inscriptions excluded; addresses from the place given after the title (occ/lex.py, occ/calc.py). The standard study of the subject: Sandra R. Joshel, <i>Work, Identity, and Legal Status at Rome. A Study of the Occupational Inscriptions</i>, Norman–London 1992.')+'</li>'
    sub=t(f'{fmt(D["nocc"])} felirat orvosokról, szakácsokról, aranyművesekről: ágazatok, jogállás, műhelyek címe',f'{fmt(D["nocc"])} inscriptions naming physicians, cooks, goldsmiths: sectors, legal status, workshop addresses')
    return '\n'.join(L)+'\n',src,sub
if __name__=='__main__':
    for l in ('hu','en'):
        c,s,sub=build(l);print(len(c.split('\n')),sub)
