# THM-M-0590 frozen obligation tree

Registry version 1 freezes 17 semantic obligations before proof work. The
machine denominator is the 15 obligations marked `required`; the source-only
and provenance overlays cannot add proof credit. Every leaf below has an
explicit budget of at most 100 substantive steps, but that budget is only a
decomposition boundary, not evidence of closure.

## M0590-ROOT

The exact target is `THMM0590.brownDouglasFillmoreTarget`. It is open at `M4`.
Its proof path requires the checked final assembly node, which in turn requires
both directional packages.

## M0590-S-DEFINITIONS

The local Fredholm predicate, integer index, essential spectrum, essential
normality, and unitary-equivalence-modulo-compacts definitions elaborate in
`Statement.lean`. This node fixes notation only and supplies no classification.

## M0590-S-DOMAINS

The root quantifies over possibly different separable infinite-dimensional
complex Hilbert spaces and bounded endomorphisms. The hypotheses and the
off-spectrum lambda scope remain exactly as elaborated.

## M0590-S-BOUNDARY

Proof work must preserve the normal-operator boundary, exclude finite-dimensional
domains, and compare indices only away from the essential spectrum. Exact
boundary lemmas are open.

## M0590-S-FOUNDATION

A release needs the transitive declaration, axiom, quotient, classical-choice,
TCB, and no-oracle inventory. The conditional composition currently reports
only `propext`, `Classical.choice`, and `Quot.sound`; this is not the eventual
terminal proof closure.

## M0590-N-CALKIN

Construct the quotient of bounded operators by compact operators and prove that
compactness of the self-commutator is equivalent to normality of the quotient
image. This representation-crossing node is critical and open.

## M0590-N-FREDHOLM

Prove the Atkinson bridge between the local kernel/cokernel/closed-range
definition and invertibility modulo compacts, including the frozen `T - lambda I`
index sign. This critical transport is open.

## M0590-L-FWD-SPECTRUM

From unitary conjugacy modulo compacts, derive equality of the essential spectra
using the checked Calkin bridge. Open.

## M0590-L-FWD-INDEX

For every off-spectrum lambda, prove invariance of Fredholm index under unitary
conjugacy and compact perturbation. Open.

## M0590-B-FORWARD

Combine the two forward invariant nodes to inhabit
`THMM0590.ForwardInvariantPackage`. The package is an explicit proposition, not
an axiom or theorem claim, and remains open.

## M0590-C-BUSBY

For a common essential spectrum `X`, construct the Busby extension of `C(X)` by
the compact operators, with functional-calculus well-definedness, compatibility,
and independence-of-choice obligations. Open.

## M0590-L-EXT-CLASS

Formalize the BDF extension classification with precisely the equivalence that
yields a unitary conjugacy error in the compact ideal. A citation or one-line
invocation cannot close this bridge. Open.

## M0590-L-INDEX-COMPLETE

Show that the off-spectrum index function completely determines the relevant
extension class over the common essential spectrum. This is a central bridge,
not a definitional rewrite. Open.

## M0590-T-BACKWARD

Compose the Calkin, Busby, extension-classification, and index-completeness
nodes to inhabit `THMM0590.BackwardClassificationPackage`. Open.

## M0590-T-ASSEMBLE

`THMM0590.root_of_directional_packages` kernel-checks the exact biconditional
from the forward and backward packages and consumes both premises. It proves
only conditional composition; neither package has a proof body.

## M0590-X-SOURCE

Every analytic and extension-theoretic node needs a primary-source theorem/page
pinpoint, premise crosswalk, convention check, errata review, and independent
approval. The existing bibliography is `H1`, so this overlay remains open and
provides no machine credit.

## M0590-X-PROVENANCE

The proof phase must populate terminal body identities and declaration origins;
validation must derive the full dependency, axiom, TCB, license, and replay
closure. This informational overlay remains open and cannot close the root.

## Graph boundary

Typed proof edges are reciprocal `proof_requires`/`composes` pairs. Refinement,
source, provenance, trust, documentation, and workflow graphs are separate in
`typed-graphs.json`; none is silently interpreted as a proof premise. The current
root cut set is `M0590-B-FORWARD` and `M0590-T-BACKWARD`. The theorem, source
audit, readability review, validation, and release decisions all remain open.
