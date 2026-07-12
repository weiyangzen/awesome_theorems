# Scope map

## Preserved catalog scope

The repository fixes only target `THM-M-1342`, the title "Lyapunov stability theory," the gloss
"stability of an equilibrium," attribution to Aleksandr Lyapunov, and the year 1892. Intake
preserves that ordinary-differential-equation stability topic. It does not treat the attribution as
a primary-source citation or the untrusted `已验证` label as source or kernel evidence.

## Proposition-changing decisions

An approved source decision must first determine whether this target is a definition, a criterion,
a characterization, or an implication. It must then freeze:

- an autonomous ODE, nonautonomous ODE, flow, semiflow, discrete system, differential inclusion,
  or another dynamical model;
- the time domain, state space, topology or metric, system domain, vector-field regularity, and
  exact solution or flow notion;
- a fixed point, equilibrium trajectory, invariant set, orbit, or another stability object, with
  its equilibrium or invariance hypotheses;
- local versus global existence, uniqueness versus all-solution quantification, forward-time
  completeness, and the handling of finite escape or boundary contact;
- Lyapunov, uniform, asymptotic, exponential, orbital, practical, input-to-state, or another
  stability notion, including whether instability is part of the root;
- neighborhood, epsilon-delta, metric-ball, filter, sequence, or uniform-space encoding and every
  ordered quantifier dependency;
- whether convergence is required in addition to stability, the basin and rate if any, and whether
  the conclusion is local, semiglobal, or global; and
- all endpoint, empty-domain, zero-dimensional, nonunique-solution, and boundary cases.

These choices produce materially different propositions. They are a resolution ledger, not a
canonical statement.

## Candidate families not credited

1. Definition of Lyapunov stability for a fixed point: every neighborhood admits a smaller
   neighborhood whose forward trajectories remain in the first.
2. Definition of asymptotic stability: Lyapunov stability together with local convergence to the
   fixed point.
3. Definition of exponential stability: a source-specific local exponential estimate on the flow.
4. An epsilon-delta reformulation of Lyapunov stability for a metric state space.
5. Stability criteria supplied by Lyapunov functions, linearization, invariance principles, or
   spectral information.

No family in this list is selected, asserted, conjoined, or credited at intake. In particular, a
definition alone may not even match the catalog's classification as a mathematical theorem.

## Explicit exclusions and neighbor boundaries

- `THM-M-1343`, Lyapunov's direct method, is a Lyapunov-function criterion and is not silently
  absorbed into this general stability-theory target.
- `THM-M-1344`, Lyapunov's indirect method, transfers linearized behavior and is not a substitute.
- `THM-M-1355`, stability of linear systems, is a distinct classification target and is neither
  the general nonlinear theory root nor proof of it.
- `THM-P-0796`, the related physics-catalog stability theorem, is metadata from another target and
  supplies no source or proof credit.
- Stability, asymptotic stability, and exponential stability are not treated as synonyms.
- Attraction alone is not upgraded to asymptotic stability; the inspected source explicitly notes
  that convergence need not imply stability.
- Global forward existence, uniqueness, compactness, coercivity, differentiability, or a Lyapunov
  function is not assumed merely because a familiar textbook theorem needs it.
- A predicate field that assumes stability, a projection of such a structure, an API typecheck, or
  the catalog label `已验证` is not a proof.

## Boundary cases

The statement phase must decide a singleton or zero-dimensional state space, empty neighborhoods,
a zero vector field, constant trajectories, a non-isolated equilibrium, nonunique solutions,
finite escape, a boundary equilibrium, disconnected domains, time origins, incomplete flows, and
whether quantification is over all maximal solutions or one selected flow. It must also distinguish
mere attraction, neutral stability, asymptotic stability, and exponential estimates.

## Formal boundary

No canonical Lean expression is frozen. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, `IsIntegralCurveOn`, `IsIntegralCurveAt`,
`Function.IsFixedPt`, `Metric.ball`, `nhds`, and `Filter.Tendsto` are adjacent substrate for prospective
encodings. A bounded intake search found no obvious named ODE equilibrium-stability theory theorem
under the searched terms. The probe and search are discovery inputs only, not an exhaustive anchor
audit, exact statement, or proof.
