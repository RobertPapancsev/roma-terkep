# v112: „Mit ettek a rómaiak?” kártya (étrendi izotópok), Társadalom csoport
import shutil,sys
sys.path.insert(0,'src');import diet_card as A
p='body_v60pre.html';b=open(p,encoding='utf8').read();cp='style_v60pre.css';c=open(cp,encoding='utf8').read()
assert 'dietcard' not in b
shutil.copy(p,'src/body_v60pre_before_v112.html');shutil.copy(cp,'src/style_v60pre_before_v112.css')
def rep(s,a,x):
    assert s.count(a)==1,(a[:60],s.count(a));return s.replace(a,x)
b=rep(b,'    <section class="card" id="bldcard">',A.build('hu')+'    <section class="card" id="bldcard">')
b=rep(b,'"Építkezések időrendben":"az','"Mit ettek a rómaiak? Étrend a csontokból":"'+A.SUB[0]+'","Építkezések időrendben":"az')
b=rep(b,'      <li><b>Építkezések időrendben.</b>',A.SRCLI('hu')+'\n      <li><b>Építkezések időrendben.</b>')
b=rep(b,'origcard:"tars",','origcard:"tars",dietcard:"tars",')
c=rep(c,'</style>','/* v112 */\n.dietsvg{width:100%;height:auto;display:block;margin:6px 0 2px}.dietsvg text{fill:currentColor}.dietsvg .dax{font-size:14px;opacity:.75}.dietsvg .dlb{font-size:15px}\n.regtab.diettab td:first-child{white-space:normal;text-align:left}.regtab.diettab td,.regtab.diettab th{padding:5px 6px}\n</style>')
open(p,'w',encoding='utf8').write(b);open(cp,'w',encoding='utf8').write(c)
t=open('src/patch_tabs.py',encoding='utf8').read()
if 'dietcard' not in t: t=rep(t,'origcard:"tars",','origcard:"tars",dietcard:"tars",');open('src/patch_tabs.py','w',encoding='utf8').write(t)
e=open('en/build.py',encoding='utf8').read()
if 'Mit ettek a rómaiak?' not in e: e=rep(e,'subs={"','subs={"Mit ettek a rómaiak? Étrend a csontokból":"'+A.SUB[1]+'","');open('en/build.py','w',encoding='utf8').write(e)
print('ok')
