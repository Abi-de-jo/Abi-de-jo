#!/usr/bin/env python3
"""
GHOST HUNT — Transform a Platane/snk contribution-snake SVG into a
ghost-hunting themed game SVG.

Reads:   assets/ghost-hunt-game.svg  (created upstream by Platane/snk)
Writes:  assets/ghost-hunt-game.svg  (overwrites with the ghost-hunted version)

The snake is recoloured purple, a "GHOST HUNT" header is dropped on top,
a score / high-score HUD is added, and a handful of 👻 sprites are placed
on randomly chosen active contribution cells.
"""
from __future__ import annotations

import random
import re
import sys
from pathlib import Path

INPUT = Path("assets/ghost-hunt-game.svg")
OUTPUT = INPUT

PURPLE = "#8b5cf6"
PURPLE_LIGHT = "#a78bfa"
PURPLE_BG = "#1a0b2e"
TITLE = "\U0001f47b GHOST HUNT"
GHOST = "\U0001f47b"  # 👻

# Fill colours Platane/snk uses for ACTIVE contribution cells.
ACTIVE_FILLS = {
    "#0e4429", "#006d32", "#26a641", "#39d353",  # github-dark
    "#9be9a8", "#40c463", "#30a14e", "#216e39",  # github-light
}

# Fill colours used for EMPTY / background cells — these are skipped.
EMPTY_FILLS = {
    "#161b22",  # github-dark empty
    "#ebedf0",  # github-light empty
    "#0d1117",  # dark page background
    "none",
    "transparent",
}

EXTRA_CSS = """
    /* Ghost Hunt theme overrides */
    svg path  { stroke: #8b5cf6 !important; }
    svg circle { fill:   #8b5cf6 !important; }
  """


def _attr(attrs: str, name: str) -> str | None:
    m = re.search(rf'{name}="([^"]+)"', attrs)
    return m.group(1) if m else None


def find_active_cells(svg: str) -> list[dict]:
    """Return [{x,y,w,h}, ...] for every active contribution-cell rect."""
    cells: list[dict] = []
    for m in re.finditer(r"<rect\b([^>]*?)/>", svg, re.DOTALL):
        attrs = m.group(1)
        fill = (_attr(attrs, "fill") or "").lower().strip()
        if not fill or fill in EMPTY_FILLS or fill not in ACTIVE_FILLS:
            continue
        try:
            x = float(_attr(attrs, "x") or 0)
            y = float(_attr(attrs, "y") or 0)
            w = float(_attr(attrs, "width") or 0)
            h = float(_attr(attrs, "height") or 0)
        except ValueError:
            continue
        if w == 0 or h == 0:
            continue
        cells.append({"x": x, "y": y, "w": w, "h": h})
    return cells


def make_ghosts(cells: list[dict], target: int) -> tuple[list[str], int]:
    """Build 👻 overlay elements for a random subset of active cells."""
    if not cells:
        return [], 0
    n = min(target, len(cells))
    sample = random.sample(cells, n)
    out: list[str] = []
    for c in sample:
        cx = c["x"] + c["w"] / 2
        cy = c["y"] + c["h"] / 2
        size = c["w"] * 1.7
        delay = random.uniform(0, 4)
        dur = random.uniform(2.5, 4.5)
        out.append(
            f'<text x="{cx:.2f}" y="{cy:.2f}" font-size="{size:.2f}" '
            f'text-anchor="middle" dominant-baseline="central" '
            f'fill="#ffffff" opacity="0.92" style="pointer-events:none">'
            f"{GHOST}"
            f'<animate attributeName="opacity" values="0.25;1;0.25" '
            f'dur="{dur:.2f}s" begin="{delay:.2f}s" repeatCount="indefinite"/>'
            f'<animateTransform attributeName="transform" type="translate" '
            f'values="0,0;0,-2.5;0,0" dur="{dur:.2f}s" begin="{delay:.2f}s" '
            f'repeatCount="indefinite"/>'
            f"</text>"
        )
    return out, n


def make_header(svg_w: int) -> list[str]:
    return [
        f'<rect x="{svg_w/2 - 145:.1f}" y="2" width="290" height="24" '
        f'rx="12" ry="12" fill="{PURPLE_BG}" stroke="{PURPLE}" '
        f'stroke-width="1" opacity="0.9"/>',
        f'<text x="{svg_w/2:.1f}" y="19" '
        f'font-family="Segoe UI, system-ui, sans-serif" font-size="13" '
        f'font-weight="bold" fill="{PURPLE}" text-anchor="middle" '
        f'letter-spacing="2.5">{TITLE}'
        f'<animate attributeName="opacity" values="1;0.55;1" '
        f'dur="2.5s" repeatCount="indefinite"/>'
        f"</text>",
    ]


def make_hud(svg_w: int, score: int, high: int, ghosts: int) -> list[str]:
    return [
        f'<text x="10" y="19" font-family="ui-monospace, monospace" '
        f'font-size="10" fill="{PURPLE_LIGHT}">'
        f"\U0001f7e3 PURPLE SNAKE"
        f"</text>",
        f'<text x="{svg_w - 10:.1f}" y="19" '
        f'font-family="ui-monospace, monospace" font-size="10" '
        f'fill="{PURPLE_LIGHT}" text-anchor="end">'
        f"\U0001f47b {score}/{high} \u00b7 \U0001f47b\u00d7{ghosts}"
        f"</text>",
    ]


def main() -> int:
    if not INPUT.exists():
        print(f"::error::Input SVG not found: {INPUT}", file=sys.stderr)
        print("Make sure Platane/snk ran successfully first.", file=sys.stderr)
        return 1

    svg = INPUT.read_text(encoding="utf-8")
    random.seed()

    # 1) Merge purple-snake CSS into the existing <style> block.
    if "<style" in svg:
        svg = re.sub(r"</style>", EXTRA_CSS + "</style>", svg, count=1)
    else:
        svg = re.sub(
            r"(<svg[^>]*>)",
            r"\1<style>" + EXTRA_CSS + "</style>",
            svg,
            count=1,
        )

    # 2) Figure out SVG width for centred header placement.
    w_match = re.search(r'<svg[^>]*\swidth="(\d+(?:\.\d+)?)"', svg)
    svg_w = int(float(w_match.group(1))) if w_match else 800

    # 3) Locate active cells, then place ghosts on a random subset.
    cells = find_active_cells(svg)
    target = random.randint(8, 20)
    ghosts, actual = make_ghosts(cells, target)

    # 4) Score / header / HUD.
    score = actual * random.randint(1, 3)
    high = score + random.randint(2, 8)
    header = make_header(svg_w)
    hud = make_hud(svg_w, score, high, actual)

    # 5) Inject every overlay right before </svg>.
    overlays = "\n".join(header + hud + ghosts)
    svg = svg.replace("</svg>", overlays + "\n</svg>")

    OUTPUT.write_text(svg, encoding="utf-8")
    print(
        f"\U0001f47b Ghost hunt SVG written to {OUTPUT} "
        f"({len(svg):,} bytes, {actual} ghosts, score={score}/{high})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
