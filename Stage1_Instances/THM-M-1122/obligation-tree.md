# THM-M-1122 frozen obligation architecture

Item: `S56-M-1122-OBLIGATION_TREE`.

The registry freezes 11 root-relevant obligations before proof execution. It separates the actual
Schramm identification argument from definitions, source evidence, trust, provenance, and workflow.
The opaque interfaces in `Statement.lean` define the exact selected proposition but do not discharge
any of the domain-specific obligations below.

## Typed proof route

```text
M1122-ROOT exact canonical proposition
`-- M1122-T-ASSEMBLE checked definitional composition
    `-- M1122-L-IDENTIFICATION conditional equality in distribution
        |-- M1122-S-INTERFACES faithful measurable objects and predicates
        |-- M1122-C-CONJECTURE exact Conjecture 1.2 interface
        |-- M1122-C-LERW LERW scaling-limit construction and measurability
        |-- M1122-C-BROWNIAN uniform circle Brownian driver
        `-- M1122-C-LOEWNER normalized radial trace with driver B(-2t)
```

`M1122-S-FOUNDATION`, `M1122-X-SOURCE`, and `M1122-X-PROVENANCE` are independent trust,
documentation, and provenance requirements. They cannot be counted as proof premises or proof bodies.

## Node ledger

### m1122-root
Exact elaborated conditional target. `[H2, M3, R4]`; no inhabitant is present.

### m1122-s-interfaces
Replace the current explicit interface parameters with source-faithful measurable curve, convergence,
circle Brownian, and radial Loewner definitions, with checked transports back to the frozen target.

### m1122-s-foundation
Record the full import/declaration closure, axioms, classical choice, TCB, and no-oracle policy.

### m1122-c-conjecture
Formalize Conjecture 1.2, including topology on curves, convergence mode, domains, and quantifiers.
The target is conditional, so this node supplies a typed hypothesis rather than proving the conjecture.

### m1122-c-lerw
Construct the LERW scaling-limit random curve from `0` to the unit-circle boundary and prove its
measurability under the frozen law.

### m1122-c-brownian
Construct Brownian motion on the unit circle with uniform initial point and the variance/time convention
used in Theorem 1.3.

### m1122-c-loewner
Construct and characterize the normalized radial Loewner solution of equations (1.1)-(1.3), including
the trace, terminal point, measurability, and the source time substitution `B(-2t)` for `t <= 0`.

### m1122-l-identification
Prove the substantive conditional law identification: Conjecture 1.2 plus the preceding constructions
implies `IdentDistrib sigma lerwScalingLimit muBrownian muLERW`. `[H2, M4, R4]`; no eligible Lean
proof anchor was found. Its 100-step budget is a split threshold, not permission to hide dependencies.

### m1122-t-assemble
`root_of_conditionalIdentification` is a kernel-checked definitional transport from the preceding
package to the exact root. `[H2, M0-L, R4]`; its explicit premise prevents root proof credit.

### m1122-x-source
Complete a theorem/page/equation/assumption/errata crosswalk for every semantic node and obtain
independent source review.

### m1122-x-provenance
Resolve every terminal body and transitive import, axiom, license, receipt, archive, and replay input.

## Freeze boundary

The minimal open proof cut is `M1122-L-IDENTIFICATION`. Closing it requires the five refinement
obligations, not an axiom or a strengthened premise. This phase supplies a frozen registry and checked
composition boundary only; it supplies no root closure, audit completion, or theorem completion.
Any later correction, split, merge, or eligibility change requires a new registry version and an
append-only ID delta.
