# THM-M-0605 proof phase: blocked at base 89bb36df

Item: `S56-M-0605-PROOF`

Intent: `prove`

Recorded: `2026-07-15T09:14:56+08:00`

Base revision: `89bb36df208fff9659fdeac0e10edeea0248e711`

Base tree: `02e87afb7859de6cf58c19f6cb64715c2e7d7513`

Worker checkout: Stage1 rev-5.6 worker automation clone `slot66`

## Verdict

`blocked`. No placeholder-free Lean 4 proof body for the exact target
`Stage1.THM_M_0605.ExoticSevenSphereExists` is present in the repository or
the pinned dependency closure. No proof body or obligation closure was added.
The proof item stays `[ ]`, the lifecycle stays `planned`, the root vector
stays `[H1, M4, R3]`, and audit completion, root closure, validation, release,
and theorem completion remain false.

The immediate frozen root cut is `M0605-T-WITNESS`: a smooth
seven-manifold, a homeomorphism to the standard seven-sphere, and an
`IsEmpty Diffeomorph` certificate. The first unavailable construction is
`M0605-C-BUNDLE`, the selected Milnor 3-sphere bundle over the 4-sphere with
its clutching and characteristic data. The downstream total-space,
homotopy-sphere, topological-identification, bounding-manifold,
smooth-obstruction, standard-comparison, nondiffeomorphism, and witness
packages also remain open.

The checked theorem `exoticSevenSphereExists_of_witness` is only the frozen
child-to-parent composition: it consumes the complete witness package and
constructs none of it. The anchor theorem transports only the exact statement
shape. Choosing the standard sphere itself cannot work because its identity
map is a diffeomorphism, contradicting the required `IsEmpty` certificate.
Assuming any missing witness component or returning only this conditional
composer would be a placeholder or substituted theorem and was not done.

Pinned mathlib contains the matching signature only as
`proof_wanted exists_homeomorph_isEmpty_diffeomorph_sphere_seven` in
`Mathlib.Geometry.Manifold.PoincareConjecture`. Batteries discards that
temporary marker, and a direct trust-zero import probe reports its name as
unknown. The scoped retained-body search found no proof-bearing Milnor-sphere,
clutching, Eells-Kuiper, Kervaire-Milnor, or equivalent declaration.

Since the preceding slot66 recheck at base `71bcc40e`, only that blocker
packet was added under this target. The statement, conditional composition,
registry, typed graphs, anchor audit, validation specifications, target
manifest, Lean toolchain, and dependency manifest did not change. Their
hashes remain bound in the paired JSON record, so the blocker persists at the
current base.

## Validation

All commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts was reused
read-only. No `lake update`, `lake build`, dependency clone/fetch, network
request, or dependency mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0605` | 0 | Rank 643; planned; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0605/check_anchor_audit.py` | 0 | Exact marker, dependency pins, discard semantics, and the M4 boundary passed. |
| `python3 Stage1_Instances/THM-M-0605/check_obligation_tree.py` | 0 | 19 obligations and 90 typed edges passed; denominator `c6e29bccc0135529afc98b27c38f6c5265449f1fd054602ec55fe9d9e5b6e5b7`; root remains open M4. |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0605/Statement.lean` | 0 | The exact canonical target elaborated and printed. |
| `cd Formalizations/Lean && lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-0605/ObligationTree.lean` | 0 | The conditional composition elaborated; axioms were exactly `propext`, `Classical.choice`, and `Quot.sound`. |
| `cd Formalizations/Lean && lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-0605/AnchorAudit.lean` | 0 | The exact packaging transport elaborated and the retained-marker rejection check passed. |
| Direct trust-zero import probe of the `proof_wanted` name | 1 | Expected negative evidence: `Unknown identifier`. |
| Scoped retained-body search | 0 | Hits were confined to the discarded marker, this dossier, THM-M-0578's duplicate statement/composer, and metadata probes. |
| Pinned construction-package search | 1 | Expected no-match exit: no retained clutching, homotopy-sphere, Milnor-sphere, Eells-Kuiper, or Kervaire-Milnor package was found. |
| Prohibited-device scan of the checked Lean surface | 1 | Expected no-match exit: no `sorry`, `admit`, `sorryAx`, axiom declaration, unsafe theorem, or equivalent proof device was found. |
| Scoped diff from base `71bcc40e` | 0 | No proof input, pin, or target-manifest input changed; only the preceding slot66 blocker packet was added under this target. |

The negative probe was a disposable file containing:

```lean
import Mathlib.Geometry.Manifold.PoincareConjecture
#check exists_homeomorph_isEmpty_diffeomorph_sphere_seven
```

It exited 1 with `Unknown identifier`, confirming that the source marker is
not an importable theorem.

## Retry condition

Provide placeholder-free implementations of the frozen Milnor bundle and all
dependent topological and smooth-obstruction packages. Alternatively,
integrate an immutable compatible Lean 4 proof-bearing declaration of the
exact target with complete dependency and license evidence, then rerun the
exact-type, trust, provenance, and composition checks.

This is current-base blocker evidence, not a proof receipt. It does not
satisfy `S56-M-0605-PROOF`, promote scheduler state, close an obligation, or
support audit or theorem completion. Because the assigned phase is not
genuinely self-tested as complete, `.stage1-worker-selftest.json` remains
absent.
