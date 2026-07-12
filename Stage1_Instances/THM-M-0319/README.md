# THM-M-0319 rev-5.6 intake

This directory is the `planned` rev-5.6 dossier for the Brouwer fixed-point theorem. The frozen
human claim is the finite-dimensional compact-convex-set formulation: every continuous self-map
of a nonempty compact convex subset of a real finite-dimensional Euclidean space has a fixed
point.

The repository's Chinese source wording is only a one-line discovery description. It does not
specify the dimension encoding, the topology on the set, the exact continuity predicate, or a
primary theorem/page. Those choices and an exact Lean expression remain open for the statement
phase. In particular, this intake does not substitute the contraction mapping theorem, a
one-dimensional intermediate-value theorem, or a fixed-point theorem for an abstract lattice.

The authoritative intake data are in `instance.json`; `scope-map.md` and
`source-statement-crosswalk.md` record the mathematical boundary and source gaps. `task-dag.json`
keeps every dependent phase open. The provisional root vector is `[H1, M4, R4]`. No exact Lean
statement, proof state, audit completion, or theorem completion is claimed.

Exact intake checks and their results are recorded in `validation.md`.
