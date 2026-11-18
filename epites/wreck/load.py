import openpyxl
def load(p='/home/claude/dl/wreck/w.xlsx'):
    wb=openpyxl.load_workbook(p,data_only=True,read_only=True);o={}
    for ws in wb:
        rows=list(ws.iter_rows(values_only=True));h=[str(x) if x is not None else '_%d'%i for i,x in enumerate(rows[0])]
        o[ws.title]=[dict(zip(h,r)) for r in rows[1:] if any(c is not None for c in r)]
    return o
