# v92: CEIPAC / Roman Open Data – a Rómában talált amforák feliratai. Bemenet: /home/claude/dl/ceipac/*.json (SPARQL-lekérdezések: dump.py)
import sys,re,json,collections
sys.path.insert(0,'/home/claude/dl/ceipac');import load as D
def inrome(a):return bool(a['fp']) and any(D.PT.get(w)=='Roma' and 'Municipality' in D.PC.get(w,()) for w in D.chain(a['fp']))
ROME=[a for a in D.AM.values() if inrome(a)]
def year(a):
    """(év, forrás): 't' = a konzuli dátum magán az amforán olvasható; 'c' = az ásatási réteg kelte; None = nincs egyetlen évre szóló keltezés."""
    tit=[t for d,b,e,t in a['dates'] if t]
    ys=sorted({int(b) for d,b,e,t in a['dates'] if d.startswith('YearSpan') and b is not None and b==e})
    if len(ys)!=1:return None,None
    src='t' if any('titulus' in t.lower() for t in tit) else 'c'
    return ys[0],src
def norm(t):
    t=t.lower();t=re.sub(r'\(---\)|\(\?\)','',t);t=re.sub(r'[\[\]\(\)¨\'~]','',t);return re.sub(r'\s+',' ',t).strip()
