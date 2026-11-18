# v113: „Éghajlat az évgyűrűkből” – Büntgen et al. 2011 közép-európai csapadék- és hőmérséklet-rekonstrukciója (NOAA WDC Paleo 2011-026)
import json
D=json.load(open('tree/data.json'));A=D['A'];B=D['B']
CP='#1f5fa8';CT='#c0392b'
BANDS=[('A',235,284),('B',536,550)]
def num(x,l,dec=1,sign=False):
    s=('%.'+str(dec)+'f')%abs(x);s=s if l=='en' else s.replace('.',',')
    return ('−' if x<0 else ('+' if sign and x>0 else ''))+s
def yl(y,l):
    if y==1: return 'Kr. u. 1' if l=='hu' else 'AD 1'
    if y<0: return ('Kr. e. %d' if l=='hu' else '%d BC')%(-y)
    return str(y)
def chart(l,key,mkey,lo,hi,ticks,col,ref,unit,aria):
    W=760;H=250;L=52;R=14;top=14;bot=30
    x=lambda y:L+(y-A)*(W-L-R)/float(B-A);yy=lambda v:top+(hi-v)*(H-top-bot)/float(hi-lo)
    o=['      <svg class="treesvg" viewBox="0 0 %d %d" role="img" aria-label="%s">'%(W,H,aria)]
    for k,a,b in BANDS:
        o.append('        <rect x="%.1f" y="%d" width="%.1f" height="%d" fill="currentColor" opacity=".09"/>'%(x(a),top,x(b)-x(a),H-top-bot))
        o.append('        <text x="%.1f" y="%d" text-anchor="middle" class="tax"><tspan font-weight="700">%s</tspan></text>'%((x(a)+x(b))/2,top+14,k))
    for v in ticks:
        o.append('        <line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="currentColor" opacity=".12"/>'%(L,yy(v),W-R,yy(v)))
        o.append('        <text x="%d" y="%.1f" text-anchor="end" class="tax">%s</text>'%(L-6,yy(v)+5,(num(v,l,0) if unit=='mm' else num(v,l,0,True))))
    o.append('        <line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="currentColor" opacity=".55" stroke-dasharray="5 4"/>'%(L,yy(ref),W-R,yy(ref)))
    for y in (-300,-200,-100,1,100,200,300,400,500,600,700,800):
        o.append('        <line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="currentColor" opacity=".3"/>'%(x(y),H-bot,x(y),H-bot+5))
        if y in (-300,-100,1,200,400,600,800): o.append('        <text x="%.1f" y="%d" text-anchor="%s" class="tax">%s</text>'%(x(y),H-8,'end' if y==800 else 'middle',yl(y,l)))
    pts=' '.join('%.1f,%.1f'%(x(A+i),yy(min(hi,max(lo,v)))) for i,v in enumerate(D[key]) if v is not None)
    o.append('        <polyline points="%s" fill="none" stroke="%s" stroke-width="1" opacity=".33"/>'%(pts,col))
    pts=' '.join('%.1f,%.1f'%(x(A+i),yy(v)) for i,v in enumerate(D[mkey]) if v is not None)
    o.append('        <polyline points="%s" fill="none" stroke="%s" stroke-width="2.6"/>'%(pts,col))
    o.append('      </svg>')
    return o
def build(l):
    H=l=='hu';T=lambda h,e:h if H else e
    sw=lambda c:'<span class="sw" style="background:%s"></span>'%c
    o=[]
    o.append('    <section class="card" id="treecard">')
    o.append('      <h2>'+T('Éghajlat az évgyűrűkből: nyarak az Alpoktól északra','Climate from tree rings: summers north of the Alps')+'</h2>')
    o.append('      <p class="hint">'+T('<b>Ez nem Róma időjárása.</b> A fák évgyűrűinek szélességéből évről évre visszaszámolható a nyár eleji csapadék és a nyári hőmérséklet, de ilyen hosszú, évente felbontott sor Közép-Európából van: 7284 tölgyminta Északkelet-Franciaországból és Németországból (április–júniusi csapadék), valamint 1546 havasi cirbolya- és vörösfenyőminta az osztrák Alpokból és környékéről (június–augusztusi hőmérséklet). A birodalom északnyugati provinciáinak (Gallia, Germania, Raetia) éghajlatáról szól; a Földközi-tenger vidékén a csapadék járása ettől eltérhet.','<b>This is not the weather of Rome.</b> The width of tree rings allows early-summer rainfall and summer temperature to be reconstructed year by year, but a series this long and annually resolved comes from Central Europe: 7284 oak samples from north-eastern France and Germany (April–June precipitation) and 1546 stone pine and larch samples from the Austrian Alps and adjacent areas (June–August temperature). It describes the climate of the Empire’s north-western provinces (Gaul, Germania, Raetia); rainfall patterns around the Mediterranean may differ.')+'</p>')
    o.append('      <h4 class="aqh4">'+T('Április–júniusi csapadék (mm), Kr. e. 398 – Kr. u. 800','April–June precipitation (mm), 398 BC – AD 800')+'</h4>')
    o+=chart(l,'P','Pm',40,340,(50,100,150,200,250,300),CP,D['ref'],'mm',T('Április–júniusi csapadék','April–June precipitation'))
    o.append('      <h4 class="aqh4">'+T('Június–augusztusi hőmérséklet eltérése (°C), Kr. e. 398 – Kr. u. 800','June–August temperature anomaly (°C), 398 BC – AD 800')+'</h4>')
    o+=chart(l,'T','Tm',-3.2,2.4,(-3,-2,-1,0,1,2),CT,0,'c',T('Június–augusztusi hőmérséklet eltérése','June–August temperature anomaly'))
    o.append('      <p class="hint aqleg">'+T('Vékony vonal: évenkénti érték; vastag vonal: 31 éves mozgóátlag (saját számítás). Szaggatott vonal: az 1901–2000-es átlag (csapadék: a rekonstrukció átlaga, '+num(D['ref'],l)+' mm; hőmérséklet: 0 °C eltérés). Sávok: <b>A</b> a 3. századi válság (235–284) · <b>B</b> az 536-os vulkánkitörés utáni évek (536–550).','Thin line: annual value; bold line: 31-year moving average (own calculation). Dashed line: the 1901–2000 mean (precipitation: mean of the reconstruction, '+num(D['ref'],l)+' mm; temperature: 0 °C anomaly). Bands: <b>A</b> the third-century crisis (235–284) · <b>B</b> the years after the eruption of 536 (536–550).')+'</p>')
    SRC=T('U. Büntgen, W. Tegel, K. Nicolussi, M. McCormick és társai, „2500 Years of European Climate Variability and Human Susceptibility”, <i>Science</i> 331 (2011) 578–582; adatsor: NOAA World Data Center for Paleoclimatology, Data Contribution Series 2011-026 (a 4. ábra adatai).','U. Büntgen, W. Tegel, K. Nicolussi, M. McCormick et al., “2500 Years of European Climate Variability and Human Susceptibility”, <i>Science</i> 331 (2011) 578–582; dataset: NOAA World Data Center for Paleoclimatology, Data Contribution Series 2011-026 (data of Fig. 4).')
    o.append('      <p class="hint srcl"><b>'+T('Forrás:','Source:')+'</b> '+SRC+T(' Az ábrák saját szerkesztések. Az adatsorban van 0. év, ezért a Kr. e. évszámok egy évvel elcsúszhatnak.',' The charts are my own drawings. The dataset contains a year 0, so BC dates may be off by one year.')+'</p>')
    o.append('      <h4 class="aqh4">'+T('Évszázadonként','By century')+'</h4>')
    o.append('      <div class="regwrap"><table class="regtab aniotab treetab">')
    o.append('        <thead><tr><th>'+T('Évszázad','Century')+'</th><th>'+T('Csapadék átlaga (mm)','Mean precip. (mm)')+'</th><th>'+T('Száraz év (150 mm alatt)','Dry years (under 150 mm)')+'</th><th>'+T('Nedves év (250 mm fölött)','Wet years (over 250 mm)')+'</th><th>'+T('Hőmérséklet eltérése (°C)','Temp. anomaly (°C)')+'</th></tr></thead>')
    o.append('        <tbody>')
    for c in D['cent']:
        a=c['a'];n=(-a)//100 if a<0 else a//100+1
        nm=(('Kr. e. %d. sz.' if a<0 else 'Kr. u. %d. sz.')%n) if H else (('%s c. BC' if a<0 else '%s c. AD')%({1:'1st',2:'2nd',3:'3rd'}.get(n,'%dth'%n)))
        o.append('          <tr><td>%s</td><td>%s</td><td>%d</td><td>%d</td><td>%s</td></tr>'%(nm,num(c['p'],l,0),c['dry'],c['wet'],num(c['t'],l,1,True)))
    o.append('        </tbody>')
    o.append('      </table></div>')
    o.append('      <p class="hint srcl"><b>'+T('Forrás:','Source:')+'</b> '+T('saját számítás a fenti NOAA-adatsor évenkénti értékeiből. A 150 és 250 mm-es küszöb saját választás a szemléltetéshez, nem a szerzőké. A hőmérséklet az 1901–2000-es időszakhoz viszonyított eltérés.','own calculation from the annual values of the NOAA dataset above. The 150 and 250 mm thresholds are my own choice for illustration, not the authors’. Temperature is the anomaly relative to 1901–2000.')+'</p>')
    o.append('      <p class="hint">'+T('<b>Mit olvasnak ki belőle a szerzők.</b> A késő vaskortól nagyjából Kr. u. 250-ig a nyár eleji csapadék többnyire átlag fölötti volt és szűk határok között ingadozott; a hőmérsékletben két visszaesés látszik, Kr. e. 350 és Kr. e. 50 körül. A 3. században határozott szárazodás következett, egy időben a galliai, germaniai és raetiai provinciák válságával. A 4. században a csapadék nőtt, a nyarak viszont átlag alattiak maradtak; az 5. században a csapadék a kora császárkori szintet is meghaladta, majd a 6. század első felében meredeken visszaesett. Kb. 250 és 550 között a szerzők kivételesen nagy ingadozást látnak. A cikk egybeesésekről beszél, nem bizonyított ok-okozatról.','<b>What the authors read from it.</b> From the Late Iron Age to about AD 250 early-summer rainfall was mostly above average and fluctuated within narrow margins; temperature shows two depressions, around 350 BC and 50 BC. The 3rd century brought distinct drying, at the same time as the crisis of the provinces of Gaul, Germania and Raetia. In the 4th century rainfall increased while summers stayed below average; in the 5th century rainfall even surpassed early imperial levels, then dropped sharply in the first half of the 6th. Between about 250 and 550 the authors see exceptional variability. The paper speaks of coincidences, not of proven cause and effect.')+'</p>')
    d5=D['dry5'];c5=D['cold5']
    o.append('      <p class="hint">'+T('<b>Szélső évek az adatsorban (Kr. e. 300 – Kr. u. 600).</b> A legszárazabb öt nyárelő mind a 6. század közepére esik: 551 ('+num(d5[0][1],l,0)+' mm), 566, 564, 565 és 546. A leghidegebb nyarak: 545 ('+num(c5[0][1],l)+' °C), 549, az adatsor −44. éve ('+num(c5[2][1],l)+' °C), 543 és 562. 537 és 545 között a kilenc nyárból nyolc legalább 2 °C-kal hidegebb a 20. századi átlagnál.','<b>Extreme years in the dataset (300 BC – AD 600).</b> The five driest early summers all fall in the mid-6th century: 551 ('+num(d5[0][1],l,0)+' mm), 566, 564, 565 and 546. The coldest summers: 545 ('+num(c5[0][1],l)+' °C), 549, year −44 of the dataset ('+num(c5[2][1],l)+' °C), 543 and 562. Between 537 and 545, eight summers out of nine are at least 2 °C colder than the 20th-century mean.')+'</p>')
    o.append('      <p class="hint">'+T('<b>Mire figyeljünk.</b> Az egyes évek bizonytalansága nagy: a kalibráció hibája (RMSE) a csapadéknál ± 39 mm, a hőmérsékletnél ± 0,7 °C. A tölgyminták régészeti leletekből, szubfosszilis törzsekből, történeti épületfából és élő fákból származnak, és a számuk korszakonként erősen változik (a szerzők szerint évente átlagosan 286 sor, a római korban a legtöbb, 550, Kr. u. 400 körül a legkevesebb, 44), ezért a hosszú távú szintek kevésbé biztosak, mint az évről évre történő változás. A hajóroncsok és az ólomszennyezés kártyáján a 3. századi mélypont ugyanerre az időre esik, de ebből önmagában nem következik, hogy az éghajlat okozta.','<b>Points to bear in mind.</b> Individual years are very uncertain: the calibration error (RMSE) is ± 39 mm for precipitation and ± 0.7 °C for temperature. The oak samples come from archaeological finds, subfossil trunks, historical timber and living trees, and their number varies strongly by period (according to the authors 286 series per year on average, most in Roman times, 550, fewest around AD 400, 44), so long-term levels are less certain than year-to-year change. On the shipwrecks and lead pollution card the third-century low falls in the same period, but that alone does not show that climate caused it.')+'</p>')
    o.append('    </section>')
    return '\n'.join(o)+'\n'
SRCLI=lambda l:('      <li><b>Éghajlat az évgyűrűkből.</b> U. Büntgen, W. Tegel, K. Nicolussi, M. McCormick és társai: 2500 Years of European Climate Variability and Human Susceptibility, <i>Science</i> 331 (2011) 578–582; adatsor: NOAA World Data Center for Paleoclimatology, Data Contribution Series 2011-026. Az évszázados átlagok, a mozgóátlag és az ábrák saját számítások.</li>' if l=='hu' else '      <li><b>Climate from tree rings.</b> U. Büntgen, W. Tegel, K. Nicolussi, M. McCormick et al., 2500 Years of European Climate Variability and Human Susceptibility, <i>Science</i> 331 (2011) 578–582; dataset: NOAA World Data Center for Paleoclimatology, Data Contribution Series 2011-026. Century means, moving average and charts are own calculations.</li>')
SUB=('közép-európai csapadék és nyári hőmérséklet évről évre, Kr. e. 398 – Kr. u. 800','Central European rainfall and summer temperature year by year, 398 BC – AD 800')
