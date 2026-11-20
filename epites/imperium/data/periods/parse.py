import re, json, html, unicodedata
REIGN = {  # kulcs: (uralkodás kezdete, vége)
 'augusteisch': (-27, 14), 'augusteische': (-27, 14), 'tiberisch': (14, 37), 'caliguläisch': (37, 41), 'claudisch': (41, 54), 'neronisch': (54, 68),
 'flavisch': (69, 96), 'vespasianisch': (69, 79), 'titus': (79, 81), 'domitianisch': (81, 96), 'nervanisch': (96, 98),
 'trajanisch': (98, 117), 'traianisch': (98, 117), 'hadrianisch': (117, 138), 'antoninisch': (138, 161), 'antoninianisch': (138, 161),
 'markaurelisch': (161, 180), 'commodianisch': (180, 192), 'severisch': (193, 235), 'gallienisch': (253, 268), 'aurelianisch': (270, 275),
 'diokletianisch': (284, 305), 'diocletianisch': (284, 305), 'tetrarchisch': (293, 305), 'tetrarchie': (293, 305), 'konstantinisch': (306, 337),
 'constantinisch': (306, 337), 'valentinianisch': (364, 375), 'theodosianisch': (379, 395),
}
def clean(s):
    s = re.sub(r'<ref[^>]*/>', '', s); s = re.sub(r'<ref[^>]*>.*?</ref>', '', s, flags=re.S)
    s = re.sub(r'\[\[(?:[^|\]]*\|)?([^\]]*)\]\]', r'\1', s); s = s.replace('&nbsp;', ' ').replace(' ', ' ')
    s = re.sub(r"'{2,}", '', s); s = re.sub(r'\{\{[^}]*\}\}', '', s)
    return s
def cent(txt, side):
    # évszázad-kifejezések pontosítóval; csupasz évszázadnál None
    t = txt.lower()
    vals = []
    for m in re.finditer(r'(anfang|früh\w*|mitte|ende|spät\w*|1\. hälfte|2\. hälfte|erste[n]? hälfte|zweite[n]? hälfte|letzte[sn]? drittel|ersten drittel|1\. drittel|2\. drittel|3\. viertel)\s*(?:des|der)?\s*(\d)\.\s*(?:jh|jahrh)', t):
        q, n = m.group(1), int(m.group(2)); base = 100 * (n - 1); v = None
        if q.startswith(('anfang', 'früh')): v = base + (10 if side == 's' else 30)
        elif q == 'mitte': v = base + 50
        elif q.startswith(('ende', 'spät')): v = base + (90 if side == 's' else 100)
        elif '1.' in q or 'erste' in q: v = base + (1 if side == 's' else 50)
        elif ('2.' in q and 'hälfte' in q) or 'zweite' in q: v = base + (51 if side == 's' else 100)
        elif 'letzte' in q: v = base + (67 if side == 's' else 100)
        elif 'drittel' in q: v = base + (1 if side == 's' else 33)
        elif 'viertel' in q: v = base + (51 if side == 's' else 75)
        if v is not None: vals.append(v)
    if not vals: return None
    return min(vals) if side == 's' else max(vals)
def years(txt):
    out = []
    for m in re.finditer(r'(?<![\d.])(\d{1,3})(?!\d|\.)(?:\s*([/–-])\s*(\d{1,3})(?!\d|\.))?(\s*v\.\s*(?:chr|u\.\s*z))?', txt.lower()):
        a = int(m.group(1)); b = int(m.group(3)) if m.group(3) else None
        if m.group(4): a = -a; b = -b if b else None
        if b is not None and abs(b) < abs(a) and not m.group(4): b = None   # pl. 101/5 – nem értelmezzük
        out.append((a, b, m.group(2)))
    return out
def reign(txt, side):
    t = txt.lower().replace('-', ' ')
    best = None
    for k, (a, b) in REIGN.items():
        pat = (r'(früh|spät|mittel|ende )?\s*' + k[:-2]) if k.endswith('sch') else (r'(früh|spät|mittel|ende )?\s*' + k)
        for m in re.finditer(pat, t):
            pre = m.group(1); q = (b - a) // 4
            if side == 's': v = b - q if pre in ('spät', 'ende ') else ((a + b) // 2 if pre == 'mittel' else a)
            else: v = a + q if pre == 'früh' else ((a + b) // 2 if pre == 'mittel' else b)
            best = v if best is None else (min(best, v) if side == 's' else max(best, v))
    if 'agricola' in t: v = 77 if side == 's' else 84; best = v if best is None else best
    if 'limesfall' in t and side == 'e': best = 260 if best is None else max(best, 260)
    return best
def side_val(txt, side):
    ys = years(txt); C = []
    if ys:
        C.append((min(a for a, b, c in ys) if side == 's' else max((b if b is not None else a) for a, b, c in ys), 'év'))
    r = reign(txt, side)
    if r is not None: C.append((r, 'uralkodó'))
    c = cent(txt, side)
    if c is not None: C.append((c, 'évszázad-rész'))
    if not C: return None, None
    return min(C) if side == 's' else max(C)
def parse(raw):
    s = clean(raw)
    lines = [l.strip() for l in re.split(r'<br\s*/?>|\n', s) if l.strip()]
    j = []
    for l in lines:
        if j and re.search(r'\bbis$', j[-1]): j[-1] += ' ' + l
        else: j.append(l)
    lines = j
    lines = [l for l in lines if not re.match(r'^(vicus|lagerdorf|zivilsiedlung|siedlung|gräberfeld)', l.lower())]
    starts, ends, how = [], [], set(); last_end_missing = False
    for l in lines:
        l2 = re.sub(r'^[A-Za-z]\)|^[A-Z]\.[a-z]\)|^[a-c]\)|^\w+:', '', l).strip()
        parts = re.split(r'\bbis\b', l2)
        if len(parts) >= 2:
            sv, h1 = side_val(parts[0], 's'); ev, h2 = side_val(parts[-1], 'e'); last_end_missing = ev is None
            if sv is not None: starts.append((sv, h1)); how.add(h1)
            if ev is not None: ends.append((ev, h2)); how.add(h2)
        else:
            ys = years(l2)
            if len(ys) == 1 and ys[0][1] is not None and ys[0][2] in '–-':   # „83–86” típus
                a, b, _ = ys[0]; starts.append((a, 'év')); ends.append((b, 'év')); how.add('év')
            else:
                sv, h1 = side_val(l2, 's')
                if sv is not None: starts.append((sv, h1)); how.add(h1)
    def pick(L, f):
        if not L: return None
        y = [v for v, h in L if h == 'év']; o = [v for v, h in L if h != 'év']
        if not y: return f(o)
        if not o: return f(y)
        return f(o) if f(o) < f(y) - 30 else f(y)
    a, b = pick(starts, min), (max(v for v, h in ends) if ends else None)
    if lines:   # az utolsó szakasz nem zárul („bis” vagy évszám-tartomány nélkül): a végpont nem adható meg
        fl = re.sub(r'^[A-Za-z][.)]|^[A-Z]\.[a-z]\)|^\w+:', '', lines[-1]).strip()
        ys = years(fl)
        if not re.search(r'\bbis\b', fl) and not (len(ys) == 1 and ys[0][1] is not None and ys[0][2] in '–-') and (ys or reign(fl, 's') is not None or cent(fl, 's') is not None or re.search(r'jh|jahrh', fl.lower())):
            b = None
    if last_end_missing: b = None   # az utolsó szakasz vége csak évszázadra keltezett: a végpont nem adható meg
    if a is not None and b is not None and b < a: b = None
    return (a, b, sorted(how), s)
