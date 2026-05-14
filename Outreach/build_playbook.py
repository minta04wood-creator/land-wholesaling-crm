#!/usr/bin/env python3
"""Generates the complete Deal Playbook with links, utilities, liens, and scripts."""
import os, textwrap
from pathlib import Path

OUT = Path(__file__).parent
DEALS = [
    dict(n=1, pid="7077 001", addr="4175 Old Norcross Rd", city="Duluth", st="GA", z="30096",
         acres=18.4, zoning="RTH-Townhouse", fmv=4736600, offer=2605130, fee=710490,
         seller="Autumn Vista Acquisition LP", seller_loc="Toronto, Canada",
         seller_phone="Certified letter → 3280 Bloor St W Ste 1400, Toronto ON M8X 2X3",
         held="6 yrs", paid="$4,750,000 (2019)", bought_from="Timbercreek Autumn Vista LP",
         elec="Yes", water="Yes (City)", sewer="Yes (City)", gas="Yes", septic="No", well="No",
         liens="None on record", landlocked="No",
         buyer1="Starwood Capital Group", b1phone="(770) 541-9046", b1email="sfr_inquiries@starwood.com",
         buyer2="Invitation Homes", b2phone="(770) 442-3372", b2email="invitationhomes.com/contact-us",
         seller_script="Good afternoon, I'm [YOUR NAME], a land investor in Metro Atlanta. I'm reaching out about your 18.4-acre parcel on Old Norcross Road in Duluth — Parcel 7077 001.\n\nI understand Autumn Vista acquired this from Timbercreek in December 2019 for $4.75 million, and it's been vacant for over six years. With carrying costs, taxes, and no income, I imagine there's been discussion about the best path forward.\n\nI work with institutional buyers actively acquiring townhouse-zoned land in Duluth. I can make a cash offer closing in 30-45 days — no financing contingencies. Would you discuss a number that works for both sides?",
         buyer_script="I've secured 18.4 acres of RTH-zoned land on Old Norcross Rd in Duluth — townhouse-entitled, ready for development. Starwood already owns 48 properties in Gwinnett including the Duluth corridor.\n\nThe property last traded at $4.75M. I can deliver at $3.3M — 30% below FMV. Clean title, no liens, motivated Canadian seller. Sending the package to sfr_inquiries@starwood.com now.",
         leverage="Paid $4.75M, sat vacant 6 yrs. Canadian LP managing GA land from Toronto. Townhouse zoning in high demand."),

    dict(n=2, pid="7326 070", addr="5501 Cole Rd", city="Buford", st="GA", z="30518",
         acres=28.9, zoning="M1-Light Industry", fmv=4409100, offer=2425005, fee=661365,
         seller="BFI Waste / Republic Services", seller_loc="Phoenix, AZ",
         seller_phone="(678) 963-2800 (Republic Services GA)",
         held="8 yrs", paid="$2,900,000 (2018)", bought_from="ALW Holdings LLC",
         elec="Verify", water="Verify", sewer="Verify", gas="Verify", septic="N/A", well="N/A",
         liens="None on record", landlocked="No",
         buyer1="Prologis — Kent Mason", b1phone="(678) 249-7001", b1email="prologis.com/contact-us",
         buyer2="Shaheen & Company", b2phone="(770) 916-1775", b2email="info@shaheenco.com",
         seller_script="Hi, I'm calling about a property matter. I'm a private land investor in Gwinnett County interested in purchasing a 29-acre parcel on Cole Road in Buford under BFI Waste Systems — Parcel 7326 070.\n\nRepublic Services acquired BFI's assets, and this lot has been vacant since 2018. Rather than carrying taxes and liability on surplus land, I'd like to discuss a cash purchase. Could you connect me with property disposition or surplus real estate?",
         buyer_script="Kent, I have an off-market 28.9-acre M1-zoned industrial parcel on Cole Rd in Buford — vacant, clear, ready for warehouse development. Prologis already has $99M+ in Gwinnett industrial.\n\nI can deliver at $3.1M — well below the $4.4M assessed value. Waste management company disposing of surplus land — fast close. Can I send the package?",
         leverage="Corporate surplus — zero revenue. Waste company has no use for vacant industrial land. Offer above their $2.9M basis."),

    dict(n=3, pid="7348 013", addr="5610 Austin Garner Rd", city="Sugar Hill", st="GA", z="30518",
         acres=53.0, zoning="R100-Single Family", fmv=2120800, offer=1166440, fee=318120,
         seller="Sansing Holdings LLC (Sandy Sansing)", seller_loc="Pensacola, FL",
         seller_phone="(850) 476-2480",
         held="16 yrs", paid="$0 (family transfer 2010)", bought_from="Sansing Robert C",
         elec="Yes", water="Yes (City)", sewer="Yes (City)", gas="Yes", septic="No", well="No",
         liens="None on record", landlocked="No",
         buyer1="Starwood Capital Group", b1phone="(770) 541-9046", b1email="sfr_inquiries@starwood.com",
         buyer2="Invitation Homes", b2phone="(770) 442-3372", b2email="invitationhomes.com/contact-us",
         seller_script="Good morning, I'm trying to reach Sandy Sansing or someone managing real estate for Sansing Holdings. I'm a land investor in Gwinnett County.\n\nI'm calling about a 53-acre parcel on Austin Garner Road in Sugar Hill — Parcel 7348 013. Records show it transferred from Robert C. Sansing in October 2010 — 16 years of property taxes on 53 vacant acres.\n\nI understand your organization focuses on automotive. This doesn't seem like a core asset. I'd like to make a straightforward cash offer. Would the right person be available?",
         buyer_script="I've secured a 53-acre R100-zoned development site on Austin Garner Rd in Sugar Hill — the largest off-market residential parcel in North Gwinnett.\n\nAt $1.48M, that's $28K/acre versus $40K+ for finished lots. 150-200 lot subdivision potential. Sending to sfr_inquiries@starwood.com.",
         leverage="16 yrs of taxes on 53 empty acres ($200K+ carrying costs). Auto dealer, not developer. $0 basis = any price is profit."),

    dict(n=4, pid="7034 092", addr="1350 Lakes Pkwy", city="Lawrenceville", st="GA", z="30043",
         acres=11.8, zoning="M1-Light Industry", fmv=1675500, offer=921525, fee=251325,
         seller="PJP Holdings LLC (Timothy Madison)", seller_loc="New Albany, OH",
         seller_phone="(614) 822-9980",
         held="12 yrs", paid="$1,550,000 (2014)", bought_from="Lakes Office Two LLC",
         elec="Yes", water="Yes (City)", sewer="Yes (City)", gas="Yes", septic="No", well="No",
         liens="None on record", landlocked="No",
         buyer1="Shaheen & Company", b1phone="(770) 916-1775", b1email="info@shaheenco.com",
         buyer2="Prologis — Kent Mason", b2phone="(678) 249-7001", b2email="prologis.com/contact-us",
         seller_script="Hi, I'm looking for Timothy Madison regarding PJP Holdings. I'm a private investor in Gwinnett County calling about your 11.8-acre industrial parcel on Lakes Pkwy in Lawrenceville — Parcel 7034 092.\n\nPJP acquired this from Lakes Office Two LLC in July 2014 for $1.55M. That's 12 years undeveloped. I know PJP is active in New Albany, so this GA asset may not be priority.\n\nI have institutional industrial buyers looking for M1 land on Lakes Pkwy. I'd like to make a cash offer that gets this off your books. Open to a conversation?",
         buyer_script="Calling for Ben Newland or acquisitions. I have an off-market 11.8-acre M1-zoned industrial parcel on Lakes Pkwy in Lawrenceville.\n\nShaheen holds $74.9M in industrial assets in the Gwinnett corridor. This fits perfectly. I can deliver at $1.17M — 30% below assessed. Can I email the package to info@shaheenco.com?",
         leverage="Paid $1.55M twelve years ago — dead capital. OH-based, not active in GA. Emphasize tax write-off."),

    dict(n=5, pid="6040 158", addr="5100 Annistown Rd", city="Stone Mountain", st="GA", z="30087",
         acres=19.3, zoning="C2-General Business", fmv=1600000, offer=880000, fee=240000,
         seller="Ingles Markets Inc", seller_loc="Asheville, NC",
         seller_phone="(828) 669-2941 (Corporate HQ)",
         held="36 yrs", paid="$0 (1990)", bought_from="Unknown",
         elec="Yes", water="Yes (City)", sewer="Yes (City)", gas="Yes", septic="No", well="No",
         liens="None on record", landlocked="No",
         buyer1="AOA Parish Real Estate Trust", b1phone="(404) 920-7800", b1email="Via certified letter",
         buyer2="Toco Hill Inc", b2phone="Skip trace", b2email="1800 Briarcliff Rd NE, Atlanta GA",
         seller_script="Good morning, I'd like to speak with someone in Real Estate. My name is [YOUR NAME], commercial land investor in Atlanta.\n\nI'm calling about a 19.3-acre C2-zoned parcel on Annistown Rd in Stone Mountain — Parcel 6040 158. County records show Ingles has held this since March 1990.\n\nThat's 36 years of carrying a vacant commercial lot. Whatever development plans were intended, the project never materialized. At this point, it's a tax liability generating zero revenue.\n\nI work with commercial developers in the Stone Mountain corridor. I can present a cash offer with a 30-day close. Would Real Estate review a formal LOI?",
         buyer_script="AOA Parish holds $59.6M in commercial properties across Gwinnett and Forsyth. I have 19.3 acres of C2-zoned land on Annistown Rd — largest off-market commercial parcel in Stone Mountain.\n\nAt $1.12M ($58K/acre), well below market. Seller is a public company that's held it 36 years and is ready to dispose. Clean title, no environmental issues.",
         leverage="36 YEARS vacant. Public company (NASD: IMKTA) — shareholders want dead assets cleaned up. Grocery chain, not developer. $0 basis."),

    dict(n=6, pid="6345 001", addr="River Bottom Dr", city="Peachtree Corners", st="GA", z="30092",
         acres=33.0, zoning="R100-Single Family", fmv=1359800, offer=747890, fee=203970,
         seller="Parker Nathan N", seller_loc="New York, NY",
         seller_phone="Skip trace — TruePeopleSearch → '825 W End Ave' NYC",
         held="20+ yrs", paid="$0 (pre-digital)", bought_from="Unknown",
         elec="Yes", water="Yes (City)", sewer="Yes (City)", gas="Yes", septic="No", well="No",
         liens="None on record", landlocked="No",
         buyer1="Invitation Homes", b1phone="(770) 442-3372", b1email="invitationhomes.com/contact-us",
         buyer2="Starwood Capital", b2phone="(770) 541-9046", b2email="sfr_inquiries@starwood.com",
         seller_script="Hi Nathan, I'm [YOUR NAME], a land investor in Peachtree Corners, Georgia.\n\nI'm calling about your 33-acre parcel on River Bottom Drive — Parcel 6345 001. You've owned this for quite some time, managing it from NYC — 850 miles away.\n\nI have buyers looking for large residential tracts in Peachtree Corners right now. I can make this simple — cash offer, I handle the closing attorney, close in 30 days. Would you hear a number?",
         buyer_script="I've locked up 33 acres of R100 land on River Bottom Dr in Peachtree Corners — off-market, clear title. Invitation Homes owns 36+ properties in the area.\n\nAt $951K for 33 acres, that's $29K/acre for entitled residential land where finished lots trade at $80K+. Ground-floor development opportunity.",
         leverage="NYC to GA = 850 miles. Pre-digital records = extremely long hold. 33 acres producing zero income. Be warm — individual, not corp."),

    dict(n=7, pid="7100 020", addr="2382 Gravel Springs Rd", city="Buford", st="GA", z="30519",
         acres=10.0, zoning="RA200-Ag/Residence", fmv=372900, offer=205095, fee=55935,
         seller="Hawkins William", seller_loc="Winter Springs, FL",
         seller_phone="Skip trace — TruePeopleSearch → Winter Springs FL",
         held="9 yrs", paid="$180,000 (2016, bank foreclosure)", bought_from="Renasant Bank",
         elec="Yes", water="Yes (City)", sewer="Yes (City)", gas="Yes", septic="No", well="No",
         liens="None on record", landlocked="No",
         buyer1="Turnkey Properties LP", b1phone="Skip trace — Cumming GA", b1email="8175 Dogwood Trl, Cumming",
         buyer2="Mora Leusterio (local builder)", b2phone="Skip trace", b2email="5240 Suwanee Dam Rd, Suwanee",
         seller_script="Hi William, I'm [YOUR NAME], land investor in Buford, Georgia. Calling about your 10-acre parcel on Gravel Springs Road — Parcel 7100 020.\n\nYou purchased this from Renasant Bank in December 2016 for $180,000 — a bank-owned property. That was 9 years ago. Whatever plans you had may have changed.\n\nI work with local builders in Buford looking for acreage right now. I'd like to make a cash offer above your purchase price so you turn a profit. Interested?",
         buyer_script="I have 10 acres on Gravel Springs Rd in Buford — RA200-zoned, all city utilities connected. Perfect for an estate-lot subdivision or custom home development.\n\nTurnkey Properties already has 12 parcels in the Buford/Suwanee corridor. This fits your build profile. I can deliver at $261K.",
         leverage="Bought from a BANK — speculative purchase. FL resident. 9 yrs = plans fell through. Offer above $180K basis."),

    dict(n=8, pid="7135 013", addr="Rock Springs Rd", city="Buford", st="GA", z="30519",
         acres=12.0, zoning="RA200-Ag/Residence", fmv=318700, offer=175285, fee=47805,
         seller="Dieguez Rodolfo Valentino", seller_loc="Haiku, Hawaii",
         seller_phone="(808) 572-9502",
         held="14 yrs", paid="$0 (transfer 2012)", bought_from="Prieto George W",
         elec="Yes", water="Yes (City)", sewer="Yes (City)", gas="Yes", septic="No", well="No",
         liens="None on record", landlocked="No",
         buyer1="Turnkey Properties LP", b1phone="Skip trace — Cumming GA", b1email="8175 Dogwood Trl, Cumming",
         buyer2="Mora Leusterio", b2phone="Skip trace", b2email="5240 Suwanee Dam Rd, Suwanee",
         seller_script="Hi Rodolfo, I'm [YOUR NAME], calling from Buford, Georgia about your 12-acre property on Rock Springs Road — Parcel 7135 013.\n\nYou've held this since 2012 — 14 years — managing it from Hawaii. That's as far from Buford as you can get in the US.\n\nYou've been paying taxes every year on land generating no income. I work with Buford builders looking for this type of acreage. I handle all paperwork, coordinate the closing attorney, wire funds to you. No hassle. Open to a price discussion?",
         buyer_script="12 acres on Rock Springs Rd in Buford — RA200-zoned, full city utilities. Owner lives in Hawaii and is motivated to sell.\n\nAt $223K, that's $18.5K/acre for land with city water, sewer, electric, and gas already available. Turnkey development opportunity.",
         leverage="HAWAII to Georgia = maximum distance. 14 yrs of carrying costs. $0 basis. Be friendly — he may have forgotten he owns this."),

    dict(n=9, pid="7338 010", addr="5817 ORouke Rd", city="Buford", st="GA", z="30518",
         acres=8.2, zoning="R100-Single Family", fmv=308300, offer=169565, fee=46245,
         seller="Obe Peter", seller_loc="Suffern, NY",
         seller_phone="Skip trace — TruePeopleSearch → Suffern NY",
         held="12 yrs", paid="$300,000 (2014)", bought_from="Estate of Mary E Benson",
         elec="Yes", water="Yes (City)", sewer="Yes (City)", gas="Yes", septic="No", well="No",
         liens="None on record", landlocked="No",
         buyer1="Mora Leusterio (12 parcels, Suwanee)", b1phone="Skip trace", b1email="5240 Suwanee Dam Rd",
         buyer2="MAAG USA LLC (Norcross)", b2phone="Skip trace", b2email="Norcross GA",
         seller_script="Hi Peter, I'm [YOUR NAME], land investor in Buford, Georgia. Calling about your 8.2-acre parcel on O'Rouke Road — Parcel 7338 010.\n\nRecords show you purchased from the Estate of Mary Benson in January 2014 for $300,000. That was 12 years ago. I'm guessing development plans may not have worked out — and managing 8 acres from Suffern, New York isn't ideal.\n\nThe Buford market has changed. I have local builders looking for R100 acreage right now. Rather than continuing to pay taxes, would you consider a fair cash offer?",
         buyer_script="8.2 acres on O'Rouke Rd in Buford — R100-zoned, full city utilities (water, sewer, electric, gas). Perfect for a 6-8 lot luxury custom home subdivision.\n\nMotivated NY owner who paid $300K twelve years ago. I can deliver at $215K. Local builder opportunity.",
         leverage="Paid $300K, property barely appreciated in 12 yrs. NY resident. Bought from estate = speculative. Acknowledge his $300K."),

    dict(n=10, pid="7326 040", addr="2341 Shoal Creek Rd", city="Buford", st="GA", z="30518",
         acres=6.2, zoning="R100-Single Family", fmv=303300, offer=166815, fee=45495,
         seller="Wagner William H", seller_loc="Bristol, CT",
         seller_phone="Skip trace — TruePeopleSearch → Bristol CT",
         held="6 yrs (inherited)", paid="$0 (inherited 2020)", bought_from="Wagner Albert F",
         elec="Yes", water="Yes (City)", sewer="Yes (City)", gas="Yes", septic="No", well="No",
         liens="None on record", landlocked="No",
         buyer1="Mora Leusterio (Suwanee, 12 parcels)", b1phone="Skip trace", b1email="5240 Suwanee Dam Rd",
         buyer2="Turnkey Properties LP (Cumming, 12 parcels)", b2phone="Skip trace", b2email="8175 Dogwood Trl",
         seller_script="Hi William, I'm [YOUR NAME], land investor in Buford, Georgia. I'm reaching out about your 6.2-acre lot on Shoal Creek Road — Parcel 7326 040.\n\nRecords show this transferred from Albert Wagner in August 2020. I'm guessing this was inherited? If so, I understand this may not be an asset you planned on owning — and managing land in Georgia from Connecticut probably isn't ideal.\n\nI buy inherited properties regularly and make the process simple. I handle the closing attorney, title search, everything. You just sign and receive a wire. Interested in hearing my offer?",
         buyer_script="6.2 acres on Shoal Creek Rd in Buford — R100-zoned, full city utilities. Motivated CT owner who inherited the land and has no use for it.\n\nAt $212K, that's $34K/acre for a premium Shoal Creek location. Perfect for 4-5 luxury custom homes.",
         leverage="INHERITED ($0). CT resident = zero connection to Buford. Inherited owners are statistically the MOST willing sellers. Be empathetic."),
]

# ── Generate master script file ──
lines = []
lines.append("=" * 80)
lines.append("  DEAL PLAYBOOK — MASTER CALL SCRIPTS")
lines.append("  10 Deals | Seller + Buyer Scripts | Updated May 2026")
lines.append("=" * 80)
lines.append("")
lines.append("REPLACE BEFORE USING:")
lines.append("  [YOUR NAME]  → Your full name")
lines.append("  [YOUR PHONE] → Your phone number")
lines.append("  [YOUR EMAIL] → Your email address")
lines.append("")

for d in DEALS:
    gmap = f"https://www.google.com/maps/search/{d['addr'].replace(' ','+')},+{d['city']},+{d['st']}+{d['z']}"
    earth = f"https://earth.google.com/web/search/{d['addr'].replace(' ','+')},+{d['city']},+{d['st']}+{d['z']}"
    buyer_total = d['offer'] + d['fee']

    lines.append("=" * 80)
    lines.append(f"  DEAL #{d['n']} — ${d['fee']:,} ASSIGNMENT FEE")
    lines.append(f"  {d['addr']}, {d['city']}, {d['st']} {d['z']}")
    lines.append("=" * 80)
    lines.append("")
    lines.append(f"  VIEW PROPERTY:")
    lines.append(f"    Google Maps:  {gmap}")
    lines.append(f"    Google Earth: {earth}")
    lines.append("")
    lines.append(f"  PROPERTY DETAILS:")
    lines.append(f"    Parcel ID:    {d['pid']}")
    lines.append(f"    Acreage:      {d['acres']} acres")
    lines.append(f"    Zoning:       {d['zoning']}")
    lines.append(f"    FMV:          ${d['fmv']:,}")
    lines.append(f"    Your Offer:   ${d['offer']:,}")
    lines.append(f"    Your Fee:     ${d['fee']:,}")
    lines.append(f"    Buyer Pays:   ${buyer_total:,} (30% below FMV)")
    lines.append("")
    lines.append(f"  UTILITIES:")
    lines.append(f"    Electric:     {d['elec']}")
    lines.append(f"    Water:        {d['water']}")
    lines.append(f"    Sewer:        {d['sewer']}")
    lines.append(f"    Gas:          {d['gas']}")
    lines.append(f"    Septic Req'd: {d['septic']}")
    lines.append(f"    Well Req'd:   {d['well']}")
    lines.append("")
    lines.append(f"  LIENS & HOLDS:")
    lines.append(f"    Liens:        {d['liens']}")
    lines.append(f"    Landlocked:   {d['landlocked']}")
    lines.append("")
    lines.append(f"  OWNERSHIP HISTORY:")
    lines.append(f"    Owner:        {d['seller']}")
    lines.append(f"    Location:     {d['seller_loc']}")
    lines.append(f"    Phone:        {d['seller_phone']}")
    lines.append(f"    Held:         {d['held']}")
    lines.append(f"    Paid:         {d['paid']}")
    lines.append(f"    Bought From:  {d['bought_from']}")
    lines.append("")
    lines.append("-" * 80)
    lines.append(f"  SELLER CALL SCRIPT (to buy the land)")
    lines.append("-" * 80)
    for line in d['seller_script'].split('\n'):
        lines.append(f"    {line}")
    lines.append("")
    lines.append(f"  KEY LEVERAGE: {d['leverage']}")
    lines.append("")
    lines.append("-" * 80)
    lines.append(f"  BUYER #1: {d['buyer1']}")
    lines.append(f"    Phone: {d['b1phone']}")
    lines.append(f"    Email: {d['b1email']}")
    lines.append("-" * 80)
    for line in d['buyer_script'].split('\n'):
        lines.append(f"    {line}")
    lines.append("")
    lines.append(f"  BUYER #2: {d['buyer2']}")
    lines.append(f"    Phone: {d['b2phone']}")
    lines.append(f"    Email: {d['b2email']}")
    lines.append("")
    lines.append("")

# Priority call order
lines.append("=" * 80)
lines.append("  PRIORITY CALL ORDER")
lines.append("=" * 80)
lines.append("")
order = [
    ("#5 Ingles Markets", "(828) 669-2941", "36 yrs vacant. Corporate. Easiest yes."),
    ("#8 Dieguez (Hawaii)", "(808) 572-9502", "Direct to owner. Lives in Hawaii."),
    ("#3 Sansing Holdings", "(850) 476-2480", "53 acres. 16 yrs. Auto dealer."),
    ("#2 BFI/Republic", "(678) 963-2800", "Corporate surplus. $661K profit."),
    ("#4 PJP Holdings", "(614) 822-9980", "12 yrs. OH developer."),
    ("#1 Autumn Vista", "Certified letter", "$710K profit. Canadian LP."),
    ("#7 Hawkins (FL)", "Skip trace", "Bought from bank. 9 yrs."),
    ("#9 Obe Peter (NY)", "Skip trace", "12 yrs. Paid $300K."),
    ("#10 Wagner (CT)", "Skip trace", "Inherited. Zero attachment."),
    ("#6 Parker (NYC)", "Skip trace", "33 acres. 20+ yrs."),
]
for i, (deal, phone, why) in enumerate(order, 1):
    lines.append(f"  {i:>2}. {deal:<25} {phone:<25} {why}")
lines.append("")

master = '\n'.join(lines)
(OUT / "Call_Script_Master.txt").write_text(master)
print(f"✅ Call_Script_Master.txt — {len(DEALS)} deals, {len(lines)} lines")

# ── Generate CSV for mail merge ──
csv_lines = ["Deal_Num,Property,City,Acres,Zoning,FMV,Offer,Fee,Seller,Seller_Phone,Seller_Location,Held,Electric,Water,Sewer,Gas,Liens,Buyer1,B1_Phone,B1_Email,Buyer2,B2_Phone,B2_Email,Google_Maps"]
for d in DEALS:
    gmap = f"https://www.google.com/maps/search/{d['addr'].replace(' ','+')},+{d['city']},+{d['st']}+{d['z']}"
    csv_lines.append(f"{d['n']},\"{d['addr']}, {d['city']}\",{d['city']},{d['acres']},{d['zoning']},{d['fmv']},{d['offer']},{d['fee']},\"{d['seller']}\",\"{d['seller_phone']}\",{d['seller_loc']},{d['held']},{d['elec']},{d['water']},{d['sewer']},{d['gas']},{d['liens']},\"{d['buyer1']}\",\"{d['b1phone']}\",\"{d['b1email']}\",\"{d['buyer2']}\",\"{d['b2phone']}\",\"{d['b2email']}\",{gmap}")
(OUT / "Mail_Merge_List.csv").write_text('\n'.join(csv_lines))
print(f"✅ Mail_Merge_List.csv — {len(DEALS)} deals")

print(f"\n{'='*60}")
print(f"  DONE — All old scripts replaced with Deal Playbook")
print(f"  Files: {OUT}")
print(f"{'='*60}")
