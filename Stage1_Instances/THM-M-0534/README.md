# THM-M-0534 rev-5.6 intake

This directory is the fail-closed `planned` intake for the repository label "long exact sequence"
in algebraic topology. The authoritative source gloss says only that a short exact sequence induces
a long exact sequence in homology. It does not decide whether the intended input is a short exact
sequence of chain complexes, a pair/triple of spaces after applying singular chains, or an
Eilenberg-Steenrod homology theory.

The intake freezes the common theorem family: a short exact sequence of homological chain complexes
has connecting morphisms and an exact homology sequence. Topological specializations remain explicit
scope choices for the statement phase and may not be silently substituted for that general claim.
The provisional root vector is `[H2, M3, R4]`. `M3` records only pinned, elaborated mathlib interfaces
found by the intake probe; it is not exact-statement or proof credit for this target.

The scope map, source crosswalk, and open task DAG define the downstream work. Validation evidence is
recorded in `validation.md`. No audit completion or theorem completion is claimed.
