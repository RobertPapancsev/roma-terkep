# v86: „Életkor és család a sírfeliratokon” kártya – közös generátor (hu/en). Adat: age/calc.py -> age/data.json
import json
D=json.load(open('age/data.json'))
REL=[('spouse','házastárs (coniugi, uxori, marito)','spouse (coniugi, uxori, marito)','fam'),('child','gyermek (filio, filiae)','child (filio, filiae)','fam'),('parent','szülő (patri, matri, parentibus)','parent (patri, matri, parentibus)','fam'),
 ('patron','patrónus (patrono, patronae)','patron (patrono, patronae)','hh'),('sibling','testvér (fratri, sorori)','sibling (fratri, sorori)','fam'),('amic','barát (amico, amicae)','friend (amico, amicae)','am'),
 ('freed','saját felszabadított (liberto suo)','own freedman/woman (liberto suo)','hh'),('contub','élettárs (contubernali)','partner (contubernali)','hh'),('alumn','nevelt gyermek (alumno, alumnae)','foster-child (alumno, alumnae)','hh'),
 ('collib','felszabadított-társ (colliberto)','fellow freedman/woman (colliberto)','hh'),('nepos','távolabbi rokon (nagyszülő, unoka, após, nagybácsi)','wider kin (grandparent, grandchild, in-law, uncle)','kin'),
 ('conserv','rabszolgatárs (conservo)','fellow slave (conservo)','hh'),('nutr','dajka, nevelő (nutrici, mammae, tatae)','nurse, carer (nutrici, mammae, tatae)','hh')]
RA=[('child','gyermek','child'),('alumn','nevelt gyermek','foster-child'),('freed','saját felszabadított','own freedman/woman'),('sibling','testvér','sibling'),('wife','feleség','wife'),('contub','élettárs (contubernalis)','partner (contubernalis)'),('amic','barát','friend'),('husband','férj','husband'),('parent','szülő','parent'),('patron','patrónus','patron')]
LN=[('spouse','házastárs','spouse'),('child','gyermek','child'),('parent','szülő','parent'),('patron','patrónus','patron'),('self','saját magának is (sibi, se vivo)','also for oneself (sibi, se vivo)')]
SX=[('m','férfi','male'),('f','nő','female'),('u','a szövegből nem derül ki','not clear from the text')]
PR=[('0-5','0–4 év','0–4 years'),('5-15','5–14 év','5–14 years'),('15-30','15–29 év','15–29 years'),('30-50','30–49 év','30–49 years'),('50-121','50 év és fölötte','50 years and over')]
CXN={'liviae':('Livia szolgáinak és felszabadítottjainak kolumbáriuma (Monumentum Liviae)','The columbarium of Livia’s slaves and freedmen (Monumentum Liviae)'),'statili':('A Statiliusok kolumbáriuma','The columbarium of the Statilii'),
 'volusii':('A Volusiusok síremléke','The tomb of the Volusii'),'codini':('A Vigna Codini kolumbáriumai','The columbaria of the Vigna Codini'),'salario':('A Salaria-temető','The Salarian cemetery'),
 'spaolo':('San Paolo fuori le mura és környéke','San Paolo fuori le mura and surroundings'),'vatican':('A vatikáni nekropolisz és a via Triumphalis menti temető','The Vatican necropolis and the cemetery along the Via Triumphalis'),
 'pamphilj':('Villa Pamphilj temetői','The cemeteries of the Villa Pamphilj'),'equites':('A császári lovastestőrség (equites singulares) temetője','The cemetery of the imperial horse guard (equites singulares)'),
 'callisto':('Callistus katakombái','The catacombs of Callixtus'),'domitilla':('Domitilla katakombái','The catacombs of Domitilla'),'priscilla':('Priscilla katakombái','The catacombs of Priscilla'),'pretestato':('Praetextatus katakombái','The catacombs of Praetextatus')}
def build(lang):
    hu=lang=='hu';t=lambda a,b:a if hu else b
    fmt=(lambda n:f'{n:,}'.replace(',',' ')) if hu else (lambda n:f'{n:,}')
    pc=lambda x:(f'{x:.0f}' if x>=10 else (f'{x:.1f}'.replace('.',',') if hu else f'{x:.1f}'))
    R=D['rel'];mx=max(R.values());L=[]
    legs=' · '.join(f'<span class="ik a{k}"></span> <span class="il">{h if hu else e}</span>' for k,h,e in SX)
    legl=' · '.join(f'<span class="ik r{k}"></span> <span class="il">{h if hu else e}</span>' for k,h,e in LN)
    L.append('    <section class="card" id="agecard">')
    L.append('      <h2>'+t('Életkor és család a sírfeliratokon','Age and family in the epitaphs')+'</h2>')
    L.append('      <p class="hint">'+t(f'Az EDR {fmt(D["nt"])} olvasható szövegű római sírfeliratából {fmt(D["ninsc_age"])} közli az elhunyt életkorát (összesen {fmt(D["nage"])} életkor), {fmt(D["nrel"])} pedig megnevezi, kinek állították: házastársnak, gyermeknek, patrónusnak. A sírfelirat azt mutatja, kiről és hogyan emlékeztek meg; halandósági adatként nem használható.',
      f'Of the {fmt(D["nt"])} epitaphs from Rome with a readable text in EDR, {fmt(D["ninsc_age"])} give the age of the deceased ({fmt(D["nage"])} ages in all), and {fmt(D["nrel"])} say for whom the tomb was set up: a spouse, a child, a patron. An epitaph shows who was commemorated and how; it cannot be used as mortality data.')+'</p>')
    L.append('      <h3 class="aqh">'+t('Életkor a sírfeliratokon','Age in the epitaphs')+'</h3>')
    L.append('      <div class="bldchart" id="agechart"></div>')
    L.append('      <p class="hint bldleg" id="ageleg">'+legs+'</p>')
    L.append('      <p class="hint popinfo" id="ageinfo">'+t('Vidd az egeret egy oszlopra.','Hover over a bar.')+'</p>')
    L.append('      <p class="hint">'+t(f'A feliratokon szereplő életkorok középértéke {D["medall"]} év; {pc(100*D["u10"]/D["nage"])}%-a 10 év alatti, és csak {pc(100*D["o60"]/D["nage"])}%-a 60 év fölötti. Egyévesnél fiatalabb csecsemő {fmt(D["u1"])} szerepel. A fiatalon elhunytaknál gyakrabban írták ki az életkort, a csecsemőknek és az időseknek ritkábban állítottak ilyen feliratot; ezért a görbe a megemlékezés szokását mutatja, nem azt, hogy hány évesen haltak meg a rómaiak. Az elhunyt nemét a „qui vixit” vagy „quae vixit”, a „cum quo” vagy „cum qua”, a részes esetű név végződése és a megnevezés (filiae, marito) mutatja meg; ahol ezek a „qui/quae” alapján ellenőrizhetők, 96–99%-ban egyeznek vele. A töredékes számok (például „XX[- - -]”) és a több EDR-számon ismétlődő feliratok másodpéldányai nem számítanak.',
      f'The median of the ages given is {D["medall"]} years; {pc(100*D["u10"]/D["nage"])}% are under 10, and only {pc(100*D["o60"]/D["nage"])}% over 60. Infants under one year appear {fmt(D["u1"])} times. Age was written out more often for those who died young, while infants and the old less often received such an inscription; so the curve shows the habit of commemoration, not the ages at which Romans died. The sex of the deceased is shown by “qui vixit” or “quae vixit”, by “cum quo” or “cum qua”, by the ending of the name in the dative and by the term used (filiae, marito); where these can be checked against “qui/quae”, they agree with it in 96–99% of cases. Fragmentary numerals (for example “XX[- - -]”) and the second copies of inscriptions repeated under several EDR numbers are not counted.')+'</p>')
    L.append('      <h3 class="aqh">'+t('Kerek és pontos életkorok','Rounded and precise ages')+'</h3>')
    L.append('      <p class="hint">'+t(f'A 23 és 62 év közötti életkorok {pc(D["mult5"])}%-a öttel osztható (XXV, XXX, XXXV…); ha mindenki pontosan tudta volna a korát, ez 20% lenne. A demográfiában használt Whipple-index értéke {D["whipple"]} (100: nincs kerekítés, 500: minden életkor kerek). A gyerekek korát viszont gyakran hónapra és napra megadták:',
      f'Of the ages between 23 and 62, {pc(D["mult5"])}% are divisible by five (XXV, XXX, XXXV…); if everyone had known their exact age this would be 20%. The Whipple index used in demography is {D["whipple"]} (100: no rounding, 500: every age rounded). Children’s ages, by contrast, were often given to the month and day:')+'</p>')
    L.append('      <div class="regwrap"><table class="regtab insctab agetab">')
    L.append('        <thead><tr><th>'+t('Életkor','Age')+'</th><th>'+t('Életkor-adat','Ages given')+'</th><th>'+t('Hónap is szerepel','Months also given')+'</th><th>'+t('Nap is szerepel','Days also given')+'</th></tr></thead>')
    L.append('        <tbody>')
    for k,h,e in PR:
        n,m,d=D['prec'][k];L.append(f'          <tr><td>{h if hu else e}</td><td class="pn">{fmt(n)}</td><td class="pn">{pc(100*m/n)}%</td><td class="pn">{pc(100*d/n)}%</td></tr>')
    L.append('        </tbody>')
    L.append('      </table></div>')
    M=D['mar'];Wf=D['wed']['f'];Wm=D['wed']['m']
    L.append('      <h3 class="aqh">'+t('A házasság hossza','Length of marriage')+'</h3>')
    L.append('      <p class="hint">'+t(f'{M["n"]} feliraton áll, hány évig élt együtt a házaspár („cum qua vixit annis XXII”). A középérték {M["q"][1]} év, a feliratok középső fele {M["q"][0]} és {M["q"][2]} év közé esik. Ahol az elhunyt életkora is szerepel, a kettő különbsége a házasságkötéskori életkor: a feleségeknél {Wf[0]} feliratból a középérték {Wf[2]} év ({Wf[1]}–{Wf[3]}), a férjeknél {Wm[0]} feliratból {Wm[2]} év ({Wm[1]}–{Wm[3]}). Ez kevés adat, csak nagyságrendet mutat.',
      f'{M["n"]} inscriptions say how many years the couple lived together (“cum qua vixit annis XXII”). The median is {M["q"][1]} years, and the middle half of the inscriptions falls between {M["q"][0]} and {M["q"][2]} years. Where the age of the deceased is also given, the difference is the age at marriage: for wives the median from {Wf[0]} inscriptions is {Wf[2]} years ({Wf[1]}–{Wf[3]}), for husbands from {Wm[0]} inscriptions {Wm[2]} years ({Wm[1]}–{Wm[3]}). This is a small sample and only shows the order of magnitude.')+'</p>')
    L.append('      <h3 class="aqh">'+t('Kinek állították a sírt?','For whom was the tomb set up?')+'</h3>')
    L.append('      <p class="hint">'+t('A sáv azoknak a feliratoknak a számát mutatja, amelyeken az adott megnevezés részes esetben áll, vagyis az elhunytra vonatkozik („coniugi bene merenti”: jól megérdemelt házastársának). Egy feliraton több is szerepelhet.','The bar shows the number of inscriptions where the term stands in the dative, that is, refers to the deceased (“coniugi bene merenti”: to a well-deserving spouse). One inscription can contain several.')+'</p>')
    L.append('      <div class="foodest agerel">')
    for k,h,e,g in sorted(REL,key=lambda x:-R[x[0]]):
        L.append(f'        <div class="fe"><span class="fen">{h if hu else e}</span><span class="feb"><span class="g{g}" style="width:{100*R[k]/mx:.1f}%"></span></span><span class="fev">{fmt(R[k])}</span></div>')
    L.append('      </div>')
    G=D['grp']
    L.append('      <p class="hint">'+t(f'A kapcsolatot megnevező {fmt(D["nrel"])} felirat {pc(100*G["fam"]/D["nrel"])}%-án szűk családtag áll (házastárs, gyermek, szülő, testvér), {pc(100*G["hh"]/D["nrel"])}%-án a háztartás és a patrónusi viszony szereplői (patrónus, felszabadított, rabszolgatárs, élettárs, nevelt gyermek, dajka), {pc(100*G["amic"]/D["nrel"])}%-án barát. {fmt(D["nself"])} feliraton az állíttató magának is készítette a sírt („sibi et suis”, „se vivo fecit”).',
      f'Of the {fmt(D["nrel"])} inscriptions naming a relationship, {pc(100*G["fam"]/D["nrel"])}% name a member of the immediate family (spouse, child, parent, sibling), {pc(100*G["hh"]/D["nrel"])}% someone from the household or the patronal relationship (patron, freed person, fellow slave, partner, foster-child, nurse), and {pc(100*G["amic"]/D["nrel"])}% a friend. In {fmt(D["nself"])} inscriptions the dedicator made the tomb for himself or herself too (“sibi et suis”, “se vivo fecit”).')+'</p>')
    L.append('      <h3 class="aqh">'+t('Hány évesen haltak meg, akikről megemlékeztek?','At what age did the commemorated die?')+'</h3>')
    L.append('      <div class="regwrap"><table class="regtab insctab agetab">')
    L.append('        <thead><tr><th>'+t('Az elhunyt','The deceased')+'</th><th>'+t('Felirat','Inscriptions')+'</th><th>'+t('Életkor középértéke','Median age')+'</th><th>'+t('A középső fele','Middle half')+'</th></tr></thead>')
    L.append('        <tbody>')
    for k,h,e in RA:
        n,a,b,c=D['relage'][k];L.append(f'          <tr><td>{h if hu else e}</td><td class="pn">{fmt(n)}</td><td class="pn">{b}</td><td class="pn">{a}–{c}</td></tr>')
    L.append('        </tbody>')
    L.append('      </table></div>')
    ra=D['relage']
    L.append('      <p class="hint">'+t(f'Csak azok a feliratok számítanak, amelyeken egyetlen életkor és egyetlen megnevezés áll. A megemlékezett feleségek fiatalabbak voltak, mint a férjek (középérték {ra["wife"][2]} és {ra["husband"][2]} év); a „feleség” és a „férj” ott különíthető el, ahol az elhunyt neme megállapítható.',
      f'Only inscriptions with a single age and a single term are counted. The commemorated wives were younger than the husbands (median {ra["wife"][2]} and {ra["husband"][2]} years); “wife” and “husband” can be told apart where the sex of the deceased can be established.')+'</p>')
    L.append('      <h3 class="aqh">'+t('A megnevezések időben','The terms over time')+'</h3>')
    L.append('      <div class="bldchart agechart2" id="agechart2" data-k="'+','.join(k for k,_,_ in LN)+'"></div>')
    L.append('      <p class="hint bldleg" id="ageleg2">'+legl+'</p>')
    L.append('      <p class="hint popinfo" id="ageinfo2">'+t('Vidd az egeret a görbére; kattintásra a térkép évcsúszkája arra az időre áll.','Hover over the curve; click to set the map’s year slider to that time.')+'</p>')
    L.append('      <p class="hint">'+t('A Kr. u. 1. század közepén a megnevezések aránya hirtelen megnő. A korai kolumbáriumok felirata többnyire csak név a fülke alatt; a „Dis Manibus” kezdetű, az állíttatót és a rokoni viszonyt is megnevező sírfelirat ekkor terjed el. A keltezés itt is részben a szövegformán alapul, ezért az ugrás élessége részben a keltezés módszeréből következik.',
      'In the middle of the 1st century AD the share of these terms rises sharply. The inscriptions of the early columbaria are mostly just a name under the niche; the epitaph beginning “Dis Manibus”, naming the dedicator and the relationship, spreads at this time. Here too the dating is partly based on the form of the text, so the sharpness of the jump partly follows from the dating method.')+'</p>')
    L.append('      <h3 class="aqh">'+t('Lelőhelyek szerint','By findspot')+'</h3>')
    L.append('      <div class="regwrap"><table class="regtab insctab agetab">')
    L.append('        <thead><tr><th>'+t('Lelőhely','Findspot')+'</th><th>'+t('Sírfelirat','Epitaphs')+'</th><th>'+t('Életkor-adat','Ages given')+'</th><th>'+t('Középérték','Median')+'</th><th>'+t('10 év alatti','Under 10')+'</th><th>'+t('Szűk család','Immediate family')+'</th><th>'+t('Háztartás, patrónus','Household, patron')+'</th></tr></thead>')
    L.append('        <tbody>')
    for k,v in sorted(D['cx'].items(),key=lambda x:-x[1]['n']):
        nm=CXN[k][0 if hu else 1];name=f'<a href="#" data-goto="{v["e"]}">{nm}</a>' if v['e'] else nm
        L.append(f'          <tr><td>{name}</td><td class="pn">{fmt(v["n"])}</td><td class="pn">{v["na"]}</td><td class="pn">{v["med"]}</td><td class="pn">{pc(100*v["u10"]/v["na"])}%</td><td class="pn">{pc(100*v["fam"]/v["n"])}%</td><td class="pn">{pc(100*v["hh"]/v["n"])}%</td></tr>')
    L.append('        </tbody>')
    L.append('      </table></div>')
    eq=D['cx']['equites']
    L.append('      <p class="hint">'+t(f'A császári lovastestőrség temetője elüt a többitől: az életkor középértéke {eq["med"]} év, gyerek alig van, és a sírt többnyire nem családtagnak, hanem barátnak nevezett társnak állították (a feliratok {pc(100*eq["rel"][0][1]/eq["n"])}%-án „amico”).',
      f'The cemetery of the imperial horse guard differs from the rest: the median age is {eq["med"]} years, there are hardly any children, and the tomb was mostly set up not for a relative but for a companion called a friend (“amico” in {pc(100*eq["rel"][0][1]/eq["n"])}% of the inscriptions).')+'</p>')
    L.append('    </section>')
    src='      <li><b>'+t('Életkor és család a sírfeliratokon.','Age and family in the epitaphs.')+'</b> '+t('Adat: EDR (lásd „Feliratok”), a sírfeliratként besorolt római feliratok. A kimutatás saját: az életkor a „vixit annis” és az „annorum” utáni római számból, a házasság hossza a „cum quo/qua vixit annis” kifejezésből, a megnevezések a részes esetű rokonsági és háztartási szavakból (age/calc.py). A módszer korlátairól és eredményeiről: K. Hopkins, <i>On the Probable Age Structure of the Roman Population</i>, Population Studies 20 (1966); R. Duncan-Jones, <i>Age-rounding, Illiteracy and Social Differentiation in the Roman Empire</i>, Chiron 7 (1977); R. P. Saller – B. D. Shaw, <i>Tombstones and Roman Family Relations in the Principate</i>, Journal of Roman Studies 74 (1984).',
      'Data: EDR (see “Inscriptions”), the inscriptions from Rome classified as epitaphs. The summary is our own: age from the Roman numeral after “vixit annis” and “annorum”, length of marriage from the phrase “cum quo/qua vixit annis”, the terms from kinship and household words in the dative (age/calc.py). On the limits and results of the method: K. Hopkins, <i>On the Probable Age Structure of the Roman Population</i>, Population Studies 20 (1966); R. Duncan-Jones, <i>Age-rounding, Illiteracy and Social Differentiation in the Roman Empire</i>, Chiron 7 (1977); R. P. Saller – B. D. Shaw, <i>Tombstones and Roman Family Relations in the Principate</i>, Journal of Roman Studies 74 (1984).')+'</li>'
    sub=t(f'{fmt(D["nage"])} életkor, kerekítés, házasság hossza, kinek állították a sírt',f'{fmt(D["nage"])} ages, age-rounding, length of marriage, for whom the tomb was set up')
    return '\n'.join(L)+'\n',src,sub
if __name__=='__main__':
    for l in ('hu','en'):c,s,sub=build(l);print(len(c.split('\n')),sub)
