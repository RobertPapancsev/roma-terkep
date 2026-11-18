# v91: foglalkozások a keresztény feliratokon (EDB) – ugyanaz a szótár és ugyanazok a szabályok, mint az EDR-nél (occ/calc.py)
import sys,re,json,collections,importlib.util
def load(n,p):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
sys.path.insert(0,'/home/claude/roma/edb');sys.path.insert(0,'/home/claude/roma/occ')
E=load('edbcalc','/home/claude/roma/edb/calc.py');import lex
PN=re.compile(r'^(?:marc(?:us|i|o|um)|luci(?:us|o|um)?|gai(?:us|o|um)?|cai(?:us|o|um)?|quint(?:us|i|o|um)|publi(?:us|o|um)?|tit(?:us|i|o|um)|gnae(?:us|i|o|um)|cnae(?:us|i|o|um)|aul(?:us|i|o|um)|sext(?:us|i|o|um)|decim(?:us|i|o|um)|tiberi(?:us|o|um)?|mani(?:us|o|um)?|numeri(?:us|o|um)?|spuri(?:us|o|um)?|servi(?:us|o|um)?|appi(?:us|o|um)?|sex|l|c|m|q|p|t|a|d|cn|ti)$')
try:
    import chrex;EX=set(map(tuple,chrex.EX))
except ImportError:EX=set()
H=[];nmil=0
for r in E.LAT:
    c=r['c']
    if lex.MIL.search(c):nmil+=1;continue
    for k,rx in lex.CL:
        for m in rx.finditer(c):
            pt=c[:m.start()].split()
            if pt and PN.match(pt[-1]) and not m.group(0).startswith(('a ','ab ','ad ')):continue
            if (r['id'],k) in EX:break
            H.append((r['id'],k,m.group(0),c[max(0,m.start()-90):m.end()+70]));break
if __name__=='__main__':
    print(len(E.LAT),nmil,len(H),len({h[0] for h in H}))
    for i,k,w,s in sorted(H,key=lambda h:(h[1],int(h[0]))):print(i,k,'|',s.replace(w,'['+w+']',1))
