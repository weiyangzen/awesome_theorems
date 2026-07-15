# THM-M-0612 proof recheck at `3a40b196` (slot23)

Item: `S56-M-0612-PROOF`

Date: `2026-07-15T12:49:48+08:00`

Base revision: `3a40b1969f841e07036db5c4d7f03e97c7c57949`

Base tree: `404cccc598c2d4c8831d55138df788f0438ddce8`

## Verdict

`blocked`. No eligible proof body was implemented or found for the exact target
`Stage1.THM_M_0612.StatementShape`. The frozen immediate root cut remains
`M0612-T-SQUARED`, represented by
`Stage1.THM_M_0612.RadiusSquaredObstruction`: from the canonical local smooth
symplectic embedding and cylinder hypotheses, derive `r ^ 2 <= R ^ 2`.

The first deep unavailable package is `M0612-C-CAPACITY`. Neither the repository
nor the pinned package sources construct a symplectic capacity on the canonical
local-domain model together with the required invariance, monotonicity,
conformality, and ball and cylinder computations. The frozen alternative branch
also lacks compatible almost-complex structures and pseudoholomorphic-curve
existence, compactness, energy, and monotonicity results.

`ObligationTree.lean` supplies only the real ordered-field transport
`radius_le_of_sq_le` and the conditional final composition
`root_of_radiusSquaredObstruction`. The latter accepts the whole missing
geometric obstruction as a premise; it does not construct that premise. The
additional local-encoding and sanity declarations establish nonvacuity,
openness, differentiability, form nondegeneracy, and derivative injectivity, but
none closes the frozen root cut.

A fresh source audit found no terminal declaration in the repo-local or pinned
Lean sources. Pinned mathlib provides finite symplectic-matrix infrastructure,
not nonlinear nonsqueezing. The legacy `S1_M_256.lean` file uses a different
global embedding interface and proves only definitions, order lemmas, and
conditional reductions. The only audited external Lean 4 theorem named
`gromovNonsqueezing`, at immutable commit
`acc509702046aaae6a3c9be4546d5735ad7450cf`, has a `sorry` body and admitted
supporting declarations, so it is ineligible for pinning or proof credit.

The automation-provided top-level Lake cache is not a valid checkout:
`.lake/packages/flt-regular/.git/HEAD` is `refs/heads/.invalid`. Consequently the
prescribed top-level `lake env lean --version` did not finish within 20 seconds
and was terminated with exit 124. This worker did not repair, fetch, clone, or
otherwise mutate `.lake`. As diagnostic evidence only, Lean 4.29.0 was invoked
with an explicit read-only `LEAN_PATH` assembled from the already-present pinned
package build artifacts. All four owned Lean sources elaborated with `--trust=0`;
the ten printed declarations reported exactly `propext`, `Classical.choice`, and
`Quot.sound`. This does not make the recorded top-level Lake recipe pass and does
not close `M0612-T-SQUARED`.

No proof source or positive receipt was added. The root vector remains
`[H2, M3, R4]`, `root_closed=false`, and `theorem_complete=false`. The
prerequisite obligation-tree item is worker-provisional `[_]`, not
master-accepted `[x]`. Because the proof deliverable is incomplete,
`.stage1-worker-selftest.json` is deliberately absent.

## Validation

All commands ran in this worker clone. No `lake update`, `lake build`, dependency
clone/fetch, checkout, repair, or other `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0612` | 0 | Rank 256; planned hard-mathlib-anchor-and-wrapper lane; legacy artifacts unaccepted; theorem incomplete. |
| `git status --short --untracked-files=all` before edits | 0 | Only the automation-provided untracked `Formalizations/Lean/.lake` symlink was present. |
| `python3 Stage1_Instances/THM-M-0612/check_obligation_tree.py` | 0 | `PASS THM-M-0612 obligation tree: 26 obligations, 58 typed edges`; denominator `2cad29b7...a4bc8`; root open M3 because the squared-radius package remains M4. |
| `cd Formalizations/Lean && timeout 20s lake env lean --version` | 124 | The malformed `flt-regular` checkout prevented Lake from reaching Lean; the bounded command produced no output. |
| explicit-path pinned Lean `--trust=0 -t0` replay of `Statement.lean`, `ObligationTree.lean`, `LocalEncoding.lean`, and `EncodingSanityProbe.lean` | 0 | All four sources elaborated. Output SHA-256 values were respectively `e3b0c442...b855`, `039f16b7...35a`, `4515cf76...0a3c5`, and `94de4565...81e`; all ten axiom reports were exactly `[propext, Classical.choice, Quot.sound]`. |
| `cd Formalizations/Lean && lake --version && elan show && elan which lean` | 0 | Lake `5.0.0-src+98dc76e`; active Lean `4.29.0`, commit `98dc76e...16740`. |
| `git -C Formalizations/Lean/.lake/packages/flt-regular rev-parse HEAD` | 128 | `HEAD` cannot be resolved; `.git/HEAD` contains `ref: refs/heads/.invalid`. |
| `git -C Formalizations/Lean/.lake/packages/flt-regular cat-file -t 56161b6eb5281fbfe9c38f2bcec0f429ebc11a27` | 0 | The manifest-pinned object is present and has type `commit`, but it is not checked out at a valid `HEAD`. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | Mathlib revision `8a178386...ea95`, tree `bdc39a31...1c2b`. |
| owned Lean prohibited-construct scan | 1 | Expected no-match exit; no `sorry`, `admit`, axiom/bodyless declaration, unsafe/oracle construct, or native-decision shortcut occurs. |
| complete pinned-package topical scan | 1 | Expected no-match exit for nonsqueezing, Gromov width, symplectic capacity, or pseudoholomorphic declarations. |
| source and frozen-artifact SHA-256 check | 0 | Statement `2de623b5...f919`; conditional composition `0392a18a...07007`; registry file `635af26d...8850`; typed graphs `def70532...50b2`; pins unchanged. |
| paired JSON parse, fail-closed invariant, hash, and fresh-file whitespace assertions | 0 | `PASS current-head blocker identity, hashes, fail-closed state, changed paths, whitespace, and absent selftest`. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent. |

The explicit replay compiled `Statement.lean` to a temporary `Statement.olean`,
prepended that temporary directory while checking the three modules that import
`Statement`, and removed all temporary output. The input is nonrelease evidence:
the untracked `.lake` symlink points to the canonical automation cache outside
the clone.

## Retry Condition

Resume after a placeholder-free implementation of `M0612-T-SQUARED` and its
frozen nonlinear dependencies, or discovery of an immutable compatible Lean 4
terminal proof that can be pinned, exact-type transported, and checked without
changing the dependency lock. A recorded top-level Lake replay additionally
requires the automation cache to expose manifest-pinned `flt-regular` commit
`56161b6eb5281fbfe9c38f2bcec0f429ebc11a27` through a valid checkout.

This is fresh owned blocker evidence, not a proof receipt. It does not satisfy
`S56-M-0612-PROOF`, propose checklist state, or support audit completion,
theorem completion, validation, release, or master acceptance.
