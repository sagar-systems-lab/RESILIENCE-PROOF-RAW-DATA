# Evidence methodology and verification boundaries

**Campaign:** archived 2026-08-24 QUICK controlled/offline test run.  
**Status:** internal archived test records; not third-party attested.

## What the released files demonstrate

- `raw_original/*.json` contains **three unchanged source output files**. Their byte-identical Git blob identifiers are listed in `provenance.json`. Each output contains its own challenge ID, tested iteration counts, recorded verdict, correctness counters and evidence digests.
- The partial-fill/cancel and partial-fill/replace cases are **isolated deterministic event-state tests**, 833 iterations per case. They are **not** 833 live exchange races.
- The ambiguous NEW case is a bounded **blind-retry denial guard** with 10,000 recorded iterations and 10,000 recorded rejections.
- The 50 journal entries are **selected-field excerpts** from individual OS-process termination and deliberately torn-record verification schedules. A recorded `SIGKILL` exit code of `-9` and verifier `PASS / TORN_RECORD` represent the narrow checked outcomes; they do **not** establish full trading-state recovery after a restart.
- The 84 composite records preserve **relative task start/end windows in milliseconds** (rounded to 0.001 ms). Four task classes are represented: engine API probe, local TCP, resource pressure and journal-child process termination. All four intervals overlap in each released schedule as computed from the archived timestamps. This **does not** mean the program performed integrated end-to-end exchange reconciliation.
- ACK-loss supporting evidence concerns **local TCP loopback** tests, not an external exchange.

## Campaign coverage and limitations

The recorded campaign-level totals are 241 mandatory challenges passed, 7 additional catalog challenges not run, 10,000 state-ordering schedules, 4,714 OS SIGKILL events, 3,608 local loopback connections, 1,000 composite schedules, and 100 reconnects. The released evidence is **selected**, not every original case or raw OS log.

The campaign is not equivalent to extended 7–14 day qualification, production deployment results, service-level guarantees, or an independent audit.

**A passing self-reported record is not proof of historical authenticity.** Checksums establish that files match declared bytes; the public verifier checks internal consistency, not that the tests were run. Independent reproduction requires controlled access to the engine under a separate evaluation agreement.

## Release handling

The original Rust files are unchanged for audit traceability. The journal and composite records are **redacted transformations**, explicitly not original byte-for-byte copies. Redaction removes internal paths, raw journal payloads, command-line arguments, implementation layout parameters, resource-tuning data and host clock values. It does not alter released outcome fields.

The three original source blob hashes can be recomputed from the published JSON bytes. SHA-256 values referring to complete private schedules are provenance references for a reviewer granted original access, not publicly verifiable attestations.
