# THM-M-0949 rev-5.6 intake

`THM-M-0949` is the combinatorics catalog item "density Hales-Jewett theorem." The
catalog gives only the gloss "existence of a combinatorial line," the attribution
Hales/Jewett/Furstenberg/Katznelson, the year 1991, and an untrusted `verified` label.
Those fields identify the theorem family, but they do not state the density hypothesis or a
binder-complete proposition.

## Intake result

This dossier records a fail-closed `planned` instance. An accessible primary proof source,
D. H. J. Polymath, *A new proof of the density Hales-Jewett theorem*, Annals of Mathematics
175 (2012), Theorem 1.4 on page 1285, states the usual finite-word theorem: for every
positive alphabet size `k` and real `delta > 0`, sufficiently high-dimensional subsets of
`[k]^n` having density at least `delta` contain a nondegenerate combinatorial line. The paper
attributes the original 1991 proof to Furstenberg and Katznelson. This is a strong candidate
root, but the repository does not cite it, the original source has not been fully inspected,
and no independent source review has accepted the crosswalk. Intake therefore does not promote
the candidate restatement to the canonical claim or to `H0`.

## Formal boundary

Pinned mathlib contains a kernel-checked ordinary coloring Hales-Jewett theorem and the exact
`Combinatorics.Line` interface for nondegenerate combinatorial lines. It also contains finite-set
density infrastructure. It does not contain a density Hales-Jewett declaration in the bounded
repo-local search. `IntakeProbe.lean` elaborates these adjacent interfaces and a candidate target
shape only; the shape deliberately remains a proposition-valued definition rather than a theorem.
It receives no root statement or proof credit.

The planned root vector is `[H1, M3, R4]`: a complete published proof and exact candidate
restatement are located, but the source edition, original-proof relationship, incorporated
definitions, premise mapping, errata status, and independent review are not accepted; only an
unproved candidate statement shape and adjacent APIs elaborate, with no exact density-theorem proof
located in the local Lean closure; and no source-faithful proof
reconstruction is complete. All six downstream tasks remain open. Neither audit completion nor
theorem completion is claimed.
