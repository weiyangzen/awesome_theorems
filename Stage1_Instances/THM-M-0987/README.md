# THM-M-0987 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the central limit theorem target. It does not
inherit proof credit or accepted state from the legacy `S1-M-267` Lean file or its historical build.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Human root | Normal convergence of suitably centered and scaled sums of independent random variables | The source wording is a theorem-family label and does not specify a unique exact theorem |
| Candidate exact branch | One-dimensional, real-valued, identically distributed variables with finite second moment | Candidate only; exact elaboration and transport belong to the statement phase |
| Assumptions | probability spaces, measurability, independence, identical laws, finite second moment | None is silently omitted from the formal candidate |
| Conclusion | convergence in distribution to the Gaussian law with variance `Var (X 0)` | Normalization and variance-zero behavior require statement checks |
| Excluded variants | triangular-array/Lindeberg-Feller, multivariate, martingale, functional/Donsker, Berry-Esseen | Separate family members, not consequences credited to this intake |
| Foundations | Lean 4 kernel and pinned mathlib | Exact toolchain, dependency, foundation, and TCB fingerprints remain open |

The legacy wrapper in `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_267.lean` is discovery input.
It identifies a plausible mathlib-backed i.i.d. branch but explicitly says that the public wording is
broader. This intake preserves that mismatch rather than substituting the narrower theorem.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H2, M3, R3]`. The first failed theorem gate is
the exact-statement gate: the historical source line does not determine ordered binders,
hypotheses, normalization, or which CLT variant is canonical. The dependent statement phase must
either justify an exact scoped root from primary sources or retain an explicit family/root split.
No proof, audit completion, or theorem completion is claimed.

Validation commands and their results are recorded in `validation.md`.
