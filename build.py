"""Builds the TechVestVentures AI Job Displacement Graphs site from the charts in focus/jobs/ (captions from the Risk Graphs records, sources linked). Numbers come only from the linked sources."""
import os,sys,shutil,json,glob
sys.path.insert(0,'/workspace/risk-watcher/graphs-site');sys.path.insert(0,'/workspace/risk-watcher');os.chdir(os.path.dirname(os.path.abspath(__file__)))
from common import *
T="TechVestVentures AI Job Displacement Graphs";J="/workspace/risk-watcher/focus/jobs/"
R={}
for p in ["/workspace/risk-watcher/issues/2026-10-30/graphs/Graphs 2026-10-30.json","/workspace/risk-watcher/issues/2026-10-31/graphs/Graphs 2026-10-31.json","/workspace/risk-watcher/issues/2026-11-01/graphs/Graphs 2026-11-01.json",J+"_growth_data/records_2026-10-31.json"]:
    d=json.load(open(p));d=d["graphs"] if isinstance(d,dict) else d
    for g in d: R[os.path.basename(g["file"])]=g
TABS=[("displacement","Displacement Risk","Where AI is expected to touch work, and where early pressure shows up: published exposure estimates, entry-level graduates, tech-services jobs and software job postings.",
  ["12 AI HYPERGROWTH published AI job exposure vs displacement estimates 2026-10-31.png","12 AI HYPERGROWTH BLS young college graduates vs all workers unemployment 2026-10-30.png","12 AI HYPERGROWTH BLS computer systems design and information jobs vs payrolls 2026-10-30.png","12 AI HYPERGROWTH BLS data processing and hosting jobs vs IT services jobs 2026-10-31.png","12 AI HYPERGROWTH Indeed software development job postings vs all postings 2026-11-01.png"]),
 ("labor","Labor Market Reality","What the official US labor data show today: openings vs layoffs, jobless claims, long-term unemployment vs quits, temp help as an early signal, and job losers not expecting recall vs temporary layoffs.",
  ["06 ECON BLS JOLTS layoffs vs job openings 2026-10-30.png","06 ECON DOL continuing vs initial jobless claims 2026-10-30.png","06 ECON BLS long-term unemployed share vs quits rate 2026-10-31.png","06 ECON BLS temporary help jobs early layoff signal 2026-10-31.png","06 ECON BLS job losers not on temporary layoff vs temporary layoff 2026-11-01.png"]),
 ("growth","Where Jobs Will Grow","The counter-strategy side: occupations and groups projected to grow most (BLS 2025-35) and the roles global employers expect to grow or shrink by 2030 (WEF). Projections and survey expectations, not TVV forecasts.",
  ["12 AI HYPERGROWTH BLS fastest-growing occupations 2025-35 2026-10-31.png","12 AI HYPERGROWTH BLS occupations adding the most jobs 2025-35 2026-10-31.png","12 AI HYPERGROWTH BLS projected job growth by major occupational group 2025-35 2026-10-31.png","12 AI HYPERGROWTH WEF fastest-growing vs fastest-declining jobs 2025-30 2026-10-31.png"])]
shutil.rmtree("issues",ignore_errors=True);os.makedirs("issues/img")
# Published set is a chosen subset of focus/jobs (later daily charts stay unpublished until selected).
# Do not require equality with every PNG in the folder.
tab_files=[f for _,_,_,fs in TABS for f in fs]
have=set(os.path.basename(p) for p in glob.glob(J+"*.png"))
missing=[f for f in tab_files if f not in have]
assert not missing, f"missing focus/jobs files: {missing}"
# M49 (Stanford / ADP software-developer employment by age), added 2026-11-10. Keep existing image filenames (displacement-01..05, labor-06..10, growth-11..14).
M49F="12 AI HYPERGROWTH Stanford ADP software developer employment by age 2026-11-10.png"
assert M49F in have, M49F
R[M49F]={
  "file": M49F,
  "title": "Developers aged 22–25: jobs index down 18.6% since Nov 2022",
  "caption": "Sep 2026: developers aged 22–25 at 81.4, aged 41–49 at 120.2 (Nov 2022=100). Stanford Canaries, ADP.",
  "label": "Data",
  "data_date": "Sep 2026 (vintage Oct 16, published Oct 21, 2026)",
  "source": "https://digitaleconomy.stanford.edu/project/indicators/canaries-dashboard/",
  "extra_sources": [
    "https://storage.googleapis.com/aviary-del-public/release_memos/latest/downloads/canaries_software_developers_results.zip",
    "https://storage.googleapis.com/aviary-del-public/release_memos/latest/downloads/canaries_by_age_results.zip",
    "https://digitaleconomy.stanford.edu/app/uploads/2026/08/Canaries_August2026.pdf",
    "https://budgetlab.yale.edu/research/evaluating-impact-ai-labor-market-current-state-affairs",
    "https://x.com/randgroup/status/2120088546350428535",
  ],
  "doubt": "Rand’s headline says “1 in 5 junior dev jobs gone since ChatGPT.” Stanford says the dashboard shows correlation, not a causal link, and that earlier declines are likely non-AI. The fixed firm panel leaves out new firms, and the index tracks fewer young hires, not jobs destroyed. All six age series also jump together in May 2025, which may be a sample effect.",
  "rebuttal": ["Yale Budget Lab: Evaluating the impact of AI on the labor market", "https://budgetlab.yale.edu/research/evaluating-impact-ai-labor-market-current-state-affairs"],
}
EXTRA={"displacement": [(M49F, "img/displacement-15.webp")]}
tabs=[];src={};n=0
def w(k,lab,body): open(f"issues/{k}.html","w").write(page(T,k,body));tabs.append((k,lab))
# Optional doubt/rebuttal block for selected charts (M49); other charts keep the standard figure().
def fig_plus(g,out,urls):
    body=figure(out,g["title"],f'{g["caption"]} [{g.get("label","Data")}. Data: {g["data_date"]}]',urls)
    extra=""
    if g.get("doubt"):
        extra+=f'<p class="doubt">{E(g["doubt"])}</p>'
    if g.get("rebuttal"):
        extra+=f'<p>Rebuttal: <a href="{E(g["rebuttal"][1])}">{E(g["rebuttal"][0])}</a></p>'
    if extra:
        body=body.replace("</figcaption>"," "+extra+"</figcaption>")
    return body
for k,lab,note,fs in TABS:
    b=f'<h2 class="desk">{E(lab)}</h2><p>{E(note)}</p>'
    for f in fs:
        g=R[f];n+=1;out=f"img/{k}-{n:02d}.webp";save_img(J+f,"issues/"+out)
        urls=list(dict.fromkeys([g["source"]]+list(g.get("extra_sources") or [])))
        for u in urls: src.setdefault(u,g["title"])
        b+=fig_plus(g,out,urls)
    for f,out in EXTRA.get(k,[]):
        g=R[f];save_img(J+f,"issues/"+out)
        urls=list(dict.fromkeys([g["source"]]+list(g.get("extra_sources") or [])))
        for u in urls: src.setdefault(u,g["title"])
        b+=fig_plus(g,out,urls)
        n+=1  # count only; do not use n for EXTRA filenames (keeps labor-06..10, growth-11..14)
    w(k,lab,b)
w("sources","Sources",f'<h2 class="desk">Sources ({len(src)} links)</h2><p>All charts were drawn by TechVestVentures from the data linked below. Published third-party values are cited as such in each caption.</p><ul class="src">'+"".join(f'<li>{E(l)}: <a href="{E(u)}">{E(u)}</a></li>' for u,l in src.items())+"</ul>")
import common
common.CSS+="""
figure.g .doubt{border-left:4px solid #FCA311;background:#fff8ea;padding:8px 12px;margin:8px 0}"""
index(T,tabs,"Sections",cur="jobs");print(n,"charts",len(src),"sources",[t[0] for t in tabs])
