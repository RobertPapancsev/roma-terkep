# Russell 2013, Gazetteer of Stone Quarries in the Roman World (OxREP PDF) -> data/quarries/quarries.json
import pdfplumber, re, json
R='/home/claude/imperium/data/quarries/'
H=['Site','Latitude','Longitude','Location','Country','Province','Material','Bibliography']
rows=[]
with pdfplumber.open(R+'Stone_Quarries_Database.pdf') as pdf:
    for pg in pdf.pages:
        ws=pg.extract_words()
        hd={w['text']:w for w in ws if w['text'] in H}
        if 'Latitude' not in hd or 'Material' not in hd: continue
        top0=max(hd[h]['bottom'] for h in hd)
        xs=[hd[h]['x0'] if h in hd else None for h in H]
        bnd=[xs[i]-3 for i in range(len(H))]
        col=lambda x: max(i for i,b in enumerate(bnd) if x>=b) if x>=bnd[0] else 0
        lines={}
        for w in ws:
            if w['top']<=top0+1 or w['top']>pg.height-40: continue
            lines.setdefault(round(w['top']),[]).append(w)
        cur=None
        for t in sorted(lines):
            cells=['']*len(H)
            for w in sorted(lines[t],key=lambda w:w['x0']): c=col(w['x0']); cells[c]=(cells[c]+' '+w['text']).strip()
            if re.fullmatch(r'-?\d+\.\d+',cells[1]) and re.fullmatch(r'-?\d+\.\d+',cells[2]):
                cur=cells[:]; rows.append(cur)
            elif cur:
                for i in (0,3,4,5,6,7):
                    if cells[i]: cur[i]=(cur[i]+' '+cells[i]).strip()
out=[dict(zip(H,r)) for r in rows]
for o in out: o['Latitude']=float(o['Latitude']); o['Longitude']=float(o['Longitude'])
json.dump(out,open(R+'quarries.json','w'),ensure_ascii=False,indent=0)
print(len(out)); print(out[0]); print(out[-1])
