# Scope map

## Preserved catalog scope

The repository fixes only target `THM-M-1374`, the title `Noether定理`, the gloss
`对称性与守恒量` (symmetries and conserved quantities), the attribution Emmy Noether, the year
1918, and the ordinary-differential-equations catalog category. Intake preserves that provenance
without interpreting the gloss as a quantified implication or correspondence.

## Proposition-changing decisions

An approved source correction must freeze all of the following before statement elaboration:

- whether the root is Noether's first theorem, second theorem, a converse, a conjunction of
  source-defined clauses, or a later theorem with its own source;
- the variational setting: one independent variable or several, finite-dimensional configuration
  space or fields, jet order, domains, scalar field, universes, regularity, and boundary behavior;
- the action or variational integral, admissible fields or trajectories, variations, Euler-Lagrange
  expressions, solution predicate, and every integration-by-parts hypothesis;
- the symmetry object: a finite-dimensional Lie group, local action, infinitesimal generator,
  generalized transformation involving derivatives, infinite group depending on arbitrary
  functions, or another source-defined notion;
- exact invariance versus invariance up to a divergence or total derivative, transformation of
  independent variables and measure/Jacobian terms, and whether only infinitesimal invariance is
  assumed;
- the rank, effectiveness, linear-independence, locality, connectedness, and global integrability
  conditions needed to move between infinitesimal and finite transformations;
- the output: divergence identities, first integrals, conserved currents or charges, differential
  identities among Euler-Lagrange expressions, independence qualifications, and on-shell versus
  off-shell scope;
- whether a converse is asserted and the source-specific exceptions or integrability conditions;
  and
- ordered binders, all degenerate cases, foundation/TCB/computation profiles, and one exact
  truth-valued conclusion with a complete source and proof boundary.

These choices yield inequivalent propositions. They are not notation cleanup that a Lean encoder
may decide silently.

## Candidate theorem families not selected

1. **Historical first theorem.** Invariance of a variational integral under a finite continuous
   group with `rho` essential parameters gives `rho` linearly independent combinations of the
   Lagrange expressions that are divergences; a source-qualified converse reconstructs invariance
   and group data. On solutions, the divergence relations yield first integrals in one dimension or
   conservation laws in several dimensions.
2. **Historical second theorem.** Invariance under an infinite continuous group depending on
   `rho` arbitrary functions and derivatives through order `sigma` yields `rho` differential
   identities among Lagrange expressions and their derivatives, with source-specific converse
   qualifications.
3. **Point-mechanics first theorem.** A differentiable one-parameter (or finite-dimensional)
   variational symmetry of a Lagrangian produces a conserved quantity along Euler-Lagrange
   trajectories, with competing conventions for time transformations and boundary terms.
4. **Field-theory current theorem.** A continuous global variational symmetry gives an on-shell
   divergence-free current, subject to locality, compact-support, boundary, gauge, and improvement
   conventions.
5. **Hamiltonian or geometric variants.** Moment maps, symplectic actions, Hamiltonian flows, and
   momentum conservation form related theorem families but are not automatically identical to the
   1918 variational statement.
6. **Converse and inverse problems.** Recovering a symmetry from a conservation law requires
   additional regularity, nondegeneracy, equivalence, and trivial-current conventions and cannot be
   inferred from the word `correspondence`.

These are scope discriminators only. None is credited as the canonical claim.

## Degenerate and boundary cases

Source selection must explicitly resolve a zero-parameter or ineffective group; dependent
infinitesimal generators; a trivial action or zero Lagrangian; constant trajectories; a current
that vanishes identically; singular or higher-order Lagrangians; transformations defined only
locally; noncompact domains; boundaries and nonvanishing endpoint terms; quasi-symmetries whose
action changes by a divergence; transformations of time or other independent variables; gauge
symmetries depending on arbitrary functions; currents differing by identically conserved
improvement terms; weak versus classical solutions; failure of required differentiability;
topological or global obstructions; and converse clauses with source-noted exceptions.

No case is excluded at intake because there is no canonical proposition yet.

## Neighbor and substitution exclusions

- `THM-M-1515` is a separate mathematical-physics target sourced from a different catalog record
  with the wording `对称性与守恒量的对应`. Its legacy `S1-M-184` statement, examples, search notes,
  or validation cannot be imported as `THM-M-1374` evidence.
- `THM-M-1373` (Hamiltonian systems), `THM-M-1378` (Euler-Lagrange equations), and
  `THM-M-1382` (least-action principle) are neighboring topics, not interchangeable roots.
- A proof that time-translation invariance conserves energy, spatial translation conserves
  momentum, or rotational invariance conserves angular momentum is only a special case unless the
  selected source makes it the exact target.
- A structure field or hypothesis named `currentDerivativeFormula`, `conserved`, `invariant`, or
  `eulerLagrange` cannot assume the main symmetry-to-conservation bridge and then receive proof
  credit for projecting it.
- A zero-Lagrangian or identity-symmetry example does not prove the general theorem.
- Generic derivative, Frechet derivative, flow, invariant-set, ODE, integral, or manifold APIs are
  substrate rather than a Noether theorem.
- Numerical trajectory checks, symbolic differentiation without a checked certificate, and the
  catalog's `已验证` label provide no theorem credit.

## Formal boundary

Pinned mathlib exposes derivatives, Frechet derivatives, continuous linear maps, flows, invariant
sets, ODE interfaces, integration, and manifold infrastructure. The probe authenticates only a
small adjacent subset. A bounded exact-topic search located no terminal variational Noether theorem
in pinned mathlib; repo-local exact-topic hits lead to the separate legacy `THM-M-1515` artifact and
unrelated algebraic uses of the name Noether. This is intake discovery, not the later exhaustive
anchor audit and not evidence of absence from external Lean projects.

The canonical Lean module, expression, expression hash, environment fingerprint, checked
transports, mutations, discovery-protocol hash, obligation registry, and proof bodies remain null or
open.
