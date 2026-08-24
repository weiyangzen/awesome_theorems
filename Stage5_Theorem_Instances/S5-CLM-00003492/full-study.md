# Full study: the `n²` upper bound for 2-increasing triples

## Statement and definitions

For triples `a,b : Fin 3 → ℕ`, write `a <₂ b` when there are two distinct coordinates at which `a` is strictly smaller than `b`. A list is 2-increasing when every earlier element is `<₂` every later element. The coordinates are restricted to the discrete interval `{1,…,n}`. The theorem says that such a list has length at most `n²`, and hence its maximal possible length `F(n)` is at most `n²`.

The bound depends on positions, not on set cardinality. A list may in principle contain repeated values, but repeated triples immediately violate the pairwise strict-growth condition. The formal argument nonetheless maps positions, which avoids silently assuming nodup.

## Pigeonhole map

For a position `k`, retain only `(s[k] 0, s[k] 1)`. The range hypothesis places both entries in `Finset.Icc 1 n`. Natural interval cardinality gives `n` choices per coordinate and hence `n²` pairs. If the list has more than `n²` positions, `Finset.exists_ne_map_eq_of_card_lt_of_maps_to` produces two distinct positions with the same pair.

This step works uniformly for small `n`. When `n=0`, the target box is empty and the hypotheses of a too-long admissible list are inconsistent; no separate provider lemmas for `F(0)` or `F(1)` are needed.

## Order-sensitive contradiction

The collision indices are distinct but initially unordered. `Fin` is linearly ordered, so either `i<j` or `j<i`. Pairwise list membership supplies `<₂` in the corresponding direction. Equality at coordinates `0` and `1` gives weak reverse inequalities at both coordinates. Any strict-growth witness must avoid both; because `Fin 3` has only one remaining coordinate, its two witness indices cannot remain distinct. The helper lemma closes this finite case with arithmetic over `Fin 3`.

## Supremum closure

The defining set contains `0`, witnessed by the empty list. The collision argument bounds every member by `n²`. The natural complete-lattice lemma `csSup_le` now gives the required supremum inequality. This is the exact role of nonemptiness: it is recorded explicitly rather than hidden behind a special-case formula for natural supremum.

## Semantic identity

The frozen header uses the local notation `F`. Its expansion is determined by source declarations `maximalLength`, `IsIncreasing₂`, and `lt₂`. The claim-owned root spells out all three bodies, retaining the same binder-style set comprehension and universe/types. No symbol is locally redefined, aliased, coerced, or parsed differently. A second explicit-witness presentation is related by proved set equalities in `Statement.lean` and the standalone provider-native `Audit.lean`; both transport directions are named in the audit.

The canonical Master must still recompute the elaborated source and target expressions and the transitive non-foundation environment. Worker-supplied digests are routing commitments, never a substitute for that recomputation.

## Exceptional cases and downstream use

The proof covers every `n : ℕ` without a positivity assumption. Its output is the sharp elementary upper bound used to bracket later asymptotic and construction results in the same source family. The argument does not prove attainability, the perfect-square lower bound, or the later logarithmic improvement; those are separate downstream declarations.

## Trust boundary

Mathlib's finite-set cardinality, pigeonhole, list-pairwise, arithmetic, and supremum lemmas, reached through the exact provider module, are the only imported proof infrastructure. The claim adds only transparent theorem/lemma declarations. `Proof.lean` records the modular reconstruction, while `Audit.lean` repeats the terminal root so it can be compiled directly from the sealed provider environment without a claim-module search-path assumption. The provider import establishes provenance and exact semantics, while the provider theorem body provides no proof authority. Canonical trust-zero compilation, axiom inspection, cold from-source replay, read tracing, and semantic-substitution mutation remain Master responsibilities.
