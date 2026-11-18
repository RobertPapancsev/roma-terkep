import json,urllib.request,urllib.parse,time,sys
UA="roman-empire-map/1.0 (https://eidmar-roma.netlify.app; personal non-commercial research map)"
C=dict(rs=('Q403','sr'),ba=('Q225','bs'),me=('Q236','sr'),bg=('Q219','bg'),al=('Q222','sq'),xk=('Q1246','sq'),tn=('Q948','ar'),dz=('Q262','ar'),ma=('Q1028','ar'),ly=('Q1016','ar'),eg=('Q79','ar'),jo=('Q810','ar'),lb=('Q822','ar'),sy=('Q858','ar'),ps=('Q219060','ar'),ge=('Q230','ka'),am=('Q399','hy'),ua=('Q212','uk'),md=('Q217','ro'),iq=('Q796','ar'),sa=('Q851','ar'),az=('Q227','az'),es=('Q29','es'),il=('Q801','he'))
P='PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> '
def get(s):
    u='https://qlever.dev/api/wikidata?'+urllib.parse.urlencode({'query':P+s})
    for t in range(5):
        try:
            r=urllib.request.Request(u,headers={'User-Agent':UA,'Accept':'application/sparql-results+json'})
            with urllib.request.urlopen(r,timeout=180) as f: return json.load(f)['results']['bindings']
        except Exception as e: print('err',e,flush=True); time.sleep(30*(t+1))
def lab(qs):
    out={}
    qs=list(qs)
    for k in range(0,len(qs),300):
        vals=' '.join('wd:'+q for q in qs[k:k+300])
        for x in get(f'SELECT ?x ?l WHERE {{ VALUES ?x {{ {vals} }} ?x rdfs:label ?l FILTER(LANG(?l)="en") }}') or []:
            out[x['x']['value'].rsplit('/',1)[1]]=x['l']['value']
    return out
for cc in sys.argv[1:]:
    q,lg=C[cc]
    B=get(f'''SELECT ?i ?c ?le ?ll (GROUP_CONCAT(DISTINCT STR(?ty);separator="|") AS ?ts) (GROUP_CONCAT(DISTINCT STR(?pe);separator="|") AS ?ps) (SAMPLE(?hd) AS ?h) (SAMPLE(?a) AS ?ad) WHERE {{
 ?i wdt:P17 wd:{q} ; wdt:P1435 ?hd ; wdt:P625 ?c .
 OPTIONAL{{?i rdfs:label ?le FILTER(LANG(?le)="en")}} OPTIONAL{{?i rdfs:label ?ll FILTER(LANG(?ll)="{lg}")}}
 OPTIONAL{{?i wdt:P31 ?ty}} OPTIONAL{{?i wdt:P2348 ?pe}} OPTIONAL{{?i wdt:P131 ?a}} }} GROUP BY ?i ?c ?le ?ll''')
    if B is None: continue
    ids=set()
    for x in B:
        for k in ('ts','ps'): ids|={v.rsplit('/',1)[1] for v in x.get(k,{}).get('value','').split('|') if v}
        for k in ('h','ad'):
            if k in x: ids.add(x[k]['value'].rsplit('/',1)[1])
    L=lab(ids); out=[]
    for x in B:
        f=lambda k: x.get(k,{}).get('value','')
        out.append({'i':{'value':f('i')},'c':{'value':f('c')},'lab':{'value':f('ll')},'len':{'value':f('le')},
          't':{'value':'|'.join(L.get(v.rsplit('/',1)[1],'') for v in f('ts').split('|') if v)},
          'per':{'value':'|'.join(L.get(v.rsplit('/',1)[1],'') for v in f('ps').split('|') if v)},
          'h':{'value':L.get(f('h').rsplit('/',1)[-1],'')},'adm':{'value':L.get(f('ad').rsplit('/',1)[-1],'')}})
    json.dump({'results':{'bindings':out}},open(f'{cc}.json','w')); print(cc,len(out),flush=True); time.sleep(3)
