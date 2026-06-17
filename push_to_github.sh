#!/bin/bash
# Run in Git Bash from inside P1_German_Auto_DeepDive/
# Pre-req: create repo "german-auto-analysis" on github.com (empty, no README)

set -e
git init
git branch -M main
git config user.name "Shardul Pundir"
git config user.email "shardul.pundir21@gmail.com"

cat > .gitignore << 'IGNORE'
__pycache__/
*.py[cod]
.env
venv/
charts/*.png
.ipynb_checkpoints/
.DS_Store
Thumbs.db
IGNORE

git add .
git commit -m "feat: P1 German Auto Industry Analysis

Four-module Python project analysing the German automotive sector.
- Valuation comps: EV/EBITDA vs P/E for BMW, Mercedes, VW, Porsche, Tesla
- EBIT margin trends FY2021-2025
- EV transition scorecard vs EU 2035 mandate
- China exposure: revenue % and unit volume decline

Part of BMW Equity Research chain: P1 Industry -> P2 Business -> P3 3-Statement -> P4 DCF -> P5 Report
Data vintage check built in. Live yfinance + hand-curated CSVs."

git remote add origin https://github.com/SharDXL/german-auto-analysis.git
git push -u origin main
echo "Done: https://github.com/SharDXL/german-auto-analysis"
