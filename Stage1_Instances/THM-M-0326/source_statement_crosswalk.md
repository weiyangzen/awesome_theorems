# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Nuclear spaces have the approximation property | A. Grothendieck, *Produits tensoriels topologiques et espaces nucleaires*, Memoirs of the AMS 16 (1955) | future canonical locally convex target | Primary monograph identified, but an exact theorem/page, edition hash, premise map, and errata audit are not yet accepted: `H1` |
| Approximation property via finite-rank maps | The monograph's approximation-property framework; exact definition/pinpoint still required | closure of finite-rank endomorphisms in compact-convergence topology | Mathematically plausible normalization only; topology and closure/net encoding need source and Lean checks |
| Nuclear locally convex hypothesis | Grothendieck's nuclear-space definitions and theorem hypotheses | no canonical repo-local or mathlib `NuclearSpace` API identified at intake | The legacy `NuclearNormedSpace` is a custom normed identity-decomposition predicate and must not silently substitute for the source domain |
| Real and complex scalar cases | Source scalar conventions require pinpoint audit | candidate explicit `Real`/`Complex` statements or a justified `RCLike` abstraction | Binder/domain choice remains open |
| Legacy root-shaped declaration | No independent human-source equivalence established | `AwesomeTheorems.Stage1.S1_M_215.StatementShape` | Discovery input only: custom hypotheses include a proposition-valued compatibility field, so this is not credited as the exact classical theorem |
| Finite-dimensional and truncation lemmas | Standard supporting facts | checked declarations in legacy `S1_M_215.lean` | Potential later leaves only; no root proof credit is inherited |

The short catalog phrase "nuclear spaces and approximation property" is not by itself an exact
statement. In particular, the source may impose separation, completeness, or a particular category
of locally convex spaces, and several approximation properties occur in the literature. The
statement phase must resolve those conventions from a pinned primary source before selecting Lean
binders or accepting the compact-convergence formulation.

Discovery link, not immutable evidence: Grothendieck's memoir is catalogued as Memoirs of the
American Mathematical Society, no. 16 (1955). No `H0` claim is made. Required follow-up comprises a
scan or stable edition hash, exact definition and theorem/page locations, assumptions and notation
crosswalk, corrections/errata search, and independent review.
