# v94: amforafeliratok II (β, célterületek, α) + a „Róma vízvezetékei” kártya átrendezése (adatok felül, felsorolás alul)
import shutil,sys
sys.path.insert(0,'src');import amph2_card as A2
p='body_v60pre.html';b=open(p,encoding='utf8').read();cp='style_v60pre.css';c=open(cp,encoding='utf8').read()
assert 'Kik szállították az olajat' not in b and 'Az amforafeliratok adatbázisa' in b
shutil.copy(p,'src/body_v60pre_before_v94.html');shutil.copy(cp,'src/style_v60pre_before_v94.css')
def rep(s,a,x):
    assert s.count(a)==1,(a[:60],s.count(a));return s.replace(a,x)
b=rep(b,'      <h3 class="aqh">A 3. század végén</h3>',A2.build('hu')+'      <h3 class="aqh">A 3. század végén</h3>')
# vízvezetékek: [bevezető, lista, fürdők] a kártya végére, új címmel
L=b.split('\n');i=next(k for k,x in enumerate(L) if x.strip()=='<h2>Róma vízvezetékei</h2>')
assert L[i+1].startswith('      <p class="hint">Frontinus, a vízügyek') and L[i+2].strip()=='<ol class="itin aqlist">'
j=next(k for k in range(i,len(L)) if L[k].strip()=='</ol>');assert L[j+1].startswith('      <p class="hint">A vezetékek által táplált fürdők')
e=next(k for k in range(i,len(L)) if L[k].strip()=='</section>')
lst=L[i+1:j+2];data=L[j+2:e]
assert data[0].startswith('      <h3 class="aqh">Hozam és elosztás')
L[i+1:e]=data+[LISTH]+lst if False else data+['      <h3 class="aqh">A tizenegy vezeték a térképen</h3>']+lst
b='\n'.join(L)
c=rep(c,'</style>','''/* v94 */
#foodcard .regtab .sub{opacity:.7;font-size:.92em}#foodcard .amphbars .sub i{font-style:italic}
</style>''')
open(p,'w',encoding='utf8').write(b);open(cp,'w',encoding='utf8').write(c);print('ok')
