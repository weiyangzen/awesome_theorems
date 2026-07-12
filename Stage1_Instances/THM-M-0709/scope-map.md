# Scope map

## Included claim

1. **Instance:** a finite ordered collection of tiles `(u_i, v_i)`, where both components are
   finite words over one fixed finite alphabet.
2. **Witness:** a nonempty finite sequence of valid tile indices; repetition is allowed.
3. **Match:** concatenating the `u` components in witness order equals concatenating the `v`
   components in the same order.
4. **Uniform problem:** the input ranges over arbitrary effectively encoded finite instances, not
   over witnesses for one fixed instance.
5. **Conclusion:** the solvability predicate has no total computable decider under the selected
   encoding (or under a machine model connected to it by checked equivalence).

## Decisions required at statement freeze

- Select a concrete fixed alphabet, probably a binary finite type, and state its nondegeneracy.
- Select the tile container, word representation, code type, encoder/decoder, and malformed-code
  convention. Prove that coding preserves the semantic match relation.
- Select whether undecidability is expressed as `¬ ComputablePred p`, absence of a Turing-machine
  decider, or a reduction theorem plus a checked wrapper. Freeze ordered binders and negation scope.
- Decide whether the empty tile list is admitted as a negative instance and ensure the empty
  witness is excluded.
- Record minimal imports, elaborated expression and environment fingerprints, and mutation tests.

## Explicit exclusions

- The modified correspondence problem with a prescribed first tile, without a checked reduction.
- Bounded PCP, mortality, matrix mortality, semi-Thue reachability, the word problem, or tiling
  undecidability as substitutes.
- Merely proving that solution search is recursively enumerable.
- A theorem assuming an undecidable predicate or an assumed reduction package as input.
- A Boolean `Decidable` instance in Lean: classical decidability is not computability.
- An abstract `Prop` called `HasMatch` with no effective instance representation.
- Any claim derived solely from the repository's `已验证` label.

The proof architecture, canonical obligation registry, candidate formal anchors, and proof-body
provenance deliberately remain unfrozen because those belong to later dependent phases.

