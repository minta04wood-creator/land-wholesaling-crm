import json
import sys
from pathlib import Path

# Need to import build_playbook2_data
sys.path.append(str(Path(__file__).parent / "Outreach"))
from build_playbook2_data import DEALS

ts_content = "export const deals = " + json.dumps(DEALS, indent=2) + ";\n"
Path(__file__).parent.joinpath("LandDashboard", "src", "data.ts").write_text(ts_content)
print("✅ Extracted DEALS to src/data.ts")
