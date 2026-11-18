# v97: kereszt-összefüggések öt kártyán (src/xan_card.py)
import shutil,sys
sys.path.insert(0,'src');import xan_card as XC
p='body_v60pre.html';b=open(p,encoding='utf8').read()
assert 'A kereskedők a kőfeliratokon' not in b and 'class="hint srcl"' in b
shutil.copy(p,'src/body_v60pre_before_v97.html')
B=XC.build('hu')
def before(s,a,x):
    assert s.count(a)==1,(a[:50],s.count(a));return s.replace(a,x+a)
b=before(b,'      <h4 class="aqh4">Róma és a határvidék: hová jutottak ugyanannak a műhelynek az amforái</h4>',B['mer'])
b=before(b,'      <h3 class="aqh">A házasság hossza</h3>',B['age'])
b=before(b,'      <h3 class="aqh">Életkor: keresztény és korábbi sírfeliratok</h3>',B['season'])
b=before(b,'      <h3 class="aqh">A római kincsek egyenként</h3>',B['crisis'])
L=b.split('\n');i=[k for k,x in enumerate(L) if x.startswith('      <p class="hint">A kör a kerület egy biztosan')];assert len(i)==1
L.insert(i[0]+1,B['reg'].rstrip('\n'));b='\n'.join(L)
open(p,'w',encoding='utf8').write(b);print('ok')
