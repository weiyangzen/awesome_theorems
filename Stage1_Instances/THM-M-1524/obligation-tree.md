# THM-M-1524 frozen obligation architecture

The canonical route centers both observable vectors, uses symmetry and the explicit product-domain
witnesses to relate their inner products to the commutator expectation, applies Cauchy-Schwarz, and
obtains Robertson. The CCR component rewrites the commutator expectation to `i * hbar` on a unit
state, evaluates its norm using `0 <= hbar`, and specializes Robertson. The two exact component
conclusions are then paired into the frozen root.

## m1524-root
Exact canonical conjunction; open.
## m1524-s-definitions
Checked observable, expectation, deviation, commutator, and self-adjointness definitions.
## m1524-s-domains
Checked dense domain and both product-domain interfaces.
## m1524-s-boundary
Checked statement boundary retaining zero deviation, `hbar = 0`, and arbitrary complex Hilbert spaces.
## m1524-s-foundation
Release-time transitive axiom and TCB audit; open.
## m1524-n-center
Centered-vector construction and deviation identities; open.
## m1524-l-symmetry
Commutator/centered-inner-product identity from symmetry; open critical lemma.
## m1524-l-cauchy-schwarz
Kernel-checked pinned mathlib Cauchy-Schwarz leaf.
## m1524-l-robertson
Conditional combination into the exact Robertson target; open until its three children close.
## m1524-l-ccr-scalar
CCR expectation and scalar-norm evaluation under normalization and nonnegative `hbar`; open.
## m1524-t-ccr
Transport from exact Robertson to the CCR-specialized target; open.
## m1524-t-assemble
Kernel-checked conditional pairing of the two exact target components.
## m1524-x-source
Primary-source pinpoint and assumption crosswalk; open and carries no machine credit.
## m1524-x-provenance
Release provenance overlay; open and carries no proof credit.

The branch layer is inapplicable because this route has no mathematical case split: the explicit
`0 <= hbar` premise permits a uniform scalar-norm proof, including `hbar = 0`. Every leaf has a
40-step split budget. The minimal open root cut set is `M1524-N-CENTER`, `M1524-L-SYMMETRY`, and
`M1524-L-CCR-SCALAR`.
