# Network Automation Portfolio (Offline-First)

A small, interview-friendly **network automation toolkit** that focuses on:
- **Standardized config templates**
- **Inventory-driven workflows**
- **Audit checks** (SSH, NTP, logging, insecure services)
- **Evidence + reporting**
- **Offline demo mode** (works without devices, labs, or extra installs)

> ✅ Runs with **Python 3 only** (no external libraries required).

## What you can demonstrate (without a lab)
- How you structure automation projects (inventory, templates, evidence, reports)
- How you validate configurations and produce audit-ready reports
- How you document security posture and recommended fixes

## Quick start (offline demo)
```bash
python3 tool.py offline-audit --device R1
python3 tool.py offline-audit --all
python3 tool.py render-report --all
```

Outputs:
- `reports/report.md`
- `reports/report.json`

## Repository layout
- `tool.py` – CLI entry point (offline-first)
- `src/na_toolkit/` – parsers + audit checks
- `inventory_examples/` – sample inventories
- `configs/baseline/` – reusable config templates
- `sample_outputs/` – saved device outputs used for offline demo
- `reports/` – generated evidence + reports
- `.github/` – issue templates + basic CI

## Portfolio notes (what to claim in interviews)
- Built an inventory-driven audit/reporting flow (offline-first for portability)
- Implemented config compliance checks (SSH/NTP/logging/insecure services)
- Produced evidence artifacts (markdown + json) for traceability

## License
MIT — see `LICENSE`.
