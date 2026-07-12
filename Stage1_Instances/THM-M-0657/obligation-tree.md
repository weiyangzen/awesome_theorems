# THM-M-0657 frozen obligation architecture

Registry v1 freezes 14 canonical IDs against the exact hashes of
`Statement.lean` and `anchor-audit.json`. The frozen denominator is recorded in
`obligation-registry.json`; later proof discovery cannot delete, merge, or
exclude an inconvenient obligation without a new registry version and delta.

## Proof architecture

The selected project-level route first audits the exact categoricity encoding
and the checked existential-source transport. Under fixed `L`, `T`, and the
source cardinal, it must derive the complete-theory working context rather
than silently assuming completeness. It then develops the rank/type apparatus,
derives the stability consequence of the source categoricity hypothesis, and
uses that result to establish saturation at each uncountable target cardinal.
In parallel it constructs a model of the exact target cardinal. Saturated-model
back-and-forth supplies pairwise isomorphism, and the terminal package combines
existence and uniqueness into `CategoricalWithExistence` before abstracting all
root binders.

This is a provisional modern route, not a claim that Morley's 1965 paper uses
these exact packages. `M0657-X-SOURCE` therefore remains root-relevant and open:
the proof phase must inspect the primary proof and either crosswalk this route
node by node or issue registry v2 with an explicit architectural delta.

The proof graph has reciprocal `proof_requires` and `composes` edges. Separate
refinement, provenance, evidence, trust, documentation, and workflow graphs
prevent citations, receipts, and TCB records from masquerading as proof
premises. Every project-level leaf has a substantive ledger and a budget of at
most 100 steps; invoking compactness, stability, saturation, model existence,
or saturated uniqueness must not be collapsed into a one-line library call.

## Closure boundary

`ObligationTree.lean` defines `MorleyTransferPackage` to be the exact canonical
target and checks that an already-established package returns that target. The
identity boundary validates the terminal type only: it does not construct the
package, close any semantic child, or prove Morley's theorem. The statement
interface and existential transport remain `M3`; all substantive formalization
packages remain open. The root is `[H1, M3, R3]`, and neither audit completion
nor theorem completion is claimed.
