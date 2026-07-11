# Source-statement crosswalk

| Claim component | Human source anchor | Lean target | Intake assessment |
|---|---|---|---|
| Positive energy theorem via spinors | E. Witten, "A new proof of the positive energy theorem", *Communications in Mathematical Physics* **80** (1981), 381-402, DOI `10.1007/BF01208277` | Not yet identified | Primary proof source identified; exact theorem/premise and errata audit remains open (`H1`) |
| Energy-momentum inequality | Witten 1981, the positive-energy result for asymptotically flat gravitational initial data under the dominant energy condition | Future canonical expression `E >= norm P` | Intended root; definitions, sign conventions, decay, dimension, and end quantification remain unresolved |
| Time-symmetric positive mass statement | Witten's method specialized to vanishing second fundamental form | Future specialization with nonnegative scalar curvature and ADM mass | Candidate consequence only; it must not replace the stronger initial-data root |
| Equality/rigidity | Rigidity portion of the positive energy theorem family | Future equality theorem | Included in scope, but exact source hypotheses and conclusion require pinpoint audit |
| Dirac analytic input | Witten spinor equation and its asymptotic solution | No repo-local declaration located at intake | Required proof architecture, not evidence of closure |
| Boundary-to-bulk identity | Spinorial/Lichnerowicz identity relating the ADM boundary term to a nonnegative bulk integral | No repo-local declaration located at intake | Required proof architecture; analytic and convention-sensitive premises remain open |

The Stage0 wording `正质量定理的旋量证明` denotes a method and theorem family. The canonical claim
above preserves Witten's spacetime energy-momentum inequality. Recording only nonnegative Riemannian
ADM mass would weaken it, while claiming arbitrary dimensions or boundary variants would broaden it.
The statement phase must use the primary paper to freeze the exact dimension, differentiability,
falloff, completeness, end, boundary, dominant-energy, and equality assumptions before elaboration.

Discovery link (not an immutable evidence receipt):
<https://doi.org/10.1007/BF01208277>.

No `H0` or machine-closure claim is made. Required follow-up includes an immutable source copy and
hash, theorem/page-level premise mapping, errata and later-correction search, independent source
review, repository/mathlib declaration search at pinned revisions, and checked transports for every
alternate encoding.
