# v89b: görög nyelvű feliratok feldolgozása (életkor, temetési dátum, tisztségek, formulák)
import re,unicodedata
def gclean(t):
    t=re.sub(r'=\s*/\s*','',t);t=re.sub(r'(?<=[^\s\-])-\s*/\s*(\[?)',r'\1',t)
    t=re.sub(r'(?<=[^\s\(\[])\[[\s\-–?]*\]',' ¤t ',t);t=re.sub(r'\[[\s\-–?]*\]',' ¤ ',t);t=re.sub(r'(?:-\s){2,}-',' ¤ ',t)
    t=unicodedata.normalize('NFD',t.lower());t=''.join(ch for ch in t if unicodedata.category(ch)!='Mn')
    t=t.replace('ς','σ').replace('ϛ','σ').replace('ϲ','σ')
    t=re.sub(r'\(\([^)]*\)\)',' ',t);t=re.sub(r'[\[\]\(\)<>{}`´?!+〚〛《》⌜⌝"ʹ΄\'᾿῾%0-9]','',t)
    t=re.sub(r'〈[^〉]*〉',' § ',t);t=re.sub(r'[/,.;:·\-=]+',' ',t);return re.sub(r'\s+',' ',t).strip()
U={'α':1,'β':2,'γ':3,'δ':4,'ε':5,'σ':6,'ζ':7,'η':8,'θ':9};TN={'ι':10,'κ':20,'λ':30,'μ':40,'ν':50,'ξ':60,'ο':70,'π':80,'ϙ':90}
GN=re.compile(r'^(ρ)?([ικλμνξοπϙ])?([αβγδεσζηθ])?$')
WD={'ενα':1,'μιαν':1,'ενοσ':1,'δυο':2,'δυω':2,'τρια':3,'τριων':3,'τρισ':3,'τεσσαρα':4,'τεσσερα':4,'τεσσαρων':4,'πεντε':5,'εξ':6,'επτα':7,'οκτω':8,'εννεα':9,'δεκα':10,'ενδεκα':11,'δωδεκα':12,'δυοδεκα':12,'δεκαπεντε':15,
 'εικοσι':20,'εικοσιν':20,'τριακοντα':30,'τριαντα':30,'τεσσαρακοντα':40,'τεσσερακοντα':40,'πεντηκοντα':50,'εξηκοντα':60,'εβδομηκοντα':70,'ογδοηκοντα':80,'ενενηκοντα':90}
V={'i':1,'v':5,'x':10,'l':50,'c':100}
def rom(s):
    t=0;mx=0
    for ch in reversed(s):
        v=V[ch]
        if v<mx:t-=v
        else:t+=v;mx=v
    return t
def num(toks):
    """A számot adja vissza a kezdő tokenekből, vagy None-t (hiány, nem szám)."""
    if not toks or toks[0].startswith('¤'):return None
    w=toks[0]
    if re.fullmatch(r'[ivxlc]+',w):return rom(w)
    if w in WD:
        v=WD[w]
        if v>=10 and len(toks)>1:
            w2=toks[2] if toks[1]=='και' and len(toks)>2 else toks[1]
            if w2 in WD and WD[w2]<10:v+=WD[w2]
        return v
    m=GN.match(w)
    if m and w:
        if len(toks)>1 and toks[1]=='¤t':return None   # csonka szám
        return (100 if m.group(1) else 0)+TN.get(m.group(2),0)+U.get(m.group(3),0)
    return None
AGEW=re.compile(r'\b(?:ετη|ετων|ετε|αιτη|ετεα|ετι|ετ)\b')   # az „ετουσ” (uralkodási év) nem életkor
MARW=re.compile(r'συν[εβ]|συμβιωσ|συνζησ|συζησ|μετ εμου|μετα του|μετα τησ|οικησασ|\bαπο$|\bαλλα$')
def ages(c):
    out=[]
    for m in AGEW.finditer(c):
        pre=' '.join(c[:m.start()].split()[-6:])
        if MARW.search(pre):continue          # együttélés hossza, nem életkor
        v=num(c[m.end():].split()[:3])
        if v and 0<v<=120:out.append(v)
    return out
GM=['ιανουαρ','φεβρ','μαρτ','απριλ','μαι','ιουν','ιουλ','αυγουστ','σεπτε','οκτω','νοε','δεκε']
GDATE=re.compile(r'(?:\b(προ) ([α-ω]+|[ivxlc]+) )?\b(καλανδ[α-ω]*|καλενδ[α-ω]*|ειδ[α-ω]*|ιδων|ιδοισ|νων[α-ω]*) ((?:'+'|'.join(GM)+r')[α-ω]*)')
DEATH=re.compile(r'καταθεσ|κατετεθη|εκοιμηθη|κοιμησ|ετελευτ|τελευτα|απεθαν|ανεπα|κατακ[ιε]τ|κειται|κιτε|απεδωκ|εξηλθ|ανελημφθη|ανεληφθη')
def month(c,hasage=False):
    if not (DEATH.search(c) or hasage):return None   # halál- vagy temetésige, vagy életkor a feliraton
    for m in GDATE.finditer(c):
        mi=[i for i,x in enumerate(GM) if m.group(4).startswith(x)][0]
        if m.group(4).startswith('μαι') and not re.match(r'μαι(?:ων|ασ|αισ|ου)?$',m.group(4)):continue
        if m.group(1):
            n=num([m.group(2)])
            if n is None:continue
            if m.group(3).startswith(('καλανδ','καλενδ')):mi=(mi-1)%12
        return mi
    return None
TIT={'episc':r'\bεπισκοπ|\bπαπα\b|\bπαπασ\b','presb':r'\bπρεσβυτερ|\bπρεσβ\b','diac':r'(?<!υπο)\bδιακον','subd':r'\bυποδιακον','acol':r'\bακολουθ','lect':r'\bαναγνωστ','exor':r'\bεξορκιστ','foss':r'\bκοπιατ|\bφοσσορ','neof':r'\bνεοφωτιστ|\bνεοφυτ','mart':r'\bμαρτυσ\b|\bμαρτυρ(?:οσ|ι|α|εσ|ων)\b'}
FORM={'pace':r'\bεν (?:ε?ιρην|ηρην)|\bιν πακε|\bεισ ειρην','dep':r'\bκαταθεσ|\bκατετεθη','locus':r'\bτοποσ\b','emit':r'\bηγορασ'}
