# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Existence of a tubular neighborhood for an embedded submanifold | John M. Lee, *Introduction to Smooth Manifolds*, 2nd ed., Graduate Texts in Mathematics 218, Springer (2013), chapter "Tubular Neighborhoods" | future exact root; legacy `AwesomeTheorems.Stage1.S1_M_253.StatementShape` | A standard primary textbook witness is identified, but theorem number/page, edition text, hypotheses, and errata have not yet received independent audit: `H1` |
| Normal bundle and zero section | Same chapter's normal-bundle setup | legacy `CarrierNormalBundleModel` and its `Total`/`zeroSection` | Local names are discovery candidates; their explicit fiberwise data are not yet shown to be the source normal bundle |
| Diffeomorphism from a zero-section neighborhood onto an ambient neighborhood | Same chapter's definition and theorem on tubular neighborhoods | legacy `TubularNeighborhoodPackage` | The legacy package leaves smoothness and diffeomorphism as bare `Prop` fields, so it cannot yet serve as an exact checked encoding |
| Agreement with the embedded submanifold | Tubular map restricts to the inclusion on the zero section | legacy field `tubularMap_zeroSection` | Shape matches the intended component; exact composition and typing remain for the statement phase |
| Euclidean formulation | Morris W. Hirsch, *Differential Topology*, Graduate Texts in Mathematics 33, Springer (1976), tubular-neighborhood discussion | future Euclidean specialization | Secondary corroborating source candidate only; immutable pinpoint and assumptions audit remain open |

The repository source record says only "submanifolds have tubular neighborhoods." That wording does
not decide embedded versus immersed, boundary/corners conventions, compactness, a uniform-radius
claim, or which definition of tubular neighborhood is intended. This intake conservatively freezes
the standard embedded smooth, finite-dimensional Riemannian formulation and explicitly excludes
stronger variants. The source-audit phase must verify the precise Lee edition theorem/page and
errata, and the statement phase must either produce a source-faithful Lean encoding or record a
concrete `M4` blocker rather than weaken the theorem.

Discovery links (not immutable evidence receipts):

- Lee book DOI: <https://doi.org/10.1007/978-1-4419-9982-5>
- Hirsch book DOI: <https://doi.org/10.1007/978-1-4684-9449-5>

No `H0` or machine-closure claim is made.
