# THM-M-0958 validation-phase result

Item: `S56-M-0958-VALIDATION`. Base revision:
`51c2828e82ffb19860830f78b771f80e13ad7dff` (tree
`4655b8b40829513de6fb5661344b33fc7cd17cd1`).

## Narrow validation

The structured recipe copies `Statement.lean`, `ObligationTree.lean`,
`Proof.lean`, and `Validation.lean` into a fresh temporary directory. It runs
the pinned Lean 4.29.0 executable directly with `--trust=0`, a fixed locale,
timezone, and thread count. Bubblewrap denies network access and makes the host
and shared dependency cache read-only; only the temporary module directory is
writable. It runs no Lake update/build, clone, fetch, or dependency repair.

The exact statement, three conditional composition declarations, and all nine
partial radix declarations elaborate. `Validation.lean` imports neither
`Proof` nor `ObligationTree`; it separately reconstructs the finite digit-image
package and the conditional witness-to-root transport. Both differential
declarations pass `assert_no_sorry`, report exactly `propext`,
`Classical.choice`, and `Quot.sound`, and have a 17,070-declaration closure
across 672 modules with no bodyless nonaxiom or unsafe declaration.

This is intentionally a blocked-root result. The conditional transport still
consumes `WitnessConstructionTarget`, while the digit package consumes the
unconstructed vector set and proves no Elkin-scale cardinality. The proof
receipt accepts zero frozen obligations, and `M0958-T-WITNESS` remains open.
The exact root stays `[H1, M3, R4]`, with `audit_complete=false` and
`theorem_complete=false`.

## Commands and results

Commands ran from the repository root on 2026-07-15 (Asia/Shanghai). The
automation-provided `.lake` symlink was reused read-only and left unmodified.

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0958` | 0 | rank 1492, planned, L0/rework-required, theorem incomplete |
| exact DAG assertions | 0 | validation `[ ]` depends on provisional proof `[_]`; positive acceptance is dependency-illegal |
| `python3 -B Stage1_Instances/THM-M-0958/build_obligation_artifacts.py --check` | 0 | 64 obligations, 85 typed edges, denominator `a6628059...383e5b` passed |
| `python3 -B Stage1_Instances/THM-M-0958/check_obligation_tree.py` | 1 | historical checker rejected current HEAD at its stale base assertion; no validation credit assigned |
| `bash Stage1_Instances/THM-M-0958/check_proof.sh` | 1 | Lean replay portion ran, then historical `check_proof.py` rejected current HEAD at its stale base assertion; validation independently replays the sources |
| `python3 -I -B Stage1_Instances/THM-M-0958/check_validation.py --probe` | 0 | network-isolated trust-zero replay passed for the exact statement, 12 existing conditional/partial declarations, and 2 differential declarations; root remained open |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0958/check_validation.py --worker-packet .stage1-worker-selftest.json` | 0 | packet, receipt, hashes, pins, trust observations, selected provenance, and fail-closed decisions passed |
| JSON parsing and external Python syntax checks | 0 | spec, receipt, worker packet, and checker syntax passed |
| prohibited-construct scan over the four checked Lean modules | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, local axiom/constant/opaque/unsafe/extern, `implemented_by`, or `native_decide` found outside comments |
| `git diff --check -- Stage1_Instances/THM-M-0958 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The historical `validation-specs.json` belongs to
`S56-M-0958-OBLIGATION_TREE`: its 64 no-closure recipes all call the stale
obligation-tree checker. Likewise, `check_proof.py` is deliberately bound to
the prior proof worker's base, DAG state, and worker packet. This phase binds
the integrated proof receipt and re-elaborates actual Lean sources rather than
weakening those predecessor contracts or falsely claiming they pass.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | provisional pass | Exact statement plus all existing conditional/partial declarations and both differential declarations elaborate at trust zero. |
| Placeholder and unsafe boundary | provisional pass | Differential declarations are sorry-free; source and transitive-closure checks find no prohibited mechanism, bodyless nonaxiom, or unsafe declaration in the checked scope. |
| Axiom observation | provisional pass | Only `propext`, `Classical.choice`, and `Quot.sound` are observed. No accepted theorem-specific foundation or complete TCB closure exists. |
| Selected direct provenance | provisional pass | Local hashes, mathlib revision/tree/origin/license, and Defs, Log/Base, and Behrend source/blob/olean identities agree. Complete transitive provenance remains open. |
| Proof dependency and exact root | fail closed | Proof is not master accepted, and no premise-free Elkin witness/root exists. The mathematical cut remains `M0958-T-WITNESS`, including missing discrepancy and asymptotic work. |
| Human source and readability | fail closed | Exact edition/errata/node mapping and independent H0 review remain open; no independently accepted R0 reconstruction exists. |
| Hermetic release replay | fail closed | Shared warm artifacts are not a clean checkout, empty-cache cold bootstrap, offline restoration, or deterministic release bundle. |
| Independent verification | fail closed | This same-worker differential run is not a second signed independently provisioned runner or independent minimal verifier. |

The first failed gate is proof master acceptance together with exact witness/root
kernel closure. Retry requires an exact placeholder-free `M0958-T-WITNESS`
implementation and graph reconciliation, followed by the complete release
assurance work recorded in `validation-receipt.json`.

## Status boundary

This self-tested validation packet truthfully records both passed narrow gates
and failed assurance gates. It grants no accepted obligation state, root
closure, `M0-*`, `E0/E1`, `H0`, `R0`, `AUDIT-Z`, `THEOREM-Z`, release,
theorem completion, or master acceptance.
