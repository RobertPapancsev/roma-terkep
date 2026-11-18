import json
M=json.load(open('en/missing.json'))
E=['      <h2>Feeding Rome</h2>',
'      <p class="hint">Most of the food for a city of a million came by sea. According to Josephus, Africa fed Rome for eight months of the year and Egypt for four (Jewish War 2.383, 2.386). According to the <i>Epitome de Caesaribus</i>, under Augustus twenty million units of grain came from Egypt every year (1.6); the text does not name the unit, which scholars usually take to be the modius.</p>',
'      <h3 class="aqh">Grain</h3>',
'      <p class="hint">From the law of Gaius Gracchus (123 BC) eligible citizens received grain at a reduced price, and from the law of Clodius (58 BC) free, five modii a head each month, about 33 kg (P. Garnsey – D. Rathbone 1985). Under Augustus a little over 200,000 citizens received public grain (<i>Res gestae</i> 15; see “The population of Rome”). From the end of Augustus’s reign the grain supply was supervised by the <i>praefectus annonae</i> (Tacitus, <i>Annals</i> 1.7).</p>',
'      <p class="hint">Transport was in the hands of private shippers, so the emperors encouraged them with privileges. Claudius took on himself the loss of cargoes wrecked in storms and granted privileges to anyone who built a grain ship (Suetonius, <i>Claudius</i> 18–19). According to the jurist Gaius, a man of Latin status who built a ship of at least 10,000 modii and carried grain to Rome with it for six years received Roman citizenship (<i>Institutes</i> 1.32c). In the 2nd century the owner of a 50,000-modius ship was exempted from public duties (<i>Digest</i> 50.5.3).</p>',
'      <p class="hint">According to the <i>Historia Augusta</i>, Septimius Severus left at his death a seven years’ store of grain, reckoning a distribution of 75,000 modii a day (Severus 23.2).</p>',
'      <h3 class="aqh">Oil: Monte Testaccio</h3>',
'      <p class="hint">Behind the river harbour, the Emporium, stands Rome’s largest archaeological “database”: an artificial hill made almost entirely of broken olive oil amphorae. Sherds soaked in oil could not be reused. The hill is no haphazard dump: amphorae with their bases removed were filled with sherds and built into stepped retaining walls, the other sherds were tipped in behind them, and the smell of rancid oil was covered with lime (J. A. Lobell 2009, on J. Remesal’s excavation).</p>',
'          <tr><td>Base area</td><td>c. 2 ha</td><td>Claridge; Peña</td></tr>',
'          <tr><td>Volume</td><td>c. 580,000 m³</td><td>Claridge; Peña</td></tr>',
'          <tr><td>Height</td><td>c. 35 m; other summaries give 40–50 m above the surrounding ground</td><td>Claridge; Peña; Broekaert</td></tr>',
'          <tr><td>Circumference</td><td>nearly 1 km</td><td>Claridge; Peña</td></tr>',
'          <tr><td>In use</td><td>from Augustus to the mid-3rd century; the latest consular date found so far is AD 265</td><td>Dressel; Lobell 2009</td></tr>',
'      <h4 class="aqh4">What is it made of?</h4>',
'      <div class="foodbar"><span class="fb1" style="width:80%">c. 80%</span><span class="fb2" style="width:15%">15–17%</span><span class="fb3" style="width:5%"></span></div>',
'      <p class="hint aqleg"><span class="sw f1"></span> southern Spanish (Baetican) oil amphora, type Dressel 20 · <span class="sw f2"></span> North African (Tripolitanian and Tunisian) amphorae · <span class="sw f3"></span> c. 5% Spanish and Gaulish wine and fish-sauce containers (W. Broekaert 2011). Another summary puts the Baetican share above 85% (Lobell 2009).</p>',
'      <h4 class="aqh4">How many amphorae? Three estimates</h4>',
'        <div class="fe"><span class="fen">E. Rodríguez Almeida 1984</span><span class="feb"><span style="width:37.7%"></span></span><span class="fev">c. 20 million</span></div>',
'        <div class="fe"><span class="fen">J. Remesal (Lobell 2009)</span><span class="feb"><span style="width:47.2%"></span></span><span class="fev">c. 25 million</span></div>',
'        <div class="fe"><span class="fen">B. Ward-Perkins 2005</span><span class="feb"><span style="width:100%"></span></span><span class="fev">c. 53 million</span></div>',
'      <p class="hint">The estimates start from the volume of the hill and the density of the excavated sections, which is why they differ so much. A Dressel 20 amphora held about 70 litres of oil (7–8 modii, 61–70 litres according to P. Tyers); empty it weighed about 30 kg, full about 100 kg. By Broekaert’s calculation this means 1.4–1.75 billion litres of oil from Augustus to Aurelian, about 74,000–92,600 amphorae, or 5.2–6.5 million litres, a year, and 100–150 shiploads a year (Broekaert 2011). Ward-Perkins’s higher number of amphorae implies about 6 billion litres.</p>',
'      <h4 class="aqh4">The inscriptions</h4>',
'      <p class="hint">Many amphorae carry an inscription painted after firing (<i>titulus pictus</i>); scholars label its lines with Greek letters. Line α is the weight of the empty vessel, β the name of the shipping merchant, γ the weight of the oil, δ the control entry: the checkpoint in Spain, the consular year and the names of the officials. On one amphora, for example, the empty vessel weighs 82 Roman pounds and the oil 216 Roman pounds (Lobell 2009). The stamps pressed into the handles preserve names connected with the pottery workshop or the estate. Thanks to the consular dates the layers of the hill can be dated to the year; Heinrich Dressel began collecting them in 1872, and since the 1980s the excavations of E. Rodríguez Almeida, then of J. M. Blázquez and J. Remesal, have continued the work (CEIPAC, University of Barcelona).</p>',
'      <p class="hint">According to the <i>Historia Augusta</i>, Septimius Severus gave the Roman people a free daily distribution of oil for all time (Severus 18.3). Broekaert argues that the stamps and inscriptions show imports peaking already under the Antonines; Severus’s measure was rather a reorganization of transport. It was then that the confiscated Spanish olive estates passed to the emperor: on the stamps the abbreviation AVGGGNNN stands for Severus and his two sons (Broekaert 2011).</p>',
'      <h3 class="aqh">At the end of the 3rd century</h3>',
'      <p class="hint">By the time of Aurelian (270–275) bread rather than grain was being distributed: according to the <i>Historia Augusta</i> he added an ounce to the weight of the loaves from the revenues of Egypt (Aurelian 47.1), and he also distributed pork (35.2). Besides the free oil, bread and pork he planned free wine as well: he wanted vineyards planted in Etruria, but this was not carried out; the imperial wine was sold in the porticoes of the temple of Sol (48.1–4).</p>',
'      <h3 class="aqh">On the map</h3>',
'      <p class="hint"><button class="chip" id="foodbtn" aria-pressed="false">Highlight the sites on the map</button> Click a name to jump to it on the map. The harbours of Ostia and Portus lie outside the map.</p>',
]
PL=[("emporium","Emporium","the quay of the river harbour, from 193 BC"),
("porticusaemilia","Porticus Aemilia","a great warehouse hall beside the harbour (on another reading a ship dock)"),
("horreagalbae","Horrea Galbae","warehouses for grain, oil and wine around three courtyards"),
("horrealolliana","Horrea Lolliana","warehouses in the harbour quarter"),
("monstestaceus","Monte Testaccio","the hill of emptied oil amphorae"),
("statioannonae","Statio Annonae (?)","the grain supply office in the Forum Boarium; the identification is disputed"),
("minucia","Porticus Minucia Frumentaria (?)","the place of the free grain distribution; the identification is disputed"),
("horrea","Horrea Agrippiana","a warehouse between the Forum and the Palatine"),
("horreapiper","Horrea Piperataria","the spice warehouses"),
("macellumliviae","Macellum Liviae","a food market on the Esquiline")]
E+=[f'        <li><span class="n">·</span><span><strong><a href="#" data-goto="{i}">{n}</a></strong><span class="sub">{s}</span></span></li>' for i,n,s in PL]
E.append('      <li><b>Feeding Rome.</b> Josephus, <i>Jewish War</i> 2.383, 2.386; <i>Epitome de Caesaribus</i> 1.6; <i>Res gestae</i> 15; Tacitus, <i>Annals</i> 1.7; Suetonius, <i>Claudius</i> 18–19; Gaius, <i>Institutes</i> 1.32c; <i>Digest</i> 50.5.3; <i>Historia Augusta</i>, Severus 18.3, 23.2, Aurelian 35.2, 47.1, 48.1–4. P. Garnsey – D. Rathbone, “The Background to the Grain Law of Gaius Gracchus”, <i>Journal of Roman Studies</i> 75 (1985) 20–25. Monte Testaccio: H. Dressel, <i>Ricerche sul Monte Testaccio</i>, Rome 1878; E. Rodríguez Almeida, <i>Il Monte Testaccio: ambiente, storia, materiali</i>, Rome 1984; J. M. Blázquez Martínez – J. Remesal Rodríguez (eds), <i>Estudios sobre el Monte Testaccio (Roma)</i> I–IV, Barcelona 1999–2007; W. Broekaert, “Oil for Rome during the Second and Third Century AD: a Confrontation of Archaeological Records and the Historia Augusta”, <i>Mnemosyne</i> 64 (2011) 591–623; J. A. Lobell, “Trash Talk”, <i>Archaeology</i> 62/2 (2009); B. Ward-Perkins, <i>The Fall of Rome and the End of Civilization</i>, Oxford 2005; A. Claridge, <i>Rome</i> (Oxford Archaeological Guides), 2nd ed., Oxford 2010; J. T. Peña, <i>Roman Pottery in the Archaeological Record</i>, Cambridge 2007; “Dressel 20”, in: P. Tyers, <i>Roman Amphoras in Britain</i>, <i>Internet Archaeology</i> 1 (1996).</li>')
assert len(E)==len(M),(len(E),len(M))
for u,e in zip(M,E):
    a=u['t'].strip()[:12];b=e.strip()[:12]
    assert a[:4]==b[:4],(u['id'],a,b)
json.dump([{"id":u["id"],"e":e} for u,e in zip(M,E)],open('en/fix_v78.json','w'),ensure_ascii=False,indent=0);print('ok',len(E))
