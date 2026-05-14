import re
import json
from pathlib import Path

# Paths
catalog_path = "/Users/minta/.gemini/antigravity/brain/0359bf66-bf99-4d22-aa84-f7b13d799463/artifacts/vacant_land_catalog.md"
dashboard_data_path = Path("/Users/minta/Desktop/LandWholesaling/LandDashboard/src/data.ts")

with open(catalog_path, "r") as f:
    content = f.read()

deals = []
start_index = 16 # Start deal numbering from 16 since 1-15 are already in playbook

# Match property blocks
pattern = r'(### \d+\..*?\n)\s*((?:\|.*?\n)+)'
matches = re.finditer(pattern, content)

for match in matches:
    header = match.group(1)
    table_text = match.group(2)
    
    # Extract Title (e.g. "### 1. 5120 Willow Oak Trail, Norcross — 17.5 acres")
    title_match = re.search(r'### \d+\. (.*?), (.*?) —', header)
    address = title_match.group(1).strip() if title_match else "Unknown Address"
    city = title_match.group(2).strip() if title_match else "Gwinnett County"
    
    # Extract details
    details = {}
    for line in table_text.strip().split('\n'):
        if line.startswith('|') and not line.startswith('|---|'):
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 3:
                key = re.sub(r'\*\*', '', parts[1]).strip()
                val = re.sub(r'<[^>]+>', '', parts[2]).strip() # strip HTML tags like <span...>
                val = re.sub(r'\*\*', '', val).strip()
                if key != 'Detail':
                    details[key] = val

    # Parse required fields
    seller = details.get('Owner Name', 'Unknown Owner')
    phone = details.get('Owner Phone', '(000) 000-0000')
    email = details.get('Owner Email', 'contact@email.com')
    zoning = details.get('Zoning', 'R100')
    parcel = details.get('Parcel', 'N/A')
    
    acreage_str = details.get('Acreage', '0.0 acres')
    ac_m = re.search(r'([\d\.]+)', acreage_str)
    ac = float(ac_m.group(1)) if ac_m else 0.0
    
    fmv_str = details.get('Off-Market Value (FMV)', '$0')
    fmv_str = re.sub(r'[^\d]', '', fmv_str)
    lv = float(fmv_str) if fmv_str else 0.0
    
    # Determine target buyer based on zoning
    if 'M1' in zoning or 'C2' in zoning:
        b1n = "Prologis — Kent Mason"
        b1p = "(404) 768-9800"
        buyer_type = "Industrial"
    elif 'RM' in zoning or 'RTH' in zoning:
        b1n = "Toll Brothers — Land Acquisition"
        b1p = "(770) 552-8880"
        buyer_type = "Townhome/Multi-family"
    else:
        b1n = "D.R. Horton — Atlanta Division"
        b1p = "(770) 730-5522"
        buyer_type = "Single-Family Developer"
        
    # Generate scripts
    ss = f"""Hi, this is a direct inquiry for the disposition decision-maker at {seller}.
    
We are looking to acquire {ac} acres of {zoning} zoned land in {city} (Parcel {parcel}).
Our analysts have reviewed the site off {address} and we are prepared to make a cash offer at ${(lv*0.55):,.0f} with a 30-day close.
    
Are you open to divesting this asset from your portfolio?"""

    bs = f"""Kent/Acquisitions Team,
    
We have a direct-to-seller assignment available for {ac} acres of {buyer_type} land in {city} ({zoning}).
Off-market value is estimated at ${lv:,.0f}. We can assign this to you for ${(lv*0.55 + lv*0.15):,.0f}, which leaves ~30% meat on the bone for your development proforma.
    
Let me know if you want the parcel map and demographics packet."""

    lev = f"Absentee owner / holding surplus land. They are paying property taxes on {ac} acres of vacant dirt."

    deal = {
        "n": start_index,
        "parcel": parcel,
        "ac": ac,
        "city": city,
        "zn": zoning,
        "seller": seller,
        "sph": phone,
        "semail": email,
        "lv": lv,
        "b1n": b1n,
        "b1p": b1p,
        "ss": ss,
        "bs": bs,
        "lev": lev
    }
    
    deals.append(deal)
    start_index += 1

# Read existing data from data.ts
with open(dashboard_data_path, "r") as f:
    existing_data_str = f.read()
    
# Extract the JSON array from data.ts
json_str = existing_data_str.replace("export const deals = ", "").strip()
if json_str.endswith(";"):
    json_str = json_str[:-1]

try:
    existing_deals = json.loads(json_str)
except Exception as e:
    print("Failed to parse existing deals:", e)
    existing_deals = []

# Merge and remove duplicates based on parcel number
merged_deals = existing_deals.copy()
existing_parcels = {d.get('parcel') for d in existing_deals}

for d in deals:
    if d['parcel'] not in existing_parcels:
        merged_deals.append(d)
        existing_parcels.add(d['parcel'])

# Write back to data.ts
new_ts_content = "export const deals = " + json.dumps(merged_deals, indent=2) + ";\n"
with open(dashboard_data_path, "w") as f:
    f.write(new_ts_content)

print(f"✅ Appended {len(deals)} new vacant land deals. Dashboard now has {len(merged_deals)} total deals!")
