# THM-M-0612 proof recheck at `50db6284` (slot34)

Item: `S56-M-0612-PROOF`

Date: `2026-07-15T16:33:35+08:00`

Base revision: `50db6284742415b7da294d323c820bf4b224711d`

Base tree: `bb477aa021efaf69c84ee3a98f486f4ba407bae2`

## Verdict

`blocked`. No eligible positive proof body was implemented or found for the
exact target `Stage1.THM_M_0612.StatementShape`. Its immediate remaining cut is
`M0612-T-SQUARED`, represented by
`Stage1.THM_M_0612.RadiusSquaredObstruction`: derive `r ^ 2 <= R ^ 2` from the
frozen local smooth symplectic-embedding and cylinder hypotheses.

The first deep unavailable package is `M0612-C-CAPACITY`. Neither this
repository nor the available pinned Lean package closure constructs a
compatible symplectic capacity with invariance, monotonicity, conformality,
and the required ball and cylinder computations. The frozen alternative route
also lacks compatible almost-complex and pseudoholomorphic-curve existence,
compactness, energy, and monotonicity packages.

`ObligationTree.lean` has real bodies only for the ordered-field transport from
`r ^ 2 <= R ^ 2` to `r <= R` and conditional root assembly that accepts the
entire missing obstruction as a premise. `LocalEncoding.lean` and
`EncodingSanityProbe.lean` prove nonvacuity, openness, local differentiability,
form nondegeneracy, and derivative injectivity. In particular, positive `r`
makes the source nonempty, `i : Q` excludes zero dimension, and preservation
of the nondegenerate form forces each on-ball derivative to be injective. No
vacuous or inconsistent-premise shortcut was found.

The legacy `S1_M_256.lean` module elaborates but exposes a different global
embedding interface and leaves the capacity/cylinder obstruction open. The
immutable prerequisite audit's only named external Lean 4 nonsqueezing
declaration has a `sorry` body and admitted dependencies. Fresh repository,
pinned-package, and visible worker-clone inventories found no exact terminal
body that could be pinned or imported.

No proof source or positive receipt was added. The root remains
`[H2, M3, R4]`, with `root_closed=false`, `audit_complete=false`, and
`theorem_complete=false`. The obligation-tree prerequisite is worker-
provisional `[_]`, not master-accepted `[x]`. Because the positive proof phase
is not complete, `.stage1-worker-selftest.json` is deliberately absent.

## Validation

All commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink to the canonical pinned artifacts was used
read-only. No `lake update`, `lake build`, dependency clone/fetch, checkout,
repair, or other `.lake` mutation was performed. Temporary Lean outputs were
isolated under `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0612` | 0 | Rank 256; planned hard-mathlib-anchor-and-wrapper lane; legacy artifacts unaccepted; theorem incomplete. |
| `git status --short --untracked-files=all` before edits | 0 | Only the automation-provided untracked `Formalizations/Lean/.lake` symlink was present. |
| `python3 Stage1_Instances/THM-M-0612/check_obligation_tree.py` | 0 | `PASS THM-M-0612 obligation tree: 26 obligations, 58 typed edges`; denominator `2cad29b7...a4bc8`; root open M3 because the radius-squared package remains M4. |
| isolated pinned `lake env lean --trust=0 -t0` replay of all four proof-relevant owned modules | 0 | `Statement.lean`, `ObligationTree.lean`, `LocalEncoding.lean`, and `EncodingSanityProbe.lean` elaborated; each of ten axiom reports was exactly `[propext, Classical.choice, Quot.sound]`; temporary outputs were removed. |
| `cd Formalizations/Lean && LEAN_NUM_THREADS=1 timeout 300 lake env lean --trust=0 -t0 AwesomeTheorems/Stage1/S1_M_256.lean` | 0 | The legacy interface elaborated and printed `StatementShape : Prop`, but no theorem proving it. |
| owned Lean prohibited-construct scan | 1 | Expected no-match exit; no `sorry`, `admit`, `sorryAx`, axiom/opaque declaration, unsafe construct, or native-decision shortcut occurs. |
| complete available pinned-package topical scan | 1 | Expected no-match exit for nonsqueezing, Gromov width, symplectic capacity, or pseudoholomorphic declarations. |
| repo-local topical inventory | 0 | Hits were legacy `S1_M_256` and unrelated `THM-M-0611`; inspection found no exact terminal body. |
| visible worker-clone target-source inventory | 0 | Available clones expose the same proof-relevant source hashes and no `Proof.lean`, capacity implementation, or terminal nonsqueezing body. |
| pinned environment and source-hash checks | 0 aggregate | Lean 4.29.0 commit `98dc76e...16740`; Lake 5.0.0; mathlib `8a178386...ea95`, tree `bdc39a31...1c2b`; `flt-regular` `56161b6e...1a27`; all recorded input and pin hashes matched. |
| `test ! -e .stage1-worker-selftest.json` before evidence creation | 0 | Completion self-test manifest deliberately absent because the positive proof phase is blocked. |
| JSON identity/hash/fail-closed assertions and whitespace checks | 0 aggregate | The blocker parses; item/base/hash/cut/path/state assertions passed; tracked and fresh-file whitespace checks passed. |

The isolated replay compiled a temporary `Statement.olean`, placed its
directory first in the `LEAN_PATH` selected by `lake env`, and then elaborated
the three importing modules. Output SHA-256 values were
`e3b0c442...b855`, `039f16b7...35a`, `4515cf76...0a3c5`, and
`94de4565...81e`.

Proof-input hashes remain `2de623b5...f919` for `Statement.lean`,
`0392a18a...07007` for `ObligationTree.lean`, `278177c5...a117` for
`LocalEncoding.lean`, and `1b61df00...ed82` for
`EncodingSanityProbe.lean`. The registry and typed-graph file hashes remain
`635af26d...8850` and `def70532...50b2`; the registry denominator remains
`2cad29b7...a4bc8`.

## Retry Condition

Resume after a placeholder-free implementation of `M0612-T-SQUARED` and its
frozen nonlinear dependencies, or discovery of an immutable compatible Lean 4
terminal proof that can be pinned, exact-type transported, and checked without
changing the dependency lock.

This is fresh target-owned nonrelease blocker evidence, not a proof receipt. It
does not satisfy `S56-M-0612-PROOF`, propose checklist state, or support audit
completion, theorem completion, validation, release, or master acceptance.
