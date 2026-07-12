# Scope map

## Received scope

The mathematical catalog fixes only the title `Anosov微分同胚`, the attribution Dmitri Anosov,
the year 1967, and the gloss `一致双曲系统` ("uniformly hyperbolic system"). It gives no
primary source, theorem locator, definitions, hypotheses, or truth-valued conclusion. Its
`已验证` label is preserved in the rev-5.6 manifest only as untrusted source metadata.

## Candidate mathematical boundary

An eventual exact target may concern an Anosov diffeomorphism only if an accepted source fixes all
of the following:

- a smooth manifold, including scalar field, dimension/model space, compactness, boundary,
  connectedness, topology, smooth structure, and any Riemannian metric or tangent norm;
- a global diffeomorphism and its exact differentiability class;
- whether hyperbolicity is asserted on the whole manifold or only on a specified invariant set;
- a stable/unstable tangent splitting or an equivalent source-selected encoding, including its
  continuity, directness, fiber dimensions, and invariance under the derivative cocycle;
- uniform constants and exact contraction/expansion inequalities, including the iterate domain,
  inverse convention, norm, strictness, and all side conditions;
- the exact conclusion: a definition/classification predicate, existence or nonexistence,
  equivalence of definitions, structural stability, expansivity, stable manifolds, or another
  consequence.

These bullets are a scope inventory, not a canonical claim. No candidate family is credited at
intake.

## Ambiguities to resolve

1. Whether the catalog item intends the definition of an Anosov diffeomorphism or a theorem about
   the class.
2. Whether the intended setting is a compact Riemannian manifold, a compact smooth manifold with
   an existential adapted metric, or a broader finite-dimensional or Banach-manifold setting.
3. Whether the splitting is expressed by subbundles, fiberwise subspaces, projections, cone
   fields, or another equivalent formulation, and which transports must be checked.
4. Whether estimates use `C * lambda^n`, a one-step contraction bound, forward estimates on the
   stable bundle plus backward estimates on the unstable bundle, or a two-sided integer cocycle.
5. Whether zero-dimensional stable or unstable fibers are allowed and how empty, singleton,
   disconnected, noncompact, or boundary-bearing manifolds are handled.
6. Whether "1967" points to a particular monograph result, definition, or later standard theorem;
   the repository supplies no edition, page, theorem number, or translation.
7. Whether examples such as hyperbolic toral automorphisms are inputs, witnesses, or the actual
   target, and whether consequences such as structural stability belong to this item.

## Explicit exclusions

- Replacing this item by generic hyperbolic dynamics (`THM-M-1411`), Axiom A (`THM-M-1413`),
  spectral decomposition (`THM-M-1414`), or Markov partitions (`THM-M-1415`).
- Replacing a whole-manifold Anosov condition by a hyperbolic fixed point, periodic orbit, linear
  operator, or invariant subset without a source-approved identity mapping.
- Choosing the structural stability, stable-manifold, shadowing, expansivity, mixing, ergodicity,
  or periodic-orbit theorem merely because it is associated with Anosov systems.
- Proving only a convenient toral example when the selected source asks for a general theorem, or
  generalizing a source-specific result without checked equivalence.
- Defining a structure that contains the requested splitting, invariance, and estimates as fields
  and then calling a projection of those fields the target proof.
- Treating generic `Diffeomorph`, `mfderiv`, `tangentMap`, or subspace APIs as an Anosov theorem.
- Treating the repository label `已验证`, an API probe, or a topic-level citation as source or
  proof evidence.

## Formal boundary

No canonical Lean expression is frozen at intake. Pinned mathlib exposes generic manifold
diffeomorphisms and tangent-derivative maps, but the bounded target-name search found no obvious
Anosov or uniformly-hyperbolic dynamical-system declaration. Generic substrate neither determines
nor proves a target theorem. Exact imports, binders, expression and environment fingerprints,
alternate transports, and structural mutations belong to the dependent statement phase after a
primary-source proposition has been selected and independently approved.
