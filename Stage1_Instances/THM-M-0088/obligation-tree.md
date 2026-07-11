# THM-M-0088 frozen obligation tree

The architecture expands the exact `Functor.FullyFaithful` data selected by the statement phase.
It constructs an inverse to `yoneda.map` by evaluating a natural transformation at the source
object on its identity, then proves the two inverse laws. The frozen denominator was assigned
before the audited mathlib body's availability was allowed to affect node status.

## M0088-ROOT

The exact `YonedaEmbeddingTarget C`. It requires the terminal constructor and remains open at `M3`.

## M0088-T-CONSTRUCT

`yonedaEmbedding_of_inverseLaws` is checked conditional composition: a preimage operation plus the
two inverse laws yields exactly the root. This node proves none of those three inputs.

## M0088-C-PREIMAGE

For `f : yoneda.obj X ⟶ yoneda.obj Y`, define its candidate preimage by evaluating `f.app` at
`op X` on `𝟙 X`. The proof phase must connect this expression to the frozen constructor without
hiding it behind the imported fully-faithful result.

## M0088-L-RIGHT

Prove `yoneda.map (preimage f) = f`. Natural-transformation extensionality reduces this to equality
at each object and morphism; `M0088-B-NATURALITY` supplies the substantive equation.

## M0088-L-LEFT

Prove `preimage (yoneda.map f) = f`. This is the identity-component computation for Yoneda's map.

## M0088-B-NATURALITY

Track the precise Yoneda naturality equation that recovers every component from the identity
component. A one-line use of the library lemma still belongs to this bridge obligation.

## M0088-X-SOURCE

Pinpoint the human Yoneda lemma and fully-faithful corollary, with assumptions and errata. This is
human-source evidence only and cannot close machine proof edges.

## M0088-X-PROVENANCE

Record the unique imported terminal body, transitive declarations, imports, axioms, TCB, and replay
receipts. It is an informational overlay and cannot close the proof graph.

The frozen root cut set is `M0088-C-PREIMAGE`, `M0088-L-RIGHT`, and `M0088-L-LEFT`. Every semantic
leaf has a substantive ledger and a budget below 100; those budgets are split thresholds, not proof
or readability evidence.
