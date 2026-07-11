# THM-M-0418 frozen obligation architecture

Item: `S56-M-0418-OBLIGATION_TREE`.

The registry freezes 14 semantic obligations. Its proof graph follows the
actual body of `NumberField.exists_ideal_in_class_of_norm_le` at pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`. All proof nodes share that
one terminal body identity; wrappers and source mappings receive no duplicate
proof credit.

## Typed proof route

```text
M0418-ROOT exact canonical proposition
`-- M0418-T-ADAPTER exact repo-local adapter
    `-- M0418-T-UPSTREAM-BODY pinned mathlib terminal
        |-- M0418-N-INVERSE-CLASS choose J representing C^-1
        |-- M0418-L-MINKOWSKI-ELEMENT obtain nonzero a in J with norm bound
        |-- M0418-C-QUOTIENT-IDEAL construct I0 from J * I0 = span(a)
        |-- M0418-C-NONZERO-IDEAL prove I0 != 0 and package I
        |-- M0418-L-CLASS-IDENTITY prove mk0 I = C
        `-- M0418-L-NORM-TRANSPORT derive the required absNorm inequality
```

The refinement, provenance, evidence, trust, documentation, and workflow
graphs are stored separately in `typed-graphs.json`; none is counted as a
proof premise.

## Node ledger

### m0418-root
Exact elaborated representative target. Machine route is `M0-W`; human-source
and readable release gates remain open.

### m0418-s-target
Freezes the nonzero ideal subtype, class orientation, weak endpoint, explicit
constant, universes, and typeclass context.

### m0418-s-boundary
Degree one, totally real fields, zero complex places, and equality at the bound
remain in scope. No extra nondegeneracy hypothesis is introduced.

### m0418-s-foundation
The current axiom report is `propext`, `Classical.choice`, and `Quot.sound`.
Full transitive TCB and release replay remain validation work.

### m0418-n-inverse-class
Surjectivity of `ClassGroup.mk0` supplies a representative of `C^-1`; this is
the orientation normalization later undone by inversion.

### m0418-l-minkowski-element
The geometry-of-numbers engine supplies nonzero `a` in the chosen fractional
ideal with the discriminant-dependent norm estimate.

### m0418-c-quotient-ideal
Membership of `a` yields an integral quotient ideal `I0` satisfying the
principal-product identity used by both remaining conclusions.

### m0418-c-nonzero-ideal
A contradiction through the principal-product identity proves `I0 != 0`, so
it can be packaged as the required nonzero ideal subtype.

### m0418-l-class-identity
`ClassGroup.mk0_eq_mk0_inv_iff` converts the product identity into the class
equation and cancels the earlier inverse choice.

### m0418-l-norm-transport
Fractional-ideal norm identities rewrite the Minkowski estimate to `absNorm I`;
positivity of the representative norm justifies cancellation.

### m0418-t-upstream-body
The explicit `by` proof in pinned `ClassNumber.lean:77-100` composes the six
substantive packages. This is the sole distinct terminal body.

### m0418-t-adapter
The local wrapper applies the upstream theorem at the exact canonical binders.
It is a transport and earns no independent terminal-body credit.

### m0418-x-source
The node-level primary human-source edition/page/assumption/errata crosswalk is
still pending, so H0 is not claimed.

### m0418-x-provenance
The anchor audit records the immutable mathlib revision, source hash, license,
direct body dependencies, wrapper, and provisional axiom surface. Release-grade
transitive provenance remains a later gate.

## Freeze boundary

The proof cut set is empty for machine closure because the pinned terminal body
is locally checkable, but the release cut set is not: primary-source acceptance,
R0 reconstruction, hermetic replay, and independent validation remain open.
This phase does not claim audit completion, theorem completion, or a master
receipt. Any eligibility or architecture change requires a new registry version
and append-only delta.
