# THM-M-0612 proof recheck at `9d3f687e` (slot34)

Item: `S56-M-0612-PROOF`

Date: `2026-07-15T15:39:57+08:00`

Base revision: `9d3f687e9bf0fe3120397744332e909472c52dfd`

Base tree: `558507d70ac5e5e38486f214a3e0ce7b33f7ae9b`

## Verdict

`blocked`. No eligible positive proof body was implemented or found for the
exact target `Stage1.THM_M_0612.StatementShape`. Its immediate remaining cut is
`M0612-T-SQUARED`, whose missing body is the proposition
`Stage1.THM_M_0612.RadiusSquaredObstruction`: it must derive `r ^ 2 <= R ^ 2`
from the frozen local symplectic-embedding and cylinder hypotheses.

The first deep unavailable package is `M0612-C-CAPACITY`. Neither this
repository nor the complete available pinned Lean package closure constructs a
compatible symplectic capacity with invariance, monotonicity, conformality, and
the required ball and cylinder results. The frozen local/scale route and the
alternative almost-complex and pseudoholomorphic-curve existence, compactness,
energy, and monotonicity packages also remain open. Adding any of these as an
axiom, bodyless declaration, or theorem premise would be a prohibited
placeholder rather than a proof.

`ObligationTree.lean` contains real bodies only for the elementary transport
from `r ^ 2 <= R ^ 2` to `r <= R` and for conditional root assembly that
accepts the entire missing obstruction as a premise. `LocalEncoding.lean` and
`EncodingSanityProbe.lean` prove nonvacuity, openness, local differentiability,
form nondegeneracy, and derivative injectivity. The positive-coordinate binder
and positive radii exclude degenerate shortcuts. None of these bodies closes a
frozen root-cut obligation.

The legacy `S1_M_256.lean` module elaborates and supplies a different global
embedding interface plus order-theoretic Gromov-width reductions. It still has
no proof of its `StatementShape`; its missing cylinder-width upper bound is the
hard nonsqueezing content rather than an available bridge to the canonical
local-domain target. The immutable prerequisite audit's only named external
Lean 4 nonsqueezing declaration has a `sorry` body and admitted dependencies,
so it is ineligible. Fresh repository, pinned-package, and all-worker scans
found no exact terminal body to pin or import.

Therefore no proof source or positive receipt was added. The root remains
`[H2, M3, R4]`, with `root_closed=false`, `audit_complete=false`, and
`theorem_complete=false`. The obligation-tree prerequisite is still
worker-provisional rather than master-accepted. Since the positive proof phase
is not genuinely self-tested as complete, `.stage1-worker-selftest.json` is
deliberately absent.

## Validation

All Lean checks reused the automation-provided pinned artifacts read-only. No
`lake update`, `lake build`, dependency clone/fetch, checkout/repair, or other
`.lake` mutation was requested. Temporary Lean outputs were isolated under
`/tmp` and removed. The untracked external `.lake` symlink makes this
nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0612` | 0 | Rank 256; planned; baseline L0/rework-required; legacy artifacts unaccepted; theorem incomplete. |
| `git status --short --untracked-files=all` before edits | 0 | Only the automation-provided untracked `Formalizations/Lean/.lake` symlink was present. |
| `python3 Stage1_Instances/THM-M-0612/check_obligation_tree.py` | 0 | 26 obligations and 58 typed edges passed; denominator `2cad29b7...a4bc8`; root open M3 because the squared-radius package remains M4. |
| isolated pinned `lake env lean --trust=0 -t0` replay of all four proof-relevant owned modules | 0 | `Statement.lean`, `ObligationTree.lean`, `LocalEncoding.lean`, and `EncodingSanityProbe.lean` elaborated; each of ten axiom reports was exactly `[propext, Classical.choice, Quot.sound]`; temporary outputs were removed. |
| pinned `lake env lean --trust=0 -t0` replay of `AwesomeTheorems/Stage1/S1_M_256.lean` | 0 | The legacy interface elaborated; output contains `AwesomeTheorems.Stage1.S1_M_256.StatementShape : Prop`, but no theorem proving it. |
| owned Lean prohibited-construct scan | 1 | Expected no-match exit; no `sorry`, `admit`, axiom/bodyless declaration, unsafe/oracle construct, or native decision shortcut occurs. |
| complete available pinned-package topical scan | 1 | Expected no-match exit for nonsqueezing, Gromov width, symplectic capacity, or pseudoholomorphic declarations. |
| repo-local topical inventory | 0 | Hits were legacy `S1_M_256` and unrelated `THM-M-0611`; inspection found no exact terminal body. |
| all-worker exact-target inventory | 0 | Worker clones contain the same five owned Lean modules with identical hashes and no `Proof.lean`, capacity implementation, or terminal nonsqueezing body. |
| scoped input audit since `435748c4` | 0 | No proof input or pin changed; only the preceding slot28 blocker JSON and Markdown entered this target path. |
| pinned environment and source-hash checks | 0 aggregate | Lean 4.29.0 commit `98dc76e...16740`; mathlib `8a178386...ea95`, tree `bdc39a31...1c2b`; recorded sources and pin hashes matched. |
| JSON, fail-closed identity, source-hash, and whitespace checks | 0 aggregate | Blocker identity, current base/tree, exact cut, unchanged debt vector, empty proof-credit fields, owned changed paths, and both fresh files passed. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent because the positive proof phase is blocked. |

The isolated replay compiled a temporary `Statement.olean`, then elaborated
the three modules importing `Statement` with the `LEAN_PATH` selected by
`lake env`. Output SHA-256 values were `e3b0c442...b855`,
`039f16b7...35a`, `4515cf76...0a3c5`, and `94de4565...81e`. The legacy
module output hash was `d63c0342...a3a1cb`.

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
