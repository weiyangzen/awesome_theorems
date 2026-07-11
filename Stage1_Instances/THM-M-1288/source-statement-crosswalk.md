# Source-statement crosswalk

Primary discovery anchor: Giorgio Talenti, "Best constant in Sobolev inequality",
*Annali di Matematica Pura ed Applicata* 110 (1976), 353-372,
DOI `10.1007/BF02418013`. The title, author, year, journal, volume, and page span
identify the intended theorem family. An immutable source hash, theorem/page
pinpoint, assumptions audit, and errata search have not yet been accepted.

| Claim component | Source relationship | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| `1 < p < n`, conjugate Sobolev exponent `q = np/(n-p)` | Core parameter regime of the sharp Sobolev result | naturals/reals plus proofs of inequalities and denominator positivity | Exact coercions and exponent representation open |
| Euclidean scalar test function and gradient | Classical analytic presentation | `EuclideanSpace`, smooth compact support, derivative/gradient and `MeasureTheory` norms | API and weak/classical-gradient bridge open |
| `L^q` norm controlled by gradient `L^p` norm | Inequality content associated with the paper | canonical proposition not yet authored | No elaboration or kernel credit |
| Best constant | Central sharpness claim signaled by the paper and Stage0's `Sobolev最佳常数` wording | explicit `C(n,p)` plus inequality and minimality | Formula and convention crosswalk require page-level audit |
| Equality/extremizers | Closely related Talenti/Aubin-Talenti theorem family | optional strengthening/child obligations | Deliberately not folded into the root |

The repository's Stage0 record supplies only the Chinese labels "Talenti
inequality" and "best Sobolev constant" plus the year 1976. It does not supply a
formal statement and its `已验证` field is not evidence. The chosen scope is the
narrow reading supported by that label and the primary paper's bibliographic
identity; the statement phase may refine notation but must not replace it with a
different Talenti theorem.

Discovery link (not an immutable evidence receipt):
<https://doi.org/10.1007/BF02418013>.

Current human-source status is `H1`, not `H0`: independent review, exact page or
theorem numbering, premise-by-premise mapping, formula transcription, and an
errata/corrections search remain required.
