# THM-M-1455 statement blocker

## First failed gate

The rev-5.6 exact-statement gate is blocked before Lean target elaboration. The repository gives
only the method name `共轭梯度法` and the gloss "iterative solution method for symmetric
positive-definite systems." The 1952 primary paper contains multiple inequivalent theorems and
algorithmic properties, while the catalog selects none.

The tempting finite-termination statement requires the precise recurrence, finite-dimensional real
system, positive-definiteness assumptions, early-termination interpretation, and exact arithmetic.
The source expressly says the at-most-`n` conclusion holds when no rounding error occurs. It cannot
be broadened into finite termination or numerical stability for an arbitrary implementation.

The optimization target `THM-M-1503` is separately cataloged and cannot resolve this ambiguity.

## Retry condition

An accountable statement review must select an immutable primary-source result and freeze the
matrix or operator domain, scalar field, dimension and indexing, symmetry and positive-definiteness
predicates, system and initial estimate, recurrence and denominator/early-stop convention,
iteration count, exact-arithmetic boundary, ordered binders, hypotheses, conclusion, and every
degenerate case. An independent source reviewer must approve that crosswalk. Then the statement
phase can elaborate the exact Lean expression and run the required mutations.

Until that happens, `canonical_statement`, `canonical_claim`, the Lean module/expression and its
fingerprints, alternate encodings, obligation registry, and discovery protocol remain null. The
intake may be self-tested, but the statement, audit, proof, release, `AUDIT-Z`, and `THEOREM-Z`
gates remain open.
