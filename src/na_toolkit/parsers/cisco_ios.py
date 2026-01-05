from __future__ import annotations
import re
from typing import Dict, Any

def parse_version(text: str) -> Dict[str, Any]:
    # Example: Version 15.9(3)M2
    m = re.search(r"Version\s+([0-9][^,\s]+)", text)
    return {"ios_version": m.group(1) if m else None}

def parse_clock(text: str) -> Dict[str, Any]:
    # Example: *12:01:05.123 UTC Mon Jan 5 2026
    line = text.strip().lstrip("*").strip()
    return {"clock": line or None}

def parse_features(run_snippet: str) -> Dict[str, Any]:
    ssh = bool(re.search(r"^ip\s+ssh\s+version\s+2\b", run_snippet, re.M))
    vty_ssh = bool(re.search(r"^\s*transport\s+input\s+ssh\b", run_snippet, re.M))
    ntp = bool(re.search(r"^ntp\s+server\b", run_snippet, re.M))
    ts = bool(re.search(r"^service\s+timestamps\s+log\s+datetime", run_snippet, re.M))
    return {
        "ssh_enabled": ssh and vty_ssh,
        "ntp_configured": ntp,
        "timestamps": ts,
    }

def parse_insecure(run_snippet: str) -> Dict[str, Any]:
    telnet = bool(re.search(r"^\s*transport\s+input\s+.*telnet", run_snippet, re.M))
    return {"telnet_enabled": telnet}
