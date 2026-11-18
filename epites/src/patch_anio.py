import shutil,sys
sys.path.insert(0,'src');import anio_card as A
p='body_v60pre.html';b=open(p,encoding='utf8').read();cp='style_v60pre.css';c=open(cp,encoding='utf8').read()
assert 'Mért hozam: az Anio Novus' not in b
shutil.copy(p,'src/body_v60pre_before_v101.html');shutil.copy(cp,'src/style_v60pre_before_v101.css')
def rep(s,a,x):
    assert s.count(a)==1,(a[:60],s.count(a));return s.replace(a,x)
k='      <h4 class="aqh4">A teljes kiosztás: 14 018 quinaria</h4>'
b=rep(b,k,A.build('hu')+k)
k='      <li><b>Építkezések időrendben.</b>'
b=rep(b,k,A.SRCLI('hu')+'\n'+k)
c=rep(c,'</style>','/* v101 */\n.regtab.aniotab{min-width:0;width:100%}.regtab.aniotab th,.regtab.aniotab td{padding:3px 5px}.regtab.aniotab td{white-space:normal;text-align:left;vertical-align:top}.regtab.aniotab td:nth-child(n+2){white-space:nowrap;text-align:right}.regtab.aniotab th:nth-child(n+2){white-space:normal;text-align:right}.regtab.aniotab th{text-align:left}\n</style>')
open(p,'w',encoding='utf8').write(b);open(cp,'w',encoding='utf8').write(c);print('ok')
