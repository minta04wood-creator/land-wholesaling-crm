#!/usr/bin/env python3
import sys
from pathlib import Path

# Add Outreach dir to path so we can import the playbook data
sys.path.append(str(Path(__file__).parent.parent / "Outreach"))
from build_playbook2_data import DEALS

OUT = Path(__file__).parent.parent / "Exports" / "seller_contact_and_deal_math.html"

def row_html(d):
    fmv = d['lv']
    target_buy = int(fmv * 0.55)
    fee = int(fmv * 0.15)
    target_sell = target_buy + fee

    parcel = d.get('parcel', 'Check County Map')
    
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

    return f'''
    <tr>
      <td class="text-center font-bold">#{d['n']}</td>
      <td><strong>{d['seller']}</strong><br><span class="text-sm text-gray">{parcel}</span></td>
      <td>{d['sph']}<br><span class="text-sm text-gray">{semail}</span></td>
      <td>{d['city']}<br><strong>{d['ac']} ac</strong> ({d['zn']})</td>
      <td class="money">${fmv:,}</td>
      <td class="money offer">${target_buy:,}</td>
      <td class="money pitch">${target_sell:,}</td>
      <td class="money profit">${fee:,}</td>
    </tr>
    '''

table_rows = '\n'.join(row_html(d) for d in DEALS)

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Seller Contacts & Deal Math Summary</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ 
    font-family: 'Inter', sans-serif; 
    background: #f4f4f5; 
    color: #18181b; 
    padding: 30px; 
    line-height: 1.5;
  }}
  .container {{
    max-width: 1200px;
    margin: 0 auto;
    background: white;
    padding: 40px;
    border-radius: 8px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  }}
  h1 {{ color: #0f172a; margin-bottom: 10px; font-size: 2.2em; }}
  p.subtitle {{ color: #52525b; font-size: 1.1em; margin-bottom: 30px; }}
  
  table {{
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 40px;
  }}
  th, td {{
    padding: 12px 15px;
    text-align: left;
    border-bottom: 1px solid #e4e4e7;
    font-size: 0.95em;
  }}
  th {{
    background: #0f172a;
    color: white;
    font-weight: 600;
    position: sticky;
    top: 0;
  }}
  tbody tr:hover {{ background-color: #f8fafc; }}
  .text-center {{ text-align: center; }}
  .font-bold {{ font-weight: 700; }}
  .text-sm {{ font-size: 0.85em; }}
  .text-gray {{ color: #71717a; }}
  .money {{ text-align: right; font-variant-numeric: tabular-nums; }}
  .offer {{ color: #b45309; font-weight: 600; }}
  .pitch {{ color: #0369a1; font-weight: 600; }}
  .profit {{ color: #059669; font-weight: 700; font-size: 1.1em; }}
  
  .key-breakdown {{
    background: #f8fafc;
    border-left: 4px solid #0f172a;
    padding: 20px;
    border-radius: 0 8px 8px 0;
  }}
  .key-breakdown h3 {{ margin-bottom: 10px; color: #0f172a; }}
  .key-breakdown ul {{ margin-left: 20px; }}
  .key-breakdown li {{ margin-bottom: 8px; color: #3f3f46; }}
  
  @media print {{
    body {{ background: white; padding: 0; }}
    .container {{ box-shadow: none; padding: 0; max-width: 100%; }}
  }}
</style>
</head>
<body>
  <div class="container">
    <h1>Seller Contacts & Deal Math Summary</h1>
    <p class="subtitle">Consolidated list of your 15 corporate vacant land targets, contact info, and complete deal math.</p>
    
    <table>
      <thead>
        <tr>
          <th class="text-center">Deal</th>
          <th>Seller & Parcel</th>
          <th>Contact Info</th>
          <th>Location & Size</th>
          <th class="money">Est. Market Value</th>
          <th class="money">Max Allowable Offer<br><span class="text-sm text-gray">(Buy Price)</span></th>
          <th class="money">Buyer Pitch Price<br><span class="text-sm text-gray">(Sell Price)</span></th>
          <th class="money">Target Profit<br><span class="text-sm text-gray">(Your Fee)</span></th>
        </tr>
      </thead>
      <tbody>
        {table_rows}
      </tbody>
    </table>

    <div class="key-breakdown">
      <h3>🔑 Deal Math Breakdown</h3>
      <ul>
        <li><strong>Max Allowable Offer (Buy Price):</strong> 55% of Est. Market Value. The absolute highest you should pay.</li>
        <li><strong>Target Profit (Assignment Fee):</strong> Your 15% cut of the deal for locking it up.</li>
        <li><strong>Buyer Pitch Price (Sell Price):</strong> Buy Price + Your Profit. Leaves the buyer with a ~30% discount off market value.</li>
      </ul>
    </div>
  </div>
</body>
</html>
'''

OUT.write_text(html)
print(f"✅ HTML Document saved to: {OUT}")
