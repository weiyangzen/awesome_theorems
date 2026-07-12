# THM-M-1237 frozen obligation tree

Item `S56-M-1237-OBLIGATION_TREE` freezes ten canonical obligations against the exact
`Statement.lean` target and the immutable candidate audit. All are root relevant and eligible for
machine, human-source, and readable review. No obligation is excluded or credited as closed.

## M1237-ROOT

The exact supercritical first-order Morrey-Sobolev statement. It is assembled only through `T`.

## M1237-S

Freeze dimensions, measurable bounded domain, strict `p > n`, exponent equality, concrete weak
derivative data, supplied extension data, and the `HolderRepresentative` conclusion.

## M1237-N

Normalize to the supplied whole-space extension while retaining its almost-everywhere agreement
and norm bound. This is not an extension-existence claim: the extension is an explicit hypothesis.

## M1237-B

Audit the empty-domain and zero-data cases and the positivity/range consequences of
`alpha = 1 - n/p` with `p > n`. The branch package must be exhaustive before proof acceptance.

## M1237-C

Construct a concrete representative and prove almost-everywhere agreement on `Omega`. This is an
open critical obligation represented by `RepresentativeFamily` in `ObligationTree.lean`.

## M1237-L-HOLDER

Prove the quantitative Morrey Holder estimate on `closure Omega`, with the exact exponent and the
encoded `W1p` norm. The anchor audit found no exact pinned theorem closing this obligation.

## M1237-L-VALUE

Prove the pointwise value estimate on `closure Omega` using the same chosen constant. It remains a
separate obligation because Holder control alone does not fix an additive constant.

## M1237-X-MATHLIB

Classify the pinned measure, derivative, `Lp` seminorm, and Holder API boundary. Candidate
Poincare/Sobolev inequalities and `HolderOnWith.continuousOn` are bridges, not root proof bodies.

## M1237-X-TRUST

Record the exact axiom and transitive trust closure for every eventual terminal declaration. The
composition harness currently reports only `propext`, `Classical.choice`, and `Quot.sound`.

## M1237-T

`Stage1Rev56.THMM1237.ObligationTree.root_compose` consumes the representative construction, Holder
estimate, and value estimate and builds the exact `HolderRepresentative`. Lean checks this
composition, but its premises remain open, so it gives no root proof credit.

The frozen minimal open root cut set is `M1237-C`, `M1237-L-HOLDER`, and `M1237-L-VALUE`. The root
is `M3`; audit completion and theorem completion are both false.

