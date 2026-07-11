# THM-M-0085 frozen obligation architecture

Item: `S56-M-0085-OBLIGATION_TREE`.

The registry freezes five root-relevant obligations before the proof phase.
The mathlib body is counted once: the legacy wrapper and the `eqv` projection
do not create distinct terminal-proof credit.

## Typed proof route

```text
M0085-ROOT exact universal target
`-- M0085-B-INSTANCE install explicit creates premise as a local instance
    `-- M0085-A-BECK apply the pinned Beck constructor and project eqv
```

`M0085-X-PROVENANCE` records the immutable terminal body, import, revisions,
and trust boundary without becoming a proof premise. `M0085-W-RELEASE` keeps
the later named wrapper, validation, and release receipts out of proof-credit
metrics. Separate refinement, provenance, evidence, trust, documentation, and
workflow graphs encode those roles.

## Node ledger

### m0085-root

Exact `Stage1.THM_M_0085.Statement`. The anonymous composition probe shows an
eligible M0-P route, but this phase does not publish or accept the canonical
theorem declaration.

### m0085-b-instance

Convert the explicit proposition premise to the typeclass input expected by
mathlib using `letI`. This is a logical bridge, not an extra assumption.

### m0085-a-beck

Invoke the pinned `monadicOfCreatesGSplitCoequalizers` on the same `adj` and
project `eqv`, whose type is the fixed comparison functor's equivalence.

### m0085-x-provenance

Bind the unique terminal proof body to the anchor-audit revision and axiom
surface. It receives no distinct machine-proof denominator credit.

### m0085-w-release

Require the proof phase's named exact wrapper followed by node validation and
release receipts. Those future workflow acts cannot retroactively change this
frozen proof architecture.

## Freeze boundary

The architecture and checked child-to-parent composition are frozen. Root
closure remains unaccepted: there is no named proof-phase declaration, master
receipt, hermetic replay, independent validation, or release decision. Any
split, merge, correction, or eligibility change requires a new registry
version with an append-only delta.
