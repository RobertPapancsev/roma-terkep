import json,re
M=json.load(open('en/missing.json'));D=json.load(open('insc/data.json'))
fmt=lambda n:f'{n:,}'
PH={'A Salaria-temető':'The Salarian cemetery','a via Salaria és a via Pinciana között; több lelőhely-leírás összevonva':'between the Via Salaria and the Via Pinciana; several findspot descriptions combined',
'A Vigna Codini kolumbáriumai':'The columbaria of the Vigna Codini','San Paolo fuori le mura és környéke':'San Paolo fuori le mura and surroundings','Villa Pamphilj temetői':'The cemeteries of the Villa Pamphilj',
'Livia szolgáinak és felszabadítottjainak kolumbáriuma (Monumentum Liviae)':'The columbarium of Livia’s slaves and freedmen (Monumentum Liviae)','A Vigna Randanini zsidó katakombája':'The Jewish catacomb of the Vigna Randanini',
'A Statiliusok kolumbáriuma':'The columbarium of the Statilii','a Porta Maior mellett':'beside the Porta Maior','A vatikáni nekropolisz és a via Triumphalis menti temető':'The Vatican necropolis and the cemetery along the Via Triumphalis',
'főleg az aréna mellvédjének (podium) töredékei':'mainly fragments of the arena parapet (podium)',"A Corso d'Italia, a karmelita templom környéke":"Corso d'Italia, around the Carmelite church",'a Salaria-temető része':'part of the Salarian cemetery',
'Callistus katakombái':'The catacombs of Callixtus','A monteverdei zsidó katakomba':'The Jewish catacomb of Monteverde','A császári lovastestőrség (equites singulares) temetője':'The cemetery of the imperial horse guard (equites singulares)',
'via Labicana, a SS. Marcellino e Pietro katakombánál':'Via Labicana, at the catacomb of SS. Marcellino e Pietro','A Volusiusok síremléke':'The tomb of the Volusii','falfirkák az épület falain':'graffiti on the walls of the building',
'Domitilla katakombái':'The catacombs of Domitilla','Praetextatus katakombái':'The catacombs of Praetextatus','Priscilla katakombái':'The catacombs of Priscilla','Augustus fóruma':'Forum of Augustus',
'A Villa Torlonia zsidó katakombái':'The Jewish catacombs of the Villa Torlonia','Traianus fóruma':'Forum of Trajan','A Largo Argentina szent körzete':'The sacred area of Largo Argentina',
'sírfeliratok':'epitaphs','vallási feliratok':'religious inscriptions','tiszteletbeli feliratok':'honorific inscriptions','építési feliratok':'building inscriptions','egyéb és ismeretlen':'other and unknown',
'Via Salaria (és a Pinciana felé)':'Via Salaria (and towards the Pinciana)','Via Praenestina (Porta Maior)':'Via Praenestina (Porta Maior)','Vatikán (via Triumphalis, via Cornelia)':'Vatican (Via Triumphalis, Via Cornelia)'}
def tr(s):
    for a,b in sorted(PH.items(),key=lambda x:-len(x[0])):s=s.replace('>'+a+'<','>'+b+'<').replace(' '+a+' (',' '+b+' (')
    s=re.sub(r'Kr\. e\. (\d+)',r'\1 BC',s);s=re.sub(r'Kr\. u\. (\d+)',r'AD \1',s)
    s=re.sub(r'(?<=\d) (?=\d{3}\b)',',',s)
    return s
P={
'u04062':'      <h2>Inscriptions</h2>',
'u04063':f'      <p class="hint">The open data set of the Epigraphic Database Roma (EDR) contains {fmt(D["n"])} inscriptions found in Rome. For {fmt(D["loc"])} of them the findspot is known (as a text description), and {fmt(D["dated"])} are dated. By type: {fmt(D["types"]["tomb"])} epitaphs, {fmt(D["types"]["sacred"])} religious, {fmt(D["types"]["honor"])} honorific and {fmt(D["types"]["build"])} building inscriptions; the rest are other or unknown (graffiti, seat inscriptions, fragments).</p>',
'u04064':'      <h3 class="aqh">Inscriptions over time</h3>',
'u04065':'      <p class="hint">The date is usually a period (“1st–2nd century AD”); the inscription’s weight is spread evenly over the 25-year bands of the period, as on the “Building activity over time” card.</p>',
'u04066':f'      <div class="seg inscsel" role="group" aria-label="Precision of dating"><button data-m="all" aria-pressed="true">All dated inscriptions ({fmt(D["time"]["nAll"])})</button><button data-m="tight" aria-pressed="false">Only those dated within 100 years ({fmt(D["time"]["nTight"])})</button><button data-m="notomb" aria-pressed="false">Without epitaphs</button></div>',
'u04068':'      <p class="hint popinfo" id="inscinfo">Hover over a bar; click to set the map’s year slider to that time.</p>',
'u04069':'      <p class="hint">More than four-fifths of the inscriptions are epitaphs, and these are densest in the first half of the 1st century AD. This is when most of the great columbaria were built; in some, such as Livia’s and the Statilii’s, the slaves and freedmen of a single noble household were buried. The peak of honorific, religious and building inscriptions is later, the second half of the 2nd century AD and the early 3rd. The curves show the habit of setting up inscriptions, not the population; from the mid-3rd century the number of inscriptions falls sharply.</p>',
'u04070':'      <h3 class="aqh">The largest findspots</h3>',
'u04071':'        <thead><tr><th>Findspot</th><th>Inscriptions</th><th>Main period</th><th>Most frequent type</th></tr></thead>',
'u04096':'      <p class="hint">The “main period” is the middle half of the inscriptions’ dates (based on the midpoints of the periods, rounded to 25 years). Inscriptions were assigned to a findspot from the EDR findspot descriptions (for example every description beginning “Vigna Codini” went into one row). Click a linked name to jump to it on the map.</p>',
'u04097':'      <h3 class="aqh">Epitaphs along the roads</h3>',
'u04098':f'      <p class="hint">Burial inside the city was not allowed in Rome, so tombs lined the roads leading out of it. From the names of roads, gates and catacombs in the findspot descriptions, {fmt(D["nroad"])} inscriptions can be assigned to a road; the bar shows the number of epitaphs.</p>',
}
HH=[u for u in M if u['t'].strip().startswith('<li><b>Feliratok.')]
H=HH[0]['id'] if HH else '_'
P[H]='      <li><b>Inscriptions.</b> Epigraphic Database Roma (EDR), EpiDoc files, version 12 (Sapienza Università di Roma – Università di Napoli L’Orientale – Università di Firenze – Università di Foggia; S. Panciera, G. Camodeca, G. A. Cecconi, S. Orlandi, L. Fabriani, S. Evangelisti), Zenodo 2026, <a href="https://doi.org/10.5281/zenodo.18468635">10.5281/zenodo.18468635</a>, CC BY 4.0. The summary is our own: inscriptions found in Rome (findspot: Roma), type as classified by EDR, dating from the EDR “notBefore–notAfter” data, findspots and roads from keywords in the findspot descriptions (insc/calc.py).</li>'
out=[]
for u in M:
    if u['id'] in P:e=P[u['id']]
    elif 'class="hint bldleg"' in u['t'] or '<tr><td>' in u['t'] or 'class="fe"' in u['t']:e=tr(u['t'])
    else:raise SystemExit('missing '+u['id']+u['t'][:60])
    out.append({"id":u['id'],"e":e})
json.dump(out,open('en/fix_v82c.json' if len(M)<10 else 'en/fix_v82.json','w'),ensure_ascii=False,indent=0)
import sys
for o in out:
    if re.search(r'[őűáéíóöüú]',re.sub(r'<[^>]+>','',o['e']).replace('Pamphilj','')) and 'Università' not in o['e']:print('HU?',o['id'],re.sub(r'<[^>]+>','',o['e'])[:120])
print('ok',len(out))
