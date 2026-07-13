# THM-M-0834 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-0834`, the five-color
theorem. The repository gives Percy Heawood, the year 1890, and the gloss "every planar graph can
be colored with five colors." It gives no citation, definition of planarity, graph class, coloring
convention, numbered result, proof boundary, correction history, or formal artifact. The catalog's
`已验证` field is untrusted metadata under rev-5.6.

## Intake result

The gloss identifies the classical theorem family: a finite planar graph admits a proper vertex
coloring using at most five colors. It does not yet select a binder-complete proposition. In
particular, the repository does not settle finite versus locally finite graphs, abstract graph
planarity versus a supplied plane embedding or the dual map formulation, simple versus multi-
graphs, `Colorable 5` versus a chromatic-number inequality, disconnected graphs, or boundary cases.
Choosing any one of these at intake would add source decisions that the catalog does not make.

The leading historical source is P. J. Heawood's *Map-Colour Theorem*, published in the
*Quarterly Journal of Pure and Applied Mathematics* 24 (1890), pages 332-338. This identity was
independently confirmed through the zbMATH/JFM record `22.0562.02`. Its contemporary secondary
review describes map regions that share a boundary line and says the simple-case upper bound can be
improved from six to five. No immutable primary text, pinpoint statement, proof, definitions, or
errata record was admitted. It therefore supplies an H1 source lead, not H0 source fidelity.

Pinned mathlib supplies ordinary simple-graph coloring. Its module documentation defines
`G.Colorable n` as the existence of a proper coloring with colors `Fin n`, but lists planar graphs
as future work. Its `docs/1000.yaml` names the five-color theorem but attaches no `decl` entry. A
bounded repository and pinned-dependency search found no graph-planarity predicate or five-color
theorem. `IntakeProbe.lean` checks only the adjacent coloring APIs and gives no target statement or
proof credit. One immutable external Lean lead has a syntactic five-color declaration, but it
depends on numerous `sorry`-backed results and an incompatible newer toolchain; it is explicitly
blocked and supplies no machine credit.

Accordingly the canonical human and Lean statements remain null, the provisional root vector is
`[H1, M4, R4]`, and all six downstream tasks remain open. No H0, M0, R0, accepted proof state,
audit completion, theorem completion, or master acceptance is claimed.
