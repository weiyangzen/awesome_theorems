# Scope map

## Included theorem family

| Surface | Provisional scope | Statement-phase decision still required |
|---|---|---|
| Manifold | closed, oriented, smooth, simply connected four-manifold `X` | exact smoothness, compactness, connectedness, and boundary conventions from the selected theorem |
| Algebraic object | integral intersection pairing on `H_2(X; Z)` modulo torsion | exact carrier, torsion quotient, unimodularity, and equivalence encoding |
| Main hypothesis | the intersection form is definite | positive-only source form versus positive/negative form using orientation reversal |
| Conclusion | integral diagonalizability; positive form equivalent to `+I` | matrix, lattice-isometry, or basis formulation and the rank-zero convention |
| Formal surface | concrete smooth-manifold, homology, fundamental-class, and cup/intersection-pairing APIs | exact minimal imports and any missing mathlib interfaces |

This scope distinguishes the famous diagonalization obstruction for smooth four-manifolds from a
classification of all smooth structures. The theorem constrains which topological intersection
forms can occur smoothly; it does not itself classify every smooth four-manifold or construct an
exotic smooth structure.

## Explicit exclusions

- The ASD moduli-space regularity, dimension, orientation, and compactification family represented
  by `THM-M-0184`.
- Donaldson polynomial invariants or the full Donaldson series.
- Freedman's topological classification theorem or an assertion that homeomorphism implies
  diffeomorphism.
- A theorem over an arbitrary supplied bilinear form with no checked construction from `X`.
- Rational or real diagonalization, which is strictly weaker than integral diagonalization.
- Indefinite intersection forms, manifolds with boundary, or arbitrary fundamental groups as silent
  broadenings of the selected classical theorem.

## Exact-statement blocker

The repository phrase does not name a theorem number or state hypotheses. The diagonalization
family is the best-supported interpretation, but the statement phase must inspect and hash a stable
primary-source copy and map each hypothesis and conclusion before freezing the Lean proposition.

