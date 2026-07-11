# Source-statement crosswalk

## Primary-source anchors

The independent original proofs are attributed to:

- Ju. I. Manin, "Parabolic points and zeta functions of modular curves", *Mathematics of the USSR-Izvestiya* 6 (1972), 19-64 (English translation of the 1972 Russian publication), DOI `10.1070/IM1972v006n01ABEH001867`.
- V. G. Drinfeld, "Two theorems on modular curves", *Functional Analysis and Its Applications* 7 (1973), 155-156 (English translation), DOI `10.1007/BF01078845`.

These bibliographic anchors identify the intended theorem family, but the exact original theorem labels, printed pages, hypotheses, translation differences, and errata have not yet received page-level inspection and independent review. Therefore this intake is `H1`, not `H0`.

## Statement crosswalk

| Intake component | Source-side mathematical role | Disposition |
|---|---|---|
| congruence modular curve | curve on which parabolic/cuspidal points live | included; exact generality to audit |
| cusps | parabolic boundary points | included |
| degree-zero cuspidal divisor | integral combination of cusps with coefficient sum zero | included |
| Jacobian / degree-zero Picard class | Abel-Jacobi target of the divisor | included; encoding transport open |
| torsion | some positive integer multiple of the class is zero | included |
| pairwise difference | generator formulation `[c-d]` | included; equivalence proof open |

## Metadata correction and provenance boundary

The generated Stage1 gloss says "properties of Heegner points on elliptic curves". That describes a different subject and cannot source this target. The theorem name and the legacy Lean commentary instead point to the cuspidal-divisor torsion theorem; this dossier freezes that standard claim and records the metadata discrepancy for later correction by an authorized integration lane.

The legacy file `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_043.lean` supplies an abstract statement-shape discovery lead only. Its user-supplied compactified curve and divisor-class map do not construct the source objects and receive no statement or proof credit.

## Open H-gate work

Inspect stable scans of both originals, record exact theorem labels/pages and scope, resolve whether the most faithful root is stated for all congruence subgroups or a specific modular-curve family, check published errata and translation variance, and obtain an independent source-to-canonical-statement review.
