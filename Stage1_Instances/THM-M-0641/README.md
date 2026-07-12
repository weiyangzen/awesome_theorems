# THM-M-0641 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the Lefschetz fixed-point theorem.
The repository identifies Solomon Lefschetz, the year 1926, and only the gloss `莱夫谢茨数与不动点`
("the Lefschetz number and fixed points"). It supplies no cited theorem, definitions, ordered
binders, hypotheses, conclusion, coefficient convention, or boundary cases. The catalog value
`已验证` is untrusted metadata and gives no human-source or Lean proof credit.

The gloss points to a recognizable classical family: a self-map of a suitably finite topological
space has a fixed point when its Lefschetz number is nonzero. It does not select the space category,
homology or cohomology theory, coefficients, reduced convention, definition of the alternating
trace, or whether the root is only the nonzero-number implication or also a fixed-point index
formula. Choosing one familiar formulation now would add mathematics absent from the source.

This intake therefore freezes the ambiguity rather than inventing a target. The provisional vector
is `[H1, M4, R4]`: `H1` records a historically proved theorem family whose exact source statement
and assumptions are not audited; `M4` records that no usable source-identical formal artifact has
been located; and `R4` records that no accepted readable proof reconstruction exists.

Pinned mathlib provides adjacent singular-homology, linear-trace, and fixed-point APIs.
`IntakeProbe.lean` checks only those interfaces. It does not define a Lefschetz number, state the
target theorem, establish source identity, or receive proof credit. The authoritative intake data
are in `instance.json`; all six dependent phases remain open in `task-dag.json`.

No exact statement, H0, M0, R0, accepted execution state, audit completion, theorem completion, or
master acceptance is claimed.
