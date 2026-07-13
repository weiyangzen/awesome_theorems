# THM-M-0810 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the graph-theoretic Euler formula.
The repository catalog supplies Leonhard Euler, the year 1750, and only the gloss `平面图顶点、
边、面的关系` ("the relationship among the vertices, edges, and faces of a planar graph"). Its
`已验证` label is untrusted metadata under rev-5.6, not a source audit, exact proposition, or proof
receipt.

The gloss identifies the planar-graph Euler-relation family but not one truth-valued proposition.
In particular, it does not state an equation; select a connected plane embedding or an abstract
planar graph; define a face or the outer face; choose simple graphs, multigraphs, loops, bridges, or
cellular maps; or settle the disconnected and sphere-versus-plane variants. Writing the familiar
connected formula at intake would add proposition-changing mathematics absent from the source.

Pinned mathlib supplies finite simple-graph edge counting and connectedness APIs. A bounded search
of the pinned `SimpleGraph` sources located no planar-embedding, face-count, or graph Euler-formula
interface. `IntakeProbe.lean` authenticates only that adjacent substrate. It neither defines a face
model nor states or proves this target.

Accordingly the canonical statement and formal target remain null, the provisional root is
`[H5, M4, R4]`, and all six downstream tasks remain open. `H5` classifies the received catalog
wording as not yet a stable proposition; it does not refute or question the classical Euler
theorem. No accepted proof state, audit completion, theorem completion, or master acceptance is
claimed.
