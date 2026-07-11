# Source-statement crosswalk

| Claim component | Human source anchor | Lean target at intake | Assessment |
|---|---|---|---|
| Exponential-integrability condition involving one half of terminal quadratic variation | A. A. Novikov, “On an identity for stochastic integrals,” *Theory of Probability and Its Applications* 17 (1972), 717-720 (English translation bibliographic anchor; original pagination/edition requires audit) | planned hypothesis over a continuous local martingale | Primary-source family identified, but theorem/page wording, assumptions, edition, and errata have not been independently checked: `H1` |
| Stochastic exponential is a true martingale on a finite horizon | Same Novikov paper; exact proposition-to-wording mapping remains open | planned root conclusion | This is the intended canonical conclusion, not yet an elaborated Lean proposition |
| Brownian integrand condition `E exp(1/2 integral theta^2) < infinity` | Standard Girsanov-theorem corollary obtained from quadratic variation of an Itô integral; no primary pinpoint accepted yet | alternate candidate only | Must not replace the more general continuous-local-martingale root |
| Expectation equals one | Consequence of the martingale conclusion and initial value one | planned corollary in the root statement | Direction is mathematically routine but receives no formal credit without a checked Lean composition |
| Uniform integrability of localized exponentials | Standard proof mechanism/stronger formulation; source-node pinpoint open | future proof obligation or alternate formulation | Not silently included in the conclusion until exact equivalence/implication direction is frozen |

## Scope decisions

The phrase “指数鞅的鞅性条件” in the generated metadata is too short to determine binders,
filtration conventions, horizon, or whether the Brownian special case was intended. This intake
chooses the classical finite-horizon continuous-local-martingale theorem as the canonical human
claim because it is the general result named Novikov's condition. The Brownian stochastic-integral
version is retained only as a candidate corollary. Infinite-horizon, discontinuous-semimartingale,
and Kazamaki variants are excluded.

No Lean candidate is claimed here. The dependent statement phase must first establish whether the
pinned environment has adequate process, filtration, continuous-local-martingale, quadratic-
variation, and stochastic-exponential APIs. It must then elaborate one exact target, serialize its
expression and environment fingerprints, check every credited transport, and mutation-test a
removed exponential-integrability hypothesis, a Brownian-only domain change, binder/horizon scope,
and the `T = 0` boundary.

Discovery link (not an immutable evidence receipt):

- Novikov paper DOI: <https://doi.org/10.1137/1117081>

The source year differs across original/translation cataloguing, while repository metadata says
1973. That discrepancy is deliberately unresolved at intake. H0 requires an acquired immutable
edition, exact theorem/page and premise mapping, errata search, and independent review.
