# Source-statement crosswalk

| Claim component | Source discovery anchor | Proposed formal component | Intake assessment |
|---|---|---|---|
| Action as a time integral of a Lagrangian | W. R. Hamilton, *On a General Method in Dynamics*, Philosophical Transactions of the Royal Society of London 124 (1834), pp. 247-308 | `Action L q := integral (fun t => L t (q t) (q' t))` | Historical primary family located; exact formula/page and notation crosswalk are not yet accepted |
| Fixed-endpoint stationary variation | C. Lanczos, *The Variational Principles of Mechanics*, 4th ed., University of Toronto Press (1970), chapter I, sections on Hamilton's principle | derivative of `Action L (q + s • eta)` at `s = 0` is zero for every endpoint-vanishing `eta` | Expository source only; edition pages, assumptions, and errata require audit |
| Euler-Lagrange differential equation | Same Lanczos chapter; modern proof uses first variation, integration by parts, and the fundamental lemma of calculus of variations | interior equality `d/dt (D_v L) = D_q L` along `q` | Mathematical endpoint frozen; exact Fréchet-derivative and interval encoding deferred |
| “Least” versus stationary action | The classical variational formulation gives stationarity; minimum requires additional conditions | explicitly an implication from zero first variation, not `IsMin` | Semantic guard against broadening or a false universal minimum claim |

Discovery links (not immutable evidence receipts):

- Hamilton bibliographic record: <https://doi.org/10.1098/rstl.1834.0017>
- Lanczos publisher/edition metadata must be pinned during source audit.

The repository's Stage0 wording is only “physical-system variational principle” and supplies no
equations, regularity, endpoint conditions, or source pinpoint. Consequently this intake does not
claim `H0`. `SRC-PINPOINT` must inspect the cited editions, map every analytic premise to the frozen
statement, check historical terminology and errata, and obtain independent review. The statement
phase must then elaborate the exact Lean expression and test mutations that remove endpoint
conditions, weaken differentiability, change the variation quantifier, or replace stationarity by
minimality.

