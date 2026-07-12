# Scope map

## Preserved theorem family

The intake preserves the Morse-Smale dynamical-systems family named by the catalog. A later
statement phase may select an exact root only from a lawfully preserved, independently reviewed
source passage. Candidate components, none yet credited as the theorem, include:

- a smooth diffeomorphism or a complete smooth vector field and its one-parameter flow;
- a compact smooth manifold, possibly with a source-specified boundary convention;
- finitely many hyperbolic fixed points and periodic orbits, or an equivalent description of the
  nonwandering set;
- stable and unstable manifolds whose intersections are transverse;
- simple forward and backward limiting behavior or a source-specific no-cycle condition; and
- structural stability, openness, gradient-flow density, a Morse decomposition, or another exact
  conclusion supplied by the selected source.

## Decisions required at statement freeze

1. Preserve one complete primary-source edition, select a numbered theorem or precisely bounded
   result, map incorporated definitions and proof boundary, review corrections and errata, and
   obtain independent source approval.
2. Decide whether the system is a discrete diffeomorphism, a vector field, or its flow; fix the time
   domain, invertibility, completeness, and whether orbit equivalence preserves time or only
   orientation.
3. Fix the manifold dimension, compactness, connectedness, boundary convention, smooth structure,
   Riemannian choices, and the regularity class of systems and perturbations.
4. Define the recurrent objects exactly: fixed points, closed/periodic orbits, critical elements,
   the nonwandering set, finiteness, minimal periods, and whether equilibria count as periodic.
5. Define hyperbolicity for each critical element, including derivative/Poincare-map conventions,
   invariant splitting, flow direction, spectrum, norms, and uniformity.
6. Define global and local stable/unstable manifolds and transversality, including every quantified
   pair and intersections that are empty or coincide along an orbit.
7. Fix the conclusion: a defining equivalence, a sufficient structural-stability theorem, a full
   characterization, openness, density among gradient systems, Morse inequalities/cell structure,
   or an explicit source-defined conjunction.
8. Define structural stability and the ambient topology if it occurs: `C1` or another topology,
   topological conjugacy for maps, orbit equivalence for flows, and parameter-orientation rules.
9. Freeze all universes, ordered binders, quantifier dependencies, hypotheses, conclusion clauses,
   boundary cases, foundation policy, and checked relationships to alternate encodings.

## Degenerate and boundary cases

Source review must explicitly dispose of an empty or zero-dimensional manifold; a system with no
critical elements; noncompact or incomplete dynamics; manifolds with boundary; nonisolated or
nonhyperbolic equilibria; zero or nonminimal periods; a nonhyperbolic Poincare return map; infinitely
many periodic orbits; recurrence outside the listed critical elements; tangential stable/unstable
intersections; heteroclinic or homoclinic cycles; nontransverse self-incidence; loss of completeness
under perturbation; and differences between conjugacy, time-preserving conjugacy, and orbit
equivalence.

## Neighbor and substitution exclusions

- `THM-M-1366` owns the broad structural-stability topic, and `THM-M-1367` owns Peixoto's
  two-dimensional characterization. Neither supplies this target's root or proof credit.
- `THM-M-1346` stable-manifold theorem supplies at most a dependency; it is not the global
  Morse-Smale or structural-stability result.
- `THM-M-1365` Smale horseshoe is hyperbolic chaotic dynamics, not a Morse-Smale system.
- `THM-M-1411` through `THM-M-1414` separately own hyperbolic dynamics, Anosov diffeomorphisms,
  Axiom A systems, and spectral decomposition. Axiom A plus no cycles, Omega-stability, or spectral
  decomposition cannot silently replace this target.
- Peixoto's surface `iff`, Kupka-Smale generic transversality, gradient-flow density, Morse
  inequalities, and a cell decomposition are materially different propositions.
- The familiar statement "Morse-Smale systems are structurally stable" is a plausible later
  Palis-Smale result, not automatically the proposition selected by a 1961 catalog record.
- A structure that stores hyperbolicity, transversality, or structural stability as a field does
  not prove that property. A finite toy map, numerical orbit plot, sampled spectrum, or simulation
  does not prove the general theorem.
- Generic ODE, flow, periodic-point, manifold, and derivative APIs are substrate only. The catalog's
  `verified` label and this intake probe supply no source-fidelity or machine-proof evidence.

## Formal boundary

Pinned mathlib exposes generic flows and invariant sets, Euclidean and manifold integral curves,
discrete periodic points, manifold derivatives, and tangent maps. It does not expose, under an
exact-topic name found by the bounded search, the selected notions of hyperbolic periodic orbit,
stable/unstable manifold transversality, Morse-Smale system, structural stability, or their target
theorem. No canonical Lean target, expression fingerprint, checked transport, mutation suite,
discovery-protocol hash, obligation registry, or proof body is frozen at intake.
