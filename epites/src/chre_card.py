# v95: „Éremkincsek: mikor rejtettek el pénzt” kártya – közös generátor (hu/en). Adat: chre/calc.py -> chre/data.json
import json
D=json.load(open('chre/data.json'));B=D['bins'];W=D['w']
EXCL={'6138':('a leírás szerint 5. századi érméket is tartalmaz, a keltezése mégis 161','contains coins up to the 5th century according to its description, yet is dated 161'),'16183':('két aureus, nem biztos, hogy együtt kerültek elő','two aurei, not certain that they were found together')}
# egyenként átolvasva (a CHRE neve és összefoglalója alapján): megnevezés, tartalom, egykorú esemény Rómában
HN={'6929':('Hotel Zara, 1935','Hotel Zara, 1935','254 denarius','254 denarii','',''),
 '6232':('Via Portuense, 1888','Via Portuense, 1888','82 bronzérme','82 bronze coins','',''),
 '6252':('Tiberis, 1885–1886','Tiber, 1885–1886','294 denarius','294 denarii','',''),
 '5482':('Via Po, 1927','Via Po, 1927','378 aureus','378 aurei','Marcus Aurelius és Lucius Verus közös uralma (161–169)','joint reign of Marcus Aurelius and Lucius Verus (161–169)'),
 '6146':('Aventinus, 1892','Aventine, 1892','300–400 aureus (42 maradt meg)','300–400 aurei (42 recovered)','Marcus Aurelius és Lucius Verus közös uralma (161–169)','joint reign of Marcus Aurelius and Lucius Verus (161–169)'),
 '14228':('Vigna Fumaroli, 1908','Vigna Fumaroli, 1908','45 denarius','45 denarii','Elagabalus meggyilkolása (222)','murder of Elagabalus (222)'),
 '3006':('Villa Patrizi, 1908','Villa Patrizi, 1908','40 ezüstérme','40 silver coins','Elagabalus meggyilkolása (222)','murder of Elagabalus (222)'),
 '14244':('Via Monte Polacco, 1889','Via Monte Polacco, 1889','300 ezüst- és billonérme','300 silver and billon coins','Valerianus fogságba esik; alamann betörés Itáliába (260)','capture of Valerian; Alamannic invasion of Italy (260)'),
 '15031':('Esquilinus, Via Turati, 2001','Esquiline, Via Turati, 2001','6 antoninianus, ékszerekkel','6 antoniniani, with jewellery','Valerianus fogságba esik; alamann betörés Itáliába (260)','capture of Valerian; Alamannic invasion of Italy (260)'),
 '14245':('Testaccio, 1911','Testaccio, 1911','758 érme','758 coins','Gallienus meggyilkolása (268); Aurelianus fala (271-től)','murder of Gallienus (268); Aurelian’s wall (from 271)'),
 '14988':('Testaccio, Via Branca és Via Franklin között, 1911','Testaccio, between Via Branca and Via Franklin, 1911','885 bronzérme és antoninianus','885 bronze coins and antoniniani','Gallienus meggyilkolása (268); Aurelianus fala (271-től)','murder of Gallienus (268); Aurelian’s wall (from 271)'),
 '4116':('Róma, 1902','Rome, 1902','arany és ezüst díszérmék','gold and silver medallions','Carinus és Diocletianus polgárháborúja (285)','civil war of Carinus and Diocletian (285)'),
 '15413':('Róma, 1929','Rome, 1929','219 bronz nummus','219 bronze nummi','Alarich első ostroma (408)','Alaric’s first siege (408)'),
 '4473':('Tiberis','Tiber','69 arany solidus','69 gold solidi','Alarich kifosztja Rómát (410)','Alaric sacks Rome (410)'),
 '13939':('Villa Giulia, 1922','Villa Giulia, 1922','680 bronz nummus','680 bronze nummi','a vandálok kifosztják Rómát (455)','the Vandals sack Rome (455)'),
 '13938':('La Magliana','La Magliana','33 bronz nummus','33 bronze nummi','a vandálok kifosztják Rómát (455)','the Vandals sack Rome (455)'),
 '4622':('Palatinus, a Vesta-szüzek háza, 1899','Palatine, House of the Vestals, 1899','397 arany solidus','397 gold solidi','Ricimer ostroma (472)','Ricimer’s siege (472)'),
 '4623':('Esquilinus, 1875','Esquiline, 1875','19 arany solidus','19 gold solidi','','')}
PN=[('Kr. e. 50 – Kr. u. 68','50 BC – AD 68'),('Kr. u. 69–192','AD 69–192'),('193–284','193–284'),('285–395','285–395'),('396–500','396–500')]
def build(lang):
    hu=lang=='hu';t=lambda a,b:a if hu else b
    fmt=(lambda n:f'{n:,}'.replace(',',' ')) if hu else (lambda n:f'{n:,}')
    d1=lambda x:(f'{x:.1f}'.replace('.',',') if hu else f'{x:.1f}')
    pc=lambda x:(f'{x:.0f}' if x>=10 or x<0.05 else d1(x))
    def yy(a,b):
        f=lambda y:(f'Kr. e. {-y}' if y<0 else str(y)) if hu else (f'{-y} BC' if y<0 else str(y))
        return f(a) if a==b else f(a)+'–'+f(b)
    rome=[r for r in D['rome'] if r['id'] not in EXCL];assert all(r['id'] in HN for r in rome)
    he,hi,ne,ni=D['he'],D['hi'],D['ne'],D['ni'];L=[]
    L.append('    <section class="card" id="chrecard">')
    L.append('      <h2>'+t('Éremkincsek: mikor rejtettek el pénzt','Coin hoards: when money was hidden')+'</h2>')
    L.append('      <p class="hint">'+t(f'Az oxfordi Coin Hoards of the Roman Empire (CHRE) adatbázis a Kr. e. 30 és Kr. u. 400 között forgalomban volt érmék kincsleleteit gyűjti a birodalom egész területéről (a későbbi, 5. századi leleteket is felveszi). A letöltött állomány {fmt(D["nall"])} tételt tartalmaz: ebből {fmt(D["nh"])} kincslelet, a többi magányos aranyérme vagy szórványlelet. Itáliából {D["nit"]} kincslelet ismert, Rómából és 10 kilométeres körzetéből mindössze {len(rome)}, amelynek a keltezése megbízható.',
      f'The Oxford database Coin Hoards of the Roman Empire (CHRE) collects the hoards of coins in circulation between 30 BC and AD 400 from the whole empire (it also records later, 5th-century finds). The downloaded file contains {fmt(D["nall"])} entries: {fmt(D["nh"])} of them are hoards, the rest single gold coins or stray finds. {D["nit"]} hoards are known from Italy, and from Rome and its 10-kilometre surroundings only {len(rome)} with a reliable date.')+'</p>')
    L.append('      <p class="hint">'+t('Egy kincset a legkésőbbi érméje keltez. Ez az elrejtés legkorábbi lehetséges ideje, nem a tényleges ideje: a pénzt ennél később is elrejthették. Az is torzít, hogy csak azokat a kincseket ismerjük, amelyekért a gazdájuk nem ment vissza.',
      'A hoard is dated by its latest coin. This is the earliest possible time of concealment, not the actual one: the money may have been hidden later. It also matters that we know only those hoards whose owners never came back for them.')+'</p>')
    L.append('      <h3 class="aqh">'+t('A birodalom, Itália és Róma','The empire, Italy and Rome')+'</h3>')
    Wd,H,Lm,Rm,Tp,Bt=660,270,40,10,10,44;pe=[100*v/ne for v in he];pi=[100*v/ni for v in hi];mx=max(pe+pi)*1.06;X0,X1=B[0],B[-1]+W
    xs=lambda x:Lm+(x-X0)/(X1-X0)*(Wd-Lm-Rm);sy=lambda v:Tp+(1-v/mx)*(H-Tp-Bt)
    sv=[f'      <div class="bldchart chrechart"><svg viewBox="0 0 {Wd} {H}" class="bldsvg chresvg" role="img">']
    for v in range(0,int(mx)+1,5):sv.append(f'<line x1="{Lm}" x2="{Wd-Rm}" y1="{sy(v):.1f}" y2="{sy(v):.1f}" class="pg"/><text x="{Lm-5}" y="{sy(v)+4:.1f}" text-anchor="end" class="pt">{v}%</text>')
    for x in (-50,100,200,300,400,500):
        lab=(t('Kr. e. 50','50 BC') if x==-50 else '1' if x==0 else (t('Kr. u. 100','AD 100') if x==100 else str(x)))
        sv.append(f'<text x="{xs(x):.1f}" y="{H-Bt+30}" text-anchor="{"start" if x==-50 else "end" if x==500 else "middle"}" class="pt">{lab}</text>')
    sv.append(f'<line x1="{Lm}" x2="{Wd-Rm}" y1="{H-Bt}" y2="{H-Bt}" class="pax"/>')
    for ev in (410,455,472):sv.append(f'<line x1="{xs(ev):.1f}" x2="{xs(ev):.1f}" y1="{Tp}" y2="{H-Bt+14}" class="chev"/>')
    for k,p in (('ce',pe),('ci',pi)):sv.append('<path class="chrel '+k+'" d="'+''.join(('L' if i else 'M')+f'{xs(B[i]+W/2):.1f},{sy(v):.1f}' for i,v in enumerate(p))+'"/>')
    for r in rome:
        m=(r['t1']+r['t2'])/2;sv.append(f'<line x1="{xs(m):.1f}" x2="{xs(m):.1f}" y1="{H-Bt+2}" y2="{H-Bt+14}" class="chrt"/>')
    sv.append('</svg></div>');L.append(''.join(sv))
    L.append('      <p class="hint bldleg"><span class="ik ce"></span> <span class="il">'+t('a birodalom','the empire')+'</span> · <span class="ik ci"></span> <span class="il">'+t('Itália','Italy')+'</span> · <span class="ik crt"></span> <span class="il">'+t('egy-egy római kincs','one hoard from Rome each')+'</span> · <span class="ik cev"></span> <span class="il">'+t('Róma ostromai: 410, 455, 472','sieges of Rome: 410, 455, 472')+'</span></p>')
    i250=B.index(250);i25=B.index(25)
    L.append('      <p class="hint">'+t(f'A görbe azt mutatja, hogy a keltezett kincsek hány százaléka zárul egy-egy 25 éves szakaszban. A birodalomban a kincsek {pc(pe[i250])}%-a a 250 és 275 közötti negyedszázadban zárul: ez a 3. századi válság, a polgárháborúk, a betörések és a pénzromlás ideje. Itáliában ugyanez a csúcs megvan ({pc(pi[i250])}%), de a legnagyobb az 1. századi: ezek a Vezúv Kr. u. 79-es kitörésekor betemetett campaniai városok pénzei (az itáliai kincsek közül {D["nit_cities"][0][1]} campaniai). Ott nem a gazdák döntése, hanem a katasztrófa őrizte meg a pénzt.',
      f'The curve shows what percentage of the dated hoards close in each 25-year span. In the empire {pc(pe[i250])}% of the hoards close in the quarter-century between 250 and 275: the time of the 3rd-century crisis, of civil wars, invasions and debasement. Italy has the same peak ({pc(pi[i250])}%), but its largest is in the 1st century: this is the money of the Campanian towns buried by the eruption of Vesuvius in AD 79 ({D["nit_cities"][0][1]} of the Italian hoards are from Campania). There it was not the owners’ decision but the catastrophe that preserved the money.')+'</p>')
    L.append('      <h3 class="aqh">'+t('A római kincsek egyenként','The hoards of Rome one by one')+'</h3>')
    L.append('      <div class="regwrap"><table class="regtab insctab chretab">')
    L.append('        <thead><tr><th>'+t('A legkésőbbi érme','Latest coin')+'</th><th>'+t('Lelőhely, év','Findspot, year')+'</th><th>'+t('Tartalom','Contents')+'</th><th>'+t('Egykorú esemény Rómában','Contemporary event in Rome')+'</th></tr></thead>')
    L.append('        <tbody>')
    for r in rome:
        h=HN[r['id']];L.append(f'          <tr><td class="pn">{yy(r["t1"],r["t2"])}</td><td>{h[0 if hu else 1]}</td><td>{h[2 if hu else 3]}</td><td>{h[4 if hu else 5] or "–"}</td></tr>')
    L.append('        </tbody>')
    L.append('      </table></div>')
    c3=sum(1 for r in rome if 250<=(r['t1']+r['t2'])/2<275);c5=[r for r in rome if (r['t1']+r['t2'])/2>=400];s5=sum(1 for r in c5 if HN[r['id']][4])
    L.append('      <p class="hint">'+t(f'Egybeesik-e az elrejtés az ostromokkal? Az 5. században igen: a hat kincsből öt záró érméje egy-egy ostrom évére vagy az azt megelőző néhány évre esik. A Tiberisből előkerült 69 solidus legkésőbbi darabja éppen 410 körüli, a Palatinuson, a Vesta-szüzek házában talált 397 solidusé 467–472 közötti, Ricimer ostroma idejéből. A 3. században négy római kincs zárul 253 és 268 között, ugyanakkor, amikor a birodalomban a legtöbb.',
      f'Does concealment coincide with the sieges? In the 5th century it does: for five of the six hoards the latest coin falls in the year of a siege or in the few years before it. The latest piece of the 69 solidi recovered from the Tiber is of about 410; that of the 397 solidi found in the House of the Vestals on the Palatine is of 467–472, the time of Ricimer’s siege. In the 3rd century four hoards from Rome close between 253 and 268, at the same time as most hoards in the empire.')+'</p>')
    L.append('      <p class="hint">'+t(f'Ez azonban {len(rome)} kincs, nem statisztika. Az „egykorú esemény” oszlop időbeli egybeesést mutat, nem bizonyított okot; az 5. századi Rómát olyan sűrűn érte támadás, hogy szinte bármely kincs közel esik valamelyikhez. A birodalmi csúcsoknak Rómában nincs megfelelőjük: a 2. század második feléből, amikor a birodalomban sok kincs zárul, a városból csak két aranykincs ismert. Két tételt kihagytunk: az egyik {EXCL["6138"][0]}, a másik {EXCL["16183"][0]}. A város 25 kilométeres körzetében további {len(D["sub"])} kincs van (például három Ostiából, 260–282 közötti záró érmével).',
      f'But these are {len(rome)} hoards, not statistics. The “contemporary event” column shows coincidence in time, not a proven cause; 5th-century Rome was attacked so often that almost any hoard falls near one of the attacks. The peaks of the empire have no counterpart in Rome: from the second half of the 2nd century, when many hoards close in the empire, only two gold hoards are known from the city. We left out two entries: one {EXCL["6138"][1]}, the other {EXCL["16183"][1]}. Within 25 kilometres of the city there are a further {len(D["sub"])} hoards (for example three from Ostia, with latest coins of 260–282).')+'</p>')
    L.append('      <h3 class="aqh">'+t('Mit mutatnak még a kincsek? Pénzromlás és pénzverdék','What else do the hoards show? Debasement and mints')+'</h3>')
    L.append('      <div class="regwrap"><table class="regtab insctab agetab">')
    L.append('        <thead><tr><th>'+t('A kincs zárása','Closing of the hoard')+'</th><th>'+t('Érme','Coins')+'</th><th>'+t('arany','gold')+'</th><th>'+t('ezüst','silver')+'</th><th>'+t('gyenge ezüst (billon)','base silver (billon)')+'</th><th>'+t('bronz','bronze')+'</th><th>'+t('Róma verdéjéből','from the mint of Rome')+'</th></tr></thead>')
    L.append('        <tbody>')
    for i,m in enumerate(D['mat2']):
        n=sum(v for k,v in m.items() if k!='other')
        L.append(f'          <tr><td>{PN[i][0 if hu else 1]}</td><td class="pn">{fmt(n)}</td>'+''.join(f'<td class="pn">{pc(100*m.get(k,0)/n)}%</td>' for k in('gold','silver','billon','bronze'))+f'<td class="pn">{pc(D["romesh"][i])}%</td></tr>')
    L.append('        </tbody>')
    L.append('      </table></div>')
    m2=D['mat2'];sh=lambda i,k:pc(100*m2[i].get(k,0)/sum(v for kk,v in m2[i].items() if kk!='other'))
    L.append('      <p class="hint">'+t(f'Az itáliai kincsek {fmt(D["nco"])} érméje a kincs zárásának ideje szerint. Az anyag oszlopai az ismert anyagú érmék megoszlását adják, az utolsó oszlop azt, hogy az ismert verdéjű érmék hány százaléka készült Rómában. A 3. században a jó ezüst helyére a gyenge ezüstötvözet lép ({sh(2,"billon")}%), az 5. századra pedig csak apró bronzpénz és arany solidus marad. Róma verdéje a 2. században szinte egyedül látta el Itáliát ({pc(D["romesh"][1])}%); a 3. század végétől a mediolanumi, ticinumi és sisciai verde osztozik vele ({pc(D["romesh"][3])}%). A sorok érmeszáma néhány nagy kincstől függ, ezért az arányok csak nagyságrendet mutatnak.',
      f'The {fmt(D["nco"])} coins of the Italian hoards by the time the hoard closes. The material columns give the distribution of the coins of known material; the last column shows what percentage of the coins of known mint were struck in Rome. In the 3rd century good silver gives way to a base silver alloy ({sh(2,"billon")}%), and by the 5th century only small bronze coins and gold solidi remain. In the 2nd century the mint of Rome supplied Italy almost alone ({pc(D["romesh"][1])}%); from the late 3rd century it shares the task with the mints of Mediolanum, Ticinum and Siscia ({pc(D["romesh"][3])}%). The coin totals of the rows depend on a few large hoards, so the shares show only the order of magnitude.')+'</p>')
    ra=D['reign_all'];ri=D['reign_it']
    L.append('      <p class="hint">'+t(f'A birodalomban a legtöbb kincs Marcus Aurelius ({ra[0][1]}), I. Constantinus ({ra[1][1]}) és a galliai ellencsászár, Tetricus ({ra[2][1]}) érméjével zárul; Itáliában Vespasianuséval ({ri[0][1]}, a Vezúv miatt), utána Augustus ({ri[1][1]}) és Aurelianus ({ri[2][1]}) következik.',
      f'In the empire most hoards close with a coin of Marcus Aurelius ({ra[0][1]}), Constantine I ({ra[1][1]}) and the Gallic usurper Tetricus ({ra[2][1]}); in Italy with one of Vespasian ({ri[0][1]}, because of Vesuvius), followed by Augustus ({ri[1][1]}) and Aurelian ({ri[2][1]}).')+'</p>')
    L.append('    </section>')
    src='      <li><b>'+t('Éremkincsek.','Coin hoards.')+'</b> '+t('Coin Hoards of the Roman Empire (CHRE), Ashmolean Museum és Oxford Roman Economy Project, University of Oxford: <a href="https://chre.ashmus.ox.ac.uk">chre.ashmus.ox.ac.uk</a>; CSV-letöltés 2026. november 12-én; licenc: CC BY-NC-SA (nem kereskedelmi felhasználás). Az összesítés saját: a kincsek zárása 25 éves szakaszokban, a Róma 10 kilométeres körzetében talált kincsek egyenként átolvasva, az itáliai kincsek érméinek anyaga és verdéje (chre/calc.py). Az események évszámai a szokásos történeti kronológiát követik.',
      'Coin Hoards of the Roman Empire (CHRE), Ashmolean Museum and Oxford Roman Economy Project, University of Oxford: <a href="https://chre.ashmus.ox.ac.uk">chre.ashmus.ox.ac.uk</a>; CSV download on 12 November 2026; licence: CC BY-NC-SA (non-commercial use). The summary is our own: closing of the hoards in 25-year spans, the hoards found within 10 kilometres of Rome read one by one, material and mint of the coins of the Italian hoards (chre/calc.py). The dates of the events follow the standard historical chronology.')+'</li>'
    sub=t(f'{fmt(D["nh"])} kincslelet a birodalomból, {len(rome)} Rómából: válság, ostromok, pénzromlás',f'{fmt(D["nh"])} hoards from the empire, {len(rome)} from Rome: crisis, sieges, debasement')
    return '\n'.join(L)+'\n',src,sub
if __name__=='__main__':
    import re
    for l in('hu','en'):print(build(l)[2])
    print(re.sub(r'<[^>]+>',' ',build('hu')[0]))
