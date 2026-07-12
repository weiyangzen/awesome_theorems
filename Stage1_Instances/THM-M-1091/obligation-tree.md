# THM-M-1091 frozen obligation architecture

## Freeze boundary

Registry version 1 freezes twelve canonical obligations before proof-phase closure metrics are
observed. Nine are mathematical/formal obligations and three are provenance, trust, and workflow
overlays with no independent proof credit. The ordered denominator and canonical digest are stored
in `obligation-registry.json`. Any later split, merge, exclusion, or eligibility change requires a
new registry version and an append-only delta.

The root is exactly the homogeneous discrete-time Markov-kernel statement frozen in
`statement.json`. The general inhomogeneous three-time equation and continuous-time semigroups stay
outside this target; this tree does not broaden the selected theorem.

## Typed proof route

```text
M1091-ROOT exact frozen kernel equation [open M1]
`-- M1091-T-ASSEMBLE conditional exact composition
    |-- M1091-L-POWADD pinned central bridge [open proof-phase cut]
    `-- M1091-N-ADD index swap and n+m = m+n

M1091-S-CONTEXT       binders, typeclasses, degenerate-state policy
M1091-S-ORIENTATION   chronological composition direction
M1091-S-INTEGRAL      checked setwise integral equivalence
M1091-B-ZERO          both identity-kernel boundaries
M1091-C-POWCOMP       kernel-power construction semantics
M1091-X-PROVENANCE    pinned body identity and axiom inventory
M1091-X-TCB           release trust boundary
M1091-W-FOLLOWUP      proof, validation, release ordering
```

The proof graph has reciprocal `proof_requires` and `composes` edges. Refinement, provenance,
evidence, trust, documentation, and workflow edges live in separate graphs in `typed-graphs.json`;
none can masquerade as a proof premise.

## Node ledgers

### root

The conclusion is exactly `ChapmanKolmogorovTarget`, including arbitrary measurable state types,
the Markov-kernel instance, all natural step counts, and the frozen composition orientation.

### s-context

No finiteness, countability, nonemptiness, irreducibility, positivity, or standard-Borel assumption
is introduced. Natural step counts include zero.

### s-orientation

`(kappa ^ n) comp (kappa ^ m)` means that the `m`-step transition acts first. This explicit node
prevents the displayed order of `Kernel.pow_add` from silently reversing the intended chronology.

### s-integral

The already checked `target_iff_integralTarget` transports both ways between kernel equality and
the measurable-set lintegral equation. It is not a second semantic proof obligation.

### n-add

The audited anchor is instantiated at `n,m`; `add_comm` changes `n+m` to the frozen `m+n`. No
kernel-equality symmetry or hidden composition rewrite is used.

### b-zero

Both `m=0` and `n=0` reduce to left or right composition with `Kernel.id`.
`ObligationTree.lean` checks both boundary theorems.

### c-powcomp

Kernel exponentiation is the iterated-composition construction underlying the bridge. Its identity
and composition APIs are formulation dependencies, not separately credited terminal proofs.

### l-powadd

This is the central imported theorem package. The anchor audit identifies
`ProbabilityTheory.Kernel.pow_add` at mathlib revision `8a178386...`, but the obligation remains
open here because adoption and proof credit belong to the dependent proof phase.

### t-assemble

`compose_root` binds the exact child proposition as a named hypothesis, consumes it at swapped
indices, applies only addition commutativity, and returns the exact root. This is a checked
child-to-parent composition certificate, not closure of its child.

### x-provenance

The terminal body is the pinned mathlib `Kernel.pow_add`, rather than the repo-local wrappers or
the composition harness. Wrapper names receive no duplicate credit.

### x-tcb

The observed candidate axiom set is `propext`, `Classical.choice`, and `Quot.sound`. Transitive
trust, hermetic replay, supply chain, freshness, and independent verification remain release gates.

### w-followup

Proof adoption must precede validation, which must precede release. Human source fidelity remains
`H1`, and readable independent review remains open.

## Status boundary

This phase freezes architecture and validates conditional composition and boundary cases. It uses
no `sorry`, axiom declaration, placeholder, external solver, or fetched dependency. No obligation
is marked closed; no H0, M0, R0, audit completion, theorem completion, or master acceptance is
claimed.
