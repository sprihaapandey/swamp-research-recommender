import feedparser
import json
import time

categories = [
    "cs.AI", "cs.CL", "cs.CC", "cs.CE", "cs.CG", "cs.CV", "cs.CY", "cs.DB", "cs.DC", 
    "cs.DL", "cs.DM", "cs.DS", "cs.ET", "cs.FL", "cs.GL", "cs.GR", "cs.GT", "cs.HC", 
    "cs.IR", "cs.IT", "cs.LG", "cs.LO", "cs.MA", "cs.MM", "cs.MS", "cs.NA", "cs.NE", 
    "cs.NI", "cs.OH", "cs.OS", "cs.PF", "cs.PL", "cs.RO", "cs.SC", "cs.SD", "cs.SE", "cs.SI", "cs.SY",

    "math.AG", "math.AT", "math.AP", "math.CT", "math.CA", "math.CO", "math.AC", "math.CV", "math.DG",
    "math.DS", "math.FA", "math.GM", "math.GN", "math.GT", "math.GR", "math.HO", "math.IT", "math.KT",
    "math.LO", "math.MG", "math.MP", "math.NT", "math.NA", "math.OA", "math.OC", "math.PR", "math.QA",
    "math.RT", "math.RA", "math.SP", "math.ST", "math.SG",

    "physics.app-ph", "physics.atom-ph", "physics.atm-clus", "physics.bio-ph", "physics.chem-ph",
    "physics.class-ph", "physics.comp-ph", "physics.data-an", "physics.ed-ph", "physics.flu-dyn",
    "physics.gen-ph", "physics.geo-ph", "physics.hist-ph", "physics.ins-det", "physics.med-ph",
    "physics.optics", "physics.plasm-ph", "physics.pop-ph", "physics.soc-ph", "physics.space-ph",

    "stat.AP", "stat.CO", "stat.ME", "stat.ML", "stat.TH",

    "q-bio.BM", "q-bio.GN", "q-bio.MN", "q-bio.NC", "q-bio.OT", "q-bio.PE", "q-bio.QM", "q-bio.SC", "q-bio.TO",
    "q-fin.CP", "q-fin.EC", "q-fin.GN", "q-fin.MF", "q-fin.PM", "q-fin.PR", "q-fin.RM", "q-fin.ST", "q-fin.TR",
    "econ.EM", "econ.GN", "econ.TH",
    "eess.AS", "eess.IV", "eess.SP", "eess.SY"
]

all_papers = []

for cat in categories:
    url = f"http://export.arxiv.org/api/query?search_query=cat:{cat}&start=0&max_results=100"
    print(f"Fetching {cat} ...")
    feed = feedparser.parse(url)
    for entry in feed.entries:
        all_papers.append({
            "id": entry.id,
            "title": entry.title,
            "summary": entry.summary,
            "published": entry.published,
            "authors": [a.name for a in entry.authors],
            "link": entry.link,
            "category": cat
        })
    time.sleep(3)

with open("../data/papers.json", "w") as f:
    json.dump(all_papers, f, indent=2)

print(f"Saved {len(all_papers)} papers across {len(categories)} categories")