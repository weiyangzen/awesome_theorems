# Source-statement crosswalk

## Candidate sources

- Alexander Grothendieck, *Produits tensoriels topologiques et espaces nucleaires*, Memoirs of the
  American Mathematical Society 16 (1955). This is the primary monograph candidate for the nuclear
  space and topological tensor-product results. The exact theorem/proposition number, page,
  hypotheses, edition pagination, and errata have not yet been inspected.
- Francois Treves, *Topological Vector Spaces, Distributions and Kernels*, Academic Press (1967),
  chapters on tensor products and nuclear spaces. This is a secondary exposition candidate for
  disambiguating modern notation, not yet H0 evidence.

These bibliographic records are discovery anchors only. The generic theorem name and repository
summary do not determine a unique theorem.

## Crosswalk

| Repository phrase | Intended source component | Required Lean component | Intake status |
|---|---|---|---|
| "Grothendieck duality" | nuclear-space tensor duality, not scheme duality | exact named theorem after source inspection | disambiguated only |
| "topological tensor products" | projective/injective tensor topologies and completions | concrete completed locally convex tensor products | included; API open |
| "nuclear spaces" | a nuclear locally convex factor under source hypotheses | concrete nuclearity predicate | included; API open |
| topology agreement | canonical comparison between completed pi and epsilon products | continuous linear equivalence/homeomorphism | central claim; exact form open |
| duality | bilinear forms or maps into a topologized continuous dual | concrete dual topology and representation map | source-dependent |

## Existing Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_213.lean` checks useful finite algebraic tensor
seminorm facts from mathlib. Its `StatementShape` quantifies over a record whose fields already
contain the nuclear hypothesis and desired conclusions. It therefore neither states the concrete
source theorem nor proves it. The statement phase must independently inspect the selected source,
freeze every binder and hypothesis, and elaborate a concrete target before any proof credit.
