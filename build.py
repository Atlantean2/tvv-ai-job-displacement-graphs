"""Builds the TechVestVentures AI Job Displacement Graphs site from the charts in focus/jobs/ (captions from the Risk Graphs records, sources linked). Numbers come only from the linked sources."""
import os,sys,shutil,json,glob
sys.path.insert(0,'/workspace/risk-watcher/graphs-site');sys.path.insert(0,'/workspace/risk-watcher');os.chdir(os.path.dirname(os.path.abspath(__file__)))
from common import *
T="TechVestVentures AI Job Displacement Graphs";J="/workspace/risk-watcher/focus/jobs/"
R={}
for p in ["/workspace/risk-watcher/issues/2026-10-30/graphs/Graphs 2026-10-30.json","/workspace/risk-watcher/issues/2026-10-31/graphs/Graphs 2026-10-31.json",J+"_growth_data/records_2026-10-31.json"]:
    d=json.load(open(p));d=d["graphs"] if isinstance(d,dict) else d
    for g in d: R[os.path.basename(g["file"])]=g
TABS=[("displacement","Displacement Risk","Where AI is expected to touch work, and where early pressure shows up: published exposure estimates, entry-level graduates and tech-services jobs.",
  ["12 AI HYPERGROWTH published AI job exposure vs displacement estimates 2026-10-31.png","12 AI HYPERGROWTH BLS young college graduates vs all workers unemployment 2026-10-30.png","12 AI HYPERGROWTH BLS computer systems design and information jobs vs payrolls 2026-10-30.png","12 AI HYPERGROWTH BLS data processing and hosting jobs vs IT services jobs 2026-10-31.png"]),
 ("labor","Labor Market Reality","What the official US labor data show today: openings vs layoffs, jobless claims, long-term unemployment vs quits, and temp help as an early signal.",
  ["06 ECON BLS JOLTS layoffs vs job openings 2026-10-30.png","06 ECON DOL continuing vs initial jobless claims 2026-10-30.png","06 ECON BLS long-term unemployed share vs quits rate 2026-10-31.png","06 ECON BLS temporary help jobs early layoff signal 2026-10-31.png"]),
 ("growth","Where Jobs Will Grow","The counter-strategy side: occupations and groups projected to grow most (BLS 2025-35) and the roles global employers expect to grow or shrink by 2030 (WEF). Projections and survey expectations, not TVV forecasts.",
  ["12 AI HYPERGROWTH BLS fastest-growing occupations 2025-35 2026-10-31.png","12 AI HYPERGROWTH BLS occupations adding the most jobs 2025-35 2026-10-31.png","12 AI HYPERGROWTH BLS projected job growth by major occupational group 2025-35 2026-10-31.png","12 AI HYPERGROWTH WEF fastest-growing vs fastest-declining jobs 2025-30 2026-10-31.png"])]
shutil.rmtree("issues",ignore_errors=True);os.makedirs("issues/img")
assert sorted(f for _,_,_,fs in TABS for f in fs)==sorted(os.path.basename(p) for p in glob.glob(J+"*.png")),"focus/jobs set changed"
tabs=[];src={};n=0
def w(k,lab,body): open(f"issues/{k}.html","w").write(page(T,k,body));tabs.append((k,lab))
for k,lab,note,fs in TABS:
    b=f'<h2 class="desk">{E(lab)}</h2><p>{E(note)}</p>'
    for f in fs:
        g=R[f];n+=1;out=f"img/{k}-{n:02d}.webp";save_img(J+f,"issues/"+out)
        urls=[g["source"]]+list(g.get("extra_sources") or [])
        for u in urls: src.setdefault(u,g["title"])
        b+=figure(out,g["title"],f'{g["caption"]} [{g.get("label","Data")}. Data: {g["data_date"]}]',urls)
    w(k,lab,b)
w("sources","Sources",f'<h2 class="desk">Sources ({len(src)} links)</h2><p>All charts were drawn by TechVestVentures from the data linked below. Published third-party values are cited as such in each caption.</p><ul class="src">'+"".join(f'<li>{E(l)}: <a href="{E(u)}">{E(u)}</a></li>' for u,l in src.items())+"</ul>")
index(T,tabs,"Sections",cur="jobs");print(n,"charts",len(src),"sources",[t[0] for t in tabs])
