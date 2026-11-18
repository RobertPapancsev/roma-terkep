# Étrend izotópokból: De Angelis et al. 2020 (Archaeol Anthropol Sci 12:244, CC BY 4.0), 3. táblázat (egyéni adatok) -> diet/data.json
import re,json,statistics as st
T=open('/home/claude/dl/iso2/deangelis2020.txt',encoding='utf8').read().replace('−','-')
rows=[]
for l in T.split('\n'):
    m=re.match(r'\s*(CM|CBM|CBQ|CBN|PS|QCP)\s+(\S+)\s+(F|M|Ind)\s+(\S+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+(-\s?[\d.]+)\s+([\d.]+)\s*$',l)
    if m: rows.append(dict(site=m[1],id=m[2],sex=m[3],age=m[4],C=float(m[5]),N=float(m[6]),CN=float(m[7]),d13=float(m[8].replace(' ','')),d15=float(m[9])))
def ok(r): return r['C']>=30 and r['N']>=10 and 2.9<=r['CN']<=3.6
if __name__=='__main__':
    print(len(rows),{s:sum(1 for r in rows if r['site']==s) for s in ['CM','CBM','CBQ','CBN','PS','QCP']})
    for s in ['CBM','CBN','CBQ','CM','PS','QCP']:
        v=[r for r in rows if r['site']==s]
        print(s,len(v),'d13 mean',round(st.mean(r['d13'] for r in v),2),'min',min(r['d13'] for r in v),'max',max(r['d13'] for r in v),'d15 mean',round(st.mean(r['d15'] for r in v),2),'median',st.median(r['d15'] for r in v),'min',min(r['d15'] for r in v),'max',max(r['d15'] for r in v))
    print('sex',{x:sum(1 for r in rows if r['sex']==x) for x in ('F','M','Ind')})
    print('dups',len(rows)-len({r['id'] for r in rows}))
