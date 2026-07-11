# Source-statement crosswalk

The repository source says only "a gradient estimate for positive solutions." The canonical root
below is therefore an explicit, conservative selection from the Li-Yau family, not a claim that the
metadata already encoded all its assumptions.

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Differential estimate for a positive heat solution | P. Li and S.-T. Yau, *On the parabolic kernel of the Schrödinger operator*, Acta Mathematica 156 (1986), 153-201, DOI `10.1007/BF02399203` | No declaration credited | Primary paper identified; exact theorem/page and premise-by-premise audit remains open |
| Complete manifold and Ricci lower bound | Same paper's gradient-estimate framework | Manifold completeness and Ricci-tensor predicates remain to be located | Precise convention and specialization to `Ric >= 0` require source and formal checks |
| Formula `|grad u|^2/u^2 - u_t/u <= n/(2t)` | Standard zero-curvature scalar Li-Yau specialization | Provisional expression only | Denominators, coercions, Laplacian sign, and dimension encoding are unelaborated |
| Logarithmic formula | Chain rules give `|grad log u|^2 - partial_t log u` for `u > 0` | No checked transport | Candidate equivalent encoding, not evidence |
| Integrated Harnack and heat-kernel estimates | Downstream applications in the Li-Yau theory | No candidate | Consequences are excluded from the exact root |

Discovery link: <https://doi.org/10.1007/BF02399203>. This is not an immutable evidence receipt.
The source audit must acquire a fixed edition, hash it, verify the exact numbered result and pages,
map every assumption and normalization, inspect corrections/errata, and obtain independent review
before `H0`. The Stage0 `已验证` label is untrusted metadata and supplies neither human-source nor
machine-proof credit.

No repo-local Lean declaration was found or tested during intake. The statement phase must choose
actual mathlib representations, elaborate the complete expression, record the environment
fingerprint, prove any logarithmic transport, and mutation-test positivity, heat-equation sign,
Ricci bound, completeness, dimension, and the `t > 0` boundary before proof search.
