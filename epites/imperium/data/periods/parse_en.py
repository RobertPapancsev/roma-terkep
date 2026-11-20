import re
RE = {'augustus': (-27, 14), 'tiberius': (14, 37), 'caligula': (37, 41), 'claudius': (41, 54), 'nero': (54, 68), 'vespasian': (69, 79), 'flavian': (69, 96),
      'titus': (79, 81), 'domitian': (81, 96), 'nerva': (96, 98), 'trajan': (98, 117), 'hadrian': (117, 138), 'antoninus pius': (138, 161), 'antonine': (138, 161),
      'marcus aurelius': (161, 180), 'commodus': (180, 192), 'septimius severus': (193, 211), 'severan': (193, 235), 'caracalla': (211, 217), 'gallienus': (253, 268),
      'aurelian': (270, 275), 'diocletian': (284, 305), 'tetrarch': (293, 305), 'constantine': (306, 337), 'constantius ii': (337, 361), 'valentinian': (364, 375),
      'justinian': (527, 565), 'agricola': (77, 84)}
ORD = {'first': 1, 'second': 2, 'third': 3, 'fourth': 4, 'fifth': 5, 'sixth': 6}
def clean(s):
    s = re.sub(r'<ref[^>]*/>', '', s); s = re.sub(r'<ref[^>]*>.*?</ref>', '', s, flags=re.S); s = re.sub(r'\{\{(?:citation needed|cn|when|dubious)[^}]*\}\}', '', s, flags=re.I)
    s = re.sub(r'\{\{circa\}\}|\{\{c\.\}\}', 'c. ', s, flags=re.I)
    s = re.sub(r'\{\{(?:AD|CE)\|([^}]*)\}\}', r'AD \1', s); s = re.sub(r'\{\{(?:BC|BCE)\|([^}]*)\}\}', r'\1 BC', s)
    s = re.sub(r'\[\[(?:[^|\]]*\|)?([^\]]*)\]\]', r'\1', s); s = re.sub(r"'{2,}", '', s); s = re.sub(r'\{\{[^}]*\}\}', '', s)
    return s.replace('&nbsp;', ' ').strip()
def val(txt, side):
    t = txt.lower(); C = []
    for m in re.finditer(r'(?<![\d])(\d{1,3})(?:\s*[–-]\s*(\d{1,3}))?(?![\d]|(?:st|nd|rd|th))(\s*(?:bc|bce|b\.c\.))?', t):
        a = int(m.group(1)); b = int(m.group(2)) if m.group(2) else a
        if b < a and not m.group(3): b = a
        if m.group(3): a, b = -a, -b
        C.append(min(a, b) if side == 's' else max(a, b))
    for k, (a, b) in RE.items():
        for m in re.finditer(r'(early|late|mid)?[\s-]*' + k, t):
            pre = m.group(1); q = (b - a) // 4
            C.append((b - q if pre == 'late' else a) if side == 's' else (a + q if pre == 'early' else b))
    for m in re.finditer(r'(early|mid|middle of the|late|end of the|beginning of the|first half of the|second half of the)?[\s-]*(\d)(?:st|nd|rd|th)\s+century', t):
        q, n = m.group(1), int(m.group(2)); base = 100 * (n - 1)
        if not q: continue
        if q in ('early', 'beginning of the'): C.append(base + (10 if side == 's' else 30))
        elif q in ('mid', 'middle of the'): C.append(base + 50)
        elif q in ('late', 'end of the'): C.append(base + (90 if side == 's' else 100))
        elif q == 'first half of the': C.append(base + (1 if side == 's' else 50))
        elif q == 'second half of the': C.append(base + (51 if side == 's' else 100))
    if not C: return None
    return min(C) if side == 's' else max(C)
def parse_en(s):
    g = lambda f: (re.search(r'\n\s*\|\s*' + f + r'\s*=([^\n]*)', s) or [None, ''])[1]
    bs = clean(g('built') or g('founded') or g('construction_start_date')); ab = clean(g('abandoned') or g('demolished_date'))
    if re.search(r'unknown|\?', bs, re.I) and not re.search(r'\d', bs): bs = ''
    if re.search(r'unknown', ab, re.I): ab = ''
    a = val(bs, 's') if bs else None; e = val(ab, 'e') if ab else None
    if a is not None and e is not None and e < a: e = None
    return a, e, (bs, ab)
