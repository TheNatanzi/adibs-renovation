import re, os, sys
T=os.path.dirname(os.path.abspath(__file__))+'/'
SITE=os.path.abspath(os.path.join(T,'..','..'))+'/'
rd=lambda f: open(T+f).read()
head=rd('head.html')
EXTRA_CSS='''
.rs{table-layout:fixed;width:100%}.rs td{vertical-align:top;overflow-wrap:anywhere}.rs td.n{white-space:normal;font:13px/1.45 var(--mono)}.rs td.d{font-size:13px;color:var(--muted)}
@media (max-width:700px){.rs colgroup{display:none}.rs thead{display:none}.rs,.rs tbody,.rs tr,.rs td{display:block;width:auto}.rs tr{border-bottom:1px solid var(--rule);padding:8px 0}.rs td{border:0;padding:2px 10px}}
.top{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:10px 16px;padding-block:4px 12px;border-bottom:1px solid var(--rule);margin-bottom:18px}
.tabs{display:flex;flex-wrap:wrap;gap:4px}
.tabs a{font:600 14px/1 var(--body);padding:9px 14px;border-radius:6px;color:var(--muted);text-decoration:none;border:1px solid transparent}
.tabs a[aria-current="page"]{color:var(--fg);background:var(--surface);border-color:var(--rule)}
.tabs a:hover,.tabs a:focus-visible{color:var(--madder)}
.acts{display:flex;flex-wrap:wrap;gap:8px}
.btn{display:inline-block;font:600 14px/1 var(--body);padding:10px 16px;border-radius:6px;text-decoration:none;border:1px solid var(--indigo)}
.btn.pri{background:var(--indigo);color:var(--bg)}
.btn.sec{color:var(--indigo);background:transparent}
.btn:focus-visible{outline:2px solid var(--madder);outline-offset:2px}
.ba{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
@media (max-width:760px){.ba{grid-template-columns:minmax(0,1fr)}}
.phgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px}
.ph{margin:0}.ph img{display:block;width:100%;height:auto;border:1px solid var(--rule);border-radius:4px}
.h3{font:600 1.05rem/1.3 var(--display);margin:1.4rem 0 .4rem}
ul.facts{padding-left:1.1rem;margin:.4rem 0}ul.facts li{margin:.3rem 0}
.chart{border:1px solid var(--rule);border-radius:6px;padding:12px;overflow-x:auto;background:var(--bg)}
.chart svg{display:block;min-width:640px;width:100%;height:auto}
.chart .ax{stroke:var(--rule)}.chart .tk{fill:var(--muted);font:12px var(--mono)}
.chart .done{fill:var(--indigo)}.chart .due{fill:var(--bg);stroke:var(--madder);stroke-width:2.5}
.chart .bar{fill:var(--surface);stroke:var(--rule)}
.chart .lb{fill:var(--fg);font:600 12px var(--body)}.chart .ld{fill:var(--muted);font:11px var(--mono)}
.legend{display:flex;gap:16px;font-size:12px;color:var(--muted);margin-top:6px}
.legend span::before{content:"";display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px;vertical-align:-1px}
.legend .l1::before{background:var(--indigo)}.legend .l2::before{border:2px solid var(--madder);width:7px;height:7px}
td.r{text-align:right}tr.tot td{font-weight:700;border-top:2px solid var(--rule)}
@media print{.top .acts,.tabs{display:none}.wrap{max-width:none;padding:0}figure.sheet{break-before:page}figure.sheet img{width:auto;max-width:100%;max-height:9.4in;margin:0 auto}h2{break-after:avoid}.tablewrap{overflow:visible}.chart svg{min-width:0}}
'''
SK='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><style>:root{color-scheme:light}body{margin:0;font:14px system-ui,sans-serif}img{max-width:100%}[hidden]{display:none!important}</style></head><body>'
TABS=[('index.html','Renovation'),('drawings.html','Drawings'),('photos.html','Photos'),('storage.html','Storage'),('research.html','Research')]
def page(fname,title,pdf,cross,body):
    hd=re.sub(r"<title>.*?</title>",f"<title>{title}</title>",head).replace('</style>',EXTRA_CSS+'</style>')
    tabs=''.join(f'<a href="{h}"'+(' aria-current="page"' if h==fname else '')+f'>{l}</a>' for h,l in TABS)
    acts=(f'<a class="btn sec" href="{cross[0]}">{cross[1]}</a>' if cross else '')+(f'<a class="btn pri" href="{pdf}" download>Download PDF</a>' if pdf else '')
    top=f'<div class="top"><nav class="tabs" aria-label="Pages">{tabs}</nav><div class="acts">{acts}</div></div>'
    html=SK+hd+'\n<div class="wrap">\n'+top+'\n'+body+'\n</div>\n</body></html>'
    open(SITE+fname,'w').write(html)
def fig(src,alt,cap,cls='sheet'):
    return (f'<figure class="{cls}"><a href="{src}" target="_blank" rel="noopener"><img src="{src}" alt="{alt}" loading="lazy"></a>'
            f'<figcaption>{cap} · <a href="{src}" target="_blank" rel="noopener">Open full size</a></figcaption></figure>')

# ---------- RENOVATION (overview) ----------
ft=lambda f,i: f+i/12
W=17.0; E=ft(20,9.25); D=ft(5,2); VW=ft(12,9); VD=13.0
aw,ae,av=W*D,E*D,VW*VD
sqft=f'''<div class="tablewrap"><table>
<thead><tr><th>New enclosed space</th><th>Width</th><th>Depth</th><th class="r">Area</th><th>Basis</th></tr></thead><tbody>
<tr><td>West display area</td><td class="n">17′-0″ ±</td><td class="n">5′-2″</td><td class="n r">≈ {aw:.0f} sf</td><td class="src">A-2.1 width · A-1.1 depth</td></tr>
<tr><td>East display area</td><td class="n">20′-9¼″</td><td class="n">5′-2″</td><td class="n r">≈ {ae:.0f} sf</td><td class="src">A-2.1 width · A-1.1 depth</td></tr>
<tr><td>Entry vestibule (porch enclosed)</td><td class="n">12′-9″</td><td class="n">≈ 13′ (scaled)</td><td class="n r">≈ {av:.0f} sf</td><td class="src">A-2.1 width · depth scaled from A-2.1</td></tr>
<tr class="tot"><td>Total newly enclosed</td><td></td><td></td><td class="n r">≈ {aw+ae+av:.0f} sf</td><td class="src">All non-conditioned; existing building ≈ 3,727 sf</td></tr>
</tbody></table></div>'''
changes='''<div class="tablewrap"><table>
<thead><tr><th>Change</th><th>Existing</th><th>2024 ATA design</th><th>Sheet</th></tr></thead><tbody>
<tr><td>Walkway bays</td><td>Open, roofed walkways</td><td>Enclosed display areas, non-conditioned</td><td class="src">A-2.1</td></tr>
<tr><td>Bay walls</td><td>None</td><td>2×6 pony wall, 3-coat ⅞″ stucco both faces, fixed tempered double-pane glazing</td><td class="src">A-3.1</td></tr>
<tr><td>Bay floor</td><td>Walkway paving</td><td>New 4″ slab, #3 @ 12″ o.c. each way, on new footing</td><td class="src">S-1, SD-1</td></tr>
<tr><td>Walkway posts</td><td>7×7 / 6×6 posts</td><td>New 6×6 posts (3 locations); existing headers kept</td><td class="src">A-2.1, S-1</td></tr>
<tr><td>Entry</td><td>Open porch; (2) 3′-0″ × 6′-8″ doors</td><td>New outer glass door pair 7′-0″ × 8′-0″ (2 × 3′-6″), double-pane tempered; fixed sidelights 2′-3″± × 7′-6″; existing doors stay as inner doors → secure vestibule</td><td class="src">A-2.1, ATA email 8/6/2024</td></tr>
<tr><td>Security doors</td><td>None</td><td>New security door from each display area to the porch</td><td class="src">A-2.1</td></tr>
<tr><td>Porch posts</td><td>—</td><td>New P.T. 4×6 posts at the new entry</td><td class="src">A-2.1</td></tr>
<tr><td>Roof, electrical, HVAC, site</td><td colspan="2">Unchanged (all work under existing roofs; electrical as-is; non-conditioned; no site work). A-2.1 notes "new lights by others".</td><td class="src">ATA letter 8/8/2024 · A-0.1</td></tr>
</tbody></table></div>
<p class="src">Plan status: permit set dated 2024-08-10, not submitted. Stamp shows CE49976 exp. 6-30-25; sheets cite 2022 codes (2025 codes in effect since 1 Jan 2026).</p>'''
ba=fig('photos/p06.jpg','Existing front of the store from South Main Street, July 2023, with open roofed walkways either side of the entry.','Existing storefront · 25 Jul 2023','ph')

# roof timeline (SVG, one scale)
import datetime as dt
def x(d): # 2026-07-01 .. 2030-12-31 mapped to 40..1060
    a=dt.date(2026,7,1); b=dt.date(2030,12,31); return 40+(d-a).days/(b-a).days*1020
ms=[(dt.date(2026,8,6),'Routed for review','2026-08-06','done',0),(dt.date(2026,8,20),'Not approved','08-20','done',1),(dt.date(2026,9,28),'Resubmitted','09-28','done',2),(dt.date(2026,10,13),'Issued','2026-10-13','done',3),
    (dt.date(2027,10,13),'Work must start by','2027-10-13','due',0),(dt.date(2030,10,13),'Work must finish by','2030-10-13','due',0)]
svg=['<svg viewBox="0 0 1100 200" role="img" aria-label="Permit S26106 timeline: issued 13 Oct 2026; work must start by 13 Oct 2027 and finish by 13 Oct 2030.">']
svg.append(f'<rect class="bar" x="{x(dt.date(2026,10,13)):.1f}" y="92" width="{x(dt.date(2027,10,13))-x(dt.date(2026,10,13)):.1f}" height="16" rx="3"/>')
svg.append(f'<text class="ld" x="{(x(dt.date(2026,10,13))+x(dt.date(2027,10,13)))/2:.1f}" y="124" text-anchor="middle">365-day start window</text>')
svg.append('<line class="ax" x1="40" y1="100" x2="1060" y2="100" stroke-width="2"/>')
for y in range(2027,2031):
    xx=x(dt.date(y,1,1)); svg.append(f'<line class="ax" x1="{xx:.1f}" y1="94" x2="{xx:.1f}" y2="106"/><text class="tk" x="{xx:.1f}" y="190" text-anchor="middle">{y}</text>')
for d,l,ds,k,i in ms:
    xx=x(d)
    if k=='done':
        ly=20+i*18; svg.append(f'<line class="ax" x1="{xx:.1f}" y1="{ly+4}" x2="{xx:.1f}" y2="94"/><circle class="done" cx="{xx:.1f}" cy="100" r="6"/><text class="lb" x="{xx+8:.1f}" y="{ly}">{l}</text><text class="ld" x="{xx+8:.1f}" y="{ly+13}">{ds}</text>' if False else f'<circle class="done" cx="{xx:.1f}" cy="100" r="6"/>')
    else:
        svg.append(f'<circle class="due" cx="{xx:.1f}" cy="100" r="7"/><line class="ax" x1="{xx:.1f}" y1="108" x2="{xx:.1f}" y2="140"/><text class="lb" x="{xx:.1f}" y="156" text-anchor="middle">{l}</text><text class="ld" x="{xx:.1f}" y="170" text-anchor="middle">{ds}</text>')
# review-phase labels stacked above
labels=[('Jul 2026','Application submitted'),('Aug 6','Routed for review'),('Aug 20','Not approved'),('Sep 28','Resubmitted'),('Oct 12','Approved'),('Oct 13','Issued')]
svg.append(f'<line class="ax" x1="{x(dt.date(2026,8,6)):.1f}" y1="70" x2="{x(dt.date(2026,8,6)):.1f}" y2="94"/>')
svg.append(f'<text class="lb" x="{x(dt.date(2026,7,1)):.1f}" y="40">Plan review: Aug 6 → Oct 13, 2026</text><text class="ld" x="{x(dt.date(2026,7,1)):.1f}" y="56">routed 08-06 · not approved 08-20 · resubmitted 09-28 · approved 10-12 · issued 10-13</text>')
svg.append('</svg>')
roof=f'''<h2 id="roof">Roof &amp; solar — permit S26106 (SolCore)</h2>
<ul class="facts">
<li><strong>Scope:</strong> new roof (GAF asphalt shingles) + rooftop solar, by SolCore, Inc. Separate from the ATA front work; already financed.</li>
<li><strong>Solar:</strong> 26.84 kW PV system on ≈ 1,286 sf of roof.</li>
<li><strong>Storage:</strong> 3 batteries, 34.5 kW.</li>
<li><strong>Shingles:</strong> GAF color deck sent 20 Jul 2026 (Charcoal, Aged Chestnut, Coastal Slate, Hickory, Sagewood, Sandalwood, Stone Gray); selection not on record.</li>
<li><strong>Status:</strong> issued 13 Oct 2026; no inspections yet; start date not scheduled.</li>
<li><strong>Drawings:</strong> SolCore's approved plans not yet obtained (city portal login or request from SolCore).</li>
</ul>
<div class="chart">{''.join(svg)}</div>
<div class="legend"><span class="l1">Completed</span><span class="l2">Deadline</span></div>
<p class="src">Source: City of Walnut Creek permit portal and issuance notice, 13 Oct 2026.</p>'''
tiles='''<div class="tiles">
  <div class="tile"><div class="v">22,137 sf</div><div class="k">Lot (0.51 ac)</div></div>
  <div class="tile"><div class="v">3,727 sf</div><div class="k">Building, 1957</div></div>
  <div class="tile"><div class="v">96′-6″ × 41′-2″</div><div class="k">Footprint, overall</div></div>
  <div class="tile"><div class="v">16 + 3</div><div class="k">Parking spots on site + off site</div></div>
</div>'''
body=f'''<p class="eyebrow">Reference toolkit · 19 Oct 2026</p>
<h1>1426 S Main St — Adib's Persian Rug Co</h1>
<p class="sub">Walnut Creek, CA 94596 · APN 183-030-005 · <a href="https://my.matterport.com/show/?m=MCQFszUDenU" target="_blank" rel="noopener">3D Matterport tour</a></p>
{tiles}
<h2 id="ata">2024 ATA front design — summary</h2>
<p class="src">Ali Adib, P.E., ATA Engineering. All sheets on the <a href="drawings.html">Drawings</a> tab.</p>
{ba}
<h3 class="h3">Square footage added</h3>
{sqft}
<h3 class="h3">Summary of changes</h3>
{changes}
{roof}
<h2 id="site">Site &amp; building</h2>
{rd('p_site_table.html')}
{rd('p_building_table.html')}
{rd('p_rules.html')}
{rd('p_people.html')}'''
page('index.html',"Adib's Renovation",'Adibs-Store-Toolkit.pdf',('storage.html','Storage plan →'),body)

# ---------- DRAWINGS ----------
dr=rd('p_drawings.html')
dr=re.sub(r'<figure class="sheet"><a href="sheets/survey1318-1.jpg".*?</figure>\n?','',dr,flags=re.S)
dr=dr.replace('All drawing sheets (17)','All drawing sheets (16)').replace('Every sheet shown whole.','Every sheet shown whole. The 1318 site survey is on the <a href="storage.html">Storage</a> tab.')
dr=dr.replace("S-2</strong> Roof framing plan","S-2</strong> Roof framing plan (ATA, existing roof structure; not the SolCore re-roof)")
page('drawings.html',"Adib's Drawings",'Adibs-Drawings.pdf',('storage.html','Storage plan →'),'<p class="eyebrow">Drawings · ATA Engineering 2024</p>\n<h1>Drawing sheets &amp; documents</h1>\n'+dr+'\n'+rd('p_docs.html'))

# ---------- PHOTOS ----------
ph=rd('p_photos.html')
ph=re.sub(r'<figure class="ph"><a href="photos/p0[6789].jpg".*?</figure>\n?','',ph,flags=re.S)
page('photos.html',"Adib's Photos",None,('storage.html','Storage plan →'),'<p class="eyebrow">Photos · 25 &amp; 31 Jul 2023</p>\n<h1>Store photos</h1>\n<p class="src">Album "California Gallery Walnut Creek". The front view is on the <a href="index.html">Renovation</a> tab. Click any photo for full size.</p>\n'+ph)

# ---------- STORAGE ----------
st=rd('storage_src.html')
i=st.index('<div class="tiles">'); j=st.rindex('</div>\n</body>') if '</div>\n</body>' in st else st.rindex('</body>')
sbody='<p class="eyebrow">Reference toolkit · 19 Oct 2026</p>\n<h1>1426 S Main St — Storage</h1>\n<p class="sub">Where the overflow rugs are, what the site allows, and what insurance requires. Includes Hamed\'s container research and vendor quotes (2023–2025).</p>\n'+st[i:j]

# ---------- STORAGE: web-research sections ----------
import json as _j, html as _h
RJ={r['id']:r for r in _j.load(open(SITE+'research.json'))}
def rtable(groups):
    e=_h.escape
    out=('<div class="tablewrap"><table class="rs"><colgroup><col style="width:15%"><col style="width:27%"><col style="width:44%"><col style="width:14%"></colgroup>'
         '<thead><tr><th>Item</th><th>Value</th><th>Detail</th><th>Source</th></tr></thead><tbody>')
    for g,ids in groups:
        for k,i in enumerate(ids):
            r=RJ[i]; t=r["source_title"].split(" | ")[0].split(" - ")[0]
            t=t if len(t)<=34 else t[:32].rstrip()+"…"
            out+=(f'<tr><td>{e(g) if k==0 else ""}</td><td class="n">{e(r["value"]) or "—"}</td><td class="d">{e(r["finding"])}</td>'
                  f'<td class="src"><a href="{e(r["url"])}" target="_blank" rel="noopener">{e(t)}</a><br><a href="research.html#{i}">{i}</a></td></tr>')
    return out+'</tbody></table></div>'
INST=[('City rules',['R003','R011','R010','R013','R017','R014']),
      ('Placement on lot',['R009','R022','R026','R039','R041','R037']),
      ('Delivery',['R134','R171','R135']),
      ('Ground + anchoring',['R167','R170','R096']),
      ('Climate inside',['R098','R100','R102','R104','R111']),
      ('Rug handling',['R107','R108','R110']),
      ('Locks + alarm',['R095','R093','R086','R087'])]
COST=[('Buy, used 20 ft',['R120','R126','R131']),
      ('Buy, new 20 ft',['R124','R128']),
      ('Buy, 40 ft',['R121','R127']),
      ('Rent',['R138','R139','R141','R144','R145']),
      ('Delivery',['R132','R136']),
      ('Site prep',['R167','R168','R170']),
      ('Doors, vents, moisture',['R158','R163','R165']),
      ('Alarm + monitoring',['R081','R079','R088']),
      ('Instead of a container',['R188','R193','R197','R219','R200','R213']),
      ('Racks',['R222','R224'])]
SEC=('<h2 id="install">Installation — web research</h2>\n<p class="src">From public web sources (city code, fire code, vendors, conservators), not from the emails. Click a row ID for the full quote. Nothing here is a city ruling: the zoning question goes to the Duty Planner.</p>\n'+rtable(INST)+
     '\n<h2 id="cost">Cost — web research</h2>\n<p class="src">Published list prices seen Oct 2026, before tax, delivery and permits unless stated. Not quotes, and not from the emails.</p>\n'+rtable(COST)+'\n')
sbody=sbody.replace('<h2 id="vendor">',SEC+'<h2 id="vendor">',1)
sbody=sbody.replace('<a href="#rules">','<a href="#install">Installation</a><a href="#cost">Cost</a><a href="#rules">',1)
page('storage.html',"Adib's Storage Toolkit",'Adibs-Storage-Toolkit.pdf',('index.html','← Renovation plan'),sbody)
print('built')

# ---------- RESEARCH ----------
RCSS="""<style>
.filters{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0}
.filters select,.filters input{font:14px var(--body);padding:8px 10px;border:1px solid var(--rule);border-radius:6px;background:var(--bg);color:var(--fg)}
.filters input{flex:1 1 220px;min-width:0}
.count{font:12px var(--mono);color:var(--muted);margin:6px 0}
td .q{font-size:12px;color:var(--muted);font-style:italic;margin-top:4px}
td.conf span{font:600 11px/1 var(--body);padding:3px 7px;border-radius:99px;border:1px solid currentColor;white-space:nowrap}
.c-high{color:#2f6b3a}.c-medium{color:#94600b}.c-low{color:#a1271b}
#rt{table-layout:fixed;width:100%}
.hl td.n{white-space:normal;font:13px/1.45 var(--mono)}
.hl td{vertical-align:top}
#rt td{vertical-align:top;overflow-wrap:anywhere}
#rt td.n{white-space:normal;font:12px/1.45 var(--mono)}
#rt td a{overflow-wrap:anywhere}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0 2px}
.chips button{font:12px var(--body);padding:5px 10px;border:1px solid var(--rule);border-radius:99px;background:var(--bg);color:var(--fg);cursor:pointer}
.chips button b{font-family:var(--mono);margin-left:4px}
.chips button[aria-pressed=true]{border-color:var(--fg);background:var(--fg);color:var(--bg)}
@media (max-width:700px){#rt thead{display:none}#rt,#rt tbody,#rt tr,#rt td{display:block;width:auto}#rt tr{border-bottom:1px solid var(--rule);padding:10px 0}#rt td{border:0;padding:3px 10px}}
</style>"""
rbody=RCSS+"""<p class="eyebrow">Web research · compiled Oct 2026</p>
<h1>Research database</h1>
<p class="sub">Outside research from public web sources (codes, vendors, guides). <strong>Not from the family's emails.</strong> Every row links to its source with a verbatim quote; check prices and code text before relying on them. Download: <a href="research.csv">CSV</a> · <a href="research.json">JSON</a></p>
<h2>Headline numbers</h2><div class="tablewrap"><table class="hl"><thead><tr><th>Area</th><th>Item</th><th>Number</th><th>Rows</th></tr></thead><tbody><tr><td>Storage</td><td>Outdoor storage in C-R zone</td><td class="n">Banned except listed uses; containers need a planner ruling</td><td><a href="#" data-id="R003">R003</a> <a href="#" data-id="R011">R011</a></td></tr><tr><td>Storage</td><td>Building permit trigger</td><td class="n">> 120 sf (20 ft container ≈ 160 sf)</td><td><a href="#" data-id="R013">R013</a> <a href="#" data-id="R017">R017</a></td></tr><tr><td>Storage</td><td>ISO portable-storage coverage</td><td class="n">$10,000 · 90 days · within 100 ft</td><td><a href="#" data-id="R073">R073</a></td></tr><tr><td>Storage</td><td>Used 20 ft container, Oakland</td><td class="n">$1,345 – $1,899 + delivery</td><td><a href="#" data-id="R120">R120</a> <a href="#" data-id="R126">R126</a></td></tr><tr><td>Storage</td><td>20 ft container rent, East Bay</td><td class="n">$60 / 4 wk – $145 / mo + delivery</td><td><a href="#" data-id="R138">R138</a> <a href="#" data-id="R144">R144</a></td></tr><tr><td>Storage</td><td>Dry Box</td><td class="n">Does not serve California</td><td><a href="#" data-id="R153">R153</a></td></tr><tr><td>Storage</td><td>Delivery clearance</td><td class="n">75 ft (20 ft) · 120 ft (40 ft) straight</td><td><a href="#" data-id="R134">R134</a></td></tr><tr><td>Storage</td><td>Self-storage 10×20, ≤ 5 mi</td><td class="n">$194 – $441 / mo</td><td><a href="#" data-id="R188">R188</a> <a href="#" data-id="R197">R197</a></td></tr><tr><td>Storage</td><td>Monitored alarm</td><td class="n">$40 – $120 / mo + $300 – $2,000 install</td><td><a href="#" data-id="R079">R079</a> <a href="#" data-id="R081">R081</a></td></tr><tr><td>Renovation</td><td>Design review</td><td class="n">Required before building permit; minor if ≤ 500 sf</td><td><a href="#" data-id="R044">R044</a> <a href="#" data-id="R045">R045</a></td></tr><tr><td>Renovation</td><td>Glass doors + sidelights</td><td class="n">Safety glazing (CBC 2406.4)</td><td><a href="#" data-id="R233">R233</a> <a href="#" data-id="R234">R234</a></td></tr><tr><td>Renovation</td><td>Entry door</td><td class="n">32 in clear · ½ in threshold · 5 lb force</td><td><a href="#" data-id="R238">R238</a> <a href="#" data-id="R241">R241</a> <a href="#" data-id="R243">R243</a></td></tr><tr><td>Renovation</td><td>ADA path-of-travel cap</td><td class="n">20 % of cost if ≤ $209,208 (2026)</td><td><a href="#" data-id="R249">R249</a> <a href="#" data-id="R248">R248</a></td></tr><tr><td>Roof</td><td>Permit S26106 clock</td><td class="n">Start ≤ 12 mo of issue · finish ≤ 4 yr</td><td><a href="#" data-id="R299">R299</a> <a href="#" data-id="R300">R300</a></td></tr><tr><td>Roof</td><td>Federal solar credit (§48E)</td><td class="n">In service ≤ 2027-12-31 unless begun ≤ 2026-07-04</td><td><a href="#" data-id="R337">R337</a></td></tr></tbody></table></div>
<h2>All findings</h2>
<div class="filters">
<label class="sr" for="f-topic" hidden>Topic</label><select id="f-topic"><option value="">All topics</option></select>
<select id="f-app" aria-label="Applies to"><option value="">All areas</option><option value="storage">Storage</option><option value="renovation">Renovation</option><option value="roof">Roof &amp; solar</option></select>
<select id="f-conf" aria-label="Confidence"><option value="">Any confidence</option><option>high</option><option>medium</option><option>low</option></select>
<input id="f-q" type="search" placeholder="Search findings, values, sources" aria-label="Search">
</div>
<div class="chips" id="chips"></div>
<p class="count" id="cnt">Loading…</p>
<div class="tablewrap"><table id="rt"><colgroup><col style="width:14%"><col style="width:42%"><col style="width:18%"><col style="width:17%"><col style="width:9%"></colgroup><thead><tr><th>Topic</th><th>Finding</th><th>Value</th><th>Source</th><th>Confidence</th></tr></thead><tbody></tbody></table></div>
<script>
(function(){
 const tb=document.querySelector('#rt tbody'),cnt=document.getElementById('cnt');
 const ft=document.getElementById('f-topic'),fa=document.getElementById('f-app'),fc=document.getElementById('f-conf'),fq=document.getElementById('f-q');
 let rows=[];
 function el(t,c,txt){const e=document.createElement(t);if(c)e.className=c;if(txt!=null)e.textContent=txt;return e;}
 function render(){
  const q=fq.value.trim().toLowerCase();tb.textContent='';let n=0;
  rows.forEach(r=>{
   if(ft.value&&r.topic!==ft.value)return;
   if(fa.value&&r.applies_to!==fa.value&&r.applies_to!=='both')return;
   if(fc.value&&r.confidence!==fc.value)return;
   if(q&&!(r.id+' '+r.topic+' '+r.subtopic+' '+r.finding+' '+r.value+' '+r.source_title+' '+r.quote).toLowerCase().includes(q))return;
   n++;const tr=el('tr');
   const t=el('td');t.appendChild(el('div','',r.topic));t.appendChild(el('div','src',r.subtopic));tr.appendChild(t);
   const f=el('td');f.appendChild(el('div','',r.finding));if(r.quote)f.appendChild(el('div','q','“'+r.quote+'”'));tr.appendChild(f);
   tr.appendChild(el('td','n',r.value||''));
   const s=el('td');const a=el('a','',r.source_title||r.url);a.href=r.url;a.target='_blank';a.rel='noopener';s.appendChild(a);if(r.source_date)s.appendChild(el('div','src',r.source_date));tr.appendChild(s);
   const c=el('td','conf');c.appendChild(el('span','c-'+r.confidence,r.confidence));tr.appendChild(c);
   tb.appendChild(tr);});
  cnt.textContent=n+' of '+rows.length+' rows';
 }
 fetch('research.json').then(r=>r.json()).then(d=>{rows=d;const ch=document.getElementById('chips');const cn={};d.forEach(r=>cn[r.topic]=(cn[r.topic]||0)+1);if(/^#R[0-9]{3}$/.test(location.hash))fq.value=location.hash.slice(1);Object.keys(cn).sort().forEach(t=>{const o=el('option','',t);o.value=t;ft.appendChild(o);const b=el('button','',t);b.type='button';b.appendChild(el('b','',cn[t]));b.setAttribute('aria-pressed','false');b.onclick=()=>{ft.value=ft.value===t?'':t;sync();render();};ch.appendChild(b);});render();}).catch(()=>{cnt.textContent='Could not load research.json';});
 function sync(){document.querySelectorAll('#chips button').forEach(b=>b.setAttribute('aria-pressed',String(b.firstChild.textContent===ft.value)));}
 ft.addEventListener('change',sync);
 document.querySelectorAll('a[data-id]').forEach(a=>a.onclick=e=>{e.preventDefault();ft.value='';fa.value='';fc.value='';sync();fq.value=a.dataset.id;render();document.getElementById('f-q').scrollIntoView({behavior:'smooth'});});
 [ft,fa,fc].forEach(x=>x.addEventListener('change',render));fq.addEventListener('input',render);
})();
</script>"""
page('research.html',"Adib's Research",None,('index.html','← Renovation plan'),rbody)
