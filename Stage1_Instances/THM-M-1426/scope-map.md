# Scope map

## Preserved source scope

The repository fixes only the label `多值随机动力系统` ("multivalued random dynamical systems"),
the attribution "many mathematicians," the period "21st century," and the gloss
`非唯一解的随机系统` ("random systems with nonunique solutions"). It supplies no bibliography,
definition, premise, conclusion, or formal artifact. Intake therefore preserves a mathematical
framework and motivation boundary only.

## Proposition-changing decisions

An approved source correction must select one immutable primary-source proposition and freeze:

- the phase space and universes, topology, metric and completeness or separability conditions, and
  whether values are arbitrary, nonempty, closed, bounded, or compact subsets;
- the sample space, sigma algebra, probability measure, completed-measure convention, and the
  measurable measure-preserving driving flow or transformation;
- continuous versus discrete time, nonnegative evolution time versus a two-sided base flow, and all
  identity, associativity, commutativity, and measurability assumptions on time;
- the set-valued evolution map and its action on points and sets, including graph, hit, distance,
  Effros, or another multifunction-measurability convention;
- equality versus inclusion in the cocycle/concatenation law, and perfect, crude, or very crude
  almost-sure scope with exact dependence of exceptional sets;
- the source of nonuniqueness: a differential inclusion, weak or mild PDE solution, generalized
  semiflow, non-Lipschitz SDE, control family, or another solution relation;
- global existence, compactness, semicontinuity, closed-graph, absorption, invariance, attraction,
  measurability, selection, uniqueness, or another exact hypothesis;
- one truth-valued conclusion, rather than the definition or availability of the framework; and
- every ordered binder, null-set scope, dependent definition, degenerate case, and boundary rule.

These choices yield inequivalent propositions. They are a resolution checklist, not a canonical
claim.

## Candidate families not credited

- Definition or characterization of a measurable set-valued cocycle over a metric dynamical system.
- Construction of an MRDS from a stochastic differential or parabolic inclusion with nonunique
  solutions.
- Existence, uniqueness, minimality, invariance, or measurability of a global random attractor under
  absorbing-compactness and semicontinuity assumptions.
- Perfection of a crude or very crude cocycle by choosing compatible exceptional sets.
- Compactness, upper/lower semicontinuity, closed-graph, or asymptotic-compactness of a multivalued
  stochastic flow.
- A model-specific attractor result for a reaction-diffusion inclusion or another stochastic PDE.

No family in this list is selected, asserted, or credited at intake.

## Explicit exclusions

The target must not be silently replaced by the separately cataloged random dynamical systems
(`THM-M-1424`) or random attractors (`THM-M-1425`). A deterministic multivalued semiflow omits the
random base, while assuming uniqueness collapses the multivalued boundary; neither is a substitute.

Generic relation composition and image laws, measurable-space or measure-preserving APIs, a finite
toy relation, a numerical stochastic simulation, or a record that assumes the desired cocycle or
attractor property cannot identify or close this target. Nor can a paper title, a bare definition,
or the catalog's untrusted `已验证` status.

## Formal boundary

No canonical Lean expression is frozen. Pinned mathlib supplies `SetRel` as a relation/set-valued
map representation, relation composition and image, measurable spaces, measures, and
measure-preserving iteration. A bounded exact-topic search found no named multivalued or set-valued
random dynamical-system declaration. `IntakeProbe.lean` checks only this adjacent substrate. These
facts are not an exhaustive anchor audit, an MRDS definition, a canonical statement, or machine-
proof evidence.
