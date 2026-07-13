# THM-M-0878 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-0878`, the repository topic
`最小费用流` (minimum-cost flow). The catalog supplies only the gloss `带费用的网络流` (a
costed network flow), attributes it collectively to the twentieth century, and labels it
`已验证`. Under rev-5.6 that label is untrusted metadata, not source or proof evidence.

The gloss identifies a problem family rather than one truth-valued proposition. It does not choose
minimum-cost circulation, fixed-value minimum-cost flow, minimum-cost maximum flow, transshipment,
an existence or integrality result, residual-cycle or price optimality, or correctness and
complexity of a particular algorithm. These choices change the domains, hypotheses, conclusion,
and proof architecture, so this intake leaves the canonical mathematical and Lean statements null.

An immutable copy of Goldberg and Tarjan's 1987 technical report *Finding Minimum-Cost
Circulations by Canceling Negative Cycles* was inspected as a primary-source lead. Section 2 gives
a precise circulation model and Theorem 2.1 characterizes optimal circulations by absence of
negative residual cycles. Sections 3 and 4 state distinct price-duality, termination, correctness,
and complexity results. The report calls circulation, minimum-cost flow, and transshipment
equivalent, but neither it nor any single theorem in it is selected by the catalog. The inspected
family supports provisional H1 only; root selection, complete premise and correction mapping, and
independent review remain open.

Pinned mathlib provides directed-graph, path-weight, finite-sum, and finite-argmin substrate.
`IntakeProbe.lean` authenticates only those interfaces. A bounded topic search found no
minimum-cost-flow or minimum-cost-circulation declaration in the pinned tree. The probe neither
defines a network flow nor states or proves a candidate root.

The provisional vector is `[H1, M4, R4]`: a strong primary proof-family source is inspected, but
the exact repository root is not selected; no usable exact formal artifact is credited; and no
source-faithful readable reconstruction can attach to an unidentified root. `instance.json` is
the structured scope authority and `task-dag.json` keeps all six downstream phases open. No H0,
M0, R0, accepted state, audit completion, theorem completion, or master acceptance is claimed.
