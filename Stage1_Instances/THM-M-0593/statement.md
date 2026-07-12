# Exact statement receipt

Item: `S56-M-0593-STATEMENT`  
Theorem: `THM-M-0593`  
Base revision: `58fdfa878cd8184113e4aca370fee8a6b8e375c2`

## Source selection and scope

The canonical claim is the smooth specialization of Arthur Sard's original Euclidean-region
theorem, not the broader manifold paraphrase provisionally used at intake. The inspected source is
Arthur Sard, *The measure of the critical values of differentiable maps*, Bulletin of the AMS 48
(1942), 883-890, AMS scan SHA-256
`9ccd011bf9a623a3fac2f27a2b3ce1ad9687b20944a7b0b64e04deffff1efca8`.

Pages 883-884 define a map from a region `R` in Euclidean `m`-space to Euclidean `n`-space, a
critical point as one where the first-derivative matrix has less than maximum rank, a critical
value as its image, and `n`-nullity as zero `n`-dimensional Hausdorff-Saks measure, equal to outer
Lebesgue measure in `n`-space. Theorems 4.1 (p. 885) and 7.2 (p. 889) together give null critical
values for all dimension relations. Their finite differentiability conditions are implied by the
repository's stated smoothness hypothesis. The paper does not state a manifold theorem, so no
manifold or boundary claim is silently added.

For `m ≥ n`, the paper's less-than-maximum-rank definition is exactly nonsurjectivity. For `m < n`,
the modern differential-topology convention makes every point critical, while Sard's Theorem 4.1
proves the stronger needed dimensional fact: the whole image is `m`-null and hence `n`-null. The
canonical target therefore uses the uniform modern nonsurjectivity predicate across all dimensions;
the original rank-stratified formulation is not claimed as a checked alternate Lean encoding here.

## Frozen Lean target

The authoritative expression is `Stage1Instances.THMM0593.SardTarget` in `Statement.lean`:

```lean
∀ (m n : ℕ) (f : EuclideanSpace ℝ (Fin m) → EuclideanSpace ℝ (Fin n))
    (R : Set (EuclideanSpace ℝ (Fin m))),
  IsOpen R → ContDiffOn ℝ (⊤ : ℕ∞) f R →
    (volume : Measure (EuclideanSpace ℝ (Fin n))) (f '' criticalPointsOn f R) = 0
```

Here `criticalPointsOn f R` is exactly
`{x | x ∈ R ∧ ¬ Function.Surjective (fderiv ℝ f x)}`. The ordered binders expose both dimensions,
the globally represented map, and its open region. Smoothness is required only on `R`. The target
uses the pinned Euclidean `volume`, the Lebesgue/Haar measure on the codomain. It includes zero
dimensions and the empty open region; it excludes boundaries, corners, manifolds, merely finite
regularity, critical points outside `R`, and nullity for any different measure.

Minimal imports, determined by deletion testing, are:

```lean
import Mathlib.Geometry.Euclidean.Volume.Measure
import Mathlib.Analysis.Calculus.ContDiff.Defs
```

Deleting the second import makes `fderiv` and `ContDiffOn` unknown. Deleting the first leaves no
usable Euclidean `volume`/`Measure` surface. No theorem body, axiom, `sorry`, or placeholder occurs
in the canonical file: this phase elaborates a proposition only and claims no proof closure.

The environment fingerprint is Lean `4.29.0` commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, mathlib commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, toolchain-file SHA-256
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`, manifest SHA-256
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`, and canonical source
SHA-256 `dd2a4da4f6cb0b0723a656e627378047834867641d63c6e5a8a0255108aed3bb`.

## Mutation evidence

Each mutation file assumes the exact target and tries to derive a proposition-changing variant.
Every command exits 1 at the displayed exact type mismatch:

| Mutation | Expected failure |
|---|---|
| `MutationRemovedSmoothness.lean` | the exact target still requires `ContDiffOn` |
| `MutationCriticalPoints.lean` | nullity of critical values does not type-match nullity of `f '' R` |
| `MutationBoundary.lean` | deleting the open-region hypothesis leaves an unapplied `IsOpen R` premise |
| `MutationTargetMeasure.lean` | `volume` nullity does not type-match `(n+1)`-Hausdorff nullity |

These are statement-identity tests, not mathematical independence proofs. A changed binder scope is
covered by `MutationBoundary.lean`: moving from an open-region binder to an arbitrary set without
the openness premise cannot be obtained by applying the frozen expression.

## Validation and status boundary

All commands ran from `Formalizations/Lean` against the existing pinned `.lake` tree; no dependency
mutation or fetch was performed.

| Command | Result |
|---|---|
| `lake env lean ../../Stage1_Instances/THM-M-0593/Statement.lean` | exit 0; `Stage1Instances.THMM0593.SardTarget : Prop` |
| `lake env lean ../../Stage1_Instances/THM-M-0593/MutationRemovedSmoothness.lean` | exit 1; expected `ContDiffOn` function but a measure equality was required |
| `lake env lean ../../Stage1_Instances/THM-M-0593/MutationCriticalPoints.lean` | exit 1; `f '' criticalPointsOn f R` mismatched `f '' R` |
| `lake env lean ../../Stage1_Instances/THM-M-0593/MutationBoundary.lean` | exit 1; unapplied `IsOpen R` and `ContDiffOn` premises |
| `lake env lean ../../Stage1_Instances/THM-M-0593/MutationTargetMeasure.lean` | exit 1; `volume` mismatched `μH[n+1]` |
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 1546 uniform-L0 targets and all assurance groups consistent |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0593` | exit 0; rank 633, planned, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-0593 .stage1-worker-selftest.json` | exit 0; no output |

Statement status is self-tested and proposed for master acceptance. The phase establishes exact
elaboration and source scope only. It does not establish `H0`, an anchor audit, an obligation tree,
a proof of `SardTarget`, `M0`, audit completion, or theorem completion.
