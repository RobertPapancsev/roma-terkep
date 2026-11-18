# v92: amforafeliratok (CEIPAC) a „Róma élelmezése” kártyán
import shutil,sys
sys.path.insert(0,'src');import amph_card as AC
p='body_v60pre.html';b=open(p,encoding='utf8').read();cp='style_v60pre.css';c=open(cp,encoding='utf8').read()
assert 'Az amforafeliratok adatbázisa' not in b and 'Foglalkozások a keresztény sírfeliratokon' in b
shutil.copy(p,'src/body_v60pre_before_v92.html');shutil.copy(cp,'src/style_v60pre_before_v92.css')
def rep(s,a,x):
    assert s.count(a)==1,(a[:60],s.count(a));return s.replace(a,x)
card,src=AC.build('hu')
b=rep(b,'      <h3 class="aqh">A 3. század végén</h3>',card+'      <h3 class="aqh">A 3. század végén</h3>')
b=rep(b,'      <li><b>Építkezések időrendben.</b>',src+'\n      <li><b>Építkezések időrendben.</b>')
c=rep(c,'</style>','''/* v92: amforafeliratok */
#foodcard .amphbars .fe{grid-template-columns:minmax(0,1.3fr) minmax(80px,1.4fr) 3.2em}#foodcard .amphbars .fev{text-align:right}#foodcard .amphbars .sub{opacity:.7;font-size:.92em}
</style>''')
open(p,'w',encoding='utf8').write(b);open(cp,'w',encoding='utf8').write(c);print('ok')
