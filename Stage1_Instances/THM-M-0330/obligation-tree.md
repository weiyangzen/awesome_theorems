# THM-M-0330 frozen obligation architecture

Item: `S56-M-0330-OBLIGATION_TREE`.

The version-1 registry freezes 19 semantic obligations before proof execution.
It selects the Laplace-resolvent forward route and Yosida-approximation converse
route for the exact real contraction theorem. This choice does not assert that
either analytic package is available in Lean.

## Typed proof route

```text
M0330-ROOT exact canonical proposition
`-- M0330-T-ASSEMBLE checked conditional iff composition
    |-- M0330-B-FORWARD exact semigroup-to-resolvent implication
    |   |-- M0330-L-FWD-DENSE generator domain is dense
    |   |-- M0330-L-FWD-CLOSED generator graph is closed
    |   `-- M0330-C-LAPLACE-RESOLVENT construct the resolvent
    |       `-- M0330-L-RESOLVENT-LAWS two inverse laws and 1/a bound
    `-- M0330-B-CONVERSE exact resolvent-to-semigroup implication
        |-- M0330-C-YOSIDA construct bounded approximants
        |-- M0330-C-APPROX-SEMIGROUP exponentiate approximants
        |-- M0330-L-CONTRACTION uniform contraction estimates
        |-- M0330-L-STRONG-LIMIT construct the limiting C0 semigroup
        `-- M0330-T-GENERATOR identify its generator with A
```

The statement, boundary, foundation, external-integration, source,
documentation, provenance, trust, and workflow nodes live in separate typed
graphs and cannot be counted as proof premises.

## Node ledger

### m0330-root
Exact elaborated target. `[H3, M4, R4]`; no root inhabitant exists.

### m0330-s-definitions
Checked definitions in `Statement.lean`. `[H3, M0-L, R4]`.

### m0330-s-boundary
Zero time, strict positive axis, zero space, real scalars, and nonnegative time.
`[H3, M4, R4]`; dedicated boundary lemmas remain open.

### m0330-s-foundation
Transitive axiom, classical-choice, TCB, and no-oracle report. `[H3, M4, R4]`.

### m0330-b-forward
Exact forward implication packaged by `ForwardPackage`. `[H3, M4, R4]`.

### m0330-l-fwd-dense
Density of the strong-derivative generator domain. `[H3, M4, R4]`.

### m0330-l-fwd-closed
Closedness of the strong-derivative generator graph. `[H3, M4, R4]`.

### m0330-c-laplace-resolvent
Bochner/Laplace construction of a bounded resolvent for each `a > 0`.
`[H3, M4, R4]`.

### m0330-l-resolvent-laws
Both inverse identities and the pointwise `1/a` norm estimate. `[H3, M4, R4]`.

### m0330-b-converse
Exact converse implication packaged by `ConversePackage`. `[H3, M4, R4]`.

### m0330-c-yosida
Bounded Yosida approximants and their identities. `[H3, M4, R4]`.

### m0330-c-approx-semigroup
Exponential semigroups of the bounded approximants. `[H3, M4, R4]`.

### m0330-l-contraction
Uniform contraction estimates and approximate semigroup laws. `[H3, M4, R4]`.

### m0330-l-strong-limit
Locally uniform strong convergence and preservation of the C0 semigroup laws.
`[H3, M4, R4]`.

### m0330-t-generator
Identification of the limiting strong-derivative graph with exactly `A`.
`[H3, M4, R4]`.

### m0330-t-assemble
Kernel-checked composition from both exact implications to the root.
`[H3, M0-L, R4]`; its open premises prevent proof credit.

### m0330-x-external
Pinned build, adapter, axiom, and terminal-body audit for any reused external
forward declarations. `[H3, M4, R4]`.

### m0330-x-source
Pending node-level primary-source theorem/page/assumption/errata map.
`[H3, M4, R4]`.

### m0330-x-provenance
Pending body, import, wrapper, axiom, TCB, and replay inventory. `[H3, M4, R4]`.

## Freeze boundary

The minimal open root cut is `M0330-B-FORWARD` plus
`M0330-B-CONVERSE`. The checked conditional composition proves neither input.
This phase supplies no root closure, audit completion, source acceptance, or
theorem completion. Any correction, split, merge, exclusion, or eligibility
change requires registry version 2 and an append-only delta.
