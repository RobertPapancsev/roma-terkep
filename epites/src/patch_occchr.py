# v91: keresztény feliratok foglalkozásai az occ-kártyán
import shutil,sys
sys.path.insert(0,'src');import occchr_card as OC
p='body_v60pre.html';b=open(p,encoding='utf8').read()
assert 'Foglalkozások a keresztény sírfeliratokon' not in b and 'listcard' in b
shutil.copy(p,'src/body_v60pre_before_v91.html')
a="      <h3 class=\"aqh\">Műhelyek és boltok címe</h3>"
assert b.count(a)==1
b=b.replace(a,OC.build('hu')+a)
open(p,'w',encoding='utf8').write(b);print('ok')
