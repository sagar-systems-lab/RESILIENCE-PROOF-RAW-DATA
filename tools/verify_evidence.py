#!/usr/bin/env python3
"""Verify archived, released records. Does not execute TREX or attest historical execution."""
from pathlib import Path
import csv
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "evidence" / "2026-08-24-quick"
errors = []


def check(condition, message):
    if not condition:
        errors.append(message)


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def git_blob_id(contents):
    return hashlib.sha1(b"blob " + str(len(contents)).encode("ascii") + b"\0" + contents).hexdigest()


campaign = read_json(BASE / "campaign.json")
provenance = read_json(BASE / "provenance.json")
check(campaign["challenges"]["mandatory"] == 241, "mandatory challenges")
check(campaign["challenges"]["mandatory_recorded_pass"] == 241, "mandatory PASS")
check(campaign["challenges"]["not_run"] == 7, "catalog NOT_RUN")

for path, expected_blob in provenance["original_raw_json_git_blob_shas"].items():
    payload = (ROOT / path).read_bytes()
    result = json.loads(payload)
    check(git_blob_id(payload) == expected_blob, "original blob fingerprint: " + path)
    check(result["verdict"] == "PASS", "original recorded verdict: " + path)
    check(result["violations"] == 0, "original recorded violations: " + path)
    check(result["duplicate_economic_actions"] == 0, "duplicate economic actions: " + path)
    if result["challenge_id"] in ("ch.v1.0074", "ch.v1.0075"):
        check(result["executed"] == 833, "order-state iterations: " + path)
    elif result["challenge_id"] == "ch.v1.0102":
        check(result["executed"] == 10000, "ambiguous iterations")
        check(result["rejected"] == 10000, "blind retries rejected")

journal = read_json(BASE / "sanitized" / "journal_sigkill_50.json")
js = journal["schedules"]
check(len(js) == 50 and len({x["schedule"] for x in js}) == 50, "journal schedule IDs")
check(len({x["run_seed"] for x in js}) == 50, "journal distinct seeds")
for x in js:
    proc, verifier = x["process"], x["journal_check"]
    check(x["recorded_pass"] and proc["terminated_by_sigkill"] and
          proc["signal"] == 9 and proc["exit_code"] == -9,
          "journal process exit " + str(x["schedule"]))
    check(verifier["expected"] == "TORN_RECORD" and
          verifier["reported"] == "TORN_RECORD" and
          verifier["verifier_exit_code"] == 0 and
          verifier["verifier_verdict"] == "PASS",
          "journal verification " + str(x["schedule"]))

comp = read_json(BASE / "sanitized" / "composite_overlap_84.json")
cs = comp["schedules"]
check(len(cs) == 84 and len({x["schedule"] for x in cs}) == 84, "composite schedule IDs")
check(len({x["run_seed"] for x in cs}) == 84, "composite distinct seeds")
expected_task_names = {
    "engine_api_probe", "local_tcp", "resource_pressure", "process_sigkill"
}
for row in cs:
    windows = row["task_windows"]
    check(set(windows) == expected_task_names, "task names " + str(row["schedule"]))
    starts = [w["start_ms"] for w in windows.values()]
    ends = [w["end_ms"] for w in windows.values()]
    overlap = len(starts) == 4 and max(starts) < min(ends)
    check(overlap and row["concurrent_four_way_window_observed"],
          "four-way overlap " + str(row["schedule"]))
    check(all(w["recorded_pass"] and w["end_ms"] > w["start_ms"]
              for w in windows.values()), "probe results " + str(row["schedule"]))
    check(row["recorded_pass"] and row["os_process_exit_code"] == -9 and
          row["local_tcp_connection_observed"] and row["api_probe_violations"] == 0,
          "composite safety fields " + str(row["schedule"]))

ack = read_json(BASE / "sanitized" / "ack_loss_loopback.json")
check(ack["recorded_verdict"] == "PASS" and ack["recorded_cycles"] == 10
      and ack["recorded_local_tcp_connections"] == 10, "local ACK loss")
with (BASE / "challenge_summary.csv").open(newline="", encoding="utf-8") as f:
    check(len(list(csv.DictReader(f))) == 6, "CSV index")

if errors:
    print("FAIL:", "; ".join(errors))
    sys.exit(1)
print("PASS — released original hashes and recorded trace consistency checks")
print("LIMITATION — not an independent engine run or test execution attestation")
