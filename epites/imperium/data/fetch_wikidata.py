# Wikidata (CC0): minden Pleiades-azonosítós elem magyar és angol Wikipédia-cikke és képe (P18)
import urllib.request,urllib.parse,json
Q='''SELECT ?item ?pl ?hu ?en ?img WHERE { ?item wdt:P1584 ?pl .
 OPTIONAL { ?hu schema:about ?item ; schema:isPartOf <https://hu.wikipedia.org/> . }
 OPTIONAL { ?en schema:about ?item ; schema:isPartOf <https://en.wikipedia.org/> . }
 OPTIONAL { ?item wdt:P18 ?img . } }'''
u='https://query.wikidata.org/sparql?format=json&query='+urllib.parse.quote(Q)
r=json.loads(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'roman-map-research/1.0 (personal, non-commercial)'}),timeout=300).read())
out={}
for b in r['results']['bindings']:
    pl=b['pl']['value'];q=b['item']['value'].rsplit('/',1)[1]
    o=out.setdefault(pl,{'q':q})
    if 'hu' in b: o['hu']=urllib.parse.unquote(b['hu']['value'].rsplit('/wiki/',1)[1])
    if 'en' in b: o['en']=urllib.parse.unquote(b['en']['value'].rsplit('/wiki/',1)[1])
    if 'img' in b and 'img' not in o: o['img']=urllib.parse.unquote(b['img']['value'].rsplit('/',1)[1])
json.dump(out,open('/home/claude/imperium/data/agg/wikidata_by_pleiades.json','w'),ensure_ascii=False)
print(len(out),'hu',sum(1 for v in out.values() if 'hu' in v),'en',sum(1 for v in out.values() if 'en' in v),'img',sum(1 for v in out.values() if 'img' in v))
print(out.get('197130'))
