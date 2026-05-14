#!/usr/bin/env python3
"""Build Deal Playbook #2 — 15 new leads with scripts, deal math, links."""
from build_playbook2_data import DEALS
from pathlib import Path

OUT = Path(__file__).parent
lines = []
lines.append("="*80)
lines.append("  DEAL PLAYBOOK #2 — 15 NEW LEADS | MASTER CALL SCRIPTS")
lines.append("  All Verified Corporate Contacts | Updated May 2026")
lines.append("="*80)
lines.append("\nREPLACE: [YOUR NAME] [YOUR PHONE] [YOUR EMAIL]\n")

for d in DEALS:
    offer = int(d['lv'] * 0.55)
    fee = int(d['lv'] * 0.15)
    buyer_pays = offer + fee
    gmap = f"https://www.google.com/maps/search/{d['addr'].replace(' ','+')},+{d['city']},+GA+{d['zp']}"
    earth = f"https://earth.google.com/web/search/{d['addr'].replace(' ','+')},+{d['city']},+GA+{d['zp']}"

    lines.append("="*80)
    lines.append(f"  DEAL #{d['n']} — ${fee:,} ASSIGNMENT FEE")
    lines.append(f"  {d['addr']}, {d['city']}, GA {d['zp']}")
    lines.append("="*80)
    lines.append(f"\n  VIEW PROPERTY:")
    lines.append(f"    Google Maps:  {gmap}")
    lines.append(f"    Google Earth: {earth}")
    lines.append(f"\n  DEAL MATH:")
    lines.append(f"    Land Value:   ${d['lv']:,}")
    lines.append(f"    Your Offer:   ${offer:,} (55% of value)")
    lines.append(f"    Your Fee:     ${fee:,}")
    lines.append(f"    Buyer Pays:   ${buyer_pays:,} (30% below value)")
    lines.append(f"\n  PROPERTY:")
    lines.append(f"    Acreage:      {d['ac']} acres")
    lines.append(f"    Zoning:       {d['zn']}")
    lines.append(f"    Liens:        {d['liens']}")
    lines.append(f"    Held:         {d['held']}")
    lines.append(f"    Paid:         {d['paid']}")
    lines.append(f"\n  SELLER:")
    lines.append(f"    Name:         {d['seller']}")
    lines.append(f"    Location:     {d['sloc']}")
    lines.append(f"    Phone:        {d['sph']}")
    lines.append(f"    Email/Web:    {d['sem']}")
    lines.append(f"\n" + "-"*80)
    lines.append(f"  SELLER CALL SCRIPT")
    lines.append("-"*80)
    for l in d['ss'].split('\n'): lines.append(f"    {l}")
    lines.append(f"\n  LEVERAGE: {d['lev']}")
    lines.append(f"\n" + "-"*80)
    lines.append(f"  BUYER #1: {d['b1n']}")
    lines.append(f"    Phone: {d['b1p']} | Email: {d['b1e']}")
    lines.append("-"*80)
    for l in d['bs'].split('\n'): lines.append(f"    {l}")
    lines.append(f"\n  BUYER #2: {d['b2n']}")
    lines.append(f"    Phone: {d['b2p']} | Email: {d['b2e']}")
    lines.append("\n")

lines.append("="*80)
lines.append("  PRIORITY CALL ORDER")
lines.append("="*80)
order = [
    ("#5 CSX (36 yrs)","(877) 835-8279","36 years. Railroad surplus. Dedicated RE dept."),
    ("#4 Lidl US","(703) 214-3433","Dedicated RE email: realestate@lidl.us"),
    ("#1 Prologis","(678) 249-7001","43 acres. Duke legacy. Kent Mason."),
    ("#3 SE Freight","(803) 794-7300","12 acres. Trucking surplus."),
    ("#2 Schwan's","(800) 533-5290","15.7 acres. Post-acquisition."),
    ("#8 Copart","(972) 868-4400","NASDAQ. Paid $295K."),
    ("#6 Penske","(855) 345-7268","Legacy Rollins asset. Doraville boom."),
    ("#7 Ryerson","(312) 292-5000","NYSE steel co. Non-core land."),
    ("#9 Stanley Martin","(703) 621-2050","National builder surplus."),
    ("#10 AMERCO","(602) 263-6645","U-Haul. Paid $3.5M."),
]
for i,(deal,ph,why) in enumerate(order,1):
    lines.append(f"  {i:>2}. {deal:<22} {ph:<22} {why}")

(OUT / "Call_Script_Playbook2.txt").write_text('\n'.join(lines))
print(f"Done: Call_Script_Playbook2.txt — {len(DEALS)} deals, {len(lines)} lines")
