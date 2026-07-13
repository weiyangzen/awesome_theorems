# Scope map

## Frozen identity

| Field | Intake value | Status |
|---|---|---|
| repository ID | `THM-M-0913` | frozen |
| execution item | `S56-M-0913-INTAKE`, rank 1455 | frozen |
| catalog name | `容斥原理` | frozen as source wording |
| catalog claim | `并集元素个数的计算公式` | frozen literally |
| attribution | many mathematicians; 19th century | catalog metadata only |
| lifecycle | `planned`, uniform `L0 / rework_required` | frozen |

The intake preserves only a cardinality-of-union inclusion-exclusion family. The catalog does not
contain a formula, binders, hypotheses, citation, or definition chain from which a single theorem
can be recovered without a scope decision.

## Candidate roots, not selected

1. **Two finite sets.** `|A union B| = |A| + |B| - |A inter B|`, with either natural-number
   rearrangement or a cast into an additive group.
2. **Arbitrary finite family.** The cardinality of a finite union equals the alternating integer
   sum of the cardinalities of all nonempty finite intersections. Pinned mathlib's
   `Finset.inclusion_exclusion_card_biUnion` has this shape.
3. **Weighted finite-family form.** The corresponding identity for a sum of a function over the
   union, of which cardinality is the constant-one specialization.
4. **Complement form.** The size of the intersection of complements as an alternating sum,
   requiring a finite ambient type.
5. **Measure or probability form.** A finite-union identity for measures or probabilities, with
   measurability and finiteness conditions that the catalog never states.

The theorem name favors a general inclusion-exclusion identity and the gloss favors a cardinality
form, but neither observation lawfully chooses one of these roots at intake.

## Proposition-changing decisions

The statement phase must freeze:

- two sets, a fixed number of sets, or an arbitrary finite indexed family;
- `Finset`, finite `Set`, `Fintype`, measure, or probability encoding;
- universe levels, index type, element type, finiteness and decidable-equality assumptions;
- the union operator and the intersection convention for every nonempty subfamily;
- equality in natural numbers via rearrangement or truncating subtraction, or equality after a
  cast to integers or another additive group;
- whether the empty family is included and what its union contributes;
- whether duplicate indexed sets, empty members, empty intersections, or an empty element type
  need explicit handling;
- whether weighted sums, complements, measure forms, and the two-set formula are alternate
  encodings, consequences, or outside the root;
- ordered binders, hypotheses, conclusion, foundation policy, and checked transports.

## Excluded substitutions

- the union bound `|union S_i| <= sum |S_i|`, which omits alternating correction terms;
- equality for pairwise-disjoint unions, which is a strictly easier special case;
- the two-set identity presented as the arbitrary finite-family formula without a checked bridge;
- a complement identity presented as the union identity without a finite-universe transport;
- a probability or measure formula with unstated measurability or finiteness assumptions;
- a structure or hypothesis that stores the desired equality;
- the catalog label `已验证` treated as source or kernel evidence.

## Boundary-case ledger

No case is excluded at intake. Later work must settle an empty index family, singleton family,
empty members, duplicate family members, empty element type, intersections indexed by nonempty
subsets, infinite ambient types with finite member sets, and any natural-to-integer cast. For the
pinned candidate, `s = empty` gives an empty union and empty alternating sum; this observed library
behavior is not yet an approved source boundary.

## Formal boundary

The discovery probe imports `Mathlib.Combinatorics.Enumerative.InclusionExclusion` and checks its
cardinality, weighted-sum, indicator, and complement variants plus the two-set cast identity. It
authenticates pinned names, types, and reported axioms. It does not prove that this import is
minimal, select a root, compare an elaborated target to the catalog, inspect terminal-body
provenance, or grant M0 credit.

## Gate boundary

`S56-M-0913-STATEMENT` must admit an immutable, independently reviewable source proposition or an
explicitly approved normalization of the catalog wording; settle every choice above; elaborate the
exact target under minimal imports; serialize expression and environment fingerprints; check every
credited transport; and run removed-hypothesis, changed-domain, changed-binder-scope, and boundary
mutations. Anchor audit, registry/graph freeze, proof, validation, and release remain open.
