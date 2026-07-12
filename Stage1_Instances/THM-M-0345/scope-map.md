# Scope map

## Included topic boundary

- A complex- or real-valued function on a source-specified Euclidean domain.
- A source-specified Fourier transform, including character, measure, sign, and `2*pi` convention.
- Quantitative Gaussian decay hypotheses on the function and its Fourier transform.
- The exact threshold conclusion: vanishing in the supercritical case and, only if the selected
  source includes it, classification by a Gaussian at the critical threshold.
- All regularity, measurability, integrability, and dimensional hypotheses required by the source.

## Ambiguities to resolve at statement freeze

The repository record does not decide among materially different formulations:

1. Pointwise bounds `|f x| <= C exp (-a x^2)` and `|Fourier f y| <= C exp (-b y^2)` on `R`.
2. Bounds with separate constants, big-O notation, or almost-everywhere representatives.
3. Weighted `L2` integrability formulations rather than pointwise Gaussian bounds.
4. Higher-dimensional formulations on `R^n` or finite-dimensional inner-product spaces.
5. Only the strict-threshold vanishing result versus a theorem also classifying the equality case.

The numerical threshold changes with the Fourier convention. The statement phase must inspect an
immutable source and freeze the domain, codomain, transform normalization, ordered binders, decay
parameters and constants, strict/critical inequalities, regularity assumptions, and equality
conclusion. It must also decide whether equality is literal, almost everywhere, or in an `L2`
quotient and whether the zero function is included in the critical classification.

## Explicit exclusions

- The Heisenberg variance uncertainty principle (`THM-M-0344`) as a substitute.
- The Fourier transform of a Gaussian alone; it establishes the shape of an extremizer but not the
  rigidity or vanishing implication of Hardy's theorem.
- Paley-Wiener, Cowling-Price, Beurling, or support-based uncertainty principles as substitutes.
- A tautological statement obtained by assuming the desired zero/Gaussian conclusion.
- The repository label `已验证` as human-source or machine-proof evidence.

No canonical Lean target is frozen at intake because the source record does not identify a
normalized proposition.
