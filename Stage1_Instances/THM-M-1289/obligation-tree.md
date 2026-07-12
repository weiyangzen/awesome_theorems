# Frozen obligation architecture

Node: `S56-M-1289-OBLIGATION_TREE`. Registry version 1 freezes 20 canonical obligations before
machine closure is measured. `obligation-registry.json` is denominator authority and
`typed-graphs.json` is node and typed-edge authority. This document is only their readable map.

## Proof route

The root consumes six independent analytic results: positivity, smoothness, the normalized critical
PDE, finite critical function norm, finite gradient norm, and sharp equality. The equality package
itself requires both the least-constant Sobolev theorem and exact evaluation of the bubble norms.
Translation and positive dilation reduce the derivative and integral work to a centered radial
profile, without dropping any binder or changing the test-function class.

`ObligationTree.lean` defines the six exact component propositions and kernel-checks their
composition into `AubinTalentiTarget`. They are abstract hypotheses, not imported facts or proofs.

## Canonical nodes

### m1289-root
Exact public proposition; open at M3 because every analytic component remains unproved.

### m1289-s-defs
Exact definitions of the Euclidean domain, critical exponent, bubble, gradient seminorm, and sharp constant.

### m1289-s-domain
Binder order and assumptions `n >= 3`, arbitrary center, and `lambda > 0`.

### m1289-s-boundary
Denominator, scale, and center-point side conditions, including strict rather than weak positivity.

### m1289-s-foundation
Classical logic, real powers, measure, differentiation, imports, axioms, and TCB audit.

### m1289-n-radial
Translation/dilation normalization with constants and measure scaling preserved.

### m1289-c-bubble
Well-definedness and strict positivity of the real-power construction.

### m1289-l-pos
Pointwise positivity component.

### m1289-l-smooth
Infinite Frechet differentiability component.

### m1289-l-radial-deriv
Exact first and second derivative identities for the translated radial profile.

### m1289-l-pde
Pointwise Laplacian computation and normalized critical PDE.

### m1289-l-fun-norm
Finiteness of the critical `eLpNorm`.

### m1289-l-grad-norm
Finiteness of the L2 Frechet-gradient `eLpNorm`.

### m1289-l-sharp
Sharp homogeneous Sobolev inequality and leastness over the exact compactly supported smooth class.

### m1289-l-norm-eval
Radial integration, scaling, exact seminorm evaluation, and equality constant.

### m1289-t-extremal
One shared constant witness satisfying sharpness and explicit bubble equality.

### m1289-t-assemble
Checked conditional child-to-root composition; the only provisionally closed obligation.

### m1289-x-source
Primary-source pinpoint crosswalk, currently open at H2.

### m1289-x-provenance
Proof-body origin overlay, with no machine-proof credit.

### m1289-x-trust
Kernel, dependency, automation, executable, and computation trust overlay.

## Status boundary

This phase freezes architecture, denominators, graph roles, and a conditional composition interface.
It proves none of the six analytic components. Source review, proof bodies, provenance and trust
closure, readable reconstruction, hermetic replay, independent validation, master acceptance, and
theorem completion remain open.
