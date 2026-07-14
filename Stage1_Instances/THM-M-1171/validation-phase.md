# THM-M-1171 validation-phase result

Item: `S56-M-1171-VALIDATION`. Base revision:
`a1a7e939e58f103f5ff5d23af51437fa8658aa04`.

## Narrow validation

The structured recipe re-elaborates the exact target in `Statement.lean`, both
partial declarations in `Proof.lean`, and two separately written no-import versions in
`Validation.lean`. Every Lean process runs at trust level zero inside a
bubblewrap network namespace, with a read-only host root, a fresh writable
output directory, and fixed locale, timezone, and thread count. The
differential module imports neither `Proof` nor an obligation-tree module.

All four proof bodies report exactly `propext`, `Classical.choice`, and
`Quot.sound`. The differential module reports both declarations sorry-free;
its 23,207-declaration, 895-module observed closure contains no bodyless
nonaxiom or unsafe declaration. Nested-comment-aware supplemental scans find no
placeholder, bodyless declaration, unsafe declaration, native oracle, or
implementation escape in the three local Lean sources. Current source hashes,
the clean pinned mathlib revision/tree/origin/license, and the selected source
and compiled boundaries for `opNorm_le_bound₂` and `eLpNorm_sum_le` agree.

This is intentionally a negative-root validation. The proof predecessor is
only provisional and closes zero frozen obligations. Both checked results are
generic ingredients whose frozen interfaces remain planned prose; neither
supplies the missing strong `L^p` multiplier estimate or full Hessian
assembly. The exact root remains `[H2, M4, R4]`, with
`M1171-L-MIHLIN`, `M1171-L-FOURIER-DERIV`, and
`M1171-L-LP-ASSEMBLY` as the recorded open cut and
`theorem_complete=false`.

## Commands and results

Commands ran from the repository root on 2026-07-15 (Asia/Shanghai). The
automation-provided canonical `.lake` symlink was reused read-only. No `lake
update`, `lake build`, dependency clone, or dependency fetch was run.

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-1171` | 0 | rank 372, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 Stage1_Instances/THM-M-1171/check_obligation_tree.py` | 0 | 18 obligations, 59 typed edges, denominator `b3c709ee...1fc10`; root open M4 |
| `python3 -I -B Stage1_Instances/THM-M-1171/check_validation.py --worker-packet .stage1-worker-selftest.json` | 0 | network-isolated trust-zero fresh-output replay, receipt, pins, selected provenance, and fail-closed decisions passed |
| `python3 -m json.tool Stage1_Instances/THM-M-1171/validation-spec.json >/dev/null && python3 -m json.tool Stage1_Instances/THM-M-1171/validation-receipt.json >/dev/null && python3 -m json.tool .stage1-worker-selftest.json >/dev/null` | 0 | all validation JSON documents parsed |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-m1171-validation-pycache python3 -m py_compile Stage1_Instances/THM-M-1171/check_validation.py` | 0 | checker syntax compiled outside the repository |
| `git diff --check -- Stage1_Instances/THM-M-1171 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | provisional pass | Fresh local output elaborates the exact statement and all four extant proof bodies at trust level zero. |
| Placeholder and unsafe boundary | provisional pass | Source scans pass, both differential declarations are kernel-reported sorry-free, and their observed closure has no bodyless nonaxiom or unsafe declaration. |
| Axiom observation | provisional pass | Every checked body uses only the selected classical trio. This is not an accepted theorem-specific foundation or complete TCB closure. |
| Selected direct provenance | provisional pass | Local inputs are hash-bound; the pinned mathlib revision/tree/origin/license and two direct source/olean boundaries agree. Complete transitive import, artifact, and TCB provenance remains open. |
| Proof dependency and exact root | fail closed | The proof receipt is unaccepted, closes zero frozen obligations, and supplies no Mikhlin bridge, component multiplier estimate, full assembly, or root composition. |
| Human source and readability | fail closed | The primary source lacks theorem/page-level assumption and errata mapping; no independent H0 or R0 review exists. |
| Hermetic release replay | fail closed | The run reused shared warm artifacts, not a clean checkout with empty caches, a cold build, offline restoration, or complete SBOM/TCB archive. |
| Independent verification | fail closed | The differential module shares this worker, checkout, toolchain, and cache; there is no distinct signed verifier or independently provisioned runner. |

The validation node is self-tested only as an honest, nonrelease blocked
receipt. It grants no accepted obligation state, root closure, `M0-*`,
`E0/E1`, `AUDIT-Z`, `THEOREM-Z`, release, theorem completion, or master
acceptance.
