# THM-M-0612 dimension-two partial proof self-test

Item: `S56-M-0612-PROOF`

Recorded: `2026-07-15T18:49:11+08:00`

Base revision: `43f55bb87aa8883be277a6660f49c6f8ba647082`

Base tree: `8e624c67ebaa9cd00a352276e1fca6d17c18e0b9`

## Implemented Bodies

`DimensionTwo.lean` adds four unconditional, placeholder-free bodies for the
exact `Q = Fin 1` specialization of the canonical local-domain encoding.

`symplectic_det_dimTwo` computes the determinant of a two-dimensional
continuous linear map from preservation of `standardForm`. It reindexes the
matrix to `Fin 2`, evaluates the form on the two coordinate basis vectors, and
obtains determinant one.

`image_volume_eq_dimTwo` applies mathlib's differentiable injective
change-of-variables formula on the open source ball. Local smoothness supplies
the derivative, local injectivity supplies the image hypothesis, and the
determinant lemma makes the Jacobian integrand one.

`volume_ball_dimTwo` computes the volume of the coordinate ball as
`ENNReal.ofReal r ^ 2 * ENNReal.ofReal Real.pi` from
`MeasureTheory.volume_sum_rpow_lt`, including the Gamma-function
normalization. `dimTwo_radiusSquaredObstruction` identifies the `Fin 1`
cylinder with the same coordinate ball, uses image inclusion and volume
monotonicity, then cancels the positive factor `pi` to prove `r ^ 2 <= R ^ 2`.

This is mathematically substantive progress toward `M0612-B-DIM2`,
`M0612-L-MONOTONE`, `M0612-L-BALL`, `M0612-L-CYLINDER`, and
`M0612-T-SQUARED`. The frozen registry supplies only a planned prose
fingerprint for `M0612-B-DIM2`, not an exact typed declaration, so this worker
claims no whole frozen-obligation closure before integration-lane
reconciliation.

## Root Boundary

The exact root remains open at `[H2, M3, R4]`. In particular,
`RadiusSquaredObstruction` quantifies over every finite coordinate type, while
the new theorem fixes `Q = Fin 1`. The higher-dimensional branch
`M0612-B-HIGHER`, its symplectic-capacity construction and computations, and
the alternative compatible almost-complex and pseudoholomorphic-curve
packages still have no eligible proof body in the repository or pinned
dependency closure.

The graph-derived immediate cut therefore remains `M0612-T-SQUARED`.
`root_of_radiusSquaredObstruction` is still only a conditional composer and is
not promoted to root proof credit. The proof item is not complete.

## Validation

All commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` link to canonical pinned artifacts was reused
read-only. No `lake update`, `lake build`, dependency clone/fetch, checkout,
repair, or other `.lake` mutation was performed. Lean objects were generated
only in disposable directories under `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0612` | 0 | Rank 256; lifecycle `planned`; hard-mathlib-anchor-and-wrapper lane; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0612/check_obligation_tree.py` | 0 | `PASS THM-M-0612 obligation tree: 26 obligations, 58 typed edges`; denominator `2cad29b7...a4bc8`; the frozen root remains open M3. |
| `bash Stage1_Instances/THM-M-0612/check_proof.sh` | 0 | `Statement.lean`, `LocalEncoding.lean`, and `DimensionTwo.lean` elaborated into temporary oleans with `--trust=0 -t0`; `assert_no_sorry` and `#print sorries` reported all four new declarations sorry-free; their axiom reports were exactly `[propext, Classical.choice, Quot.sound]`; final line `PASS THM-M-0612 dimension-two proof bodies`. |
| Owned Lean prohibited-construct scan | 1 (expected) | No `sorry`, `admit`, `sorryAx`, axiom/bodyless declaration, opaque or unsafe escape, `extern`, `implemented_by`, `run_tac`, or `native_decide` was found. |
| Available pinned-package topical scan | 1 (expected) | No nonsqueezing, Gromov-width, symplectic-capacity, or pseudoholomorphic declaration exists in the pinned package sources. |
| Lean, Lake, and dependency identity checks | 0 | Lean 4.29.0 commit `98dc76e...16740`; Lake 5.0.0; mathlib `8a178386...ea95`, tree `bdc39a31...1c2b`; dependency worktree clean. |
| JSON parsing, receipt invariants, and scoped whitespace checks | 0 | The structured receipt and self-test packet parse; source hashes, base identity, declaration list, unchanged root vector, open cut, changed paths, and status boundary agree; no whitespace errors. |

The first failed proof gate is the higher-dimensional nonlinear branch. A
future execution must either implement the compatible capacity or
pseudoholomorphic packages without placeholders, or integrate an immutable
compatible terminal proof with exact-type and provenance checks. The master
must also reconcile the planned `M0612-B-DIM2` fingerprint with this exact
declaration before assigning whole-node credit. This target has accumulated
far more than five unresolved root rechecks while the authoritative proof item
still records `attempts: 0` and no children. Rev-5.6 section 10.2 therefore
requires dependency-legal child nodes rather than another undifferentiated
root retry. The natural next child is `M0612-B-HIGHER`, with its capacity and
pseudoholomorphic dependencies split below it.

This packet proposes only `[_]` for a self-tested partial proof contribution.
It does not establish the universal root, proof-phase completion, accepted
state, audit completion, validation, release, master acceptance, or theorem
completion.
