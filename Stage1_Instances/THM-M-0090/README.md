# THM-M-0090 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog entry named the Weyl
character formula. The repository supplies only the gloss "a character formula for Lie-group
representations," attributes it to Hermann Weyl in 1925, and labels it verified. Under rev-5.6
that label is untrusted inventory metadata, not a primary source, an exact proposition, or proof
evidence.

The gloss identifies the classical theorem family but does not select a compact Lie-group or
complex semisimple Lie-algebra formulation, fix the group or Lie algebra and representation class,
choose a maximal torus or Cartan subalgebra and positive roots, define the weight lattice, Weyl
group, sign, and Weyl vector, or choose between a formal group-algebra identity and pointwise
evaluation on regular torus elements. It also omits integrability, connectedness and simply
connectedness conventions, denominator-zero behavior, and boundary cases. Intake does not silently
supply those proposition-changing clauses from memory.

Pavel Etingof's author-identified MIT OpenCourseWare lecture notes were inspected as an
authoritative modern source lead. Section 26.3, Theorem 26.4 states the formal-character formula for
the irreducible finite-dimensional representation of a complex semisimple Lie algebra with dominant
integral highest weight. This disambiguates one standard reading, but the catalog does not cite
these notes, the source's definitions and assumptions have not been independently reviewed or
transported to Lean, and a Lie-group reading remains possible. It is a source lead, not `H0`
evidence.

Pinned mathlib supplies representation characters, Lie-module weight spaces, Lie-algebra root
systems, and Weyl groups. `IntakeProbe.lean` authenticates those interfaces. A bounded exact-topic
search found no Weyl character formula declaration. The interfaces are ingredients, not a proof or
an alternate target.

The provisional vector is `[H1, M4, R4]`: a complete modern human proof source lead is known, but
the exact source-to-catalog statement and assumptions are not accepted; no usable exact formal
artifact is credited; and no source-faithful proof reconstruction is available. `instance.json` is
the structured scope authority, while `task-dag.json` keeps all six downstream phases open. No H0,
M0, R0, accepted execution state, audit completion, theorem completion, or master acceptance is
claimed.
