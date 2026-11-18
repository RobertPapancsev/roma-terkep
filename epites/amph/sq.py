import sys,urllib.request,urllib.parse,json
EP='https://romanopendata.eu/sparql-endpoint'
def q(s,timeout=300):
    d=urllib.parse.urlencode({'query':s}).encode()
    r=urllib.request.Request(EP,data=d,headers={'Accept':'application/sparql-results+json','User-Agent':'Mozilla/5.0'})
    return json.load(urllib.request.urlopen(r,timeout=timeout))
def rows(s,**k):
    j=q(s,**k);v=j['head']['vars'];return [[b.get(x,{}).get('value') for x in v] for b in j['results']['bindings']]
if __name__=='__main__':
    for r in rows(sys.stdin.read()):print('\t'.join(str(x) for x in r))
