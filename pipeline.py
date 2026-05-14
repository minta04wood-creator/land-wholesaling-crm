import os
import json
import urllib.request
import urllib.parse
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# Configuration
WORKSPACE = os.path.expanduser("~/Desktop/LandWholesaling")
EMAILS_DIR = os.path.join(WORKSPACE, "GORA_Requests")
DATA_DIR = os.path.join(WORKSPACE, "Data")
os.makedirs(EMAILS_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

# 1. GORA Requests Generation
def generate_gora_emails():
    print("[Task 1] Generating GORA Request Emails...")
    counties = [
        {"name": "Gwinnett", "email": "taxcommissioner@gwinnettcounty.com"},
        {"name": "Hall", "email": "propertytax@hallcounty.org"},
        {"name": "Bartow", "email": "taxcommissioner@bartowcountyga.gov"},
        {"name": "Walton", "email": "WCTC@co.walton.ga.us"},
        {"name": "Rockdale", "email": "taxoffice@rockdalecountyga.gov"}
    ]
    
    template = """Subject: Open Records Request — Tax Delinquent Property List & Assessment Data
To: {email}
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8

Dear {county} County Tax Commissioner / Tax Assessor,

Pursuant to the Georgia Open Records Act (O.C.G.A. § 50-18-70 et seq.),
I am requesting copies of the following public records:

1. CURRENT TAX DELINQUENT PROPERTY LIST (Fi.Fa. List)
   - All properties with delinquent property taxes
   - Including: Parcel ID, owner name, mailing address, property address,
     tax amount owed, years delinquent, legal description, acreage

2. CURRENT TAX DIGEST / ASSESSMENT ROLL (if available in digital format)
   - All parcels in {county} County
   - Including: Parcel ID, owner name, mailing address, property address,
     land use code, acreage, fair market value, assessed value,
     last sale date, last sale price

I request this data in electronic format (CSV, Excel, or database export
preferred). I understand there may be reasonable charges for this request
and am willing to pay up to $50 for the cost of production.

Please contact me if you have any questions regarding this request.

Thank you,

[Your Name]
[Your Phone Number]
"""
    
    for county in counties:
        content = template.format(county=county["name"], email=county["email"])
        filepath = os.path.join(EMAILS_DIR, f"GORA_Request_{county['name']}.eml")
        with open(filepath, "w") as f:
            f.write(content)
        print(f"  -> Created email draft for {county['name']}")

# 2. Download Parcel Data (Rockdale Sample)
def download_rockdale_parcels():
    print("\n[Task 2] Downloading Rockdale Parcel Data (Sample 1000 records)...")
    # Rockdale County Parcels REST URL
    url = "https://services.arcgis.com/seTexOicoRXDvRsJ/arcgis/rest/services/Parcels_Enriched/FeatureServer/0/query"
    params = {
        "where": "1=1",
        "outFields": "STATE_PARCEL_NO,OWNER_NAME,MAILING_ADDRESS_LINE_1,LOCATION_ADDRESS,TOTAL_NET_ACRES,PARCEL_TYPE,TOTAL_ASSESSED_VALUE",
        "f": "json",
        "resultRecordCount": 1000,
        "outSR": "4326" # WGS84 for lat/lon
    }
    
    query_string = urllib.parse.urlencode(params)
    req_url = f"{url}?{query_string}"
    
    req = urllib.request.Request(req_url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            output_file = os.path.join(DATA_DIR, "rockdale_parcels_sample.json")
            with open(output_file, "w") as f:
                json.dump(data, f, indent=2)
            print(f"  -> Downloaded {len(data.get('features', []))} features to {output_file}")
            return data.get('features', [])
    except Exception as e:
        print(f"  -> Failed to download: {e}")
        return []

# 3. Filter Data
def filter_parcels(features):
    print("\n[Task 3] Filtering for Vacant + Absentee Owners...")
    filtered = []
    for feature in features:
        attr = feature.get('attributes', {})
        site_addr = str(attr.get('LOCATION_ADDRESS', '')).strip().upper()
        mail_addr = str(attr.get('MAILING_ADDRESS_LINE_1', '')).strip().upper()
        parcel_type = str(attr.get('PARCEL_TYPE', '')).strip().upper()
        
        # A property without a physical address is almost certainly vacant land
        is_vacant = ('VACANT' in parcel_type) or (parcel_type == 'TRACT') or (site_addr == '' or site_addr == 'None')
        
        # Absentee = Mail Address exists, AND (Site Address is blank OR they don't match)
        if site_addr == '' or site_addr == 'NONE':
            is_absentee = True
        else:
            # Check if the street number/name from site address is inside mailing address
            is_absentee = site_addr not in mail_addr

        if is_absentee and is_vacant:
            filtered.append(feature)
            
    print(f"  -> Found {len(filtered)} prime vacant absentee-owned parcels out of {len(features)}")
    return filtered

# 4. Check FEMA Flood Maps
def check_fema_flood(feature):
    geom = feature.get('geometry')
    if not geom or 'x' not in geom or 'y' not in geom:
        return False
    
    url = "https://hazards.fema.gov/gis/nfhl/rest/services/public/NFHL/MapServer/28/query"
    params = {
        "geometry": f"{geom['x']},{geom['y']}",
        "geometryType": "esriGeometryPoint",
        "spatialRel": "esriSpatialRelIntersects",
        "f": "json",
        "inSR": "4326"
    }
    
    try:
        req_url = f"{url}?{urllib.parse.urlencode(params)}"
        req = urllib.request.Request(req_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            return len(data.get('features', [])) > 0
    except:
        return False

def run_pipeline():
    generate_gora_emails()
    features = download_rockdale_parcels()
    filtered = filter_parcels(features)
    
    if filtered:
        print("\n[Task 4] Cross-referencing top 20 with FEMA Flood Maps in parallel...")
        subset = filtered[:20]
        results = []
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            flood_status = list(executor.map(check_fema_flood, subset))
            
        final_leads = []
        for feat, is_flood in zip(subset, flood_status):
            attr = feat['attributes']
            # We want properties NOT in flood zones
            if not is_flood:
                final_leads.append({
                    "PIN": attr.get('STATE_PARCEL_NO'),
                    "OWNER": attr.get('OWNER_NAME'),
                    "ACREAGE": attr.get('TOTAL_NET_ACRES'),
                    "IN_FLOOD_ZONE": False
                })
        
        leads_file = os.path.join(DATA_DIR, "final_wholesaling_leads.json")
        with open(leads_file, "w") as f:
            json.dump(final_leads, f, indent=2)
            
        print(f"  -> Pipeline complete! Found {len(final_leads)} prime leads (Absentee, Not in Flood Zone).")
        print(f"  -> Leads saved to {leads_file}")

if __name__ == "__main__":
    run_pipeline()
