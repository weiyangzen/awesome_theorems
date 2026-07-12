# Frozen obligation architecture

## Freeze boundary

This is registry version 1 for `S56-M-1041-OBLIGATION_TREE`. It freezes 21
root-relevant obligations before proof execution. Eligibility does not depend
on proof availability. Planned fingerprints describe intended interfaces, not
Lean evidence. Corrections, splits, merges, or exclusions require a new
registry version and an append-only delta.

## Typed proof route

```text
M1041-ROOT exact canonical equivalence
`-- M1041-T-ASSEMBLE checked conditional composition
    |-- M1041-F-ASSEMBLE generation implies resolvent conditions
    |   |-- M1041-F-CLOSED
    |   |-- M1041-F-DENSE
    |   |-- M1041-F-RESOLVENT-RIGHT
    |   |   `-- M1041-F-RESOLVENT-CONSTRUCT
    |   |-- M1041-F-RESOLVENT-LEFT
    |   |   `-- M1041-F-RESOLVENT-CONSTRUCT (shared body)
    |   `-- M1041-F-RESOLVENT-BOUND
    |       `-- M1041-F-RESOLVENT-CONSTRUCT (shared body)
    `-- M1041-C-ASSEMBLE resolvent conditions imply generation
        |-- M1041-C-SEMIGROUP-CONSTRUCT
        |   `-- M1041-C-YOSIDA-APPROX
        |-- M1041-C-SEMIGROUP-LAWS
        |   `-- M1041-C-SEMIGROUP-CONSTRUCT (shared body)
        |-- M1041-C-STRONG-CONTINUITY
        |   `-- M1041-C-SEMIGROUP-CONSTRUCT (shared body)
        |-- M1041-C-CONTRACTION
        |   `-- M1041-C-SEMIGROUP-CONSTRUCT (shared body)
        `-- M1041-C-GENERATOR
            |-- M1041-C-SEMIGROUP-CONSTRUCT (shared body)
            `-- M1041-C-YOSIDA-APPROX (shared body)
```

The definition, boundary, foundation, source, provenance, documentation, and
workflow graphs are separately typed. The external partial anchor may support
forward children only after pinning, local elaboration, exact adapters, axiom
inspection, and terminal-body provenance; it cannot close `F-ASSEMBLE` or the
root by itself.

## Node ledger

### m1041-root
Exact frozen contraction Hille--Yosida target. `[H2, M4, R4]`; open.

### m1041-s-definitions
Checked semigroup, generator, and two-sided resolvent vocabulary.
`[H2, M0-L, R4]`; statement evidence only.

### m1041-s-boundary
Checked expanded transport preserving real scalars, nonnegative time, strict
positive resolvent parameters, and the zero space. `[H2, M0-L, R4]`.

### m1041-s-foundation
Pending transitive imports, axioms, classical-choice, integration theory, TCB,
and no-oracle certificate. `[H2, M4, R4]`.

### m1041-f-closed
Generator closedness from the semigroup and derivative graph. Budget 100;
`[H2, M4, R4]`.

### m1041-f-dense
Density of the generator domain from strong continuity. Budget 100;
`[H2, M4, R4]`.

### m1041-f-resolvent-construct
Construct the Laplace/Bochner resolvent for every positive parameter and prove
its bounded-linear-map invariants. Shared terminal body; budget 100;
`[H2, M4, R4]`.

### m1041-f-resolvent-right
Range-in-domain and right-inverse equation. The audited external project is
only a prospective `E3/M3` child anchor. Budget 100; `[H2, M4, R4]`.

### m1041-f-resolvent-left
Left inverse on every point of `A.domain`; absent from the audited external
anchor. Budget 100; `[H2, M4, R4]`.

### m1041-f-resolvent-bound
The `a^-1` contraction resolvent estimate. Prospective external partial anchor,
with no local proof credit yet. Budget 100; `[H2, M4, R4]`.

### m1041-f-assemble
Combine all forward fields into `ForwardPackage`. Minimal forward cut;
`[H2, M4, R4]`.

### m1041-c-yosida-approx
Construct bounded Yosida approximants with compatibility and convergence
estimates. Budget 100; `[H2, M4, R4]`.

### m1041-c-semigroup-construct
Construct the limiting semigroup from exponentials of approximants. Budget
100; `[H2, M4, R4]`.

### m1041-c-semigroup-laws
Prove identity and composition laws for the limit. Budget 100;
`[H2, M4, R4]`.

### m1041-c-strong-continuity
Prove continuity of every orbit. Budget 100; `[H2, M4, R4]`.

### m1041-c-contraction
Pass approximant bounds to the limiting contraction estimate. Budget 100;
`[H2, M4, R4]`.

### m1041-c-generator
Identify the strong right-derivative graph at zero with `A`. Budget 100;
`[H2, M4, R4]`.

### m1041-c-assemble
Combine construction and invariants into `ConversePackage`. Minimal converse
cut; `[H2, M4, R4]`.

### m1041-t-assemble
`root_of_directionPackages` kernel-checks the final `Iff` composition while
keeping both directions explicit premises. `[H2, M0-L, R4]`; conditional
composition is not root proof credit.

### m1041-x-source
Pending primary-source theorem/page/assumption/convention/errata mapping for
every analytic bridge. `[H2, M4, R4]`.

### m1041-x-provenance
Pending terminal-body, shared-body, external-anchor, import, axiom, TCB, and
replay inventory. Informational overlay; `[H2, M4, R4]`.

## Status boundary

The frozen root cut is `{M1041-F-ASSEMBLE, M1041-C-ASSEMBLE}`. Shared
construction bodies are counted once. The checked final composition introduces
no Hille--Yosida proof. This phase claims no H0, root closure, audit completion,
theorem completion, or accepted receipt.
