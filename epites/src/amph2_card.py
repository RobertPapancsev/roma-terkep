# v94: amforafeliratok II – kereskedők (β), a bélyegek célterületei, az üres amfora súlya (α). Adat: amph/extra.py -> amph/extra.json
import json
X=json.load(open('amph/extra.json'));BE=X['beta'];DE=X['dest'];AL=X['alpha']
GN={'caecil':('Caecilii','DD. Caeciliorum Hospitalis et Materni'),'ualer':('Valerii','C. Valeri Alexandri'),'iul':('Iulii','C. Iuli Alfi Thesei'),'anton':('Antonii','L. Antoni Plebeiani'),'cornel':('Cornelii','M. Corneli Ianuari'),'fad':('Fadii','Sex. Fadi Secundi'),
 'mar':('Marii','L. Mari Phoebi'),'claud':('Claudii','MM. Claudiorum Senecionum'),'pompe':('Pompeii','II Pompeiorum'),'memm':('Memmii','L. Memmi Berylli'),'litucc':('Lituccii','T. Litucci Sabini'),'uinis':('Vinisii','Q. Vinisi Sereni')}
def build(lang):
    hu=lang=='hu';t=lambda a,b:a if hu else b
    fmt=(lambda n:f'{n:,}'.replace(',',' ')) if hu else (lambda n:f'{n:,}')
    pc=lambda x:f'{x:.0f}'
    yr=lambda a,b:(f'Kr. u. {a}–{b}' if hu else f'AD {a}–{b}')
    k=BE['k'];read=k['priv']+k['fisc']+k['dom'];L=[]
    L.append('      <h4 class="aqh4">'+t('Kik szállították az olajat? A β sor','Who shipped the oil? The β line')+'</h4>')
    L.append('      <p class="hint">'+t(f'A β sorban annak a neve áll birtokos esetben, akié a szállítmány volt. A római Dressel 20 amforákról {fmt(BE["n"])} β feliratot ismer az adatbázis; ebből {fmt(read)} olvasható annyira, hogy besorolható: {fmt(k["priv"])} magánszemélyt vagy családot nevez meg ({BE["ngens"]} különböző család), {k["dom"]} a császárokat, {k["fisc"]} a császári pénztárat.',
      f'The β line gives, in the genitive, the name of whoever owned the consignment. The database knows {fmt(BE["n"])} β inscriptions from the Dressel 20 amphorae of Rome; {fmt(read)} of them can be read well enough to classify: {fmt(k["priv"])} name a private person or family ({BE["ngens"]} different families), {k["dom"]} the emperors and {k["fisc"]} the imperial treasury.')+'</p>')
    L.append('      <div class="regwrap"><table class="regtab insctab agetab">')
    L.append('        <thead><tr><th>'+t('Időszak','Period')+'</th><th>'+t('magánkereskedő','private merchant')+'</th><th>'+t('a császárok neve','the emperors’ names')+'</th><th>'+t('császári pénztár (fiscus)','imperial treasury (fiscus)')+'</th></tr></thead>')
    L.append('        <tbody>')
    for (a,b),c in zip(BE['per'],BE['bp']):
        L.append(f'          <tr><td>{yr(a,265 if b==267 else b)}</td><td class="pn">{c.get("priv",0)}</td><td class="pn">{c.get("dom",0)}</td><td class="pn">{c.get("fisc",0)}</td></tr>')
    L.append('        </tbody>')
    L.append('      </table></div>')
    bp=BE['bp'];df=BE['domf'];fp=BE['fiscp']
    L.append('      <p class="hint">'+t(f'A keltezhető feliratok éles váltást mutatnak. A 2. században mind a {bp[0]["priv"]} keltezett β felirat magánkereskedőt nevez meg. Septimius Severus alatt a helyükre a császárok neve kerül („dominorum nostrorum Severi et Antonini”, {df["two"]} feliraton; Getával együtt {df["three"]} feliraton). A 214-re keltezett rétegektől a „fisci rationis patrimoni provinciae Baeticae” formula áll a β sorban: a császári magánvagyon baeticai pénztára ({fp["baet"]} felirat; {fp["tarr"]} a Tarraconensisé). A 214–235 közötti rétegekből egyetlen magánkereskedő sincs. A 3. század közepén a magánnevek visszatérnek ({bp[3].get("priv",0)} felirat {bp[3].get("fisc",0)} pénztári mellett). Ez saját számokkal támasztja alá, amit a kártya fentebb Broekaert nyomán ír: a Severusok alatt az állam maga vette kézbe a szállítást.',
      f'The datable inscriptions show a sharp change. In the 2nd century all {bp[0]["priv"]} dated β inscriptions name a private merchant. Under Septimius Severus their place is taken by the names of the emperors (“dominorum nostrorum Severi et Antonini”, on {df["two"]} inscriptions; with Geta on {df["three"]}). From the layers dated to 214 onwards the β line carries the formula “fisci rationis patrimoni provinciae Baeticae”: the Baetican treasury of the emperor’s private estate ({fp["baet"]} inscriptions; {fp["tarr"]} of Tarraconensis). From the layers of 214–235 there is not a single private merchant. In the mid-3rd century private names return ({bp[3].get("priv",0)} inscriptions beside {bp[3].get("fisc",0)} of the treasury). This supports with our own figures what the card says above after Broekaert: under the Severans the state itself took the shipping in hand.')+'</p>')
    L.append('      <div class="foodest amphbars">')
    mx=BE['top'][0]['n']
    for g in BE['top']:
        nm,ex=GN[g['g']]
        L.append(f'        <div class="fe"><span class="fen">{nm} <span class="sub"><i lang="la">{ex}</i></span></span><span class="feb"><span style="width:{100*g["n"]/mx:.1f}%"></span></span><span class="fev">{g["n"]}</span></div>')
    L.append('      </div>')
    L.append('      <p class="hint">'+t('A leggyakoribb kereskedőcsaládok a római amforákon; dőlt betűvel egy-egy név úgy, ahogy az amforán áll. A családnév itt nem feltétlenül vérrokonságot jelent: a felszabadítottak volt uruk nevét viselték, és a nagy családnevek (Valerii, Iulii) több, egymástól független kereskedőt is takarhatnak. A számok a megmaradt és kiásott feliratokat mutatják, nem a forgalmat.',
      'The most frequent merchant families on the amphorae of Rome; in italics one name each as it stands on the amphora. A family name here does not necessarily mean kinship: freedmen bore the name of their former master, and the big family names (Valerii, Iulii) may cover several unrelated merchants. The numbers show the surviving and excavated inscriptions, not the turnover.')+'</p>')
    T=DE['tot'];al=T['roma']+T['rhen']+T['brit']+T['gall']
    L.append('      <h4 class="aqh4">'+t('Róma és a határvidék: hová jutottak ugyanannak a műhelynek az amforái','Rome and the frontier: where the amphorae of the same pottery ended up')+'</h4>')
    L.append('      <div class="regwrap"><table class="regtab insctab agetab">')
    L.append('        <thead><tr><th>'+t('Műhely (körzet)','Pottery (district)')+'</th><th>'+t('Róma','Rome')+'</th><th>'+t('Rajna-vidék','Rhineland')+'</th><th>Britannia</th><th>Gallia</th><th>'+t('Róma aránya','Share of Rome')+'</th></tr></thead>')
    L.append('        <tbody>')
    for w in DE['work']:
        nm=w['n'][0].upper()+w['n'][1:]
        L.append(f'          <tr><td>{nm} <span class="sub">({w["c"]})</span></td><td class="pn">{w["roma"]}</td><td class="pn">{w["rhen"]}</td><td class="pn">{w["brit"]}</td><td class="pn">{w["gall"]}</td><td class="pn">{pc(w["sh"])}%</td></tr>')
    L.append('        </tbody>')
    L.append('      </table></div>')
    cv=DE['conv'];cs=lambda c:pc(100*cv[c]['roma']/sum(cv[c].values()))
    L.append('      <p class="hint">'+t(f'Egy műhelyhez köthető bélyeges Dressel 20 amforák lelőhely szerint, a legalább 80 példánnyal képviselt műhelyekre; a Hispaniában talált darabok (a műhelyek saját hulladéka) kimaradnak. A „Rajna-vidék” a mai Németország, Svájc, Hollandia, Belgium, Luxemburg és Ausztria, „Gallia” a mai Franciaország. Összesen {fmt(al)} amfora, ennek {pc(100*T["roma"]/al)}%-a római. A cordubai körzet műhelyeinek bélyegei túlnyomórészt Rómában kerültek elő ({cs("Corduba")}%), a hispalisi és astigi műhelyekéi megoszlanak Róma és a provinciák között ({cs("Hispalis")}% és {cs("Astigi")}%). Néhány műhely, például Sevilla és Las Sesenta, alig van jelen Rómában.',
      f'Stamped Dressel 20 amphorae that can be tied to one pottery, by findspot, for potteries represented by at least 80 examples; pieces found in Hispania (the potteries’ own waste) are left out. “Rhineland” is today’s Germany, Switzerland, the Netherlands, Belgium, Luxembourg and Austria; “Gallia” is today’s France. {fmt(al)} amphorae in all, {pc(100*T["roma"]/al)}% of them from Rome. The stamps of the potteries of the district of Corduba were found overwhelmingly in Rome ({cs("Corduba")}%), those of Hispalis and Astigi are divided between Rome and the provinces ({cs("Hispalis")}% and {cs("Astigi")}%). A few potteries, such as Sevilla and Las Sesenta, are hardly present in Rome.')+'</p>')
    L.append('      <p class="hint">'+t('Ezt nem lehet egyszerűen úgy olvasni, hogy az egyik műhely Rómának, a másik a hadseregnek dolgozott. A római anyag zöme a Monte Testaccio 2–3. századi rétegeiből való, a rajnai és britanniai leletek között sok a korábbi; egy korán működő műhely ezért akkor is „provinciainak” látszik, ha annak idején Rómába is szállított. A számok a kutatás sűrűségétől is függnek.',
      'This cannot simply be read as one pottery working for Rome and another for the army. Most of the material from Rome comes from the 2nd–3rd-century layers of Monte Testaccio, while many of the finds from the Rhine and Britain are earlier; a pottery active early therefore looks “provincial” even if it also supplied Rome in its day. The numbers also depend on how intensively each area has been studied.')+'</p>')
    kg=lambda p:f'{p*0.327:.0f}'
    L.append('      <h4 class="aqh4">'+t('Az üres amfora súlya: az α sor','The weight of the empty amphora: the α line')+'</h4>')
    L.append('      <p class="hint">'+t(f'Az α sor az üres edény súlyát adja meg római fontban. Rómából {fmt(AL["nall"])} α feliratot ismerünk, de a szám csak {AL["n"]} amforán olvasható teljesen. A középérték {AL["med"]} font (kb. {kg(AL["med"])} kg), a felük {AL["q1"]} és {AL["q3"]} font közé esik. {AL["npair"]} amforán az α és a γ sor is ép: ezeken az edény a teli amfora súlyának átlagosan {pc(AL["ratio"])}%-át tette ki (középérték: {AL["pmed"][0]} font edény, {AL["pmed"][1]} font olaj). Ez megerősíti a fenti becslést: egy teli Dressel 20 nagyjából 100 kg volt, és ebből 30 kg az edény.',
      f'The α line gives the weight of the empty vessel in Roman pounds. {fmt(AL["nall"])} α inscriptions are known from Rome, but the number can be read in full on only {AL["n"]} amphorae. The median is {AL["med"]} pounds (about {kg(AL["med"])} kg) and half of them fall between {AL["q1"]} and {AL["q3"]} pounds. On {AL["npair"]} amphorae both the α and the γ line are intact: on these the vessel made up on average {pc(AL["ratio"])}% of the weight of the full amphora (medians: {AL["pmed"][0]} pounds of vessel, {AL["pmed"][1]} pounds of oil). This confirms the estimate above: a full Dressel 20 weighed roughly 100 kg, 30 kg of it the vessel.')+'</p>')
    return '\n'.join(L)+'\n'
if __name__=='__main__':
    import re;print(re.sub(r'<[^>]+>',' ',build('hu')))
