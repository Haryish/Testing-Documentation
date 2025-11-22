# Python Selenium + Pytest Starter (POM, screenshots on pass/fail, HTML report)

## Quick Start
```bash
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
pip install -r requirements.txt
pytest -m smoke --browser=chrome --headless
# Or full:
pytest -m "smoke or regression" --browser=chrome --headless -n auto
```

Reports: `reports/report.html` with embedded screenshots for every test.

## Project Layout
```
pages/          # Page Objects
core/           # Base classes
tests/          # Test cases
resources/      # Config (environments)
utils/          # (placeholder for future helpers)
conftest.py     # Fixtures, driver, screenshots, config, hooks
pytest.ini      # Markers & default options
Jenkinsfile     # CI pipeline
```

## Markers
- `@pytest.mark.smoke` → quick health checks
- `@pytest.mark.regression` → broader coverage

## Notes
- Uses Selenium Manager (no manual drivers).
- Screenshots are captured for both pass and fail and attached to pytest-html.
- Switch environment: `--env=qa` (reads from `resources/config.yaml`).
- Parallel: `-n auto` (requires `pytest-xdist`).
