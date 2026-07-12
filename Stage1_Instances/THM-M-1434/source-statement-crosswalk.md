# Source-statement crosswalk

## Repository authority

`Docs/researches/math_theorems.md:10474` records `Sullivan无游荡域定理`; lines 10475-10479 give
Dennis Sullivan, 1985, the complete gloss `有理函数的无游荡域` ("no wandering domains for
rational functions"), importance "high," and status `已验证`. The record first entered the
repository in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. That commit is repository
provenance, not a mathematical source revision.

`Docs/Stage0_Blueprint.md:38996` repeats the gloss while explicitly leaving precise definitions and
premises, proof process, dependencies, equivalent forms, axioms, machine status, and artifact links
open. The rev-5.6 manifest preserves `已验证` solely as `source_status_untrusted`.

## Primary-source lead inspected

The official Annals bibliography page identifies Dennis Sullivan, *Quasiconformal homeomorphisms
and dynamics I. Solution of the Fatou-Julia problem on wandering domains*, **Annals of
Mathematics** 122(2) (1985), 401-418, DOI `10.2307/1971308`. The page was retrieved twice on
2026-07-12; the byte streams were identical with SHA-256
`f050a74ac40cd5492598cc8c9d0b0d7aefc3d09029cc2c0958f6cf62dddc1fe6`.

That page explicitly says "No abstract available" and exposes neither the paper text nor a theorem
locator. The paper was not recovered or inspected, and its definitions, exact assumptions,
statement, proof boundary, cited dependencies, corrections, and errata are therefore open. The
bibliography is a strong source lead, not a pinpoint `H0` crosswalk.

## Candidate crosswalk

| Repository/source phrase | Mathematical content to freeze | Required Lean surface | Intake status |
|---|---|---|---|
| "rational functions" | complex rational self-map, total on the Riemann sphere, with exact degree hypothesis | `RatFunc Complex` or numerator/denominator data plus a proved total sphere action | algebraic evaluation API probed; analytic sphere map open |
| "Fatou-Julia problem" | Fatou set as the locus where the iterates form a normal family in spherical topology | sphere topology, iterates, local normal convergence, openness and invariance | no target-specific normal-family/Fatou interface located |
| "domains" | connected components of the Fatou set | `connectedComponentIn` or a source-faithful component type | generic topology API probed; component action open |
| "wandering" | all forward component iterates are distinct, under the exact induced action | component iteration and set/component equality | definition and indexing open |
| "no wandering" | every component is preperiodic/eventually periodic | witnesses such as `m < n` and equality in the selected component encoding | leading candidate only; equivalence unchecked |
| point at infinity and poles | a total map on the chosen Riemann-sphere model | `OnePoint Complex` or projectivization plus rational evaluation at every point | compactification API probed; required map absent |
| Sullivan 1985 article | human theorem and proof source | node-specific source ledger and readable proof map | bibliography verified; primary text and mapping uninspected |
| `已验证` | untrusted inventory metadata | no declaration or proof component | explicitly rejected as evidence |

## Human-source boundary

The provisional `H1` classification records that a published source explicitly devoted to the
wandering-domain problem is known while exact source reconstruction remains open. It does not claim
that the customary textbook formulation has been verified against Sullivan's paper. Before `H0`,
an independent qualified reviewer must inspect an immutable edition; pinpoint the exact theorem and
dependent definitions; transcribe every domain, binder, hypothesis, conclusion, and exceptional
case; map the proof and its cited dependencies; check corrections and errata; and approve the
Chinese-to-source identity.

## Lean boundary

The pinned environment is Lean 4.29.0 at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740` with mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The bounded intake probe checks algebraic rational
functions, meromorphicity, one-point compactification, connected components, iteration, and generic
periodic points. A scoped name search found no obvious Sullivan, wandering-domain, Fatou-set,
Fatou-component, or Julia-set declaration in pinned mathlib. This is intake discovery only, not an
exhaustive anchor audit and not a claim about external Lean projects.

Before statement credit, the reviewed source claim must map to one exact elaborated Lean expression
with minimal pinned imports, fixed profiles, a serialized expression/environment fingerprint,
checked alternate transports, and all required statement mutations. Until then, no source,
statement, proof, audit-completion, or theorem-completion credit is legal.
