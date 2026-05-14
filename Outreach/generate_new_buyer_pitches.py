#!/usr/bin/env python3
"""Generate personalized pitch emails for 14 NEW institutional buyers matched to all 25 properties."""
from pathlib import Path
from datetime import datetime

BASE = Path.home() / "Desktop" / "LandWholesaling"
OUT_DIR = BASE / "Outreach" / "New_Buyer_Pitches"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ── NEW BUYER CONTACTS ──────────────────────────────────────────────
NEW_BUYERS = {
    "STONEMONT": {
        "company": "Stonemont Financial Group",
        "dept": "Industrial Acquisitions",
        "contact": "Acquisitions Team",
        "phone": "(404) 846-3200",
        "email": "Via stonemontfinancial.com → Contact",
        "address": "Three Alliance Center, 3550 Lenox Rd NE, Suite 1700, Atlanta, GA 30326",
        "types": ["INDUSTRIAL", "COMMERCIAL"],
        "pitch": "Stonemont is Atlanta-headquartered and specializes in industrial real estate, including Industrial Service Facilities and logistics parks. With active projects in Duluth and across Gwinnett County, this parcel fits squarely within your acquisition footprint.",
    },
    "IDI": {
        "company": "IDI Logistics",
        "dept": "Financial Planning & Investments",
        "contact": "Chris Kazanowski, SVP",
        "phone": "(404) 479-1660",
        "email": "chris.kazanowski@idilogistics.com",
        "address": "1100 Peachtree St NE, Suite 1000, Atlanta, GA 30309",
        "types": ["INDUSTRIAL"],
        "pitch": "IDI Logistics, backed by Ivanhoé Cambridge and Oxford Properties, is one of the most active industrial developers in the Southeast. With your Atlanta headquarters and focus on speculative development and build-to-suit logistics, this off-market parcel represents a compelling addition to your development pipeline.",
    },
    "TRAMMELL_CROW": {
        "company": "Trammell Crow Company (CBRE)",
        "dept": "Industrial Development",
        "contact": "Atlanta Development Team",
        "phone": "(404) 923-1544",
        "email": "Via trammellcrow.com → Contact",
        "address": "3550 Lenox Rd NE, Suite 2200, Atlanta, GA 30326",
        "types": ["INDUSTRIAL", "COMMERCIAL"],
        "pitch": "Trammell Crow recently completed the Buford Creek Business Center — a 686,400 SF industrial park in Buford. With CBRE's capital backing and your proven track record in the Gwinnett/Buford submarket, this parcel is a natural fit for your next phase of development.",
    },
    "SCANNELL": {
        "company": "Scannell Properties",
        "dept": "Development — Southeast Region",
        "contact": "Jacob Holdeman, Director of Development",
        "phone": "(317) 843-5959",
        "email": "Via scannellproperties.com → Contact",
        "address": "1776 Peachtree St NW, Suite 280S, Atlanta, GA 30309",
        "types": ["INDUSTRIAL"],
        "pitch": "Scannell Properties has a proven track record of Class A industrial development in the Atlanta market, including Gardner Logistics Park and Chastain Crossings. This highway-accessible industrial parcel aligns with your speculative development strategy.",
    },
    "DERMODY": {
        "company": "Dermody Properties",
        "dept": "Development & Investments — Southeast Region",
        "contact": "Wes Hardy, Partner",
        "phone": "(770) 200-4007",
        "email": "whardy@dermody.com",
        "address": "3715 Davinci Court, Suite 350, Peachtree Corners, GA 30092",
        "types": ["INDUSTRIAL"],
        "pitch": "Dermody Properties just broke ground on LogistiCenter at South Forsyth and recently acquired a 10-acre site for Class A industrial development. With your Southeast office located in Peachtree Corners — right in the heart of Gwinnett — this parcel is in your backyard.",
    },
    "ROCKEFELLER": {
        "company": "Rockefeller Group",
        "dept": "Industrial Logistics Development",
        "contact": "Atlanta Regional Office",
        "phone": "(770) 884-1322",
        "email": "Via rockefellergroup.com → Contact",
        "address": "309 East Paces Ferry Rd NE, Suite 925, Atlanta, GA 30305",
        "types": ["INDUSTRIAL"],
        "pitch": "Rockefeller Group recently completed the Braselton 85 distribution center (427,655 SF) in the I-85 corridor. With your focus on large-scale logistics development in Metro Atlanta, this parcel represents a strategic land banking or development opportunity.",
    },
    "AMH": {
        "company": "American Homes 4 Rent (NYSE: AMH)",
        "dept": "Land Acquisitions — Georgia Market",
        "contact": "Land Acquisitions Team",
        "phone": "(833) 736-8264",
        "email": "Via amh.com → Contact",
        "address": "20 Mansell Ct, Roswell, GA 30076",
        "types": ["SFR", "RESIDENTIAL"],
        "pitch": "American Homes 4 Rent is one of the largest SFR REITs in the US with a massive Atlanta portfolio. This parcel is ideal for a Build-to-Rent community — the fastest-growing segment of SFR development. At this acreage, you're looking at a 50-200 unit BTR subdivision opportunity.",
    },
    "PROGRESS": {
        "company": "Progress Residential (Pretium Partners)",
        "dept": "SFR Acquisitions & BTR Development",
        "contact": "Acquisitions Team",
        "phone": "Via rentprogress.com → Contact",
        "email": "Via pretium.com → Contact",
        "address": "7500 N Dobson Rd, Suite 300, Scottsdale, AZ 85256",
        "types": ["SFR", "RESIDENTIAL"],
        "pitch": "Progress Residential, backed by Pretium Partners, is one of the largest SFR operators in the Atlanta market. With your data-driven acquisition approach and focus on Sun Belt growth markets, this entitled residential parcel presents a Build-to-Rent development opportunity in one of Atlanta's fastest-growing corridors.",
    },
    "DR_HORTON": {
        "company": "D.R. Horton (NYSE: DHI)",
        "dept": "Land Acquisitions — Atlanta East Division",
        "contact": "Land Acquisition Team",
        "phone": "(678) 509-0555",
        "email": "drhorton.com/contact/property-submittal",
        "address": "1371 Dogwood Dr SW, Conyers, GA 30012",
        "types": ["SFR", "RESIDENTIAL"],
        "pitch": "D.R. Horton is America's #1 homebuilder by volume with three Atlanta-area division offices. This entitled residential parcel is ready for subdivision development. I've also submitted details through your Property Submittal Portal for your acquisitions team's review.",
    },
    "TOLL_BROTHERS": {
        "company": "Toll Brothers (NYSE: TOL)",
        "dept": "Land Acquisitions — Georgia Division",
        "contact": "Georgia Division Office",
        "phone": "(888) 686-5542",
        "email": "Via tollbrothers.com → Sell Land to Toll Brothers",
        "address": "2400 Lakeview Pkwy, Alpharetta, GA 30009",
        "types": ["SFR", "RESIDENTIAL"],
        "pitch": "Toll Brothers just launched Ledgestone — your first community in Gwinnett County — with luxury homes starting at $1M+. As you build out your Georgia land pipeline, this premium residential parcel offers exceptional development potential for your luxury brand.",
    },
    "MERITAGE": {
        "company": "Meritage Homes (NYSE: MTH)",
        "dept": "Land Acquisitions — Atlanta Division",
        "contact": "Atlanta Division Land Team",
        "phone": "(678) 348-8350",
        "email": "Via meritagehomes.com → Contact",
        "address": "3700 Mansell Rd, Suite 550, Alpharetta, GA 30022",
        "types": ["SFR", "RESIDENTIAL"],
        "pitch": "Meritage Homes has been one of the most active builders in Gwinnett County since acquiring Legendary Communities. With multiple active communities and a constant need for entitled residential land, this parcel fits your energy-efficient, move-up housing strategy.",
    },
    "CORTLAND": {
        "company": "Cortland",
        "dept": "Development & Acquisitions",
        "contact": "Development Team",
        "phone": "(404) 965-3988",
        "email": "Via cortland.com → Contact",
        "address": "3424 Peachtree Rd NE, Suite 300, Atlanta, GA 30326",
        "types": ["MULTIFAMILY"],
        "pitch": "Cortland is one of the largest vertically integrated multifamily developers in the US, headquartered right here in Atlanta. With in-house construction and design capabilities, this RM-zoned parcel presents a ground-up apartment or townhouse development opportunity in a high-demand Gwinnett submarket.",
    },
    "WOOD_PARTNERS": {
        "company": "Wood Partners",
        "dept": "Development — Southeast Region",
        "contact": "Atlanta Development Team",
        "phone": "Via woodpartners.com → Contact",
        "email": "Via woodpartners.com → Contact",
        "address": "Atlanta, GA (HQ)",
        "types": ["MULTIFAMILY"],
        "pitch": "Wood Partners is one of the top multifamily developers in the country, with your \"Alta\" brand communities across Metro Atlanta. This RM-zoned parcel offers a ground-up apartment development opportunity in a rapidly growing Gwinnett corridor.",
    },
    "WALTON_GLOBAL": {
        "company": "Walton Global",
        "dept": "Land Acquisitions & Banking",
        "contact": "Acquisitions Team",
        "phone": "Via walton.com → Contact",
        "email": "Via walton.com → Contact",
        "address": "Scottsdale, AZ (HQ)",
        "types": ["SFR", "INDUSTRIAL", "COMMERCIAL"],
        "pitch": "Walton Global specializes in pre-development land banking in high-growth corridors, partnering with national builders like D.R. Horton and Meritage for builder take-downs. This large-acreage parcel sits in one of Metro Atlanta's fastest-growing corridors — ideal for your land banking strategy.",
    },
}

# ── PROPERTY DATA (Combined PB1 + PB2) ──────────────────────────────
PROPERTIES = [
    # Playbook 2 — 15 deals
    dict(src="PB2", n=1, addr="4415 Thompson Mill Rd", city="Buford", zp="30519", ac=43.52,
         zn="M1-Light Industry", lv=7502400, ptype="INDUSTRIAL",
         buyers=["STONEMONT","IDI","TRAMMELL_CROW","ROCKEFELLER","SCANNELL"]),
    dict(src="PB2", n=2, addr="2900 Rolling Pin Ln", city="Suwanee", zp="30024", ac=15.69,
         zn="M1-Light Industry", lv=2500000, ptype="INDUSTRIAL",
         buyers=["TRAMMELL_CROW","DERMODY","STONEMONT"]),
    dict(src="PB2", n=3, addr="Windsor Park Dr", city="Suwanee", zp="30024", ac=12.09,
         zn="M1-Light Industry", lv=1689200, ptype="INDUSTRIAL",
         buyers=["DERMODY","TRAMMELL_CROW","SCANNELL"]),
    dict(src="PB2", n=4, addr="2172 Lawrenceville Suwanee Rd", city="Suwanee", zp="30024", ac=7.31,
         zn="C2-General Business", lv=4407500, ptype="COMMERCIAL",
         buyers=["STONEMONT","TRAMMELL_CROW"]),
    dict(src="PB2", n=5, addr="Hwy 316", city="Dacula", zp="30019", ac=10.01,
         zn="M1-Light Industry", lv=500000, ptype="INDUSTRIAL",
         buyers=["SCANNELL","STONEMONT","DERMODY"]),
    dict(src="PB2", n=6, addr="Best Friend Rd", city="Doraville", zp="30340", ac=4.31,
         zn="M1-Light Industry", lv=598100, ptype="INDUSTRIAL",
         buyers=["DERMODY","STONEMONT"]),
    dict(src="PB2", n=7, addr="Turman Dr", city="Berkeley Lake", zp="30071", ac=2.97,
         zn="R100-Single Family", lv=246300, ptype="SFR",
         buyers=["TOLL_BROTHERS","AMH","MERITAGE"]),
    dict(src="PB2", n=8, addr="Hwy 20", city="Loganville", zp="30052", ac=6.66,
         zn="M1-Light Industry", lv=45700, ptype="INDUSTRIAL",
         buyers=["SCANNELL","STONEMONT"]),
    dict(src="PB2", n=9, addr="3145 Willow Glade Trl", city="Lawrenceville", zp="30043", ac=6.62,
         zn="R100-Single Family", lv=347800, ptype="SFR",
         buyers=["DR_HORTON","TOLL_BROTHERS","MERITAGE","AMH"]),
    dict(src="PB2", n=10, addr="5380 Cole Rd", city="Buford", zp="30518", ac=9.73,
         zn="C2-General Business", lv=3204200, ptype="COMMERCIAL",
         buyers=["TRAMMELL_CROW","STONEMONT"]),
    dict(src="PB2", n=11, addr="302 Satellite Blvd", city="Suwanee", zp="30024", ac=20.28,
         zn="M1-Light Industry", lv=3000000, ptype="INDUSTRIAL",
         buyers=["IDI","ROCKEFELLER","SCANNELL","STONEMONT"]),
    dict(src="PB2", n=12, addr="1000 Sugarmont Pass", city="Lawrenceville", zp="30043", ac=74.52,
         zn="M1-Light Industry", lv=12547500, ptype="INDUSTRIAL",
         buyers=["IDI","ROCKEFELLER","STONEMONT","WALTON_GLOBAL"]),
    dict(src="PB2", n=13, addr="Richland Creek", city="Buford", zp="30518", ac=8.3,
         zn="M1-Light Industry", lv=1610800, ptype="INDUSTRIAL",
         buyers=["TRAMMELL_CROW","DERMODY","STONEMONT"]),
    dict(src="PB2", n=14, addr="1750 Pirkle Rd", city="Norcross", zp="30093", ac=7.78,
         zn="RM-Multi-family", lv=157400, ptype="MULTIFAMILY",
         buyers=["CORTLAND","WOOD_PARTNERS"]),
    dict(src="PB2", n=15, addr="Lebanon Rd", city="Lawrenceville", zp="30043", ac=9.43,
         zn="R100-Single Family", lv=1000, ptype="SFR",
         buyers=["DR_HORTON","MERITAGE","AMH","PROGRESS"]),
    # Playbook 1 — 10 deals
    dict(src="PB1", n=1, addr="4175 Old Norcross Rd", city="Duluth", zp="30096", ac=18.4,
         zn="RTH-Townhouse", lv=4736600, ptype="MULTIFAMILY",
         buyers=["AMH","PROGRESS","CORTLAND"]),
    dict(src="PB1", n=2, addr="5501 Cole Rd", city="Buford", zp="30518", ac=28.9,
         zn="M1-Light Industry", lv=4409100, ptype="INDUSTRIAL",
         buyers=["TRAMMELL_CROW","IDI","STONEMONT","ROCKEFELLER"]),
    dict(src="PB1", n=3, addr="5610 Austin Garner Rd", city="Sugar Hill", zp="30518", ac=53.0,
         zn="R100-Single Family", lv=2120800, ptype="SFR",
         buyers=["DR_HORTON","AMH","WALTON_GLOBAL","TOLL_BROTHERS"]),
    dict(src="PB1", n=4, addr="1350 Lakes Pkwy", city="Lawrenceville", zp="30043", ac=11.8,
         zn="M1-Light Industry", lv=1675500, ptype="INDUSTRIAL",
         buyers=["DERMODY","SCANNELL","STONEMONT"]),
    dict(src="PB1", n=5, addr="5100 Annistown Rd", city="Stone Mountain", zp="30087", ac=19.3,
         zn="C2-General Business", lv=1600000, ptype="COMMERCIAL",
         buyers=["STONEMONT","TRAMMELL_CROW"]),
    dict(src="PB1", n=6, addr="River Bottom Dr", city="Peachtree Corners", zp="30092", ac=33.0,
         zn="R100-Single Family", lv=1359800, ptype="SFR",
         buyers=["AMH","DR_HORTON","PROGRESS","WALTON_GLOBAL"]),
    dict(src="PB1", n=7, addr="2382 Gravel Springs Rd", city="Buford", zp="30519", ac=10.0,
         zn="RA200-Ag/Residence", lv=372900, ptype="SFR",
         buyers=["MERITAGE","DR_HORTON"]),
    dict(src="PB1", n=8, addr="Rock Springs Rd", city="Buford", zp="30519", ac=12.0,
         zn="RA200-Ag/Residence", lv=318700, ptype="SFR",
         buyers=["MERITAGE","DR_HORTON","AMH"]),
    dict(src="PB1", n=9, addr="5817 ORouke Rd", city="Buford", zp="30518", ac=8.2,
         zn="R100-Single Family", lv=308300, ptype="SFR",
         buyers=["MERITAGE","DR_HORTON"]),
    dict(src="PB1", n=10, addr="2341 Shoal Creek Rd", city="Buford", zp="30518", ac=6.2,
         zn="R100-Single Family", lv=303300, ptype="SFR",
         buyers=["TOLL_BROTHERS","MERITAGE","DR_HORTON"]),
]

# ── EMAIL TEMPLATE ───────────────────────────────────────────────────
TPL = """Subject: Off-Market {ptype} Land — {ac} Acres, {zn}, {city} GA
To: {to_email}
From: [YOUR NAME] <[YOUR EMAIL]>
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8

Dear {contact},

RE: {dept}

I'm a private land investor in Metro Atlanta with an off-market
opportunity I believe aligns with {company}'s acquisition criteria.

PROPERTY AT A GLANCE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Location:    {addr}, {city}, GA {zp}
  Acreage:     {ac} acres
  Zoning:      {zn}
  Status:      Vacant Land — Clear Title
  Est. Value:  ${lv:,}
  Offer Price: ${offer:,} (30% below market)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WHY THIS FITS YOUR PORTFOLIO:
{pitch}

DEAL STRUCTURE:
• Off-market, direct-to-principal opportunity
• All-cash, fast close (30-45 days)
• Clean title — no liens or encumbrances
• Assignment contract available for immediate transfer

I'd welcome 15 minutes to discuss whether this fits your
current pipeline. Available at your convenience.

Best regards,

[YOUR NAME]
[YOUR TITLE]
[YOUR COMPANY]
[YOUR PHONE]
[YOUR EMAIL]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BUYER CONTACT:
  Company:    {company}
  Department: {dept}
  Contact:    {contact}
  Phone:      {phone}
  Email:      {to_email}
  Address:    {address}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

# ── GENERATE EMAILS ──────────────────────────────────────────────────
total = 0
for prop in PROPERTIES:
    for bkey in prop["buyers"]:
        buyer = NEW_BUYERS[bkey]
        offer = int(prop["lv"] * 0.70)  # 30% below market
        bname_safe = bkey[:20]
        fname = OUT_DIR / f"Pitch_{prop['src']}_{prop['n']:02d}_{prop['addr'][:20].replace(' ','_')}_to_{bname_safe}.eml"

        content = TPL.format(
            ptype=prop["ptype"].title(),
            ac=prop["ac"],
            zn=prop["zn"],
            city=prop["city"],
            zp=prop["zp"],
            addr=prop["addr"],
            lv=prop["lv"],
            offer=offer,
            to_email=buyer["email"],
            contact=buyer["contact"],
            dept=buyer["dept"],
            company=buyer["company"],
            phone=buyer["phone"],
            address=buyer["address"],
            pitch=buyer["pitch"],
        )
        fname.write_text(content)
        total += 1

# ── GENERATE SUMMARY REPORT ─────────────────────────────────────────
report_lines = []
report_lines.append("=" * 80)
report_lines.append("  NEW BUYER PITCH SUMMARY — Generated " + datetime.now().strftime("%B %d, %Y %I:%M %p"))
report_lines.append("=" * 80)
report_lines.append(f"\n  Total emails generated: {total}")
report_lines.append(f"  Total new buyers: {len(NEW_BUYERS)}")
report_lines.append(f"  Total properties covered: {len(PROPERTIES)}")
report_lines.append(f"\n  Output directory: {OUT_DIR}/")
report_lines.append("\n" + "-" * 80)
report_lines.append("  PRIORITY CALL ORDER — START HERE")
report_lines.append("-" * 80)

priority = [
    ("IDI Logistics — Chris Kazanowski", "(404) 479-1660", "chris.kazanowski@idilogistics.com", "Named SVP. Direct email. Land deals daily."),
    ("Dermody — Wes Hardy", "(770) 200-4007", "whardy@dermody.com", "Named Partner. Office IN Gwinnett."),
    ("D.R. Horton — Atlanta East", "(678) 509-0555", "drhorton.com/property-submittal", "#1 builder. Online portal. Gwinnett."),
    ("Stonemont Financial", "(404) 846-3200", "stonemontfinancial.com", "Atlanta HQ. Industrial specialist."),
    ("Trammell Crow (CBRE)", "(404) 923-1544", "trammellcrow.com", "Building in Buford NOW."),
    ("Cortland", "(404) 965-3988", "cortland.com", "Atlanta HQ. Multifamily."),
    ("Meritage Homes", "(678) 348-8350", "meritagehomes.com", "Active Gwinnett builder."),
    ("AMH — Land Acquisitions", "(833) 736-8264", "amh.com", "NYSE REIT. BTR."),
    ("Toll Brothers — GA Division", "(888) 686-5542", "tollbrothers.com", "Just entered Gwinnett."),
    ("Scannell Properties", "(317) 843-5959", "scannellproperties.com", "National industrial dev."),
    ("Rockefeller Group", "(770) 884-1322", "rockefellergroup.com", "Whale deals."),
    ("Progress / Pretium", "rentprogress.com", "pretium.com", "SFR / BTR."),
    ("Wood Partners", "woodpartners.com", "woodpartners.com", "Top MF developer."),
    ("Walton Global", "walton.com", "walton.com", "Land banking."),
]

for i, (name, phone, email, why) in enumerate(priority, 1):
    report_lines.append(f"\n  {i:>2}. {name}")
    report_lines.append(f"      Phone: {phone}")
    report_lines.append(f"      Email: {email}")
    report_lines.append(f"      Why:   {why}")

report = "\n".join(report_lines)
(OUT_DIR / "CALL_ORDER_NEW_BUYERS.txt").write_text(report)

print(f"\n{'='*60}")
print(f"  ✅ Generated {total} new buyer pitch emails")
print(f"  ✅ Covering {len(PROPERTIES)} properties × {len(NEW_BUYERS)} new buyers")
print(f"  ✅ Output: {OUT_DIR}/")
print(f"  ✅ Call order: CALL_ORDER_NEW_BUYERS.txt")
print(f"{'='*60}")
print(f"\n  IMPORTANT: Replace [YOUR NAME], [YOUR EMAIL], etc. before sending.\n")
