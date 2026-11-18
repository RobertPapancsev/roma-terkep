# v75: negyedik regényséta: Colleen McCullough, Róma első embere (1990; magyarul Árkádia, 1991). Előtte: src/novel_fmr.py
import json,re,shutil,sys
sys.path.insert(0,'src');from novel_fmr import FMR as Q
p='body_v60pre.html';b=open(p,encoding='utf8').read()
assert '"id":"fmr"' not in b
shutil.copy(p,'src/body_v60pre_before_v75.html')
def rep(s,a,x,n=1):
    assert s.count(a)==n,(a[:60],s.count(a));return s.replace(a,x)
m=re.search(r'^const WALKS=(\[.*\]);$',b,re.M);W=json.loads(m.group(1))
W.append({"id":Q["id"],"nov":1,"t":Q["t"],"intro":Q["intro"],"s":[{"id":i,"h":h,"x":x} for i,h,x in Q["s"]]})
b=b[:m.start()]+'const WALKS='+json.dumps(W,ensure_ascii=False,separators=(',',':'))+';'+b[m.end():]
b=rep(b,'Lactantius, <i>De mortibus persecutorum</i> 13.</li>',
'Lactantius, <i>De mortibus persecutorum</i> 13. Colleen McCullough, <i>Róma első embere</i> (<i>The First Man in Rome</i>, 1990), ford. Dániel Anna és mások, Árkádia, Budapest 1991, I–II. kötet; a hivatkozás a kötet- és oldalszám. A regényen kívüli megjegyzések: Sallustius, <i>Iugurtha háborúja</i> 35, 73, 86; Plutarkhosz, <i>Marius</i> 12, 29; Appianosz, <i>A polgárháborúk</i> 1.28–32; Orosius 5.17; Cicero, <i>De domo sua</i> 102, <i>De oratore</i> 2.197–203; Suetonius, <i>Divus Iulius</i> 46.</li>')
open(p,'w',encoding='utf8').write(b);print('ok')
