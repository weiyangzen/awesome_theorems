# Scope map

## Preserved catalog scope

The intake preserves target `THM-M-1363`, the title `混沌理论` (chaos theory), the gloss
`确定性系统的混沌行为` (chaotic behavior of deterministic systems), a collective attribution to
many mathematicians, and the twentieth-century date. Importance `high`, ODE category, and status
`已验证` are inventory metadata, not mathematical premises, source fidelity, or Lean evidence.

The subject boundary is deterministic dynamical systems and chaotic behavior. It does not select
one theorem. In particular, the literal wording has no quantifier. An `all systems` reading fails
on identity and constant dynamics. A `some system` reading requires a selected system and chaos
notion. A definitional reading creates an interface rather than a theorem.

## Proposition-changing decisions

An approved exact-source statement must freeze all of the following:

- a discrete self-map, monoid action, semiflow, flow, ODE solution operator, or another dynamics
  model, including the phase space, time object, invariant subset, domains, and universes;
- topological, uniform, metric, measurable, smooth, compactness, completeness, separability, and
  cardinality structures and the regularity of the dynamics;
- the precise chaos notion: Devaney, sensitive dependence, Li-Yorke, distributional, positive
  topological or measure entropy, mixing, symbolic factor, horseshoe, or another source definition;
- whether transitivity, mixing, dense positive-period points, recurrence, expansivity, entropy,
  scrambled pairs, or sensitivity are assumed, defined, derived, or conjoined;
- whether the result is a definition, equivalence, implication between chaos notions, existence or
  genericity theorem, classification, or proof that one named system is chaotic;
- local versus global scope, restriction to an invariant set or attractor, basin conventions, and
  whether the claim concerns points, orbits, measures, subsets, or the entire phase space; and
- every ordered binder, hypothesis, conclusion, incorporated definition, proof boundary, source
  correction, erratum, and exceptional case.

These choices yield inequivalent propositions. They are a resolution ledger, not a canonical claim.

## Candidate families not credited

1. Devaney chaos for a continuous self-map on an infinite metric or topological space: topological
   transitivity plus dense periodic points, with sensitivity derived or separately included.
2. Sensitive dependence on initial conditions under a fixed metric and positive separation scale.
3. Positive topological or measure-theoretic entropy as a chaos criterion or consequence.
4. Li-Yorke chaos via an uncountable scrambled set and liminf/limsup separation conditions.
5. Topological mixing, weak mixing, expansivity, specification, symbolic dynamics, or existence of
   a shift/horseshoe factor.
6. A model theorem proving that the logistic map, tent map, Lorenz system, Smale horseshoe, or
   another named system has a selected chaos property.

No family in this list is selected, conjoined, asserted, or credited at intake.

## Boundary cases to resolve

- empty, singleton, finite, disconnected, discrete, or indiscrete spaces and spaces with isolated
  points;
- identity, constant, periodic, noninjective, discontinuous, partial, or finite-time dynamics;
- empty or total invariant subsets and whether dynamics must map the chosen subset into itself;
- period zero versus positive period, minimal-period conventions, and density in a subset versus the
  ambient space;
- empty open sets in transitivity, one-sided versus two-sided time, and discrete versus continuous
  time;
- a zero sensitivity constant, metric dependence, uniform versus pointwise sensitivity, compact
  versus noncompact spaces, and topologically equivalent but metrically different systems;
- zero, infinite, or subset entropy and topological versus measure-theoretic entropy; and
- local chaotic invariant sets versus global phase-space or basin claims.

## Neighbor boundaries and exclusions

- `THM-M-1358` (bifurcation theory), `THM-M-1364` (Lorenz system), `THM-M-1365` (Smale
  horseshoe), and `THM-M-1366` (structural stability) remain distinct targets. Their future
  statements or evidence cannot select or close this root.
- `THM-M-1403` (topological entropy) and `THM-M-1404` (measure-theoretic entropy) are separate
  invariant topics; an entropy definition or theorem cannot silently replace chaos theory.
- A logistic/tent-map calculation, shift map, horseshoe, Lorenz trajectory, or one convenient
  finite-dimensional example cannot replace an unspecified field-level target.
- A predicate or structure called `IsChaotic`, or a premise containing the desired chaos property,
  is an interface or assumption rather than proof of chaotic behavior.
- A simulation, orbit plot, floating-point Lyapunov exponent, sampled sensitivity observation, or
  numerical entropy estimate receives no theorem credit without a source-identical verified
  certificate and proof boundary.
- The catalog label `已验证` and generic flow, periodic-point, transitivity, or entropy APIs supply
  neither a human proof nor a kernel proof of this target.

## Formal boundary

No canonical Lean expression is frozen. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe checks `Flow`, `IsInvariant`,
`Function.IsPeriodicPt`, `Function.periodicPts`, `MulAction.IsTopologicallyTransitive`,
`AddAction.IsTopologicallyTransitive`, and `Dynamics.coverEntropy`. These declarations formalize
separate pieces under specific encodings; they do not define chaos or establish the catalog gloss.
A bounded exact-topic search is intake discovery only, not an exhaustive anchor audit or an absence
claim about external Lean projects.
