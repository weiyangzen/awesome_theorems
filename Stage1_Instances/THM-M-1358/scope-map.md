# Scope map

## Preserved catalog scope

The repository fixes only target `THM-M-1358`, the label `分岔理论` (bifurcation theory), the gloss
`参数变化导致的定性变化` (qualitative changes caused by varying a parameter), a collective
twentieth-century attribution, and an untrusted `已验证` status. Intake preserves this dynamical-
systems subject boundary. It does not turn the field name into a proposition or select a textbook
result without source authority.

## Proposition-changing decisions

An approved source correction must freeze all of the following before statement elaboration:

- a static parameterized equation, discrete map, autonomous or nonautonomous ODE, local or global
  flow, semiflow, or another system model;
- the parameter space and dimension, distinguished parameter value, phase space, scalar field,
  domains, universes, topology or smooth structure, regularity class, and time convention;
- the invariant object whose behavior changes: equilibria, periodic orbits, invariant sets,
  connecting orbits, attractors, or another source-defined object;
- the meaning of qualitative equivalence or change, such as topological conjugacy, orbit
  equivalence, phase portrait, stability type, number of invariant objects, or spectral data;
- local versus global scope in state and parameter space, and whether existence, uniqueness,
  persistence, disappearance, stability exchange, or classification is assumed or concluded;
- the bifurcation-value predicate, genericity, codimension, transversality, eigenvalue crossing,
  normal-form coefficient, symmetry, and nondegeneracy hypotheses; and
- one exact truth-valued conclusion with ordered binders, all exceptional cases, and a complete
  proof and source boundary.

These choices define inequivalent propositions. They are a resolution ledger, not a canonical
claim.

The literal gloss also lacks a quantifier. Read universally, it is false because a constant
parameter family need not change qualitatively. Read existentially, it requires a selected system
and behavior. Read definitionally, it names a phenomenon rather than proving a theorem. Intake
therefore cannot repair the wording by silently choosing universal, existential, definitional,
persistence, necessary-condition, or classification form.

## Candidate families not credited

- Persistence of a nondegenerate equilibrium under parameter variation by an implicit-function
  theorem, or failure of persistence at a singular point.
- A local codimension-one saddle-node, transcritical, pitchfork, or Hopf bifurcation theorem with
  its source-specific normal form and nondegeneracy conditions.
- A period-doubling, homoclinic, heteroclinic, global, or higher-codimension bifurcation result.
- A classification or genericity theorem for bifurcations of equilibria, periodic orbits, maps, or
  flows.
- A definition or characterization of a bifurcation value under a selected equivalence relation.

No family in this list is selected, conjoined, asserted, or credited at intake.

## Neighbor boundaries and exclusions

- `THM-M-1359` owns saddle-node bifurcation, `THM-M-1360` Hopf bifurcation,
  `THM-M-1361` transcritical bifurcation, and `THM-M-1362` pitchfork bifurcation. None may replace
  this generic field label, and their future evidence is not shared.
- `THM-M-1363` chaos theory and `THM-M-1366` structural stability are related dynamical topics,
  not a canonical bifurcation proposition for this target.
- An implicit-function persistence theorem is not automatically a bifurcation existence or
  classification theorem; conversely, a singular derivative alone does not establish a
  bifurcation.
- A single polynomial normal form, finite-dimensional linear example, numerical continuation,
  plotted branch diagram, simulation, or observed stability change cannot substitute for a
  source-selected theorem.
- A predicate named `IsBifurcationValue`, a structure field, or a hypothesis that directly assumes
  the desired qualitative change supplies an interface, not a proof.
- Generic ODE, flow, fixed-point, derivative, continuity, or implicit-function APIs alone receive
  no statement or proof credit.
- The catalog label `已验证` supplies neither a human proof nor a kernel-checked artifact.

## Boundary cases

The later statement phase must decide constant parameter families; empty, singleton, or zero-
dimensional state and parameter spaces; equilibria existing on the boundary; nonisolated invariant
objects; nonunique or finite-time solutions; one-sided parameter neighborhoods; zero eigenvalues
and eigenvalues on the imaginary axis or unit circle; multiplicity and resonance; vanishing
nondegeneracy coefficients; symmetry-forced branches; coordinate and parameter changes; and whether
the asserted qualitative difference occurs on both sides of the distinguished parameter.

## Formal boundary

No canonical Lean expression is frozen. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe checks generic implicit-function,
integral-curve, flow, fixed-point, derivative, and smoothness interfaces. A bounded local exact-topic
search found no `bifurcat` declaration in pinned mathlib or repo-local Lean sources. This is an
intake discovery observation, not an exhaustive anchor audit or a global absence claim.
