# v110: „Árak és bérek 301-ben” kártya, Gazdaság csoport
import shutil,sys
sys.path.insert(0,'src');import price_card as A
p='body_v60pre.html';b=open(p,encoding='utf8').read();cp='style_v60pre.css';c=open(cp,encoding='utf8').read()
assert 'pricecard' not in b
shutil.copy(p,'src/body_v60pre_before_v110.html');shutil.copy(cp,'src/style_v60pre_before_v110.css')
def rep(s,a,x):
    assert s.count(a)==1,(a[:60],s.count(a));return s.replace(a,x)
b=rep(b,'    <section class="card" id="bldcard">',A.build('hu')+'    <section class="card" id="bldcard">')
b=rep(b,'"Építkezések időrendben":"az','"Árak és bérek 301-ben: Diocletianus árrendelete":"'+A.SUB[0]+'","Építkezések időrendben":"az')
b=rep(b,'      <li><b>Építkezések időrendben.</b>',A.SRCLI('hu')+'\n      <li><b>Építkezések időrendben.</b>')
b=rep(b,'chrecard:"gazd",','chrecard:"gazd",pricecard:"gazd",')
c=rep(c,'</style>','''/* v110: árrendelet */
#pricecard .prbars{margin:6px 0}#pricecard .pbr{display:flex;align-items:center;gap:6px;margin:2px 0;font-size:13px}#pricecard .pbl{width:44%;text-align:right;color:var(--ink,#333)}#pricecard .pbb{height:12px;background:#1f5fa8;border-radius:2px;min-width:2px}#pricecard .prbars.sea .pbb{background:#2f7fb8}#pricecard .pbn{font:12px var(--font-mono,monospace);color:var(--muted)}
#pricecard .regtab.prtab,#pricecard .regtab.prtab2{min-width:0;width:100%}#pricecard .prtab td:nth-child(3),#pricecard .prtab th:nth-child(3){white-space:normal;text-align:left}#pricecard .prtab td:first-child,#pricecard .prtab2 td:first-child{white-space:normal}
#pricecard .prtab2 th,#pricecard .prtab2 td{white-space:normal}#pricecard .prtab2 th,#pricecard .prtab2 td{padding:3px 5px}
</style>''')
open(p,'w',encoding='utf8').write(b);open(cp,'w',encoding='utf8').write(c)
t=open('src/patch_tabs.py',encoding='utf8').read()
if 'pricecard' not in t: t=rep(t,'chrecard:"gazd",','chrecard:"gazd",pricecard:"gazd",');open('src/patch_tabs.py','w',encoding='utf8').write(t)
e=open('en/build.py',encoding='utf8').read()
if 'Árak és bérek 301-ben' not in e: e=rep(e,'subs={"','subs={"Árak és bérek 301-ben: Diocletianus árrendelete":"'+A.SUB[1]+'","');open('en/build.py','w',encoding='utf8').write(e)
print('ok')
