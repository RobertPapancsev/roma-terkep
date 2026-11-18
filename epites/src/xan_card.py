# v97: kereszt-összefüggések öt kártyán. Adat: xan/calc.py -> xan/data.json
import json
X=json.load(open('xan/data.json'))
SL=lambda hu,en,l:'      <p class="hint srcl"><b>'+('Forrás:' if l=='hu' else 'Source:')+'</b> '+(hu if l=='hu' else en)+'</p>'
MR=[('phoebus','L. Marius Phoebus','Róma','Rome','„a Baetica provinciából való hispán olaj kereskedője” (<i lang="la">mercator olei Hispani ex provincia Baetica</i>), a néptribunusok hivatalszolgája','“merchant of Spanish oil from the province of Baetica” (<i lang="la">mercator olei Hispani ex provincia Baetica</i>), attendant of the tribunes of the plebs'),
 ('onesimus','D. Caecilius Onesimus','Róma','Rome','„baeticai olajszállító” (<i lang="la">diffusor olearius ex Baetica</i>), császári hivatalszolga','“oil shipper from Baetica” (<i lang="la">diffusor olearius ex Baetica</i>), imperial attendant'),
 ('hospitalis','D. Caecilius Hospitalis, D. Caecilius Maternus','Astigi (Écija)','Astigi (Écija)','D. Caecilius Hospitalis és Caecilia Materna örökösként ezüstszobrot állít','D. Caecilius Hospitalis and Caecilia Materna set up a silver statue as heirs'),
 ('hermes','M. Iulius Hermes','Astigi és Hispalis','Astigi and Hispalis','M. Iulius Hermes Frontinianus szobrot állít apjának, M. Iulius Hermesianusnak, aki olajszállító volt „a város élelmezésére”, és az olajosok testületének elöljárója','M. Iulius Hermes Frontinianus sets up a statue to his father M. Iulius Hermesianus, an oil shipper “for the food supply of the City” and head of the corporation of oil dealers'),
 ('fadius','Sex. Fadius Secundus','Narbo (Narbonne), Kr. u. 149','Narbo (Narbonne), AD 149','Sex. Fadius Secundus Musa a város minden tisztségét viselte, az ácsok testületének patrónusa','Sex. Fadius Secundus Musa held every office of the town and was patron of the carpenters’ guild'),
 ('olitius','P. Olitius Apollonius','Narbo (Narbonne)','Narbo (Narbonne)','hajótulajdonos (<i lang="la">navicularius</i>), a császárkultusz papi testületének tagja','shipowner (<i lang="la">navicularius</i>), member of the priesthood of the imperial cult')]
AG=[('fil','szabad születésű (az apa nevével)','freeborn (with the father’s name)'),('lib','felszabadított','freed'),('mil','katona','soldier'),('ser','rabszolga','slave'),('patron','patrónus','patron'),('sex_f','nő','women'),('sex_m','férfi','men'),
 ('t0','Kr. u. 50 előtt','before AD 50'),('t1','Kr. u. 50–150','AD 50–150'),('t2','Kr. u. 150 után','after AD 150')]
def build(lang):
    hu=lang=='hu';t=lambda a,b:a if hu else b
    fmt=(lambda n:f'{n:,}'.replace(',',' ')) if hu else (lambda n:f'{n:,}')
    d1=lambda x:(f'{x:.1f}'.replace('.',',') if hu else f'{x:.1f}')
    pc=lambda x:f'{x:.0f}'
    B={}
    # 1. kereskedők
    L=['      <h4 class="aqh4">'+t('A kereskedők a kőfeliratokon','The merchants in stone inscriptions')+'</h4>']
    L.append('      <div class="regwrap"><table class="regtab insctab">')
    L.append('        <thead><tr><th>'+t('Név az amforákon','Name on the amphorae')+'</th><th>'+t('Amfora Rómában','Amphorae in Rome')+'</th><th>'+t('Kőfelirat','Stone inscription')+'</th><th>'+t('Mit mond róla','What it says')+'</th></tr></thead>')
    L.append('        <tbody>')
    for k,nm,ph,pe,dh,de in MR:
        m=X['mer'][k];y=(t(f', {m["y"][0]}–{m["y"][1]}',f', {m["y"][0]}–{m["y"][1]}') if m['y'] else t(', keltezés nélkül',', undated'))
        ids=', '.join(s['id'] for s in m['stone'])
        L.append(f'          <tr><td><i lang="la">{nm}</i></td><td class="pn">{m["n"]}{y}</td><td>{ph if hu else pe}<br><span class="sub">{ids}</span></td><td>{dh if hu else de}</td></tr>')
    L.append('        </tbody>');L.append('      </table></div>')
    L.append(SL('CEIPAC – Roman Open Data és LIST v1.2 (az EDCS szövegei), saját összevetés.','CEIPAC – Roman Open Data and LIST v1.2 (texts of EDCS), our own comparison.',lang))
    L.append('      <p class="hint">'+t('Az amforákra festett nevek közül hatot a birodalom kőfeliratain is megtaláltunk, a latin feliratok adatbázisában keresve. Ketten Rómában nevezik magukat baeticai olajkereskedőnek, kettő családja a termelővidéken, Astigiben és Hispalisban állít szobrot, ketten Narbo kikötővárosának előkelői. Az amforák és a kőfeliratok kora, ahol mindkettő ismert, egyezik: Sex. Fadius Secundus narbói felirata 149-ből való, az amforái 146 és 161 közöttiek. Ezek az azonosítások a kutatásban ismertek; itt a két adatbázis összekapcsolása önállóan adta ki őket. A gyakori nevű kereskedők (például C. Valerius Alexander) nem azonosíthatók, ezért kimaradtak.',
      'Six of the names painted on the amphorae were also found in the stone inscriptions of the empire, by searching the database of Latin inscriptions. Two call themselves merchants of Baetican oil in Rome, the families of two set up statues in the producing region, at Astigi and Hispalis, and two are notables of the port town of Narbo. Where both are known, the dates of the amphorae and of the stones agree: the inscription of Sex. Fadius Secundus at Narbo is of 149, his amphorae of 146–161. These identifications are known to scholarship; here the linking of the two databases produced them independently. Merchants with common names (for example C. Valerius Alexander) cannot be identified and were left out.')+'</p>')
    B['mer']='\n'.join(L)+'\n'
    # 2. életkor
    a=X['age'];L=['      <h3 class="aqh">'+t('Ki tudta pontosan a korát?','Who knew their exact age?')+'</h3>']
    L.append('      <div class="regwrap"><table class="regtab insctab agetab">')
    L.append('        <thead><tr><th>'+t('Csoport','Group')+'</th><th>'+t('Életkor-adat','Ages given')+'</th><th>'+t('Középérték','Median')+'</th><th>'+t('23–62 éves','Aged 23–62')+'</th><th>'+t('Whipple-index','Whipple index')+'</th></tr></thead>')
    L.append('        <tbody>')
    for k,h,e in AG:
        v=a[k];L.append(f'          <tr><td>{h if hu else e}</td><td class="pn">{fmt(v["n"])}</td><td class="pn">'+t(f'{v["med"]} év',f'{v["med"]} years')+f'</td><td class="pn">{fmt(v["nad"])}</td><td class="pn">{v["w"]}</td></tr>')
    L.append('        </tbody>');L.append('      </table></div>')
    L.append(SL('Epigraphic Database Roma (EDR), saját összesítés.','Epigraphic Database Roma (EDR), our own summary.',lang))
    L.append('      <p class="hint">'+t(f'A kerek életkorok torlódása csoportonként eltér. A szabad születésűek feliratain a legkisebb ({a["fil"]["w"]}), a rabszolgákén és a patrónusokén a legnagyobb ({a["ser"]["w"]} és {a["patron"]["w"]}); a felszabadítottak és a katonák a kettő között állnak. Időben a kerekítés csökken: a Kr. u. 50 előtti feliratokon {a["t0"]["w"]}, a 150 utániakon {a["t2"]["w"]}. A csoportot a szöveg jelölései adják (libertus, servus vagy verna, katonai megnevezés, az apa neve), egy életkort közlő feliratokon; a patrónus sorban az a felirat áll, amelyet valaki a patrónusának állított. A rabszolgák és a patrónusok sora 23–62 éves korban csak {a["ser"]["nad"]}, illetve {a["patron"]["nad"]} adaton alapul, ezért ott az index csak irányt mutat.',
      f'The heaping of round ages differs by group. It is lowest in the inscriptions of the freeborn ({a["fil"]["w"]}) and highest in those of slaves and patrons ({a["ser"]["w"]} and {a["patron"]["w"]}); the freed and the soldiers stand between the two. Over time rounding decreases: {a["t0"]["w"]} in inscriptions before AD 50, {a["t2"]["w"]} after 150. The group is given by markers in the text (libertus, servus or verna, a military term, the father’s name), in inscriptions giving one age; the patron row holds inscriptions set up by someone to their patron. The rows of slaves and patrons rest on only {a["ser"]["nad"]} and {a["patron"]["nad"]} ages between 23 and 62, so there the index shows only a direction.')+'</p>')
    B['age']='\n'.join(L)+'\n'
    # 3. évszak és életkor
    s=X['season'];sh=lambda k:pc(100*s[k]['k']/s[k]['n']);ntot=s['a']['n']+s['b']['n']+s['c']['n']
    L=['      <h4 class="aqh4">'+t('Kit vitt el a késő nyár?','Whom did late summer carry off?')+'</h4>']
    L.append('      <div class="regwrap"><table class="regtab insctab agetab">')
    L.append('        <thead><tr><th>'+t('Életkor','Age')+'</th><th>'+t('Felirat','Inscriptions')+'</th><th>'+t('Temetés augusztus és október között','Burial between August and October')+'</th></tr></thead>')
    L.append('        <tbody>')
    for k,h,e in (('a','10 év alatt','under 10'),('b','10–29 év','10–29'),('c','30 év és fölötte','30 and over')):
        L.append(f'          <tr><td>{h if hu else e}</td><td class="pn">{s[k]["n"]}</td><td class="pn">{s[k]["k"]} ({sh(k)}%)</td></tr>')
    L.append('        </tbody>');L.append('      </table></div>')
    L.append(SL('Epigraphic Database Bari (EDB), saját összesítés.','Epigraphic Database Bari (EDB), our own summary.',lang))
    L.append('      <p class="hint">'+t(f'{ntot} latin feliraton olvasható egyszerre az elhunyt életkora és a temetés hónapja. Ha a temetések egyenletesen oszlanának el, a három hónapra 25% jutna. A 10 és 29 év közöttieknél ez {sh("b")}%, a 30 év fölöttieknél {sh("c")}%; ekkora különbség véletlenül nagyjából százból egyszer adódna (p = {d1(s["p"]*100)}%). A késő nyári halálozás tehát a fiatal felnőtteket sújtotta leginkább. Ez egybevág azzal, amit a kutatás a malária mellett szokott felhozni, de a halál okát a feliratok nem mondják meg.',
      f'In {ntot} Latin inscriptions both the age of the deceased and the month of burial can be read. If burials were evenly spread, the three months would hold 25%. For those between 10 and 29 it is {sh("b")}%, for those over 30 {sh("c")}%; a difference of this size would arise by chance about once in a hundred (p = {d1(s["p"]*100)}%). Late-summer mortality thus hit young adults hardest. This agrees with what scholarship adduces in favour of malaria, but the inscriptions do not state the cause of death.')+'</p>')
    B['season']='\n'.join(L)+'\n'
    # 4. kerületek
    r=X['reg'];f2=lambda x:(f'{x:.2f}'.replace('.',',') if hu else f'{x:.2f}')
    B['reg']='      <p class="hint">'+t(f'A kerületek számai össze is függnek. Ahol több a bérház, ott több a fürdő (rangkorreláció: {f2(r["ins_bal"])}), és ahol több a kút, ott több a pékség ({f2(r["lac_pis"])}). A bérházak száma azzal is együtt jár, hogy Frontinus szerint Kr. u. 97-ben hány vízvezeték látta el a kerületet ({f2(r["aq_ins"])}). Tizennégy kerületnél a 0,54 fölötti érték már aligha véletlen. Óvatosságra int, hogy a jegyzék számai részben sematikusak (a pékségeké többnyire 15, 16 vagy 20), és Frontinus adata két és fél évszázaddal korábbi.',
      f'The figures of the regions are also related. Where there are more apartment blocks there are more baths (rank correlation: {f2(r["ins_bal"])}), and where there are more fountains there are more bakeries ({f2(r["lac_pis"])}). The number of apartment blocks also goes with the number of aqueducts that supplied the region in AD 97 according to Frontinus ({f2(r["aq_ins"])}). With fourteen regions a value above 0.54 is unlikely to be chance. Caution is needed because the figures of the catalogue are partly schematic (those of the bakeries are mostly 15, 16 or 20) and Frontinus’ data are two and a half centuries earlier.')+'</p>\n'
    # 5. 250–275
    c=X['crisis']
    B['crisis']='      <p class="hint">'+t(f'A 250 és 275 közötti negyedszázad a térkép más adatsoraiban is mélypont. Rómában az ásatások keltezett építési fázisaiból ekkor {c["sitar"]} ismert (a Kr. u. 75–100 közötti csúcson {c["sitar_max"]}), és az EDR feliratainak száma a 2. századi átlag harmadára esik ({fmt(c["insc"])} a {fmt(c["insc_2c"])} helyett). Három, egymástól független adatsor mutatja ugyanazt az időszakot; okot ez nem bizonyít, mert mindegyik sornak megvan a maga hosszú távú iránya.',
      f'The quarter-century between 250 and 275 is a low point in the map’s other data series as well. In Rome only {c["sitar"]} dated construction phases from excavations are known from this time ({c["sitar_max"]} at the peak of AD 75–100), and the number of inscriptions in EDR falls to a third of the 2nd-century average ({fmt(c["insc"])} instead of {fmt(c["insc_2c"])}). Three independent data series point to the same period; this proves no cause, because each series has its own long-term trend.')+'</p>\n'
    return B
if __name__=='__main__':
    import re
    for k,v in build('hu').items():print(k,re.sub(r'<[^>]+>',' ',v)[:1500],'\n')
