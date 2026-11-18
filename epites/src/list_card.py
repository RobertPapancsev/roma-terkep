# v90: „Róma a birodalom feliratai között” kártya – közös generátor (hu/en). Adat: list/calc.py, list/stats.py, list/fin.py -> list/data.json
import json
D=json.load(open('list/data.json'));B=D['bins'];W=D['w'];T=D['time'];R=D['reg']
RN={'roma':('Róma','Rome'),'italia':('Itália (Róma nélkül)','Italy (without Rome)'),'insulae':('Szicília, Szardínia, Korzika','Sicily, Sardinia, Corsica'),'africa':('Észak-Afrika','North Africa'),'hispania':('Hispania','Hispania'),
 'gallia':('Gallia és Germania','Gaul and the Germanies'),'britannia':('Britannia','Britain'),'danuvius':('Duna-vidék és Balkán','Danube provinces and the Balkans'),'oriens':('Görög Kelet (latin feliratok)','Greek East (Latin inscriptions)')}
TL=[('roma','Róma','Rome'),('italia','Itália (Róma nélkül)','Italy (without Rome)'),('prov','provinciák','provinces')]
def build(lang):
    hu=lang=='hu';t=lambda a,b:a if hu else b
    fmt=(lambda n:f'{n:,}'.replace(',',' ')) if hu else (lambda n:f'{n:,}')
    d1=lambda x:(f'{x:.1f}'.replace('.',',') if hu else f'{x:.1f}')
    pc=lambda x:(f'{x:.0f}' if x>=10 else d1(x))
    yr=lambda y:((f'Kr. e. {-y}' if y<0 else f'Kr. u. {y}') if hu else (f'{-y} BC' if y<0 else f'AD {y}'))
    ro=R['roma'];n=D['n'];O=D['ord'];A=lambda k:R[k]['age'];F=lambda k:R[k]['f'];E=D['edr']
    stone=sum(R[k]['stone'] for k in O);instr=sum(R[k]['instr'] for k in O);dt=D['dated']
    L=[]
    L.append('    <section class="card" id="listcard">')
    L.append('      <h2>'+t('Róma a birodalom feliratai között','Rome among the inscriptions of the empire')+'</h2>')
    L.append('      <p class="hint">'+t(f'A LIST (Latin Inscriptions in Space and Time) adatállomány a Római Birodalom latin feliratait egyesíti két nagy adatbázisból (EDCS és EDH): {fmt(n)} felirat, ebből {fmt(ro["n"])} Rómából, vagyis a birodalom ismert latin feliratainak {pc(100*ro["n"]/n)}%-a egyetlen városból származik. Ez a kártya Rómát a birodalom többi részével veti össze. Minden mutatót a feliratok szövegéből, mindenütt ugyanazzal a szabállyal számoltunk, nem az adatbázis kulcsszavaiból.',
      f'The LIST data set (Latin Inscriptions in Space and Time) merges the Latin inscriptions of the Roman Empire from two large databases (EDCS and EDH): {fmt(n)} inscriptions, {fmt(ro["n"])} of them from Rome, so {pc(100*ro["n"]/n)}% of the known Latin inscriptions of the empire come from a single city. This card compares Rome with the rest of the empire. Every figure was computed from the texts of the inscriptions, with the same rule everywhere, not from the keywords of the database.')+'</p>')
    L.append('      <p class="hint">'+t(f'A bélyegzett téglák, amforák és más használati tárgyak feliratai ({fmt(instr)}) és a 15 betűnél rövidebb töredékek kimaradnak; így {fmt(stone)} hosszabb szövegű felirat marad, ebből {fmt(ro["stone"])} római ({pc(100*ro["stone"]/stone)}%).',
      f'Stamps on bricks, amphorae and other everyday objects ({fmt(instr)}) and fragments shorter than 15 letters are left out; this leaves {fmt(stone)} inscriptions with a longer text, {fmt(ro["stone"])} of them from Rome ({pc(100*ro["stone"]/stone)}%).')+'</p>')
    L.append('      <h3 class="aqh">'+t('A legtöbb feliratot adó városok','The cities with the most inscriptions')+'</h3>')
    cmx=D['cities'][1]['stone']
    L.append('      <div class="foodest listbars">')
    for c in D['cities']:
        w=min(100,100*c['stone']/cmx);cl='lct lcr' if c['c']=='Roma' else 'lct'
        L.append(f'        <div class="fe"><span class="fen"><i lang="la">{c["c"]}</i></span><span class="feb"><span class="{cl}" style="width:{w:.1f}%"></span></span><span class="fev">{fmt(c["stone"])}</span></div>')
    L.append('      </div>')
    L.append('      <p class="hint">'+t(f'Hosszabb szövegű feliratok az ókori város 5 kilométeres körzetében (a LIST besorolása). Róma sávja nem fér a skálára: {round(D["cities"][0]["stone"]/cmx)}-szer annyi feliratot adott, mint a második helyen álló kikötővárosa, Ostia.',
      f'Inscriptions with a longer text within 5 kilometres of the ancient city (as assigned by LIST). The bar of Rome does not fit the scale: it produced {round(D["cities"][0]["stone"]/cmx)} times as many inscriptions as its port, Ostia, in second place.')+'</p>')
    # időgörbe: statikus SVG
    L.append('      <h3 class="aqh">'+t('Mikor állították a feliratokat','When the inscriptions were set up')+'</h3>')
    Wd,H,Lm,Rm,Tp,Bt=660,250,46,10,8,26;mx=max(max(T[k]) for k,_,_ in TL)*1.06;X0,X1=B[0],B[-1]+W
    xs=lambda x:Lm+(x-X0)/(X1-X0)*(Wd-Lm-Rm);sy=lambda v:Tp+(1-v/mx)*(H-Tp-Bt)
    sv=[f'      <div class="bldchart listchart"><svg viewBox="0 0 {Wd} {H}" class="bldsvg listsvg" role="img">']
    for v in range(0,int(mx)+1,2000):
        sv.append(f'<line x1="{Lm}" x2="{Wd-Rm}" y1="{sy(v):.1f}" y2="{sy(v):.1f}" class="pg"/><text x="{Lm-5}" y="{sy(v)+4:.1f}" text-anchor="end" class="pt">{fmt(v)}</text>')
    for x in (-100,0,100,200,300,400,500,600):
        lab=(yr(x) if x in(-100,100) else (('1' if x==0 else str(x))))
        sv.append(f'<text x="{xs(x):.1f}" y="{H-Bt+16}" text-anchor="{"start" if x==-100 else "end" if x==600 else "middle"}" class="pt">{lab}</text>')
    sv.append(f'<line x1="{Lm}" x2="{Wd-Rm}" y1="{H-Bt}" y2="{H-Bt}" class="pax"/>')
    for k,_,_ in TL:
        sv.append('<path class="listl l'+k+'" d="'+''.join(('L' if i else 'M')+f'{xs(B[i]+W/2):.1f},{sy(v):.1f}' for i,v in enumerate(T[k]))+'"/>')
    sv.append('</svg></div>')
    L.append(''.join(sv))
    L.append('      <p class="hint bldleg">'+' · '.join(f'<span class="ik l{k}"></span> <span class="il">{h if hu else e}</span>' for k,h,e in TL)+'</p>')
    pk=lambda k:B[max(range(len(B)),key=lambda i:T[k][i] if B[i]<250 else -1)]
    sh=lambda lo,hi:100*sum(T['roma'][i] for i,x in enumerate(B) if lo<=x<hi)/sum(T['roma'][i]+T['italia'][i]+T['prov'][i] for i,x in enumerate(B) if lo<=x<hi)
    L.append('      <p class="hint">'+t(f'Keltezett, hosszabb szövegű feliratok száma 50 évenként; a tág keltezésű felirat arányosan oszlik meg az évtizedek között. Rómában a feliratállítás már az 1. század első felében tetőzik, a provinciákban csak a 2. század második felében. A 3. század közepén mindenütt visszaesik. A 4. században Róma görbéje újra megugrik: ezek a katakombák keresztény sírfeliratai, és ekkor a birodalom keltezett feliratainak {pc(sh(300,400))}%-a római (az 1. században {pc(sh(0,100))}%-a).',
      f'Number of dated inscriptions with a longer text per 50 years; an inscription with a broad date is spread proportionally over the decades. In Rome the setting up of inscriptions already peaks in the first half of the 1st century, in the provinces only in the second half of the 2nd. In the mid-3rd century it falls everywhere. In the 4th century the curve of Rome rises again: these are the Christian epitaphs of the catacombs, and at that time {pc(sh(300,400))}% of the dated inscriptions of the empire are from Rome ({pc(sh(0,100))}% in the 1st century).')+'</p>')
    L.append('      <p class="hint">'+t(f'A görbe óvatosan olvasandó. Rómában a hosszabb feliratok {pc(100*dt["roma_dated"]/dt["roma_all"])}%-a keltezett, a provinciákban {pc(100*dt["prov_dated"]/dt["prov_all"])}%-a, és a keltezés gyakran csak egy-két évszázadnyi sáv; sok római keresztény felirat egységesen a „301–500” keltezést kapta.',
      f'The curve should be read with caution. In Rome {pc(100*dt["roma_dated"]/dt["roma_all"])}% of the longer inscriptions are dated, in the provinces {pc(100*dt["prov_dated"]/dt["prov_all"])}%, and the date is often only a band of one or two centuries; many Christian inscriptions of Rome were uniformly given the date “301–500”.')+'</p>')
    L.append('      <h3 class="aqh">'+t('Sírfeliratok: formulák és társadalmi helyzet','Epitaphs: formulae and social status')+'</h3>')
    L.append('      <div class="regwrap"><table class="regtab insctab agetab listtab">')
    L.append('        <thead><tr><th>'+t('Terület','Region')+'</th><th>'+t('Sírfelirat','Epitaphs')+'</th><th><i lang="la">Dis Manibus</i></th><th><i lang="la">bene merenti</i></th><th><i lang="la">hic situs est</i></th><th><i lang="la">sit tibi terra levis</i></th><th>'+t('felszabadított','freed')+'</th><th>'+t('rabszolga','slave')+'</th><th>'+t('katona','soldier')+'</th></tr></thead>')
    L.append('        <tbody>')
    for k in O:
        f=F(k);L.append(f'          <tr><td>{RN[k][0 if hu else 1]}</td><td class="pn">{fmt(R[k]["pe"])}</td>'+''.join(f'<td class="pn">{pc(f[x])}%</td>' for x in('dm','bm','hse','sttl','lib','ser','mil'))+'</tr>')
    L.append('        </tbody>')
    L.append('      </table></div>')
    L.append('      <p class="hint">'+t(f'A nem keresztény sírfeliratok hány százalékán áll az adott formula vagy megnevezés. A formulák tájanként mások: a „bene merenti” (jól megérdemelten) Róma és Itália szokása (Rómában {pc(F("roma")["bm"])}%, Észak-Afrikában {pc(F("africa")["bm"])}%), a „hic situs est” (itt nyugszik) Hispaniáé és Afrikáé ({pc(F("hispania")["hse"])}% és {pc(F("africa")["hse"])}%, Rómában {pc(F("roma")["hse"])}%), a „sit tibi terra levis” (legyen neked könnyű a föld) szinte csak Hispaniában él ({pc(F("hispania")["sttl"])}%).',
      f'The percentage of non-Christian epitaphs carrying the given formula or term. The formulae differ by region: “bene merenti” (well deserving) is the habit of Rome and Italy ({pc(F("roma")["bm"])}% in Rome, {pc(F("africa")["bm"])}% in North Africa), “hic situs est” (here lies) that of Hispania and Africa ({pc(F("hispania")["hse"])}% and {pc(F("africa")["hse"])}%; {pc(F("roma")["hse"])}% in Rome), and “sit tibi terra levis” (may the earth lie light on you) lives almost only in Hispania ({pc(F("hispania")["sttl"])}%).')+'</p>')
    L.append('      <p class="hint">'+t(f'Felszabadítottat (libertus, liberta) Rómában a sírfeliratok {pc(F("roma")["lib"])}%-a nevez meg, Itáliában {pc(F("italia")["lib"])}%-a, Észak-Afrikában {pc(F("africa")["lib"])}%-a: a felszabadítottak sírfelirata a főváros és Itália sajátossága. A katonák aránya fordított: Britanniában {pc(F("britannia")["mil"])}%, a Duna-vidéken {pc(F("danuvius")["mil"])}%, Rómában {pc(F("roma")["mil"])}%. A „katona” oszlop minden olyan sírfeliratot számol, amely katonát, veteránt vagy alakulatot említ; a „rabszolga” a servus, serva és verna szót.',
      f'A freed person (libertus, liberta) is named in {pc(F("roma")["lib"])}% of the epitaphs of Rome, {pc(F("italia")["lib"])}% in Italy and {pc(F("africa")["lib"])}% in North Africa: the epitaph of the freed is a feature of the capital and of Italy. With soldiers it is the reverse: {pc(F("britannia")["mil"])}% in Britain, {pc(F("danuvius")["mil"])}% in the Danube provinces, {pc(F("roma")["mil"])}% in Rome. The “soldier” column counts every epitaph that mentions a soldier, a veteran or a unit; “slave” counts the words servus, serva and verna.')+'</p>')
    L.append('      <h3 class="aqh">'+t('Életkor a sírfeliratokon','Age in the epitaphs')+'</h3>')
    L.append('      <div class="regwrap"><table class="regtab insctab agetab listtab">')
    L.append('        <thead><tr><th>'+t('Terület','Region')+'</th><th>'+t('Életkor-adat','Ages given')+'</th><th>'+t('Középérték','Median')+'</th><th>'+t('10 év alatti','Under 10')+'</th><th>'+t('60 év fölötti','Over 60')+'</th><th>'+t('Whipple-index','Whipple index')+'</th></tr></thead>')
    L.append('        <tbody>')
    for k in O:
        a=A(k);L.append(f'          <tr><td>{RN[k][0 if hu else 1]}</td><td class="pn">{fmt(a["n"])}</td><td class="pn">'+t(f'{a["med"]} év',f'{a["med"]} years')+f'</td><td class="pn">{pc(a["u10"])}%</td><td class="pn">{pc(a["o60"])}%</td><td class="pn">{a["whipple"]}</td></tr>')
    L.append('        </tbody>')
    L.append('      </table></div>')
    L.append('      <p class="hint">'+t(f'Rómában a sírfeliraton megörökített életkorok középértéke {A("roma")["med"]} év, és {pc(A("roma")["u10"])}%-uk tíz év alatti gyermeké; Észak-Afrikában a középérték {A("africa")["med"]} év, és az életkorok {pc(A("africa")["o60"])}%-a hatvan év fölötti. Ez nem a halandóság különbsége, hanem a szokásé: Rómában főleg a fiatalon elhunytak életkorát vésték kőbe, Afrikában az öregekét is, és gyakrabban kerekítve. A Whipple-index a kerek (5-re és 0-ra végződő) életkorok torlódását méri: 100, ha nincs kerekítés, 500, ha minden életkor kerek.',
      f'In Rome the median of the ages recorded in epitaphs is {A("roma")["med"]} years, and {pc(A("roma")["u10"])}% of them belong to children under ten; in North Africa the median is {A("africa")["med"]} years and {pc(A("africa")["o60"])}% of the ages are over sixty. This is a difference not of mortality but of custom: in Rome it was mainly the ages of those who died young that were carved in stone, in Africa those of the old as well, and more often rounded. The Whipple index measures the heaping of round ages (ending in 5 or 0): 100 if there is no rounding, 500 if every age is round.')+'</p>')
    L.append('      <p class="hint">'+t(f'Ellenőrzés két független adatbázissal: a római sírfeliratokra itt (EDCS-szövegekből, a keresztény feliratokkal együtt) {A("roma")["med"]} év középértéket, {pc(A("roma")["u10"])}% tíz év alattit és {pc(A("roma")["o60"])}% hatvan év fölöttit kaptunk; az „Életkor és család a sírfeliratokon” kártya az EDR szövegeiből {E["medall"]} évet, {pc(100*E["u10"]/E["nage"])}%-ot és {pc(100*E["o60"]/E["nage"])}%-ot ad. Az életkorhoz itt az „annorum XXX” alakot is számoltuk, mert a provinciákban ez a gyakoribb; a csonka számok, a házasság és a katonai szolgálat hossza nem életkor. Azonos szövegű, legalább 40 betűs feliratot provinciánként csak egyszer számoltunk.',
      f'A check with two independent databases: for the epitaphs of Rome we obtained here (from EDCS texts, Christian inscriptions included) a median of {A("roma")["med"]} years, {pc(A("roma")["u10"])}% under ten and {pc(A("roma")["o60"])}% over sixty; the card “Age and family in the epitaphs” gives {E["medall"]} years, {pc(100*E["u10"]/E["nage"])}% and {pc(100*E["o60"]/E["nage"])}% from the texts of EDR. For age we also counted the form “annorum XXX” here, because it is the more common one in the provinces; truncated numerals and lengths of marriage or military service are not ages. An inscription with an identical text of at least 40 letters was counted only once per province.')+'</p>')
    L.append('    </section>')
    src='      <li><b>'+t('Róma a birodalom feliratai között.','Rome among the inscriptions of the empire.')+'</b> '+t('V. Kaše, P. Heřmánková, A. Sobotková: <i>LIST – Latin Inscriptions in Space and Time</i>, v1.2, Zenodo 2024, <a href="https://doi.org/10.5281/zenodo.10473706">10.5281/zenodo.10473706</a> (CC BY 4.0); forrásai az Epigraphik-Datenbank Clauss/Slaby (EDCS) és az Epigraphic Database Heidelberg (EDH). A városok besorolása a LIST-ből (J. W. Hanson városlistája alapján). Az összesítés saját: a szövegek tisztítása, a formulák, a jogállás, a katonák és az életkor a feliratok szövegéből (list/calc.py, list/stats.py, list/fin.py).',
      'V. Kaše, P. Heřmánková, A. Sobotková: <i>LIST – Latin Inscriptions in Space and Time</i>, v1.2, Zenodo 2024, <a href="https://doi.org/10.5281/zenodo.10473706">10.5281/zenodo.10473706</a> (CC BY 4.0); its sources are the Epigraphik-Datenbank Clauss/Slaby (EDCS) and the Epigraphic Database Heidelberg (EDH). The assignment to cities is from LIST (based on J. W. Hanson’s list of cities). The summary is our own: text cleaning, formulae, legal status, soldiers and age from the texts of the inscriptions (list/calc.py, list/stats.py, list/fin.py).')+'</li>'
    sub=t(f'Róma és a provinciák: {fmt(n)} latin felirat, formulák, felszabadítottak, katonák, életkor',f'Rome and the provinces: {fmt(n)} Latin inscriptions, formulae, the freed, soldiers, age')
    return '\n'.join(L)+'\n',src,sub
if __name__=='__main__':
    import re
    for l in ('hu','en'):
        c,s,sub=build(l);print(len(c.split('\n')),sub)
    print(re.sub(r'<[^>]+>','',' '.join(x for x in build('hu')[0].split('\n') if 'class="hint"' in x)))
