# v103: „Honnan jöttek a rómaiak?” kártya (ősi DNS + izotópok), Társadalom csoport
import shutil,sys
sys.path.insert(0,'src');import orig_card as A
p='body_v60pre.html';b=open(p,encoding='utf8').read();cp='style_v60pre.css';c=open(cp,encoding='utf8').read()
assert 'origcard' not in b
shutil.copy(p,'src/body_v60pre_before_v103.html');shutil.copy(cp,'src/style_v60pre_before_v103.css')
def rep(s,a,x):
    assert s.count(a)==1,(a[:60],s.count(a));return s.replace(a,x)
b=rep(b,'    <section class="card" id="bldcard">',A.build('hu')+'    <section class="card" id="bldcard">')
b=rep(b,'"Építkezések időrendben":"az','"Honnan jöttek a rómaiak?":"'+A.SUB[0]+'","Építkezések időrendben":"az')
b=rep(b,'      <li><b>Építkezések időrendben.</b>',A.SRCLI('hu')+'\n      <li><b>Építkezések időrendben.</b>')
b=rep(b,'listcard:"tars",','listcard:"tars",origcard:"tars",')
c=rep(c,'</style>','/* v103 */\n.origbar{margin:8px 0 4px}.regtab.origtab td:nth-child(2){text-align:right}.regtab.origtab td:nth-child(3){white-space:normal;text-align:left}.regtab.origtab th:nth-child(3){text-align:left}\n</style>')
open(p,'w',encoding='utf8').write(b);open(cp,'w',encoding='utf8').write(c)
t=open('src/patch_tabs.py',encoding='utf8').read()
if 'origcard' not in t: t=rep(t,'listcard:"tars",','listcard:"tars",origcard:"tars",');open('src/patch_tabs.py','w',encoding='utf8').write(t)
e=open('en/build.py',encoding='utf8').read()
if 'Honnan jöttek a rómaiak?' not in e: e=rep(e,'subs={"Éremkincsek','subs={"Honnan jöttek a rómaiak?":"'+A.SUB[1]+'","Éremkincsek');open('en/build.py','w',encoding='utf8').write(e)
print('ok')
