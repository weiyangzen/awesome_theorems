# Source-statement crosswalk

## Repository record and source candidates

The Stage0 record supplies only the Chinese title and the gloss "the excision property of relative
homology groups." Its `已验证` label is untrusted under rev-5.6 and supplies no coefficient,
topological hypothesis, map, degree convention, theorem locator, or proof evidence.

A standard source candidate is Allen Hatcher, *Algebraic Topology* (2002), Proposition 2.21 in the
singular-homology chapter, commonly stated for subspaces `Z subset A subset X` with the closure of
`Z` contained in the interior of `A`. A foundational source candidate is Samuel Eilenberg and
Norman Steenrod, *Foundations of Algebraic Topology* (1952), in its treatment of the excision
axiom. These are discovery anchors only. This intake did not independently freeze an immutable
edition, inspect the exact pages and definitions row by row, check errata, or obtain independent
review; therefore they are not `H0` evidence.

## Crosswalk

| Repository/source phrase | Mathematical component to freeze | Required Lean component | Intake status |
|---|---|---|---|
| "relative homology groups" | relative singular homology of `(X, A)` | concrete relative chain complex and homology functor | theory intended; coefficients and API open |
| excised subspace `Z` | removal from both members of the pair | set differences with induced subspace topologies | included; representation open |
| excision hypothesis | `closure Z subset interior A` or exact source equivalent | closure, interior, subset proof in ambient `X` | conventional variant identified; source wording open |
| inclusion of pairs | `(X \ Z, A \ Z) -> (X, A)` | commuting morphism of pairs / induced chain map | required; exact API open |
| "induces an isomorphism" | relative homology map is an isomorphism | `IsIso`, linear equivalence, or group isomorphism for each degree | conclusion fixed as a family; encoding open |
| every degree | quantification over homological grading | source-compatible degree index | required; indexing convention open |
| coefficients | source-selected coefficient group or ring | coefficient object and typeclass assumptions | unresolved |

## Human and machine boundary

A narrow repository and pinned-mathlib text search found no declaration named for the excision
theorem and no obvious relative-singular-homology excision implementation. That observation is not
an exhaustive anchor audit and does not establish absence of reusable chain-complex or homology
infrastructure. The pinned mathlib revision is recorded in `validation.md`; external projects were
not searched during this intake phase.

Before `H0`, an independent reviewer must approve the selected immutable edition, exact
proposition/page, definitions, assumptions, coefficient convention, proof boundaries, and errata.
Before statement credit, every approved row must map to one elaborated Lean target without weakening
the neighborhood hypothesis, replacing the relative result by an absolute corollary, or assuming
the induced isomorphism.
