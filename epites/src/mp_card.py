# v88: „Sírtelkek mérete” és „Katonák Róma sírfeliratain” kártya – közös generátor (hu/en). Adat: plot/data.json, mil/data.json
import json
P=json.load(open('plot/data.json'));M=json.load(open('mil/data.json'))
RN={'appia':'Via Appia','salaria':'Via Salaria','praenestina':'Via Praenestina','labicana':'Via Labicana','latina':'Via Latina','ostiensis':'Via Ostiensis','nomentana':'Via Nomentana','aurelia':'Via Aurelia','portuensis':'Via Portuensis','vaticana':('Vatikán','Vatican'),'tiburtina':'Via Tiburtina','ardeatina':'Via Ardeatina','flaminia':'Via Flaminia','cassia':'Via Cassia'}
UN=[('praet','A testőrség (cohortes praetoriae)','The Praetorian Guard (cohortes praetoriae)',[('castrapraetoria','Castra Praetoria')]),
 ('eqs','A császári lovastestőrség (equites singulares Augusti)','The imperial horse guard (equites singulares Augusti)',[('castrapriora','Castra Priora'),('castranova','Castra Nova')]),
 ('urb','A városi kohorszok (cohortes urbanae)','The urban cohorts (cohortes urbanae)',[]),
 ('cla','A misenumi és a ravennai flotta katonái','Soldiers of the fleets of Misenum and Ravenna',[('misenatium','Castra Misenatium')]),
 ('vig','A tűzoltó-őrség (cohortes vigilum)','The watch (cohortes vigilum)',[]),
 ('fru','A frumentarii és a Castra Peregrina katonái','The frumentarii and the soldiers of the Castra Peregrina',[('castraperegrina','Castra Peregrina')]),
 ('ger','A germán testőrök (corporis custodes)','The German bodyguard (corporis custodes)',[]),
 ('part','A legio II Parthica (az albanói táborból)','Legio II Parthica (from the camp at Albanum)',[])]
LN=[('praet','testőrség','Praetorian Guard'),('eqs','lovastestőrség','horse guard'),('urb','városi kohorszok','urban cohorts'),('cla','flotta','fleets')]
VIGL={4:'statiocohiv',5:'cohortisv',7:'excubitoriumvii'}
ROMN=['','I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII','XIII','XIV']
def build(lang):
    hu=lang=='hu';t=lambda a,b:a if hu else b
    fmt=(lambda n:f'{n:,}'.replace(',',' ')) if hu else (lambda n:f'{n:,}')
    dec=lambda x,d=1:(f'{x:.{d}f}'.replace('.',',') if hu else f'{x:.{d}f}')
    pc=lambda x:(f'{x:.0f}' if x>=10 else dec(x))
    num=lambda x:(str(int(x)) if float(x)==int(x) else dec(x))
    yr=lambda y:(f'Kr. e. {-y}' if y<0 else f'Kr. u. {y}') if hu else (f'{-y} BC' if y<0 else f'AD {y}')
    rn=lambda k:(RN[k] if isinstance(RN[k],str) else RN[k][0 if hu else 1])
    ft=P['ft'];m2=lambda a:a*ft*ft;L=[]
    # ---------- sírtelkek
    L.append('    <section class="card" id="plotcard">')
    L.append('      <h2>'+t('Sírtelkek mérete','The size of tomb plots')+'</h2>')
    L.append('      <p class="hint">'+t(f'A sírkövek gyakran megadják a telek méretét: „in fronte pedes XII, in agro pedes XX”, vagyis 12 láb az út mentén és 20 láb befelé. Az EDR római feliratai közül {fmt(P["n"])} feliraton olvasható mindkét méret ép számmal. Egy római láb 29,6 cm.',
      f'Tombstones often give the size of the plot: “in fronte pedes XII, in agro pedes XX”, that is, 12 feet along the road and 20 feet back from it. Among the inscriptions from Rome in EDR, {fmt(P["n"])} give both measurements with an intact numeral. One Roman foot is 29.6 cm.')+'</p>')
    L.append('      <p class="hint">'+t(f'A leggyakoribb méret a 12 × 12 láb (3,55 × 3,55 m): {P["top"][0][2]} telek, az összes {pc(100*P["top"][0][2]/P["n"])}%-a. Az út menti szélesség a telkek {pc(100*P["f12"]/P["n"])}%-ánál pontosan 12 láb. A telkek területének középértéke {num(P["ar"][1])} négyzetláb ({dec(m2(P["ar"][1]))} m²), a középső fele {num(P["ar"][0])} és {num(P["ar"][2])} négyzetláb közé esik ({dec(m2(P["ar"][0]))}–{dec(m2(P["ar"][2]))} m²). {fmt(P["deeper"])} telek mélyebb, mint amilyen széles, {fmt(P["sq"])} négyzet alakú, {fmt(P["wider"])} szélesebb, mint amilyen mély.',
      f'The most common size is 12 × 12 feet (3.55 × 3.55 m): {P["top"][0][2]} plots, {pc(100*P["top"][0][2]/P["n"])}% of all. The frontage along the road is exactly 12 feet in {pc(100*P["f12"]/P["n"])}% of the plots. The median area is {num(P["ar"][1])} square feet ({dec(m2(P["ar"][1]))} m²), and the middle half falls between {num(P["ar"][0])} and {num(P["ar"][2])} square feet ({dec(m2(P["ar"][0]))}–{dec(m2(P["ar"][2]))} m²). {fmt(P["deeper"])} plots are deeper than they are wide, {fmt(P["sq"])} are square, and {fmt(P["wider"])} are wider than deep.')+'</p>')
    L.append('      <h3 class="aqh">'+t('A telkek területe','Area of the plots')+'</h3>')
    L.append('      <div class="foodest plotbars">')
    mx=max(P['ahist'])
    for (lo,hi),n in zip(P['bands'],P['ahist']):
        lab=(t(f'{lo}–{hi} négyzetláb ({dec(m2(lo))}–{dec(m2(hi))} m²)',f'{lo}–{hi} sq ft ({dec(m2(lo))}–{dec(m2(hi))} m²)') if hi else t(f'{lo} négyzetláb fölött ({dec(m2(lo))} m² fölött)',f'over {lo} sq ft (over {dec(m2(lo))} m²)')) if lo else t(f'{hi} négyzetláb alatt ({dec(m2(hi))} m² alatt)',f'under {hi} sq ft (under {dec(m2(hi))} m²)')
        L.append(f'        <div class="fe"><span class="fen">{lab}</span><span class="feb"><span style="width:{100*n/mx:.1f}%"></span></span><span class="fev">{n}</span></div>')
    L.append('      </div>')
    b=P['big'][0]
    L.append('      <p class="hint">'+t(f'A legkisebb tételek (2 × 2, 3 × 3 láb) valószínűleg nem önálló telkek, hanem egy-egy temetkezési hely méretei. A legnagyobb telek {num(b[0])} × {num(b[1])} láb ({dec(b[0]*ft,0)} × {dec(b[1]*ft,0)} m; {b[2]}, Via Ardeatina).',
      f'The smallest items (2 × 2, 3 × 3 feet) are probably not separate plots but the dimensions of a single burial place. The largest plot is {num(b[0])} × {num(b[1])} feet ({dec(b[0]*ft,0)} × {dec(b[1]*ft,0)} m; {b[2]}, Via Ardeatina).')+'</p>')
    L.append('      <h3 class="aqh">'+t('A leggyakoribb méretek','The most common sizes')+'</h3>')
    L.append('      <div class="regwrap"><table class="regtab insctab numtab">')
    L.append('        <thead><tr><th>'+t('Szélesség × mélység','Frontage × depth')+'</th><th>'+t('Méterben','In metres')+'</th><th>'+t('Felirat','Inscriptions')+'</th></tr></thead>')
    L.append('        <tbody>')
    for f,a,n in P['top']:
        L.append(f'          <tr><td>{num(f)} × {num(a)} {t("láb","feet")}</td><td class="pn">{dec(f*ft)} × {dec(a*ft)} m</td><td class="pn">{n}</td></tr>')
    L.append('        </tbody>')
    L.append('      </table></div>')
    L.append('      <h3 class="aqh">'+t('Utak szerint','By road')+'</h3>')
    L.append('      <div class="regwrap"><table class="regtab insctab numtab">')
    L.append('        <thead><tr><th>'+t('Út','Road')+'</th><th>'+t('Telek','Plots')+'</th><th>'+t('Jellemző méret (láb)','Typical size (feet)')+'</th><th>'+t('Terület középértéke','Median area')+'</th><th>'+t('A középső fele','Middle half')+'</th></tr></thead>')
    L.append('        <tbody>')
    for k,v in sorted(P['roads'].items(),key=lambda x:-x[1]['n']):
        L.append(f'          <tr><td>{rn(k)}</td><td class="pn">{v["n"]}</td><td class="pn">{num(v["f"])} × {num(v["a"])}</td><td class="pn">{num(v["ar"])} ({dec(m2(v["ar"]))} m²)</td><td class="pn">{num(v["q1"])}–{num(v["q3"])}</td></tr>')
    L.append('        </tbody>')
    L.append('      </table></div>')
    L.append('      <p class="hint">'+t('A „jellemző méret” a szélességek és a mélységek középértéke, a terület négyzetlábban értendő. Csak a legalább 15 telket adó utak szerepelnek; az utakhoz a lelőhely-leírás alapján soroltuk a feliratokat, mint a „Feliratok” kártyán.',
      'The “typical size” is the median frontage and the median depth; areas are in square feet. Only roads with at least 15 plots are listed; inscriptions were assigned to roads from the findspot description, as on the “Inscriptions” card.')+'</p>')
    L.append('      <h3 class="aqh">'+t('Korszakok szerint','By period')+'</h3>')
    L.append('      <div class="regwrap"><table class="regtab insctab numtab">')
    L.append('        <thead><tr><th>'+t('Korszak','Period')+'</th><th>'+t('Telek','Plots')+'</th><th>'+t('Jellemző méret (láb)','Typical size (feet)')+'</th><th>'+t('Terület középértéke','Median area')+'</th></tr></thead>')
    L.append('        <tbody>')
    for v in P['per']:
        L.append(f'          <tr><td>{yr(v["lo"])} – {yr(v["hi"])}</td><td class="pn">{v["n"]}</td><td class="pn">{num(v["f"])} × {num(v["a"])}</td><td class="pn">{num(v["ar"])} ({dec(m2(v["ar"]))} m²)</td></tr>')
    L.append('        </tbody>')
    L.append('      </table></div>')
    L.append('      <p class="hint">'+t('A feliratot a keltezése közepe szerint soroltuk korszakba; a 150 évnél tágabban keltezett feliratok kimaradtak. A Kr. u. 1. század végétől a kiírt telkek kisebbek. A töredékes számok és az ismétlődő feliratok másodpéldányai itt sem számítanak.',
      'Each inscription was placed in a period by the midpoint of its dating; inscriptions dated more broadly than 150 years were left out. From the end of the 1st century AD the plots recorded are smaller. Fragmentary numerals and the second copies of repeated inscriptions are not counted here either.')+'</p>')
    L.append('    </section>')
    # ---------- katonák
    C=M['cnt']
    leg=' · '.join(f'<span class="ik u{k}"></span> <span class="il">{h if hu else e}</span>' for k,h,e in LN)
    L.append('    <section class="card" id="milcard">')
    L.append('      <h2>'+t('Katonák Róma sírfeliratain','Soldiers in the epitaphs of Rome')+'</h2>')
    L.append('      <p class="hint">'+t(f'A római sírfeliratok közül {fmt(M["nany"])} nevez meg a városban vagy a közelében állomásozó alakulatot. A táblázat alakulatonként mutatja a feliratok számát, korát, az elhunytak életkorát és szolgálati idejét, és azt, hogy melyik út mentén kerültek elő. A laktanyák nevére kattintva a térkép odaugrik.',
      f'{fmt(M["nany"])} of the epitaphs from Rome name a unit stationed in or near the city. The table shows for each unit the number of inscriptions, their date, the age and length of service of the deceased, and along which road they were found. Click the name of a camp to jump to it on the map.')+'</p>')
    L.append('      <div class="regwrap"><table class="regtab insctab miltab">')
    L.append('        <thead><tr><th>'+t('Alakulat','Unit')+'</th><th>'+t('Felirat','Inscriptions')+'</th><th>'+t('Fő időszak','Main period')+'</th><th>'+t('Életkor','Age')+'</th><th>'+t('Szolgálati évek','Years of service')+'</th><th>'+t('Leggyakoribb lelőhely','Most frequent findspot')+'</th></tr></thead>')
    L.append('        <tbody>')
    for k,h,e,links in sorted(UN,key=lambda x:-C.get(x[0],0)):
        if not C.get(k):continue
        nm=h if hu else e
        sub=''
        if links:sub='<span class="sub">'+', '.join(f'<a href="#" data-goto="{i}">{n}</a>' for i,n in links)+'</span>'
        pr=M['per'][k];per=f'{yr(pr[0])} – {yr(pr[1])}' if pr else '–'
        ag=M['age'][k];sv=M['serv'][k];rd=M['roads'][k]
        ags=f'{ag[2]} <span class="sm">({ag[1]}–{ag[3]}; {ag[0]})</span>' if ag[0]>=10 else '–'
        svs=f'{sv[2]} <span class="sm">({sv[1]}–{sv[3]}; {sv[0]})</span>' if sv[0]>=10 else '–'
        rds=f'{rn(rd["top"][0][0])} <span class="sm">({rd["top"][0][1]} / {rd["n"]})</span>' if rd['n']>=10 else '–'
        L.append(f'          <tr><td>{nm}{sub}</td><td class="pn">{fmt(C[k])}</td><td>{per}</td><td class="pn">{ags}</td><td class="pn">{svs}</td><td>{rds}</td></tr>')
    L.append('        </tbody>')
    L.append('      </table></div>')
    L.append('      <p class="hint">'+t('Az életkornál és a szolgálati éveknél a középérték áll, zárójelben a középső fele és a feliratok száma; a lelőhelynél zárójelben: hány felirat került elő az adott út mentén az úthoz sorolható feliratok közül. Tíznél kevesebb adatnál vonás áll.',
      'For age and years of service the median is given, with the middle half and the number of inscriptions in brackets; for the findspot, in brackets: how many inscriptions were found along that road out of those that can be assigned to a road. A dash stands where there are fewer than ten data points.')+'</p>')
    en=M['enl_all'];pr=M['roads']['praet'];eq=M['roads']['eqs']
    L.append('      <p class="hint">'+t(f'A testőrök sírfeliratai a Castra Praetoria közelében, a Via Salaria és a Via Nomentana mentén sűrűsödnek (az úthoz sorolható {pr["n"]} feliratból {pr["top"][0][1]+pr["top"][1][1]}). A lovastestőrök szinte mind a Via Labicana menti temetőjükből kerültek elő (az úthoz sorolható {eq["n"]} feliratból {eq["top"][0][1]}). Ahol az életkor és a szolgálati idő is szerepel, a kettő különbsége a bevonulás kora: {en[0]} feliratból a középérték {en[2]} év, a középső fele {en[1]} és {en[3]} év közé esik.',
      f'The epitaphs of the Praetorians cluster near the Castra Praetoria, along the Via Salaria and the Via Nomentana ({pr["top"][0][1]+pr["top"][1][1]} of the {pr["n"]} that can be assigned to a road). Almost all those of the horse guard come from their cemetery on the Via Labicana ({eq["top"][0][1]} of {eq["n"]}). Where both age and length of service are given, the difference is the age at enlistment: from {en[0]} inscriptions the median is {en[2]} years, and the middle half falls between {en[1]} and {en[3]} years.')+'</p>')
    L.append('      <h3 class="aqh">'+t('Az alakulatok időben','The units over time')+'</h3>')
    L.append('      <div class="bldchart" id="milchart" data-k="'+','.join(k for k,_,_ in LN)+'"></div>')
    L.append('      <p class="hint bldleg" id="milleg">'+leg+'</p>')
    L.append('      <p class="hint popinfo" id="milinfo">'+t('Vidd az egeret a görbére; kattintásra a térkép évcsúszkája arra az időre áll.','Hover over the curve; click to set the map’s year slider to that time.')+'</p>')
    L.append('      <p class="hint">'+t('A görbe a sírfeliratok számát mutatja 25 éves sávokban, ugyanúgy számolva, mint a „Feliratok” kártyán. A lovastestőrséget a Kr. u. 1. század végén vagy Traianus alatt szervezték meg, és Kr. u. 312-ben Constantinus oszlatta fel a testőrséggel együtt; a görbéje ennek megfelelően a 2–3. századra esik.',
      'The curve shows the number of epitaphs in 25-year bands, counted in the same way as on the “Inscriptions” card. The horse guard was organised at the end of the 1st century AD or under Trajan and disbanded, together with the Praetorian Guard, by Constantine in AD 312; accordingly its curve falls in the 2nd–3rd centuries.')+'</p>')
    L.append('      <h3 class="aqh">'+t('Kohorszok szerint','By cohort')+'</h3>')
    def cohrow(k,lo,hi,links=None):
        d=dict(M['num'][k]);cells=[]
        for i in range(lo,hi+1):
            lab=ROMN[i]
            if links and i in links:lab=f'<a href="#" data-goto="{links[i]}">{lab}</a>'
            cells.append((lab,d.get(i,0)))
        return cells
    for k,ttl,lo,hi,links in (('praet',t('Cohortes praetoriae','Cohortes praetoriae'),1,12,None),('urb',t('Cohortes urbanae','Cohortes urbanae'),10,14,None),('vig',t('Cohortes vigilum','Cohortes vigilum'),1,7,VIGL)):
        cells=cohrow(k,lo,hi,links)
        L.append('      <div class="regwrap"><table class="regtab insctab cohtab">')
        L.append('        <thead><tr><th>'+ttl+'</th>'+''.join(f'<th>{a}</th>' for a,_ in cells)+'</tr></thead>')
        L.append('        <tbody><tr><td>'+t('felirat','inscriptions')+'</td>'+''.join(f'<td class="pn">{n}</td>' for _,n in cells)+'</tr></tbody>')
        L.append('      </table></div>')
    L.append('      <p class="hint">'+t('A XI. és a XII. praetorianus kohorsz csak a Kr. u. 1. században létezett, ezért ritka. A városi kohorszok közül a X., XI., XII. és XIV. állomásozott Rómában. A tűzoltó-őrség hét kohorsza közül három őrhelye szerepel a térképen (a számra kattintva odaugrik); róluk kevés a sírfelirat, a legtöbb adatuk névsorokból ismert.',
      'The 11th and 12th Praetorian cohorts existed only in the 1st century AD, hence their rarity. Of the urban cohorts, the 10th, 11th, 12th and 14th were stationed in Rome. Of the seven cohorts of the watch, the posts of three are on the map (click the number to jump there); few epitaphs survive for them, and most of what is known about them comes from rosters.')+'</p>')
    L.append('      <h3 class="aqh">'+t('Honnan jöttek?','Where did they come from?')+'</h3>')
    L.append('      <div class="regwrap"><table class="regtab insctab miltab">')
    L.append('        <thead><tr><th>'+t('Alakulat','Unit')+'</th><th>'+t('A leggyakoribb népnevek („natione …”)','Most frequent ethnic names (“natione …”)')+'</th></tr></thead>')
    L.append('        <tbody>')
    for k,h,e,_ in UN:
        nt=[x for x in M['nat'][k] if x[1]>=2]
        if len(nt)<2:continue
        L.append(f'          <tr><td>{h if hu else e}</td><td>'+', '.join(f'<i lang="la">{n}</i> ({c})' for n,c in nt)+'</td></tr>')
    L.append('        </tbody>')
    L.append('      </table></div>')
    L.append('      <p class="hint">'+t('A lovastestőröket a dunai és a rajnai határvidék lovascsapataiból válogatták (pannonok, noricumiak, raetusok, batavusok), a korai császárok germán testőrei batavusok és ubiusok voltak, a flotta katonái között egyiptomiak, szárdok és thrák bessusok szerepelnek. A testőrök ritkán írnak népnevet; ők többnyire a szülővárosukat adják meg.',
      'The horse guard was picked from the cavalry units of the Danube and Rhine frontiers (Pannonians, Noricans, Raetians, Batavians); the German bodyguard of the early emperors were Batavians and Ubians; among the fleet soldiers there are Egyptians, Sardinians and Thracian Bessi. Praetorians rarely give an ethnic name; they mostly name their home town.')+'</p>')
    L.append('      <p class="hint">'+t('Korlátok: csak a sírfeliratok számítanak, a fogadalmi feliratok és a névsorok nem. A feliraton megnevezett alakulat az állíttatóé (az örökösé vagy a bajtársé) is lehet. A többi légió nem szerepel, mert a nevük Rómában többnyire tisztek pályafutásának felsorolásában áll.',
      'Limits: only epitaphs are counted, not votive inscriptions or rosters. The unit named in an inscription may be that of the dedicator (the heir or a comrade). Other legions are not included, because in Rome their names mostly occur in lists of officers’ careers.')+'</p>')
    L.append('    </section>')
    src=['      <li><b>'+t('Sírtelkek mérete.','The size of tomb plots.')+'</b> '+t('Adat: EDR (lásd „Feliratok”). A kimutatás saját: az „in fronte pedes … in agro pedes …” és a „quoquoversus pedes …” kifejezések római számai, a töredékes számok nélkül; 1 római láb = 29,6 cm (plot/calc.py).','Data: EDR (see “Inscriptions”). The summary is our own: the Roman numerals in the phrases “in fronte pedes … in agro pedes …” and “quoquoversus pedes …”, without fragmentary numerals; 1 Roman foot = 29.6 cm (plot/calc.py).')+'</li>',
         '      <li><b>'+t('Katonák Róma sírfeliratain.','Soldiers in the epitaphs of Rome.')+'</b> '+t('Adat: EDR (lásd „Feliratok”), a sírfeliratként besorolt római feliratok. A kimutatás saját: az alakulatnevek keresése a szövegben; életkor a „vixit annis”, szolgálati idő a „militavit annis” és a „stipendiorum” utáni számból; származás a „natione” utáni népnévből (mil/calc.py).','Data: EDR (see “Inscriptions”), the inscriptions from Rome classified as epitaphs. The summary is our own: a search for unit names in the text; age from the numeral after “vixit annis”, length of service from that after “militavit annis” and “stipendiorum”; origin from the ethnic name after “natione” (mil/calc.py).')+'</li>']
    subs={t('Sírtelkek mérete','Sírtelkek mérete'):t(f'{fmt(P["n"])} telek mérete lábban és méterben, utak és korszakok szerint',f'the size of {fmt(P["n"])} plots in feet and metres, by road and period'),
          t('Katonák Róma sírfeliratain','Katonák Róma sírfeliratain'):t('testőrség, lovastestőrség, városi kohorszok, flotta: kor, szolgálat, származás, lelőhely','Praetorians, horse guard, urban cohorts, fleets: age, service, origin, findspot')}
    return '\n'.join(L)+'\n',src,subs
if __name__=='__main__':
    for l in ('hu','en'):c,s,sub=build(l);print(len(c.split('\n')),sub)
