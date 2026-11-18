# McConnell et al. 2018 (PNAS 115, 5726–5731), Dataset S1, „Fig. 3” lap -> lead/data.json
import openpyxl,json,statistics as st
wb=openpyxl.load_workbook('/home/claude/dl/lead/sd01.xlsx',data_only=True);ws=wb['Fig. 3']
R=[r for r in ws.iter_rows(min_row=8,values_only=True) if isinstance(r[0],(int,float))]
Y=[(1950-r[0],r[2]) for r in R if isinstance(r[2],(int,float)) and r[2]>-0.9]  # CE év (törtév), kt/a (11 éves medián)
Y.sort()
def mean(a,b): 
    v=[e for y,e in Y if a<=y<b];return (round(st.mean(v),3),round(min(v),3),round(max(v),3),len(v)) if v else None
res={'n':len(Y),'y0':Y[0][0],'y1':Y[-1][0],'series':[[round(y,1),round(e,3)] for y,e in Y]}
res['per']={k:mean(a,b) for k,(a,b) in {'bg_-1100_-1000':(-1100,-1000),'-400_-125':(-400,-125),'-125_-31':(-125,-31),'-80_-61':(-80,-61),'-17_160':(-17,161),'1_100':(1,101),'165_193':(165,194),'194_234':(194,235),'235_284':(235,285),'285_400':(285,401),'401_700':(401,701),'701_800':(701,801)}.items()}
res['b50']=[mean(b,b+50)[0] for b in range(-500,700,50)]
res['max']=max(Y,key=lambda t:t[1]);res['min_after_-900']=min((t for t in Y if t[0]>=-900),key=lambda t:t[1])
json.dump(res,open('/home/claude/roma/lead/data.json','w'))
if __name__=='__main__':
    print(res['n'],res['y0'],res['y1'],res['max'],res['min_after_-900'])
    for k,v in res['per'].items(): print(k,v)
    W=json.load(open('/home/claude/roma/wreck/data.json'))
    a=W['all'];b=res['b50']
    def rank(x):
        s=sorted(range(len(x)),key=lambda i:x[i]);r=[0]*len(x)
        for k,i in enumerate(s): r[i]=k+1
        return r
    def sp(x,y):
        rx,ry=rank(x),rank(y);n=len(x);mx=sum(rx)/n;my=sum(ry)/n
        return sum((p-mx)*(q-my) for p,q in zip(rx,ry))/(sum((p-mx)**2 for p in rx)*sum((q-my)**2 for q in ry))**.5
    print('spearman wrecks(all) vs lead 50y, n=',len(a),round(sp(a,b),2),'p100',round(sp(W['p100'],b),2))
    for bb,x,y in zip(W['bins'],a,b): print(bb,x,y)
    # years of local extremes
    for a0,b0 in [(50,70),(100,110),(160,200),(230,290)]:
        print(a0,b0,[(round(y),e) for y,e in Y if a0<=y<b0][::3])
