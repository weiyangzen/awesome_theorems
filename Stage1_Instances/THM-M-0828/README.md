# THM-M-0828 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog entry named the
Edmonds-Karp algorithm. The repository supplies only the gloss "a polynomial-time algorithm for
maximum flow," attributes it to Jack Edmonds and Richard Karp in 1972, and labels it verified.
Under rev-5.6 that label is untrusted inventory metadata, not a precise theorem, source audit, Lean
statement, or proof.

The gloss identifies a standard algorithmic theorem family, but it does not fix a directed-network
model, capacity domain, source and sink conditions, residual-edge convention, breadth-first path
selection, output contract, correctness clause, termination claim, or cost model. It also does not
say whether the intended root is only polynomiality or the usual conjunction of maximum-flow
correctness and an `O(V * E^2)` worst-case bound. Intake does not fill those proposition-changing
clauses from memory.

The bibliographic identity of Edmonds and Karp's 1972 paper, *Theoretical Improvements in
Algorithmic Efficiency for Network Flow Problems*, was independently crosschecked through its DOI
record. The available metadata confirms authors, journal, volume, issue, pages, year, and title,
but the primary paper text was not accessible for inspection during this run. It therefore remains
a source lead rather than an accepted statement/proof crosswalk.

Pinned mathlib exposes generic quiver paths, additive path weights, undirected simple-graph walks,
shortest-walk distance, and finite bounded-walk enumeration. `IntakeProbe.lean` authenticates those
interfaces. A bounded exact-topic search found no maximum-flow, residual-network, augmenting-path,
Ford-Fulkerson, or Edmonds-Karp declaration. The checked APIs are infrastructure clues only; the
simple-graph metric is undirected and cannot silently become the residual directed network.

The provisional vector is `[H1, M4, R4]`: a complete published human result is identified by an
exact bibliographic lead, but its statement, assumptions, proof, corrections, and source-to-node
mapping have not been inspected; no usable exact formal artifact is located; and no source-faithful
proof reconstruction exists. All six downstream phases remain open. No H0, M0, R0, accepted state,
audit completion, theorem completion, or master acceptance is claimed.
