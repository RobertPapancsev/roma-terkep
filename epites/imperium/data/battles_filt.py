import csv,re,json,sys
R=list(csv.DictReader(open('/home/claude/dl/battles/all.csv')));B={}
for r in R:
    if r['b'] in B:
        if int(r['prec'])>int(B[r['b']]['prec']): B[r['b']]=r
    else: B[r['b']]=r
K=re.compile(r"Roman|Rome|Punic|Samnite|Pyrrhic|Macedonian War|Mithridat|Gallic War|Caesar|Cimbri|Jugurth|Servile|Social War|Latin War|Seleucid War|Sasanian|Sassanid|Parthian|Dacian|Marcomann|Gothic War|Tetrarchy|Constantin|Licinius|Emperors|Jewish|Boudica|Cantabrian|Sertori|Hannibal|Hun|Vandal|Byzantine|Sulla|Pompe|optimates|populares|Septimius|Aurelian|Julian|Antony|Octavian|Lusitanian|Numantine|Celtiberian|Achaean War|Illyrian War|Veii|Volsci|Aequi|Goth|Palmyr|Alaric|Stilicho|Aetius|Bar Kokhba|Teutoburg|Germanicus|Arminius|Crisis of the Third",re.I)
def yr(d):
    m=re.match(r'(-?)(\d+)-',d);y=int(m.group(2));return -(y+1) if m.group(1) else y
keep=[]
for r in B.values():
    lon,lat=map(float,r['coord'][6:-1].split())
    txt=' '.join([r['bLabel'],r['parts'],r['partof'],r['desc']])
    if not(-12<=lon<=52 and 22<=lat<=60) or not r['bLabel'] or not r['enwiki'] or not K.search(txt): continue
    keep.append(dict(q=r['b'].split('/')[-1],y=yr(r['date']),en=r['bLabel'],hu=r['huLabel'],po=r['partof'],pa=r['parts'],de=r['desc'],lon=lon,lat=lat,t=r['type'].split('/')[-1],p=int(r['prec']),w=r['enwiki'],hw=r['huwiki']))
keep.sort(key=lambda k:k['y'])
if __name__=='__main__':
    for k in keep: print(k['y'],'|',k['en'],'|',k['po'][:38],'|',k['pa'][:40])
