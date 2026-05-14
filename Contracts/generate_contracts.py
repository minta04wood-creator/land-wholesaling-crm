#!/usr/bin/env python3
"""
Land Wholesaling Contract Generator
Generates Georgia-compliant PSA and Assignment contracts for each deal.
"""
import os, sqlite3, textwrap
from pathlib import Path
from datetime import date

BASE = Path(__file__).parent
PSA_DIR = BASE / "PSA_Seller"
ASSIGN_DIR = BASE / "Assignment_Buyer"
PSA_DIR.mkdir(exist_ok=True)
ASSIGN_DIR.mkdir(exist_ok=True)

TODAY = date.today().strftime("%B %d, %Y")
YEAR = date.today().year

# Property deals
DEALS = [
    {"pid":"7077 001","addr":"4175 Old Norcross Rd","city":"Duluth","state":"GA","zip":"30096",
     "county":"Gwinnett","acres":"18.40","zoning":"RTH-Single Family Res-Twnhse",
     "seller":"AUTUMN VISTA ACQUISITION LP","seller_addr":"3280 Bloor St W Ste 1400, Toronto ON M8X 2X3",
     "fmv":4736600,"offer":2605130,"fee":355245,
     "buyers":[
         {"name":"Invitation Homes","contact":"Atlanta Regional Office","phone":"(770) 442-3372","email":"invitationhomes.com/contact-us","addr":"8601 Dunwoody Pl Ste 520, Sandy Springs GA 30350"},
         {"name":"Starwood Capital Group","contact":"SFR Acquisitions","phone":"(770) 541-9046","email":"sfr_inquiries@starwood.com","addr":"400 Galleria Pkwy Ste 1450, Atlanta GA 30339"},
     ]},
    {"pid":"7326 070","addr":"5501 Cole Rd","city":"Buford","state":"GA","zip":"30518",
     "county":"Gwinnett","acres":"28.92","zoning":"M1-Light Industry",
     "seller":"BFI WASTE SYSTEMS OF GEORGIA LLC (c/o Republic Services)","seller_addr":"PO Box 29246, Phoenix AZ 85038",
     "fmv":4409100,"offer":2425005,"fee":330682,
     "buyers":[
         {"name":"Prologis Inc.","contact":"Kent Mason, GA Market Officer","phone":"(678) 249-7001","email":"prologis.com/contact-us","addr":"3475 Piedmont Rd NE Ste 650, Atlanta GA 30305"},
         {"name":"Shaheen & Company","contact":"Ben Newland / Emma Jackson","phone":"(770) 916-1775","email":"info@shaheenco.com","addr":"3625 Cumberland Blvd SE Ste 250, Atlanta GA 30339"},
     ]},
    {"pid":"7348 013","addr":"5610 Austin Garner Rd","city":"Sugar Hill","state":"GA","zip":"30518",
     "county":"Gwinnett","acres":"53.02","zoning":"R100-Single Family Residence",
     "seller":"SERIES 20 OF SANSING HOLDINGS LLC","seller_addr":"5705 Pensacola Blvd, Pensacola FL 32505",
     "fmv":2120800,"offer":1166440,"fee":159060,
     "buyers":[
         {"name":"Invitation Homes","contact":"Atlanta Regional Office","phone":"(770) 442-3372","email":"invitationhomes.com/contact-us","addr":"8601 Dunwoody Pl Ste 520, Sandy Springs GA 30350"},
         {"name":"Starwood Capital Group","contact":"SFR Acquisitions","phone":"(770) 541-9046","email":"sfr_inquiries@starwood.com","addr":"400 Galleria Pkwy Ste 1450, Atlanta GA 30339"},
     ]},
    {"pid":"7034 092","addr":"1350 Lakes Pkwy","city":"Lawrenceville","state":"GA","zip":"30043",
     "county":"Gwinnett","acres":"11.84","zoning":"M1-Light Industry",
     "seller":"PJP HOLDINGS LLC","seller_addr":"9005 Smiths Mill Rd N, New Albany OH 43054",
     "fmv":1675500,"offer":921525,"fee":125662,
     "buyers":[
         {"name":"Shaheen & Company","contact":"Ben Newland / Emma Jackson","phone":"(770) 916-1775","email":"info@shaheenco.com","addr":"3625 Cumberland Blvd SE Ste 250, Atlanta GA 30339"},
         {"name":"Georgia Piedmont Land Trust","contact":"Acquisitions","phone":"(678) 884-7588","email":"gplt.org/contact","addr":"PO Box 3687, Suwanee GA 30024"},
     ]},
    {"pid":"6040 158","addr":"5100 Annistown Rd","city":"Stone Mountain","state":"GA","zip":"30087",
     "county":"Gwinnett","acres":"19.33","zoning":"C2-General Business",
     "seller":"INGLES MARKETS INC","seller_addr":"PO Box 6676, Asheville NC 28816",
     "fmv":1600000,"offer":880000,"fee":120000,
     "buyers":[
         {"name":"AOA Parish Real Estate Trust","contact":"Office Administrator","phone":"(404) 920-7800","email":"Via certified letter","addr":"2401 Lake Park Dr SE, Smyrna GA 30080"},
     ]},
    {"pid":"6345 001","addr":"River Bottom Dr","city":"Peachtree Corners","state":"GA","zip":"30092",
     "county":"Gwinnett","acres":"33.02","zoning":"R100-Single Family Residence",
     "seller":"PARKER NATHAN N","seller_addr":"825 W End Ave Apt 12-G, New York NY 10025",
     "fmv":1359800,"offer":747890,"fee":101985,
     "buyers":[
         {"name":"Invitation Homes","contact":"Atlanta Regional Office","phone":"(770) 442-3372","email":"invitationhomes.com/contact-us","addr":"8601 Dunwoody Pl Ste 520, Sandy Springs GA 30350"},
         {"name":"Starwood Capital Group","contact":"SFR Acquisitions","phone":"(770) 541-9046","email":"sfr_inquiries@starwood.com","addr":"400 Galleria Pkwy Ste 1450, Atlanta GA 30339"},
     ]},
    {"pid":"7135 013","addr":"Rock Springs Rd","city":"Buford","state":"GA","zip":"30519",
     "county":"Gwinnett","acres":"12.04","zoning":"RA200-Agriculture/Residence",
     "seller":"DIEGUEZ RODOLFO VALENTINO","seller_addr":"915 E Kuiaha Rd, Haiku HI 96708",
     "fmv":318700,"offer":175285,"fee":23902,
     "buyers":[
         {"name":"Invitation Homes","contact":"Atlanta Regional Office","phone":"(770) 442-3372","email":"invitationhomes.com/contact-us","addr":"8601 Dunwoody Pl Ste 520, Sandy Springs GA 30350"},
     ]},
]

def generate_psa(deal):
    return f"""
================================================================================
     PURCHASE AND SALE AGREEMENT — VACANT LAND
     State of Georgia | {deal['county']} County
================================================================================

                    CONTRACT DATE: ___________________
                    EFFECTIVE DATE: Date of last signature

THIS PURCHASE AND SALE AGREEMENT ("Agreement") is entered into as of the
Contract Date written above, by and between:

SELLER:     {deal['seller']}
            {deal['seller_addr']}

BUYER:      [YOUR NAME] and/or assigns
            [YOUR ADDRESS]
            [YOUR PHONE] | [YOUR EMAIL]

(Seller and Buyer collectively referred to as the "Parties")

RECITALS:
Buyer is a private real estate investor acquiring equitable interest in the
Property described herein. Buyer intends to purchase or assign this contract to
a third party. Seller acknowledges and consents to this arrangement.

================================================================================
                        ARTICLE 1 — PROPERTY
================================================================================

1.1  PROPERTY ADDRESS:    {deal['addr']}, {deal['city']}, {deal['state']} {deal['zip']}
1.2  PARCEL ID:           {deal['pid']}
1.3  COUNTY:              {deal['county']} County, Georgia
1.4  ACREAGE:             {deal['acres']} acres (approximately)
1.5  ZONING:              {deal['zoning']}
1.6  LEGAL DESCRIPTION:   As recorded in the Official Records of {deal['county']}
                          County, Georgia, and as set forth in the title
                          commitment to be obtained by Buyer.

================================================================================
                      ARTICLE 2 — PURCHASE PRICE
================================================================================

2.1  PURCHASE PRICE:      ${deal['offer']:,.2f} (USD)
2.2  EARNEST MONEY:       $100.00 (One Hundred Dollars), to be deposited with
                          the Closing Attorney within five (5) business days of
                          the Effective Date.
2.3  BALANCE AT CLOSING:  The remaining balance of ${deal['offer'] - 100:,.2f}
                          shall be paid at Closing via certified funds or wire
                          transfer.

================================================================================
               ARTICLE 3 — ASSIGNMENT RIGHTS (CRITICAL)
================================================================================

3.1  RIGHT TO ASSIGN. Buyer shall have the unrestricted right to assign this
     Agreement, in whole or in part, to any individual, entity, trust, LLC, or
     nominee (collectively, "Assignee") at any time prior to Closing, without
     the prior written consent of Seller. Seller hereby irrevocably consents
     to any such assignment.

3.2  RELEASE UPON ASSIGNMENT. Upon valid assignment and written notice to
     Seller, Buyer (Assignor) shall be fully released from all obligations
     under this Agreement, and the Assignee shall assume all rights and
     obligations hereunder.

3.3  ASSIGNMENT FEE. Any assignment fee charged by Buyer to the Assignee is a
     private matter between Buyer and Assignee. Seller has no right, claim, or
     interest in the assignment fee.

================================================================================
          ARTICLE 4 — INSPECTION & FEASIBILITY PERIOD (EXIT CLAUSE)
================================================================================

4.1  FEASIBILITY PERIOD. Buyer shall have a period of SIXTY (60) calendar days
     from the Effective Date (the "Feasibility Period") to conduct any and all
     inspections, investigations, tests, surveys, studies, and due diligence
     Buyer deems necessary, including but not limited to:

     (a) Physical inspection of the Property
     (b) Environmental site assessments (Phase I and/or Phase II)
     (c) Soil and geotechnical testing
     (d) Boundary and topographic surveys
     (e) Title examination and title insurance commitment review
     (f) Zoning and land-use verification
     (g) FEMA flood zone determination
     (h) Utility availability and capacity confirmation
     (i) Market analysis and financial feasibility
     (j) Review by Buyer's partners, members, managers, or investors
     (k) Any other investigation Buyer deems appropriate

4.2  TERMINATION RIGHT (FREE LOOK). Buyer may terminate this Agreement for
     ANY REASON OR NO REASON AT ALL during the Feasibility Period by
     delivering written notice to Seller. Upon such termination:

     (a) Buyer's Earnest Money shall be IMMEDIATELY and FULLY refunded.
     (b) Buyer shall have NO further obligation or liability under this
         Agreement whatsoever.
     (c) This Agreement shall be null and void and of no further force or
         effect.

4.3  SELLER'S COOPERATION. Seller shall provide Buyer and Buyer's agents,
     contractors, and consultants with reasonable access to the Property
     during the Feasibility Period for inspections and testing.

================================================================================
         ARTICLE 5 — ADDITIONAL CONTINGENCIES (EXIT CLAUSES)
================================================================================

5.1  TITLE CONTINGENCY. This Agreement is contingent upon Buyer's receipt and
     approval of a title commitment showing marketable and insurable title,
     free and clear of all liens, encumbrances, easements, restrictions, and
     defects that are unacceptable to Buyer in Buyer's sole discretion.

5.2  SURVEY CONTINGENCY. This Agreement is contingent upon Buyer's receipt and
     approval of a current boundary survey, at Buyer's option.

5.3  ENVIRONMENTAL CONTINGENCY. This Agreement is contingent upon the Property
     being free of Hazardous Materials, contamination, underground storage
     tanks, and environmental issues. If any environmental concern is
     discovered, Buyer may terminate this Agreement and receive a full
     refund of Earnest Money.

5.4  PARTNER/INVESTOR APPROVAL. This Agreement is contingent upon the
     approval of Buyer's partners, members, managers, lenders, or investors,
     in their sole and absolute discretion.

5.5  FINANCING CONTINGENCY. If Buyer is unable to obtain financing on terms
     acceptable to Buyer in Buyer's sole discretion, Buyer may terminate
     this Agreement and receive a full refund of Earnest Money.

5.6  APPRAISAL CONTINGENCY. If an appraisal obtained by Buyer values the
     Property below the Purchase Price, Buyer may terminate this Agreement
     and receive a full refund of Earnest Money.

================================================================================
                    ARTICLE 6 — PROPERTY CONDITION
================================================================================

6.1  AS-IS, WHERE-IS. Buyer is purchasing the Property in its present "AS-IS,
     WHERE-IS" condition, with all faults and defects. Seller makes NO
     warranties or representations regarding the Property's condition,
     suitability, fitness, or value.

6.2  SELLER'S DISCLOSURES. Seller shall disclose all known material defects,
     environmental conditions, liens, assessments, pending litigation, and
     any facts that could materially affect the value or desirability of the
     Property per O.C.G.A. Section 44-1-16.

================================================================================
                       ARTICLE 7 — CLOSING
================================================================================

7.1  CLOSING DATE. Closing shall occur within NINETY (90) calendar days from
     the Effective Date, or within thirty (30) days after the expiration of
     the Feasibility Period, whichever is later.

7.2  CLOSING ATTORNEY. Closing shall be conducted by a Georgia-licensed real
     estate attorney selected by Buyer, as required by Georgia law.

7.3  CLOSING COSTS. Seller shall pay: (a) State and county transfer taxes,
     (b) Seller's attorney fees, (c) Any outstanding liens or assessments.
     Buyer shall pay: (a) Buyer's attorney fees, (b) Title insurance
     premium, (c) Recording fees.

7.4  EXTENSIONS. Buyer may extend the Closing Date by up to thirty (30) days
     by providing written notice to Seller at least five (5) days prior to
     the scheduled Closing Date. No additional consideration is required.

================================================================================
            ARTICLE 8 — LIMITATION OF LIABILITY (CRITICAL)
================================================================================

8.1  LIMITATION OF REMEDIES. IN THE EVENT OF BUYER'S DEFAULT, SELLER'S SOLE
     AND EXCLUSIVE REMEDY SHALL BE TO RETAIN THE EARNEST MONEY DEPOSIT OF
     $100.00 AS LIQUIDATED DAMAGES. SELLER HEREBY WAIVES ANY AND ALL RIGHTS
     TO SPECIFIC PERFORMANCE, CONSEQUENTIAL DAMAGES, PUNITIVE DAMAGES, OR
     ANY OTHER REMEDY AT LAW OR IN EQUITY.

8.2  NO PERSONAL LIABILITY. Buyer shall have NO personal liability under this
     Agreement. Buyer's maximum exposure shall be limited to the Earnest
     Money Deposit of $100.00.

8.3  NO OBLIGATION TO CLOSE. Buyer has no obligation to close on this
     transaction. If Buyer elects not to close for any reason, Seller's
     sole remedy is retention of the Earnest Money.

8.4  INDEMNIFICATION. Seller shall indemnify, defend, and hold harmless
     Buyer from and against any and all claims, damages, liabilities, costs,
     and expenses (including reasonable attorney fees) arising from or
     related to: (a) Seller's representations, (b) Property conditions
     existing prior to Closing, (c) Environmental contamination, and
     (d) Any third-party claims related to the Property.

================================================================================
                    ARTICLE 9 — GENERAL PROVISIONS
================================================================================

9.1  GOVERNING LAW. This Agreement shall be governed by the laws of the State
     of Georgia without regard to conflict of laws principles.

9.2  ATTORNEY REVIEW. Both Parties acknowledge the right to have this
     Agreement reviewed by an attorney of their choosing.

9.3  ENTIRE AGREEMENT. This Agreement constitutes the entire understanding
     between the Parties and supersedes all prior negotiations.

9.4  AMENDMENTS. This Agreement may only be amended in writing signed by both
     Parties.

9.5  COUNTERPARTS & ELECTRONIC SIGNATURES. This Agreement may be executed in
     counterparts and via electronic signature, each of which shall be
     deemed an original per O.C.G.A. Section 10-12-4 (Georgia UETA).

9.6  DISPUTE RESOLUTION. Any dispute shall be resolved through binding
     arbitration in {deal['county']} County, Georgia, under AAA rules.

9.7  WHOLESALING DISCLOSURE. Buyer hereby discloses:
     (a) Buyer is a real estate investor, not a licensed real estate broker.
     (b) Buyer intends to assign this contract to a third-party buyer.
     (c) Buyer is marketing the contractual interest, not the Property.
     (d) This transaction complies with O.C.G.A. Section 43-40-29 and the
         Georgia Real Estate Commission guidelines.

================================================================================
                        SIGNATURES
================================================================================

SELLER:

Signature: __________________________________  Date: _______________

Printed Name: {deal['seller']}

Title (if entity): __________________________


BUYER:

Signature: __________________________________  Date: _______________

Printed Name: [YOUR NAME]

Title: Managing Member / Principal


================================================================================
                        EXHIBIT A
                    LEGAL DESCRIPTION
================================================================================

Parcel ID: {deal['pid']}
Address: {deal['addr']}, {deal['city']}, {deal['state']} {deal['zip']}
County: {deal['county']} County, Georgia
Acreage: {deal['acres']} acres (approximate)
Zoning: {deal['zoning']}

[ATTACH FULL LEGAL DESCRIPTION FROM TITLE COMMITMENT]

================================================================================
END OF PURCHASE AND SALE AGREEMENT
================================================================================
"""


def generate_assignment(deal, buyer):
    assign_price = deal['offer'] + deal['fee']
    return f"""
================================================================================
           ASSIGNMENT OF PURCHASE AND SALE AGREEMENT
                State of Georgia | {deal['county']} County
================================================================================

                    ASSIGNMENT DATE: ___________________

THIS ASSIGNMENT OF PURCHASE AND SALE AGREEMENT ("Assignment") is entered into
as of the date written above, by and between:

ASSIGNOR:   [YOUR NAME] and/or assigns
            [YOUR ADDRESS]
            [YOUR PHONE] | [YOUR EMAIL]

ASSIGNEE:   {buyer['name']}
            Attn: {buyer['contact']}
            {buyer['addr']}
            Phone: {buyer['phone']}
            Email: {buyer['email']}

(Assignor and Assignee collectively referred to as the "Parties")

================================================================================
                         RECITALS
================================================================================

A.  Assignor entered into a Purchase and Sale Agreement ("Underlying PSA")
    dated _________________, {YEAR}, with {deal['seller']}
    ("Seller") for the purchase of certain real property described below.

B.  The Underlying PSA grants Assignor the right to assign the contract.

C.  Assignor desires to assign all rights, title, and interest in the
    Underlying PSA to Assignee, and Assignee desires to accept such
    assignment, subject to the terms below.

================================================================================
                    ARTICLE 1 — PROPERTY
================================================================================

1.1  PROPERTY ADDRESS:    {deal['addr']}, {deal['city']}, {deal['state']} {deal['zip']}
1.2  PARCEL ID:           {deal['pid']}
1.3  COUNTY:              {deal['county']} County, Georgia
1.4  ACREAGE:             {deal['acres']} acres (approximately)
1.5  ZONING:              {deal['zoning']}

================================================================================
                    ARTICLE 2 — ASSIGNMENT
================================================================================

2.1  ASSIGNMENT. Assignor hereby assigns, transfers, and conveys to Assignee
     all of Assignor's right, title, and interest in and to the Underlying
     PSA, including the right to purchase the Property.

2.2  ASSUMPTION. Assignee hereby accepts this Assignment and assumes all of
     the Buyer's obligations under the Underlying PSA, including the
     obligation to close on the purchase of the Property.

2.3  ORIGINAL PURCHASE PRICE. The purchase price in the Underlying PSA
     between Assignor and Seller is: ${deal['offer']:,.2f}

================================================================================
             ARTICLE 3 — ASSIGNMENT FEE (CONSIDERATION)
================================================================================

3.1  ASSIGNMENT FEE. In consideration for this Assignment, Assignee shall
     pay Assignor a non-refundable Assignment Fee of:

                    ${deal['fee']:,.2f}

     ("Assignment Fee")

3.2  PAYMENT OF ASSIGNMENT FEE. The Assignment Fee shall be paid as follows:

     (a) DEPOSIT: ${deal['fee'] * 0.10:,.2f} (10% of Assignment Fee) due
         within three (3) business days of execution of this Assignment,
         payable to Assignor or Assignor's designated closing attorney.

     (b) BALANCE: ${deal['fee'] * 0.90:,.2f} (90% of Assignment Fee) due at
         Closing, payable through the closing attorney's escrow.

3.3  TOTAL COST TO ASSIGNEE AT CLOSING:

     Original Purchase Price:     ${deal['offer']:,.2f}
     Assignment Fee:            + ${deal['fee']:,.2f}
     ──────────────────────────────────────────
     TOTAL:                       ${assign_price:,.2f}

3.4  NON-REFUNDABLE. The Assignment Fee Deposit is NON-REFUNDABLE once paid,
     except in the event of Assignor's material breach of this Assignment.

================================================================================
                    ARTICLE 4 — CLOSING
================================================================================

4.1  CLOSING. Closing shall occur per the terms of the Underlying PSA. All
     remaining contingency and inspection rights transfer to Assignee.

4.2  CLOSING ATTORNEY. A Georgia-licensed closing attorney shall conduct
     the closing as required by Georgia law.

4.3  SIMULTANEOUS CLOSE. At Assignor's option, the Assignment Fee and the
     purchase of the Property may be handled through a simultaneous close
     (also known as a "double close") rather than a direct assignment.

================================================================================
         ARTICLE 5 — ASSIGNOR PROTECTIONS (EXIT CLAUSES)
================================================================================

5.1  NO LIABILITY POST-ASSIGNMENT. Upon the execution of this Assignment and
     receipt of the Assignment Fee Deposit, Assignor shall be fully and
     irrevocably released from all obligations under the Underlying PSA.

5.2  NO WARRANTIES. Assignor makes NO warranties or representations regarding
     the Property's condition, value, zoning compliance, environmental status,
     title, or suitability for any purpose. Assignee accepts the Property
     "AS-IS, WHERE-IS."

5.3  ASSIGNEE'S DUE DILIGENCE. Assignee acknowledges that it has conducted
     or will conduct its own independent due diligence and is relying solely
     upon its own investigations and inspections.

5.4  INDEMNIFICATION. Assignee shall indemnify, defend, and hold harmless
     Assignor from any claims, damages, costs, or liabilities arising from:
     (a) Assignee's failure to close, (b) Property conditions discovered
     after assignment, and (c) Any third-party claims post-assignment.

5.5  LIMITATION OF ASSIGNOR'S LIABILITY. Assignor's maximum liability under
     this Assignment shall not exceed the amount of the Assignment Fee
     Deposit received by Assignor. In no event shall Assignor be liable for
     consequential, incidental, punitive, or special damages.

================================================================================
          ARTICLE 6 — COMPLIANCE & DISCLOSURES
================================================================================

6.1  WHOLESALE TRANSACTION DISCLOSURE. Both Parties acknowledge:
     (a) Assignor is a private real estate investor, not a licensed broker.
     (b) Assignor acquired equitable interest via the Underlying PSA.
     (c) Assignor is assigning contractual rights, not real property.
     (d) This transaction complies with O.C.G.A. Section 43-40-29.
     (e) Assignor is not acting as a real estate agent for any party.

6.2  GEORGIA CLOSING REQUIREMENT. Both Parties agree that a Georgia-licensed
     attorney shall oversee and conduct the Closing per state requirements.

6.3  FEDERAL COMPLIANCE. If the Property was built before 1978, lead-based
     paint disclosures shall be provided per 42 U.S.C. Section 4852d.

================================================================================
                    ARTICLE 7 — GENERAL
================================================================================

7.1  GOVERNING LAW. Georgia law governs. Venue: {deal['county']} County, GA.

7.2  ENTIRE AGREEMENT. This Assignment, together with the Underlying PSA,
     constitutes the complete agreement between the Parties.

7.3  AMENDMENTS. Only in writing signed by both Parties.

7.4  ELECTRONIC SIGNATURES. Valid per O.C.G.A. Section 10-12-4 (Georgia UETA).

7.5  SEVERABILITY. If any provision is found unenforceable, the remaining
     provisions remain in full force and effect.

7.6  TIME IS OF THE ESSENCE. Time is of the essence for all provisions.

7.7  CONFIDENTIALITY. The terms of this Assignment, including the Assignment
     Fee, are confidential between the Parties and shall not be disclosed
     to Seller or any third party without written consent.

================================================================================
                        SIGNATURES
================================================================================

ASSIGNOR:

Signature: __________________________________  Date: _______________

Printed Name: [YOUR NAME]

Title: Managing Member / Principal


ASSIGNEE:

Company: {buyer['name']}

Signature: __________________________________  Date: _______________

Printed Name: {buyer['contact']}

Title: ______________________________________


================================================================================
                    EXHIBIT A — UNDERLYING PSA
================================================================================

[ATTACH COPY OF ORIGINAL PURCHASE AND SALE AGREEMENT]

================================================================================
END OF ASSIGNMENT AGREEMENT
================================================================================
"""


# ── GENERATE ALL CONTRACTS ──
count_psa = 0
count_assign = 0

for deal in DEALS:
    safe = deal['addr'].replace(' ', '_').replace('/', '-')

    # PSA with Seller
    psa_path = PSA_DIR / f"PSA_{safe}_{deal['city']}.txt"
    psa_path.write_text(generate_psa(deal))
    count_psa += 1
    print(f"✅ PSA: {psa_path.name}")

    # Assignment for each buyer
    for buyer in deal['buyers']:
        bname = buyer['name'].replace(' ', '_').replace('/', '-').replace('.','')
        assign_path = ASSIGN_DIR / f"ASSIGN_{safe}_{bname}.txt"
        assign_path.write_text(generate_assignment(deal, buyer))
        count_assign += 1
        print(f"   📎 Assignment: {assign_path.name}")

print(f"\n{'='*60}")
print(f"  DONE — Generated {count_psa} PSAs + {count_assign} Assignments")
print(f"  PSA Folder:        {PSA_DIR}")
print(f"  Assignment Folder: {ASSIGN_DIR}")
print(f"{'='*60}")
