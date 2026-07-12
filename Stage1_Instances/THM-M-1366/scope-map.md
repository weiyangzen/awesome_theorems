# Scope map

## Received scope

The repository fixes only the title `结构稳定性`, the attribution `Andronov/Pontryagin`, the year
1937, and the gloss `系统在扰动下的稳定性` ("stability of systems under perturbations"). It gives
no bibliography, definition, binder, hypothesis, conclusion, boundary case, or formal artifact.
The same six-line record occurs twice in the mathematical source corpus. Stage0 repeats it and
explicitly leaves the formal system, exact premises, proof route, equivalent forms, axioms,
machine status, and artifact links open. The `已验证` label is untrusted metadata.

The title and gloss identify a subject, not one proposition. In ordinary usage, structural
stability is relative to a chosen space of systems, topology on that space, and equivalence
relation. None is fixed here.

## Candidate mathematical families

An eventual source-approved target could be one of the following, but none is credited by this
intake:

- a definition of structural stability for a specified map, diffeomorphism, vector field, or flow;
- an Andronov-Pontryagin theorem about rough planar autonomous systems;
- a necessary-and-sufficient characterization or an openness/density theorem;
- Peixoto's theorem for vector fields on compact surfaces;
- structural stability for Morse-Smale, Anosov, Axiom A, or hyperbolic invariant systems;
- local persistence or conjugacy near a hyperbolic equilibrium or periodic orbit.

These statements differ in domain, hypotheses, quantifier order, and conclusion. A familiar name
or historical association cannot choose among them.

## Proposition-changing decisions

Before the statement phase can freeze a canonical claim, an accepted source and reviewer must fix:

1. Whether the system is a vector field, ODE solution family, flow, map, or diffeomorphism.
2. The phase space, dimension, compactness, connectedness, boundary, scalar field, and smoothness.
3. Continuous or discrete time and, for flows, global completeness or maximal local trajectories.
4. The regularity class and topology used to say that a perturbation is small.
5. Whether the theorem is global or restricted to a neighborhood, invariant set, orbit, or
   nonwandering set.
6. Whether equivalence means topological conjugacy, semiconjugacy, orbit equivalence, or another
   relation, and whether time reparametrization is allowed.
7. Whether the conjugating map must be close or isotopic to the identity or preserve orientation.
8. The exact order of the neighborhood, perturbation, and conjugacy quantifiers.
9. Whether the target is a definition, implication, equivalence, classification, openness/density
   theorem, or existence/nonexistence result.
10. Every exceptional and boundary case and every source correction or erratum.

## Boundary and degenerate cases

No case is excluded before a proposition is selected. The source review must explicitly decide
empty and zero-dimensional spaces; noncompact or boundary-bearing manifolds; stationary systems;
equilibria and periodic orbits; separatrices and nonhyperbolic points; zero perturbation;
strict/non-strict perturbation radii; systems at a bifurcation boundary; local trajectories leaving
the chosen domain; and weak versus strong perturbation topologies.

## Explicit exclusions

The intake must not replace this item with Peixoto's theorem (`THM-M-1367`), Morse-Smale systems
(`THM-M-1368`), Hartman-Grobman (`THM-M-1345`), stable manifolds (`THM-M-1346`), the Smale
horseshoe (`THM-M-1365`), hyperbolic dynamical systems (`THM-M-1411`), or Anosov diffeomorphisms
(`THM-M-1412`). Those are separate roots even when a reviewed theorem later relates them.

Also excluded are a scalar, linear, discrete, finite, or globally defined example substituted for
a general result; a structure whose fields assume the requested conjugacy; generic flow,
homeomorphism, ODE, or topology APIs without an exact theorem bridge; numerical perturbation tests;
and the untrusted catalog label used as source or kernel evidence.

## Lean boundary

Pinned mathlib provides generic continuous `Flow` objects, orbits, invariant sets, homeomorphisms,
semiconjugacy, and factor relations. It does not follow that these interfaces encode the intended
system space, perturbation topology, equivalence, or theorem. `IntakeProbe.lean` authenticates only
that adjacent surface. It declares no structural-stability predicate or theorem and supplies no
proof-body credit.

## Retry condition

Select a lawful immutable primary or authoritative source and pinpoint proposition; record its
edition, theorem/section/page, incorporated definitions, complete binders, hypotheses, conclusion,
proof boundary, corrections, and boundary conventions; reconcile the neighboring Peixoto and
Morse-Smale ownership boundaries; and obtain independent source review. A later statement phase
may then encode exactly that proposition, minimize pinned imports, serialize its elaborated
expression and environment, check every credited transport, and run the required statement
mutations.
