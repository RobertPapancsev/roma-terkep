# DARE HTML-adatlapok feldolgozása: külső hivatkozások, terület, alhelyek, pontosság, történeti nevek
import re,os,json,html,glob
D='/home/claude/dl/dare_html/'
def fix(s):
    s=html.unescape(s)
    for enc in ('latin-1','cp1252'):
        try: return s.encode(enc).decode('utf-8')
        except Exception: pass
    return s
def parse(t):
    r={};rows=re.findall(r"<tr><td>([^<]*)</td><td>(.*?)</td></tr>",t)
    links={}
    for k,v in rows:
        k=fix(k).strip();m=re.search(r"href='([^']*)'[^>]*>([^<]*)</a>",v);txt=fix(re.sub(r'<[^>]+>','',v)).strip()
        if k=='precision': r['prec']=txt
        elif k=='historical name(s)': r['hist']=txt
        elif k=='area': r['area']=txt
        elif k in('place type',):
            r['ptype']=txt
        elif k=='Late Roman province': r['lrp']=txt
        elif k.startswith('name:') and not m: r.setdefault('names',{})[k[5:]]=txt
        elif m: links.setdefault(k,[]).append([m.group(1),fix(m.group(2))])
    r['links']=links
    sub=re.search(r"contains the sites</em></td></tr>(.*?)<tr><td colspan='2'>",t,re.S)
    if sub: r['sub']=[[i,fix(n),fix(ty)] for i,n,ty in re.findall(r"places/(\d+)'>([^<]*)</a>\s*(?:&lt;([^&]*)&gt;)?",sub.group(1))]
    pa=re.search(r"is contained in.*?places/(\d+)'>([^<]*)</a>",t,re.S)
    if pa: r['parent']=[pa.group(1),fix(pa.group(2))]
    return r
if __name__=='__main__':
    out={}
    for f in glob.glob(D+'*.html'):
        i=os.path.basename(f)[:-5]
        try: out[i]=parse(open(f,encoding='utf-8',errors='replace').read())
        except Exception as e: print('ERR',i,e)
    json.dump(out,open('/home/claude/imperium/data/agg/dare_parsed.json','w'),ensure_ascii=False)
    import collections as C
    print(len(out),C.Counter(k for v in out.values() for k in v['links']).most_common(30))
    print('area',sum(1 for v in out.values() if v.get('area')),'sub',sum(1 for v in out.values() if v.get('sub')),'parent',sum(1 for v in out.values() if v.get('parent')))
    for i in ['10898','10899','10847']:
        if i in out: print(i,json.dumps(out[i],ensure_ascii=False)[:700])
