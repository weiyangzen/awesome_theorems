# THM-M-0168 frozen obligation architecture

Registry version 1 freezes eleven canonical obligations before proof execution. The analytic route
is deliberately explicit: turn the PDE into minimal graph geometry, obtain stability, use a
logarithmic-cutoff curvature argument to force flatness, recover constant coordinate derivatives,
and integrate them. This route is a proof plan, not a credited proof or a source-faithful H0 claim.

## root

`M0168-ROOT` is the exact statement fingerprint `b5cef8a8...54f5`. The Lean composition harness
consumes both `DerivativeRigidity` and `ConstantPartialsToAffine`; both remain open propositions.

## s-interface

`M0168-S-INTERFACE` owns the entire `Real x Real` domain, `C2` regularity, the exact ordered Frechet
partials and PDE, and the global affine conclusion. No higher-dimensional or local theorem is used.

## c-graph

`M0168-C-GRAPH` constructs the graph immersion, induced metric, unit normal, and second fundamental
form. Immersion and well-definedness are substantive obligations rather than notation.

## n-pde-minimal

`M0168-N-PDE-MINIMAL` computes mean curvature and checks that the frozen PDE implies zero mean
curvature. The geometric/PDE equivalence found open during intake is therefore not assumed.

## l-stability

`M0168-L-STABILITY` derives the stability inequality from the positive vertical component of the
graph normal, exposing the Jacobi equation and compact-support integration by parts.

## c-cutoff

`M0168-C-CUTOFF` owns logarithmic cutoffs, compact support, energy bounds, and noncompact exhaustion.

## l-curvature

`M0168-L-CURVATURE` combines stability, the curvature identity, and cutoffs to obtain pointwise
vanishing of the second fundamental form. Integral-to-pointwise passage is an explicit step.

## l-derivative-rigidity

`M0168-L-DERIVATIVE-RIGIDITY` composes the geometric packages and translates flatness of the
connected graph into constancy of both coordinate derivatives.

## t-integrate

`M0168-T-INTEGRATE` restricts the function to line segments and applies a constant-derivative
calculus result to recover the affine formula with `c = u (0,0)`.

## x-source

`M0168-X-SOURCE` keeps primary-source identity, a modern exposition, assumptions, proof-step
crosswalk, errata, and independent review open. The route cannot raise the current H1 status.

## x-trust

`M0168-X-TRUST` owns eventual declaration dependencies, axiom reports, pinned imports, automation,
and the no-unrecorded-computation boundary.

The frozen cut set contains the seven open theorem-bearing construction, transport, curvature,
rigidity, and integration packages. Master acceptance of this architecture would not establish any
of those packages and would not establish theorem completion.
