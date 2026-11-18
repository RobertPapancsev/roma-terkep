# Wikidata (CC0) SPARQL: a DARE által megadott Wikidata-elemek hu/en Wikipédia-cikke és képfájl-neve (P18)
import urllib.request,urllib.parse,json,time
D=json.load(open('/home/claude/imperium/data/agg/dare_parsed.json'))
Q=sorted({l[1].strip() for v in D.values() for l in v['links'].get('wikidata',[]) if l[1].strip().startswith('Q')})
out={};H={'User-Agent':'roman-map-research/1.0 (personal, non-commercial)','Accept':'application/sparql-results+json'}
PAT={'hu':'?a schema:about ?item; schema:isPartOf <https://hu.wikipedia.org/>.','en':'?a schema:about ?item; schema:isPartOf <https://en.wikipedia.org/>.','img':'?item wdt:P18 ?a.'}
def run(s):
    for t in range(5):
        try:
            req=urllib.request.Request('https://query.wikidata.org/sparql',data=urllib.parse.urlencode({'query':s}).encode(),headers=H)
            return json.loads(urllib.request.urlopen(req,timeout=90).read())['results']['bindings']
        except Exception as e: print('retry',t,e,flush=True);time.sleep(10*(t+1))
    raise SystemExit('fail')
for k in range(0,len(Q),200):
    vals=' '.join('wd:'+q for q in Q[k:k+200])
    for key,pat in PAT.items():
        for b in run('SELECT ?item ?a WHERE { VALUES ?item {%s} %s }'%(vals,pat)):
            q=b['item']['value'].rsplit('/',1)[1];o=out.setdefault(q,{});v=urllib.parse.unquote(b['a']['value'].rsplit('/',1)[1])
            if key not in o:o[key]=v.replace('_',' ') if key!='img' else v
        time.sleep(1)
    print(k,flush=True)
json.dump(out,open('/home/claude/imperium/data/agg/wikidata_by_q.json','w'),ensure_ascii=False)
print(len(Q),len(out),'hu',sum(1 for v in out.values() if 'hu' in v),'en',sum(1 for v in out.values() if 'en' in v),'img',sum(1 for v in out.values() if 'img' in v));print(out.get('Q623345'))
