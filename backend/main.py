import os
import requests
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Land Wholesaling API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For local development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/intel")
def get_buyer_intel(buyer: str = Query(..., description="Target buyer name")):
    """
    Calls the Exa Neural Search API to find real-time acquisitions and news about the buyer.
    """
    exa_key = os.getenv("EXA_API_KEY")
    if not exa_key:
        # Fallback to simulated data if no key is provided, so the frontend doesn't crash
        return {
            "status": "success",
            "intel": f"EXA MCP SEARCH RESULTS [MOCK]:\n- {buyer} recently announced a $50M expansion in Gwinnett County logistics infrastructure.\n- They just closed a 12 acre parcel in neighboring Forsyth County last month.\n- Key decision maker to reference: Director of Land Acquisitions.\n\n(Note: Add EXA_API_KEY to backend/.env to see real live-searched results!)"
        }

    url = "https://api.exa.ai/search"
    headers = {
        "x-api-key": exa_key,
        "Content-Type": "application/json"
    }
    payload = {
        "query": f"latest land acquisitions and developments by {buyer} in Georgia",
        "type": "auto",
        "num_results": 3,
        "contents": {
            "highlights": True
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        
        intel_lines = [f"EXA MCP LIVE SEARCH RESULTS FOR {buyer}:"]
        for res in data.get('results', []):
            title = res.get('title', 'Unknown Source')
            highlights = res.get('highlights', ['No highlights available.'])
            intel_lines.append(f"- {title}: {highlights[0]}")
            
        return {"status": "success", "intel": "\n\n".join(intel_lines)}
    except Exception as e:
        return {"status": "error", "intel": f"Error contacting Exa API: {str(e)}"}


@app.get("/api/risk")
def check_environmental_risk(ac: float = Query(...), zn: str = Query(...)):
    """
    Simulates checking environmental APIs (FEMA, Wetlands, EPA) based on acreage and zoning.
    """
    risks = []
    
    # Simple algorithmic rules simulating a real GIS backend
    if ac > 10:
        risks.append("Potential Wetlands on Northern Boundary (Tract > 10 Acres)")
    if 'M' in zn.upper() or 'IND' in zn.upper():
        risks.append("Phase 1 Environmental Recommended (Industrial Zoning)")
    if 'R' in zn.upper() and ac < 2:
        risks.append("Check Setbacks & Sewer Access for Residential Density")
        
    if not risks:
        risks.append("No immediate environmental red flags found.")
        
    return {"status": "success", "risks": risks}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
