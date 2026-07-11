# Source-statement crosswalk

| Claim component | Human source anchor | Provisional Lean surface | Intake assessment |
|---|---|---|---|
| Constant scalar curvature in a conformal class on a compact manifold | H. Yamabe, *On a deformation of Riemannian structures on compact manifolds*, Osaka Math. J. 12 (1960), 21-37 | Smooth manifold, Riemannian metric, scalar curvature, conformal rescaling | Original program and claimed proof; the proof contained a gap, so this source alone cannot support closure |
| Variational/PDE repair under an additional range condition | N. S. Trudinger, *Remarks concerning the conformal deformation of Riemannian structures on compact manifolds*, Ann. Scuola Norm. Sup. Pisa 22 (1968), 265-274 | Conformal Laplacian, Sobolev quotient, positive weak/smooth solution | Primary repair source located; premise and convention audit remains open |
| Strict inequality and broad dimensional/codimension cases | T. Aubin, *Équations différentielles non linéaires et problème de Yamabe concernant la courbure scalaire*, J. Math. Pures Appl. 55 (1976), 269-296 | Yamabe constant and comparison with the round sphere | Primary source located; exact case boundary and theorem pinpoint remain open |
| Completion of the remaining locally conformally flat / positive mass cases | R. Schoen, *Conformal deformation of a Riemannian metric to constant scalar curvature*, J. Differential Geometry 20 (1984), 479-495 | Remaining branch plus positive-mass input | Primary completion source located; assumptions, errata, and node mapping remain open |
| Metric conclusion | The four-source historical chain above | `exists u > 0, IsConstant (scalarCurvature (u^(4/(n-2)) • g))` (schematic only) | No Lean syntax or declaration is asserted; exact representation is deferred to statement phase |
| Yamabe equation | Conformal scalar-curvature transformation used by the cited sources | `L_g u = lambda * u^((n+2)/(n-2))` (schematic only) | Equivalence requires checked coefficient, power, regularity, and Laplacian-sign conventions |

The root is the solved Yamabe existence theorem, not merely Yamabe's original attempted proof and
not the assertion that a particular flow converges. The phrase “共形度量的常数标量曲率” in the
repository source is therefore narrowed only by the standard hypotheses intrinsic to that theorem:
smooth compact boundaryless connected manifold, dimension at least three, and a given smooth
Riemannian metric. This scope decision must be reviewed at the statement gate; it is not yet an H0
source receipt.

No public Lean 4 formalization is claimed or credited at intake. Follow-up must obtain immutable
source artifacts and hashes, identify theorem/page statements and all assumptions, check corrections
and errata, freeze geometric/PDE conventions, inspect pinned mathlib APIs, and independently review
the completed premise-to-node crosswalk.

Discovery links (not immutable evidence receipts):

- Yamabe: <https://projecteuclid.org/journals/osaka-mathematical-journal/volume-12/issue-1/On-a-deformation-of-Riemannian-structures-on-compact-manifolds/ojm/1200689814.full>
- Trudinger: <http://www.numdam.org/item/ASNSP_1968_3_22_2_265_0/>
- Aubin: <https://zbmath.org/0346.53033>
- Schoen: <https://doi.org/10.4310/jdg/1214439291>
