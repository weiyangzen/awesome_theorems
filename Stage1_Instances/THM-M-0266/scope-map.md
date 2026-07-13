# Scope map

## Frozen identity

- Theorem ID: `THM-M-0266`.
- Assigned node: `S56-M-0266-INTAKE`.
- Manifest rank: 1274.
- Catalog name: Stone-Weierstrass theorem.
- Catalog attribution and date: Marshall Stone, 1937.
- Literal catalog claim: density of algebras of continuous functions.
- Category: analysis / real analysis.
- Lifecycle: `planned`; uniform baseline `L0 / rework_required`.

The catalog wording identifies a theorem family, not an exact statement. The canonical human claim,
Lean expression, expression hash, and environment fingerprint therefore remain null. This is a
hard blocker for the dependent statement phase, not permission to choose a familiar version.

## Proposition-changing decisions

An admitted primary source and independent review must decide all of the following before statement
freeze:

1. Whether the root is the real theorem for a unital `Real`-subalgebra, a complex or general
   `RCLike` theorem for a star-subalgebra, or another historically faithful form.
2. Whether the domain is a compact topological space, a compact Hausdorff space under a historical
   convention, or a compact subset of a noncompact ambient space.
3. Whether density is stated as closure equal to top, membership of every continuous function in
   the closure, uniform norm approximation, or pointwise epsilon bounds.
4. Which topology or norm is used on the continuous-function algebra and whether functions are
   bundled as continuous maps.
5. The exact unital/constant-function hypothesis, point-separation predicate, scalar structure,
   star or conjugation-closure requirement, typeclass assumptions, universes, and binder order.
6. Whether the empty and singleton spaces, the bottom or top algebra, zero epsilon, and trivial
   separation cases are included, excluded, or discharged by convention.
7. Which credited alternate forms require equality, `Iff`, or one-way checked transports.

Mathlib's real `Subalgebra` is unital, so its constants requirement is structural rather than an
explicit hypothesis. Its complex/RCLike interface uses `StarSubalgebra`; silently dropping that
star-closure premise would strengthen the proposition. Those encoding choices need a reviewed
source crosswalk.

## Pinned formal candidates, not credited

The pinned module `Mathlib.Topology.ContinuousMap.StoneWeierstrass` exposes:

- `ContinuousMap.subalgebra_topologicalClosure_eq_top_of_separatesPoints`, the compact-domain real
  subalgebra closure-equality form;
- `ContinuousMap.continuousMap_mem_subalgebra_closure_of_separatesPoints`, the real elementwise
  closure-membership form;
- `ContinuousMap.exists_mem_subalgebra_near_continuousMap_of_separatesPoints`, the bundled uniform
  norm epsilon form;
- `ContinuousMap.exists_mem_subalgebra_near_continuous_of_separatesPoints`, an unbundled pointwise
  epsilon form;
- `ContinuousMap.exists_mem_subalgebra_near_continuous_of_isCompact_of_separatesPoints`, a
  compact-set form with a noncompact ambient space;
- `ContinuousMap.starSubalgebra_topologicalClosure_eq_top_of_separatesPoints`, the compact-domain
  `RCLike` star-subalgebra form.

The intake probe confirms that these names and types elaborate at the pinned revision. It does not
freeze minimal imports, normalize an exact root expression, establish a source-to-Lean transport,
inspect terminal bodies, or grant M0 proof credit.

## Excluded substitutions

- The polynomial Weierstrass approximation theorem (`THM-M-0265`) is a special case or supporting
  bridge, not a substitute for the separating-subalgebra root.
- Bishop's generalized Stone-Weierstrass theorem, lattice variants, nonunital locally compact
  variants, C*-algebra consequences, Fourier-density applications, and neural-network universal
  approximation are distinct targets unless a source-approved checked transport says otherwise.
- A real theorem cannot silently replace a complex theorem, nor can the RCLike star theorem replace
  a source that omits the star-closure premise.
- A compact-set local approximation cannot replace global density on a compact domain, or vice
  versa.
- The catalog's untrusted `verified` label, a theorem name, mathlib documentation, or successful
  API elaboration supplies no statement-identity or proof credit.

## Gate boundary

The intake may truthfully reach planned `[H1, M3, R4]`: a classical published family and direct
pinned Lean interfaces are identified, while source fidelity, exact target identity, and readable
root reconstruction remain open. Obligation and discovery hashes stay null. Every dependent phase
remains open in `task-dag.json`.
