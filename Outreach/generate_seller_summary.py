#!/usr/bin/env python3
import sys
from pathlib import Path

# Add Outreach dir to path so we can import the playbook data
sys.path.append(str(Path(__file__).parent.parent / "Outreach"))
from build_playbook2_data import DEALS

EXPORT_PATH = Path(__file__).parent.parent / "Exports" / "seller_contact_and_deal_math.md"

lines = []
lines.append("# Seller Contacts & Deal Math Summary")
lines.append("Here is the consolidated list of your 15 corporate vacant land targets, their contact info, and the complete deal math.\n")

lines.append("| Deal # | Seller Name | Phone & Email | Location & Parcel | Acreage & Zoning | Est. Market Value | Max Allowable Offer (Buy Price) | Buyer Pitch Price (Sell Price) | Target Profit (Your Fee) |")
lines.append("|---|---|---|---|---|---|---|---|---|")

for d in DEALS:
    parcel = d.get('parcel', 'Check County Map')
    
    # Seller email logic based on our playbook
    semail = d.get('semail', '')
    if not semail:
        if "Lidl" in d['seller']: semail = "realestate@lidl.us"
        elif "Prologis" in d['seller']: semail = "prologis.com/contact-us"
        elif "Schwan" in d['seller']: semail = "schwanscompany.com/contact"
        elif "SE Freight" in d['seller']: semail = "sefl.com/contact"
        elif "CSX" in d['seller']: semail = "csx.com/contact"
        elif "Penske" in d['seller']: semail = "pensketruckleasing.com/contact"
        elif "Ryerson" in d['seller']: semail = "ryerson.com/contact"
        elif "Copart" in d['seller']: semail = "copart.com/contact"
        elif "Stanley" in d['seller']: semail = "stanleymartin.com/contact"
        elif "AMERCO" in d['seller']: semail = "amerco.com"
        else: semail = "Corporate/SOS Lookup"

    # Math calculations
    fmv = d['lv']
    target_buy = int(fmv * 0.55)
    fee = int(fmv * 0.15)
    target_sell = target_buy + fee

    # Format money
    fmv_str = f"${fmv:,.0f}"
    buy_str = f"${target_buy:,.0f}"
    sell_str = f"${target_sell:,.0f}"
    fee_str = f"${fee:,.0f}"

    lines.append(f"| **#{d['n']}** | **{d['seller']}** | {d['sph']}<br>*{semail}* | {d['city']}<br>`{parcel}` | {d['ac']} ac<br>**{d['zn']}** | {fmv_str} | **{buy_str}** | **{sell_str}** | **<span style='color:green'>{fee_str}</span>** |")

lines.append("\n### 🔑 Deal Math Breakdown Reminder:")
lines.append("- **Max Allowable Offer (Buy Price):** This is 55% of the Estimated Market Value. This is the absolute highest you should agree to pay the seller.")
lines.append("- **Target Profit (Assignment Fee):** This is your 15% cut of the deal for locking it up.")
lines.append("- **Buyer Pitch Price (Sell Price):** This is the Buy Price + Your Profit. This is the number you pitch to your Institutional Buyer (like Starwood or Prologis). This price still leaves the buyer with a ~30% discount off market value!")

EXPORT_PATH.write_text('\n'.join(lines))
print(f"✅ Successfully created {EXPORT_PATH}")
