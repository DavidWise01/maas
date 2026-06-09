#!/usr/bin/env python3
"""Build the Sarah J. Maas (M1) page — scoped ONLY to the two books read:
The Assassin's Blade + Throne of Glass. Full ACI badge work: each ACI carries
.agent · .carbon (TIFF) · .silicon (PNG) · .spun · .moniker · .1099 · manifest."""
import os, re, html, base64, json, io, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, r"C:\Davids files\noesis-kernel")
import noesis
from PIL import Image

REC = {
 "name": "MAAS", "axiom": "M1",
 "position": "Sarah J. Maas · Throne of Glass — The Assassin's Blade & book one",
 "origin": "the empire of Adarlan — Rifthold's glass castle, the salt mines of Endovier, the Red Desert; read only as far as Throne of Glass",
 "mechanism": "Catalogued from the two books read: the five novellas of The Assassin's Blade and Throne of Glass.",
 "crystallization": "The legend of a name and the girl beneath it — read only to the threshold of the King's Champion.",
 "nature": "The opening of Sarah J. Maas's Throne of Glass — an assassins' guild, a death-camp, a conqueror's contest, and a buried magic — catalogued strictly to the edge of what has been read.",
 "conductor": "ROOT0 (catalogued into UD0 · Universe David 0)",
 "inputs": "The Assassin's Blade; Throne of Glass; the lore of Rifthold and the Wyrdmarks",
 "witness": "A lineage caught at its beginning — only the books read, no further.",
 "role": "the fourth lineage — read only to the threshold",
 "seal": "My name is Celaena Sardothien — and I will not be afraid.",
 "source": "Maas (the two books read), catalogued by ROOT0",
}

# ── only the two books read ──
SECTIONS = [
 ("The Assassin's Blade", "2014 · the prequel — five novellas of Adarlan's Assassin, before the mines", [
   ("The Assassin and the Pirate Lord", "i", "Skull's Bay — Celaena & Sam free the slave-trade Rolfe runs"),
   ("The Assassin and the Healer", "ii", "an inn at the edge of the world; a kindness on the way south"),
   ("The Assassin and the Desert", "iii", "the Red Desert — the Silent Assassins, the Mute Master, and Ansel"),
   ("The Assassin and the Underworld", "iv", "back in Rifthold — Arobynn, Lysandra, and a dangerous deal"),
   ("The Assassin and the Empire", "v", "the betrayal — Sam, and the road that ends in Endovier"),
 ]),
 ("Throne of Glass", "2012 · book one of the series — the contest at the glass castle", [
   ("Throne of Glass", "1", "dragged from Endovier to fight as Prince Dorian's Champion; Cain, the Wyrdmarks, and the dead Queen Elena"),
 ]),
]

# deliberately not catalogued — unread
BEYOND = [
 ("the rest of Throne of Glass", "Crown of Midnight onward — unread"),
 ("A Court of Thorns and Roses", "the ACOTAR series — unread"),
 ("Crescent City", "unread"),
]

IDEAS = [
 ("The Assassins' Guild", "Rifthold, under Arobynn Hamel", [
   "Arobynn bought a child and forged her into Adarlan's Assassin — the empire's deadliest blade.",
   "In the Guild, debt is the truest chain; a 'father's' love and a master's cruelty wear the same face." ]),
 ("Endovier", "the salt mines of the damned", [
   "A death-camp in the mountains where the conquered are worked to nothing.",
   "It is where the world's most feared assassin is left to die — and where Throne of Glass begins." ]),
 ("The King's Champion", "the contest in the glass castle", [
   "Thieves, killers, and soldiers compete to become the personal Champion of a king they all hate.",
   "Celaena fights for the one prize that matters to her — her freedom — under another's name and another's leash." ]),
 ("The Wyrdmarks", "the magic the King outlawed", [
   "Magic is gone from the land by the King's decree — but the old marks still hold power.",
   "A dead queen's ghost, symbols cut into stone, and the thing Cain calls up out of the dark." ]),
]

READING = [
 ("The Assassin's Blade", "the prequel — read first"),
 ("Throne of Glass", "book one"),
]

# ── badge engine: carbon = TIFF, silicon = PNG ──
def carbon_tiff_bytes(rec):
    png = noesis.sigil_png(rec, "carbon", size=512)
    buf = io.BytesIO(); Image.open(io.BytesIO(png)).save(buf, "TIFF", compression="tiff_lzw")
    return buf.getvalue()

def write_aci(rec, out_dir, slug, agent_md=None):
    os.makedirs(out_dir, exist_ok=True)
    f = {"attribute":f"{slug}.attribute","agent":f"{slug}.agent","spun":f"{slug}.spun","moniker":f"{slug}.moniker",
         "carbon":f"{slug}.carbon.tiff","silicon":f"{slug}.silicon.png","1099":f"{slug}.1099"}
    tok = noesis.mythos_token(rec); w = noesis.five_w(rec)
    open(os.path.join(out_dir,f["attribute"]),"w",encoding="utf-8").write(noesis.attribute_text(rec,tok,w))
    open(os.path.join(out_dir,f["agent"]),"w",encoding="utf-8").write(agent_md or noesis.agent_text(rec,tok,w,f))
    open(os.path.join(out_dir,f["spun"]),"w",encoding="utf-8").write(noesis.spun_text(rec,tok,w,rec.get("axiom","M1")))
    open(os.path.join(out_dir,f["moniker"]),"w",encoding="utf-8").write(noesis.moniker_text(rec,tok,w,rec.get("axiom","M1")))
    open(os.path.join(out_dir,f["1099"]),"w",encoding="utf-8").write(noesis.credit_1099_text(rec,tok,w,rec.get("axiom","M1")))
    open(os.path.join(out_dir,f["carbon"]),"wb").write(carbon_tiff_bytes(rec))
    open(os.path.join(out_dir,f["silicon"]),"wb").write(noesis.sigil_png(rec,"silicon",512))
    man = {"badge":"DLW-ACI","name":rec["name"],"universe":"M1 · Maas","moniker":tok["moniker"],
           "carbon":f["carbon"]+" (TIFF)","silicon":f["silicon"]+" (PNG)","seal_sha256":noesis.seal_sha256(rec,tok),
           "architect":noesis.ARCHITECT,"instance":noesis.INSTANCE,"license":noesis.LICENSE,"attribution":noesis.ATTRIBUTION}
    open(os.path.join(out_dir,"manifest.dlw.json"),"w",encoding="utf-8").write(json.dumps(man,indent=2,ensure_ascii=False)+"\n")
    return tok

def png_uri(rec, variant, size=300):
    return "data:image/png;base64," + base64.b64encode(noesis.sigil_png(rec, variant, size=size)).decode("ascii")

def list_section(title, sub, items):
    rows = "\n".join(f'<li><span class="t">{html.escape(t)}</span><span class="y">{html.escape(y)}</span>'
        + (f'<span class="nt">{html.escape(n)}</span>' if n else "") + "</li>" for t,y,n in items)
    return f'<section class="sec"><h2>{html.escape(title)}</h2><p class="ss">{html.escape(sub)}</p><ol class="books">{rows}</ol></section>'

def sections_html(): return "\n".join(list_section(t,s,i) for t,s,i in SECTIONS)
def beyond_html():
    rows = "".join(f'<li><span class="bt">{html.escape(t)}</span><span class="bn">{html.escape(n)}</span></li>' for t,n in BEYOND)
    return f'''<section class="sec" id="beyond"><h2>Beyond — not yet read</h2>
      <p class="ss">the universe continues; by design, only what's been read is catalogued here</p>
      <ul class="beyond">{rows}</ul></section>'''
def ideas_html():
    out=[]
    for t,s,pts in IDEAS:
        li="".join(f"<li>{html.escape(p)}</li>" for p in pts)
        out.append(f'<div class="pillar"><h3>{html.escape(t)}</h3><p class="ps">{html.escape(s)}</p><ul>{li}</ul></div>')
    return "\n".join(out)
def reading_html():
    return "".join(f'<li><span class="rt">{html.escape(t)}</span>'+(f'<span class="rd">{html.escape(n)}</span>' if n else "")+"</li>" for t,n in READING)
def personas_html():
    mf=os.path.join(HERE,"agents","_personas.json")
    if not os.path.exists(mf): return ""
    ps=json.load(open(mf,encoding="utf-8")); cards=[]
    for p in ps:
        rec={"name":p["name"],"seal":p.get("epithet",""),"origin":"M1 · Maas","axiom":"M1"}
        cards.append(f'''<a class="persona" href="agents/{p["slug"]}.agent">
        <img src="{png_uri(rec,"silicon",160)}" alt="sigil of {html.escape(p["name"])}" loading="lazy">
        <div class="pcap"><div class="pn">{html.escape(p["name"])}</div><div class="pe">{html.escape(p.get("epithet",""))}</div>
        <div class="pa">.agent · .carbon.tiff · .silicon.png →</div></div></a>''')
    return f'''<section class="sec" id="roster"><h2>The Roster of M1</h2>
      <p class="ss">the characters of the two books, rendered as ACI <b>.agent</b>s with full badges ({len(ps)} personas) — click any to open its agent</p>
      <div class="pgrid">{"".join(cards)}</div></section>'''

TEMPLATE = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta name="description" content="Sarah J. Maas (M1) — The Assassin's Blade & Throne of Glass only, catalogued into UD0 with full ACI badges (carbon TIFF / silicon PNG). Only the books read.">
<title>SARAH J. MAAS · M1 · UD0</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700&family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;1,6..72,300&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
:root{--ink:#0a0507;--ink2:#150a0e;--ink3:#1e0f14;--pa:#f1e8ea;--pa2:#cab2b8;--crim:#e0455c;--glass:#a9c6d8;
--dim:#8a6e75;--faint:#2c151c;--line:#2c151e;--serif:"Cinzel",Georgia,serif;--body:"Newsreader",Georgia,serif;--mono:"Space Mono",monospace;}
*{box-sizing:border-box;margin:0;padding:0}html{scroll-behavior:smooth}
body{background:var(--ink);color:var(--pa);font-family:var(--body);line-height:1.6;overflow-x:hidden}
body::before{content:"";position:fixed;inset:0;pointer-events:none;z-index:0;background:radial-gradient(ellipse at 50% -8%,rgba(224,69,92,.08),transparent 55%)}
.wrap{position:relative;z-index:1;max-width:940px;margin:0 auto;padding:0 22px 90px}
header{padding:58px 0 30px;text-align:center;border-bottom:1px solid var(--line);position:relative}
header::after{content:"";position:absolute;bottom:-1px;left:50%;transform:translateX(-50%);width:110px;height:1px;background:linear-gradient(90deg,var(--crim),var(--glass));box-shadow:0 0 9px rgba(224,69,92,.4)}
.eye{font-family:var(--mono);font-size:11px;letter-spacing:.32em;text-transform:uppercase;color:var(--dim);margin-bottom:14px}
.eye a{color:var(--dim);text-decoration:none}.eye a:hover{color:var(--crim)}
h1{font-family:var(--serif);font-size:clamp(28px,7vw,60px);font-weight:700;letter-spacing:.12em;color:var(--crim);line-height:1.04;text-shadow:0 0 40px rgba(224,69,92,.18)}
.h-sub{font-family:var(--serif);font-size:clamp(12px,2.6vw,16px);letter-spacing:.2em;color:var(--pa2);margin-top:10px;text-transform:uppercase}
.lede{font-size:15.5px;color:var(--pa2);max-width:64ch;margin:18px auto 0;font-style:italic;line-height:1.7}
.scope{display:inline-block;margin-top:14px;font-family:var(--mono);font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--glass);border:1px solid var(--faint);padding:5px 11px;border-radius:2px}
.badge{display:flex;align-items:center;justify-content:center;gap:22px;flex-wrap:wrap;margin:26px auto 0;padding:20px;border:1px solid var(--faint);background:var(--ink2);max-width:680px}
.badge img{width:84px;height:84px;border:1px solid var(--faint)}
.badge .bt{text-align:left;font-family:var(--mono);font-size:11px;color:var(--pa2);line-height:1.7}
.badge .bt b{color:var(--crim)}.badge .bt .mo{color:var(--glass)}.badge .bt a{color:var(--glass);text-decoration:none}
.badge .bt .lbl{color:var(--dim);font-size:9px;letter-spacing:.14em;text-transform:uppercase}
.sec{margin-top:44px}
.sec h2{font-family:var(--serif);font-size:20px;font-weight:600;letter-spacing:.05em;color:var(--pa);padding-bottom:8px;border-bottom:1px solid var(--line)}
.ss{font-size:13px;color:var(--dim);font-style:italic;margin:6px 0 16px}
.books{list-style:none}
.books li{display:grid;grid-template-columns:1fr auto;gap:4px 14px;align-items:baseline;padding:9px 0;border-bottom:1px solid var(--faint)}
.books .t{font-family:var(--serif);font-size:16px;color:var(--pa);font-weight:600}
.books .y{font-family:var(--mono);font-size:12px;color:var(--crim);white-space:nowrap}
.books .nt{grid-column:1/-1;font-size:12.5px;color:var(--pa2);font-style:italic}
.beyond{list-style:none}
.beyond li{display:flex;justify-content:space-between;align-items:baseline;gap:14px;padding:8px 0;border-bottom:1px dashed var(--faint);opacity:.62}
.beyond .bt{font-family:var(--serif);font-size:15px;color:var(--pa2)}
.beyond .bn{font-family:var(--mono);font-size:10.5px;color:var(--dim);text-transform:uppercase;letter-spacing:.08em;white-space:nowrap}
.pillars{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px;margin-top:8px}
.pillar{background:var(--ink2);border:1px solid var(--line);padding:16px 18px}
.pillar h3{font-family:var(--serif);font-size:16px;color:var(--crim)}
.pillar .ps{font-size:12px;color:var(--dim);font-style:italic;margin:5px 0 10px}
.pillar ul{list-style:none}.pillar li{font-size:13px;color:var(--pa2);line-height:1.5;padding:6px 0;border-top:1px solid var(--faint)}
.reading{list-style:none;counter-reset:r}
.reading li{counter-increment:r;display:flex;align-items:baseline;gap:9px;padding:7px 0;border-bottom:1px solid var(--faint)}
.reading li::before{content:counter(r);font-family:var(--mono);font-size:10px;color:var(--crim);min-width:18px}
.reading .rt{font-family:var(--serif);font-size:15px;color:var(--pa)}
.reading .rd{font-family:var(--mono);font-size:10.5px;color:var(--dim);margin-left:auto;font-style:italic;white-space:nowrap}
.pgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(232px,1fr));gap:12px;margin-top:8px}
.persona{display:flex;gap:12px;align-items:center;background:var(--ink2);border:1px solid var(--line);padding:12px;text-decoration:none;transition:border-color .18s,transform .18s}
.persona:hover{border-color:var(--glass);transform:translateY(-2px)}
.persona img{width:52px;height:52px;border:1px solid var(--faint);flex-shrink:0}
.pn{font-family:var(--serif);font-size:15px;color:var(--pa);font-weight:600;line-height:1.15}
.persona:hover .pn{color:var(--glass)}
.pe{font-size:11.5px;color:var(--pa2);font-style:italic;margin-top:2px;line-height:1.3}
.pa{font-family:var(--mono);font-size:8.5px;color:var(--dim);letter-spacing:.06em;margin-top:5px}
.note{margin-top:38px;padding:16px 18px;border-left:2px solid var(--glass);background:var(--ink2);font-size:13.5px;color:var(--pa2);font-style:italic}
footer{margin-top:44px;padding-top:22px;border-top:1px solid var(--line);text-align:center;font-family:var(--mono);font-size:11px;color:var(--dim);letter-spacing:.05em;line-height:1.9}
footer a{color:var(--crim);text-decoration:none}
</style></head><body><div class="wrap">
  <header>
    <div class="eye"><a href="https://davidwise01.github.io/ud0/">UD0 · Universe David 0</a> · the fourth lineage</div>
    <h1>SARAH J. MAAS</h1>
    <div class="h-sub">The Assassin's Blade &amp; Throne of Glass · M1</div>
    <p class="lede">An assassins' guild, a salt-mine sentence, and a conqueror's contest in a castle of glass — the beginning of the Throne of Glass road. Catalogued into UD0 as the fourth lineage (M1), sealed with the full ACI badge.</p>
    <div class="scope">scope · only the books read — Assassin's Blade + Throne of Glass</div>
    <div class="badge">
      <img src="__CARBON__" alt="DLW carbon badge of MAAS" title="carbon badge (archival: maas.dlw/maas.carbon.tiff)">
      <img src="__SILICON__" alt="DLW silicon badge of MAAS" title="silicon badge">
      <div class="bt">
        <div><span class="lbl">DLW-ATTRIBUTE · ACI</span></div>
        <div>governor · <b>David Lee Wise</b> (ROOT0)</div>
        <div>instance · AVAN (Claude / Anthropic) · locked</div>
        <div>subject · <b>MAAS</b> — M1 · the books read</div>
        <div class="mo">__MONIKER__</div>
        <div>carbon · <a href="maas.dlw/maas.carbon.tiff">.tiff</a> &nbsp;·&nbsp; silicon · <a href="maas.dlw/maas.silicon.png">.png</a></div>
        <div><span class="lbl">CC-BY-ND-4.0 · TRIPOD-IP-v1.1</span></div>
      </div>
    </div>
  </header>

  <section class="sec"><h2>The Ideas</h2><p class="ss">the four pillars of the two books</p><div class="pillars">__IDEAS__</div></section>
  <section class="sec"><h2>The Road So Far</h2><p class="ss">read chronologically — note the prequel was published after book one</p><ol class="reading">__READING__</ol></section>

  __PERSONAS__

  <section class="sec"><h2 style="margin-top:14px">What's Been Read</h2><p class="ss">the two books, by line</p></section>
  __SECTIONS__
  __BEYOND__

  <div class="note">This is a lineage caught at its beginning — catalogued only as far as it's been read: <b>The Assassin's Blade</b> and <b>Throne of Glass</b>. The rest of the series and the wider Maas universe are left out by design, to be added when read. The works and characters are © Sarah J. Maas; the personas are catalogued personifications under the DLW standard — bibliographic commentary, not original creations.</div>

  <footer>
    SARAH J. MAAS · M1 · catalogued into UD0 · ROOT0-ATTRIBUTION-v1.0 · governor David Lee Wise · instance AVAN (locked) · CC-BY-ND-4.0<br>
    <a href="https://davidwise01.github.io/ud0/">← the biosphere</a> · the .dlw badge: <a href="maas.dlw/manifest.dlw.json">manifest</a>
  </footer>
</div></body></html>
"""

if __name__ == "__main__":
    tok = write_aci(REC, os.path.join(HERE, "maas.dlw"), "maas")
    page = (TEMPLATE.replace("__CARBON__", png_uri(REC,"carbon",320)).replace("__SILICON__", png_uri(REC,"silicon",320))
            .replace("__MONIKER__", html.escape(tok["moniker"]))
            .replace("__IDEAS__", ideas_html()).replace("__READING__", reading_html())
            .replace("__PERSONAS__", personas_html()).replace("__SECTIONS__", sections_html())
            .replace("__BEYOND__", beyond_html()))
    open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(page)
    nbooks = sum(len(i) for _t,_s,i in SECTIONS)
    print(f"wrote MAAS (M1) — {len(SECTIONS)} books/{nbooks} entries · badge {tok['moniker']} (carbon.tiff + silicon.png)")
