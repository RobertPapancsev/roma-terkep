import json
M=json.load(open('en/missing.json'))
def row(i,a,b,c,d):return f'          <tr data-p="{i}"><td>{a}</td><td class="pn">{b}</td><td>{c}</td><td>{d}</td></tr>'
ER={"beard":("c. 510 BC, end of the monarchy","20,000–30,000","M. Beard 2015",""),
"hop09":("225 BC","c. 150,000","K. Hopkins 2009",""),
"man1":("c. 225 BC","c. 200,000","M. J. Mandich 2016","“urban scaling”: from the relation between a city’s population and its size observed in other cities"),
"sch":("28 BC","800,000–1,000,000","W. Scheidel 2007",""),
"hop78":("late 1st century BC","800,000–1,000,000","K. Hopkins 1978",""),
"brunt":("Age of Augustus","c. 750,000","P. A. Brunt 1971",""),
"mor":("Age of Augustus","c. 1,000,000","N. Morley 1996",""),
"man2":("2 BC","c. 1,000,000 (low scenario: 750,000)","M. J. Mandich 2016",""),
"sto":("Imperial period","c. 450,000","G. R. Storey 1997","from density: projects onto Rome the density of the excavated blocks of Pompeii and Ostia"),
"sal1":("early 4th century","700,000–1,000,000","M. R. Salzman 2021",""),
"lan1":("4th century","700,000–900,000","B. Lançon 2000",""),
"kra1":("c. 400","c. 800,000","R. Krautheimer 1980",""),
"lan2":("408, before the Gothic sieges","c. 800,000","B. Lançon 2000",""),
"lan3":("419","c. 500,000","B. Lançon 2000",""),
"rus":("c. 419","c. 58,000","J. C. Russell 1958","far from all other estimates"),
"dur1":("5th century","c. 350,000","J. Durliat 1990",""),
"kra2":("452","c. 500,000","R. Krautheimer 1980",""),
"sal2":("mid-5th century","300,000–500,000","M. R. Salzman 2021",""),
"kra3":("c. 500","c. 100,000","R. Krautheimer 1980",""),
"dur2":("6th century","c. 60,000","J. Durliat 1990",""),
"kra4":("after 552","c. 30,000","R. Krautheimer 1980",""),
"suet":("46 BC","320,000 → 150,000","recipients of free grain before and after Caesar’s review","Suetonius, <i>Divus Iulius</i> 41.3"),
"rg1":("12 BC","at least 250,000","citizens who received Augustus’s cash gift (<i>congiarium</i>)","<i>Res gestae</i> 15"),
"rg2":("5 BC","320,000","the urban plebs, who received Augustus’s cash gift","<i>Res gestae</i> 15"),
"rg3":("2 BC","a little over 200,000","citizens receiving public grain","<i>Res gestae</i> 15"),
"dio":("AD 202","c. 200,000","grain recipients and praetorians together: Septimius Severus gave 10 aurei each, 50 million denarii in all, from which the head count follows","Cassius Dio 76(77).1"),
"jon":("mid-5th century","c. 120,000","recipients of free bread and pork, mostly heads of families","A. H. M. Jones 1966"),
"pro1":("546","no more than 500","the number of people left in the city when Totila entered","Procopius, <i>Gothic War</i> (<i>Wars</i> 7.20.19)"),
"pro2":("547","0","when Totila withdrew, the city was left empty of people","Procopius, <i>Wars</i> 7.22.19")}
E={}
for u in M:
    t=u['t']
    if '<tr data-p="' in t:
        i=t.split('data-p="')[1].split('"')[0];E[u['id']]=row(i,*ER[i]);continue
O={
'      <h2>Róma népessége</h2>':'      <h2>The population of Rome</h2>',
'      <h3 class="aqh">Modern becslések</h3>':'      <h3 class="aqh">Modern estimates</h3>',
'      <h3 class="aqh">Ókori számadatok</h3>':'      <h3 class="aqh">Ancient figures</h3>',
'      <h3 class="aqh">Miért térnek el a becslések?</h3>':'      <h3 class="aqh">Why do the estimates differ?</h3>',
'        <thead><tr><th>Időpont</th><th>Becslés (lakos)</th><th>Kutató</th><th>Megjegyzés</th></tr></thead>':'        <thead><tr><th>Date</th><th>Estimate (inhabitants)</th><th>Scholar</th><th>Note</th></tr></thead>',
'        <thead><tr><th>Időpont</th><th>Szám</th><th>Kiket számol</th><th>Forrás</th></tr></thead>':'        <thead><tr><th>Date</th><th>Figure</th><th>Who is counted</th><th>Source</th></tr></thead>',
'      <p class="hint popinfo" id="popinfo">Vidd az egeret egy jelre, vagy kattints egy táblázatsorra.</p>':'      <p class="hint popinfo" id="popinfo">Hover over a marker or click a table row.</p>',
'      <div class="seg popsel" role="group" aria-label="Skála"><button data-s="lin" aria-pressed="true">Lineáris skála</button><button data-s="log" aria-pressed="false">Logaritmikus skála</button></div>':'      <div class="seg popsel" role="group" aria-label="Scale"><button data-s="lin" aria-pressed="true">Linear scale</button><button data-s="log" aria-pressed="false">Logarithmic scale</button></div>',
}
P={
'u03991':'      <p class="hint">No census figure for the population of Rome survives. Ancient sources count only certain groups, mainly the adult male citizens entitled to free grain or cash gifts. Modern scholars estimate the total population from these and other indirect evidence, so the figures below are estimates, not data. Even for the same period they differ by as much as a factor of two.</p>',
'u03993':'      <p class="hint popleg"><span class="pk e"></span> modern estimate (dot: a single figure, vertical bar: a range) · <span class="pk a"></span> ancient figure for one group, not the whole population · <span class="pk y"></span> the year set on the map’s year slider</p>',
'u03995':'      <p class="hint">The points are deliberately not joined by a line: there are no data for the years between the estimates, and a curve would invent them. The two largest uncertainties: how large the city was in the middle Republic, and how fast it shrank in the 5th–6th centuries.</p>',
'u04030':'      <p class="hint"><b>The grain-dole multiplier.</b> The number of recipients (c. 200,000 under Augustus) counts only adult male citizens. For the total population one must add women, children, slaves, non-citizen foreigners, soldiers and the elite. There is no ancient figure for their share, so the choice of multiplier alone produces differences of hundreds of thousands. This is the route to the often-quoted figure of about one million.</p>',
'u04031':'      <p class="hint"><b>Density.</b> According to Storey (1997), one million inhabitants on the 13.86 km² of the ancient city would mean 72,150 people per square kilometre, similar to the densest parts of modern Hong Kong. The density of the excavated blocks of Pompeii and Ostia gives a much smaller population, about 450,000.</p>',
'u04032':'      <p class="hint"><b>The number of buildings.</b> The 4th-century regionary catalogue lists 46,602 apartment blocks (<i>insulae</i>) and 1,790 houses (<i>domus</i>) (see “The 14 regions in numbers”). If <i>insula</i> means a whole building, this points to a large population; if only a flat or a plot unit, a much smaller one. The meaning of the word is disputed, so no population can be calculated from the figure.</p>',
'u04033':'      <p class="hint"><b>Late antiquity.</b> The spread between estimates is largest for the sieges of the 5th century (410, 455, 472) and the Gothic War of the 6th: scholars interpret the same few pieces of evidence (the recipients of the meat and bread distribution, Procopius’s account) in different ways.</p>',
'u04112':'      <li><b>The population of Rome.</b> Modern estimates: M. Beard, <i>SPQR: A History of Ancient Rome</i>, London 2015; K. Hopkins, “The political economy of the Roman empire”, in: I. Morris – W. Scheidel (eds), <i>The Dynamics of Ancient Empires</i>, Oxford 2009; M. J. Mandich, “Urban Scaling and the Growth of Rome”, <i>TRAC 2015</i> (2016); W. Scheidel, “Demography”, in: <i>The Cambridge Economic History of the Greco-Roman World</i>, Cambridge 2007; K. Hopkins, <i>Conquerors and Slaves</i>, Cambridge 1978; P. A. Brunt, <i>Italian Manpower 225 B.C.–A.D. 14</i>, Oxford 1971; N. Morley, <i>Metropolis and Hinterland</i>, Cambridge 1996, p. 182; G. R. Storey, “The population of ancient Rome”, <i>Antiquity</i> 71 (1997) 966–978; B. Lançon, <i>Rome in Late Antiquity</i>, Edinburgh 2000; R. Krautheimer, <i>Rome: Profile of a City, 312–1308</i>, Princeton 1980; J. Durliat, <i>De la ville antique à la ville byzantine: le problème des subsistances</i>, Rome 1990; J. C. Russell, <i>Late Ancient and Medieval Population</i>, Philadelphia 1958; M. R. Salzman, <i>The Falls of Rome</i>, Cambridge 2021; A. H. M. Jones, <i>The Decline of the Ancient World</i>, London 1966. Ancient figures: Suetonius, <i>Divus Iulius</i> 41.3; <i>Res gestae divi Augusti</i> 15; Cassius Dio 76(77).1; Procopius, <i>Wars</i> 7.20.19 and 7.22.19.</li>'}
for u in M:
    if u['id'] in E:continue
    if u['t'] in O:E[u['id']]=O[u['t']]
    elif u['id'] in P:E[u['id']]=P[u['id']]
miss=[u['id'] for u in M if u['id'] not in E];assert not miss,miss
json.dump([{"id":u["id"],"e":E[u["id"]]} for u in M],open('en/fix_v74.json','w'),ensure_ascii=False,indent=0);print('ok',len(M))
