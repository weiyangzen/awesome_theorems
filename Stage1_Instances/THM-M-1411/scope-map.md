# Scope map

## Preserved source scope

The repository fixes only the Chinese label `双曲动力系统`, the gloss `双曲性的理论` ("the theory
of hyperbolicity"), a collective attribution, the twentieth century, and an untrusted `已验证`
status. It supplies no primary source, theorem locator, definition, premise, or conclusion. The
intake therefore preserves a subject-area boundary only.

## Proposition-changing decisions

An approved statement correction must obtain an exact source and freeze all of the following:

- discrete time (a self-map or diffeomorphism) versus continuous time (a flow), including
  invertibility and the time domain;
- a smooth finite-dimensional manifold, a Banach manifold, a vector bundle cocycle, or another
  phase-space category, with dimension, universes, compactness, metric, norm, and regularity;
- a fixed point, periodic orbit, compact invariant subset, nonwandering set, or whole phase space;
- local linear hyperbolicity, uniform hyperbolicity, partial hyperbolicity, or nonuniform/Pesin
  hyperbolicity;
- the stable/unstable splitting, or stable/center/unstable splitting for a flow, its continuity or
  measurability, derivative/cocycle invariance, and direct-sum requirements;
- the exact constants, iterate directions, exponential inequalities, and strict bounds used to
  express contraction and expansion; and
- one truth-valued conclusion, with its ordered quantifiers, all assumptions, exceptional cases,
  and whether it is a definition equivalence, existence theorem, or consequence.

These choices yield inequivalent propositions. They are a resolution checklist, not a canonical
claim.

## Candidate families not credited

- A characterization of a hyperbolic fixed or periodic orbit by the derivative spectrum.
- Existence or properties of a continuous invariant stable/unstable splitting on a uniformly
  hyperbolic compact set.
- Stable/unstable manifold, shadowing, expansivity, local-product, robustness, or structural-
  stability theorems under hyperbolicity assumptions.
- Spectral decomposition or symbolic coding of a source-specified Axiom A or hyperbolic system.
- Nonuniform hyperbolicity results using Lyapunov exponents and measurable Oseledets splittings.

No family in this list is selected or credited at intake.

## Explicit exclusions

The intake must not silently replace the target with separately cataloged Anosov diffeomorphisms
(`THM-M-1412`), Axiom A systems (`THM-M-1413`), spectral decomposition (`THM-M-1414`), Markov
partitions (`THM-M-1415`), hyperbolic-system measures (`THM-M-1416` and `THM-M-1417`), Lyapunov
exponents (`THM-M-1418`), Oseledets' theorem (`THM-M-1419`), or Pesin theory (`THM-M-1420`).
Hartman-Grobman (`THM-M-1345`), the stable manifold theorem (`THM-M-1346`), the Smale horseshoe
(`THM-M-1365`), and structural stability (`THM-M-1366`) are also distinct roots.

Likewise excluded are `Matrix.IsHyperbolic` for two-by-two matrices, hyperbolic geometry or
trigonometry APIs, a finite linear example, a generic invariant-set lemma, and any record that
assumes the desired splitting, estimates, or conclusion as fields. None can identify or close the
catalog topic.

## Formal boundary

No canonical Lean expression is frozen. Pinned mathlib provides adjacent flow, invariant-set,
periodic-point, manifold-derivative, and tangent-map APIs, but the intake-only bounded search found
no exact hyperbolic-dynamics or Anosov surface. These facts show possible substrate only; they are
not an anchor audit, statement elaboration, or machine-proof evidence.
