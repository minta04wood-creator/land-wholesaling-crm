#!/usr/bin/env python3
"""Generate the Contact Match List Scripts file."""
import sys
from pathlib import Path

# Add Outreach dir to path so we can import the playbook data
sys.path.append(str(Path(__file__).parent.parent / "Outreach"))
from build_playbook2_data import DEALS

EXPORT_PATH = Path(__file__).parent.parent / "Exports" / "contact_match_list_scripts.md"

lines = []
lines.append("# MASTER PHONE SCRIPTS: SELLER & BUYER MATCHES")
lines.append("Use these scripts when calling the targeted corporate sellers and their matched institutional buyers.\n")

for d in DEALS:
    lines.append(f"## 🎯 MATCH #{d['n']}: {d['seller']} ➔ {d['b1n']}")
    lines.append(f"**Property:** {d['ac']} acres in {d['city']} (Zoning: {d['zn']})")
    lines.append(f"**Target Buy Price:** ${int(d['lv'] * 0.55):,}  |  **Target Sell Price:** ${int(d['lv'] * 0.55) + int(d['lv'] * 0.15):,}")
    lines.append(f"**Assignment Fee:** ${int(d['lv'] * 0.15):,}")
    lines.append("\n### 📞 SELLER SCRIPT")
    lines.append(f"**Call:** {d['seller']}")
    lines.append(f"**Number:** {d['sph']}")
    lines.append(f"**Script:**")
    for para in d['ss'].split('\n'):
        if para.strip():
            lines.append(f"> {para.strip()}")
    lines.append(f"\n**💡 Leverage / Talking Point:** {d['lev']}")
    
    lines.append("\n### 📞 BUYER SCRIPT")
    lines.append(f"**Call:** {d['b1n']}")
    lines.append(f"**Number:** {d['b1p']}")
    lines.append(f"**Script:**")
    for para in d['bs'].split('\n'):
        if para.strip():
            lines.append(f"> {para.strip()}")
    
    lines.append("\n---\n")

EXPORT_PATH.write_text('\n'.join(lines))
print(f"✅ Successfully created {EXPORT_PATH.name} in the Exports folder.")
