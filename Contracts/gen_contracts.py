#!/usr/bin/env python3
"""Generate GA-compliant PSA + Assignment contracts for all 10 deals."""
from pathlib import Path
from datetime import date

PSA = Path(__file__).parent / "PSA_Seller"
ASN = Path(__file__).parent / "Assignment_Buyer"
PSA.mkdir(exist_ok=True); ASN.mkdir(exist_ok=True)
YR = date.today().year

DEALS = [
  dict(pid="7077 001",addr="4175 Old Norcross Rd",city="Duluth",st="GA",zp="30096",county="Gwinnett",
    acres="18.40",zoning="RTH-Single Family Res-Twnhse",seller="AUTUMN VISTA ACQUISITION LP",
    seller_addr="3280 Bloor St W Ste 1400, Toronto ON M8X 2X3, Canada",
    fmv=4736600,offer=2605130,fee=710490,
    elec="Yes",water="City",sewer="City",gas="Yes",septic="No",well="No",liens="None",
    buyers=[("Starwood Capital Group","SFR Acquisitions","(770) 541-9046","sfr_inquiries@starwood.com","400 Galleria Pkwy Ste 1450, Atlanta GA 30339"),
            ("Invitation Homes","Atlanta Regional Office","(770) 442-3372","invitationhomes.com/contact-us","8601 Dunwoody Pl Ste 520, Sandy Springs GA 30350")]),
  dict(pid="7326 070",addr="5501 Cole Rd",city="Buford",st="GA",zp="30518",county="Gwinnett",
    acres="28.92",zoning="M1-Light Industry",seller="BFI WASTE SYSTEMS OF GEORGIA LLC (c/o Republic Services)",
    seller_addr="PO Box 29246, Phoenix AZ 85038",
    fmv=4409100,offer=2425005,fee=661365,
    elec="Verify",water="Verify",sewer="Verify",gas="Verify",septic="N/A",well="N/A",liens="None",
    buyers=[("Prologis Inc.","Kent Mason, GA Market Officer","(678) 249-7001","prologis.com/contact-us","3475 Piedmont Rd NE Ste 650, Atlanta GA 30305"),
            ("Shaheen & Company","Ben Newland","(770) 916-1775","info@shaheenco.com","3625 Cumberland Blvd SE Ste 250, Atlanta GA 30339")]),
  dict(pid="7348 013",addr="5610 Austin Garner Rd",city="Sugar Hill",st="GA",zp="30518",county="Gwinnett",
    acres="53.02",zoning="R100-Single Family Residence",seller="SERIES 20 OF SANSING HOLDINGS LLC",
    seller_addr="5705 Pensacola Blvd, Pensacola FL 32505",
    fmv=2120800,offer=1166440,fee=318120,
    elec="Yes",water="City",sewer="City",gas="Yes",septic="No",well="No",liens="None",
    buyers=[("Starwood Capital Group","SFR Acquisitions","(770) 541-9046","sfr_inquiries@starwood.com","400 Galleria Pkwy Ste 1450, Atlanta GA 30339"),
            ("Invitation Homes","Atlanta Regional Office","(770) 442-3372","invitationhomes.com/contact-us","8601 Dunwoody Pl Ste 520, Sandy Springs GA 30350")]),
  dict(pid="7034 092",addr="1350 Lakes Pkwy",city="Lawrenceville",st="GA",zp="30043",county="Gwinnett",
    acres="11.84",zoning="M1-Light Industry",seller="PJP HOLDINGS LLC",
    seller_addr="9005 Smiths Mill Rd N, New Albany OH 43054",
    fmv=1675500,offer=921525,fee=251325,
    elec="Yes",water="City",sewer="City",gas="Yes",septic="No",well="No",liens="None",
    buyers=[("Shaheen & Company","Ben Newland","(770) 916-1775","info@shaheenco.com","3625 Cumberland Blvd SE Ste 250, Atlanta GA 30339"),
            ("Prologis Inc.","Kent Mason","(678) 249-7001","prologis.com/contact-us","3475 Piedmont Rd NE Ste 650, Atlanta GA 30305")]),
  dict(pid="6040 158",addr="5100 Annistown Rd",city="Stone Mountain",st="GA",zp="30087",county="Gwinnett",
    acres="19.33",zoning="C2-General Business",seller="INGLES MARKETS INC",
    seller_addr="PO Box 6676, Asheville NC 28816",
    fmv=1600000,offer=880000,fee=240000,
    elec="Yes",water="City",sewer="City",gas="Yes",septic="No",well="No",liens="None",
    buyers=[("AOA Parish Real Estate Trust","Office Administrator","(404) 920-7800","Via certified letter","2401 Lake Park Dr SE, Smyrna GA 30080")]),
  dict(pid="6345 001",addr="River Bottom Dr",city="Peachtree Corners",st="GA",zp="30092",county="Gwinnett",
    acres="33.02",zoning="R100-Single Family Residence",seller="PARKER NATHAN N",
    seller_addr="825 W End Ave Apt 12-G, New York NY 10025",
    fmv=1359800,offer=747890,fee=203970,
    elec="Yes",water="City",sewer="City",gas="Yes",septic="No",well="No",liens="None",
    buyers=[("Invitation Homes","Atlanta Regional Office","(770) 442-3372","invitationhomes.com/contact-us","8601 Dunwoody Pl Ste 520, Sandy Springs GA 30350"),
            ("Starwood Capital Group","SFR Acquisitions","(770) 541-9046","sfr_inquiries@starwood.com","400 Galleria Pkwy Ste 1450, Atlanta GA 30339")]),
  dict(pid="7100 020",addr="2382 Gravel Springs Rd",city="Buford",st="GA",zp="30519",county="Gwinnett",
    acres="10.00",zoning="RA200-Agriculture/Residence",seller="HAWKINS WILLIAM",
    seller_addr="1110 Duncan Dr, Winter Springs FL 32708",
    fmv=372900,offer=205095,fee=55935,
    elec="Yes",water="City",sewer="City",gas="Yes",septic="No",well="No",liens="None",
    buyers=[("Turnkey Properties LP","Acquisitions","Skip trace","8175 Dogwood Trl, Cumming GA 30041","8175 Dogwood Trl, Cumming GA 30041")]),
  dict(pid="7135 013",addr="Rock Springs Rd",city="Buford",st="GA",zp="30519",county="Gwinnett",
    acres="12.04",zoning="RA200-Agriculture/Residence",seller="DIEGUEZ RODOLFO VALENTINO",
    seller_addr="915 E Kuiaha Rd, Haiku HI 96708",
    fmv=318700,offer=175285,fee=47805,
    elec="Yes",water="City",sewer="City",gas="Yes",septic="No",well="No",liens="None",
    buyers=[("Turnkey Properties LP","Acquisitions","Skip trace","8175 Dogwood Trl, Cumming GA 30041","8175 Dogwood Trl, Cumming GA 30041")]),
  dict(pid="7338 010",addr="5817 ORouke Rd",city="Buford",st="GA",zp="30518",county="Gwinnett",
    acres="8.20",zoning="R100-Single Family Residence",seller="OBE PETER",
    seller_addr="96 Spook Rock Rd, Suffern NY 10901",
    fmv=308300,offer=169565,fee=46245,
    elec="Yes",water="City",sewer="City",gas="Yes",septic="No",well="No",liens="None",
    buyers=[("Mora Leusterio","Principal","Skip trace","5240 Suwanee Dam Rd, Suwanee GA 30024","5240 Suwanee Dam Rd, Suwanee GA 30024")]),
  dict(pid="7326 040",addr="2341 Shoal Creek Rd",city="Buford",st="GA",zp="30518",county="Gwinnett",
    acres="6.24",zoning="R100-Single Family Residence",seller="WAGNER WILLIAM H",
    seller_addr="95 Burton St, Bristol CT 06010",
    fmv=303300,offer=166815,fee=45495,
    elec="Yes",water="City",sewer="City",gas="Yes",septic="No",well="No",liens="None",
    buyers=[("Mora Leusterio","Principal","Skip trace","5240 Suwanee Dam Rd, Suwanee GA 30024","5240 Suwanee Dam Rd, Suwanee GA 30024"),
            ("Turnkey Properties LP","Acquisitions","Skip trace","8175 Dogwood Trl, Cumming GA 30041","8175 Dogwood Trl, Cumming GA 30041")]),
]

def psa(d):
    return f"""
{'='*80}
PURCHASE AND SALE AGREEMENT — VACANT LAND
State of Georgia | {d['county']} County | {YR}
{'='*80}

CONTRACT DATE: ___________________
EFFECTIVE DATE: Date of last signature below

SELLER:  {d['seller']}
         {d['seller_addr']}

BUYER:   [YOUR NAME] and/or assigns
         [YOUR ADDRESS]
         [YOUR PHONE] | [YOUR EMAIL]

{'='*80}
ARTICLE 1 — PROPERTY DESCRIPTION
{'='*80}

Address:      {d['addr']}, {d['city']}, {d['st']} {d['zp']}
Parcel ID:    {d['pid']}
County:       {d['county']} County, Georgia
Acreage:      {d['acres']} acres (approx.)
Zoning:       {d['zoning']}
Legal Desc:   Per title commitment (Exhibit A)

UTILITIES (per {d['county']} County records):
  Electric:   {d['elec']}
  Water:      {d['water']}
  Sewer:      {d['sewer']}
  Gas:        {d['gas']}
  Septic:     {d['septic']}
  Well:       {d['well']}

LIENS & ENCUMBRANCES: {d['liens']} (per county records as of contract date)

{'='*80}
ARTICLE 2 — PURCHASE PRICE
{'='*80}

Purchase Price:     ${d['offer']:,.2f}
Earnest Money:      $10.00 (Ten Dollars), deposited with Closing Attorney
                    within five (5) business days of Effective Date.
Balance at Close:   ${d['offer'] - 10:,.2f} via certified funds or wire.

{'='*80}
ARTICLE 3 — ASSIGNMENT RIGHTS
{'='*80}

3.1  Buyer has the UNRESTRICTED RIGHT to assign this Agreement, in whole or
     part, to any person, entity, trust, LLC, or nominee at any time prior
     to Closing WITHOUT Seller's consent. Seller irrevocably consents.

3.2  Upon valid assignment and written notice, Buyer (Assignor) is FULLY
     RELEASED from ALL obligations. Assignee assumes all rights/obligations.

3.3  Any assignment fee is a private matter between Buyer and Assignee.
     Seller has NO right, claim, or interest in any assignment fee.

{'='*80}
ARTICLE 4 — FEASIBILITY PERIOD (PRIMARY EXIT)
{'='*80}

4.1  FEASIBILITY PERIOD: SIXTY (60) calendar days from Effective Date.
     Buyer may conduct ANY investigation including but not limited to:

     (a) Physical inspection           (g) FEMA flood zone verification
     (b) Phase I/II environmental      (h) Utility capacity confirmation
     (c) Soil & geotechnical testing   (i) Market & financial feasibility
     (d) Boundary & topographic survey (j) Partner/investor approval
     (e) Title examination & review    (k) Zoning & land-use verification
     (f) Appraisal                     (l) ANY other investigation

4.2  FREE TERMINATION: Buyer may terminate for ANY REASON OR NO REASON
     during the Feasibility Period by written notice to Seller. Upon
     termination:

     (a) Earnest Money IMMEDIATELY and FULLY refunded;
     (b) Buyer has ZERO further obligation or liability;
     (c) Agreement becomes null and void.

4.3  AUTOMATIC EXTENSION: If Buyer has not delivered termination notice by
     expiration of the Feasibility Period, Buyer may extend by an
     additional thirty (30) days by written notice, without additional
     consideration.

4.4  Seller grants Buyer and agents reasonable access for inspections.

{'='*80}
ARTICLE 5 — ADDITIONAL CONTINGENCIES (EACH AN INDEPENDENT EXIT)
{'='*80}

5.1  TITLE CONTINGENCY: Contingent on marketable, insurable title free of
     liens, encumbrances, easements, and defects unacceptable to Buyer in
     Buyer's SOLE discretion. If title is unsatisfactory, Buyer may
     terminate with full Earnest Money refund.

5.2  SURVEY CONTINGENCY: Contingent on Buyer's approval of boundary survey.
     If survey reveals encroachments, boundary disputes, or discrepancies,
     Buyer may terminate with full refund.

5.3  ENVIRONMENTAL CONTINGENCY: Contingent on Property being free of
     Hazardous Materials, contamination, underground storage tanks, and
     environmental issues per applicable federal, state, and local law
     including O.C.G.A. Section 12-8-90 et seq. (GA Hazardous Waste
     Management Act). Buyer may terminate with full refund if any
     environmental concern is discovered.

5.4  PARTNER/INVESTOR APPROVAL: Contingent on approval of Buyer's
     partners, members, managers, lenders, or investors in their SOLE
     AND ABSOLUTE discretion. If not approved, Buyer terminates with
     full refund.

5.5  FINANCING CONTINGENCY: If Buyer cannot obtain financing on terms
     acceptable to Buyer, Buyer may terminate with full refund.

5.6  APPRAISAL CONTINGENCY: If appraisal values Property below Purchase
     Price, Buyer may terminate with full refund.

5.7  GOVERNMENT APPROVAL: If any governmental authority denies, conditions,
     or delays any permit, rezoning, or approval needed for Buyer's
     intended use, Buyer may terminate with full refund.

5.8  FORCE MAJEURE: If any act of God, pandemic, government order, war,
     civil disturbance, or other event beyond Buyer's control materially
     affects the transaction, Buyer may terminate with full refund.

{'='*80}
ARTICLE 6 — PROPERTY CONDITION
{'='*80}

6.1  AS-IS, WHERE-IS: Buyer purchases in present condition with ALL faults.
     Seller makes NO warranties regarding condition, suitability, fitness,
     value, environmental status, utilities, or zoning compliance.

6.2  SELLER DISCLOSURES: Seller shall disclose ALL known material defects,
     environmental conditions, liens, assessments, pending litigation, HOA
     obligations, and facts materially affecting value per O.C.G.A.
     Section 44-1-16 and applicable Georgia law.

6.3  LEAD-BASED PAINT: If improvements were built before 1978, Seller
     shall provide disclosures per 42 U.S.C. Section 4852d.

{'='*80}
ARTICLE 7 — CLOSING
{'='*80}

7.1  CLOSING DATE: Within NINETY (90) calendar days from Effective Date,
     or thirty (30) days after Feasibility Period, whichever is LATER.

7.2  CLOSING ATTORNEY: Georgia-licensed real estate attorney selected by
     Buyer, as required by Georgia law (O.C.G.A. Section 15-19-50 et seq.).

7.3  SELLER'S COSTS: Transfer tax, Seller's attorney, outstanding liens,
     past-due property taxes, and HOA/assessment arrears.

7.4  BUYER'S COSTS: Buyer's attorney, title insurance, and recording fees.

7.5  EXTENSIONS: Buyer may extend Closing by thirty (30) days via written
     notice at least five (5) days prior. No additional consideration.

7.6  PRORATION: Property taxes prorated as of Closing Date.

{'='*80}
ARTICLE 8 — LIMITATION OF LIABILITY (CRITICAL — BUYER PROTECTION)
{'='*80}

8.1  LIQUIDATED DAMAGES: IF BUYER DEFAULTS, SELLER'S SOLE AND EXCLUSIVE
     REMEDY IS RETENTION OF THE $10.00 EARNEST MONEY AS LIQUIDATED
     DAMAGES. BOTH PARTIES AGREE THIS AMOUNT IS A REASONABLE ESTIMATE
     OF SELLER'S DAMAGES AND NOT A PENALTY.

8.2  WAIVER OF SPECIFIC PERFORMANCE: SELLER HEREBY IRREVOCABLY WAIVES
     ANY AND ALL RIGHTS TO SPECIFIC PERFORMANCE, CONSEQUENTIAL DAMAGES,
     PUNITIVE DAMAGES, INCIDENTAL DAMAGES, LOST PROFITS, OR ANY OTHER
     REMEDY AT LAW OR IN EQUITY AGAINST BUYER.

8.3  NO PERSONAL LIABILITY: Buyer has NO personal liability under this
     Agreement. Maximum exposure = $10.00 Earnest Money.

8.4  NO OBLIGATION TO CLOSE: Buyer has NO obligation to close. If Buyer
     does not close for any reason, Seller's sole remedy = $10.00.

8.5  INDEMNIFICATION BY SELLER: Seller shall indemnify, defend, and hold
     harmless Buyer from ALL claims, damages, liabilities, costs, and
     expenses (including attorney fees) arising from:
     (a) Seller's representations or omissions;
     (b) Property conditions existing prior to Closing;
     (c) Environmental contamination or hazardous materials;
     (d) Third-party claims related to the Property;
     (e) Tax liens, HOA liens, or assessment liens;
     (f) Any violation of federal, state, or local law.

8.6  SURVIVAL: Seller's indemnification obligations survive Closing and
     any termination of this Agreement.

{'='*80}
ARTICLE 9 — DISPUTE RESOLUTION
{'='*80}

9.1  MEDIATION FIRST: Any dispute shall first be submitted to mediation
     in {d['county']} County, Georgia, with costs shared equally.

9.2  BINDING ARBITRATION: If mediation fails within thirty (30) days,
     disputes shall be resolved by binding arbitration under AAA rules
     in {d['county']} County, Georgia. NO JURY TRIAL.

9.3  ATTORNEY FEES: Prevailing party entitled to reasonable attorney fees.

9.4  WAIVER OF JURY TRIAL: BOTH PARTIES KNOWINGLY, VOLUNTARILY, AND
     IRREVOCABLY WAIVE THE RIGHT TO TRIAL BY JURY.

{'='*80}
ARTICLE 10 — GENERAL PROVISIONS
{'='*80}

10.1  GOVERNING LAW: Georgia law, without conflict of laws principles.

10.2  WHOLESALING DISCLOSURE (O.C.G.A. Section 43-40-29):
      (a) Buyer is a private real estate investor, NOT a licensed broker;
      (b) Buyer intends to assign this contract to a third-party buyer;
      (c) Buyer is marketing contractual interest, NOT the Property;
      (d) Buyer is not acting as agent for any party;
      (e) Buyer acquired equitable interest via this Agreement.

10.3  ATTORNEY REVIEW: Both Parties have the right to attorney review.
      If either Party's attorney objects within ten (10) business days,
      this Agreement may be voided with full Earnest Money refund.

10.4  ENTIRE AGREEMENT: Supersedes all prior negotiations.

10.5  AMENDMENTS: Only in writing signed by both Parties.

10.6  ELECTRONIC SIGNATURES: Valid per O.C.G.A. Section 10-12-4 (UETA)
      and the federal ESIGN Act (15 U.S.C. Section 7001).

10.7  SEVERABILITY: Invalid provisions do not affect remaining terms.

10.8  TIME IS OF THE ESSENCE for all deadlines and obligations.

10.9  NOTICES: Written notice by email, certified mail, or hand delivery
      to addresses above. Effective upon receipt.

10.10 COUNTERPARTS: May be executed in counterparts, each an original.

10.11 BINDING EFFECT: Binds and inures to benefit of Parties, successors,
      and permitted assigns.

10.12 NO RECORDING: Neither Party shall record this Agreement or any
      memorandum without the other's written consent.

{'='*80}
SIGNATURES
{'='*80}

SELLER:
Signature: ___________________________________  Date: ______________
Printed:   {d['seller']}
Title:     ___________________________________

BUYER:
Signature: ___________________________________  Date: ______________
Printed:   [YOUR NAME]
Title:     Managing Member / Principal

{'='*80}
EXHIBIT A — LEGAL DESCRIPTION
{'='*80}

Parcel ID:  {d['pid']}
Address:    {d['addr']}, {d['city']}, {d['st']} {d['zp']}
County:     {d['county']} County, Georgia
Acreage:    {d['acres']} acres (approx.)
Zoning:     {d['zoning']}

[ATTACH LEGAL DESCRIPTION FROM TITLE COMMITMENT]

{'='*80}
END OF PURCHASE AND SALE AGREEMENT
{'='*80}
"""

def assign(d, b):
    return f"""
{'='*80}
ASSIGNMENT OF PURCHASE AND SALE AGREEMENT
State of Georgia | {d['county']} County | {YR}
{'='*80}

ASSIGNMENT DATE: ___________________

ASSIGNOR:  [YOUR NAME] and/or assigns
           [YOUR ADDRESS] | [YOUR PHONE] | [YOUR EMAIL]

ASSIGNEE:  {b[0]}
           Attn: {b[1]}
           {b[4]}
           Phone: {b[2]} | Email: {b[3]}

{'='*80}
ARTICLE 1 — RECITALS & PROPERTY
{'='*80}

A. Assignor entered into a PSA dated ____________, {YR}, with
   {d['seller']} ("Seller") for the property at:

   {d['addr']}, {d['city']}, {d['st']} {d['zp']}
   Parcel: {d['pid']} | {d['acres']} acres | {d['zoning']}

   Utilities: Elec={d['elec']} | Water={d['water']} | Sewer={d['sewer']}
              Gas={d['gas']} | Septic={d['septic']} | Well={d['well']}
   Liens:     {d['liens']}

B. The PSA grants Assignor the right to assign. Assignor desires to
   assign all rights to Assignee.

{'='*80}
ARTICLE 2 — ASSIGNMENT & ASSUMPTION
{'='*80}

2.1  Assignor assigns ALL right, title, and interest in the PSA to
     Assignee, including the right to purchase the Property.

2.2  Assignee accepts and assumes ALL Buyer obligations under the PSA.

2.3  Original Purchase Price (PSA): ${d['offer']:,.2f}

{'='*80}
ARTICLE 3 — ASSIGNMENT FEE
{'='*80}

3.1  ASSIGNMENT FEE: ${d['fee']:,.2f}

3.2  PAYMENT:
     (a) Deposit:  ${d['fee'] * 0.10:,.2f} (10%) — due within 3 business
         days, payable to Assignor's closing attorney escrow.
     (b) Balance:  ${d['fee'] * 0.90:,.2f} (90%) — due at Closing through
         closing attorney escrow.

3.3  TOTAL COST TO ASSIGNEE:
     Purchase Price:    ${d['offer']:,.2f}
     Assignment Fee:  + ${d['fee']:,.2f}
     ─────────────────────────────
     TOTAL:             ${d['offer'] + d['fee']:,.2f}

3.4  The Deposit is NON-REFUNDABLE once paid, except upon Assignor's
     material breach.

{'='*80}
ARTICLE 4 — ASSIGNOR PROTECTIONS
{'='*80}

4.1  FULL RELEASE: Upon execution and receipt of Deposit, Assignor is
     FULLY AND IRREVOCABLY released from ALL PSA obligations.

4.2  NO WARRANTIES: Assignor makes NO warranties regarding Property
     condition, value, zoning, environmental status, utilities, title,
     or suitability. Assignee accepts AS-IS, WHERE-IS.

4.3  ASSIGNEE DUE DILIGENCE: Assignee relies solely on its own
     investigations and inspections.

4.4  INDEMNIFICATION BY ASSIGNEE: Assignee indemnifies, defends, and
     holds harmless Assignor from ALL claims arising from:
     (a) Assignee's failure to close;
     (b) Property conditions discovered post-assignment;
     (c) Third-party claims post-assignment;
     (d) Environmental or regulatory matters.

4.5  LIMITATION: Assignor's maximum liability shall NOT exceed the
     Deposit amount received. NO consequential, incidental, punitive,
     or special damages against Assignor under any circumstances.

{'='*80}
ARTICLE 5 — COMPLIANCE & DISCLOSURES
{'='*80}

5.1  WHOLESALE DISCLOSURE (O.C.G.A. Section 43-40-29):
     (a) Assignor is a private investor, not a licensed broker;
     (b) Assignor acquired equitable interest via the PSA;
     (c) Assignor assigns contractual rights, not real property;
     (d) Assignor is not acting as agent for any party.

5.2  Georgia-licensed attorney shall oversee Closing per state law.

5.3  Lead-based paint disclosures if pre-1978 improvements (42 U.S.C.
     Section 4852d).

{'='*80}
ARTICLE 6 — GENERAL PROVISIONS
{'='*80}

6.1  Governing Law: Georgia. Venue: {d['county']} County.
6.2  Entire Agreement with the PSA.
6.3  Amendments: Written, signed by both Parties.
6.4  Electronic Signatures: Valid per O.C.G.A. Section 10-12-4.
6.5  Severability: Invalid provisions don't affect remainder.
6.6  Time is of the essence.
6.7  CONFIDENTIALITY: Assignment Fee is confidential. Not disclosed to
     Seller or third parties without written consent.
6.8  Dispute Resolution: Mediation then binding arbitration in
     {d['county']} County under AAA rules. Jury trial waived.
6.9  Attorney fees to prevailing party.

{'='*80}
SIGNATURES
{'='*80}

ASSIGNOR:
Signature: ___________________________________  Date: ______________
Printed:   [YOUR NAME]
Title:     Managing Member / Principal

ASSIGNEE:
Company:   {b[0]}
Signature: ___________________________________  Date: ______________
Printed:   {b[1]}
Title:     ___________________________________

{'='*80}
EXHIBIT A — ATTACH COPY OF ORIGINAL PSA
{'='*80}

{'='*80}
END OF ASSIGNMENT AGREEMENT
{'='*80}
"""

# Generate
pc = ac = 0
for d in DEALS:
    safe = d['addr'].replace(' ','_').replace("'","")
    (PSA / f"PSA_{safe}_{d['city']}.txt").write_text(psa(d)); pc += 1
    print(f"PSA: {safe}_{d['city']}")
    for b in d['buyers']:
        bn = b[0].replace(' ','_').replace('.','').replace('&','and')
        (ASN / f"ASSIGN_{safe}_to_{bn}.txt").write_text(assign(d, b)); ac += 1
        print(f"  -> Assignment to {b[0]}")

print(f"\nDONE: {pc} PSAs + {ac} Assignments in Contracts/")
