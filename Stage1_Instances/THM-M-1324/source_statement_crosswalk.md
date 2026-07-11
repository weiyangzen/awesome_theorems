# Source-statement crosswalk

Primary discovery anchor: Shiu-Yuen Cheng, "Eigenvalue comparison theorems and its geometric
applications," *Mathematische Zeitschrift* **143** (1975), 289-297,
<https://doi.org/10.1007/BF01214381>. This citation is not yet an immutable evidence receipt.

| Claim component | Source anchor | Intended Lean surface | Intake assessment |
|---|---|---|---|
| Complete `n`-manifold and Ricci lower bound | Cheng (1975), exact theorem/page pending | Riemannian manifold, completeness, Ricci tensor order | Identified at theorem-family level only |
| Geodesic ball and admissible radius | Cheng (1975), exact cut/model restrictions pending | metric ball plus boundary regularity/admissibility predicate | Exact boundary conditions open |
| First Dirichlet eigenvalue | Cheng (1975), convention pending | variational infimum or Dirichlet Laplacian spectrum | No repo-local declaration identified or credited |
| Constant-curvature comparison ball | Cheng (1975), normalization pending | simply connected space-form model | Construction/API open |
| Inequality `lambda_1(B_M) <= lambda_1(B_K)` | Cheng (1975), primary text must confirm direction and hypotheses | canonical root proposition | Provisional target, not exact-statement credit |

The Stage0 phrase "流形上特征值的比较" is too broad to determine a unique theorem. In particular,
Cheng's paper contains a family of comparisons, and curvature polarity changes the comparison
direction. Intake therefore chooses the widely cited Ricci-lower-bound/upper-eigenvalue member as
the provisional root while explicitly keeping the exact-statement gate open.

Before statement acceptance, an auditor must pin a source copy and checksum, record theorem and
page, transcribe ordered assumptions and conventions, check corrections/errata, and independently
confirm that the selected member is the intended target. Only then may the statement phase encode
the root and test altered curvature direction, omitted completeness, radius boundaries, dimension
edge cases, and Laplacian sign mutations.
