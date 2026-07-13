# THM-M-0063 frozen obligation architecture

## Freeze boundary

Registry version 1 freezes 22 canonical obligations against the exact elaborated statement and the
bounded immutable anchor audit. Eligibility follows the faithful-action construction rather than
candidate availability: pointwise faithfulness gives permutation-homomorphism injectivity; a
chosen left inverse and `MulEquiv.ofLeftInverse'` give the range equivalence; specialization to the
left-regular action yields the exact root. Any correction, split, merge, exclusion, risk, or body
identity change requires registry version 2 with an append-only delta.

The direct Cayley declaration, the `MonoidHom.ofInjective` fallback, and external teaching wrappers
deduplicate to the same regular-action injectivity and range-equivalence construction. Statement
interfaces and transports are informational overlays and cannot inflate proof or proof-body credit.

## Typed proof route

```text
M0063-ROOT exact canonical statement [open M3]
`-- M0063-T-ASSEMBLE exact conditional assembly
    |-- M0063-N-REGULAR generalized-to-regular specialization
    |   `-- M0063-L-REGULAR-FAITHFUL evaluate the regular action at 1
    `-- M0063-T-GENERAL generalized faithful-action range equivalence [remaining cut]
        |-- M0063-C-PERM-HOM construct the action homomorphism
        |-- M0063-L-INJECTIVE faithful action gives injective toPermHom
        |   `-- M0063-L-POINTWISE faithful action separates elements
        |-- M0063-C-LEFT-INVERSE choose a left inverse from injectivity
        |-- M0063-C-MRANGE-EQUIV build MulEquiv to the monoid range
        `-- M0063-N-MRANGE-RANGE transport mrange to subgroup range
```

`M0063-C-PERM-HOM` refines the generalized package's action-homomorphism construction.
`M0063-S-EXACT`, `S-DOMAIN`, `S-BOUNDARY`, `S-TRANSPORT`, and `S-FOUNDATION` separately own the
statement, carrier/action contract, degenerate carriers, one-way catalog transport, and logical/TCB
boundary. The `X-*` obligations keep upstream identity, human source, provenance, trust,
documentation, and workflow out of the mathematical proof edge relation.

## Layer decisions

There is no mathematical branch split: the same symbolic construction applies to trivial, finite,
and infinite groups. `M0063-S-BOUNDARY` records that fact, but the branch layer remains
`not_applicable_pending_independent_approval`. No computation, certificate, solver, oracle, native
evaluation, or experimental result is used. The external/trust layer is nevertheless required for
the pinned mathlib proof body. These inapplicability decisions are proposals, not reviewer approval.

## Node ledger

### m0063-root

The root is exactly `Stage1Instances.THM_M_0063.CayleyTheoremTarget`, fingerprinted by the statement
gate. Its only proof child is exact assembly; its vector stays `[H1, M3, R4]`.

### m0063-s-exact

This overlay fixes `forall G : Type u, [Group G], Nonempty (G ≃* range)` and shares the root
statement fingerprint without duplicating root proof credit.

### m0063-s-domain

The carrier is arbitrary and universe-polymorphic. `MulAction.toPermHom G G` is the inferred left
action into `Equiv.Perm G`, and its range is the subgroup used in the conclusion.

### m0063-s-boundary

Trivial, finite, and infinite carriers remain in scope. There is no `Nontrivial`, `Finite`,
`Fintype`, or `DecidableEq` premise and no corresponding proof case split.

### m0063-s-transport

The checked statement theorem chooses the regular homomorphism range as the existential permutation
subgroup. Only canonical-to-existential implication is credited; no converse is asserted.

### m0063-s-foundation

This certificate owns the eventual transitive comparison with the selected foundation and TCB
profiles. Current probes report `propext`, `Classical.choice`, and `Quot.sound`; complete acceptance
is later work.

### m0063-n-regular

`exactTarget_of_generalFaithfulAction` checks the representation boundary: it specializes a
general faithful-action package to `H = G`. The package remains an explicit premise.

### m0063-c-perm-hom

`MulAction.toPermHom` packages an action into a monoid homomorphism whose values are permutations.
Its construction and multiplicativity are an imported proof boundary, not notation to ignore.

### m0063-l-pointwise

Faithfulness means that two group elements acting identically on every point are equal. For the
regular action this ultimately separates elements by evaluating at the identity and cancellation.

### m0063-l-regular-faithful

The left-regular action is faithful. Equality of the actions of `g` and `h`, evaluated at `1`,
reduces to `g = h`. `exactTarget_of_generalFaithfulAction` consumes this interface explicitly.

### m0063-l-injective

`genericInjectivity_of_pointwiseFaithfulness` evaluates equality of two output permutations at each
point and consumes `M0063-L-POINTWISE`. This conditionally checks the interface of
`MulAction.toPerm_injective` without installing its pinned body.

### m0063-c-left-inverse

An injective action homomorphism has a chosen left inverse. This is where `hasLeftInverse`,
`Classical.choose`, and `Classical.choose_spec` enter the audited mathlib body.

### m0063-c-mrange-equiv

Given a homomorphism and a specified left inverse, `MulEquiv.ofLeftInverse'` builds the
multiplicative equivalence with `MonoidHom.mrange`. This node does not conflate that monoid range
with the target's subgroup range.

### m0063-n-mrange-range

The audited Cayley body's type crosses from `MonoidHom.mrange` in `MulEquiv.ofLeftInverse'` to the
group homomorphism's `Subgroup` range. This obligation owns and must validate that representation
transport rather than hiding it in the constructor citation.

### m0063-t-general

`generalPackage_of_components` consumes the action-homomorphism construction, injectivity, the
left-inverse constructor, the exact mrange constructor, and the mrange-to-subgroup-range transport.
All five interfaces remain hypotheses in this phase.

### m0063-t-assemble

`exactAssembly_of_components` consumes both the regular-specialization interface and generalized
package. `root_of_exactAssembly` then maps the exact assembly to the literal root without adding a
premise or weakening the conclusion.

### m0063-x-upstream

The pinned terminal is `Equiv.Perm.subgroupOfMulAction` at mathlib revision `8a178386ffc0`. The
anchor audit records its exact six-line source region, body hash, Apache-2.0 license, and duplicate
wrapper family. This remains candidate rather than accepted proof evidence.

### m0063-x-source

The 1854 Cayley paper is only a bibliographic primary-source lead. Pinpoint passage, historical
definitions, assumptions, corrections, modern transport, node crosswalk, and independent review
remain open, so no H0 is claimed.

### m0063-x-provenance

Proof-phase work must traverse the actual terminal declarations and transitive body closure, bind
source and license hashes, and deduplicate wrappers by terminal proof-body identity.

### m0063-x-trust

Release requires machine-derived transitive axioms, compiled artifacts, executables, and TCB
inventory. Unknown trust fails closed; the current local composition checks are not that release
evidence.

### m0063-x-documentation

This file supplies stable architecture anchors only. It is not the independently reviewed R0
reconstruction required for readable closure.

### m0063-x-workflow

The master-owned task DAG orders anchor audit, this freeze, proof, validation, and release. This
worker does not edit that DAG or accept any receipt.

## Status boundary

`ObligationTree.lean` checks five conditional composition declarations, proves the definitional
`mrange`-to-subgroup-range transport, and returns the exact root
only from explicit child packages. It never invokes `Equiv.Perm.subgroupOfMulAction` and therefore
does not close Cayley's theorem. Accepted closed obligations and accepted receipt IDs remain empty;
the root stays `[H1, M3, R4]`. H0 source fidelity, proof integration, transitive provenance/trust,
R0 reconstruction, hermetic and independent validation, AUDIT-Z, theorem completion, and master
acceptance remain open.
