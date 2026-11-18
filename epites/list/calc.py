# v90: Róma a birodalom latin feliratai között. Bemenet: LIST v1.2 (Kaše–Heřmánková–Sobotková, Zenodo 10.5281/zenodo.10473706; EDCS + EDH), CC BY 4.0.
# Minden mutató a feliratok szövegéből, ugyanazzal a szabállyal számol Rómára és a provinciákra (nem az EDCS kulcsszavaiból).
import re,json,collections,importlib.util,sys,unicodedata
import pandas as pd
def load(n,p):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
A=load('agecalc','/home/claude/roma/age/calc.py');N=A.NMC;rom=A.rom
OL=load('occlex','/home/claude/roma/occ/lex.py')
def eclean(t):
    """EDCS-jelölés → kisbetűs, feloldott szöveg; ¤ = hiány, ¤t = a hiány közvetlenül egy szóhoz/számhoz tapad (csonka)."""
    t=t.replace('[[','[').replace(']]',']')
    t=re.sub(r'<([^=>]*)=[^>]*>',r'\1',t);t=re.sub(r'\{[^}]*\}','',t);t=re.sub(r'\((?:!|\?|vac[^)]*)\)','',t);t=t.replace('|(','(')
    t=re.sub(r'\s*//\s*',' § ',t)
    t=re.sub(r'(?<=[A-Za-z\)])\[[1-6]\]',' ¤t ',t);t=re.sub(r'\[[1-6]\]',' ¤ ',t)
    t=re.sub(r'\[([1-6]) ',r' ¤ [',t);t=re.sub(r' ([1-6])\]',r'] ¤ ',t)
    t=re.sub(r'(?<=[A-Za-z\)])\[(?=\s*(?:/|§|$))',' ¤t ',t);t=re.sub(r'\[(?=\s*(?:/|§|$))',' ¤ ',t);t=re.sub(r'(?:(?<=^)|(?<=/ )|(?<=§ ))\]',' ¤ ',t)
    t=re.sub(r'(?<=\S)/(?=\S)','',t);t=t.replace('/',' ')
    t=unicodedata.normalize('NFD',t.lower());t=''.join(ch for ch in t if unicodedata.category(ch)!='Mn')
    t=re.sub(r'[\[\]\(\)]','',t);t=re.sub(r'[^a-z¤§ ]',' ',t)
    return re.sub(r'\s+',' ',t).strip()
def tlen(c):return len(re.sub(r'[¤§ ]|¤t','',c.replace('¤t','')))
IT=re.compile('Regio|^Italia$')
REG=[('roma',lambda p:p=='Roma'),('italia',lambda p:bool(IT.search(p))),('insulae',lambda p:p in('Sicilia','Sardinia','Corsica')),
 ('africa',lambda p:p in('Africa proconsularis','Numidia','Mauretania Caesariensis','Mauretania Tingitana')),('hispania',lambda p:p in('Hispania citerior','Lusitania','Baetica')),
 ('gallia',lambda p:p.startswith(('Gallia','Aquitani','Lugudunensis','Belgica','Germania','Alpes'))),('britannia',lambda p:p=='Britannia'),
 ('danuvius',lambda p:p.startswith(('Dalmatia','Pannonia','Noricum','Raetia','Dacia','Moesia','Thracia'))),
 ('oriens',lambda p:p in('Achaia','Asia','Macedonia','Syria','Aegyptus','Arabia','Galatia','Palaestina','Cappadocia','Pontus et Bithynia','Creta et Cyrenaica','Lycia et Pamphylia','Cilicia','Cyprus','Mesopotamia','Armenia','Regnum Bospori'))]
def region(p):
    for k,f in REG:
        if f(p):return k
    return 'alia'
INSTR=re.compile(r'tituli fabricationis|sigilla impressa|signacula|tituli possessionis|tesserae nummulariae')
F={'dm':re.compile(r'\bdi?is manibus\b|\bdis man\b'),'hse':re.compile(r'\bhic sit(?:us|a|i|ae|e)\b|\bhic siti sunt\b'),'sttl':re.compile(r'\bsit (?:tibi|vobis) terra levis'),
 'bm':re.compile(r'\bbene ?merenti'),'pace':re.compile(r'\bin pace\b'),'dep':re.compile(r'\bdeposit(?:us|a|io|i|ae)\b'),'vix':re.compile(r'\bvixit\b|\bbixit\b|\bvixsit\b'),
 'lib':N.RX['lib'],'mil':OL.MIL}
for k in N.RX:
    if k not in F and k in('ser','verna','servus'):F[k]=N.RX[k]
F['ser']=re.compile(r'\bserv(?:us|a|o|ae|um|am)\b|\bvern(?:a|ae|am)\b')
CHR=re.compile(r'inscriptiones christianae')
SEP=re.compile(r'tituli sepulcrales')
X0,X1,W=-100,600,50;B=list(range(X0,X1,W))
def aw(a,b):
    L=b-a
    return [(1.0 if x<=a<x+W else 0.0) if L<=0 else max(0,min(b,x+W)-max(a,x))/L for x in B]
def run():
    t=pd.read_pickle('/home/claude/dl/list/all_text.pkl')
    rows=[]
    for i,(p,ins,st,nb,na,city) in enumerate(zip(t['province'],t['inscription'],t['status'],t['not_before'],t['not_after'],t['urban_context_city'])):
        st=st if isinstance(st,str) else '';c=eclean(ins) if isinstance(ins,str) else ''
        rows.append((region(p if isinstance(p,str) else ''),p,st,c,nb,na,city))
    return t,rows
if __name__=='__main__':
    t,rows=run()
    import pickle;pickle.dump(rows,open('/home/claude/dl/list/rows.pkl','wb'))
    print(len(rows),collections.Counter(r[0] for r in rows))
    for i in (5,500,20000,60000,300000,400000):print(t['inscription'].iloc[i][:150],'=>',rows[i][3][:150])
