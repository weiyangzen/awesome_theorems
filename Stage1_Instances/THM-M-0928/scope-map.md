# Scope map

## Preserved repository scope

The repository fixes target `THM-M-0928`, the title `波利亚计数定理`, attribution to George Pólya,
the year 1937, and the gloss `考虑对称性的计数`. This intake preserves the Pólya enumeration
theorem family: enumerating colorings or configurations modulo a finite symmetry action by using
the action's cycle information. Importance `高` and status `已验证` are catalog metadata, not
human-source or kernel evidence.

The gloss does not state one truth-valued proposition. A cycle-index identity, a coefficient
formula for a fixed color inventory, and the total number of orbits under unrestricted colors have
different inputs and conclusions even though all are conventionally called Pólya enumeration.

## Candidate formulations not credited

1. For a finite permutation group acting on a finite position set and a finite color set of size
   `q`, the number of coloring orbits is the group average of `q` raised to the number of cycles of
   each induced position permutation.
2. The cycle-index substitution form, where power-sum variables are replaced by the color inventory
   generating expression and the resulting polynomial enumerates orbits by color multiplicity.
3. A prescribed-inventory coefficient formula, where only colorings using fixed multiplicities are
   counted.
4. A weighted-color or figure-inventory formulation in a coefficient ring, which requires explicit
   semiring, finiteness, and substitution hypotheses.
5. Burnside's orbit-counting identity applied to the coloring action before the cycle-count formula
   for fixed colorings has been proved.

The fifth item is a proof route or intermediate identity, not automatically the Pólya enumeration
root. The first four are related theorem variants, not interchangeable spellings.

## Decisions required before statement freeze

The statement phase must independently approve and freeze:

1. A preserved source edition and pinpoint theorem, formula, or section, including incorporated
   definitions, proof boundary, translation policy, corrections, errata, and independent review.
2. The finite position type, symmetry group, faithful permutation representation or action, and
   whether the action is left or right.
3. The color type, its finiteness and cardinality, and whether colors are unrestricted, weighted,
   or subject to prescribed multiplicities.
4. The coloring action, orbit quotient, fixed-coloring predicate, and exact notion of equivalence.
5. Whether the conclusion is a natural-number orbit count, an averaged rational identity, a cycle
   index polynomial identity, a coefficient statement, or a source-approved package of them.
6. The cycle statistic, including fixed points as one-cycles, and the checked bridge from fixed
   colorings to a product or power indexed by cycles.
7. Ordered binders, universes, typeclass context, division or integrality convention, alternate
   encodings, foundation/TCB/computation profiles, and every boundary mutation.

## Degenerate and boundary cases

No case is excluded at intake. Statement review must explicitly disposition the trivial group, the
empty position set, an empty color set, a singleton color set, a trivial action, nonfaithful actions,
zero colors on zero or nonzero positions, repeated color weights, zero multiplicities, inventories
whose multiplicities do not sum to the number of positions, and whether one-cycles include fixed
positions outside permutation support.

It must also distinguish division in `Nat`, `Int`, `Rat`, or a polynomial coefficient ring. Burnside's
integrality consequence cannot be assumed merely by writing an average in a field.

## Neighbor and substitution boundaries

- `THM-M-0929` (Burnside's lemma) is the adjacent orbit-counting theorem. It can be a typed proof
  dependency after both scopes are accepted, but its root is not the cycle-index/substitution result.
- `THM-M-0913` (inclusion-exclusion), `THM-M-0915` (generating functions), and sequence targets such
  as `THM-M-0921` are separate theorem families and contribute no inherited status.
- Counting labeled colorings without quotienting by symmetry, counting orbits without the cycle
  evaluation, or proving a numerical necklace/graph example does not establish the general theorem.
- A structure, hypothesis, or polynomial definition that stores the desired enumeration identity,
  the catalog's `已验证` label, or successful `#check` output supplies no proof credit.

Statement ambiguity blocks obligation-tree construction. No canonical expression fingerprint,
discovery-protocol hash, obligation-registry hash, or proof body is frozen during intake.
