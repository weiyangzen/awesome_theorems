# THM-M-0605 proof phase: blocked at base 33a5b0d6

Item: `S56-M-0605-PROOF`

Intent: `prove`

Recorded: `2026-07-15T13:06:50+08:00`

Base revision: `33a5b0d654c92a894e155f5385edaae684091bb0`

Base tree: `74ed89524afb3c118e31a7fce9b5763fee26b180`

Worker checkout: Stage1 rev-5.6 worker automation clone `slot62`

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
`Mathlib.Geometry.Manifold.PoincareConjecture`. Batteries elaborates this
command inside `withoutModifyingEnv`; the temporary axiom is discarded. A
direct trust-zero import probe reports its name as unknown. The scoped
retained-body search found no proof-bearing Milnor-sphere, clutching,
homotopy-sphere, Eells-Kuiper, Kervaire-Milnor, or equivalent declaration.
Mathlib's bordism module explicitly leaves actual bordisms and bordism groups
as future work, so it also cannot supply the frozen smooth-obstruction branch.

The preceding blocker packet at base `9e9b288b` has been integrated, but the
canonical Lean sources, registry, typed graphs, audit, validation
specifications, target manifest, toolchain, and dependency manifest remain
byte-identical. Their hashes are bound in the paired JSON record, so the
mathematical blocker persists at the current base.

## Validation

All commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink was treated as read-only. No `lake update`,
`lake build`, dependency clone/fetch, checkout repair, network request, or
dependency mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0605` | 0 | Rank 643; planned; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0605/check_anchor_audit.py` | 0 | Exact marker, dependency pins, discard semantics, and the M4 boundary passed. |
| `python3 Stage1_Instances/THM-M-0605/check_obligation_tree.py` | 0 | 19 obligations and 90 typed edges passed; denominator `c6e29bccc0135529afc98b27c38f6c5265449f1fd054602ec55fe9d9e5b6e5b7`; root remains open M4. |
| Three prescribed `cd Formalizations/Lean && lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-0605/<file>.lean` invocations | 1 | Each failed before Lean because the shared manifest-pinned `flt-regular` checkout cannot resolve `HEAD`; it points at the missing ref `refs/heads/.invalid`. The worker did not repair the shared cache. |
| Direct Lean 4.29.0 with a read-only `LEAN_PATH` assembled from existing root/package `build/lib/lean` directories | 0 | `Statement.lean`, `ObligationTree.lean`, and `AnchorAudit.lean` elaborated at `--trust=0 -t0`; composer axioms were exactly `propext`, `Classical.choice`, and `Quot.sound`. This is narrow nonrelease fallback evidence, not a successful prescribed Lake replay. |
| Direct trust-zero import probe of the `proof_wanted` name | 1 | Expected negative evidence: `Unknown identifier`. |
| Scoped retained-body search | 0 | Hits were confined to the discarded marker, this dossier, THM-M-0578's duplicate statement/composer, and metadata probes. |
| Pinned construction-package search | 1 | Expected no-match exit: no retained clutching, homotopy-sphere, Milnor-sphere, Eells-Kuiper, or Kervaire-Milnor package was found. |
| Pinned nondiffeomorphism-signature search | 0 | The only matching results were the discarded exotic-seven-sphere and exotic-R4 `proof_wanted` targets. |
| Prohibited-device scan of the checked Lean surface | 1 | Expected no-match exit: no `sorry`, `admit`, `sorryAx`, bodyless declaration, unsafe theorem, or equivalent proof device was found. |
| Scoped diff from base `9e9b288b` | 0 | No proof input, pin, or target-manifest input changed. |

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
exact target with complete dependency and license evidence. The cache-owning
lane must also restore the already manifest-pinned `flt-regular` checkout
before the prescribed `lake env` checks can be replayed.

This is current-base blocker evidence, not a proof receipt. It does not
satisfy `S56-M-0605-PROOF`, promote scheduler state, close an obligation, or
support audit or theorem completion. Because the assigned proof phase is not
genuinely self-tested as complete, `.stage1-worker-selftest.json` remains
absent.
