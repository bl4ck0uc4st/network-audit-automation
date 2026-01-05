#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

from src.na_toolkit.audit import run_offline_audit, render_report

REPO_ROOT = Path(__file__).resolve().parent

def cmd_offline_audit(args: argparse.Namespace) -> None:
    report = run_offline_audit(REPO_ROOT, device=args.device, all_devices=args.all)
    out_json = REPO_ROOT / "reports" / "report.json"
    out_json.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"[OK] Wrote {out_json}")

def cmd_render_report(args: argparse.Namespace) -> None:
    # render from existing JSON if present; otherwise run audit first
    report_json = REPO_ROOT / "reports" / "report.json"
    if report_json.exists():
        report = json.loads(report_json.read_text(encoding="utf-8"))
    else:
        report = run_offline_audit(REPO_ROOT, device=args.device, all_devices=args.all)
        report_json.write_text(json.dumps(report, indent=2), encoding="utf-8")
    md = render_report(report)
    out_md = REPO_ROOT / "reports" / "report.md"
    out_md.write_text(md, encoding="utf-8")
    print(f"[OK] Wrote {out_md}")

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="na-portfolio",
        description="Offline-first network automation portfolio toolkit (audit + reporting)."
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("offline-audit", help="Run audits using sample_outputs (no devices needed).")
    a.add_argument("--device", help="Device name (e.g., R1). If omitted, use --all.", default=None)
    a.add_argument("--all", action="store_true", help="Audit all devices found in sample_outputs/")
    a.set_defaults(func=cmd_offline_audit)

    r = sub.add_parser("render-report", help="Generate reports/report.md from reports/report.json (or run audit).")
    r.add_argument("--device", help="Device name (e.g., R1). If omitted, use --all.", default=None)
    r.add_argument("--all", action="store_true", help="Report for all devices found in sample_outputs/")
    r.set_defaults(func=cmd_render_report)

    return p

def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if args.cmd in ("offline-audit", "render-report"):
        if not args.all and not args.device:
            parser.error("Provide --device <NAME> or --all")
    args.func(args)

if __name__ == "__main__":
    main()
