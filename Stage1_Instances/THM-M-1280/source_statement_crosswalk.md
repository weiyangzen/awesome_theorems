# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Every closed Riemannian `n`-manifold, `n >= 3`, admits a conformal constant-scalar-curvature metric | R. Schoen, *Conformal deformation of a Riemannian metric to constant scalar curvature*, Journal of Differential Geometry 20 (1984), 479-495 | No declaration frozen | Primary completion paper identified, but exact hypotheses, conventions, errata, and proof-node mapping remain unaudited: `H1` |
| Standard theorem statement and historical division into Yamabe, Trudinger, Aubin, and Schoen cases | J. M. Lee and T. H. Parker, *The Yamabe problem*, Bulletin of the AMS 17 (1987), 37-91, especially the introductory statement and historical survey | Future root and source-map nodes | Expository cross-check only; it cannot independently clear primary-source fidelity |
| Positive-solution PDE formulation | Scalar-curvature conformal-change equation in the sources above | Future conformal Laplacian and smooth-function APIs | Constants depend on Laplacian and scalar-curvature conventions; equivalence is not checked |
| Variational/minimizer formulation | Yamabe functional treatment in Schoen and Lee-Parker | Future Sobolev/variational APIs | Normalization, compactness, positivity, elliptic regularity, and attainment-to-metric transport remain explicit obligations |

The canonical intake wording deliberately says "closed" (compact without boundary) and dimension at
least three. The Stage0 slogan does not specify these assumptions and therefore cannot itself be the
exact target. The statement phase must decide whether connectedness is assumed, encode the
dimension-dependent exponent without an accidental natural-number division, elaborate the metric
rescaling, and mutation-test compactness, boundary, positivity, dimension, binder order, and the
constancy conclusion.

Discovery links, not immutable evidence receipts:

- Schoen 1984: <https://doi.org/10.4310/jdg/1214439291>
- Lee-Parker 1987: <https://doi.org/10.1090/S0273-0979-1987-15514-5>

No `H0` or machine-closure claim is made. Later source audit must acquire immutable copies and
hashes, check bibliographic variants and corrections, map every assumption to frozen obligations,
and obtain independent review.
