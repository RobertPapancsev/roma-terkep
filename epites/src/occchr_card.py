# v91: a „Foglalkozások a feliratokon” kártya kiegészítése – keresztény feliratok (EDB). Adat: occ/chr.py, occ/chrex.py -> occ/chr.json
import json,sys
sys.path.insert(0,'occ');import lex
D=json.load(open('occ/chr.json'));NM={k:(h,e) for k,l,rx,h,e,s in lex.L}
def build(lang):
    hu=lang=='hu';t=lambda a,b:a if hu else b
    fmt=(lambda n:f'{n:,}'.replace(',',' ')) if hu else (lambda n:f'{n:,}')
    d1=lambda x:(f'{x:.1f}'.replace('.',',') if hu else f'{x:.1f}')
    E=D['edr'];a=100*E['nocc']/E['ntext'];b=100*D['nocc']/D['ntext'];le,lb=D['long']['edr'],D['long']['edb'];la=100*le[1]/le[0];lbb=100*lb[1]/lb[0]
    L=[]
    L.append('      <h3 class="aqh">'+t('Foglalkozások a keresztény sírfeliratokon','Occupations in the Christian epitaphs')+'</h3>')
    L.append('      <div class="regwrap"><table class="regtab insctab agetab">')
    L.append('        <thead><tr><th></th><th>'+t('Az EDR feliratai','Inscriptions in EDR')+'</th><th>'+t('Keresztény feliratok (EDB)','Christian inscriptions (EDB)')+'</th></tr></thead>')
    L.append('        <tbody>')
    for lab,x,y in [(t('Olvasható latin szöveg','Readable Latin texts'),fmt(E['ntext']),fmt(D['ntext'])),(t('Foglalkozást megnevező felirat','Inscriptions naming an occupation'),fmt(E['nocc']),str(D['nocc'])),(t('Arány','Share'),d1(a)+'%',d1(b)+'%'),
                    (t('Arány a legalább 40 betűs szövegek között','Share among texts of at least 40 letters'),d1(la)+'%',d1(lbb)+'%')]:
        L.append(f'          <tr><td>{lab}</td><td class="pn">{x}</td><td class="pn">{y}</td></tr>')
    L.append('        </tbody>')
    L.append('      </table></div>')
    top=', '.join(f'{NM[k][0 if hu else 1]} ({n})' for k,n in D['top'][:6])
    L.append('      <p class="hint">'+t(f'A 3–8. századi keresztény sírfeliratok szinte soha nem nevezik meg az elhunyt foglalkozását: ugyanazzal a szótárral és ugyanazokkal a szabályokkal a szövegek {d1(b)}%-án találtunk foglalkozásnevet, az EDR jórészt korábbi, nem keresztény feliratain {d1(a)}%-án. A különbség nem csak a rövidebb keresztény szövegekből adódik: a legalább 40 betűs szövegek között is {d1(lbb)}% áll {d1(la)}%-kal szemben. A keresztény feliratok mind a {D["nread"]} találatát egyenként átolvastuk, {D["nex"]} téves vagy bizonytalan találat kimaradt (például a „mensorum”, amely itt a hónapok romlott alakja, nem földmérő). A leggyakoribbak: {top}. A görög szövegeket ez a latin szótár nem vizsgálja.',
      f'The Christian epitaphs of the 3rd–8th centuries almost never name the occupation of the deceased: with the same lexicon and the same rules we found an occupational title in {d1(b)}% of the texts, against {d1(a)}% in the mostly earlier, non-Christian inscriptions of EDR. The difference does not come only from the shorter Christian texts: among texts of at least 40 letters it is still {d1(lbb)}% against {d1(la)}%. All {D["nread"]} hits in the Christian inscriptions were read one by one, and {D["nex"]} false or uncertain hits were left out (for example “mensorum”, here a corrupt form of “months”, not a surveyor). The most frequent: {top}. The Greek texts are not covered by this Latin lexicon.')+'</p>')
    return '\n'.join(L)+'\n'
if __name__=='__main__':
    import re
    for l in('hu','en'):print(re.sub(r'<[^>]+>',' ',build(l)))
