# THM-M-0605 proof phase: blocked at base d8f84d54

Item: `S56-M-0605-PROOF`

Intent: `prove`

Recorded: `2026-07-15T17:37:09+08:00`

Base revision: `d8f84d5418027a70d6b46b6bdd4eae8b03222636`

Base tree: `c940a8fbfbffa31fd76003aabf250b486fa8a04f`

Worker checkout: Stage1 rev-5.6 automation clone `slot53`

## Verdict

`blocked`. No placeholder-free Lean 4 proof body for the frozen target
`Stage1.THM_M_0605.ExoticSevenSphereExists` is present in the repository or
the pinned dependency closure. No proof body or obligation closure was added.
The proof item stays `[ ]`, lifecycle stays `planned`, the root vector stays
`[H1, M4, R3]`, and audit completion, root closure, validation, release, and
theorem completion remain false.

The first failed gate is prerequisite exact-statement and anchor fidelity. The
frozen `SmoothSevenManifold` requires `IsManifold (𝓡 7) ω`, while the actual
pinned mathlib `proof_wanted` marker requires `IsManifold (𝓡 7) ∞`.
Pinned mathlib documents `ω` as analytic and `∞` as smooth. Trust-zero probes
prove `ω ≠ ∞` and infer analytic-to-smooth, but smooth-to-analytic instance
synthesis fails. `AnchorAudit.lean` defines a local marker shape with `ω` and
proves packaging equivalence only to that analytic shape. It does not establish
the recorded exact transport to the actual smooth source marker.
`check_anchor_audit.py` passes because it checks the marker name and `IsEmpty`
tail, but never checks the source marker's `IsManifold` binder.

Independently, the proof-body blocker remains. The immediate frozen root cut is
`M0605-T-WITNESS`: a particular manifold, a homeomorphism to the standard
seven-sphere, and an `IsEmpty Diffeomorph` certificate. The first unavailable
construction is `M0605-C-BUNDLE`, the selected Milnor 3-sphere bundle over the
4-sphere with its clutching and characteristic data. The total-space,
homotopy-sphere, topological-identification, bounding-manifold,
smooth-obstruction, standard-comparison, nondiffeomorphism, and witness
packages also remain open. The stronger analytic target additionally needs an
analytic construction or a justified smooth-to-analytic transport.

The checked theorem `exoticSevenSphereExists_of_witness` is conditional
assembly only: it consumes the complete witness and constructs none of it. A
trust-zero probe rejects the standard sphere as a shortcut because its smooth
identity diffeomorphism contradicts the required `IsEmpty`. Assuming any
missing component or returning only the conditional composer would be a
placeholder or substituted theorem and was not done.

Pinned mathlib contains the nearby smooth signature only as
`proof_wanted exists_homeomorph_isEmpty_diffeomorph_sphere_seven`.
`proof_wanted` elaborates a temporary helper axiom inside
`withoutModifyingEnv` and discards it. A direct trust-zero import probe reports
the name as unknown. Repository and pinned-source searches found no retained
Milnor-sphere, clutching, homotopy-sphere, Eells-Kuiper, Kervaire-Milnor, or
equivalent terminal proof body.

The mismatch-aware packet at base `a4326e8e` was integrated in the current
base. From the earlier mismatch evidence through this base, the canonical Lean
sources, frozen architecture inputs, target manifest, toolchain, and dependency
manifest are byte-identical. Only blocker packets changed under this target,
so both blockers persist.

## Validation

All commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts was reused
read-only. No `lake update`, `lake build`, dependency clone/fetch, checkout
repair, network request, or dependency mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0605` | 0 | Rank 643; planned; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0605/check_anchor_audit.py` | 0 | The existing validator reported an exact marker, but source inspection shows it does not check the mismatched `IsManifold` binder; this is not exact-transport evidence. |
| `python3 Stage1_Instances/THM-M-0605/check_obligation_tree.py` | 0 | 19 obligations and 90 typed edges passed; denominator `c6e29bccc0135529afc98b27c38f6c5265449f1fd054602ec55fe9d9e5b6e5b7`; root remains open M4. |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 at commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake 5.0.0. |
| `cd Formalizations/Lean && lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-0605/Statement.lean` | 0 | Frozen analytic target elaborated; output was 15,602 bytes with SHA-256 `b45c5a871dc9b5862356b1fd2540c8d770d8b4488230005303cc6b41f7b33469`. |
| Same command for `ObligationTree.lean` | 0 | Conditional composition elaborated; axioms were exactly `propext`, `Classical.choice`, and `Quot.sound`. |
| Same command for `AnchorAudit.lean` | 0 | Local analytic-shape transport elaborated and retained-name rejection passed; it did not compare to the actual smooth marker binder. |
| Trust-zero `ω`/`∞` distinction probe | 0 | Lean proved `(ω : WithTop ℕ∞) ≠ ∞`; axioms were `propext` and `Quot.sound`. |
| Trust-zero analytic-to-smooth instance probe | 0 | `[IsManifold (𝓡 7) ω M]` synthesized `IsManifold (𝓡 7) ∞ M`. |
| Trust-zero smooth-to-analytic instance probe | 1 | Expected negative evidence: `[IsManifold (𝓡 7) ∞ M]` could not synthesize `IsManifold (𝓡 7) ω M`. |
| Direct trust-zero import probe of the `proof_wanted` name | 1 | Expected negative evidence: `Unknown identifier exists_homeomorph_isEmpty_diffeomorph_sphere_seven`. |
| Trust-zero standard-sphere shortcut probe | 0 | `Diffeomorph.refl (𝓡 7) StandardSevenSphere ∞` refuted `IsEmpty`; axioms were exactly `propext`, `Classical.choice`, and `Quot.sound`. |
| Scoped retained construction-package search | 1 | Expected no-match exit: pinned mathlib and Batteries contain no retained clutching, homotopy-sphere, Milnor-sphere, Eells-Kuiper, or Kervaire-Milnor package. |
| Prohibited-device scan of the checked Lean surface | 1 | Expected no-match exit: no `sorry`, `admit`, `sorryAx`, `native_decide`, `implemented_by`, bodyless declaration, unsafe declaration, or equivalent proof escape occurs. |
| Scoped diff from mismatch evidence base `51c2828e` | 0 | No canonical Lean source, frozen architecture input, target manifest, toolchain, or dependency manifest changed; only blocker packets were added under this target. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion manifest is absent because the assigned proof phase is incomplete. |

## Retry condition

First reopen the statement and anchor phases. Either deliberately freeze the
infinity-smooth target matching the source marker, or justify the stronger
analytic target and provide a checked transport. Then implement the Milnor
bundle and all dependent topological and smooth-obstruction packages without
placeholders, or integrate an immutable compatible proof-bearing declaration
for the exact corrected target. Rerun exact-type, trust, provenance, and
composition checks afterward.

This is current-base proof-phase blocker evidence, not a proof receipt. It does
not satisfy `S56-M-0605-PROOF`, repair or accept a prerequisite node, promote
scheduler state, close any obligation, or support theorem completion. Because
the assigned phase is not genuinely complete, `.stage1-worker-selftest.json`
remains absent.
