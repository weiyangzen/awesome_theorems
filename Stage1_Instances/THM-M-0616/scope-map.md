# Scope map

## Preserved theorem family

- Stable target: `THM-M-0616`; intake item: `S56-M-0616-INTAKE`; execution rank: 1310.
- Literal catalog claim: `ε-δ定义与开集原像定义等价`.
- Faithful English gloss: the epsilon-delta definition of continuity is equivalent to the
  definition by open preimages.
- Intended subject boundary: ordinary continuity of functions, not uniform continuity, compactness,
  convergence alone, or continuity of a particular named function.

The catalog wording is proposition-shaped and describes a recognizable theorem family. It still
does not determine the exact domain, quantifiers, definition variants, or formal packaging needed
for a canonical statement.

## Decisions required at the statement gate

| Surface | Open decision and proposition-changing effect |
|---|---|
| Domain and codomain | Choose real spaces, metric spaces, or pseudometric spaces. The Lean candidate is stated for two pseudometric spaces; this is broader than the inspected real-to-real source passage. |
| Continuity scope | Choose global `Continuous`, pointwise `ContinuousAt`, or relative `ContinuousOn`/`ContinuousWithinAt`. These have different binders and conclusions. |
| Open-set side | State that every open codomain set has an open preimage, or use the local open-neighborhood condition. A checked bridge is required for either alternate form. |
| Epsilon-delta side | Fix quantifier order, centers, source and target distances, positivity conditions, and strict or non-strict inequalities. |
| Topology-distance relationship | Require that both topologies are the ones induced by the selected metric or pseudometric structures; arbitrary unrelated topologies would make the equivalence false. |
| Root packaging | Decide whether the root directly equates the two expanded predicates or uses `Continuous f` as the common middle proposition and checked composition. |
| Source scope | Approve an exact source passage and decide whether its real-to-real theorem is the root or only a special case of a general metric-space theorem. |
| Profiles | Freeze ordered binders, universes, minimal imports, foundation/TCB/computation policy, expression fingerprint, and checked alternate transports. |

## Boundary cases to decide

No case is excluded at intake. The statement and source review must explicitly cover empty and
singleton domains or codomains, constant functions, empty subsets for an on-set formulation,
nonseparated pseudometric spaces where distinct points can have distance zero, arbitrary positive
epsilon, possible zero or nonpositive delta mutations, and whether extended metrics or only
real-valued distances are admitted.

The statement gate must also distinguish ordinary pointwise continuity, where delta may depend on
the center and epsilon, from uniform continuity, where delta is independent of the center.

## Explicit non-substitutions

- `THM-M-0633`, the separate uniform-continuity theorem on compact sets, is not this target.
- `ContinuousAt`, `ContinuousOn`, and `ContinuousWithinAt` may be alternate candidate scopes, but
  none can silently replace global continuity.
- A theorem only for `Real -> Real`, a fixed function, a compact domain, or a single point cannot
  replace a source-selected general metric-space claim.
- Sequential continuity, neighborhood-filter continuity, closed-set preimages, or preservation of
  limits require checked equivalences before they can be credited as alternate encodings.
- Uniform continuity, Lipschitz continuity, Holder continuity, differentiability, measurability,
  open-map behavior, and inverse continuity are materially different properties.
- An open-preimage structure field projected as its own proof does not establish the expanded
  epsilon-delta equivalence unless the exact composition is checked.
- A theorem name, `#check`, catalog status, textbook prose, numerical experiment, or assumed
  conclusion gives no proof credit.

## Formal boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`continuous_def` and the three `Metric.continuous*iff` declarations are direct formal leads.
Intake does not choose one as the root, freeze a normalized expression, establish a source
transport, audit terminal proof bodies or transitive trust, or claim `M0`. Those are dependent
statement, anchor-audit, proof, and validation tasks.
