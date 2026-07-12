# THM-M-0041 scope map

## Human claim selected at intake

For every finite square matrix `A` over a commutative ring, evaluating the characteristic
polynomial of `A` at `A` yields the zero matrix. The characteristic polynomial is provisionally
`det(X I - A)`, and evaluation is polynomial evaluation in the generally noncommutative matrix
algebra with scalar coefficients acting as scalar matrices.

This is a conventional repository-scope selection from a concise catalog gloss, not an `H0` source
finding. The statement phase has now elaborated, fingerprinted, boundary-tested, and mutation-tested
this exact selection; its provisional receipt still requires master acceptance. Immutable pinpoint
source fidelity remains independently open on the human-proof axis.

## Scope decisions

| Surface | Intake-selected meaning | Open verification |
|---|---|---|
| Matrix | finite square matrix indexed by one finite type | exact Lean carrier/binders frozen; source convention review open |
| Coefficients | arbitrary commutative ring | exact `CommRing` hierarchy frozen; historical source generality open |
| Characteristic polynomial | `det(X I - A)` | local expanded definition frozen; `Matrix.charpoly` transport is downstream |
| Evaluation | substitute `A`, with coefficients mapped to scalar matrices | exact `Polynomial.aeval` expression frozen |
| Conclusion | result equals the zero matrix | explicit universe/typeclass expression fingerprint frozen |

## Boundary cases

- The empty index type and the zero ring are included because the catalog excludes neither.
  `BoundaryProbe.lean` checks both, and the mutation adding `Nonempty` and `Nontrivial` is killed.
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

The statement phase has frozen the coefficient domain, index convention, expanded characteristic
polynomial, evaluation semantics, boundaries, minimal imports, fingerprints, and required mutation
classes. Master acceptance is pending. The source audit must still admit and independently review a
pinpoint source passage. The later anchor audit must check the `Matrix.charpoly` relationship and
inspect proof bodies, provenance, transitive dependencies, and trust closure of pinned candidates.
