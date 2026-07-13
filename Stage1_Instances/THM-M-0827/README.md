# THM-M-0827 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog entry named the
Floyd-Warshall algorithm. The repository supplies only the gloss "all-pairs shortest-path
algorithm," attributes it to Robert Floyd and Stephen Warshall in 1962, and labels it verified.
Under rev-5.6 that label is untrusted inventory metadata, not a binder-complete proposition, a
source audit, a Lean statement, or a proof.

The gloss identifies a familiar dynamic-programming algorithm family, but it does not fix the
finite graph and edge representation, weight domain, absent-edge and infinity conventions, walk
and shortest-distance semantics, negative-cycle boundary, vertex enumeration, matrix recurrence,
in-place update semantics, output relation, path reconstruction, or whether correctness,
termination, and complexity are separate results or one conjunction. Intake does not fill those
proposition-changing clauses from memory.

Bibliographic metadata was checked for Robert W. Floyd's *Algorithm 97: Shortest path* and Stephen
Warshall's *A Theorem on Boolean Matrices*. The records corroborate authorship and 1962, but the ACM
primary texts were unavailable to this worker. Floyd is the direct shortest-path lead; Warshall's
paper is a Boolean-matrix paper lead whose exact relationship to this target remains uninspected.
Neither metadata record supplies an accepted exact statement, assumptions, proof map, corrections
review, or source transport for the combined catalog name.

Pinned mathlib exposes directed adjacency, dependent paths, additive path weights, and unweighted
undirected graph distance. `IntakeProbe.lean` authenticates those interfaces. A bounded topic
search found no Floyd-Warshall or all-pairs-shortest-path declaration. These APIs are possible
substrate only; they do not define the matrix recurrence, negative-cycle semantics, or algorithm
correctness.

The provisional vector is `[H1, M4, R4]`. Published source-family leads are identified, but the
exact target, source text, assumptions, proof, Floyd/Warshall transport, corrections, and
source-to-statement mapping remain unaudited. No usable exact formal artifact or source-faithful
proof reconstruction is credited. All six downstream phases remain open. No H0, M0, R0, accepted
state, audit completion, theorem completion, or master acceptance is claimed.
