# Full study: epsilon-light vertex subsets

## FS-source — frozen statement and trust boundary

The authority is the declaration at the pinned Formal Conjectures revision,
including its exact module, namespace, type, and source bytes.  Its body has
`sorryAx`, so the body is negative evidence rather than proof authority.  The
claim-owned formulation expands `IsEpsilonLight` without changing the order of
quantifiers or the strict assumptions `0 < ε` and `ε < 1`.  The output retains
both the PSD condition and the real-valued cardinality lower bound.  Downstream
transport and release nodes depend on this anchor.  Exceptional case: the
provider module is a provenance string and is not imported by canonical Lake.

## FS-normalize — Laplacian normalization

For fixed `n`, `G`, and `ε`, write the graph Laplacian as the sum of positive
rank-one edge Laplacians.  The induced spanning graph keeps exactly those edge
summands whose two endpoints lie in `S`.  Thus epsilon-lightness is precisely
the Loewner inequality between that selected sum and `ε` times the original
sum.  The hypotheses are finite vertex type, decidable equality, and the two
strict bounds on `ε`; the output is the normalized spectral selection goal.
This feeds the selection node.  Empty graphs and isolated vertices contribute
zero summands and are preserved, not divided away.  Trust boundary: matrix and
graph primitives come only from pinned Mathlib.

## FS-select — finite spectral selection

Apply the finite spectral-selection step to the normalized edge family.  Its
input is the full rank-one decomposition and `0 < ε < 1`; its two simultaneous
outputs are a vertex set with cardinality at least `c ε n` and the operator
bound for all quadratic forms.  This is stronger than a trace or average-edge
estimate: it supplies the Loewner inequality needed by every vector.  The
selected constant is universal and is fixed before `n`, `G`, and `ε`.
Downstream composition uses both outputs.  Exceptional cases for `n = 0`, an
edgeless graph, disconnected graphs, and zero Laplacian blocks are handled
componentwise without inverse-Laplacian assumptions.  Trust boundary: the
selection proof must be a claim-owned kernel term, never the provider body.

## FS-compose — reconstruct the source proposition

Unfold the local names introduced only by `let` binders, identify the selected
edge sum with the Laplacian of `(G.induce S).spanningCoe`, and package the
positive-semidefinite witness with the cardinality witness.  Then introduce the
quantifiers in their frozen order and provide the positive universal constant.
The hypotheses are exactly the selection outputs; the result is the expanded
right side of the provider equivalence.  Both semantic transports consume this
node.  The natural-to-real coercion on `S.card` and `n` is retained.  Trust
boundary: no local alias or notation may reinterpret a source surface symbol.

## FS-audit — transport and closure

The forward and reverse crosswalk declarations witness that source and target
expressions agree after elaboration; their composites reduce to identity.  The
audit consumes the reconstructed proposition and emits the proposed root plus
its dependency and axiom census.  Release depends on exact M0, total R0, empty
human/machine/readability cuts, and the current trace.  A text-identical header
or worker hash is insufficient: the Master must recompute the root expression,
all transitive non-foundation constants, mutation outcomes, and cold trust-zero
replay.  Until then `master_accepted` remains false.
