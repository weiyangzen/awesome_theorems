# Source-statement crosswalk

| Claim component | Primary-source candidate | Lean surface | Intake assessment |
|---|---|---|---|
| Cyclotomic main conjecture and its proof | B. Mazur and A. Wiles, *Class fields of abelian extensions of Q*, Inventiones Mathematicae 76 (1984), 179-330, DOI `10.1007/BF01388599` | No exact terminal declaration identified | Primary proof source located, but theorem/page, hypotheses, errata, and convention audit remain open: `H1` |
| Iwasawa's original cyclotomic formulation | K. Iwasawa, *On Z_l-extensions of algebraic number fields*, Annals of Mathematics (2) 98 (1973), 246-326 | Future exact statement node | Genealogical primary source candidate; exact statement pinpoint and relation to the Mazur-Wiles formulation remain open |
| Completed Iwasawa algebra | Same sources, after fixing coefficient and Galois-group conventions | legacy `IwasawaAlgebraBoundary` / `IwasawaAlgebraAPI` | Interface discovery only; not a constructed completed group algebra |
| Inverse-limit class-group module and characteristic ideal | Same sources, with transition maps and component conventions fixed | legacy `ClassGroupTowerAPI`, `IwasawaModuleBoundary` | Candidate object inventory only; terminal norm maps and characteristic-ideal semantics are not established |
| Cyclotomic `p`-adic L-function | Same sources, with interpolation normalization and Euler factors fixed | legacy `PadicLFunctionAPI` | Candidate interface only; its abstract interpolation values do not encode the source normalization |
| Equality of ideals | Main-conjecture theorem in the selected primary source | legacy `StatementShape` | Mismatch: `StatementShape` asserts nonemptiness of a package containing a proposition field, not that the proposition holds |

The metadata description "p-adic L-functions and class groups" selects the theorem family but not
one exact formal statement. The statement phase must pin scans or immutable editions, locate the
precise theorem/page, audit corrections, and freeze: odd-prime policy, plus/minus or character
components, primitive/imprimitive characters, Euler factors, periods, exceptional zeros, the
Iwasawa algebra, transition maps, and the orientation of the characteristic-ideal equality.

Discovery links (not immutable evidence receipts):

- Mazur-Wiles: <https://doi.org/10.1007/BF01388599>
- Iwasawa: <https://doi.org/10.2307/1970910>

No `H0` or machine-closure claim is made. A later source audit must map every source assumption to
the exact Lean binders and obtain independent review.
