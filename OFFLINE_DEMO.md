# Offline Demo Mode

Offline demo mode lets you demonstrate network automation concepts without:
- lab routers/switches
- GNS3/EVE-NG
- installing extra Python libraries

## How it works
- The repo includes `sample_outputs/<device>/...` files that represent typical device command outputs.
- The CLI reads these files and runs compliance/audit checks.
- Results are generated in `reports/`.

## Commands
```bash
python3 tool.py offline-audit --device R1
python3 tool.py offline-audit --all
python3 tool.py render-report --all
```

## What to say in an interview
- “I can run audits and produce evidence even when I don't have live access—useful for repeatable demos and testing.”
- “The same checks can be reused for live devices later by swapping the data source.”
