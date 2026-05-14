#!/usr/bin/env python3
"""Generate a beautiful HTML document for the Contact Match List Scripts."""
import sys
from pathlib import Path

# Add Outreach dir to path so we can import the playbook data
sys.path.append(str(Path(__file__).parent.parent / "Outreach"))
from build_playbook2_data import DEALS

OUT = Path(__file__).parent.parent / "Exports" / "contact_match_list_scripts.html"

def script_html(d):
    target_buy = int(d['lv'] * 0.55)
    fee = int(d['lv'] * 0.15)
    target_sell = target_buy + fee
    
    ss = d['ss'].replace('\n\n', '</p><p>').replace('\n', ' ')
    bs = d['bs'].replace('\n\n', '</p><p>').replace('\n', ' ')
    
    return f'''
    <div class="match-card">
      <div class="match-header">
        <div class="match-title">🎯 MATCH #{d['n']}: {d['seller']} ➔ {d['b1n']}</div>
      </div>
      <div class="property-info">
        <strong>Property:</strong> {d['ac']} acres in {d['city']} (Zoning: {d['zn']})<br>
        <strong>Target Buy Price:</strong> ${target_buy:,} &nbsp;|&nbsp; 
        <strong>Target Sell Price:</strong> ${target_sell:,} &nbsp;|&nbsp; 
        <strong style="color:#059669;">Assignment Fee: ${fee:,}</strong>
      </div>
      
      <div class="script-section seller-section">
        <h3>📞 SELLER SCRIPT: {d['seller']}</h3>
        <div class="contact-number"><strong>Number:</strong> {d['sph']}</div>
        <div class="script-box">
          <p>{ss}</p>
        </div>
        <div class="leverage"><strong>💡 Leverage / Talking Point:</strong> {d['lev']}</div>
      </div>

      <div class="script-section buyer-section">
        <h3>📞 BUYER SCRIPT: {d['b1n']}</h3>
        <div class="contact-number"><strong>Number:</strong> {d['b1p']}</div>
        <div class="script-box">
          <p>{bs}</p>
        </div>
      </div>
    </div>
    '''

html_content = '\n'.join(script_html(d) for d in DEALS)

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Contact Match List Scripts</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Georgia&family=Inter:wght@400;600;700&display=swap');
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ 
    font-family: 'Inter', sans-serif; 
    background: #f4f4f5; 
    color: #18181b; 
    padding: 30px; 
    line-height: 1.6;
  }}
  .container {{
    max-width: 900px;
    margin: 0 auto;
    background: white;
    padding: 40px;
    border-radius: 8px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  }}
  .header {{
    text-align: center;
    border-bottom: 2px solid #e4e4e7;
    padding-bottom: 20px;
    margin-bottom: 30px;
  }}
  .header h1 {{
    font-family: 'Georgia', serif;
    font-size: 2.2em;
    color: #0f172a;
    margin-bottom: 10px;
  }}
  .header p {{
    color: #52525b;
    font-size: 1.1em;
  }}
  .match-card {{
    border: 1px solid #d4d4d8;
    border-radius: 8px;
    margin-bottom: 30px;
    background: #fafafa;
    page-break-inside: avoid;
  }}
  .match-header {{
    background: #0f172a;
    color: white;
    padding: 15px 20px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
  }}
  .match-title {{
    font-size: 1.2em;
    font-weight: 700;
  }}
  .property-info {{
    padding: 15px 20px;
    background: #f1f5f9;
    border-bottom: 1px solid #e2e8f0;
    font-size: 0.95em;
  }}
  .script-section {{
    padding: 20px;
  }}
  .seller-section {{
    border-bottom: 1px dashed #d4d4d8;
  }}
  .script-section h3 {{
    font-size: 1.05em;
    color: #3f3f46;
    margin-bottom: 5px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }}
  .seller-section h3 {{ color: #b45309; }}
  .buyer-section h3 {{ color: #0369a1; }}
  .contact-number {{
    font-size: 0.95em;
    color: #52525b;
    margin-bottom: 10px;
  }}
  .script-box {{
    background: white;
    border-left: 4px solid #d4d4d8;
    padding: 15px;
    font-family: 'Georgia', serif;
    font-size: 1.05em;
    font-style: italic;
    color: #27272a;
  }}
  .seller-section .script-box {{ border-left-color: #f59e0b; }}
  .buyer-section .script-box {{ border-left-color: #0ea5e9; }}
  .leverage {{
    margin-top: 15px;
    padding: 10px 15px;
    background: #fef3c7;
    border-radius: 4px;
    font-size: 0.9em;
    color: #92400e;
  }}
  @media print {{
    body {{ background: white; padding: 0; }}
    .container {{ box-shadow: none; padding: 0; max-width: 100%; }}
    .match-card {{ border-color: #e4e4e7; }}
  }}
</style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>Master Phone Scripts: Seller & Buyer Matches</h1>
      <p>Use these scripts when calling the targeted corporate sellers and their matched institutional buyers.</p>
    </div>
    {html_content}
  </div>
</body>
</html>
'''

OUT.write_text(html)
print(f"✅ HTML Script Document saved to: {OUT}")
print(f"   Open in Chrome → File → Print → Save as PDF")
