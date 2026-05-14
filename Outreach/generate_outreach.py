#!/usr/bin/env python3
"""Generate personalized outreach letters, emails, and call scripts for top leads."""
import sqlite3, os, csv
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).parent.parent
DB = BASE / "landbot.db"
LETTERS_DIR = Path(__file__).parent / "Letters"
EMAILS_DIR = Path(__file__).parent / "Emails"
LETTERS_DIR.mkdir(exist_ok=True)
EMAILS_DIR.mkdir(exist_ok=True)

# ── Letter Template (Direct Mail) ──────────────────────────────
LETTER_TPL = """
                                                    {date}

{owner_name}
{mail_address}
{mail_city}, {mail_state} {mail_zip}

RE: Your property at {site_address}, {site_city}, GA {site_zip}
    Parcel ID: {parcel_id} | {acreage} acres | {zoning_desc}

Dear {owner_name},

I hope this letter finds you well. My name is [YOUR NAME], and I am a
local real estate investor here in the greater Atlanta area.

I am writing to you because I noticed you own a {acreage}-acre parcel
of land on {site_address} in {site_city}, Georgia. I am actively
looking to purchase vacant land in Gwinnett County and would love the
opportunity to make you a fair, all-cash offer for your property.

Here's what I can offer:

  • CASH purchase — no banks, no financing delays
  • Close on YOUR timeline — as fast as 14 days or whenever you prefer
  • I pay all closing costs — you walk away with your full amount
  • No realtors, no commissions, no fees to you

I understand that owning land you aren't actively using can become a
burden — property taxes, maintenance, liability concerns. I would be
happy to take that off your plate while putting cash in your pocket.

If you have any interest in selling — or even just want to hear what
I'd offer — please reach out. There is absolutely no obligation.

You can reach me at:
  Phone: [YOUR PHONE]
  Email: [YOUR EMAIL]

I look forward to hearing from you.

Sincerely,

[YOUR NAME]
[YOUR COMPANY NAME]
[YOUR PHONE]

P.S. — Even if you're not ready to sell today, I'd appreciate the
chance to stay in touch. Circumstances change, and I want to be the
first person you think of when the time is right.
"""

# ── Email Template ─────────────────────────────────────────────
EMAIL_TPL = """Subject: Cash Offer for Your {acreage}-Acre Property in {site_city}, GA (Parcel {parcel_id})
To: [OWNER EMAIL - Skip Trace Required]
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8

Hi {first_name},

I came across your {acreage}-acre property on {site_address} in
{site_city}, GA (Parcel ID: {parcel_id}), and wanted to reach out
directly.

I'm a local land buyer in the metro Atlanta area, and I'm interested
in making you a fair, all-cash offer. I can close quickly — as fast
as 14 days — and I'll cover all closing costs. No realtors or
commissions involved.

Would you be open to a quick conversation about it? I'm happy to
work around your schedule.

Thanks,
[YOUR NAME]
[YOUR PHONE]
[YOUR COMPANY]
"""

# ── Cold Call Script ───────────────────────────────────────────
CALL_SCRIPT = """
╔══════════════════════════════════════════════════════════════════╗
║                    COLD CALL SCRIPT                             ║
╠══════════════════════════════════════════════════════════════════╣

OWNER: {owner_name}
PROPERTY: {site_address}, {site_city}, GA
PARCEL: {parcel_id} | {acreage} acres | {zoning_desc}

──────────────────────────────────────────────────────────────────

INTRO:
"Hi, is this {first_name}? My name is [YOUR NAME]. I'm a local
real estate investor here in the Atlanta area. I'm calling because
I noticed you own a property on {site_address} in {site_city} —
about {acreage} acres of land. Do you have just a minute?"

IF YES → DISCOVERY:
"Great, I appreciate your time. I'm actively buying land in
Gwinnett County right now, and your property caught my eye.
I was curious — have you ever thought about selling it?"

IF INTERESTED → OFFER FRAME:
"Perfect. Well, I buy properties for cash, and I can close
really quickly — sometimes in as little as two weeks. I also
cover all the closing costs, so there are no fees on your end.

If I could get you a fair cash offer in the next day or two,
would that be something worth looking at?"

IF ASKS PRICE:
"I want to make sure I give you a number that's fair for both
of us. Can I ask — what did you have in mind for the property?
What would you need to walk away happy?"

(Let them anchor first. Then work toward your target of
${suggested_offer:,.0f} based on our analysis.)

IF NOT INTERESTED:
"I completely understand — no pressure at all. Would it be okay
if I checked back with you in a few months? Sometimes
circumstances change, and I'd love to be a resource for you."

CLOSE:
"Thanks so much for your time, {first_name}. I'll [send over
an offer / follow up in a few months]. Have a great day!"

──────────────────────────────────────────────────────────────────
"""

def guess_first_name(owner_name):
    """Try to extract a first name from owner string."""
    name = owner_name.strip()
    # If it's an LLC/Corp/Inc, use the entity name
    for suffix in ['LLC','LP','INC','CORP','TRUST','ASSOCIATION','ASSN','LTD','CO']:
        if suffix in name.upper():
            return name.split()[0].title()
    # For individuals like "SMITH JOHN P", first name is usually second word
    parts = name.split()
    if len(parts) >= 2:
        return parts[1].title()
    return parts[0].title()

def main():
    db = sqlite3.connect(str(DB))
    db.row_factory = sqlite3.Row

    rows = db.execute('''
        SELECT * FROM parcels
        WHERE is_vacant=1 AND is_absentee=1 AND score >= 60
        AND owner_name != '' AND mail_address != ''
        ORDER BY score DESC, acreage DESC
        LIMIT 30
    ''').fetchall()

    today = datetime.now().strftime("%B %d, %Y")
    print(f"Generating outreach for {len(rows)} top leads...")

    # Generate personalized letters
    all_letters = []
    for r in rows:
        first = guess_first_name(r["owner_name"])
        data = {
            "date": today,
            "owner_name": r["owner_name"],
            "first_name": first,
            "mail_address": r["mail_address"],
            "mail_city": r["mail_city"] or "",
            "mail_state": r["mail_state"] or "",
            "mail_zip": r["mail_zip"] or "",
            "site_address": r["site_address"] or "your property",
            "site_city": r["site_city"] or "Gwinnett County",
            "site_zip": r["site_zip"] or "",
            "parcel_id": r["parcel_id"],
            "acreage": f"{r['acreage']:.1f}" if r["acreage"] else "N/A",
            "zoning_desc": r["zoning_desc"] or "",
            "suggested_offer": r["suggested_offer"] or 0,
            "estimated_fmv": r["estimated_fmv"] or 0,
        }

        # Letter
        letter = LETTER_TPL.format(**data)
        pid_safe = r["parcel_id"].replace(" ", "_").replace("/", "-")
        with open(LETTERS_DIR / f"Letter_{pid_safe}.txt", "w") as f:
            f.write(letter)

        # Email
        email = EMAIL_TPL.format(**data)
        with open(EMAILS_DIR / f"Email_{pid_safe}.eml", "w") as f:
            f.write(email)

        all_letters.append(data)

    # Generate master call script
    print(f"  → Generated {len(rows)} personalized letters in Outreach/Letters/")
    print(f"  → Generated {len(rows)} email drafts in Outreach/Emails/")

    # Master call list
    with open(Path(__file__).parent / "Call_Script_Master.txt", "w") as f:
        f.write("=" * 66 + "\n")
        f.write("  LAND WHOLESALING — MASTER CALL LIST\n")
        f.write(f"  Generated: {today}\n")
        f.write(f"  Total Leads: {len(rows)}\n")
        f.write("=" * 66 + "\n\n")
        for r in rows:
            first = guess_first_name(r["owner_name"])
            data = {
                "owner_name": r["owner_name"],
                "first_name": first,
                "site_address": r["site_address"] or "property",
                "site_city": r["site_city"] or "Gwinnett County",
                "parcel_id": r["parcel_id"],
                "acreage": f"{r['acreage']:.1f}" if r["acreage"] else "N/A",
                "zoning_desc": r["zoning_desc"] or "",
                "suggested_offer": r["suggested_offer"] or 0,
            }
            f.write(CALL_SCRIPT.format(**data))
            f.write("\n\n")
    print(f"  → Generated master call script: Outreach/Call_Script_Master.txt")

    # CSV mail merge list
    with open(Path(__file__).parent / "Mail_Merge_List.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Owner","First_Name","Mail_Address","Mail_City","Mail_State","Mail_Zip",
                     "Site_Address","Site_City","Parcel_ID","Acreage","Zoning","Score",
                     "Est_FMV","Suggested_Offer"])
        for r in rows:
            first = guess_first_name(r["owner_name"])
            w.writerow([r["owner_name"], first, r["mail_address"],
                        r["mail_city"], r["mail_state"], r["mail_zip"],
                        r["site_address"], r["site_city"], r["parcel_id"],
                        r["acreage"], r["zoning_desc"], r["score"],
                        r["estimated_fmv"], r["suggested_offer"]])
    print(f"  → Generated mail merge CSV: Outreach/Mail_Merge_List.csv")
    print(f"\nDone! Replace [YOUR NAME], [YOUR PHONE], etc. in the templates before sending.")

if __name__ == "__main__":
    main()
