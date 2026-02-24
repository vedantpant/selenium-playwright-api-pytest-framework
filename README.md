# Selenium + Playwright + API Test Framework (Pytest)

## Tech
- Pytest
- Selenium (UI)
- Playwright (UI)
- Requests (API)
- Pytest HTML report
- Logging

## Setup
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
playwright install

## Run
# all
pytest -v

# ui only
pytest -m ui -v

# api only
pytest -m api -v

# parallel
pytest -n 2 -v

# html report
pytest --html=reports/report.html --self-contained-html