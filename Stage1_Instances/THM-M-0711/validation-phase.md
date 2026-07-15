# THM-M-0711 validation-phase result

Item: `S56-M-0711-VALIDATION`. Validation date: 2026-07-15. Base
revision: `3a40b1969f841e07036db5c4d7f03e97c7c57949`.

## Gate result

The node-scoped replay passes for the exact frozen statement, the conditional
obligation composition, and every existing proof-phase declaration. It runs
Lean at trust level zero under `bubblewrap --unshare-net`, uses a read-only
host view with only a fresh `/tmp` output directory writable, and fixes the
locale, timezone, thread count, executable hashes, dependency revision, and
explicit `LEAN_PATH`.

`Validation.lean` imports neither `Proof` nor `ObligationTree`. It separately
reconstructs quotient identity normalization, generic noncomputability
transfer, the pinned halting leaf, and the conditional final adapter. All
proof and differential declarations are reported sorry-free and depend on
exactly `propext`, `Classical.choice`, and `Quot.sound`. Its machine-derived
closure contains 6104 declarations from 226 modules, with no bodyless
nonaxiom or unsafe declaration observed.

This does not validate the theorem root. Both final adapters retain the
halting-to-finite-presentation reduction as an explicit premise. No finite
presentation construction, computable word compiler, or reduction
correctness proof is present. The exact root therefore remains
`[H1, M4, R4]`, with `M0711-B-REDUCTION` and `M0711-S-FOUNDATION` as its
open cut. Accepted obligation state remains empty and
`theorem_complete=false`.

## Commands and results

Commands ran from the repository root. No `lake update`, `lake build`,
dependency clone, dependency fetch, or `.lake` mutation was performed.

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0711` | 0 | rank 751, planned, L0/rework-required, theorem incomplete |
| `python3 Stage1_Instances/THM-M-0711/check_obligation_tree.py` | 0 | 17 obligations and 38 typed edges passed; root open M4 |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0711/check_validation.py --worker-packet .stage1-worker-selftest.json` | 0 | network-isolated trust-zero replay, selected provenance, exact open-root decisions, and worker packet passed |
| `python3 -m json.tool` on the validation spec, receipt, and worker packet | 0 | all structured validation documents parsed |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-m0711-validation-pycache python3 -m py_compile Stage1_Instances/THM-M-0711/check_validation.py` | 0 | checker syntax compiled outside the repository |
| `git diff --check -- Stage1_Instances/THM-M-0711 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | provisional pass | Fresh local outputs elaborate the exact statement, frozen composition, five local partial/conditional proof declarations, and four differential declarations at trust zero. |
| Placeholder and unsafe boundary | provisional pass | Owned Lean sources pass a nested-comment-aware prohibited-device scan; the checked declarations are kernel-reported sorry-free; the differential transitive closure reports no bodyless nonaxiom or unsafe declaration. |
| Axiom observation | provisional pass | Every proof and differential declaration reports exactly the classical trio. This is not an accepted theorem-specific foundation policy or complete TCB closure. |
| Selected direct provenance | provisional pass | Local inputs are hash-bound; the pinned clean mathlib revision/tree/origin/license and three direct source/olean boundaries agree. Complete terminal-root and transitive TCB provenance remains open. |
| Proof dependency and exact root | fail closed | The proof receipt is unaccepted and no premise-free body proves the finite-presentation reduction or exact root. |
| Complete trust/provenance | fail closed | The accepted foundation profile, complete transitive import/artifact inventory, and full TCB/SBOM are absent. |
| Hermetic release replay | fail closed | The run is network-isolated and fresh-output, but reuses a shared warm dependency cache rather than a clean checkout, empty caches, cold build, and offline dependency restoration. |
| Independent verification | fail closed | The differential module shares this worker clone and cache; no distinct signed verifier or independently provisioned runner exists. |

The validation item is genuinely self-tested as an honest blocked worker
receipt. It grants no accepted proof state, `M0-*`, `E0/E1`, `AUDIT-Z`,
`THEOREM-Z`, release, theorem completion, or master acceptance.
