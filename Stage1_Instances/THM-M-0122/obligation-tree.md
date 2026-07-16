# THM-M-0122 frozen obligation architecture

Item: `S56-M-0122-OBLIGATION_TREE`

Registry v1 freezes 23 canonical obligations for the exact statement-phase
`FaltingsTarget`. The selected route passes to a pointed curve over a finite
number-field extension, embeds it in its Jacobian, applies Mordell-Weil and
Faltings/Mordell-Lang, excludes positive-dimensional cosets in the curve, and
transports the resulting finiteness back to the original rational points.

This is a proof architecture, not a proof. The anchor audit found no
placeholder-free terminal Lean body. `ObligationTree.lean` checks only the
abstract package composition and a generic finiteness transport. Every
arithmetic-geometric package remains an explicit premise.

## Proof Route

```text
M0122-ROOT
`-- M0122-T-TERMINAL
    |-- M0122-N-FINITE-EXTENSION
    |   |-- M0122-N-EXTENSION-EXISTS
    |   `-- M0122-N-BASE-CHANGE
    |-- M0122-C-ABEL-JACOBI
    |   |-- M0122-C-JACOBIAN
    |   `-- M0122-L-ABEL-JACOBI-INJECTIVE
    `-- M0122-L-MORDELL-LANG
        `-- M0122-X-IMPORTED-BOUNDARY
```

The refinement graph expands the aggregate Mordell-Lang package through
Mordell-Weil, the no-positive-coset lemma, the finite-intersection step, and
range transport. These refinements are not extra direct premises of the Lean
terminal composer. The separate refinement, provenance, evidence, trust,
documentation, and workflow graphs cannot become proof premises. No candidate,
receipt, or checkbox state is counted as an inhabited mathematical child.

### m0122-root

`M0122-ROOT` is the exact canonical proposition
`Stage1Instances.THMM0122.FaltingsTarget`. It consumes only the exact terminal
package. Status: `H1/M3/R3`, open.

### m0122-s-interface

`M0122-S-INTERFACE` freezes the universe, number-field binders, concrete
scheme and structure morphism, relative smoothness, projectivity through a
closed immersion, geometric connectedness, structure-sheaf `H^1` genus
condition, and rational sections. It shares the root expression fingerprint
and creates no second theorem.

### m0122-s-boundary

`M0122-S-BOUNDARY` retains the original universal scope. Genus zero and one,
non-number-field bases, singular or nonprojective curves, bounded-height
subsets, and finite generation are not substitutes. No hidden nonemptiness
hypothesis is added.

### m0122-s-point-transport

`M0122-S-POINT-TRANSPORT` records the checked section/slice-category point
equivalence `faltingsTarget_iff_over`. It changes representation only and
does not supply rational-point finiteness.

### m0122-s-foundation

`M0122-S-FOUNDATION` owns the eventual axiom, compiled-artifact, executable,
and TCB audit. The conditional composition currently reports only `propext`,
`Classical.choice`, and `Quot.sound`; that provisional observation is not an
accepted trust closure.

### m0122-n-finite-extension

`M0122-N-FINITE-EXTENSION` packages the reduction to a pointed curve over a
finite number-field extension while retaining an injection from `C(K)`.
`ObligationTree.lean` exposes its exact consumer interface but does not
construct the extension.

### m0122-n-extension-exists

`M0122-N-EXTENSION-EXISTS` must produce a finite extension on which the curve
has a rational point. It is a high-risk arithmetic-geometric leaf with an
explicit eight-step ceiling and no current formal body.

### m0122-n-base-change

`M0122-N-BASE-CHANGE` must construct the base-changed curve, preserve all
frozen hypotheses including the cohomological genus encoding, and prove the
map on rational points injective. Its ten-step ledger is a planning bound, not
closure evidence.

### m0122-c-abel-jacobi

`M0122-C-ABEL-JACOBI` packages the pointed curve's Jacobian and injective
Abel-Jacobi map on rational points. The package remains an uninhabited premise
of the checked terminal composer.

### m0122-c-jacobian

`M0122-C-JACOBIAN` constructs the Jacobian abelian variety and its rational
point group in a representation compatible with the frozen curve. No pinned
mathlib declaration currently supplies this package.

### m0122-l-abel-jacobi-injective

`M0122-L-ABEL-JACOBI-INJECTIVE` proves that the based Abel-Jacobi map for a
genus-greater-than-one curve is a closed immersion and hence injective on
rational points. It remains open.

### m0122-l-mordell-weil

`M0122-L-MORDELL-WEIL` establishes finite generation of the Jacobian's
rational points. The generic descent declaration found by the anchor audit is
only adjacent infrastructure and is not this result.

### m0122-l-mordell-lang

`M0122-L-MORDELL-LANG` is the central imported-theorem boundary: describe the
intersection of the Abel-Jacobi curve with the finitely generated group by a
finite union of cosets. It remains open and depends on
`M0122-X-IMPORTED-BOUNDARY`.

### m0122-l-no-positive-coset

`M0122-L-NO-POSITIVE-COSET` shows that the genus-greater-than-one curve image
contains no translate of a positive-dimensional abelian subvariety. This is a
material geometric lemma, not a routine cleanup.

### m0122-l-finite-intersection

`M0122-L-FINITE-INTERSECTION` combines the finite coset decomposition with
the no-positive-coset result to obtain finiteness of the curve image. Its
child-to-parent composition still needs an exact Lean certificate.

### m0122-t-terminal

`M0122-T-TERMINAL` composes normalization, Abel-Jacobi, and the aggregate
Mordell-Lang finiteness package. The checked declaration consumes those three
direct package children exactly. Mordell-Weil, no-positive-coset,
finite-intersection, and range transport refine the aggregate package in the
separate refinement graph and retain future composition obligations. No
premise is proved here.

### m0122-t-range-transport

`M0122-T-RANGE-TRANSPORT` is the generic checked fact that an injective map
with finite range has finite domain. It is not counted as a Faltings proof
body, and it cannot close any arithmetic-geometric child.

### m0122-x-imported-boundary

`M0122-X-IMPORTED-BOUNDARY` requires a placeholder-free exact
Faltings/Mordell-Lang body or compatible checked implementation. Northcott
sublevel finiteness, abstract descent, the mismatched peer dossier, and the
Atlas `by sorry` declaration are explicitly rejected as terminal bodies.

### m0122-x-source

`M0122-X-SOURCE` keeps the exact primary-source locator, assumption and
convention mapping, errata audit, and independent review open. A famous paper
title alone is not `H0`.

### m0122-x-provenance

`M0122-X-PROVENANCE` must resolve wrapper-to-terminal-body identity, complete
declaration/import closure, immutable source bytes, revision, origin, and
license without multiplying aliases.

### m0122-x-trust

`M0122-X-TRUST` owns the exact terminal object's axioms, unsafe/oracle status,
compiled dependencies, executable identities, and replay boundary.

### m0122-x-readable

`M0122-X-READABLE` requires an independently reviewed node-by-node proof
reconstruction. This architecture page names the route and open boundaries;
it is not `R0` and does not narrate open premises as completed mathematics.

### m0122-x-workflow

`M0122-X-WORKFLOW` binds dependency-ordered phase acceptance, validation,
freshness, revocation, independent verification, and release. Worker
self-testing cannot satisfy master acceptance or a terminal decision.

## Leaf Ledgers

Every node owns one structured semantic step in `typed-graphs.json`. Each step
names its premise IDs, inference or source, exact output, and outgoing use.
The substantive planned leaves have explicit bounds of 4 to 18 steps in the
registry; those bounds force later splitting if exceeded and never imply
proof, source, or readability closure.

## Frozen Boundary

The registry denominator is content-addressed in `obligation-registry.json`.
Any target correction, split, merge, eligibility change, or exclusion requires
registry v2 with an append-only delta. No obligation is accepted closed. H0,
root M0, R0, transitive provenance and trust, hermetic replay, independent
validation, `AUDIT-Z`, `THEOREM-Z`, release, and master acceptance remain open.
