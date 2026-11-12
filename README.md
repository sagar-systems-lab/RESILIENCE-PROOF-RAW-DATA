# TREX Execution Resilience — Test Evidence

**Machine-readable records from an archived controlled stress campaign (24 August 2026).**

The repository provides selected **original Rust test outputs**, event-level **process termination / journal verification records**, and **timestamped parallel stress observations**. These are archived internal test records, not generated performance claims or an independent third-party certification.

## Campaign overview

| Recorded test workload | Result |
|---|---:|
| Mandatory challenge verdicts | **241 / 241 PASS** |
| Race schedules (controlled state/event orderings) | **10,000** |
| OS SIGKILL events | **4,714** |
| Local TCP loopback connections | **3,608** |
| Composite stress schedules | **1,000** |
| Session reconnects | **100** |
| Additional catalog challenges not run | **7** |

Source: [campaign.json](evidence/2026-08-24-quick/campaign.json). Values are campaign-level counts; the public records below are a selected subset.

## Three technical cases worth inspecting

| Failure condition | Public evidence | Recorded outcome |
|---|---|---|
| **Partial fill arrives during cancel/replace** | [Cancel result](evidence/2026-08-24-quick/raw_original/ch.v1.0074.json) · [Replace result](evidence/2026-08-24-quick/raw_original/ch.v1.0075.json) | 833 isolated iterations **per case**, 0 recorded correctness violations |
| **Order submission becomes ambiguous** | [Original blind-retry guard result](evidence/2026-08-24-quick/raw_original/ch.v1.0102.json) | 10,000 guard iterations, 10,000 recorded rejections, 0 recorded violations |
| **Process is killed while a journal is present** | [50 recorded SIGKILL + torn-journal verifier checks](evidence/2026-08-24-quick/sanitized/journal_sigkill_50.json) | Exit code -9 and expected torn-record verdict across 50 recorded schedules |

Additional records: [84 concurrent four-probe timing schedules](evidence/2026-08-24-quick/sanitized/composite_overlap_84.json), [10 local ACK-loss test cycles](evidence/2026-08-24-quick/sanitized/ack_loss_loopback.json), [CSV index](evidence/2026-08-24-quick/challenge_summary.csv), [source fingerprints](evidence/2026-08-24-quick/provenance.json).

**Important:** The 84 concurrent schedules are **not** presented as end-to-end journal corruption plus exchange reconciliation tests. See [Methodology and boundaries](docs/METHODOLOGY.md).

## Inspect and validate

```bash
python3 tools/verify_evidence.py
```

The standard-library-only verifier checks the unchanged original Git blob IDs, counters, recorded process exit codes, journal verdicts and all 84 four-way overlap windows. It validates the **internal consistency of supplied artifacts**, not independent execution of proprietary engine code.

**Release boundary:** no trading strategy, order payload, engine source/binaries, account credentials, internal command paths, or low-level resource tuning is included.

*Your Strategy. Your Infrastructure. Our Execution Engine.*
