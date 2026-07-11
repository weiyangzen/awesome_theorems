# THM-M-1025 rev-5.6 intake

This is the `planned` instance for stable distributions. The repository source says only
"characteristics of stable distributions" (`稳定分布的特征`). That wording identifies a theorem
family, not a unique proposition: it can refer to the convolution/scaling definition, the
classification by characteristic functions, or a parameterization theorem with a particular
location convention. This intake preserves that uncertainty instead of selecting a convenient
formula silently. The screened `已验证` label supplies no proof credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Literal root | A characterization of one-dimensional real stable probability laws | The source does not state which characterization or parameter convention |
| Probabilistic side | Stability of a Borel probability law under convolution powers, with positive scale and real shift | Strict versus non-strict stability and admissible scale laws must be fixed |
| Analytic side | A characteristic-function classification with stability index, skewness, scale, and location parameters | The `alpha = 1` branch and Fourier/location conventions must be explicit |
| Branches | `0 < alpha < 2`, `alpha = 1`, `alpha = 2`, symmetric, one-sided, and degenerate boundaries | Which are theorem branches versus corollaries remains open |
| Transports | Random-variable versus probability-law statements and alternate standard parameterizations | No equivalence or transport is credited at intake |
| Foundations | Lean 4 kernel, pinned mathlib, and explicit probability/measure/integration policy | Imports, toolchain, axioms, and transitive TCB remain open |

A mere definition of stability, the Gaussian case alone, or a generalized central limit theorem is
not a substitute. Multivariate stable laws and domains of attraction are excluded from this target;
the adjacent `THM-M-1026` owns the latter family.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H2, M4, R3]`. The first failed theorem gate is
exact-statement selection: the available source metadata does not determine the quantified claim or
the characteristic-function convention. Consequently there is no canonical Lean expression,
environment fingerprint, checked transport, or mutation evidence. The theorem is not complete.

## Open task DAG

`STATEMENT -> ANCHOR_AUDIT -> OBLIGATION_TREE -> PROOF -> VALIDATION -> RELEASE`.
Each dependent node remains open and requires master acceptance of this intake. The ambiguity and
the retry conditions for statement work are recorded in `source_statement_crosswalk.md`.

## Validation

The commands in `validation.md` establish target membership, standard consistency, JSON syntax,
dossier-local references, and formatting only. This phase introduces no Lean declaration and
claims no kernel result.
