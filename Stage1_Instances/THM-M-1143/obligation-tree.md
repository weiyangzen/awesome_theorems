# THM-M-1143 frozen obligation architecture

Item: `S56-M-1143-OBLIGATION_TREE`.

The registry freezes 12 semantic obligations before proof execution. It uses the classical
gradient-estimate route in arbitrary positive finite dimension. The pinned complex-plane theorem
is retained only as an informational provenance overlay and cannot close the general target.

## Typed proof route

```text
M1143-ROOT exact canonical proposition
`-- M1143-T-ASSEMBLE checked conditional composition
    |-- M1143-T-VANISH derivative vanishes everywhere
    |   |-- M1143-N-BOUND bounded range to uniform norm bound
    |   |-- M1143-L-GRADIENT n-dimensional interior gradient estimate
    |   `-- M1143-L-LIMIT send the ball radius to infinity
    `-- M1143-L-CONSTANT zero derivative implies constancy
```

The statement, foundation, source, plane-anchor, provenance, trust, documentation, and workflow
relations live in separate typed graphs. They are not proof premises.

## Semantic ledgers

### m1143-root

Exact elaborated all-positive-dimensions target. `[H4, M3, R4]`; no inhabitant is supplied.

### m1143-s-statement

Checked binders and hypotheses: positive dimension, global `HarmonicOnNhd`, bounded real range, and
pairwise equality. `[H4, M0-L, R4]`.

### m1143-s-foundation

Pending transitive axiom, TCB, computation, and no-oracle policy. `[H4, M4, R4]`.

### m1143-n-bound

Convert `Bornology.IsBounded (Set.range f)` into one uniform absolute-value bound. `[H4, M4, R4]`.

### m1143-l-gradient

For every center and radius, use global harmonicity on the enclosing ball to bound the Frechet
derivative by a dimension-dependent constant times the global bound divided by the radius. This is
the central missing arbitrary-dimensional analytic theorem. `[H4, M4, R4]`.

### m1143-l-limit

Because the gradient estimate holds for arbitrarily large radii, its right side tends to zero;
norm nonnegativity then forces the derivative to be zero. `[H4, M4, R4]`.

### m1143-t-vanish

Assemble bound extraction, the gradient estimate, and the radius limit into
`VanishingDerivativePackage`. `[H4, M4, R4]`.

### m1143-l-constant

Use connectedness/convexity of real Euclidean space and the zero derivative everywhere to obtain
pairwise equality. `[H4, M4, R4]`.

### m1143-t-assemble

Kernel-checked application of `VanishingDerivativePackage` and `ZeroDerivativeConstantPackage` to
the exact root. `[H4, M0-L, R4]`; its explicit parameters give no proof credit to either package.

### m1143-x-plane

Pinned mathlib theorem for `Complex -> Real`, audited at revision `8a178386...`. It is a strict
two-real-dimensional special case and an informational anchor only. `[H4, M0-L, R4]`.

### m1143-x-source

Pending primary-source theorem/page/assumption/errata crosswalk for every analytic node.
`[H4, M4, R4]`.

### m1143-x-provenance

Pending terminal-body, import, axiom, TCB, and replay inventory. `[H4, M4, R4]`.

## Freeze boundary

The minimal open root cut is `M1143-T-VANISH` plus `M1143-L-CONSTANT`. The former expands the
high-risk imported mathematics rather than hiding it behind “standard gradient estimate.” Every
leaf has a substantive ledger and a budget of at most 100 steps. This phase supplies no root
closure, audit completion, or theorem completion. Registry changes require a new version and an
append-only delta.
