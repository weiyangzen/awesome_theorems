# THM-M-0027 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the Wedderburn-Artin theorem. The
repository catalogue gives only the Chinese gloss `半单环的结构定理` ("the structure theorem for
semisimple rings"), attributes it to Joseph Wedderburn and Emil Artin, dates it to 1907, and labels
it `已验证`. Under rev-5.6 that label is untrusted metadata, not an exact statement, source audit,
or proof receipt.

The gloss identifies a classical theorem family but does not fix ring conventions, left-versus-
right semisimplicity, the existence form versus a biconditional, factor and matrix-size data, the
zero-ring and empty-product cases, or whether uniqueness is part of the claim. It also does not
select the simple Artinian, algebra, finite-dimensional, or algebraically closed specializations.
The historical date and attribution do not by themselves identify a source passage.

Pinned mathlib has a strong formal candidate in
`Mathlib.RingTheory.SimpleModule.WedderburnArtin`:
`IsSemisimpleRing.exists_ringEquiv_pi_matrix_divisionRing` gives a finite product of matrix rings
over division rings, and `isSemisimpleRing_iff_pi_matrix_divisionRing` also gives the converse.
The intake probe authenticates these declarations and their current axiom reports. It does not
silently identify either expression with the underspecified catalogue gloss or claim proof credit.
A legacy Brauer-group file contains, as its relevant Wedderburn-Artin result, only a finite
central-simple-algebra specialization and is foreign discovery evidence, not this target's root.

A separate catalogue target, `THM-M-0036`, names the Artin-Wedderburn classification of central
simple algebras. This intake keeps that algebra-specific target out of the general semisimple-ring
root; the statement phase must preserve the partition explicitly.

The provisional root vector is `[H1, M3, R4]`. A classical theorem family and historical source
leads are known but no pinpoint source statement is accepted; usable pinned formal candidates
exist but no canonical target or checked source transport is frozen; and no source-faithful proof
reconstruction exists.

`instance.json` is the structured scope authority. `scope-map.md` and
`source-statement-crosswalk.md` freeze the admissible family and non-substitution boundary.
`task-dag.json` keeps all six downstream phases open. Exact commands and results are in
`validation.md`. No H0, M0, R0, accepted proof state, audit completion, theorem completion, or
master acceptance is claimed.
