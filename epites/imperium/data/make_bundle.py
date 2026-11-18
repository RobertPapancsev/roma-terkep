# v188: a kis kimutatás-adatfájlok összevonása egyetlen imp_st/b.json csomagba (fájlszám-korlát: 512).
# Az egyes fájlok helyben forrásként megmaradnak, de a műtárgyba csak a b.json kerül fel.
# A betöltő (imp_stats.js) BUN listájának egyeznie kell a lenti B listával.
import json, os
R='/home/claude/imperium/'
B=['leg23','leg220','nic','sonata','epi','pap','raad','iso','amph','orbis','insc','wrecks','clim2','clim','arena','mints2','battles']
b={k:json.load(open(R+f'imp_st/{k}.json')) for k in B}
json.dump(b,open(R+'imp_st/b.json','w'),ensure_ascii=False,separators=(',',':'))
print('b.json', os.path.getsize(R+'imp_st/b.json'), len(B),'fájl')
