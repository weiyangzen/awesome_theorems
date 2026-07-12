# THM-M-0041 scope map

## Human claim selected at intake

For every finite square matrix `A` over a commutative ring, evaluating the characteristic
polynomial of `A` at `A` yields the zero matrix. The characteristic polynomial is provisionally
`det(X I - A)`, and evaluation is polynomial evaluation in the generally noncommutative matrix
algebra with scalar coefficients acting as scalar matrices.

This is a conventional repository-scope selection from a concise catalog gloss, not an `H0` source
finding and not an accepted Lean statement. The statement phase must ratify it against an immutable
source packet, elaborate it, fingerprint it, and mutation-test it before tree construction.

## Scope decisions

| Surface | Intake-selected meaning | Open verification |
|---|---|---|
| Matrix | finite square matrix indexed by one finite type | exact source dimension/index convention and binder order |
| Coefficients | arbitrary commutative ring | source generality and exact Lean structure hierarchy |
| Characteristic polynomial | `det(X I - A)` | sign convention and checked definition unfolding |
| Evaluation | substitute `A`, with coefficients mapped to scalar matrices | exact `Polynomial.aeval` expression and noncommutative evaluation semantics |
| Conclusion | result equals the zero matrix | elaborated equality, universe, and typeclass fingerprint |

## Boundary cases

- The empty index type and the zero ring are provisionally included because the catalog excludes
  neither and the pinned matrix candidate supports them. The statement gate must test both rather
  than silently add `Nonempty`, positive dimension, or `Nontrivial`.
- Zero, identity, scalar, singular, noninvertible, nondiagonalizable, and repeated-eigenvalue
  matrices remain in scope.
- Rectangular matrices are excluded because the characteristic polynomial and self-evaluation root
  are selected for square matrices.
- Matrices over noncommutative coefficient rings are not selected. A different determinant or
  characteristic-polynomial theory would require a separately source-mapped statement.
- The finite free-module endomorphism form is a candidate alternate encoding. It may receive credit
  only after a checked relationship to the matrix root and all basis/choice assumptions are mapped.

## Non-substitution rules

- Do not replace the theorem by a fixed dimension, a field-only case, diagonalizable matrices,
  complex matrices, or a numerical example.
- Do not replace it by divisibility of the minimal polynomial, a recurrence for matrix powers, or
  trace/determinant/eigenvalue corollaries.
- Do not use the determinant identity `adj(X I - A) (X I - A) = charpoly(A) I` alone as terminal
  proof credit without the checked evaluation step.
- Do not confuse polynomial evaluation at the matrix with scalar evaluation at one eigenvalue.
- Do not substitute Hamiltonian mechanics, Hamiltonian graphs, or an attribution discussion for
  the algebraic matrix theorem.
- Do not treat the catalog's verified label, a declaration name, successful `#check`, or an axiom
  report as proof completion.

## Downstream handoff

The statement phase must admit and independently review a pinpoint source passage; freeze the
coefficient domain, dimension/index convention, characteristic polynomial, evaluation semantics,
and boundary cases; elaborate the minimal-import canonical target; record expression and environment
fingerprints; check the matrix/endomorphism relationship if credited; and distinguish the required
removed-hypothesis, changed-domain, changed-binder-scope, and boundary mutations. Only the later
anchor audit may inspect and classify proof bodies, provenance, transitive dependencies, and trust
closure of the pinned candidates.
