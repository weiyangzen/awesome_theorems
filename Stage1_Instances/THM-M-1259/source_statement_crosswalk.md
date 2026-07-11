# Source-statement crosswalk

| Claim component | Human source anchor | Lean target status | Intake assessment |
|---|---|---|---|
| Bracket-generating vector fields yield a hypoelliptic second-order operator | Lars Hormander, "Hypoelliptic second order differential equations", *Acta Mathematica* 119 (1967), 147-171, DOI `10.1007/BF02392081`, especially the opening theorem family | No declaration selected | Primary source identified, but an immutable copy, exact theorem/page transcription, assumptions, and errata check are still required |
| Operator consists of squares plus lower-order/drift terms | Same 1967 paper | Lean differential-operator expression not designed | Signs, indexing, coefficient regularity, and the precise participation of `X_0` in the rank condition must be copied rather than reconstructed from memory |
| Lie brackets span all tangent directions | Same theorem family | Finite iterated-bracket/rank predicate absent | Domain, pointwise versus neighborhood form, and finite-step witnesses remain statement obligations |
| Positive Sobolev gain (subelliptic estimate) | Analytic estimate in the proof tradition of the same theorem | Sobolev/distribution formulation absent | The estimate is not automatically identical to the named root; localization, norms, gain, and lower-order remainder must be pinned |
| Smoothness of `P u` implies smoothness of `u` | Hypoellipticity conclusion of the 1967 theorem family | Distributional regularity implication absent | A future estimate-to-regularity bridge must be explicit and kernel checked |

The repository's label, `Hörmander定理(次椭圆)`, is not an exact citation. In particular,
"subelliptic" may name the estimate while the classic published theorem is commonly stated as
hypoellipticity under a bracket condition. Those formulations cannot be merged at intake. The next
phase must acquire and hash a stable primary-source artifact, transcribe the exact operator and
ordered hypotheses with a pinpoint, check corrections/errata, and then select one canonical root.

Discovery link (not an immutable evidence receipt):
<https://doi.org/10.1007/BF02392081>

No `H0`, exact-statement, mathlib-anchor, or machine-closure claim is made. The source label
`已验证` in the generated manifest remains untrusted metadata.
