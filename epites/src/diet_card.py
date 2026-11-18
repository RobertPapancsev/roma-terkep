# v112: „Mit ettek a rómaiak?” – étrend a csontkollagén szén- és nitrogénizotópjaiból
# De Angelis et al. 2020 (császárkor, Table 2 és 4), Varano et al. 2020 (kora középkor, Table 1 és 3); mindkettő CC BY 4.0
# császárkor: (kód, n, d13C átlag, d15N átlag, medián, min, max)
IMP=[('CM',72,-19.2,10.8,11.1,7.2,12.9),('CBM',26,-19.0,10.8,11.1,8.1,12.2),('CBN',18,-18.9,11.1,11.4,8.4,12.4),
     ('CBQ',19,-19.1,11.0,11.1,8.3,12.6),('PS',27,-19.1,11.4,11.4,10.0,13.2),('QCP',37,-19.3,10.0,9.7,7.7,14.3)]
IN={'CM':('Castel Malnome (délnyugati külváros; a közeli sólepárlókhoz kötik)','Castel Malnome (south-western suburbs; linked to the nearby salt flats)'),
    'CBM':('Casal Bertone, mauzóleum (keleti külváros, az Aurelianus-fal közelében)','Casal Bertone, mausoleum (eastern suburbs, near the Aurelian Wall)'),
    'CBN':('Casal Bertone, nekropolisz','Casal Bertone, necropolis'),
    'CBQ':('Casal Bertone, „Q” terület (az üzem mellett; a halottak 48%-a 0–6 éves)','Casal Bertone, Area Q (next to the workshop; 48% of the dead aged 0–6)'),
    'PS':('Via Padre Semeria (délen, az Aurelianus-fal közelében; gazdálkodó közösség, villa rustica)','Via Padre Semeria (south, near the Aurelian Wall; farming community, villa rustica)'),
    'QCP':('Quarto Cappello del Prete (a Via Praenestinán, Gabii mellett; több mint 70% gyerek és fiatal)','Quarto Cappello del Prete (on the Via Praenestina, near Gabii; over 70% infants and juveniles)')}
# kora középkor: (név hu, név en, kor hu, kor en, n, d13C átlag, d15N átlag, szórás)
MED=[('Piazzale Ostiense','Piazzale Ostiense','4–5. sz.','4th–5th c.',8,-19.4,8.6,0.9),
     ('Amba Aradam','Amba Aradam','5. sz.','5th c.',4,-20.1,8.2,0.8),
     ('San Pancrazio','San Pancrazio','7–8. sz.','7th–8th c.',9,-18.3,11.5,1.4),
     ('Celio I','Celio I','6–9. sz.','6th–9th c.',22,-19.0,8.2,0.9),
     ('Celio II','Celio II','10–11. sz.','10th–11th c.',8,-18.7,8.8,0.9),
     ('Foro della Pace (a Béke temploma helyén)','Foro della Pace (on the site of the Temple of Peace)','10–11. sz.','10th–11th c.',18,-19.2,8.8,0.8),
     ('Gabii, San Primitivo','Gabii, San Primitivo','10–11. sz.','10th–11th c.',32,-19.1,8.6,1.2)]
HERB=(3.8,6.7)   # 9 növényevő (szarvas 2, marha 3, juh 2, kecske 1, nyúl 1), d15N
CI='#1f5fa8';CM_='#c8792b'
def num(x,l):
    s=('%.1f'%abs(x));s=s if l=='en' else s.replace('.',',')
    return ('−' if x<0 else '')+s
def chart(l):
    T=lambda h,e:h if l=='hu' else e
    W=760;L=250;R=20;top=34;rh=26;rows=len(IMP)+len(MED);gap=16;H=top+rows*rh+gap+44
    x=lambda v:L+(v-3)*(W-L-R)/11.0
    o=['      <svg class="dietsvg" viewBox="0 0 %d %d" role="img" aria-label="%s">'%(W,H,T('A δ15N átlaga temetőnként','Mean δ15N by cemetery'))]
    o.append('        <rect x="%.1f" y="%d" width="%.1f" height="%d" fill="#5f8f4e" opacity=".16"/>'%(x(HERB[0]),top-6,x(HERB[1])-x(HERB[0]),rows*rh+gap+6))
    o.append('        <text x="%.1f" y="%d" text-anchor="middle" class="dax">%s</text>'%((x(HERB[0])+x(HERB[1]))/2,top-12,T('növényevő állatok','herbivores')))
    for v in range(3,15,1):
        o.append('        <line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="currentColor" opacity=".12"/>'%(x(v),top-6,x(v),top+rows*rh+gap))
        if v%2==1 or v==14: o.append('        <text x="%.1f" y="%d" text-anchor="middle" class="dax">%d</text>'%(x(v),top+rows*rh+gap+18,v))
    o.append('        <text x="%d" y="%d" text-anchor="end" class="dax">δ15N (‰)</text>'%(W-R,H-4))
    y=top
    for k,n,c,m,md,mn,mx in IMP:
        cy=y+rh/2
        o.append('        <text x="%d" y="%.1f" text-anchor="end" class="dlb">%s</text>'%(L-12,cy+5,IN[k][0 if l=='hu' else 1].split(' (')[0]))
        o.append('        <line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="3" opacity=".35"/>'%(x(mn),cy,x(mx),cy,CI))
        o.append('        <circle cx="%.1f" cy="%.1f" r="6" fill="%s"/>'%(x(m),cy,CI))
        y+=rh
    y+=gap
    o.append('        <line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="currentColor" opacity=".3" stroke-dasharray="4 4"/>'%(8,y-gap/2,W-R,y-gap/2))
    for a,b,_,_,n,c,m,sd in MED:
        cy=y+rh/2
        o.append('        <text x="%d" y="%.1f" text-anchor="end" class="dlb">%s</text>'%(L-12,cy+5,(a if l=='hu' else b).split(' (')[0]))
        o.append('        <line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="3" opacity=".35"/>'%(x(m-sd),cy,x(m+sd),cy,CM_))
        o.append('        <circle cx="%.1f" cy="%.1f" r="6" fill="%s"/>'%(x(m),cy,CM_))
        y+=rh
    o.append('      </svg>')
    return o
def build(l):
    H=l=='hu';T=lambda h,e:h if H else e
    sw=lambda c:'<span class="sw" style="background:%s"></span>'%c
    o=[]
    o.append('    <section class="card" id="dietcard">')
    o.append('      <h2>'+T('Mit ettek a rómaiak? Étrend a csontokból','What did the Romans eat? Diet from the bones')+'</h2>')
    o.append('      <p class="hint">'+T('A csontok kollagénje megőrzi az utolsó évek táplálékának szén- és nitrogénizotópjait. A δ13C azt mutatja, milyen növényekre épült a tápláléklánc (búza, árpa, hüvelyesek: C3; köles: C4) és volt-e benne tengeri eredetű fehérje; a δ15N a táplálékláncban elfoglalt helyet jelzi: minél több hús, tejtermék vagy hal, annál magasabb. Ételeket nem mutat, csak a fehérje forrását.','Bone collagen preserves the carbon and nitrogen isotopes of the food eaten in the last years of life. δ13C shows which plants the food chain was built on (wheat, barley, pulses: C3; millet: C4) and whether marine protein was part of it; δ15N marks the position in the food chain: the more meat, dairy or fish, the higher it is. It does not show dishes, only the source of the protein.')+'</p>')
    o.append('      <h4 class="aqh4">'+T('A δ15N átlaga temetőnként: császárkor és kora középkor','Mean δ15N by cemetery: imperial period and early Middle Ages')+'</h4>')
    o+=chart(l)
    o.append('      <p class="hint aqleg">'+sw(CI)+T(' császárkor (1–3. sz.): átlag, a vonal a legkisebb és legnagyobb mért érték · ',' imperial period (1st–3rd c.): mean, the line spans the lowest and highest measured value · ')+sw(CM_)+T(' kora középkor (4–11. sz.): átlag, a vonal ± 1 szórás · ',' early Middle Ages (4th–11th c.): mean, the line is ± 1 standard deviation · ')+sw('#5f8f4e')+T(' a 9 növényevő állat tartománya (3,8–6,7‰)',' range of the 9 herbivores (3.8–6.7‰)')+'</p>')
    o.append('      <p class="hint srcl"><b>'+T('Forrás:','Source:')+'</b> '+T('De Angelis és társai 2020, Table 2 és 4; Varano és társai 2020, Table 3 (teljes hivatkozás a táblázatok alatt). Az ábra saját szerkesztés a közölt értékekből; a két tanulmány eltérő szóródási mutatót közöl, ezért a vonalak jelentése a két csoportban más.','De Angelis et al. 2020, Tables 2 and 4; Varano et al. 2020, Table 3 (full references under the tables). The chart is my own drawing from the published values; the two studies report different measures of spread, so the lines mean different things in the two groups.')+'</p>')
    o.append('      <h4 class="aqh4">'+T('Császárkor: hat temető, 199 egyén','Imperial period: six cemeteries, 199 individuals')+'</h4>')
    o.append('      <div class="regwrap"><table class="regtab aniotab diettab">')
    o.append('        <thead><tr><th>'+T('Temető','Cemetery')+'</th><th>'+T('Egyén','Indiv.')+'</th><th>δ13C '+T('átlag','mean')+'</th><th>δ15N '+T('átlag','mean')+'</th><th>δ15N '+T('medián','median')+'</th><th>δ15N '+T('tartomány','range')+'</th></tr></thead>')
    o.append('        <tbody>')
    for k,n,c,m,md,mn,mx in IMP:
        o.append('          <tr><td>'+IN[k][0 if H else 1]+'</td><td>%d</td><td>%s</td><td>%s</td><td>%s</td><td>%s–%s</td></tr>'%(n,num(c,l),num(m,l),num(md,l),num(mn,l),num(mx,l)))
    o.append('        </tbody>')
    o.append('      </table></div>')
    o.append('      <p class="hint srcl"><b>'+T('Forrás:','Source:')+'</b> '+T('F. De Angelis, S. Varano, A. Battistini és társai, „Food at the heart of the Empire: dietary reconstruction for Imperial Rome inhabitants”, <i>Archaeological and Anthropological Sciences</i> 12 (2020) 244, doi:10.1007/s12520-020-01194-z (CC BY 4.0), Table 4; értékek ‰-ben. 214 csontmintából 199 felelt meg a kollagén minőségi feltételeinek. A temetők leírása a cikk szövegéből.','F. De Angelis, S. Varano, A. Battistini et al., “Food at the heart of the Empire: dietary reconstruction for Imperial Rome inhabitants”, <i>Archaeological and Anthropological Sciences</i> 12 (2020) 244, doi:10.1007/s12520-020-01194-z (CC BY 4.0), Table 4; values in ‰. Of 214 bone samples 199 met the collagen quality criteria. Cemetery descriptions from the text of the paper.')+'</p>')
    o.append('      <p class="hint">'+T('Viszonyításul a szerzők 17 egykorú állatcsontot is megmértek (Castel Malnome, Via Padre Semeria, a Colosseum környéke): a 9 növényevő (szarvas, marha, juh, kecske, nyúl) δ15N értéke 3,8–6,7‰, a 3 sertésé 4,6–6,8‰, a 3 kutyáé 9,1–10,6‰. Az emberek átlaga mind a hat temetőben 10‰ vagy afölött van, tehát a kutyákéhoz hasonló vagy annál magasabb, és jóval a növényevők fölött.','For comparison the authors also measured 17 contemporary animal bones (Castel Malnome, Via Padre Semeria, the Colosseum area): δ15N is 3.8–6.7‰ for the 9 herbivores (deer, cattle, sheep, goat, hare), 4.6–6.8‰ for the 3 pigs and 9.1–10.6‰ for the 3 dogs. The human mean is 10‰ or above in all six cemeteries, i.e. similar to or higher than the dogs and well above the herbivores.')+'</p>')
    o.append('      <p class="hint">'+T('<b>A szerzők következtetései.</b> Az étrend alapvetően szárazföldi eredetű volt, a növényi alap C3 növény (gabona, hüvelyesek); a C4 növények, például a köles fogyasztása kimutatható, de nem volt általános. Kizárólag tengeri táplálkozásra nincs bizonyíték; alkalmi halfogyasztás viszont nem zárható ki, mert a fehérje akár 20%-a is származhat a tengerből úgy, hogy a kollagén értékein nem látszik. A temetők közötti eltéréseket a szerzők azzal magyarázzák, hogy ki mihez jutott hozzá a lakóhelye környékén. A Gabii melletti Quarto Cappello del Prete átlaga a legalacsonyabb és a szórása a legnagyobb; ott a halottak többsége gyerek volt.','<b>The authors’ conclusions.</b> The diet was basically terrestrial, with C3 plants (cereals, pulses) as the plant base; consumption of C4 plants such as millet is detectable but was not widespread. There is no evidence of an exclusively marine diet; occasional fish eating cannot be ruled out, though, since up to 20% of the protein could come from the sea without showing in the collagen values. The authors explain the differences between cemeteries by what people could get in the neighbourhood where they lived. Quarto Cappello del Prete near Gabii has the lowest mean and the widest spread; most of the dead there were children.')+'</p>')
    o.append('      <h4 class="aqh4">'+T('Kora középkor: hét közösség, 101 egyén','Early Middle Ages: seven communities, 101 individuals')+'</h4>')
    o.append('      <div class="regwrap"><table class="regtab aniotab diettab">')
    o.append('        <thead><tr><th>'+T('Temető','Cemetery')+'</th><th>'+T('Kor','Date')+'</th><th>'+T('Egyén','Indiv.')+'</th><th>δ13C '+T('átlag','mean')+'</th><th>δ15N '+T('átlag','mean')+'</th><th>δ15N '+T('szórás','SD')+'</th></tr></thead>')
    o.append('        <tbody>')
    for a,b,d1,d2,n,c,m,sd in MED:
        o.append('          <tr><td>'+(a if H else b)+'</td><td>'+(d1 if H else d2)+'</td><td>%d</td><td>%s</td><td>%s</td><td>%s</td></tr>'%(n,num(c,l),num(m,l),num(sd,l)))
    o.append('        </tbody>')
    o.append('      </table></div>')
    o.append('      <p class="hint srcl"><b>'+T('Forrás:','Source:')+'</b> '+T('S. Varano, F. De Angelis, A. Battistini és társai, „The edge of the Empire: diet characterization of medieval Rome through stable isotope analysis”, <i>Archaeological and Anthropological Sciences</i> 12 (2020) 196, doi:10.1007/s12520-020-01158-3 (CC BY 4.0), Table 1 és 3; értékek ‰-ben. A 110 mintázott egyénből a 3. táblázat 101-et tartalmaz.','S. Varano, F. De Angelis, A. Battistini et al., “The edge of the Empire: diet characterization of medieval Rome through stable isotope analysis”, <i>Archaeological and Anthropological Sciences</i> 12 (2020) 196, doi:10.1007/s12520-020-01158-3 (CC BY 4.0), Tables 1 and 3; values in ‰. Of the 110 individuals sampled, Table 3 contains 101.')+'</p>')
    o.append('      <p class="hint">'+T('A hét közösségből hatnak az átlaga 8,2–8,8‰, vagyis 1–3‰-kel alacsonyabb, mint a császárkori temetőké (10,0–11,4‰). A szerzők ezt étrendváltásként értelmezik: a birodalom összeomlásával a kereskedelmi rendszer válsága leszűkítette a rómaiak számára elérhető élelmiszerek körét, és kevesebb magas fehérjetartalmú táplálék jutott. Gabiiban ugyanezt látják (császárkor 10,7‰, középkor 8,7‰). Kivétel a San Pancrazio közössége (11,5‰), az egyetlen, ahol vízi eredetű táplálék fogyasztását mutatták ki.','Six of the seven communities have means of 8.2–8.8‰, i.e. 1–3‰ lower than the imperial cemeteries (10.0–11.4‰). The authors read this as a dietary transition: with the collapse of the Empire the crisis of the trade system narrowed the range of foods available to the Romans, and less high-protein food was eaten. They see the same at Gabii (imperial 10.7‰, medieval 8.7‰). The exception is the San Pancrazio community (11.5‰), the only one where consumption of aquatic resources was detected.')+'</p>')
    o.append('      <p class="hint">'+T('<b>Mire figyeljünk.</b> A császárkori temetők a falakon kívül fekszenek, és a szerzők szerint az alsóbb rétegekhez, termelőhelyekhez vagy villagazdaságokhoz kötődnek; a város elitjéről ezek az adatok nem szólnak. A δ15N-t az étrenden kívül más is emelheti (szoptatott csecsemők, éhezés, trágyázott földek), ezért a temetők közti néhány tized ‰ különbség önmagában keveset jelent. A középkori minták egy része kicsi (Amba Aradam 4, Piazzale Ostiense 8 egyén). Az IsoArcH adatbázisból közvetlen letöltés nem sikerült; a két szabadon hozzáférhető tanulmány közölt táblázatait használtam.','<b>Points to bear in mind.</b> The imperial cemeteries lie outside the walls and, according to the authors, belong to the lower classes, tied to production sites or rural villas; these data say nothing about the city’s elite. δ15N can be raised by things other than diet (breastfed infants, starvation, manured fields), so a difference of a few tenths of a ‰ between cemeteries means little by itself. Some medieval samples are small (Amba Aradam 4, Piazzale Ostiense 8 individuals). A direct download from the IsoArcH database did not work; I used the published tables of the two open-access studies.')+'</p>')
    o.append('    </section>')
    return '\n'.join(o)+'\n'
SRCLI=lambda l:('      <li><b>A rómaiak étrendje: szén- és nitrogénizotópok.</b> F. De Angelis és társai: Food at the heart of the Empire: dietary reconstruction for Imperial Rome inhabitants, <i>Archaeological and Anthropological Sciences</i> 12 (2020) 244 (Table 2 és 4); S. Varano és társai: The edge of the Empire: diet characterization of medieval Rome through stable isotope analysis, uo. 12 (2020) 196 (Table 1 és 3). Mindkettő CC BY 4.0. Az ábra saját szerkesztés a közölt átlagokból.</li>' if l=='hu' else '      <li><b>The diet of the Romans: carbon and nitrogen isotopes.</b> F. De Angelis et al., Food at the heart of the Empire: dietary reconstruction for Imperial Rome inhabitants, <i>Archaeological and Anthropological Sciences</i> 12 (2020) 244 (Tables 2 and 4); S. Varano et al., The edge of the Empire: diet characterization of medieval Rome through stable isotope analysis, ibid. 12 (2020) 196 (Tables 1 and 3). Both CC BY 4.0. The chart is my own drawing from the published means.</li>')
SUB=('300 csontváz izotópjai: fehérjeforrások a császárkorban és a kora középkorban','isotopes of 300 skeletons: protein sources in the imperial period and the early Middle Ages')
