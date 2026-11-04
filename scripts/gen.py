"""Génère les SVG du README de profil GitHub (identité « forge » du portfolio)."""
import random
from pathlib import Path

from textpath import measure, text_path

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(parents=True, exist_ok=True)

VOID, COAL, LINE = "#0d0907", "#1c1411", "#2e221c"
ASH, INK = "#93857b", "#ede5dd"
EMBER, EMBER_HOT = "#ff5a14", "#ffb070"
EASE = "cubic-bezier(0.16, 1, 0.3, 1)"  # ease-out-expo

REDUCED = "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"


def svg(w, h, body, css="", title=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        f'role="img" aria-label="{title}"><title>{title}</title>'
        f"<style>{css}{REDUCED}</style>"
        f'<rect width="{w}" height="{h}" rx="20" fill="{VOID}"/>{body}</svg>'
    )


def p(d, fill=INK, extra=""):
    return f'<path d="{d}" fill="{fill}" {extra}/>'


def mono(t, x, y, size=13, fill=ASH, wght=400, tracking=0.0, anchor="start", extra=""):
    return p(text_path(t, x, y, size, "mono", wght, tracking, wdth=100, anchor=anchor), fill, extra)


def display(t, x, y, size, fill=INK, wght=800, tracking=0.0, anchor="start", extra=""):
    return p(text_path(t, x, y, size, "display", wght, tracking, anchor=anchor), fill, extra)


def kicker(num, label, url, x, y):
    """« 01 · EN LIGNE · domaine » avec un point braise qui pulse."""
    head = f"{num}  ·  {label}  ·  "
    w = measure(head, "mono", 500, 12, 0.6, 100)
    return (
        f'<circle class="live" cx="{x + 5}" cy="{y - 4.5}" r="4.5" fill="{EMBER}"/>'
        + mono(head, x + 20, y, 12, ASH, 500, 0.6)
        + mono(url, x + 20 + w, y, 12, EMBER_HOT, 500, 0.6)
    )


LIVE_CSS = ".live{animation:live 2.4s ease-in-out infinite}@keyframes live{50%{opacity:.25}}"


def header():
    rnd = random.Random(7)
    w, h = 1200, 400
    sparks = []
    for _ in range(34):
        x = rnd.uniform(520, 1180)
        r = rnd.uniform(1.0, 2.8)
        dur = rnd.uniform(3.2, 7.5)
        sparks.append(
            f'<circle class="s" cx="{x:.0f}" cy="{h + 6}" r="{r:.1f}" fill="{rnd.choice([EMBER, EMBER, EMBER_HOT])}" '
            f'style="--dx:{rnd.uniform(-90, 40):.0f}px;--dy:-{rnd.uniform(220, 400):.0f}px;'
            f'animation-duration:{dur:.1f}s;animation-delay:-{rnd.uniform(0, dur):.1f}s"/>'
        )
    first, last = "CALIXTE", "REYMOND"
    gap, avail = 34, w - 128
    size = 300
    while measure(first, "display", 800, size, 2) + gap + measure(last, "display", 800, size, 2) > avail:
        size -= 2
    fx = 64 + measure(first, "display", 800, size, 2) + gap
    tagline = "Cybersécurité · self-hosting · tout tourne sur mon propre serveur"
    tw = measure(tagline, "mono", 400, 16, 0, 100)
    body = (
        '<defs><radialGradient id="heat" cx="82%" cy="112%" r="75%">'
        f'<stop offset="0" stop-color="{EMBER}" stop-opacity=".6"/>'
        f'<stop offset=".45" stop-color="{EMBER}" stop-opacity=".12"/>'
        f'<stop offset="1" stop-color="{EMBER}" stop-opacity="0"/></radialGradient>'
        '<clipPath id="c"><rect width="1200" height="400" rx="20"/></clipPath></defs>'
        f'<g clip-path="url(#c)"><rect width="{w}" height="{h}" fill="url(#heat)" class="breathe"/>'
        + "".join(sparks)
        + "</g>"
        + f'<g class="in">'
        + f'<rect x="64" y="58" width="10" height="10" fill="{EMBER}"/>'
        + mono("CALIXTEAIR  /  PARIS  /  ÉTUDIANT INGÉNIEUR", 88, 68, 13, ASH, 500, 1.2)
        + display(first, 64, 268, size, INK, 800, 2)
        + display(last, fx, 268, size, EMBER, 800, 2)
        + mono(tagline, 66, 326, 16, INK)
        + f'<rect class="cur" x="{66 + tw + 8}" y="312" width="9" height="17" fill="{EMBER}"/>'
        + "</g>"
    )
    css = (
        ".s{animation:rise linear infinite;opacity:0}"
        "@keyframes rise{0%{transform:translate(0,0);opacity:0}12%{opacity:1}"
        "100%{transform:translate(var(--dx),var(--dy));opacity:0}}"
        ".breathe{animation:breathe 6s ease-in-out infinite}@keyframes breathe{50%{opacity:.7}}"
        f".in{{animation:in 1.1s {EASE} both}}@keyframes in{{from{{opacity:0;transform:translateY(14px)}}}}"
        ".cur{animation:blink 1.1s steps(1) infinite}@keyframes blink{50%{opacity:0}}"
    )
    return svg(w, h, body, css, "Calixte Reymond, cybersécurité et self-hosting")


STATIONS = [
    ("2022", "IUT BELFORT", "BUT informatique", "past"),
    ("2024", "BRED", "Alternance dev full stack", "past"),
    ("2025", "ESIEA", "Cycle ingénieur cyber", "past"),
    ("2026", "RATP", "Alternance cybersécurité", "now"),
    ("2028", "INGÉNIEUR", "Terminus", "next"),
]


def station(x, y, year, name, sub, state):
    out = mono(year, x, y - 34, 13, EMBER_HOT if state == "now" else ASH, 500, 1, "middle")
    if state == "now":
        out += f'<circle class="pulse" cx="{x}" cy="{y}" r="13" fill="none" stroke="{EMBER}" stroke-width="3"/>'
        out += f'<circle cx="{x}" cy="{y}" r="11" fill="{EMBER}" stroke="{INK}" stroke-width="5"/>'
    elif state == "next":
        out += f'<circle cx="{x}" cy="{y}" r="11" fill="{VOID}" stroke="{ASH}" stroke-width="4" stroke-dasharray="4 4"/>'
    else:
        out += f'<circle cx="{x}" cy="{y}" r="11" fill="{VOID}" stroke="{INK}" stroke-width="5"/>'
    out += display(name, x, y + 52, 30, ASH if state == "next" else INK, 700, 1, "middle")
    out += mono(sub, x, y + 78, 12, ASH, 400, 0, "middle")
    return out


def timeline():
    w, h, y = 1200, 330, 190
    xs = [130 + i * 235 for i in range(len(STATIONS))]
    now = xs[3]
    body = (
        f'<rect x="56" y="48" width="38" height="38" rx="8" fill="{EMBER}"/>'
        + display("P", 75, 79, 32, VOID, 800, 0, "middle")
        + display("PARCOURS", 110, 79, 34, INK, 800, 2)
        + mono("direction ingénieur cybersécurité", 1144, 74, 13, ASH, 400, 0.4, "end")
        + f'<line x1="{xs[0] - 50}" y1="{y}" x2="{now}" y2="{y}" stroke="{EMBER}" stroke-width="8" stroke-linecap="round"/>'
        + f'<line x1="{now}" y1="{y}" x2="{xs[-1]}" y2="{y}" stroke="{LINE}" stroke-width="8" stroke-dasharray="2 12" stroke-linecap="round"/>'
        + f'<circle r="5" fill="{EMBER_HOT}"><animateMotion dur="5s" repeatCount="indefinite" '
        f'path="M{xs[0] - 50},{y} L{now},{y}" keyPoints="0;1" keyTimes="0;1" calcMode="spline" keySplines=".16 1 .3 1"/>'
        f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.1;.85;1" dur="5s" repeatCount="indefinite"/></circle>'
        + "".join(station(x, y, *s) for x, s in zip(xs, STATIONS))
    )
    css = (
        ".pulse{transform-box:fill-box;transform-origin:center;animation:pulse 2.2s ease-out infinite}"
        "@keyframes pulse{from{transform:scale(1);opacity:.9}to{transform:scale(2.6);opacity:0}}"
    )
    return svg(w, h, body, css, "Parcours : IUT Belfort, BRED, ESIEA, RATP")


def card_text(num, label, url, name, desc, stack, top_motif_end):
    y = top_motif_end
    return (
        kicker(num, label, url, 40, 50)
        + display(name, 40, 116, 62, INK, 800, 1.5)
        + "".join(mono(line, 40, y + 40 + i * 22, 13, INK) for i, line in enumerate(desc))
        + mono(stack, 40, y + 40 + len(desc) * 22 + 22, 11.5, EMBER_HOT, 500, 1.2)
    )


def kalidoku():
    w, h = 590, 420
    words = ["RUST", "SEINE", "PIXEL", "AXUM", "ORBITE", "PONT", "SVELTE", "BAUD"]
    tw, th, gap, x0 = (510 - 24) / 4, 38, 8, 40
    tiles = (
        f'<rect x="{x0}" y="146" width="510" height="{th}" rx="6" fill="{EMBER}"/>'
        + mono("LIGNES DE MÉTRO", x0 + 255, 170, 12.5, VOID, 700, 1.4, "middle")
    )
    for i, word in enumerate(words):
        r, c = divmod(i, 4)
        tx, ty = x0 + c * (tw + gap), 146 + (r + 1) * (th + gap)
        sel = ' class="pick"' if i in (2, 5) else ""
        tiles += f'<rect{sel} x="{tx:.1f}" y="{ty}" width="{tw:.1f}" height="{th}" rx="6" fill="{COAL}" stroke="{LINE}" stroke-width="1.5"/>'
        tiles += mono(word, tx + tw / 2, ty + 24, 12, INK, 500, 1, "middle")
    body = tiles + card_text(
        "02", "JOUER", "kalidoku.calixteair.fr", "KALIDOKU",
        ["Puzzle quotidien façon Connections,", "avec un vrai classement. PWA mobile."],
        "RUST · AXUM · ASTRO · SVELTE 5", 276,
    )
    css = LIVE_CSS + (
        f".pick{{animation:pick 3s {EASE} infinite}}"
        f"@keyframes pick{{0%,30%{{stroke:{LINE}}}40%,80%{{stroke:{EMBER}}}100%{{stroke:{LINE}}}}}"
    )
    return svg(w, h, body, css, "kalidoku, puzzle quotidien")


def chess():
    w, h = 590, 420
    cols, rows, x0, y0 = 12, 3, 40, 146
    sq = 510 / cols
    board = "".join(
        f'<rect x="{x0 + c * sq:.2f}" y="{y0 + r * sq:.2f}" width="{sq + .3:.2f}" height="{sq + .3:.2f}" '
        f'fill="{COAL if (r + c) % 2 else LINE}"/>'
        for r in range(rows) for c in range(cols)
    )
    hops = [(0, 2), (2, 1), (4, 0), (5, 2), (7, 1), (9, 0), (10, 2)]
    pts = [(x0 + (c + .5) * sq, y0 + (r + .5) * sq) for c, r in hops]
    path = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    n = len(pts) - 1
    key_t = ";".join(f"{i / n:.3f}" for i in range(n + 1))
    body = (
        f'<clipPath id="b"><rect x="{x0}" y="{y0}" width="510" height="{rows * sq:.1f}" rx="6"/></clipPath>'
        f'<g clip-path="url(#b)">{board}</g>'
        + f'<path d="{path}" fill="none" stroke="{EMBER}" stroke-width="2" stroke-dasharray="3 6" opacity=".55"/>'
        + f'<circle r="9" fill="{EMBER}" stroke="{INK}" stroke-width="3">'
        f'<animateMotion dur="7s" repeatCount="indefinite" path="{path}" keyPoints="{key_t}" keyTimes="{key_t}" calcMode="linear"/></circle>'
        + card_text(
            "03", "JOUER", "chess.calixteair.fr", "ÉCHECS EN LIGNE",
            ["Moteur de règles, serveur Java multithread,", "clients web React et JavaFX."],
            "JAVA · REACT · TYPESCRIPT", int(y0 + rows * sq),
        )
    )
    return svg(w, h, body, LIVE_CSS, "Jeu d'échecs multijoueur")


def devsecvault():
    w, h = 1200, 300
    rnd = random.Random(3)
    x0, y0, cw, ch = 760, 34, 400, 232
    rows = [" ".join(f"{rnd.randrange(256):02X}" for _ in range(8)) for _ in range(12)]
    lines = "".join(
        mono(r, x0 + 22, y0 + 30 + i * 22, 13, EMBER if rnd.random() < .12 else ASH, 400, 1.5)
        for i, r in enumerate(rows + rows)
    )
    body = (
        f'<defs><linearGradient id="fade" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{VOID}"/><stop offset=".22" stop-color="{VOID}" stop-opacity="0"/>'
        f'<stop offset=".78" stop-color="{VOID}" stop-opacity="0"/><stop offset="1" stop-color="{VOID}"/></linearGradient>'
        f'<clipPath id="k"><rect x="{x0}" y="{y0}" width="{cw}" height="{ch}" rx="12"/></clipPath></defs>'
        f'<rect x="{x0}" y="{y0}" width="{cw}" height="{ch}" rx="12" fill="{COAL}"/>'
        f'<g clip-path="url(#k)"><g class="scroll">{lines}</g>'
        f'<rect class="scan" x="{x0}" y="{y0}" width="{cw}" height="2" fill="{EMBER}"/>'
        f'<rect x="{x0}" y="{y0}" width="{cw}" height="{ch}" fill="url(#fade)"/></g>'
        + mono("AES-256-GCM", x0 + cw - 18, y0 + ch - 16, 11, EMBER_HOT, 600, 1.4, "end")
        + kicker("01", "EN LIGNE", "vault.calixteair.fr", 48, 70)
        + display("DEVSECVAULT", 48, 160, 88, INK, 800, 2)
        + mono("Coffre-fort pour pros de la cyber : payloads chiffrés,", 48, 206, 15, INK)
        + mono("partage de secrets E2E zero-knowledge, 23 outils côté client.", 48, 232, 15, INK)
        + mono("ANGULAR 21 · SYMFONY 8 · KEYCLOAK · MEILISEARCH", 48, 266, 12, EMBER_HOT, 500, 1.2)
    )
    css = LIVE_CSS + (
        f".scroll{{animation:scroll 18s linear infinite}}@keyframes scroll{{to{{transform:translateY(-{12 * 22}px)}}}}"
        f".scan{{animation:scan 4s {EASE} infinite}}@keyframes scan{{to{{transform:translateY({ch}px)}}}}"
    )
    return svg(w, h, body, css, "DevSecVault, coffre-fort pour pros de la cybersécurité")


for name, fn in [("header", header), ("parcours", timeline), ("devsecvault", devsecvault),
                 ("kalidoku", kalidoku), ("chess", chess)]:
    (OUT / f"{name}.svg").write_text(fn())
    print(name, (OUT / f"{name}.svg").stat().st_size)
