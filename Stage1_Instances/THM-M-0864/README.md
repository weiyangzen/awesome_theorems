# THM-M-0864 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog entry named Tutte's
connectivity theorem. The repository supplies only the gloss "wheel decomposition of 3-connected
graphs," attributes it to William Tutte in 1961, and labels it verified. Under rev-5.6 that label is
untrusted inventory metadata, not an exact proposition, source review, Lean statement, or proof.

The primary bibliographic lead is W. T. Tutte, *A theory of 3-connected graphs*, Indagationes
Mathematicae (Proceedings) 64 (1961), 441-455, DOI
`10.1016/S1385-7258(61)50045-5`. Crossref and Elsevier metadata confirm that identity, but an
inspectable copy of the original article and its exact theorem locator were not obtained. A modern
source, Carmesin and Kurkofka, *Canonical Decompositions of 3-Connected Graphs*, arXiv
`2304.00945v3`, Section 2.7, page 56, states Tutte's Wheel Theorem as: every minimally 3-connected
finite graph is a wheel, where minimality requires both deletion and contraction of every edge to
destroy 3-connectivity. This is a strong theorem-family discriminator, not an accepted replacement
for the catalog's ambiguous "wheel decomposition" wording.

Pinned mathlib supplies ordinary connectivity, vertex deletion, cycle graphs, and local graph
operations. `IntakeProbe.lean` authenticates those adjacent interfaces. A bounded search located no
vertex 3-connectivity predicate, wheel-graph predicate, edge-contraction API, or Tutte wheel theorem.
The mathlib `SimpleGraph.tutte` theorem is about perfect matchings, and `IsFiveWheelLike` is a
different extremal-graph structure; neither is a formal candidate for this target.

The provisional vector is `[H1, M4, R4]`: primary bibliographic identity and a precise modern
restatement are known, but source identity and exact statement mapping are not accepted; no usable
exact Lean artifact is credited; and no source-faithful readable proof exists. `instance.json` is
the structured planned scope record, while `task-dag.json` keeps all six downstream phases open.
No canonical statement, H0, M0, R0, accepted execution state, audit completion, theorem completion,
or master acceptance is claimed.
