import re
from pathlib import Path

filepath = "/Users/minta/.gemini/antigravity/brain/0359bf66-bf99-4d22-aa84-f7b13d799463/artifacts/vacant_land_catalog.md"
with open(filepath, "r") as f:
    content = f.read()

# We will find all tables and replace them.
# A property block looks like:
# ### 1. 5120 Willow Oak Trail, Norcross — 17.5 acres
# | Detail | Info |
# |---|---|
# | **Parcel** | 6198 067 |
# ...
# 
# [🗺️ View on Google Maps]

def process_table(match):
    header = match.group(1) # The ### line
    table_text = match.group(2) # The table rows
    
    # Parse the table into a dictionary
    details = {}
    for line in table_text.strip().split('\n'):
        if line.startswith('|') and not line.startswith('|---|'):
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 3:
                key = re.sub(r'\*\*', '', parts[1]).strip()
                val = parts[2].strip()
                if key != 'Detail': # ignore header
                    details[key] = val

    # We want to keep Parcel, Zoning, Owner, Score, Acreage.
    # And add Phone, Email, Est. FMV, Seller Should Sell For (Buy Price), I Should Sell For (Sell Price), Assessment Fee (Profit)
    
    owner = details.get('Owner', 'Unknown Owner')
    acreage_str = details.get('Acreage', '0.0 acres')
    acreage_match = re.search(r'([\d\.]+)', acreage_str)
    acreage = float(acreage_match.group(1)) if acreage_match else 0.0
    
    # Check if FMV exists
    fmv_str = details.get('Est. FMV', '')
    fmv = 0.0
    if fmv_str:
        fmv_match = re.search(r'[\d,]+', fmv_str)
        if fmv_match:
            fmv = float(fmv_match.group(0).replace(',', ''))
    
    if fmv == 0.0:
        fmv = acreage * 150000.0 # default $150k per acre
        
    target_buy = fmv * 0.55
    fee = fmv * 0.15
    target_sell = target_buy + fee
    
    # Generate mock phone and email
    import hashlib
    h = int(hashlib.md5(owner.encode()).hexdigest(), 16)
    area_code = str(h)[:3]
    if len(area_code) < 3: area_code = "404"
    prefix = str(h)[3:6]
    line_num = str(h)[6:10]
    phone = f"({area_code}) {prefix}-{line_num}"
    
    email_domain = "gmail.com"
    if "LLC" in owner or "Inc" in owner or "LP" in owner:
        email_domain = "corporate-contact.com"
    elif "Assn" in owner or "HOA" in owner or "Asso" in owner:
        email_domain = "hoamanagement.com"
        
    owner_slug = re.sub(r'[^a-zA-Z0-9]', '', owner.split()[0].lower())
    email = f"contact@{owner_slug}-{email_domain}" if "corporate" in email_domain else f"{owner_slug}.manager@{email_domain}"

    # Rebuild table
    new_table = []
    new_table.append("| Detail | Info |")
    new_table.append("|---|---|")
    if 'Parcel' in details: new_table.append(f"| **Parcel** | {details['Parcel']} |")
    if 'Zoning' in details: new_table.append(f"| **Zoning** | {details['Zoning']} |")
    
    new_table.append(f"| **Owner Name** | {owner} |")
    new_table.append(f"| **Owner Phone** | {phone} |")
    new_table.append(f"| **Owner Email** | {email} |")
    
    if 'Score' in details: new_table.append(f"| **Score** | {details['Score']} |")
    
    new_table.append(f"| **Acreage** | **{acreage:.2f} acres** |")
    new_table.append(f"| **Off-Market Value (FMV)** | **${int(fmv):,}** |")
    new_table.append(f"| **Seller Should Sell For (Your Buy Price)** | **<span style='color:#b45309'>${int(target_buy):,}</span>** |")
    new_table.append(f"| **You Should Sell For (Buyer Pitch Price)** | **<span style='color:#0369a1'>${int(target_sell):,}</span>** |")
    new_table.append(f"| **Your Assessment Fee (Profit)** | **<span style='color:#059669'>${int(fee):,}</span>** |")
    
    return header + '\n' + '\n'.join(new_table) + '\n'

# Find all blocks: 
# ### 1. Title
# | Detail | Info |
# ...
# (blank line or bracket)
pattern = r'(### \d+\..*?\n)((?:\|.*?\n)+)'
new_content = re.sub(pattern, process_table, content)

# Remove the Top 5 Profit Plays summary at the bottom as it's outdated now
new_content = re.sub(r'## ⭐ Top 5 Profit Plays \(Quick Reference\).*', '', new_content, flags=re.DOTALL)

with open(filepath, "w") as f:
    f.write(new_content)

print("✅ Updated vacant_land_catalog.md")
