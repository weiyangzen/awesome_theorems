# THM-M-0817 rev-5.6 dossier

This directory is the fail-closed `planned` intake dossier for the theorem family cataloged as
Ramsey's theorem with the gloss "arbitrarily large graphs contain large complete subgraphs or
independent sets." The catalog does not say whether this means the finite symmetric graph theorem,
the asymmetric two-color theorem, the general finite edge-coloring theorem, an infinite theorem,
or a statement about the least Ramsey number. It also leaves every parameter and boundary
convention open.

Crossref metadata identifies F. P. Ramsey's 1930 paper *On a Problem of Formal Logic*, but the
statement-bearing primary text was not obtained. An inspected secondary article states both the
general finite edge-coloring theorem and the asymmetric red/blue Ramsey-number formulation, and
cites Ramsey's paper. This confirms the theorem family while also exposing the catalog's variant
ambiguity. It supplies no primary-source passage, complete assumption/proof map, errata audit, or
independent review, so no `H0` credit is claimed.

Pinned mathlib exposes the expected simple-graph vocabulary in
`Mathlib.Combinatorics.SimpleGraph.Clique`. The narrow Lean probe checks clique, independent-set,
cardinality, and complement APIs. A bounded name/text search located no combinatorial Ramsey
terminal declaration in repo-local Lean or pinned mathlib. These are discovery observations only,
not an exhaustive anchor audit and not proof evidence.

Accordingly the intake leaves the canonical statement and formal target null, records the
provisional root vector as `[H1, M4, R4]`, and opens all six downstream tasks. Accepted proof state,
audit completion, and theorem completion remain false. Only the integration lane may accept this
self-tested worker proposal.
