# THM-M-0612 proof recheck at `8f3190fe` (slot26)

Item: `S56-M-0612-PROOF`

Date: `2026-07-15T17:24:58+08:00`

Base revision: `8f3190fed598f6cb4547035d0d96d460ba5fc5cc`

Base tree: `d8ca24ac4a840d07b81dcc099a4d31023046d649`

## Verdict

`blocked`. No eligible positive proof body was implemented or found for the
exact target `Stage1.THM_M_0612.StatementShape`. Its immediate remaining cut is
`M0612-T-SQUARED`, represented by
`Stage1.THM_M_0612.RadiusSquaredObstruction`: derive `r ^ 2 <= R ^ 2` from the
frozen local smooth symplectic-embedding and cylinder hypotheses.

The proof-relevant target sources and pinned dependency inputs are byte-identical
to the preceding integrated recheck. A fresh complete scan of the available
pinned package sources still finds no declaration for nonsqueezing, Gromov width,
symplectic capacity, or pseudoholomorphic curves. The prerequisite external audit
found one named nonsqueezing declaration, but its body and dependencies contain
admissions and are ineligible for proof credit.

`ObligationTree.lean` has real bodies only for the ordered-field transport from
`r ^ 2 <= R ^ 2` to `r <= R` and the conditional root assembly that accepts the
entire missing obstruction as a premise. `LocalEncoding.lean` and
`EncodingSanityProbe.lean` establish nonvacuity, openness, local differentiability,
form nondegeneracy, and derivative injectivity. These checked facts rule out a
vacuous shortcut but do not construct the nonlinear symplectic obstruction.

The first deep unavailable package is `M0612-C-CAPACITY`: the frozen route needs
a compatible symplectic capacity with invariance, monotonicity, conformality, and
ball/cylinder computations. Its alternative route needs almost-complex and
pseudoholomorphic-curve existence, compactness, energy, and monotonicity packages.
Introducing any missing package as an axiom, bodyless declaration, or theorem
premise would be a prohibited placeholder rather than a proof.

No proof source or positive receipt was added. The root remains `[H2, M3, R4]`,
with `root_closed=false`, `audit_complete=false`, and `theorem_complete=false`.
The prerequisite obligation-tree item is worker-provisional `[_]`, not master-
accepted `[x]`. Because this positive proof phase is not genuinely self-tested as
complete, `.stage1-worker-selftest.json` is deliberately absent.

## Validation

All commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts was reused
read-only. No `lake update`, `lake build`, dependency clone/fetch, checkout,
repair, or other `.lake` mutation was performed. Temporary Lean output was
isolated under `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0612` | 0 | Rank 256; planned hard-mathlib-anchor-and-wrapper lane; legacy artifacts unaccepted; theorem incomplete. |
| `git status --short --untracked-files=all` before edits | 0 | Only the automation-provided untracked `Formalizations/Lean/.lake` symlink was present. |
| `python3 Stage1_Instances/THM-M-0612/check_obligation_tree.py` | 0 | `PASS THM-M-0612 obligation tree: 26 obligations, 58 typed edges`; denominator `2cad29b7...a4bc8`; root open M3 because the radius-squared package remains M4. |
| isolated pinned `lake env lean --trust=0 -t0` replay of all four proof-relevant owned modules | 0 | `Statement.lean`, `ObligationTree.lean`, `LocalEncoding.lean`, and `EncodingSanityProbe.lean` elaborated; each of ten axiom reports was exactly `[propext, Classical.choice, Quot.sound]`; temporary outputs were removed. |
| owned Lean prohibited-construct scan | 1 | Expected no-match exit; no `sorry`, `admit`, `sorryAx`, axiom/bodyless or opaque declaration, unsafe construct, `implemented_by`, `native_decide`, or `extern` occurs. |
| complete available pinned-package topical scan | 1 | Expected no-match exit for nonsqueezing, Gromov width, symplectic capacity, or pseudoholomorphic declarations. |
| pinned environment and source-hash checks | 0 aggregate | Lean 4.29.0 commit `98dc76e...16740`; Lake 5.0.0; mathlib `8a178386...ea95`, tree `bdc39a31...1c2b`; `flt-regular` `56161b6e...1a27`; all proof-input, registry, graph, audit, validation-spec, toolchain, and manifest hashes matched. |
| input-freshness comparison from `4d389eb4` | 0 | Only the preceding slot26 blocker pair entered the target path; no proof source, registry, graph, legacy module, toolchain, or dependency manifest changed. |
| JSON identity/hash/fail-closed assertions and whitespace checks | 0 aggregate | The blocker parses and matches the current base/tree, source hashes, open cut, unchanged debt vector, empty proof-credit arrays, owned changed paths, and absent self-test; scoped and fresh-file whitespace checks pass. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent because the proof phase is blocked. |

The isolated replay used the existing `lake env` path and generated only a
temporary `Statement.olean` under `/tmp`. Output SHA-256 values were
`e3b0c442...b855`, `039f16b7...35a`, `4515cf76...0a3c5`, and
`94de4565...81e` for the four modules respectively.

Proof-input SHA-256 values remain `2de623b5...f919` for `Statement.lean`,
`0392a18a...07007` for `ObligationTree.lean`, `278177c5...a117` for
`LocalEncoding.lean`, and `1b61df00...ed82` for
`EncodingSanityProbe.lean`. The registry and typed-graph hashes remain
`635af26d...8850` and `def70532...50b2`; the registry denominator remains
`2cad29b7...a4bc8`.

## Scheduler Handoff

This target has now accumulated substantially more than five unresolved proof
rechecks even though the authoritative DAG still records `attempts: 0`. The
rev-5.6 split-after-five rule makes another undifferentiated root retry invalid
as an execution strategy. The master should split dependency-legal child nodes
for `M0612-N-LOCAL`, `M0612-N-SCALE`, `M0612-B-DIM2`, `M0612-B-HIGHER`, and
`M0612-C-CAPACITY`. This worker does not edit the DAG, checklist, item state, or
attempt counter.

## Retry Condition

Resume only on a dependency-legal child node after a placeholder-free
implementation plan for one frozen nonlinear package is available, or after
discovery of an immutable compatible Lean 4 terminal proof that can be pinned,
exact-type transported, and checked without changing the dependency lock.

This is fresh target-owned nonrelease blocker evidence, not a proof receipt. It
does not satisfy `S56-M-0612-PROOF`, propose checklist state, or support audit
completion, theorem completion, validation, release, or master acceptance.
