# THM-M-0860 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the graph-theoretic Shannon theorem.
The repository supplies Claude Shannon, the year 1949, and only the gloss `边色数的上界`
(`upper bound for the chromatic index`). Those fields strongly identify Shannon's multigraph
edge-colouring theorem family, but they do not state one binder-complete proposition.

The matching primary-source lead is Claude E. Shannon, *A Theorem on Coloring the Lines of a
Network*, *Journal of Mathematics and Physics* 28 (1949), 148-152, DOI
`10.1002/sapm1949281148`. Crossref confirms the bibliographic identity. The article text was not
available for page-level inspection during this intake, so its exact terminology, hypotheses,
theorem boundary, sharpness clause, proof structure, and correction history are not yet admitted.

A familiar modern formulation says that a finite loopless multigraph of maximum degree `Delta`
has chromatic index at most `floor (3 * Delta / 2)`. This is a resolution candidate, not the
canonical statement. Finiteness, loop exclusion, parallel-edge identity, degree and chromatic-index
definitions, rounding, empty cases, and whether sharpness is part of the root all require an
immutable source review before the statement phase may freeze a Lean expression.

Pinned mathlib contains an explicit-edge multigraph structure `Graph`, incidence and loop
predicates, subgraphs, and adjacent simple-graph coloring and degree APIs. `IntakeProbe.lean`
authenticates only these interfaces. A bounded local search found no Shannon, chromatic-index, or
proper multigraph edge-colouring declaration. The simple-graph APIs do not preserve parallel-edge
identity and therefore cannot silently replace the target.

The provisional root vector is `[H1, M4, R4]`: a matching published theorem and primary article are
known, but exact source fidelity is unreviewed; no usable exact Lean artifact is credited; and no
source-faithful readable reconstruction exists. `instance.json` is the structured scope authority
and `task-dag.json` keeps all six downstream phases open. No canonical statement, H0, M0, R0,
accepted state, audit completion, theorem completion, or master acceptance is claimed.
