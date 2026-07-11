# Source-statement crosswalk

| Claim component | Human source anchor | Lean target at intake | Assessment |
|---|---|---|---|
| Completeness yields a minimizing geodesic between any two points | H. Hopf and W. Rinow, "Ueber den Begriff der vollstaendigen differentialgeometrischen Flaeche", *Commentarii Mathematici Helvetici* 3 (1931), 209-225, DOI `10.1007/BF01292600` | No declaration frozen | Primary original-paper metadata located, but the paper text, exact theorem/page wording, assumptions, and errata have not been independently audited: `H1` |
| Metric completeness and geodesic completeness | Same original theorem family; exact original numbering and modern hypothesis reconciliation remain open | Candidate alternate encoding only | Not credited as equivalent until a source audit and Lean transport check |
| Closed bounded subsets are compact | Standard modern Hopf-Rinow properness formulation; a primary edition/theorem/page must be selected | Candidate intermediate or alternate target | Discovery statement only, not a source receipt |
| Global exponential-map reachability | Standard modern corollary/formulation; exact base-point and domain conventions require audit | Candidate proof bridge | Discovery statement only |

## Statement boundary

The repository summary says "geodesic existence on a complete Riemannian manifold." That wording
does not by itself decide whether completeness is metric or geodesic completeness, whether the
geodesic must minimize length, or whether the entry intends the full equivalence theorem. The
canonical intake claim uses metric completeness and the stronger, standard minimizing-geodesic
conclusion. It explicitly assumes connectedness and finite dimension. The later statement phase
must not weaken this to mere existence of an arbitrary geodesic or replace it by a special compact
case.

The modern and original presentations may differ in language, regularity, boundary, connectedness,
and dimension conventions. Consequently this crosswalk freezes a research obligation, not `H0`.
The source audit must obtain an immutable copy, record edition/file hash and exact pages/theorem,
map every premise and conclusion, search corrections, and obtain independent review.

Discovery link (not immutable evidence):

- Original paper DOI: <https://doi.org/10.1007/BF01292600>

No Lean candidate, external formal proof, or mathlib theorem is asserted here. Searching and pinning
those candidates belongs to the dependent anchor-audit phase after exact statement elaboration.
