# THM-M-0839 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-0839`, the weak perfect graph
theorem. The repository says only that a graph is perfect exactly when its complement is perfect,
attributes the result to Laszlo Lovasz in 1972, and labels it verified. Under rev-5.6 that label is
untrusted inventory metadata, not an accepted source audit or Lean proof.

## Intake result

The catalog wording and attribution identify the weak perfect graph theorem, not the strong perfect
graph theorem separately owned by `THM-M-0840`. Two 1972 Lovasz papers are direct primary-source
leads: *Normal hypergraphs and the perfect graph conjecture* and *A characterization of perfect
graphs*. Abstract records exposed by OpenAIRE say that the complement of a perfect graph is perfect;
the second also describes an induced-subgraph min-max characterization. The full primary texts, exact
numbered results, incorporated definitions, proof passages, and correction history were not
available for inspection during this bounded intake, so these leads support `H1`, not `H0`.

A 2019/2020 Coq formalization paper was also inspected as secondary corroboration. It explicitly
uses finite simple graphs, defines perfectness by chromatic-clique equality for every induced
subgraph, and states the same weak theorem. It is useful for disambiguation, but cannot replace the
unaudited 1972 human proof or establish a Lean artifact.

The canonical proposition remains null. The catalog omits finiteness and graph-model assumptions,
the definition of perfectness, the induced-subgraph quantifier, chromatic and clique-number
conventions, and boundary cases. Intake does not silently manufacture those clauses from the
standard theorem name.

Pinned mathlib has simple-graph complement, induced graphs, chromatic number, clique number, and the
universal clique lower bound. `IntakeProbe.lean` authenticates those interfaces. A bounded search
found no perfect-graph predicate or weak perfect graph theorem, so these definitions receive no
target or proof credit.

The provisional vector is `[H1, M4, R4]`. All six downstream tasks remain open. No canonical
statement, H0, M0, R0, accepted proof state, audit completion, theorem completion, or master
acceptance is claimed.
