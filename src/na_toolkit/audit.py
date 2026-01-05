from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any, List, Optional

from .parsers.cisco_ios import parse_clock, parse_features, parse_version, parse_insecure

@dataclass
class Finding:
    id: str
    title: str
    severity: str  # LOW/MED/HIGH
    status: str    # PASS/FAIL/WARN
    evidence: str
    recommendation: str

def _load_text(p: Path) -> str:
    return p.read_text(encoding="utf-8") if p.exists() else ""

def audit_device(repo_root: Path, device: str) -> Dict[str, Any]:
    dev_dir = repo_root / "sample_outputs" / device
    version = parse_version(_load_text(dev_dir / "show_version.txt"))
    clock = parse_clock(_load_text(dev_dir / "show_clock.txt"))
    features = parse_features(_load_text(dev_dir / "show_run_features.txt"))
    insecure = parse_insecure(_load_text(dev_dir / "show_run_insecure.txt"))

    findings: List[Finding] = []

    # SSH check
    if features.get("ssh_enabled"):
        findings.append(Finding(
            id="SEC-SSH-001",
            title="SSH enabled for remote management",
            severity="LOW",
            status="PASS",
            evidence="Found 'ip ssh version 2' and VTY transport input ssh.",
            recommendation="Keep SSH enabled and restrict access to trusted management subnets."
        ))
    else:
        findings.append(Finding(
            id="SEC-SSH-001",
            title="SSH not properly configured",
            severity="HIGH",
            status="FAIL",
            evidence="Missing 'ip ssh version 2' or VTY lines do not enforce SSH.",
            recommendation="Enable SSHv2, set domain-name, generate RSA keys, and enforce 'transport input ssh'."
        ))

    # NTP check
    if features.get("ntp_configured"):
        findings.append(Finding(
            id="OPS-NTP-001",
            title="NTP configured",
            severity="LOW",
            status="PASS",
            evidence="Found NTP server configuration in sample outputs.",
            recommendation="Use at least two NTP sources; consider authenticated NTP in production."
        ))
    else:
        findings.append(Finding(
            id="OPS-NTP-001",
            title="NTP not configured",
            severity="MED",
            status="WARN",
            evidence="No 'ntp server' line found.",
            recommendation="Configure NTP to keep logs, certificates, and correlation accurate."
        ))

    # Logging timestamps
    if features.get("timestamps"):
        findings.append(Finding(
            id="OPS-LOG-001",
            title="Logging timestamps enabled",
            severity="LOW",
            status="PASS",
            evidence="Found 'service timestamps ...' in configuration.",
            recommendation="Keep timestamps enabled for incident response and audit trails."
        ))
    else:
        findings.append(Finding(
            id="OPS-LOG-001",
            title="Logging timestamps missing",
            severity="MED",
            status="WARN",
            evidence="Missing 'service timestamps log datetime msec' and/or debug timestamps.",
            recommendation="Enable service timestamps for consistent troubleshooting and audits."
        ))

    # Insecure management
    if insecure.get("telnet_enabled"):
        findings.append(Finding(
            id="SEC-MGMT-002",
            title="Telnet enabled on management lines",
            severity="HIGH",
            status="FAIL",
            evidence="Found VTY lines allowing telnet in sample outputs.",
            recommendation="Disable telnet; enforce SSH only; restrict VTY access via ACL."
        ))
    else:
        findings.append(Finding(
            id="SEC-MGMT-002",
            title="No telnet exposure detected",
            severity="LOW",
            status="PASS",
            evidence="No telnet transport input found in sample outputs.",
            recommendation="Continue enforcing SSH-only access."
        ))

    return {
        "device": device,
        "platform": "cisco_ios (offline sample)",
        "facts": {
            "ios_version": version.get("ios_version"),
            "clock": clock.get("clock"),
        },
        "findings": [f.__dict__ for f in findings],
    }

def run_offline_audit(repo_root: Path, device: Optional[str], all_devices: bool) -> Dict[str, Any]:
    if all_devices:
        devices = sorted([p.name for p in (repo_root / "sample_outputs").iterdir() if p.is_dir()])
    else:
        devices = [device] if device else []

    results = [audit_device(repo_root, d) for d in devices]
    summary = {
        "PASS": sum(1 for r in results for f in r["findings"] if f["status"] == "PASS"),
        "WARN": sum(1 for r in results for f in r["findings"] if f["status"] == "WARN"),
        "FAIL": sum(1 for r in results for f in r["findings"] if f["status"] == "FAIL"),
    }
    return {
        "generated_by": "na-portfolio offline-audit",
        "devices": results,
        "summary": summary,
    }

def render_report(report: Dict[str, Any]) -> str:
    lines: List[str] = []
    lines.append("# Network Audit Report (Offline Demo)\n")
    lines.append(f"**Summary:** PASS={report['summary']['PASS']} | WARN={report['summary']['WARN']} | FAIL={report['summary']['FAIL']}\n")

    for dev in report["devices"]:
        lines.append(f"## {dev['device']}\n")
        facts = dev.get("facts", {})
        if facts:
            lines.append(f"- IOS Version: `{facts.get('ios_version') or 'unknown'}`")
            lines.append(f"- Clock: `{facts.get('clock') or 'unknown'}`\n")

        lines.append("| ID | Title | Severity | Status |")
        lines.append("|---|---|---|---|")
        for f in dev["findings"]:
            lines.append(f"| {f['id']} | {f['title']} | {f['severity']} | **{f['status']}** |")
        lines.append("\n### Details\n")
        for f in dev["findings"]:
            lines.append(f"**{f['id']} – {f['title']}**")
            lines.append(f"- Severity: {f['severity']}")
            lines.append(f"- Status: {f['status']}")
            lines.append(f"- Evidence: {f['evidence']}")
            lines.append(f"- Recommendation: {f['recommendation']}\n")
    return "\n".join(lines)
