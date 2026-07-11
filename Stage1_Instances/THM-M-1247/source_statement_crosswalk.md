# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Euclidean `L2` inequality in dimension `n >= 5` | F. Rellich, *Halbbeschraenkte Differentialoperatoren hoeherer Ordnung*, Proceedings of the International Congress of Mathematicians, Amsterdam 1954, vol. III, pp. 243-250 | No declaration has been accepted | Primary historical source identified bibliographically; theorem/page premise and errata audit remain open, so only `H1` |
| Sharp constant `(n(n-4)/4)^2` | E. B. Davies and A. M. Hinz, *Explicit constants for Rellich inequalities in Lp(Omega)*, Mathematische Zeitschrift 227 (1998), pp. 511-523, DOI `10.1007/PL00004387` | A future local exact statement over `EuclideanSpace Real (Fin n)` | Modern source located for discovery; exact theorem numbering, hypotheses, normalization, and corrections still require audit |
| Test class avoiding the origin | conventional `C_c^infinity(R^n \\ {0})` formulation in the cited literature | smoothness plus compact support plus `0` outside support | The equivalence to any eventual mathlib test-function encoding must be checked, not assumed |
| Laplacian and weighted integrals | Euclidean Laplacian and Lebesgue measure | mathlib iterated derivative/Laplacian and Bochner integral APIs, still unknown | No API anchor, type, import, revision, or elaboration is credited at intake |
| Rellich-Kondrachov compact embedding | not a component of this inequality | repository references to `abenenson/rellich-kondrachov` | Explicitly excluded: similarity of names supplies no statement or proof evidence |

The manifest contains only the name `Rellich inequality`, so variant selection is a material scope
decision. The frozen root is the classical scalar Euclidean inequality above. Weighted, boundary,
manifold, vector-valued, `Lp`, and compact-embedding results may later be comparison candidates but
cannot substitute for it.

No source has an immutable local content hash or accepted node-by-node premise crosswalk yet, and no
`H0` claim is made. The source audit must obtain stable copies, pinpoint theorem statements and
normalizations, check errata, and receive independent review. The statement phase must then elaborate
the exact binder order and types, serialize the normalized expression, and mutation-test dimension,
support, smoothness, singular weight, Laplacian order, inequality direction, and sharp constant.
