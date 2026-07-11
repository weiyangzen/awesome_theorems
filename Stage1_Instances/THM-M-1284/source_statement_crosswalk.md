# Source-statement crosswalk

| Claim component | Source anchor | Lean target | Intake assessment |
|---|---|---|---|
| Named result | R. Ye, *Global existence and convergence of Yamabe flow*, Journal of Differential Geometry 39 (1994), 35-50 | none selected | Primary bibliographic source identified; repository metadata alone is insufficient for `H0` |
| Flow equation and normalization | Exact displayed equation in the primary paper, page pinpoint pending | future metric-valued evolution definition | Must be transcribed, not reconstructed from memory |
| Global existence | Primary paper's global-existence result, theorem/page pending | future existence proposition | Time domain, regularity, and manifold assumptions unresolved |
| Convergence | Primary paper's convergence result(s), theorem/page pending | future convergence proposition | Hypotheses, topology, rate, and limiting metric unresolved |
| Constant scalar curvature limit | Consequence asserted in the source family, exact node pending | future limit-property proposition | Must be separated from convergence and checked against the exact normalization |

Repository provenance is `Docs/researches/math_theorems.md`, lines 9381-9385: the Chinese label
`Ye定理`, author Rugang Ye, year 1994, and the phrase `Yamabe流的收敛性`. Its `已验证` field is
explicitly untrusted under rev-5.6 and is not source or machine evidence.

Discovery link (not an immutable evidence receipt):
<https://projecteuclid.org/euclid.jdg/1214454674>.

The source title covers more than the manifest phrase, while "convergence" without assumptions can
broaden the theorem incorrectly. The statement phase must acquire a stable primary-source copy,
record its digest, transcribe theorem numbers/pages and ordered assumptions, check errata or later
corrections, and only then define the canonical human and Lean claims. Until that work is independently
reviewed, the source status is `H2` and the exact-statement machine status is `M4`.

