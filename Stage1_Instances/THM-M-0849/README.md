# THM-M-0849 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog item `相变现象`
(`phase-transition phenomenon`). The repository supplies only the gloss `随机图的相变`,
attributes it to Erdos and Renyi in 1960, and carries an untrusted `已验证` label. That wording
does not select a model, one numbered result, ordered asymptotic quantifiers, hypotheses, or a
conclusion.

The official scan of Erdos and Renyi's 1960 paper *On the Evolution of Random Graphs* was inspected.
It studies the uniform fixed-edge graph `Gamma(n,N)`. Section 9 describes the largest-component
"double jump": for `N(n)/n -> c`, its order changes from `log n` when `c < 1/2`, through
`n^(2/3)` at `c = 1/2`, to linear order when `c > 1/2`. The same paper contains several distinct
numbered results that contribute to this synopsis. The catalog does not say whether its root is the
three-regime synthesis, one of those theorems, or a modern transported `G(n,p)` formulation.

The intake therefore preserves that ambiguity rather than substituting a familiar theorem. It
leaves the canonical human statement and Lean target null and proposes `[H5, M4, R4]`. `H5`
classifies only the received catalog wording as not one stable proposition; it does not refute the
published theorems. No exact formal artifact or readable proof reconstruction is credited.

Pinned mathlib exposes the independent-edge law `SimpleGraph.binomialRandom` and finite connected
component APIs. `IntakeProbe.lean` checks only those ingredients. In particular, mathlib's own
documentation warns that this binomial model differs from the historical model. All six downstream
tasks remain open in `task-dag.json`. No accepted proof state, audit completion, theorem completion,
or master acceptance is claimed.
