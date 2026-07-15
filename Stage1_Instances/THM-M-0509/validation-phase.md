# THM-M-0509 validation-phase result

Item: `S56-M-0509-VALIDATION`. Base revision:
`229ca98e7478d389ccf8de8173c94e0e7c8fe670` (tree
`d3cc9562940b923aebbe7e01ce66232079760b3b`).

## Result

The node is self-tested but blocked. `Validation.lean` rechecks the three
proof-phase interfaces and the frozen conditional root handoff, then separately
composes the exact root from `EventualPositiveRepresentationCount`. That
positivity proposition remains an explicit input: no inhabitant is present, so
this is not a proof of Chen's theorem.

The validator copies `Statement.lean`, `AnchorAudit.lean`,
`ObligationTree.lean`, `Proof.lean`, and `Validation.lean` to a fresh temporary
directory. Each Lean invocation runs at trust level zero under Bubblewrap with
the host root read-only, only the temporary directory writable, the environment
fixed, and outbound networking unavailable. Existing pinned compiled package
artifacts are read through `LEAN_PATH`; no update, build, clone, fetch, or
dependency write is performed.

## Commands and results

Commands ran in the worker clone on 2026-07-15 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0509` | 0 | Rank 883, planned, L0/rework_required, theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0509/check_statement.py` | 0 | Expression hash `e2c8d378...c64f7`; four statement mutations remain killed. |
| `python3 Stage1_Instances/THM-M-0509/check_anchor_audit.py` | 0 | Audit inventory, pinned mathlib revision, and support-declaration probe agree. |
| `python3 Stage1_Instances/THM-M-0509/check_obligation_tree.py` | 0 | 15 obligations and 40 typed edges passed; denominator `74b4c30d...703bd`; root remains open M4. |
| `bash Stage1_Instances/THM-M-0509/check_proof.sh` | 1 | Both direct pinned Lean and scoped mathlib `lake env lean --trust=0` replays completed and agreed; the post-replay checker then failed because it intentionally binds the historical proof-worker HEAD and pre-integration DAG state. This stale integrated recipe is recorded, not treated as proof invalidity. |
| scoped pinned-mathlib `lake env lean --trust=0` replay of the five copied modules with explicit `LEAN_PATH` and `--root` | 0 | Statement, support audit, obligation handoff, proof interfaces, and validation probe elaborated; normalized outputs matched the isolated direct-pinned-Lean lane. |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0509/check_validation.py --worker-packet .stage1-worker-selftest.json` | 0 | Five network-isolated trust-zero Lean replays passed; closure has 5 roots, 5203 declarations, 200 modules, only `propext`, `Classical.choice`, and `Quot.sound`, no unexpected bodyless declaration, and no unsafe declaration. |
| JSON parsing for the spec, receipt, blocker, and worker packet | 0 | All four artifacts are valid JSON. |
| external-cache `py_compile` of `check_validation.py` | 0 | Checker syntax compiled without writing bytecode in the repository. |
| `git diff --check -- Stage1_Instances/THM-M-0509 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

The root-project Lake environment remains unsuitable because its unrelated
shared `flt-regular` checkout cannot resolve `HEAD`. The existing proof script
provides the required narrow `lake env lean` corroboration through pinned
mathlib while avoiding root-project discovery; the validation runner adds
stronger per-invocation network and filesystem isolation with the exact pinned
Lean binary.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Exact kernel replay | pass, nonrelease | Exact statement, support probe, three partial interfaces, conditional handoff, and differential conditional composition elaborate at trust zero. |
| Placeholder/unsafe observation | pass in observed boundary | Local replay modules are token-scanned and assertion-checked; the five-root closure reports no unexpected bodyless or unsafe declaration. |
| Axiom observation | provisional pass | Checked declarations use only `propext`, `Classical.choice`, and `Quot.sound`; no theorem-specific foundation profile is accepted. |
| Selected provenance | pass, nonrelease | Frozen hashes, mathlib revision/tree/remote/cleanliness/license, and six selected source/object pairs agree. Complete transitive provenance and TCB/SBOM closure are absent. |
| Proof dependency | fail closed | `S56-M-0509-PROOF` is worker-provisional `[_]`, not master-accepted `[x]`. |
| Exact root | fail | No body inhabits `EventualPositiveRepresentationCount`; weighted-sieve distribution, switching, remainder, positivity, and extraction remain open. |
| Hermetic release | fail closed | This uses a shared warm cache, not a clean-checkout empty-cache cold build or offline-restorable deterministic bundle. |
| Independent verification | fail closed | The differential route uses this worker, checkout, kernel, and cache; no second signature, clean runner, or independent minimal verifier exists. |
| Human/readable review | fail closed | Pinpoint primary-source `H0` and independently reviewed `R0` remain open. |

The first failed node gate is
`dependency.S56-M-0509-PROOF.master_acceptance`; the mathematical root cut is
`M0509-T-P2-EXTRACTION`. The vector remains `[H1,M4,R4]`, with
`audit_complete=false` and `theorem_complete=false`. Provisional `[_]` means
only that this fail-closed validation packet is implemented and self-tested; it
grants no `E0/E1`, accepted `M0-*`, release, or master acceptance.
