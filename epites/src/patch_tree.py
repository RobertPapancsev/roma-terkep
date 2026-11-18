# v113: „Éghajlat az évgyűrűkből” kártya (Büntgen et al. 2011), Gazdaság csoport
import shutil,sys
sys.path.insert(0,'src');import tree_card as A
p='body_v60pre.html';b=open(p,encoding='utf8').read();cp='style_v60pre.css';c=open(cp,encoding='utf8').read()
assert 'treecard' not in b
shutil.copy(p,'src/body_v60pre_before_v113.html');shutil.copy(cp,'src/style_v60pre_before_v113.css')
def rep(s,a,x):
    assert s.count(a)==1,(a[:60],s.count(a));return s.replace(a,x)
b=rep(b,'    <section class="card" id="bldcard">',A.build('hu')+'    <section class="card" id="bldcard">')
b=rep(b,'"Építkezések időrendben":"az','"Éghajlat az évgyűrűkből: nyarak az Alpoktól északra":"'+A.SUB[0]+'","Építkezések időrendben":"az')
b=rep(b,'      <li><b>Építkezések időrendben.</b>',A.SRCLI('hu')+'\n      <li><b>Építkezések időrendben.</b>')
b=rep(b,'shipcard:"gazd",','shipcard:"gazd",treecard:"gazd",')
c=rep(c,'</style>','/* v113 */\n.treesvg{width:100%;height:auto;display:block;margin:4px 0 2px}.treesvg text{fill:currentColor}.treesvg .tax{font-size:14px;opacity:.8}\n.regtab.treetab td,.regtab.treetab th{padding:5px 6px;white-space:normal}.regtab.treetab td:first-child{white-space:nowrap;text-align:left}\n</style>')
open(p,'w',encoding='utf8').write(b);open(cp,'w',encoding='utf8').write(c)
t=open('src/patch_tabs.py',encoding='utf8').read()
if 'treecard' not in t: t=rep(t,'shipcard:"gazd",','shipcard:"gazd",treecard:"gazd",');open('src/patch_tabs.py','w',encoding='utf8').write(t)
e=open('en/build.py',encoding='utf8').read()
if 'Éghajlat az évgyűrűkből' not in e: e=rep(e,'subs={"','subs={"Éghajlat az évgyűrűkből: nyarak az Alpoktól északra":"'+A.SUB[1]+'","');open('en/build.py','w',encoding='utf8').write(e)
print('ok')
