# Scope map

## Preserved catalog scope

The repository fixes only target `THM-M-1380`, the label `Jacobi定理` (Jacobi theorem), Carl
Jacobi, 1837, the gloss `Hamilton-Jacobi方程的完全解` (a complete solution of the Hamilton-Jacobi
equation), and an untrusted `已验证` status. Intake preserves this Hamilton-Jacobi-family boundary.
It does not choose a familiar formulation from memory or turn a description into a proposition.

## Proposition-changing decisions

An approved source correction must freeze all of the following before statement elaboration:

- whether the phase space is a cotangent bundle, an open subset of Euclidean phase space, a
  symplectic manifold, or another model, and the scalar field, finite dimension, coordinates,
  domains, universes, and topology;
- the Hamiltonian's time dependence, differentiability class, domain, and any completeness,
  regularity, convexity, or nondegeneracy assumptions;
- the exact Hamilton-Jacobi equation and sign convention, including whether the target is the
  time-dependent principal function or the autonomous characteristic function;
- what "complete" means: a parameterized complete integral, a maximal independent family, a
  complete characteristic, a complete integral of a first-order PDE, or merely one solution;
- the parameter space and count, independence or mixed-Hessian determinant condition, locality,
  exceptional set, and whether invertibility is pointwise or uniform;
- whether existence of a complete integral is assumed or concluded, and whether the result proves
  a canonical transformation, Hamiltonian trajectories, integration by quadratures, a general
  solution, or an equivalence among these; and
- exact ordered binders, every hypothesis and conclusion, initial or boundary data, equivalence
  notion, and all singular and degenerate cases.

These choices define inequivalent propositions. They are a resolution ledger, not a canonical
claim. In particular, not every Hamiltonian admits a global smooth complete integral, so the gloss
cannot silently become an unconditional existence theorem.

## Candidate families not credited

- A chain-rule theorem saying that a sufficiently smooth solution `S(q,t)` of the Hamilton-Jacobi
  PDE, together with the associated first Hamilton equation, yields the second Hamilton equation.
- A complete integral `S(q, alpha, t)` whose mixed derivative in `(q, alpha)` is nonsingular and
  which defines conjugate constants by differentiating with respect to `alpha`.
- A canonical-transformation theorem reducing a Hamiltonian to zero or to constants and recovering
  trajectories from a complete integral.
- For an autonomous Hamiltonian, the separated ansatz `S(q,t) = W(q) - E*t` and its characteristic
  Hamilton-Jacobi equation.
- A method-of-characteristics theorem for a first-order PDE or a variational action-value theorem.

No family in this list is selected, conjoined, asserted, or credited at intake.

## Neighbor boundaries and exclusions

- `THM-M-1379` is the separately cataloged Hamilton-Jacobi equation. Stating that PDE does not
  supply this target's missing theorem about a "complete solution."
- `THM-M-1378` Euler-Lagrange equations, `THM-M-1381` Maupertuis principle, and `THM-M-1382`
  least action are related mechanics targets, not substitutes for this theorem.
- `THM-M-1547` concerns completely integrable Hamiltonian systems. Liouville integrability and
  action-angle coordinates cannot be silently substituted for an unidentified Jacobi theorem.
- A predicate or structure field that assumes a complete integral, canonical transformation, or
  desired trajectories supplies an interface, not a proof.
- One explicitly solvable Hamiltonian, separated ansatz, numerical characteristic, or symbolic PDE
  solution cannot substitute for a general source-selected theorem.
- Generic calculus and ODE APIs receive no statement or proof credit, and the catalog label
  `已验证` supplies neither a human proof nor kernel evidence.

## Boundary cases

The statement phase must decide zero degrees of freedom; empty or singleton configuration and
parameter domains; parameter dimension different from configuration dimension; time-independent
versus time-dependent Hamiltonians; constant or singular Hamiltonians; vanishing mixed Hessian;
local versus global solutions; caustics and multivalued actions; loss of differentiability;
nonunique characteristics; boundary points; coordinate-chart overlap; incomplete Hamiltonian
flows; topology obstructing global generating functions; additive constants; parameter
reparameterization; and sign conventions for momenta and time.

## Formal boundary

No canonical Lean expression is frozen. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe checks generic differentiability,
Frechet derivatives on products, continuous linear maps, and integral curves. A bounded local
search found no exact-topic Hamilton-Jacobi or complete-integral declaration in pinned mathlib or
repo-local Lean. This is an intake discovery observation, not an exhaustive anchor audit or a
formal absence claim.
