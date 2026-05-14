#!/usr/bin/env python3
"""Generate personalized buyer pitch emails matched to specific properties."""
import sqlite3, os, csv, json
from datetime import datetime
from pathlib import Path

BASE = Path.home() / "Desktop" / "LandWholesaling"
DB = BASE / "landbot.db"
OUT_DIR = BASE / "Outreach" / "Buyer_Pitches"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Verified acquisition contacts for top institutional buyers
BUYER_CONTACTS = {
    "PROLOGIS": {
        "company": "Prologis, Inc.",
        "dept": "Property Acquisitions — Land",
        "contact": "Atlanta Acquisitions Team",
        "phone": "(404) 760-7200",
        "email": "Via prologis.com/contact-us → Select 'Property Acquisitions' → 'Land'",
        "address": "3475 Piedmont Rd NE, Suite 650, Atlanta, GA 30305",
        "parent": None,
    },
    "INVITATION HOMES": {
        "company": "Invitation Homes",
        "dept": "Acquisitions — Southeast Region",
        "contact": "Atlanta Regional Office",
        "phone": "(770) 442-3372",
        "email": "Via invitationhomes.com → Contact Us",
        "address": "8601 Dunwoody Place, Suite 520, Sandy Springs, GA 30350",
        "parent": "IH BORROWER",
    },
    "STARWOOD": {
        "company": "Starwood Capital Group / Starwood Land Advisors",
        "dept": "SFR Acquisitions",
        "contact": "Atlanta Office",
        "phone": "770-541-9046 | SFR: sfr_inquiries@starwood.com",
        "email": "sfr_inquiries@starwood.com",
        "address": "400 Galleria Parkway, Suite 1450, Atlanta, GA 30339",
        "parent": "STAR BORROWER",
    },
    "SHAHEEN": {
        "company": "Shaheen & Company",
        "dept": "Development & Acquisitions",
        "contact": "Ben Newland / Emma Jackson",
        "phone": "(770) 916-1775",
        "email": "info@shaheenco.com",
        "address": "3625 Cumberland Blvd SE, Suite 250, Atlanta, GA 30339",
        "parent": None,
    },
    "TRICON": {
        "company": "Tricon Residential (Blackstone Real Estate)",
        "dept": "Investment & Acquisitions (via Blackstone)",
        "contact": "Corporate Acquisitions",
        "phone": "Via blackstone.com → Real Estate",
        "email": "Via blackstone.com → Contact",
        "address": "Managed by Blackstone Real Estate, NY",
        "parent": "TAH",
    },
    "GEORGIA PIEDMONT LAND TRUST": {
        "company": "Georgia Piedmont Land Trust, Inc.",
        "dept": "Land Conservation & Acquisitions",
        "contact": "GPLT Team",
        "phone": "(678) 884-7588",
        "email": "Via gplt.org → Contact",
        "address": "PO Box 3687, Suwanee, GA 30024",
        "parent": None,
    },
}

def match_contact(owner_name):
    """Try to match an owner name to a known buyer contact."""
    name = owner_name.upper()
    for key, info in BUYER_CONTACTS.items():
        if key in name:
            return info
        if info["parent"] and info["parent"] in name:
            return info
    return None

PITCH_TPL = """Subject: Off-Market Land Opportunity — {acreage} Acres, {zoning_desc}, {site_city} GA
To: {to_email}
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8

{salutation}

PROPERTY DETAILS AT A GLANCE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Location:    {site_address}, {site_city}, GA {site_zip}
  Parcel ID:   {parcel_id}
  Acreage:     {acreage} acres
  Zoning:      {zoning} — {zoning_desc}
  Status:      Vacant Land
  Est. FMV:    {fmv}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{body}

DEAL STRUCTURE:
• This is an off-market, direct-to-principal opportunity
• All-cash or terms available
• Clear title — no encumbrances
• Ready for immediate due diligence

{match_reason}

I'm reaching out because {why_you}, and this {acreage}-acre
{zoning_desc} parcel aligns with your acquisition criteria in
{site_city}.

I'd welcome 15 minutes to discuss whether this fits your
current pipeline. I'm available at your convenience.

Best regards,

[YOUR NAME]
[YOUR TITLE]
[YOUR COMPANY]
[YOUR PHONE]
[YOUR EMAIL]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BUYER ACQUISITION CONTACT:
  Company:    {buyer_company}
  Department: {buyer_dept}
  Contact:    {buyer_contact}
  Phone:      {buyer_phone}
  Email:      {buyer_email}
  Address:    {buyer_address}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

PITCH_GENERIC = """Subject: Off-Market Land Opportunity — {acreage} Acres, {zoning_desc}, {site_city} GA
To: [SKIP TRACE FOR EMAIL — Owner: {buyer_name}]
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8

Dear {buyer_first_name},

I'm a local land investor in the metro Atlanta area, and I
have an off-market opportunity I think would interest you.

PROPERTY DETAILS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Location:    {site_address}, {site_city}, GA {site_zip}
  Parcel ID:   {parcel_id}
  Acreage:     {acreage} acres
  Zoning:      {zoning} — {zoning_desc}
  Status:      Vacant Land
  Est. FMV:    {fmv}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

I noticed you currently own {buyer_parcels} properties in
Gwinnett County, including other {buyer_zone_match} parcels in
the {buyer_areas} area. This {acreage}-acre parcel is in the
same zone and corridor as your existing portfolio.

I can offer this property at a significant discount to market
value, with a clean title and fast closing.

Would you have 10 minutes this week to discuss?

Best regards,

[YOUR NAME]
[YOUR COMPANY]
[YOUR PHONE]
[YOUR EMAIL]
"""

def main():
    db = sqlite3.connect(str(DB))
    db.row_factory = sqlite3.Row

    # Get top 15 hot leads
    leads = db.execute("""
        SELECT * FROM parcels
        WHERE is_vacant=1 AND is_absentee=1 AND score >= 60
        AND owner_name != '' AND mail_address != ''
        ORDER BY score DESC, acreage DESC LIMIT 15
    """).fetchall()

    # For each lead, find top 3 matched buyers
    from importlib.util import spec_from_file_location, module_from_spec
    import sys
    spec = spec_from_file_location("landbot",
        str(Path.home() / ".agents/skills/land-wholesaler/scripts/landbot.py"))
    lb = module_from_spec(spec)
    sys.modules["landbot"] = lb
    spec.loader.exec_module(lb)

    profiles = lb._build_buyer_profiles(db, "gwinnett")
    total_emails = 0

    for lead in leads:
        p_zoning = (lead["zoning"] or "").strip()
        p_city = (lead["site_city"] or "").strip().upper()
        p_acres = lead["acreage"] or 0
        p_zone_desc = (lead["zoning_desc"] or "").upper()
        p_types = set()
        if "MULTI-FAMILY" in p_zone_desc or p_zoning.startswith("RM"): p_types.add("MULTIFAMILY")
        if "SINGLE FAMILY" in p_zone_desc: p_types.add("SFR")
        if "INDUSTRY" in p_zone_desc or "MANUFACTURING" in p_zone_desc: p_types.add("INDUSTRIAL")
        if "BUSINESS" in p_zone_desc or "COMMERCIAL" in p_zone_desc: p_types.add("COMMERCIAL")
        if "AGRICULTURE" in p_zone_desc or "FOREST" in p_zone_desc: p_types.add("AGRICULTURAL")
        if "OFFICE" in p_zone_desc: p_types.add("OFFICE")

        scored = []
        for b in profiles:
            fit = 0; reasons = []
            type_overlap = p_types & set(b["types"])
            if type_overlap: fit += 40; reasons.append(f"Buys {'/'.join(type_overlap)}")
            if p_zoning in b["zonings"]: fit += 20; reasons.append(f"Same zoning ({p_zoning})")
            if p_city in b["cities"]: fit += 20; reasons.append(f"Active in {p_city}")
            if b["min_acres"] <= p_acres <= b["max_acres"] * 1.5: fit += 10
            if b["total_parcels"] >= 10: fit += 5
            if b["total_parcels"] >= 20: fit += 5
            if fit > 0: scored.append((fit, b, reasons))
        scored.sort(key=lambda x: -x[0])

        pid_safe = lead["parcel_id"].replace(" ", "_").replace("/", "-")

        for rank, (fit, buyer, reasons) in enumerate(scored[:3], 1):
            contact = match_contact(buyer["owner_name"])
            bname_safe = buyer["owner_name"][:30].replace(" ", "_").replace("/", "-")
            fname = OUT_DIR / f"Pitch_{pid_safe}_to_{bname_safe}.eml"

            if contact:
                # Institutional buyer — rich template
                body_map = {
                    "MULTIFAMILY": f"I understand {contact['company']} is actively expanding its multifamily portfolio in the Gwinnett County corridor.",
                    "INDUSTRIAL": f"Given {contact['company']}'s significant industrial holdings in the Norcross/Gwinnett submarket, I believe this parcel represents a strategic addition.",
                    "SFR": f"I'm aware that {contact['company']} has been aggressively acquiring single-family residential properties across metro Atlanta.",
                    "COMMERCIAL": f"With {contact['company']}'s existing commercial footprint in Gwinnett, this parcel offers excellent development potential.",
                }
                body = body_map.get(buyer["types"][0], f"I believe this property aligns with {contact['company']}'s current acquisition strategy in metro Atlanta.")

                content = PITCH_TPL.format(
                    salutation=f"Dear {contact['contact']},\n\nRE: Acquisitions Department — {contact['dept']}",
                    site_address=lead["site_address"] or "N/A",
                    site_city=lead["site_city"] or "Gwinnett",
                    site_zip=lead["site_zip"] or "",
                    parcel_id=lead["parcel_id"],
                    acreage=f"{p_acres:.1f}",
                    zoning=lead["zoning"] or "N/A",
                    zoning_desc=lead["zoning_desc"] or "N/A",
                    fmv=f"${(lead['estimated_fmv'] or 0):,.0f}",
                    body=body,
                    match_reason=f"MATCH CONFIDENCE: {fit}/100\n  Reason: {' | '.join(reasons)}",
                    why_you=f"your firm currently holds {buyer['total_parcels']} properties (${buyer['portfolio_value']:,.0f} portfolio) in Gwinnett County",
                    to_email=contact["email"],
                    buyer_company=contact["company"],
                    buyer_dept=contact["dept"],
                    buyer_contact=contact["contact"],
                    buyer_phone=contact["phone"],
                    buyer_email=contact["email"],
                    buyer_address=contact["address"],
                )
            else:
                # Private/unknown buyer — generic but personalized
                first = buyer["owner_name"].split()[1].title() if len(buyer["owner_name"].split()) >= 2 else buyer["owner_name"].split()[0].title()
                for suffix in ["LLC","LP","INC","CORP","TRUST","ASSOCIATION","ASSN"]:
                    if suffix in buyer["owner_name"].upper():
                        first = "Acquisitions Team"
                        break

                content = PITCH_GENERIC.format(
                    buyer_name=buyer["owner_name"],
                    buyer_first_name=first,
                    site_address=lead["site_address"] or "N/A",
                    site_city=lead["site_city"] or "Gwinnett",
                    site_zip=lead["site_zip"] or "",
                    parcel_id=lead["parcel_id"],
                    acreage=f"{p_acres:.1f}",
                    zoning=lead["zoning"] or "N/A",
                    zoning_desc=lead["zoning_desc"] or "N/A",
                    fmv=f"${(lead['estimated_fmv'] or 0):,.0f}",
                    buyer_parcels=buyer["total_parcels"],
                    buyer_zone_match=lead["zoning_desc"] or "zoned",
                    buyer_areas=", ".join(list(buyer["cities"])[:3]),
                )

            with open(fname, "w") as f:
                f.write(content)
            total_emails += 1

    print(f"Generated {total_emails} personalized buyer pitch emails in:")
    print(f"  {OUT_DIR}/")
    print(f"\nBreakdown: {len(leads)} properties × top 3 matched buyers each")
    print(f"\nIMPORTANT: Replace [YOUR NAME], [YOUR COMPANY], etc. before sending.")

if __name__ == "__main__":
    main()
