# THM-M-0605 proof phase: blocked at base 9d3f687e

Item: `S56-M-0605-PROOF`

Intent: `prove`

Recorded: `2026-07-15T15:36:38+08:00`

Base revision: `9d3f687e9bf0fe3120397744332e909472c52dfd`

Base tree: `558507d70ac5e5e38486f214a3e0ce7b33f7ae9b`

Worker checkout: Stage1 rev-5.6 automation clone `slot54`

## Verdict

`blocked`. No placeholder-free Lean 4 proof body for the frozen target
`Stage1.THM_M_0605.ExoticSevenSphereExists` is present in the repository or
the pinned dependency closure. No proof body or obligation closure was added.
The proof item stays `[ ]`, lifecycle stays `planned`, the root vector stays
`[H1, M4, R3]`, and audit completion, root closure, validation, release, and
theorem completion remain false.

This replay also found an earlier exact-statement failure. The frozen
`SmoothSevenManifold` requires `IsManifold (𝓡 7) ω`, while the actual pinned
mathlib `proof_wanted` marker requires `IsManifold (𝓡 7) ∞`. In this mathlib,
`ω` is analytic and `∞` is infinitely differentiable (smooth); a trust-zero
probe proves `ω ≠ ∞`. The existing `AnchorAudit.lean` manually changes the
marker's `∞` binder to `ω` and proves an iff only between two locally defined
analytic shapes. It therefore does not establish the claimed exact transport
to the actual marker. `check_anchor_audit.py` misses the issue because it
checks the marker name and `IsEmpty` tail, but not the manifold binder.

The proof-phase mathematical blocker independently persists. The immediate
witness cut `M0605-T-WITNESS` needs a particular manifold, a homeomorphism to
the standard seven-sphere, and an `IsEmpty Diffeomorph` certificate. The first
unavailable construction is `M0605-C-BUNDLE`, the selected Milnor 3-sphere
bundle over the 4-sphere with fixed clutching and characteristic data. The
total-space, homotopy-sphere, topological-identification, bounding-manifold,
smooth-obstruction, standard-comparison, nondiffeomorphism, and witness
packages also remain open.

The checked theorem `exoticSevenSphereExists_of_witness` is conditional
assembly only: it consumes the complete witness and constructs none of it. A
fresh trust-zero probe rejects the standard sphere as witness because its
infinity-smooth identity diffeomorphism contradicts the required `IsEmpty`.
Assuming a missing component or returning only the conditional composer would
be a placeholder or substituted theorem and was not done.

Pinned mathlib contains only the distinct smooth signature as
`proof_wanted exists_homeomorph_isEmpty_diffeomorph_sphere_seven`.
`proof_wanted` elaborates a temporary helper axiom inside
`withoutModifyingEnv` and discards it. A trust-zero import probe reports the
name as unknown. Repository-ref, pinned-source, and pinned-history searches
found no retained Milnor-sphere, clutching, homotopy-sphere, Eells-Kuiper,
Kervaire-Milnor, or equivalent terminal proof body. The mathlib history has
only marker introduction commit `041fe1fa487`, not a proof replacement.

Since the preceding recheck at base `8714972d`, only that blocker packet was
added under this target. The canonical Lean sources, frozen architecture,
target manifest, toolchain, and dependency manifest are byte-identical. Thus
the proof-body blocker persists; the omega-versus-infinity mismatch reported
here is pre-existing, not caused by the base advance.

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
| `cd Formalizations/Lean && timeout 600s lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-0605/Statement.lean` | 0 | Frozen analytic target elaborated and printed its expression; the frozen receipt identifies it as SHA-256 `b45c5a871dc9b5862356b1fd2540c8d770d8b4488230005303cc6b41f7b33469`. |
| Same command for `ObligationTree.lean` | 0 | Conditional composition elaborated; axioms were exactly `propext`, `Classical.choice`, and `Quot.sound`. |
| Same command for `AnchorAudit.lean` | 0 | Local analytic-shape transport elaborated and retained-name rejection passed; it did not compare to the actual smooth marker binder. |
| Disposable trust-zero `ω`/`∞` type probe | 0 | Lean proved `ω ≠ ∞`; mathlib documents `ω` as analytic and `∞` as smooth, and the parameterized types printed distinctly. |
| Direct trust-zero import probe of the `proof_wanted` name | 1 | Expected negative evidence: `Unknown identifier`; source SHA-256 `56696ce4376706fb604cb04d1448097c50a88e83d82d58dcd9739b37fac7c6e3`. |
| Trust-zero standard-sphere shortcut probe | 0 | Infinity-smooth `Diffeomorph.refl` refuted `IsEmpty`; axioms were exactly `propext`, `Classical.choice`, and `Quot.sound`; source SHA-256 `e87b2add8a846b23d56cd814ac2c04607be56741dcce88f4d68ed79a1ac11f1e`. |
| Scoped retained-body searches | 0 | Hits were confined to the discarded marker, this dossier, THM-M-0578's duplicate conditional dossier, and metadata probes; no eligible terminal body was found. |
| Pinned construction-package search | 1 | Expected no-match exit for clutching, homotopy-sphere, Milnor-sphere, Eells-Kuiper, and Kervaire-Milnor terms. |
| Pinned `IsEmpty Diffeomorph` search | 0 | Only discarded `proof_wanted` signatures for exotic seven-sphere and exotic R4 were found. |
| All-ref and pinned-history search | 0 | All repository refs share this base and contain no body; mathlib history contains only marker introduction commit `041fe1fa487`. |
| Prohibited-device scan of checked Lean files | 1 | Expected no-match exit: no `sorry`, `admit`, `sorryAx`, `native_decide`, bodyless declaration, unsafe declaration, or equivalent escape was found. |
| Scoped diff from `8714972d` | 0 | No proof source, architecture input, target manifest, toolchain, or dependency manifest changed; only the preceding blocker packet was added under this target. |

## Retry condition

First reopen the statement and anchor phases. Either deliberately freeze the
infinity-smooth target that matches the source marker, or justify the stronger
analytic target and supply a real checked transport. Then implement the
Milnor bundle and all dependent topological and smooth-obstruction packages
without placeholders, or integrate an immutable compatible proof-bearing
declaration for the exact corrected target. Exact-type, trust, provenance,
and composition checks must then be rerun.

This is current-base proof-phase blocker evidence, not a proof receipt. It
does not satisfy `S56-M-0605-PROOF`, repair or accept a prerequisite node,
promote scheduler state, close an obligation, or support theorem completion.
Because the assigned phase is not genuinely complete,
`.stage1-worker-selftest.json` remains absent.
