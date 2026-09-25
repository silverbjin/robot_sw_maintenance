#!/usr/bin/env python3
"""Collect installation-environment evidence using only Python stdlib."""
from __future__ import annotations

import argparse
import json
import os
import platform
import re
import shutil
import socket
import subprocess
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def run(cmd: list[str], timeout: int = 8) -> dict[str, Any]:
    try:
        cp = subprocess.run(cmd, text=True, capture_output=True, timeout=timeout, check=False)
        return {
            "command": " ".join(cmd),
            "returncode": cp.returncode,
            "stdout": cp.stdout.strip(),
            "stderr": cp.stderr.strip(),
        }
    except FileNotFoundError:
        return {"command": " ".join(cmd), "returncode": 127, "stdout": "", "stderr": "command not found"}
    except subprocess.TimeoutExpired:
        return {"command": " ".join(cmd), "returncode": 124, "stdout": "", "stderr": "timeout"}


def read_text(path: str) -> str:
    try:
        return Path(path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def os_release() -> dict[str, str]:
    out: dict[str, str] = {}
    for line in read_text("/etc/os-release").splitlines():
        if "=" not in line:
            continue
        k, v = line.split("=", 1)
        out[k] = v.strip().strip('"')
    return out


def mem_available_bytes() -> int:
    for line in read_text("/proc/meminfo").splitlines():
        if line.startswith("MemAvailable:"):
            parts = line.split()
            if len(parts) >= 2 and parts[1].isdigit():
                return int(parts[1]) * 1024
    return 0


def tcp_self_test() -> dict[str, Any]:
    ready = threading.Event()
    result: dict[str, Any] = {"passed": False, "port": None, "message": ""}

    def server():
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(("127.0.0.1", 0))
                s.listen(1)
                s.settimeout(4)
                result["port"] = s.getsockname()[1]
                ready.set()
                conn, _ = s.accept()
                with conn:
                    data = conn.recv(64)
                    if data == b"LAB02_PING":
                        conn.sendall(b"LAB02_PONG")
        except Exception as exc:  # evidence collection must not crash
            result["message"] = repr(exc)
            ready.set()

    t = threading.Thread(target=server, daemon=True)
    t.start()
    ready.wait(2)
    port = result.get("port")
    if not port:
        return result
    try:
        with socket.create_connection(("127.0.0.1", int(port)), timeout=3) as c:
            c.sendall(b"LAB02_PING")
            result["passed"] = c.recv(64) == b"LAB02_PONG"
            result["message"] = "loopback TCP request/response succeeded" if result["passed"] else "unexpected response"
    except Exception as exc:
        result["message"] = repr(exc)
    t.join(timeout=1)
    return result


def gb(n: int) -> float:
    return round(n / (1024 ** 3), 2)


def build(args: argparse.Namespace) -> dict[str, Any]:
    now = datetime.now(timezone.utc)
    osr = os_release()
    kernel = platform.release()
    procver = read_text("/proc/version")
    is_wsl = "microsoft" in kernel.lower() or "microsoft" in procver.lower()
    disk = shutil.disk_usage("/")
    disk_use_pct = round((disk.used / disk.total) * 100, 1) if disk.total else 100.0
    mem_avail = mem_available_bytes()
    ping = run(["ping", "-c", "4", "127.0.0.1"], timeout=8)
    tcp = tcp_self_test()
    ip_brief = run(["ip", "-brief", "addr"], timeout=5)
    ip_route = run(["ip", "route"], timeout=5)

    if args.expected_release:
        expected_release = args.expected_release
    else:
        expected_release = "22.04" if args.profile == "developer" else "20.04"
    if args.expected_arch:
        expected_arch = args.expected_arch
    else:
        expected_arch = "x86_64" if args.profile == "developer" else "aarch64"
    min_mem_gb = args.min_mem_gb if args.min_mem_gb is not None else (1.0 if args.profile == "developer" else 0.5)

    checks = {
        "ubuntu_release": {
            "passed": osr.get("VERSION_ID", "") == expected_release,
            "actual": osr.get("VERSION_ID", "unknown"),
            "expected": expected_release,
        },
        "architecture": {
            "passed": platform.machine() == expected_arch,
            "actual": platform.machine(),
            "expected": expected_arch,
        },
        "memory_available": {
            "passed": gb(mem_avail) >= min_mem_gb,
            "actual_gib": gb(mem_avail),
            "minimum_gib": min_mem_gb,
        },
        "root_storage": {
            "passed": disk_use_pct < args.max_disk_use_pct,
            "actual_use_pct": disk_use_pct,
            "maximum_use_pct_exclusive": args.max_disk_use_pct,
        },
        "loopback_ping": {
            "passed": ping["returncode"] == 0,
            "returncode": ping["returncode"],
        },
        "loopback_tcp": tcp,
    }
    failed = [name for name, c in checks.items() if not bool(c.get("passed"))]

    ros = {"available": shutil.which("ros2") is not None, "ros_distro": os.environ.get("ROS_DISTRO", "")}
    if ros["available"]:
        ros["topic_list"] = run(["ros2", "topic", "list"], timeout=8)

    return {
        "schema_version": "1.0",
        "record_type": "installation_environment_evidence",
        "captured_at_utc": now.isoformat(),
        "profile": args.profile,
        "course_target": {
            "expected_release": expected_release,
            "expected_arch": expected_arch,
            "min_mem_gib": min_mem_gb,
            "max_disk_use_pct_exclusive": args.max_disk_use_pct,
            "note": "교육용 판정 기준이며 실제 제품 요구사항이 아님",
        },
        "system": {
            "hostname": socket.gethostname(),
            "os_release": osr,
            "architecture": platform.machine(),
            "kernel": kernel,
            "is_wsl": is_wsl,
            "python": platform.python_version(),
            "memory_available_gib": gb(mem_avail),
            "root_disk": {
                "total_gib": gb(disk.total),
                "used_gib": gb(disk.used),
                "free_gib": gb(disk.free),
                "use_pct": disk_use_pct,
            },
        },
        "commands": {
            "lsb_release": run(["lsb_release", "-a"]),
            "uname": run(["uname", "-a"]),
            "free": run(["free", "-h"]),
            "df_root": run(["df", "-h", "/"]),
            "ip_brief": ip_brief,
            "ip_route": ip_route,
            "ping_loopback": ping,
        },
        "network": {"tcp_self_test": tcp},
        "ros2": ros,
        "checks": checks,
        "decision": "READY" if not failed else "NOT_READY",
        "failed_checks": failed,
    }


def markdown(data: dict[str, Any]) -> str:
    s = data["system"]
    lines = [
        "# Installation Environment Evidence",
        "",
        f"- Captured: `{data['captured_at_utc']}`",
        f"- Profile: `{data['profile']}`",
        f"- Decision: **{data['decision']}**",
        "",
        "## Summary",
        "",
        "| Item | Result |",
        "|---|---|",
        f"| Ubuntu | {s['os_release'].get('PRETTY_NAME', 'unknown')} |",
        f"| Architecture | {s['architecture']} |",
        f"| Kernel | {s['kernel']} |",
        f"| WSL detected | {s['is_wsl']} |",
        f"| Available memory | {s['memory_available_gib']} GiB |",
        f"| Root storage use | {s['root_disk']['use_pct']}% |",
        "",
        "## Checks",
        "",
        "| Check | Passed | Details |",
        "|---|---|---|",
    ]
    for name, c in data["checks"].items():
        details = ", ".join(f"{k}={v}" for k, v in c.items() if k != "passed")
        lines.append(f"| {name} | {'PASS' if c.get('passed') else 'FAIL'} | {details} |")
    lines += ["", "## Failed checks", "", ", ".join(data["failed_checks"]) if data["failed_checks"] else "None", ""]
    return "\n".join(lines)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--profile", choices=["developer", "robot"], default="developer")
    p.add_argument("--output-dir", default="results")
    p.add_argument("--expected-release")
    p.add_argument("--expected-arch")
    p.add_argument("--min-mem-gb", type=float)
    p.add_argument("--max-disk-use-pct", type=float, default=90.0)
    args = p.parse_args()

    data = build(args)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = Path(args.output_dir) / stamp
    out.mkdir(parents=True, exist_ok=True)
    (out / "evidence.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    (out / "evidence.md").write_text(markdown(data), encoding="utf-8")
    print(f"[RESULT] {data['decision']}")
    print(f"[PATH] {out}")
    if data["failed_checks"]:
        print("[FAILED] " + ", ".join(data["failed_checks"]))
    return 0 if data["decision"] == "READY" else 10


if __name__ == "__main__":
    raise SystemExit(main())
