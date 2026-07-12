# THM-M-1515 frozen obligation architecture

Item: `S56-M-1515-OBLIGATION_TREE`.

The registry freezes 12 semantic obligations before proof execution. The route is the direct
finite-dimensional variational-calculus proof. No terminal Noether theorem was found, so the two
analytic chain-rule packages remain explicit rather than being hidden behind an anchor.

## Typed proof route

```text
M1515-ROOT exact canonical proposition
`-- M1515-T-SUBTRACT checked conditional composition
    |-- M1515-N-CHARGE charge is momentum pairing minus boundary
    |-- M1515-L-MOMENTUM-DERIV derivative of momentum-generator pairing
    |   |-- M1515-C-MOMENTUM time-dependent momentum construction
    |   `-- M1515-X-CALCULUS imported calculus boundaries
    |-- M1515-L-BOUNDARY-DERIV derivative of boundary along q
    |   `-- M1515-X-CALCULUS imported calculus boundaries
    `-- M1515-L-SYMMETRY equality of derivative values
```

The statement/foundation, source, provenance, trust, documentation, and workflow relations are
separate typed graphs and cannot supply proof premises.

## Node ledger

### m1515-root
Exact elaborated target. `[H1, M3, R3]`; open.

### m1515-s-definitions
Frozen definitions and binder context from `Statement.lean`. `[H1, M0-L, R3]`.

### m1515-s-foundation
Pending transitive axiom, choice, fallback-value, import, and TCB audit. `[H1, M4, R3]`.

### m1515-n-charge
Checked definitional normalization of charge into a difference. `[H1, M0-L, R3]`.

### m1515-c-momentum
Construct and control differentiability of the momentum covector applied to the generator. `[H1, M4, R3]`.

### m1515-l-momentum-deriv
Product/chain rules and Euler-Lagrange yield the derivative of the pairing. `[H1, M4, R3]`.

### m1515-l-boundary-deriv
The chain rule yields the derivative of the boundary along the trajectory. `[H1, M4, R3]`.

### m1515-l-symmetry
Instantiate the frozen quasi-invariance equation at `(q t, velocity q t)`. `[H1, M0-L, R3]`.

### m1515-t-subtract
Kernel-checked conditional subtraction from both derivative packages to the exact root. `[H1, M0-L, R3]`.

### m1515-x-calculus
Audit imported chain, continuous-linear-map application, subtraction, and canonical derivative rules. `[H1, M4, R3]`.

### m1515-x-source
Pending accepted node-level source theorem/page/assumption/errata mapping. `[H1, M4, R3]`.

### m1515-x-provenance
Pending terminal body, import, axiom, TCB, and replay inventory. `[H1, M4, R3]`.

## Freeze boundary

The minimal open root cut is `M1515-L-MOMENTUM-DERIV` plus
`M1515-L-BOUNDARY-DERIV`. The checked conditional composition proves neither premise. There is no
root, audit, or theorem-completion claim. Registry changes require a new version and append-only
delta.
