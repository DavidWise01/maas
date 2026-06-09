#!/usr/bin/env python3
"""Materialize the M1 (Maas) persona ACI badges from the verified workflow output:
each persona → <slug>.agent + full ACI complement (.carbon.tiff, .silicon.png,
.spun, .moniker, .1099, manifest) + agents/_personas.json for the roster."""
import os, sys, json, re
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build  # maas/build.py — write_aci, png engine

OUTPUT = r"C:\Users\Dave\AppData\Local\Temp\claude\C--Davids-files\50f3f0da-7535-418b-8b7b-480c3727faa9\tasks\wu73ln928.output"
data = json.load(open(OUTPUT, encoding="utf-8"))["result"]
personas = data["personas"]
flagged = data.get("flagged", [])

def parse_front(md):
    m = re.match(r"^---\n(.*?)\n---\n", md, re.S)
    f = {}
    if m:
        for line in m.group(1).split("\n"):
            if ":" in line:
                k, v = line.split(":", 1)
                f[k.strip()] = v.strip()
    return f

# normalize spoiler-bearing slug/name (the verifier stripped the surname from the
# prose; keep it out of the filename + roster label too — book one knows only "Elena")
FIX = {"elena-galathynius": {"slug": "elena", "name": "Elena"}}

agents_dir = os.path.join(HERE, "agents")
os.makedirs(agents_dir, exist_ok=True)
index = []
for p in personas:
    if p["slug"] in FIX:
        p = {**p, **FIX[p["slug"]]}
    slug, md = p["slug"], p["agent"]
    fr = parse_front(md)
    rec = {
        "name": p["name"], "axiom": "M1", "seal": fr.get("seal", p.get("epithet", "")),
        "origin": "M1 · Maas", "position": fr.get("class", p.get("epithet", "")),
        "role": p.get("epithet", ""), "nature": fr.get("what", ""),
        "mechanism": fr.get("how", ""), "crystallization": fr.get("why", ""),
        "witness": fr.get("who", ""), "conductor": "ROOT0 (catalogued into UD0)",
        "inputs": fr.get("series", "Throne of Glass"),
        "source": "Maas character (books 1–2), catalogued by ROOT0",
    }
    tok = build.write_aci(rec, agents_dir, slug, agent_md=md)
    index.append({"slug": slug, "name": p["name"], "epithet": p.get("epithet", ""), "moniker": tok["moniker"]})

index.sort(key=lambda x: x["name"])
json.dump(index, open(os.path.join(agents_dir, "_personas.json"), "w", encoding="utf-8"),
          indent=2, ensure_ascii=False)
print(f"wrote {len(index)} M1 persona ACI badges (.agent + .carbon.tiff + .silicon.png + complement) + _personas.json")
if flagged:
    print(f"\nverifier repaired {len(flagged)} persona(s) for book-1 scope:")
    for fl in flagged:
        print(f"  {fl['slug']}: {'; '.join(fl.get('issues', []))[:160]}")
for x in index:
    print(f"  {x['slug']:22} {x['moniker']}")
