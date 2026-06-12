#!/usr/bin/env python3
"""
HORROR CONTRIBUTION GRAVEYARD — Horror Game SVG Generator
Fetches real GitHub contributions and generates an animated horror-themed SVG.

Usage:
    python generate-horror.py --username Abi-de-jo [--output dist/horror.svg] [--token ghp_xxx]
"""

import json
import os
import sys
import argparse
import random
from datetime import datetime, timezone
from xml.sax.saxutils import escape as xml_escape

# ─── GitHub API ──────────────────────────────────────────────────────────────

GRAPHQL_QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            contributionCount
            contributionLevel
            date
            weekday
          }
        }
      }
    }
  }
}
"""


def fetch_contributions(username: str, token: str | None = None) -> dict:
    """Fetch contribution calendar data from GitHub GraphQL API."""
    token = token or os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        print("::warning::No GitHub token found. Using mock data.", file=sys.stderr)
        return _mock_data()

    import urllib.request

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    body = json.dumps({"query": GRAPHQL_QUERY, "variables": {"login": username}}).encode()
    req = urllib.request.Request(
        "https://api.github.com/graphql", data=body, headers=headers, method="POST"
    )
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
        if "errors" in data:
            print(f"::warning::GraphQL errors: {data['errors']}", file=sys.stderr)
            return _mock_data()
        return data["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    except Exception as e:
        print(f"::warning::Failed to fetch contributions: {e}", file=sys.stderr)
        return _mock_data()


def _mock_data() -> dict:
    """Generate mock contribution data for local preview."""
    from datetime import timedelta

    weeks = []
    today = datetime.now(timezone.utc)
    for w in range(52):
        days = []
        for d in range(7):
            date = today - timedelta(weeks=52 - w, days=6 - d)
            count = random.randint(0, 12)
            days.append({
                "contributionCount": count,
                "contributionLevel": _level_name(count),
                "date": date.strftime("%Y-%m-%d"),
                "weekday": d,
            })
        weeks.append({"contributionDays": days})
    return {"totalContributions": 1276, "weeks": weeks}


def _level_name(count: int) -> str:
    if count == 0:
        return "NONE"
    if count <= 3:
        return "FIRST_QUARTILE"
    if count <= 6:
        return "SECOND_QUARTILE"
    if count <= 9:
        return "THIRD_QUARTILE"
    return "FOURTH_QUARTILE"


# ─── SVG Generator ───────────────────────────────────────────────────────────

CELL_SIZE = 10
CELL_GAP = 4
STEP = CELL_SIZE + CELL_GAP
ROWS = 7


def generate_horror_svg(calendar: dict, username: str) -> str:
    """Generate horror-themed contribution graveyard SVG."""
    weeks_data = calendar["weeks"]
    total_commits = calendar["totalContributions"]

    cols = len(weeks_data)
    grid_x_offset = 40
    top_padding = 55

    house_x = grid_x_offset + (cols * STEP) + 15
    width = house_x + 90
    ground_y = top_padding + (ROWS * STEP) + 5
    height = ground_y + 55

    level_map = {
        "NONE": "empty",
        "FIRST_QUARTILE": "fog",
        "SECOND_QUARTILE": "crypt",
        "THIRD_QUARTILE": "ghost",
        "FOURTH_QUARTILE": "skull",
    }

    random.seed(42)

    svg = [
        f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" '
        f'xmlns="http://www.w3.org/2000/svg" role="img" '
        f'aria-label="Horror contribution graveyard for {username}">',
        f'<desc>Horror-themed contribution grid showing {total_commits:,} commits as a haunted graveyard.</desc>',
        "<style>",
        "  .bg { fill: #0a0a0f; }",
        "  .ground { fill: #1a1a1a; }",
        "  .ground-top { fill: #2a0a0a; }",
        "  .empty { fill: rgba(30,30,30,0.4); rx: 1; ry: 1; }",
        "  .fog { fill: #1a1a2e; rx: 1; ry: 1; stroke: #16213e; stroke-width: 0.5; }",
        "  .crypt { fill: #1a0a2e; rx: 1; ry: 1; stroke: #4a1a5e; stroke-width: 0.5; }",
        "  .ghost { fill: #0a2a1e; rx: 1; ry: 1; stroke: #1a4a2e; stroke-width: 0.5; }",
        "  .skull { fill: #2a0a0a; rx: 1; ry: 1; stroke: #5a1a1a; stroke-width: 0.5; }",
        "  @keyframes flicker { 0%,100%{opacity:1} 50%{opacity:0.7} }",
        "  @keyframes float { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-8px)} }",
        "  @keyframes drift { 0%{transform:translateX(0)} 100%{transform:translateX(-20px)} }",
        "  @keyframes pulse-skull { 0%,100%{opacity:0.6} 50%{opacity:1} }",
        "</style>",
        "<defs>",
    ]

    # ── CHARACTER: Hooded Wanderer ──
    hooded = [
        "     DDD     ",
        "    DDDDD    ",
        "   DDDDDDD   ",
        "   DFFFDFF   ",
        "   DFEEFEE   ",
        "    FFFF     ",
        "   CCCCCC    ",
        "  CCCCCCCC   ",
        "  CC  CC     ",
        "  LL  LL     ",
    ]
    hooded_colors = {"D": "#1a1a1a", "F": "#2a2a2a", "E": "#ff4444", "C": "#3a1a2a", "L": "#1a0a1a"}

    svg.append('  <g id="hooded">')
    for y_idx, row in enumerate(hooded):
        for x_idx, ch in enumerate(row):
            if ch in hooded_colors:
                px = x_idx * 1.2
                py = y_idx * 1.2
                svg.append(f'    <rect x="{px:.1f}" y="{py:.1f}" width="1.2" height="1.2" fill="{hooded_colors[ch]}" />')
    svg.append("  </g>")

    # ── Bat sprite ──
    bat_pixels = [
        "  B   B  ",
        " BB B BB ",
        "BBBBBBBBB",
        " BBB BBB ",
        "  B   B  ",
    ]
    svg.append('  <g id="bat">')
    for y_idx, row in enumerate(bat_pixels):
        for x_idx, ch in enumerate(row):
            if ch == "B":
                svg.append(f'    <rect x="{x_idx*1.0:.1f}" y="{y_idx*1.0:.1f}" width="1" height="1" fill="#2a2a2a" />')
    svg.append("  </g>")

    # ── Skull sprite ──
    skull_pixels = [
        " WWWW ",
        "WWWWWW",
        "WBWWBW",
        "WWWWWW",
        " WW WW",
        " W  W ",
    ]
    svg.append('  <g id="skull">')
    for y_idx, row in enumerate(skull_pixels):
        for x_idx, ch in enumerate(row):
            if ch == "W":
                svg.append(f'    <rect x="{x_idx*0.8:.1f}" y="{y_idx*0.8:.1f}" width="0.8" height="0.8" fill="#cccccc" />')
            elif ch == "B":
                svg.append(f'    <rect x="{x_idx*0.8:.1f}" y="{y_idx*0.8:.1f}" width="0.8" height="0.8" fill="#1a1a1a" />')
    svg.append("  </g>")

    # ── Cross ──
    svg.append('  <g id="cross">')
    svg.append('    <rect x="3" y="0" width="2" height="8" fill="#3a3a3a" />')
    svg.append('    <rect x="0" y="2" width="8" height="2" fill="#3a3a3a" />')
    svg.append("  </g>")

    # ── Tombstone ──
    svg.append('  <g id="tomb">')
    svg.append('    <rect x="1" y="3" width="6" height="5" fill="#2a2a2a" stroke="#3a3a3a" />')
    svg.append('    <path d="M1,3 A3,3 0 0,1 7,3" fill="#2a2a2a" stroke="#3a3a3a" />')
    svg.append("  </g>")

    svg.append("</defs>")

    # ── SKY ──
    svg.append(f'  <rect width="100%" height="100%" class="bg" />')

    # Moon
    svg.append(f'  <circle cx="{width-60}" cy="20" r="14" fill="#ddd" opacity="0.9" />')
    svg.append(f'  <circle cx="{width-57}" cy="18" r="12" fill="#0a0a0f" />')

    # Stars
    for i in range(20):
        sx = random.randint(10, width - 80)
        sy = random.randint(2, top_padding - 10)
        dur = random.uniform(2, 5)
        svg.append(f'  <circle cx="{sx}" cy="{sy}" r="0.5" fill="#ffffff" opacity="0.3">')
        svg.append(f'    <animate attributeName="opacity" values="0.3;0.8;0.3" dur="{dur:.1f}s" repeatCount="indefinite" />')
        svg.append("  </circle>")

    # ── GROUND ──
    svg.append(f'  <rect x="0" y="{ground_y}" width="{width}" height="{height - ground_y}" class="ground" />')
    svg.append(f'  <rect x="0" y="{ground_y}" width="{width}" height="2" class="ground-top" />')

    # Dead trees
    for i in range(5):
        tx = random.randint(20, width - 100)
        svg.append(f'  <line x1="{tx}" y1="{ground_y}" x2="{tx}" y2="{ground_y-25}" stroke="#2a1a1a" stroke-width="2" />')
        svg.append(f'  <line x1="{tx}" y1="{ground_y-18}" x2="{tx-8}" y2="{ground_y-28}" stroke="#2a1a1a" stroke-width="1.5" />')
        svg.append(f'  <line x1="{tx}" y1="{ground_y-12}" x2="{tx+6}" y2="{ground_y-22}" stroke="#2a1a1a" stroke-width="1.5" />')

    # ── FOG ──
    for i in range(3):
        fy = ground_y - 5 + (i * 4)
        svg.append(f'  <rect x="0" y="{fy}" width="{width}" height="8" fill="#1a1a2e" opacity="{0.15 - i*0.04}">')
        svg.append(f'    <animate attributeName="x" values="0;-20;0" dur="{8+i*3}s" repeatCount="indefinite" />')
        svg.append("  </rect>")

    # ── BAT SWARMS ──
    for i in range(6):
        bx = random.randint(50, width - 120)
        by = random.randint(5, top_padding - 15)
        dur = random.uniform(12, 20)
        delay = random.uniform(0, 5)
        svg.append(f'  <use href="#bat" x="{bx}" y="{by}" transform="scale(0.8)">')
        svg.append(f'    <animate attributeName="x" from="{bx}" to="{bx+80}" dur="{dur:.1f}s" begin="{delay:.1f}s" repeatCount="indefinite" />')
        svg.append(f'    <animate attributeName="y" values="{by};{by-10};{by};{by+5};{by}" dur="{dur:.1f}s" begin="{delay:.1f}s" repeatCount="indefinite" />')
        svg.append("  </use>")

    # ── CONTRIBUTION GRID (tombstones) ──
    path_points = []
    character_height = 12

    for col, week in enumerate(weeks_data):
        highest_block_row = ROWS
        col_x = grid_x_offset + col * STEP

        for row, day in enumerate(week["contributionDays"]):
            lvl = level_map.get(day.get("contributionLevel", "NONE"), "empty")
            block_y = top_padding + row * STEP

            svg.append(f'  <rect x="{col_x}" y="{block_y}" width="{CELL_SIZE}" height="{CELL_SIZE}" class="{lvl}" />')

            if lvl != "empty":
                if row < highest_block_row:
                    highest_block_row = row

            if lvl == "skull":
                svg.append(f'  <use href="#skull" x="{col_x-1}" y="{block_y-5}" transform="scale(0.7)" opacity="0.7">')
                svg.append(f'    <animate attributeName="opacity" values="0.5;0.9;0.5" dur="3s" repeatCount="indefinite" />')
                svg.append("  </use>")

            if lvl == "ghost":
                svg.append(f'  <use href="#cross" x="{col_x+1}" y="{block_y-6}" transform="scale(0.6)" opacity="0.5" />')

        target_x = col_x
        target_y = top_padding + highest_block_row * STEP - character_height
        path_points.append((target_x, target_y))

    # ── PATH (wandering through graveyard) ──
    if path_points:
        path_d = f"M {grid_x_offset} {ground_y - character_height}"
        for idx, (px, py) in enumerate(path_points):
            if idx > 0:
                prev_x, prev_y = path_points[idx - 1]
                mid_x = (prev_x + px) / 2
            else:
                mid_x = px
            path_d += f" Q {mid_x} {py - 15} {px} {py}"

        last_x, last_y = path_points[-1]
        path_d += f" Q {last_x + 10} {last_y - 15} {house_x + 20} {ground_y - character_height}"

        svg.append(f'  <path id="horror-path" d="{path_d}" fill="none" stroke="none" />')
        svg.append('  <use href="#hooded">')
        svg.append('    <animateMotion dur="25s" repeatCount="indefinite">')
        svg.append('      <mpath href="#horror-path"/>')
        svg.append("    </animateMotion>")
        svg.append("  </use>")

    # ── HAUNTED HOUSE ──
    hy = ground_y - 50
    svg.append("  <!-- Haunted House -->")
    svg.append(f'  <path d="M {house_x} {ground_y} L {house_x} {hy} L {house_x+25} {hy-20} L {house_x+50} {hy} L {house_x+50} {ground_y} Z" fill="#1a0a1a" stroke="#2a1a2a" stroke-width="1" />')
    svg.append(f'  <rect x="{house_x+10}" y="{hy+15}" width="12" height="18" fill="#0a0a0f" />')
    svg.append(f'  <rect x="{house_x+28}" y="{hy+15}" width="12" height="18" fill="#0a0a0f" />')

    # Glowing windows
    svg.append(f'  <rect x="{house_x+12}" y="{hy+17}" width="8" height="12" fill="#ff4400" opacity="0.6">')
    svg.append(f'    <animate attributeName="opacity" values="0.4;0.8;0.4" dur="2s" repeatCount="indefinite" />')
    svg.append("  </rect>")
    svg.append(f'  <rect x="{house_x+30}" y="{hy+17}" width="8" height="12" fill="#ff4400" opacity="0.4">')
    svg.append(f'    <animate attributeName="opacity" values="0.6;0.3;0.6" dur="3s" repeatCount="indefinite" />')
    svg.append("  </rect>")

    # Door
    svg.append(f'  <rect x="{house_x+20}" y="{hy+25}" width="10" height="25" fill="#0a0505" />')

    # Roof cross
    svg.append(f'  <line x1="{house_x+25}" y1="{hy-25}" x2="{house_x+25}" y2="{hy-15}" stroke="#3a3a3a" stroke-width="1.5" />')
    svg.append(f'  <line x1="{house_x+21}" y1="{hy-21}" x2="{house_x+29}" y2="{hy-21}" stroke="#3a3a3a" stroke-width="1.5" />')

    # ── GRAVE MARKERS ──
    for i in range(8):
        gx = random.randint(grid_x_offset + cols * STEP + 5, house_x - 5)
        svg.append(f'  <use href="#tomb" x="{gx}" y="{ground_y-8}" transform="scale(0.7)" opacity="0.6" />')

    # ── LIGHTNING ──
    lx = random.randint(50, width - 100)
    svg.append(f'  <polyline points="{lx},{top_padding-15} {lx-5},{top_padding+5} {lx+3},{top_padding+5} {lx-2},{top_padding+25}" fill="none" stroke="#ffffaa" stroke-width="1" opacity="0">')
    svg.append(f'    <animate attributeName="opacity" values="0;0;0;0.8;0;0.5;0;0" dur="8s" repeatCount="indefinite" />')
    svg.append("  </polyline>")

    # ── TITLE ──
    svg.append(f'  <text x="{grid_x_offset}" y="{top_padding-25}" fill="#ff4444" font-family="monospace" font-weight="bold" font-size="16" letter-spacing="2">')
    svg.append(f"    {xml_escape(username.upper())}")
    svg.append(f'    <animate attributeName="opacity" values="1;0.6;1" dur="3s" repeatCount="indefinite" />')
    svg.append("  </text>")
    svg.append(f'  <text x="{grid_x_offset}" y="{top_padding-12}" fill="#666" font-family="monospace" font-size="10" letter-spacing="1">')
    svg.append("    contribution graveyard")
    svg.append("  </text>")

    # ── STATS ──
    svg.append(f'  <text x="{width - 100}" y="{top_padding-25}" fill="#ff4444" font-family="monospace" font-size="10" text-anchor="end">')
    svg.append(f"    {total_commits:,} commits")
    svg.append("  </text>")

    # ── LEGEND ──
    legend_y = ground_y + 10
    legend_x = grid_x_offset
    items = [("empty", "No commits"), ("fog", "Low"), ("crypt", "Medium"), ("ghost", "High"), ("skull", "Maximum")]
    for i, (cls, label) in enumerate(items):
        lx = legend_x + i * 80
        svg.append(f'  <rect x="{lx}" y="{legend_y}" width="8" height="8" class="{cls}" />')
        svg.append(f'  <text x="{lx+12}" y="{legend_y+7}" fill="#555" font-family="monospace" font-size="7">{label}</text>')

    # ── FOOTER ──
    svg.append(f'  <text x="{width // 2}" y="{height - 8}" fill="#333" font-family="monospace" font-size="7" text-anchor="middle">')
    svg.append(f"    github.com/{xml_escape(username)}/{xml_escape(username)}")
    svg.append("  </text>")

    svg.append("</svg>")

    return "\n".join(svg)


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Generate horror contribution graveyard SVG")
    parser.add_argument("--username", default="Abi-de-jo", help="GitHub username")
    parser.add_argument("--output", default="dist/horror.svg", help="Output SVG path")
    parser.add_argument("--token", default=None, help="GitHub token")
    args = parser.parse_args()

    print(f":: Fetching contributions for {args.username} ...", file=sys.stderr)
    calendar = fetch_contributions(args.username, args.token)

    print(f":: Generating horror SVG ({calendar['totalContributions']:,} commits) ...", file=sys.stderr)
    svg = generate_horror_svg(calendar, args.username)

    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(svg)

    print(f":: Written to {args.output} ({os.path.getsize(args.output):,} bytes)", file=sys.stderr)


if __name__ == "__main__":
    main()
