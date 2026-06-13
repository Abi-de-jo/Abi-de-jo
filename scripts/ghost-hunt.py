#!/usr/bin/env python3
"""
👻 Ghost Hunt Game — Transforms GitHub contribution graph into a ghost hunt game
Ghosts hide in contribution cells. Hunt them by committing!
"""

import argparse
import random
import xml.etree.ElementTree as ET
from datetime import datetime

NS = {"svg": "http://www.w3.org/2000/svg"}
random.seed(42)

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--input", default="dist/ghost-hunt.svg")
    p.add_argument("--output", default="dist/ghost-hunt-game.svg")
    p.add_argument("--username", default="Abi-de-jo")
    return p.parse_args()

def add_ghost_hunt_theme(root):
    """Add ghost hunt elements to the SVG."""
    
    # Get viewBox dimensions
    vb = root.get("viewBox", "0 0 900 300").split()
    w, h = int(vb[2]), int(vb[3])
    
    # Add ghost hunt header
    header = ET.Element("text")
    header.set("x", str(w // 2))
    header.set("y", "35")
    header.set("text-anchor", "middle")
    header.set("font-family", "system-ui, sans-serif")
    header.set("font-size", "22")
    header.set("font-weight", "800")
    header.set("fill", "#c084fc")
    header.set("letter-spacing", "2")
    header.text = "👻 GHOST HUNT — Catch the ghosts in your commits!"
    root.insert(0, header)

    # Find contribution cells (rects in the SVG that represent contributions)
    rects = root.findall(".//svg:rect", NS)
    cells = []
    
    # Check for cells with fill colors (not background)
    bg_color = "#161b22"
    for rect in rects:
        fill = rect.get("fill", "")
        rx = rect.get("rx", "0")
        if fill and fill != bg_color and fill != "none" and rx != "0":
            cells.append(rect)
    
    # Ghost cells - randomly select some cells to be "haunted"
    haunted = set()
    ghost_cells = []
    
    if cells:
        # Haunt about 8% of cells with ghosts
        num_ghosts = max(3, len(cells) // 12)
        chosen = random.sample(range(len(cells)), min(num_ghosts, len(cells)))
        
        for idx in chosen:
            rect = cells[idx]
            x = float(rect.get("x", 0))
            y = float(rect.get("y", 0))
            w_cell = float(rect.get("width", 13))
            h_cell = float(rect.get("height", 13))
            
            ghost_cell = ET.Element("text")
            ghost_cell.set("x", str(x + w_cell // 2))
            ghost_cell.set("y", str(y + h_cell - 1))
            ghost_cell.set("text-anchor", "middle")
            ghost_cell.set("font-size", "12")
            ghost_cell.set("dominant-baseline", "central")
            ghost_cell.text = "👻"
            
            # Add animation — ghost appears and disappears
            anim = ET.SubElement(ghost_cell, "animate")
            anim.set("attributeName", "opacity")
            anim.set("values", "1;0;1")
            anim.set("dur", f"{random.uniform(2, 4):.1f}s")
            anim.set("repeatCount", "indefinite")
            
            ghost_cells.append(ghost_cell)
            haunted.add(idx)

    # Add all ghost emojis
    for gc in ghost_cells:
        root.append(gc)

    # Add stats
    total_commits = len(cells)
    ghosts_found = len(haunted)
    
    # Stats box at bottom
    stats_group = ET.Element("g")
    
    stats_bg = ET.SubElement(stats_group, "rect")
    stats_bg.set("x", "20")
    stats_bg.set("y", str(h - 55))
    stats_bg.set("width", str(w - 40))
    stats_bg.set("height", "40")
    stats_bg.set("rx", "8")
    stats_bg.set("fill", "#0d1117")
    stats_bg.set("stroke", "#8b5cf6")
    stats_bg.set("stroke-width", "1")
    stats_bg.set("opacity", "0.8")
    
    stats_text = ET.SubElement(stats_group, "text")
    stats_text.set("x", "30")
    stats_text.set("y", str(h - 32))
    stats_text.set("font-family", "monospace")
    stats_text.set("font-size", "13")
    stats_text.set("fill", "#c4b5fd")
    stats_text.text = f"👻 Ghosts Spotted: {ghosts_found}  |  📦 Total Commits: {total_commits}  |  🕐 Updated: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}"
    
    root.append(stats_group)
    
    # Add play instructions
    tip = ET.Element("text")
    tip.set("x", str(w // 2))
    tip.set("y", str(h - 10))
    tip.set("text-anchor", "middle")
    tip.set("font-family", "monospace")
    tip.set("font-size", "10")
    tip.set("fill", "#6b7280")
    tip.text = "👻 Ghosts hide in contribution cells. Keep committing to hunt them all!"
    root.append(tip)

def main():
    args = parse_args()
    
    tree = ET.parse(args.input)
    root = tree.getroot()
    
    add_ghost_hunt_theme(root)
    
    tree.write(args.output, encoding="unicode")
    print(f"👻 Ghost Hunt game saved to {args.output}")

if __name__ == "__main__":
    main()
