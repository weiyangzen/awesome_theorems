# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Euclidean differential Hardy inequality | E. B. Davies, *A Review of Hardy Inequalities*, in *The Maz'ya Anniversary Collection*, Vol. 2, 1999, pp. 55-67, DOI `10.1007/978-3-0348-8672-7_4` | No repo-local declaration located by intake search | Secondary review anchor only; edition/page/formula and assumptions need primary-source audit |
| Historical Hardy family | G. H. Hardy, "Note on a theorem of Hilbert", *Mathematische Zeitschrift* 6 (1920), pp. 314-317, DOI `10.1007/BF01199965` | None selected | Historical primary anchor for the family, not evidence that its statement is the PDE root selected here |
| Dimension restriction `n >= 3` | Required for the displayed sharp differential form with denominator `n-2` | Future exact Lean target | Frozen scope; not elaborated |
| Compactly supported smooth test function | Standard test-function formulation of the differential inequality | Candidate mathlib smooth/compact-support APIs require audit | Function-space encoding and all transports remain open |
| Sharp constant `4/(n-2)^2` | Standard Euclidean `L2` constant in the review literature | Future real-valued coefficient | No sharpness theorem is separately claimed; coercions remain open |

The Stage0 record gives only the Chinese gloss "singular-weight integral inequality," the PDE
category, Hardy attribution, and year 1920. Hardy's name also labels inequivalent discrete and
one-dimensional integral inequalities. The selected PDE formulation best matches the gloss and
category, but source fidelity cannot advance to `H0` until an independent audit checks a precise
formula, hypotheses, edition or file hash, and errata.

The statement phase must choose concrete mathlib representations for test functions, gradient,
Lebesgue measure, the singular value at zero, and natural-to-real coercions; elaborate the full
expression; record its environment fingerprint; and mutation-test dimension, compact support,
smoothness, coefficient, and inequality direction. No source here is machine closure evidence.
