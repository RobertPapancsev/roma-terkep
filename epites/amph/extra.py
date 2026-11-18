# v94: β sor (kereskedők, császári pénztár), a bélyegek célterületei, α sor (az üres amfora súlya) -> amph/extra.json
import sys,re,json,collections
sys.path.insert(0,'/home/claude/roma/amph');import base as B,calc as C,beta as BT
D=B.D
# ---- β
k=collections.Counter(r[2] if isinstance(r[2],str) else 'priv' for r in BT.ROWS)
PER=[(138,192),(193,211),(212,235),(236,267)]
def per(y):
    for i,(a,b) in enumerate(PER):
        if a<=y<=b:return i
bp=[collections.Counter() for _ in PER]
for a,i,kd,y in BT.ROWS:
    kk=kd if isinstance(kd,str) else 'priv'
    if kk in('unread','frag'):continue
    t=BT.clean(i['full'])
    if y is None and kk=='dom':            # a szöveg maga keltez: Severus és fiai 198–211, „domini nostri Antonini” 212–217
        y=214 if re.search(r'domini nostri antonini',t) else 205
    if y is None:continue
    p=per(y)
    if p is not None:bp[p][kk]+=1
domf=collections.Counter()
for a,i,kd,y in BT.ROWS:
    if kd=='dom':
        t=BT.clean(i['full']).replace('v','u')
        domf['car' if 'domini nostri antonini' in t else 'three' if re.search(r'get|nnn|ggg',t) else 'two' if 'antonini' in t else 'frag']+=1
fiscp=collections.Counter()
for a,i,kd,y in BT.ROWS:
    if kd=='fisc':
        t=BT.clean(i['full']).replace(' ','')
        fiscp['baet' if re.search(r'bae?t',t) else 'tarr' if 'tarrac' in t else 'unk']+=1
G=collections.defaultdict(lambda:{'n':0,'names':collections.Counter(),'y':[]})
for a,i,kd,y in BT.ROWS:
    if not isinstance(kd,str):
        g=G[kd[1]];g['n']+=1;g['names'][BT.clean(i['full'])]+=1
        if y:g['y'].append(y)
top=sorted(G.items(),key=lambda x:-x[1]['n'])[:12]
# ---- bélyegek: hol kerültek elő ugyanannak a műhelynek az amforái
def country(a):
    if not a['fp']:return None
    ws=D.chain(a['fp'])|{a['fp']};c=[D.PT.get(w) for w in ws if 'Country' in D.PC.get(w,())];return c[0] if c else None
RH={'Germany','Switzerland','Netherlands','Austria','Luxembourg','Belgium'}
def dest(a):
    if B.inrome(a):return 'roma'
    c=country(a)
    return 'rhen' if c in RH else 'brit' if c=='United Kingdom' else 'gall' if c=='France' else 'hisp' if c in('Spain','Portugal') else 'alia'
PP=json.load(open('/home/claude/dl/ceipac/prodplace.json'));NS=D.NS
PN={p.replace(NS,''):t for p,t,la,lo in PP['p']};CONV={p.replace(NS,''):t for p,w,t,la,lo in PP['w'] if t in('Corduba','Astigi','Hispalis')}
W=collections.defaultdict(collections.Counter);tot=collections.Counter()
for a in D.AM.values():
    if 'dressel_20' not in a['type'] or len(a['prod'])!=1:continue
    if not any(D.IN[i]['kind']=='Stamp' for i in a['insc']):continue
    d=dest(a);tot[d]+=1;W[next(iter(a['prod']))][d]+=1
KD=['roma','rhen','brit','gall']
wl=[]
for p,c in W.items():
    n=sum(c[x] for x in KD)
    if n>=80:wl.append({'n':PN[p],'c':CONV.get(p,'?'),'t':n,**{x:c[x] for x in KD},'sh':round(100*c['roma']/n,1)})
wl.sort(key=lambda x:-x['sh'])
cvd=collections.defaultdict(collections.Counter)
for p,c in W.items():
    for x in KD:cvd[CONV.get(p,'?')][x]+=c[x]
# ---- α: az üres amfora súlya
al=[];pairs=[]
for a in B.ROME:
    if 'dressel_20' not in a['type']:continue
    for ii in a['insc']:
        i=D.IN[ii]
        if 'TitulusCode-ALF' in i['cls'] and i['full']:
            t=B.norm(i['full'])
            if re.fullmatch(r'[lxvic]+',t):
                v=C.rom(t)
                if 50<=v<=130:
                    al.append(v)
                    for jj in a['insc']:
                        g=D.IN[jj]
                        if 'TitulusCode-GAM' in g['cls'] and g['full'] and re.fullmatch(r'c{1,3}[lxvi]*',B.norm(g['full'])):
                            w=C.rom(B.norm(g['full']))
                            if 150<=w<=300:pairs.append((v,w))
als=sorted(al);nalf=sum(1 for a in B.ROME if 'dressel_20' in a['type'] for ii in a['insc'] if 'TitulusCode-ALF' in D.IN[ii]['cls'] and D.IN[ii]['full'])
q=lambda L,f:sorted(L)[int(f*(len(L)-1))]
OUT={'beta':{'n':len(BT.ROWS),'k':dict(k),'per':PER,'bp':[dict(c) for c in bp],'domf':dict(domf),'fiscp':dict(fiscp),'ngens':len(G),
  'top':[{'g':g,'n':v['n'],'ex':[t for t,_ in v['names'].most_common(3)],'y':[min(v['y']),max(v['y'])] if v['y'] else None,'ny':len(v['y'])} for g,v in top]},
 'dest':{'tot':{x:tot[x] for x in KD+['hisp','alia']},'work':wl,'conv':{c:dict(v) for c,v in cvd.items()}},
 'alpha':{'nall':nalf,'n':len(al),'med':q(al,.5),'q1':q(al,.25),'q3':q(al,.75),'mode':collections.Counter(al).most_common(4),'npair':len(pairs),'ratio':round(100*sum(v/(v+w) for v,w in pairs)/len(pairs),1) if pairs else None,'pmed':[q([p[0] for p in pairs],.5),q([p[1] for p in pairs],.5)] if pairs else None}}
json.dump(OUT,open('/home/claude/roma/amph/extra.json','w'),ensure_ascii=False)
if __name__=='__main__':
    for kk,v in OUT.items():print(kk,json.dumps(v,ensure_ascii=False)[:2600])
