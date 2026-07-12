# Scope map

## Preserved catalog scope

The repository fixes only target `THM-M-1361`, the label `跨临界分岔` (transcritical bifurcation),
the gloss `平衡点交换稳定性的分岔` (a bifurcation in which equilibria exchange stability), a
collective twentieth-century attribution, and an untrusted `已验证` status. Intake preserves that
dynamical-systems subject boundary. It does not turn the gloss into a quantified theorem or choose
a normal form without source authority.

## Proposition-changing decisions

An approved source correction must freeze all of the following before statement elaboration:

- whether the target is a definition, one explicit example, a local existence theorem, a smooth
  normal-form classification, a genericity theorem, or a conjunction;
- a scalar autonomous ODE, higher-dimensional vector field, discrete map, flow, semiflow, or other
  system model, including its state and parameter spaces, domains, universes, and scalar field;
- the distinguished parameter and equilibrium, the two equilibrium branches, their existence and
  uniqueness neighborhoods, their intersection or collision, and branch labels;
- regularity, solution existence and uniqueness, and the exact Lyapunov, asymptotic, exponential,
  spectral, or discrete-time stability predicate and time direction;
- local versus global scope in state and parameter space, and whether branch crossing, stability
  exchange, normal-form equivalence, or all three is assumed or concluded;
- the source-specific derivative, transversality, genericity, codimension, center-manifold, and
  nondegeneracy hypotheses, including every nonzero coefficient convention;
- allowed coordinate, time, state, and parameter changes and whether reversing a parameter or
  relabeling branches preserves the claimed form; and
- one exact truth-valued conclusion with ordered binders, exceptional cases, proof boundary, and
  source locator.

These choices define inequivalent propositions. They are a resolution ledger, not a canonical
claim. The catalog phrase also has no quantifier: it can be read as a definition, a description of
an example, or a general theorem schema. Intake cannot repair that omission silently.

## Candidate families not credited

- The scalar real normal form `x' = mu*x - x^2`, with equilibria `x = 0` and `x = mu` and an exact
  source-selected stability calculation.
- A local scalar theorem for a smooth family `x' = f(x, mu)` with a persistent equilibrium branch
  and source-specific mixed-derivative, quadratic, and transversality assumptions.
- A normal-form theorem giving smooth coordinate and parameter changes near a critical equilibrium.
- A definition or characterization using two intersecting equilibrium branches and exchange of a
  selected stability type.
- A discrete-time map theorem or a higher-dimensional theorem reduced through a center manifold.

No family in this list is selected, conjoined, asserted, or credited at intake.

## Neighbor boundaries and exclusions

- `THM-M-1358` owns generic bifurcation theory. `THM-M-1359`, `THM-M-1360`, and `THM-M-1362`
  separately own saddle-node, Hopf, and pitchfork bifurcations. Their statements and evidence do not
  transfer to this target.
- A saddle-node creation or annihilation, a Hopf periodic-orbit branch, or a pitchfork
  symmetry-breaking pattern cannot replace exchange between two equilibrium branches.
- The implicit-function necessary condition `f = 0` and state derivative `D_x f = 0` is not by
  itself sufficient for a transcritical bifurcation.
- Solving one polynomial equilibrium equation does not prove a general local classification, and
  crossing solution branches alone does not establish dynamical stability exchange.
- A predicate named `IsTranscritical`, a structure field, or a hypothesis that directly assumes
  branch crossing and stability exchange supplies an interface, not a proof.
- Numerical continuation, a plotted diagram, sampled trajectories, or a phase portrait cannot
  replace a theorem under rev-5.6.
- Generic ODE, flow, fixed-point, derivative, continuity, and implicit-function APIs alone receive
  no statement or proof credit. The catalog label `已验证` receives no H or M credit.

## Boundary cases

The later statement phase must decide the critical parameter where branches coincide and
linearization is nonhyperbolic; constant, identical, tangent, nonisolated, or multiple branches;
one-sided parameter neighborhoods and parameter reversal; state-domain boundaries and
zero-dimensional spaces; insufficient regularity and nonunique or finite-time solutions;
vanishing transversality or quadratic coefficients; multiple zero eigenvalues and symmetry; local
versus global behavior; and the exact stability notion at and on both sides of the critical value.

## Formal boundary

No canonical Lean expression is frozen. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe checks generic implicit-function,
integral-curve, flow, fixed-point, derivative, and smoothness interfaces. A bounded exact-topic
search over pinned mathlib and repo-local Lean sources found no `bifurcat` or `transcritical`
occurrence. This is an intake discovery observation, not an exhaustive anchor audit or a global
absence claim.
