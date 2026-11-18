# v114: „Kik vezették a köztársaságot?” kártya (DPRR), Társadalom csoport
import shutil,sys
sys.path.insert(0,'src');import dprr_card as A
p='body_v60pre.html';b=open(p,encoding='utf8').read();cp='style_v60pre.css';c=open(cp,encoding='utf8').read()
assert 'dprrcard' not in b
shutil.copy(p,'src/body_v60pre_before_v114.html');shutil.copy(cp,'src/style_v60pre_before_v114.css')
def rep(s,a,x):
    assert s.count(a)==1,(a[:60],s.count(a));return s.replace(a,x)
b=rep(b,'    <section class="card" id="bldcard">',A.build('hu')+'    <section class="card" id="bldcard">')
b=rep(b,'"Építkezések időrendben":"az','"Kik vezették a köztársaságot? Tisztségviselők adatbázisa":"'+A.SUB[0]+'","Építkezések időrendben":"az')
b=rep(b,'      <li><b>Építkezések időrendben.</b>',A.SRCLI('hu')+'\n      <li><b>Építkezések időrendben.</b>')
b=rep(b,'dietcard:"tars",','dietcard:"tars",dprrcard:"tars",')
c=rep(c,'</style>','/* v114 */\n.dprow{display:flex;align-items:center;gap:8px;margin:3px 0}.dprow .dpl{flex:0 0 74px;font-size:.86em;text-align:right;white-space:nowrap}.dprow .dpl2{flex-basis:38%;white-space:normal;line-height:1.2}.dprow .dpbar{margin:0;min-width:34px}\n.regtab.dprrtab td,.regtab.dprrtab th{padding:5px 6px}.regtab.dprrtab td:first-child{text-align:left}.regtab.dprrtab td:nth-child(4),.regtab.dprrtab th:nth-child(4){white-space:normal;text-align:left}\n</style>')
open(p,'w',encoding='utf8').write(b);open(cp,'w',encoding='utf8').write(c)
t=open('src/patch_tabs.py',encoding='utf8').read()
if 'dprrcard' not in t: t=rep(t,'dietcard:"tars",','dietcard:"tars",dprrcard:"tars",');open('src/patch_tabs.py','w',encoding='utf8').write(t)
e=open('en/build.py',encoding='utf8').read()
if 'Kik vezették a köztársaságot?' not in e: e=rep(e,'subs={"','subs={"Kik vezették a köztársaságot? Tisztségviselők adatbázisa":"'+A.SUB[1]+'","');open('en/build.py','w',encoding='utf8').write(e)
print('ok')
