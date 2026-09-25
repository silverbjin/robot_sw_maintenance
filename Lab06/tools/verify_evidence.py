#!/usr/bin/env python3
import json
import sys
from pathlib import Path

if len(sys.argv) != 2:
    print("Usage: verify_evidence.py <evidence_dir>")
    raise SystemExit(2)

root = Path(sys.argv[1])
facts_file = root / "facts.json"

if not facts_file.exists():
    print("FAIL: facts.json missing")
    raise SystemExit(1)

facts = json.loads(facts_file.read_text(encoding="utf-8"))
stage = facts.get("stage")

fail = []
warn = []

if not facts.get("working_tree_clean"):
    fail.append("Working tree was not clean.")

if stage == "baseline":
    if facts.get("monitor_source_present"):
        fail.append("Baseline must not contain myagv_monitor source.")
    if facts.get("branch") not in ("main", ""):
        warn.append(f"Expected main or detached baseline; got branch={facts.get('branch')!r}.")

elif stage == "upgrade":
    if facts.get("branch") != "release-v2":
        fail.append(f"Upgrade evidence must be on release-v2; got {facts.get('branch')!r}.")
    if not facts.get("monitor_source_present"):
        fail.append("release-v2 must contain myagv_monitor source.")
    if facts.get("install_available") and not facts.get("installed_myagv_monitor"):
        fail.append("install exists but myagv_monitor is not discoverable.")

elif stage == "rollback":
    if facts.get("head_tag") != "pre-upgrade-v1":
        fail.append(
            f"Rollback HEAD must match pre-upgrade-v1; got {facts.get('head_tag')!r}."
        )
    if facts.get("monitor_source_present"):
        fail.append("Rollback source still contains myagv_monitor.")
    if facts.get("install_available") and facts.get("installed_myagv_monitor"):
        fail.append("Rollback install still exposes myagv_monitor; clean rebuild is incomplete.")

else:
    fail.append(f"Unknown stage: {stage!r}")

for m in warn:
    print("WARN:", m)
for m in fail:
    print("FAIL:", m)

if fail:
    raise SystemExit(1)

print(f"PASS: {stage} evidence is structurally consistent.")
