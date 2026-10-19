import json,sys,re
src,dst=sys.argv[1],sys.argv[2]
texts=[]
for line in open(src):
    try: o=json.loads(line)
    except: continue
    def walk(x):
        if isinstance(x,dict):
            for k,v in x.items():
                if isinstance(v,str) and '"finding"' in v: texts.append(v)
                else: walk(v)
        elif isinstance(x,list):
            for v in x: walk(v)
    walk(o)
best=None
for t in texts:
    i=t.find('['); j=t.rfind(']')
    if i<0 or j<0: continue
    try:
        arr=json.loads(t[i:j+1])
        if isinstance(arr,list) and (best is None or len(arr)>len(best)): best=arr
    except Exception as e: pass
if best is None: print('NO JSON FOUND', len(texts)); sys.exit(1)
json.dump(best,open(dst,'w'),indent=1,ensure_ascii=False); print(len(best),'rows ->',dst)
