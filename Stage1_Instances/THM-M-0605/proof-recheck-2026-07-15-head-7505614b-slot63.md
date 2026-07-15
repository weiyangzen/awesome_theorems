# THM-M-0605 proof phase: blocked at base 7505614b

Item: `S56-M-0605-PROOF`

Intent: `prove`

Recorded: `2026-07-15T14:11:52+08:00`

Base revision: `7505614b75de56cf10bbd196a4aaa0ca2a117064`

Base tree: `730e162a2133e4a077d764043b5e722c1f7feb39`

Worker checkout: Stage1 rev-5.6 automation clone `slot63`

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

The checked theorem `exoticSevenSphereExists_of_witness` is only conditional
child-to-parent composition: it consumes the complete witness package and
constructs none of it. The anchor theorem only transports the exact statement
shape. Treating either theorem as a root proof, assuming a witness component,
or using the standard sphere despite its identity diffeomorphism would be a
placeholder or substituted theorem and was not done.

Pinned mathlib contains the matching signature only as
`proof_wanted exists_homeomorph_isEmpty_diffeomorph_sphere_seven` in
`Mathlib.Geometry.Manifold.PoincareConjecture`. Batteries elaborates the
temporary helper axiom inside `withoutModifyingEnv`, then discards it. A fresh
trust-zero import probe reports the name as unknown. Scoped searches found no
retained Milnor-sphere, clutching, homotopy-sphere, Eells-Kuiper,
Kervaire-Milnor, or equivalent proof-bearing declaration. Mathlib's bordism
module also states that actual bordisms and bordism groups remain future work,
so the frozen smooth-obstruction branch is unavailable.

Since the preceding slot63 recheck at base `9bce865a`, only that blocker
packet was added under this target. The statement, conditional composition,
anchor transport, registry, typed graphs, validation specifications, target
manifest, Lean toolchain, and dependency manifest are byte-identical. The
cache-owner has restored the already pinned `flt-regular` checkout, so all
prescribed narrow `lake env lean` checks now replay successfully; this removes
the prior environment-only failure but not the mathematical proof blocker.

## Validation

All commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts was reused
read-only. No `lake update`, `lake build`, dependency clone/fetch, checkout
repair, network request, or dependency mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0605` | 0 | Rank 643; planned; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0605/check_anchor_audit.py` | 0 | Exact pinned marker, Batteries discard semantics, and the M4 boundary passed. |
| `python3 Stage1_Instances/THM-M-0605/check_obligation_tree.py` | 0 | 19 obligations and 90 typed edges passed; denominator `c6e29bccc0135529afc98b27c38f6c5265449f1fd054602ec55fe9d9e5b6e5b7`; root remains open M4. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `cd Formalizations/Lean && lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-0605/Statement.lean` | 0 | The exact canonical target elaborated; output was 15,602 bytes with SHA-256 `b45c5a871dc9b5862356b1fd2540c8d770d8b4488230005303cc6b41f7b33469`. |
| `cd Formalizations/Lean && lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-0605/ObligationTree.lean` | 0 | Conditional composition elaborated; axioms were exactly `propext`, `Classical.choice`, and `Quot.sound`. |
| `cd Formalizations/Lean && lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-0605/AnchorAudit.lean` | 0 | Exact packaging transport elaborated and the retained-marker rejection check passed. |
| Direct trust-zero import probe of the `proof_wanted` name | 1 | Expected negative evidence: `Unknown identifier`. |
| Scoped retained-body search | 0 | 27 hits in 11 files were confined to the discarded marker, this dossier, THM-M-0578's duplicate statement/composer, and metadata probes; no eligible terminal body was found. |
| Pinned construction-package search | 1 | Expected no-match exit: no retained clutching, homotopy-sphere, Milnor-sphere, Eells-Kuiper, or Kervaire-Milnor package was found. |
| Prohibited-device scan of the checked Lean surface | 1 | Expected no-match exit: no `sorry`, `admit`, `sorryAx`, `native_decide`, bodyless declaration, unsafe declaration, or equivalent proof escape was found. |
| Scoped diff from base `9bce865a` | 0 | No proof source, frozen architecture input, target-manifest input, toolchain, or dependency manifest changed; only the preceding blocker packet was added under this target. |
| `git diff --check -- Stage1_Instances/THM-M-0605 .stage1-worker-selftest.json` | 0 | No whitespace errors. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion manifest is absent because the assigned proof phase is incomplete. |

The direct negative probe used a disposable file containing:

```lean
import Mathlib.Geometry.Manifold.PoincareConjecture
#check exists_homeomorph_isEmpty_diffeomorph_sphere_seven
```

It exited 1 with `Unknown identifier`, confirming that the exact source marker
is not an importable theorem.

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
