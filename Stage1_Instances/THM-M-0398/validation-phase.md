# THM-M-0398 validation-phase evidence

This phase truthfully validates only the proof bodies that exist: constant
monotonicity and conditional specialization of a uniform constant-factor Roth
estimate. `Validation.lean` independently reimplements both bodies. Kernel
elaboration reports exactly `propext`, `Classical.choice`, and `Quot.sound`,
with no `sorryAx`; the fail-closed verifier binds the sources, registry, graph,
proof receipt, toolchain, and dependency manifest by SHA-256.

The canonical theorem is **not** proved. The uniform Roth engine `M0398-L4`
and its root-critical dependencies remain open, so the root stays `M3` and
provenance/trust closure is incomplete. The warm pinned-cache run is not a
release-grade cold hermetic replay, and the same-checkout independent
implementation is not a distinct signed independent runner.

Base revision: `0699f252b887121b74c60b9864f359c46ed435d6`.
Validation time: `2026-07-11T19:52:16Z`.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets pass |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0398` | exit 0; rank 11, planned, theorem incomplete |
| `python3 Stage1_Instances/THM-M-0398/check_obligation_tree.py` | exit 0; 15 obligations, 29 edges, root open M3 |
| `python3 Stage1_Instances/THM-M-0398/check_validation.py` | exit 0; frozen inputs pass, proof and independent probes elaborate, root open |
| `git diff --check -- Stage1_Instances/THM-M-0398 .stage1-worker-selftest.json` | exit 0; no whitespace errors |

No `.lake` update, build, clone, fetch, or mutation was performed.
