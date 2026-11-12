# TREX Execution Resilience — Test Evidence

**Can a trading execution system preserve correct order handling when things go wrong?**

Trading infrastructure faces more than speed challenges. A fill can arrive while an order is being cancelled; an order acknowledgment can disappear after submission; a process can stop while recovering persistent state. Mishandling these events can create duplicate actions, uncertainty about order state, or difficult recovery.

**TREX** is client-deployed crypto execution infrastructure. This repository shows **selected machine-readable records from its controlled, offline resilience tests** (archived campaign: **24 August 2026**). It focuses on observed test outcomes—not strategy performance or marketing benchmarks.

## What the tests showed

| Operational risk | Why it matters | Recorded evidence |
|---|---|---|
| **Partial fill during cancel or replace** | An order can be partially executed while a change is being processed; incorrect state handling can cause inconsistent actions. | Two isolated order-event tests, **833 iterations each**, **0 recorded correctness violations**. [Cancel JSON](evidence/2026-08-24-quick/raw_original/ch.v1.0074.json) · [Replace JSON](evidence/2026-08-24-quick/raw_original/ch.v1.0075.json) |
| **Lost acknowledgment / ambiguous order** | Retrying an order without knowing whether the first submission took effect can create a duplicate instruction. | Blind-retry guard test: **10,000 iterations**, **10,000 recorded rejections**, **0 recorded violations**. [Original JSON](evidence/2026-08-24-quick/raw_original/ch.v1.0102.json) |
| **Unexpected process termination and damaged journal** | Unexpected shutdowns and incomplete journal records must be detected rather than silently accepted. | **50 recorded OS SIGKILL events** with corresponding **PASS** results from a torn-journal verifier. [Sanitized schedule records](evidence/2026-08-24-quick/sanitized/journal_sigkill_50.json) |

**Reading these results:** They support specific checks of *order-state correctness, ambiguous-order safeguards, and journal fault detection*. They **do not** by themselves prove complete production recovery or live exchange reconciliation.

## Wider stress campaign — recorded totals

| Archived controlled workload | Recorded |
|---|---:|
| Mandatory challenge results | **241 / 241 PASS** |
| State/event ordering (“race”) schedules | **10,000** |
| OS process SIGKILL events | **4,714** |
| Local TCP loopback connections | **3,608** |
| Composite stress schedules | **1,000** |
| Session reconnects | **100** |
| Other catalog challenges **NOT_RUN** | **7** |

These are **campaign-level internal results**. This public release contains a selected evidence subset, not all 241 underlying challenge files. The race counts describe controlled event orderings, not thousands of live exchange trades.

[Campaign data (evidence/2026-08-24-quick/campaign.json)](evidence/2026-08-24-quick/campaign.json) · [CSV challenge index](evidence/2026-08-24-quick/challenge_summary.csv)

## For technical review

Unlike a one-line PASS certificate, this repository includes:

- **Three unchanged original Rust result JSONs** with case IDs, iteration counts, correctness counters and file fingerprints.
- **50 sanitized process-termination/journal-verification schedules** containing recorded exits and verification outcomes.
- **84 sanitized concurrent stress schedules** with inspectable four-task timing windows and process-kill observations. These show bounded parallel probes, **not** a full end-to-end reconciliation test.
- **10 local ACK-loss session cycles** as additional supporting evidence.

[84 concurrent schedules](evidence/2026-08-24-quick/sanitized/composite_overlap_84.json) · [ACK-loss record](evidence/2026-08-24-quick/sanitized/ack_loss_loopback.json) · [Source fingerprints](evidence/2026-08-24-quick/provenance.json) · [Methodology & limitations](docs/METHODOLOGY.md)

To check the shared files and recorded invariants (Python 3, standard library only):

```bash
python3 tools/verify_evidence.py
```

**Evidence boundary:** These are archived internal observations, **not an independent audit, live-exchange test, or full customer-production qualification**. The checker confirms the published files' integrity and internal consistency; it does not rerun the engine or authenticate the historical execution. Independent qualification would require a separately controlled evaluation.

**Confidentiality:** No engine source or binaries, trading strategies, customer orders, credentials, private command paths, or detailed optimization parameters are released.

*Your Strategy. Your Infrastructure. Our Execution Engine.*
