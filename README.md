# 🏔️ Institutional Land Wholesaling Operations

This repository contains the complete operational pipeline for sourcing, scoring, contacting, and assigning off-market commercial, industrial, and residential land deals in Gwinnett County and Metro Atlanta.

## 📂 Repository Structure

Everything is centralized here to keep the business highly organized:

*   **`/LandDashboard`**: The interactive React (Vite/Tailwind) application that acts as your central CRM and Pipeline Viewer. Contains all 42 tracked leads, buyer matches, and assignment math.
*   **`/Outreach`**: The core Python automation scripts for generating seller scripts, buyer pitches, and consolidating math. 
    *   `build_playbook2.py` / `build_playbook2_data.py`: Creates the text-based deal playbooks.
    *   `export_vacant_to_dashboard.py`: Extracts and standardizes leads for the dashboard.
    *   `generate_seller_summary_html.py`: Creates the beautiful, printable HTML summary table.
*   **`/Exports`**: The output folder where your CSV leads, printable HTML playbooks, and formatted contact lists are saved. (e.g., `seller_contact_and_deal_math.html`).
*   **`/Contracts`**: Tools and templates for generating Purchase and Sale Agreements (PSAs) and Assignment Contracts.
*   **`/Data`**: Raw county GIS data, shapefiles, or tax assessor records used for scoring parcels.
*   **`/GORA_Requests`**: Open records requests and compliance documents.

## 🚀 Quick Start (Dashboard)

To run the interactive Land Pipeline Dashboard:

1. Open your terminal and navigate to the dashboard directory:
   ```bash
   cd LandDashboard
   ```
2. Start the development server:
   ```bash
   npm run dev
   ```
3. Open `http://localhost:5173` in your browser.

## 🧮 Standard Deal Math Model

The entire pipeline is built on a high-conversion institutional formula:
*   **Target Buy Price:** 55% of Estimated Off-Market Value (FMV)
*   **Assignment Fee:** 15% of FMV
*   **Buyer Pitch Price:** 70% of FMV (Gives the institutional buyer a 30% discount to market)

## 📞 Next Steps
Use the generated HTML playbooks in the `Exports/` folder alongside the `LandDashboard` to execute outbound calls to the Corporate Decision Makers.
