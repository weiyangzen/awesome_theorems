# Source-statement crosswalk

| Source field | Repository evidence | Lean/formal consequence | Intake assessment |
|---|---|---|---|
| Name | `transportation 不等式` | Suggests a transportation(-cost) inequality family, not a unique declaration | Insufficient for identity |
| Verbatim content | `最优传输的集中` | Mentions optimal transport and concentration but gives no proposition | No exact target can be elaborated |
| Domain | Not supplied | Metric space, Euclidean/Gaussian space, or product space cannot be chosen | Open |
| Quantifiers and hypotheses | Not supplied | Measures, absolute continuity, moments, and product assumptions cannot be frozen | Open |
| Conclusion and constants | Not supplied | Transport cost, entropy, deviation tail, exponent, and normalization are unknown | Open |
| Attribution/source | Stage0 says only `众多数学家`; no paper, edition, theorem, or page | No primary-source premise or errata audit is possible | `H4` |

## Candidate disambiguation map

| Candidate | Representative primary source | Representative mathematical shape | Why it is not selected |
|---|---|---|---|
| Talagrand Gaussian `T2` | M. Talagrand, *Transportation cost for Gaussian and other product measures*, Geometric and Functional Analysis 6 (1996), 587-600, DOI `10.1007/BF02249265` | For standard Gaussian `gamma`, quadratic transport cost to `gamma` is bounded by twice relative entropy (under the source's conventions) | The repository never says Gaussian, quadratic cost, entropy, or the constant |
| Marton transport/concentration | K. Marton, *Bounding d-distance by informational divergence: a method to prove measure concentration*, Annals of Probability 24 (1996), 857-866, DOI `10.1214/aop/1039639365` | Coupling/transport distance is controlled by informational divergence and yields concentration, notably for product-type settings | The repository never specifies the distance, product assumptions, or concentration conclusion |

These references establish that the wording has multiple credible readings; they are discovery
anchors, not accepted `H0` evidence and not an authorization to choose a theorem. The source-status
label `已验证` is explicitly untrusted under rev-5.6 and supplies no statement content.

Required resolution: provide or locate an authoritative source pinpoint whose displayed theorem
fixes the measure spaces, cost/distance convention, admissible measures, finiteness and absolute
continuity assumptions, quantifier order, conclusion, and constants. The subsequent statement phase
must then transcribe and elaborate that claim, fingerprint its environment, and mutation-test every
material hypothesis and boundary case.
