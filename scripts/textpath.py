"""Convertit du texte en chemins SVG (les <img> SVG de GitHub ne chargent pas de polices)."""
from functools import lru_cache
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

FONTS_DIR = Path(__file__).parent / "fonts"  # rempli par fetch-fonts.sh
FONTS = {
    "display": FONTS_DIR / "BigShouldersDisplay[wght].ttf",
    "mono": FONTS_DIR / "MartianMono[wdth,wght].ttf",
}


@lru_cache(maxsize=None)
def font(name, wght, wdth=None):
    f = TTFont(FONTS[name])
    axes = {"wght": wght}
    if wdth is not None:
        axes["wdth"] = wdth
    return instantiateVariableFont(f, axes)


def measure(text, name, wght, size, tracking=0.0, wdth=None):
    f = font(name, wght, wdth)
    cmap, hmtx = f.getBestCmap(), f["hmtx"]
    scale = size / f["head"].unitsPerEm
    total = sum(hmtx[cmap.get(ord(c), cmap[ord("?")])][0] * scale + tracking for c in text)
    return total - tracking if text else 0


def text_path(text, x, y, size, name="mono", wght=400, tracking=0.0, wdth=None, anchor="start"):
    """Renvoie l'attribut d d'un <path> pour `text`, ligne de base en y."""
    f = font(name, wght, wdth)
    cmap, hmtx, gs = f.getBestCmap(), f["hmtx"], f.getGlyphSet()
    scale = size / f["head"].unitsPerEm
    if anchor != "start":
        w = measure(text, name, wght, size, tracking, wdth)
        x -= w if anchor == "end" else w / 2
    pen = SVGPathPen(gs, lambda v: f"{v:.1f}".rstrip("0").rstrip("."))
    cursor = x
    for c in text:
        g = cmap.get(ord(c), cmap[ord("?")])
        gs[g].draw(TransformPen(pen, (scale, 0, 0, -scale, cursor, y)))
        cursor += hmtx[g][0] * scale + tracking
    return pen.getCommands()
