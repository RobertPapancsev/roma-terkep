# v92: a δ jelű (ellenőrző) festett felirat körzetneve és éve
import sys,re,collections
sys.path.insert(0,'/home/claude/roma/amph');import base as B
D=B.D
DIS=[('astigi',r'\bas?tig'),('hispalis',r'\bhispa?l|\bhisp\b|\bhisp-'),('corduba',r'\bcordu?b?\b|\bcordub|\bcord-|\bcordu'),('lacca',r'\blacc'),('malaca',r'\bmalac'),('portus',r'\ba[dt] port|\bportu\b|\bportus\b|\bportens')]
RX=[(k,re.compile(p)) for k,p in DIS]
try:
    import deltaex;EX=deltaex.EX
except ImportError:EX={}
def district(i):
    if i['id'] in EX:return EX[i['id']]
    t=B.norm(i['full']);h=[k for k,rx in RX if rx.search(t)]
    return h[0] if len(h)==1 else ('?' if h else None)
ROWS=[]
for a in B.ROME:
    for ii in a['insc']:
        i=D.IN[ii]
        if 'TitulusCode-DEL' in i['cls'] and i['full']:ROWS.append((a,i,district(i)))
if __name__=='__main__':
    print(len(ROWS),collections.Counter(r[2] for r in ROWS))
    for a,i,d in sorted(ROWS,key=lambda r:(str(r[2]),B.norm(r[1]['full']))):
        if d:print(d,i['id'],B.year(a),'|',B.norm(i['full'])[:150])
