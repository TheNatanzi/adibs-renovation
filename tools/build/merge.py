import json,csv,glob,os,sys,re
S=os.path.dirname(os.path.abspath(__file__))
OUT=sys.argv[1]
ORDER=['regulations','security','costs','alternatives','renovation','roof']
F=['topic','subtopic','finding','value','source_title','url','quote','source_date','confidence','applies_to']
rows=[];seen=set()
for name in ORDER:
    p=f'{S}/rows/{name}.json'
    if not os.path.exists(p): continue
    for r in json.load(open(p)):
        r={k:str(r.get(k,'') or '').strip() for k in F}
        if name=='roof': r['applies_to']='roof'
        if not r['finding'] or not r['url'].startswith('http'): continue
        if 'sprinkler' in r['finding'].lower(): continue  # user excluded sprinkler data
        for k in ('finding','value'):
            r[k]=re.sub(r'\bstalls\b','parking spots',re.sub(r'\bstall\b','parking spot',r[k]))
        key=(r['url'].rstrip('/').lower(),re.sub(r'\W+','',r['finding'].lower())[:80])
        if key in seen: continue
        seen.add(key);rows.append(r)
for i,r in enumerate(rows,1): r['id']=f'R{i:03d}'
F2=['id']+F
json.dump([{k:r[k] for k in F2} for r in rows],open(f'{OUT}/research.json','w'),ensure_ascii=False,indent=0)
with open(f'{OUT}/research.csv','w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,F2);w.writeheader();[w.writerow({k:r[k] for k in F2}) for r in rows]
print(len(rows),'rows')
