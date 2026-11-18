# v114: DPRR (Digital Prosopography of the Roman Republic, CC BY-NC 4.0) – SPARQL-lekérdezés eredményeiből
import csv,json,collections as C,sys
d=sys.argv[1]
rd=lambda f:list(csv.reader(open(d+'/'+f,encoding='utf8'),delimiter='\t',quoting=csv.QUOTE_NONE))[1:]
q=lambda s:s.strip('"')
P={}
for r in rd('persons.tsv'):
    P[q(r[0])]={'name':q(r[1]),'nomen':q(r[2]),'f':r[3].endswith('Female>'),'ef':int(r[4]),'et':int(r[5]),'pat':r[6].startswith('"true'),'patu':r[7].startswith('"true'),'nov':r[8].startswith('"true'),'nob':r[9].startswith('"true'),'hi':q(r[10]) if len(r)>10 else ''}
posts=[(q(r[1]),q(r[2]).replace('Office: ',''),int(r[3]),int(r[4]),r[5].startswith('"true') if len(r)>5 else False) for r in rd('posts.tsv')]
offc=C.Counter(o for _,o,_,_,_ in posts)
cons=[(p,ds,u) for p,o,ds,de,u in posts if o=='consul']
bins=[]
for a in range(-509,-31,50):
    b=min(a+49,-31);xs=[(p,u) for p,ds,u in cons if a<=ds<=b]
    bins.append({'a':a,'b':b,'n':len(xs),'pat':sum(1 for p,u in xs if P[p]['pat']),'unc':sum(1 for p,u in xs if u)})
bynom=C.Counter(P[p]['nomen'] for p,ds,u in cons);dist=C.defaultdict(set)
for p,ds,u in cons: dist[P[p]['nomen']].add(p)
rep=C.Counter(p for p,ds,u in cons)
first=min((ds,p) for p,ds,u in cons if not P[p]['pat'] and not u and ds>-400)
out={'persons':len(P),'women':sum(1 for v in P.values() if v['f']),'posts':len(posts),'offices':len(offc),'top':offc.most_common(14),
     'cons':len(cons),'consp':len(rep),'consunc':sum(1 for p,ds,u in cons if u),'bins':bins,
     'nom':[(n,k,len(dist[n]),all(P[p]['pat'] for p in dist[n]),any(P[p]['pat'] for p in dist[n])) for n,k in bynom.most_common(12)],
     'rep':[(P[p]['name'],k,sorted(ds for pp,ds,u in cons if pp==p)) for p,k in rep.most_common(8)],
     'pat':sum(1 for v in P.values() if v['pat']),'patu':sum(1 for v in P.values() if v['patu']),'nob':sum(1 for v in P.values() if v['nob']),
     'nov':sorted([(v['name'],v['hi'],v['ef'],v['et']) for v in P.values() if v['nov']],key=lambda x:x[2]),
     'yr':[min(ds for _,_,ds,_,_ in posts),max(de for _,_,_,de,_ in posts)],'consyr':[min(ds for p,ds,u in cons),max(ds for p,ds,u in cons)]}
json.dump(out,open('data.json','w'),ensure_ascii=False)
for k,v in out.items():
    print(k,':',str(v)[:1500])
