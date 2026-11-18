import json,urllib.request,urllib.parse,time,sys
UA="roman-empire-map/1.0 (https://eidmar-roma.netlify.app; personal non-commercial research map)"
C=dict(hu='Q28',sk='Q214',gr='Q41',pt='Q45',es='Q29',cy='Q229',mt='Q233',il='Q801',tr='Q43',hr='Q224',rs='Q403',ba='Q225',me='Q236',bg='Q219',al='Q222',xk='Q1246',tn='Q948',dz='Q262',ma='Q1028',ly='Q1016',eg='Q79',jo='Q810',lb='Q822',sy='Q858',ps='Q219060',ge='Q230',am='Q399',ua='Q212',md='Q217',lu='Q32',de='Q183',iq='Q796',sa='Q851',az='Q227',mk='Q221',si='Q215',ro='Q218',at='Q40',ch='Q39',nl='Q55',be='Q31',gb='Q145',fr='Q142',it='Q38')
ROMP='wd:Q2277 wd:Q1747689 wd:Q17167 wd:Q217050 wd:Q11768 wd:Q42834 wd:Q201038 wd:Q12544'
def q(cc):
    s=f'''PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?i ?c (SAMPLE(?l) AS ?lab) (SAMPLE(?le) AS ?len) (GROUP_CONCAT(DISTINCT ?hl;separator="|") AS ?h) (GROUP_CONCAT(DISTINCT ?tl;separator="|") AS ?t) (GROUP_CONCAT(DISTINCT ?pl;separator="|") AS ?per) (SAMPLE(?al) AS ?adm) WHERE {{
 ?i wdt:P17 wd:{C[cc]} ; wdt:P1435 ?hd ; wdt:P625 ?c .
 OPTIONAL{{?hd rdfs:label ?hl FILTER(LANG(?hl)="en")}}
 OPTIONAL{{?i rdfs:label ?l FILTER(LANG(?l)!="en")}} OPTIONAL{{?i rdfs:label ?le FILTER(LANG(?le)="en")}}
 OPTIONAL{{?i wdt:P31 ?ty . ?ty rdfs:label ?tl FILTER(LANG(?tl)="en")}}
 OPTIONAL{{?i wdt:P2348 ?pe . ?pe rdfs:label ?pl FILTER(LANG(?pl)="en")}}
 OPTIONAL{{?i wdt:P131 ?a . ?a rdfs:label ?al FILTER(LANG(?al)="en")}}
}} GROUP BY ?i ?c'''
    u='https://qlever.dev/api/wikidata?'+urllib.parse.urlencode({'query':s})
    for t in range(4):
        try:
            r=urllib.request.Request(u,headers={'User-Agent':UA,'Accept':'application/sparql-results+json'})
            with urllib.request.urlopen(r,timeout=300) as f: return json.load(f)
        except Exception as e: print(cc,'err',e); time.sleep(10)
for cc in sys.argv[1:]:
    d=q(cc)
    if d: json.dump(d,open(f'{cc}.json','w')); print(cc,len(d['results']['bindings']))
    time.sleep(2)
