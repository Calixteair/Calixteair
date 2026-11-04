#!/usr/bin/env bash
# Télécharge les polices (OFL) utilisées pour vectoriser le texte des SVG.
set -euo pipefail
dir="$(dirname "$0")/fonts"; mkdir -p "$dir"
base=https://github.com/google/fonts/raw/main/ofl
curl -sfL "$base/bigshouldersdisplay/BigShouldersDisplay%5Bwght%5D.ttf" -o "$dir/BigShouldersDisplay[wght].ttf"
curl -sfL "$base/martianmono/MartianMono%5Bwdth,wght%5D.ttf" -o "$dir/MartianMono[wdth,wght].ttf"
