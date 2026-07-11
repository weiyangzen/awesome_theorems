# Source-statement crosswalk

| Claim component | Human source anchor | Formal target component | Intake assessment |
|---|---|---|---|
| Root equality of analytic and topological indices | M. F. Atiyah and I. M. Singer, "The index of elliptic operators on compact manifolds," *Bulletin of the AMS* 69 (1963), 422-433, especially Theorem 1 | `ind_analytic(D) = ind_topological(symbol(D))` | Primary announcement located; immutable copy, exact convention audit, corrections, and independent review remain open: `H1` |
| Analytic index | Same paper, definitions preceding Theorem 1: dimension of solutions minus dimension of solutions of the adjoint | Fredholm kernel/cokernel index of the chosen realization of `D` | The equivalence of the source's adjoint formulation and a Lean cokernel formulation must be proved or avoided by matching definitions |
| Symbol and ellipticity | Same paper's elliptic-operator and symbol setup | principal symbol invertible away from the zero section; K-theory class | Exact bundle pullbacks, support condition, and real-versus-complex cotangent conventions are unresolved |
| Topological index | Same paper's K-theoretic construction leading to Theorem 1 | Thom/Gysin pushforward of the symbol class to `K(point) ~= Int` | Candidate mathematical construction only; no Lean API or checked transport is credited |
| Detailed proof lineage | M. F. Atiyah and I. M. Singer, "The index of elliptic operators: I," *Annals of Mathematics* 87 (1968), 484-530 | later proof-architecture nodes | Primary detailed source located, but theorem/page-to-obligation and errata mapping belong to anchor audit |
| Cohomological formula | Characteristic-class expression developed in the index-theorem series | alternate target after Chern character | Not accepted as the canonical root without a checked equivalence |

The provisional root intentionally uses the K-theoretic analytic-index/topological-index equality,
not merely a Dirac, signature, Riemann-Roch, or low-dimensional consequence. Before statement credit,
the next phase must select exact definitions for compactness/boundary, smooth complex bundles,
differential operators, ellipticity, Fredholm index, symbol K-class, and topological pushforward;
then elaborate the target and mutation-test every hypothesis and boundary convention.

Discovery links (not immutable evidence receipts):

- 1963 announcement: <https://doi.org/10.1090/S0002-9904-1963-10957-X>
- 1968 detailed paper: <https://doi.org/10.2307/1970715>

No `H0` claim is made. Required follow-up includes source-file hashes, pinpoint assumption mapping,
errata/correction search, and independent source review.
