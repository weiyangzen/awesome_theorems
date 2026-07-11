# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Sharp Sobolev inequality and extremals in dimension `n >= 3` | T. Aubin, “Problèmes isopérimétriques et espaces de Sobolev,” *Journal of Differential Geometry* 11 (1976), 573-598 | no declaration selected | Primary source located; exact theorem/page-premise and errata audit remain open |
| Explicit equality functions for the best Sobolev constant | G. Talenti, “Best constant in Sobolev inequality,” *Annali di Matematica Pura ed Applicata* 110 (1976), 353-372, especially the equality-function discussion on pp. 354-355 | explicit Euclidean function using `Real.rpow` and norm square | Formula family located; notation and normalization still require line-by-line reconciliation |
| PDE-normalized bubble | Euler-Lagrange rescaling of the sharp-inequality extremal | pointwise Laplacian identity on `EuclideanSpace Real (Fin n)` | Candidate root component; coefficient and derivative calculation are not yet checked in Lean |
| Equality in the sharp homogeneous Sobolev inequality | Aubin/Talenti sharp constant result | Bochner integral norms of gradient and critical power | Candidate root component; mathlib API and exact constant are unknown |
| Classification of all optimizers | stronger rigidity result associated with the extremal theorem | none | Explicitly excluded rather than silently credited |

The catalog name alone does not determine whether “Aubin-Talenti functions” means only the explicit
formula, its PDE identity, its extremizing property, or classification of all extremizers. This
intake selects the explicit family plus its PDE and equality properties, while excluding the
classification theorem. The statement phase must confirm that these conjuncts can be represented
without changing domains or conventions, serialize the elaborated target, and mutation-test the
dimension, scale, exponent, coefficient, and equality claim.

Discovery links (not immutable evidence receipts):

- Aubin: <https://doi.org/10.4310/jdg/1214433725>
- Talenti: <https://doi.org/10.1007/BF02418013>

No `H0` or machine-proof claim is made. Source file hashes, edition identity, exact pinpoint mapping,
errata search, and independent review remain required.
