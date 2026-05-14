#!/usr/bin/env python3
"""Generate a beautiful HTML Deal Playbook that can be printed/saved as PDF."""
from build_playbook2_data import DEALS
from pathlib import Path

OUT = Path(__file__).parent.parent / "Exports" / "Deal_Playbook_2.html"

def deal_html(d):
    offer = int(d['lv'] * 0.55)
    fee = int(d['lv'] * 0.15)
    bp = offer + fee
    gmap = f"https://www.google.com/maps/search/{d['addr'].replace(' ','+')},+{d['city']},+GA+{d['zp']}"
    ss = d['ss'].replace('\n\n','</p><p>').replace('\n',' ')
    bs = d['bs'].replace('\n\n','</p><p>').replace('\n',' ')
    return f'''
    <div class="deal" style="page-break-inside:avoid;">
      <div class="deal-header">
        <div class="deal-num">DEAL #{d['n']}</div>
        <div class="deal-fee">${fee:,} Assignment Fee</div>
      </div>
      <div class="deal-addr">{d['addr']}, {d['city']}, GA {d['zp']}</div>
      <div class="deal-link"><a href="{gmap}" target="_blank">🗺️ View on Google Maps</a></div>
      <div class="cols">
        <div class="col">
          <h3>📊 Deal Math</h3>
          <table class="info"><tr><td>Land Value</td><td><strong>${d['lv']:,}</strong></td></tr>
          <tr><td>Your Offer (55%)</td><td>${offer:,}</td></tr>
          <tr class="highlight"><td>Your Fee</td><td><strong>${fee:,}</strong></td></tr>
          <tr><td>Buyer Pays</td><td>${bp:,}</td></tr></table>
        </div>
        <div class="col">
          <h3>📋 Property</h3>
          <table class="info"><tr><td>Acreage</td><td>{d['ac']} acres</td></tr>
          <tr><td>Zoning</td><td>{d['zn']}</td></tr>
          <tr><td>Liens</td><td>{d['liens']}</td></tr>
          <tr><td>Held</td><td>{d['held']}</td></tr>
          <tr><td>Paid</td><td>{d['paid']}</td></tr></table>
        </div>
      </div>
      <div class="contact-box seller-box">
        <h3>🏠 Seller</h3>
        <div class="name">{d['seller']}</div>
        <div class="detail">📍 {d['sloc']}</div>
        <div class="detail">📞 {d['sph']}</div>
        <div class="detail">📧 {d['sem']}</div>
      </div>
      <div class="script-box">
        <h3>📞 Seller Call Script</h3>
        <div class="script"><p>{ss}</p></div>
        <div class="leverage">💡 <strong>Leverage:</strong> {d['lev']}</div>
      </div>
      <div class="contact-box buyer-box">
        <h3>🎯 Buyer #1: {d['b1n']}</h3>
        <div class="detail">📞 {d['b1p']} &nbsp;|&nbsp; 📧 {d['b1e']}</div>
      </div>
      <div class="script-box buyer-script">
        <h3>📞 Buyer Pitch Script</h3>
        <div class="script"><p>{bs}</p></div>
      </div>
      <div class="contact-box buyer-box" style="margin-top:8px;">
        <h3>🎯 Buyer #2: {d['b2n']}</h3>
        <div class="detail">📞 {d['b2p']} &nbsp;|&nbsp; 📧 {d['b2e']}</div>
      </div>
    </div>'''

deals_html = '\n'.join(deal_html(d) for d in DEALS)

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Deal Playbook #2 — 15 Off-Market Leads</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ font-family:'Inter',sans-serif; background:#0f172a; color:#e2e8f0; padding:20px; }}
  .cover {{ text-align:center; padding:60px 20px; margin-bottom:30px; background:linear-gradient(135deg,#1e293b,#0f172a);
    border:1px solid #334155; border-radius:16px; }}
  .cover h1 {{ font-size:2.4em; font-weight:800; background:linear-gradient(135deg,#38bdf8,#818cf8,#a78bfa);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; margin-bottom:12px; }}
  .cover .sub {{ font-size:1.1em; color:#94a3b8; margin-bottom:20px; }}
  .cover .stat {{ display:inline-block; background:#1e293b; border:1px solid #334155; border-radius:12px;
    padding:16px 28px; margin:6px; }}
  .cover .stat .num {{ font-size:1.8em; font-weight:800; color:#38bdf8; }}
  .cover .stat .lbl {{ font-size:0.8em; color:#64748b; text-transform:uppercase; letter-spacing:1px; }}
  .deal {{ background:#1e293b; border:1px solid #334155; border-radius:16px; padding:28px;
    margin-bottom:24px; }}
  .deal-header {{ display:flex; justify-content:space-between; align-items:center; margin-bottom:4px; }}
  .deal-num {{ font-size:0.85em; font-weight:700; color:#818cf8; text-transform:uppercase; letter-spacing:2px; }}
  .deal-fee {{ font-size:1.3em; font-weight:800; color:#34d399; }}
  .deal-addr {{ font-size:1.4em; font-weight:700; color:#f1f5f9; margin-bottom:4px; }}
  .deal-link a {{ color:#38bdf8; text-decoration:none; font-size:0.9em; }}
  .deal-link a:hover {{ text-decoration:underline; }}
  .cols {{ display:flex; gap:16px; margin:16px 0; flex-wrap:wrap; }}
  .col {{ flex:1; min-width:250px; background:#0f172a; border-radius:12px; padding:16px; }}
  .col h3 {{ font-size:0.85em; color:#94a3b8; text-transform:uppercase; letter-spacing:1px; margin-bottom:10px; }}
  table.info {{ width:100%; border-collapse:collapse; }}
  table.info td {{ padding:5px 8px; font-size:0.9em; border-bottom:1px solid #1e293b; }}
  table.info td:first-child {{ color:#94a3b8; width:45%; }}
  table.info tr.highlight td {{ background:#064e3b; border-radius:6px; color:#34d399; font-weight:700; }}
  .contact-box {{ background:#0f172a; border-radius:12px; padding:16px; margin:12px 0;
    border-left:4px solid #818cf8; }}
  .seller-box {{ border-left-color:#f59e0b; }}
  .buyer-box {{ border-left-color:#38bdf8; }}
  .contact-box h3 {{ font-size:0.95em; color:#f1f5f9; margin-bottom:8px; }}
  .contact-box .name {{ font-size:1.1em; font-weight:700; color:#f59e0b; margin-bottom:6px; }}
  .contact-box .detail {{ font-size:0.9em; color:#cbd5e1; margin-bottom:3px; }}
  .script-box {{ background:#0f172a; border-radius:12px; padding:16px; margin:12px 0; }}
  .script-box h3 {{ font-size:0.85em; color:#94a3b8; text-transform:uppercase; letter-spacing:1px; margin-bottom:10px; }}
  .script {{ background:#1a1a2e; border-radius:8px; padding:16px; font-size:0.92em; line-height:1.7;
    color:#e2e8f0; border:1px solid #334155; font-style:italic; }}
  .buyer-script .script {{ border-left:3px solid #38bdf8; }}
  .leverage {{ margin-top:10px; padding:10px 14px; background:#422006; border-radius:8px;
    font-size:0.85em; color:#fbbf24; }}
  .call-order {{ background:#1e293b; border:1px solid #334155; border-radius:16px; padding:28px; }}
  .call-order h2 {{ font-size:1.4em; font-weight:800; color:#f1f5f9; margin-bottom:16px; }}
  .call-order table {{ width:100%; border-collapse:collapse; }}
  .call-order th {{ text-align:left; padding:10px 12px; background:#0f172a; color:#94a3b8;
    font-size:0.8em; text-transform:uppercase; letter-spacing:1px; }}
  .call-order td {{ padding:10px 12px; border-bottom:1px solid #334155; font-size:0.9em; }}
  .call-order tr:hover {{ background:#334155; }}
  .badge {{ display:inline-block; background:#064e3b; color:#34d399; font-weight:700; padding:2px 8px;
    border-radius:6px; font-size:0.8em; }}
  @media print {{
    body {{ background:white; color:#1e293b; padding:10px; }}
    .deal,.cover,.call-order {{ border:1px solid #ddd; page-break-inside:avoid; }}
    .col,.contact-box,.script-box {{ background:#f8fafc; }}
    .script {{ background:#f1f5f9; color:#1e293b; }}
    .deal-fee {{ color:#059669; }}
  }}
</style>
</head>
<body>
<div class="cover">
  <h1>Deal Playbook #2</h1>
  <div class="sub">15 Off-Market Vacant Land Opportunities — Gwinnett County & Surrounding Areas</div>
  <div class="sub" style="color:#64748b;">All Corporate Sellers with Verified Phone Numbers · May 2026</div>
  <div>
    <div class="stat"><div class="num">15</div><div class="lbl">Deals</div></div>
    <div class="stat"><div class="num">270+</div><div class="lbl">Total Acres</div></div>
    <div class="stat"><div class="num">$3.8M+</div><div class="lbl">Total Fees</div></div>
  </div>
</div>
{deals_html}
<div class="call-order">
  <h2>📞 Priority Call Order</h2>
  <table>
    <tr><th>#</th><th>Company</th><th>Phone</th><th>Why First</th></tr>
    <tr><td><span class="badge">1</span></td><td>CSX Transportation</td><td>(877) 835-8279</td><td>36 years vacant. Dedicated RE dept.</td></tr>
    <tr><td><span class="badge">2</span></td><td>Lidl US</td><td>(703) 214-3433</td><td>Dedicated RE email: realestate@lidl.us</td></tr>
    <tr><td><span class="badge">3</span></td><td>Prologis (Duke)</td><td>(678) 249-7001</td><td>43 acres. Kent Mason, GA Market.</td></tr>
    <tr><td><span class="badge">4</span></td><td>SE Freight Lines</td><td>(803) 794-7300</td><td>12 acres. Trucking surplus.</td></tr>
    <tr><td><span class="badge">5</span></td><td>Schwan's</td><td>(800) 533-5290</td><td>15.7 acres. Post-acquisition consolidation.</td></tr>
    <tr><td><span class="badge">6</span></td><td>Copart (NASDAQ)</td><td>(972) 868-4400</td><td>Paid $295K. Auto auction surplus.</td></tr>
    <tr><td><span class="badge">7</span></td><td>Penske (Rollins)</td><td>(855) 345-7268</td><td>Legacy asset. Doraville boom.</td></tr>
    <tr><td><span class="badge">8</span></td><td>Ryerson (NYSE)</td><td>(312) 292-5000</td><td>Steel co holding residential land.</td></tr>
    <tr><td><span class="badge">9</span></td><td>Stanley Martin</td><td>(703) 621-2050</td><td>National builder surplus.</td></tr>
    <tr><td><span class="badge">10</span></td><td>AMERCO (U-Haul)</td><td>(602) 263-6645</td><td>Paid $3.5M. Plans may have changed.</td></tr>
  </table>
</div>
<div style="text-align:center;padding:40px;color:#475569;font-size:0.8em;">
  ⚠️ Replace [YOUR NAME], [YOUR PHONE], [YOUR EMAIL] in all scripts before calling.<br>
  Generated May 2026 · Gwinnett County ArcGIS Data · For Private Use Only
</div>
</body></html>'''

OUT.write_text(html)
print(f"✅ HTML Playbook saved to: {OUT}")
print(f"   Open in Chrome → File → Print → Save as PDF")
