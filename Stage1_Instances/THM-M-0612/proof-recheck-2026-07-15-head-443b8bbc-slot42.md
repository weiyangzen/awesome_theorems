# THM-M-0612 proof recheck at `443b8bbc` (slot42)

Item: `S56-M-0612-PROOF`

Date: `2026-07-15T11:38:01+08:00`

Base revision: `443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b`

Base tree: `c5771c47c12b80aba613e6d844570f83b39ded6d`

## Verdict

`blocked`. No eligible proof body was implemented or found for the exact
target `Stage1.THM_M_0612.StatementShape`. The immediate root cut remains
`M0612-T-SQUARED`: derive `r ^ 2 <= R ^ 2` from the frozen local
symplectic-embedding and cylinder hypotheses. The first deep unavailable
package is `M0612-C-CAPACITY`. Neither this repository nor the present pinned
package sources contain the compatible capacity construction, invariance,
monotonicity, conformality, ball computation, and cylinder computation needed
by that route. The alternative branch also lacks the required compatible
almost-complex structures and pseudoholomorphic-curve existence, compactness,
energy, and monotonicity results.

`ObligationTree.lean` has two real but nonterminal bodies. The theorem
`radius_le_of_sq_le` proves the ordered-field transport from squared radii, and
`root_of_radiusSquaredObstruction` composes the exact root only after accepting
the entire missing geometric obstruction as a premise. Treating that premise
as an axiom, bodyless declaration, or assumed package would be a prohibited
placeholder. The local encoding lemmas and diagnostic probe establish
nonvacuity, openness, nondegeneracy, and derivative injectivity only; they do
not close a frozen root-cut obligation.

The legacy `S1_M_256.lean` uses a different global-map interface and supplies
only definitions and conditional/order-theoretic reductions. The prerequisite
anchor audit found one named external Lean 4 nonsqueezing declaration, but its
body and dependencies contain admissions. A fresh topical source scan found no
terminal declaration in the available pinned packages. Consequently the root
vector remains `[H2, M3, R4]`, `root_closed=false`, and
`theorem_complete=false`.

There is also a new environment blocker. The automation-provided `.lake`
symlink currently exposes a corrupt or incomplete checkout for the manifest-
pinned `flt-regular` dependency: its `HEAD` is `refs/heads/.invalid`, and the
required commit `56161b6eb5281fbfe9c38f2bcec0f429ebc11a27` is absent. Lake
therefore fails before invoking Lean. Per worker policy, this checkout was not
repaired, fetched, or otherwise mutated. Earlier receipt-bound elaborations do
not become current kernel evidence for this base.

No proof source or positive receipt was added. The prerequisite obligation-
tree item is still worker-provisional `[_]`, not master-accepted `[x]`. Because
the assigned positive proof phase is not genuinely self-tested,
`.stage1-worker-selftest.json` is deliberately absent.

## Validation

All checks ran in this worker clone. No `lake update`, `lake build`, dependency
clone/fetch, or `.lake` mutation was requested.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0612` | 0 | Rank 256; planned hard-mathlib-anchor-and-wrapper lane; legacy artifacts unaccepted; theorem incomplete. |
| `git status --short --untracked-files=all` before edits | 0 | Only the automation-provided untracked `Formalizations/Lean/.lake` symlink was present. |
| `python3 Stage1_Instances/THM-M-0612/check_obligation_tree.py` | 0 | `PASS THM-M-0612 obligation tree: 26 obligations, 58 typed edges`; denominator `2cad29b7...a4bc8`; root open M3 because the radius-squared package remains M4. |
| `cd Formalizations/Lean && lake env lean --version` | 1 | Lake could not resolve `flt-regular` `HEAD` and did not invoke Lean. |
| `cd Formalizations/Lean && lake env printenv LEAN_PATH` | 1 | Same `flt-regular` checkout failure. |
| isolated `lake env lean --trust=0 -t0` replay of the four owned Lean sources | 1 preflight | Replay could not start because `lake env which lean` and `lake env printenv LEAN_PATH` fail on `flt-regular`; no current kernel result is claimed. |
| `cd Formalizations/Lean && lake --version && elan show && elan which lean` | 0 | Lake `5.0.0-src+98dc76e`; active Lean `4.29.0`, commit `98dc76e...16740`; this identifies the tool binary but does not elaborate the target. |
| `git -C Formalizations/Lean/.lake/packages/flt-regular rev-parse HEAD` | 128 | `fatal: ambiguous argument 'HEAD'`; `.git/HEAD` is `ref: refs/heads/.invalid`. |
| `git -C Formalizations/Lean/.lake/packages/flt-regular cat-file -t 56161b6eb5281fbfe9c38f2bcec0f429ebc11a27` | 128 | Required manifest commit is absent. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | Mathlib remains `8a178386...ea95`, tree `bdc39a31...1c2b`. |
| owned Lean prohibited-construct scan | 1 | Expected no-match exit; no `sorry`, `admit`, axiom/bodyless declaration, unsafe/oracle construct, or native decision shortcut occurs. |
| available pinned-package topical scan | 1 | Expected no-match exit for nonsqueezing, Gromov width, symplectic capacity, or pseudoholomorphic declarations. |
| source and frozen-artifact SHA-256 check | 0 | Statement `2de623b5...f919`; obligation composition `0392a18a...07007`; registry `635af26d...8850`; typed graphs `def70532...50b2`; pins unchanged. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent. |

The immutable repository input is HEAD `443b8bbc...bee2b`, tree
`c5771c47...ded6d`. The worker `.lake` symlink points outside the clone to the
canonical automation cache, so this remains nonrelease evidence. The manifest
still pins `flt-regular` at `56161b6e...1a27`; the observed cache state is not
the declared dependency closure.

## Retry Condition

Resume proof work after a placeholder-free implementation of
`M0612-T-SQUARED` and its frozen nonlinear dependencies, or after discovery of
an immutable compatible Lean 4 terminal proof that can be pinned,
exact-type transported, and checked without changing the dependency lock. A
future validation attempt must additionally have the already-pinned
`flt-regular` commit present and checked out in the read-only automation cache
so `lake env lean` can run.

This is fresh owned blocker evidence, not a proof receipt. It does not satisfy
`S56-M-0612-PROOF`, propose checklist state, or support audit completion,
theorem completion, validation, release, or master acceptance.
