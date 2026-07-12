# THM-M-1111 obligation registry and typed graphs

Version 1 freezes 19 root-relevant obligations before proof execution. The proof route follows the
selected Tao-Vu theorem: implement the random-matrix semantics, normalize the ensembles, construct
an entry-replacement chain, establish the good-configuration estimates, perform a Taylor/resolvent
expansion, cancel matched moments, control the remainder and bad event, and telescope diagonal and
off-diagonal replacements. Source, provenance, trust, evidence, documentation, and workflow edges
are stored separately from proof edges in `typed-graphs.json`.

## M1111-ROOT
Exact `TaoVuFourMomentTarget S`; open at M3.

## M1111-S-DEFS
Implement source-faithful random Hermitian ensembles and every field of `FourMomentSemantics`.

## M1111-S-DOMAIN
Preserve all uniformities, quantifier dependencies, matching orders, derivatives, and bulk indices.

## M1111-S-BOUNDARY
Handle index feasibility and the small dimensions absorbed by the large-`n` threshold.

## M1111-S-FOUNDATION
Audit foundations, imports, transitive axioms, and the TCB.

## M1111-N-NORMALIZE
Align matrix and eigenvalue scaling with the pinned source conventions.

## M1111-C-REPLACEMENT
Construct the Hermitian entry-by-entry replacement chain.

## M1111-L-GOODCONFIG
Obtain the uniform good-configuration event used at each swap.

## M1111-L-RIGIDITY
Supply the required bulk localization, gap, and eigenvector/resolvent estimates.

## M1111-L-TAYLOR
Expand the eigenvalue observable for one entry replacement through the source-required order.

## M1111-L-MOMENT
Cancel coefficients by fourth-order off-diagonal and second-order diagonal matching.

## M1111-L-REMAINDER
Control Taylor remainders and bad-event contributions quantitatively.

## M1111-B-OFFDIAGONAL
Compose every off-diagonal replacement.

## M1111-B-DIAGONAL
Compose every diagonal replacement with its distinct order-two argument.

## M1111-T-TELESCOPE
Sum replacement errors and choose a uniform threshold and positive exponent.

## M1111-T-ASSEMBLE
The checked conditional transport returns the exact root from the still-open comparison package.

## M1111-X-SOURCE
Pinpoint primary-source support for every material transition.

## M1111-X-PROVENANCE
Close terminal proof-body and declaration provenance without adding proof credit.

## M1111-X-TRUST
Close executable, dependency, computation, and compiled-artifact trust boundaries.

## Boundary

Only `M1111-T-ASSEMBLE` has a checked body, and that body consumes the comparison package as an
explicit premise. The semantic interface contains arbitrary operations and predicates but no laws;
therefore it is not a formalization of Wigner matrices and cannot support proof completion. The
root, analytic children, source review, trust closure, H0/R0, validation, and release remain open.
