# Full study — `Arxiv.«1609.08688».maximalLength_le`

<a id="fragment-input-contract"></a>
## Fragment N0 — input and semantic contract

**Hypotheses.** Fix `n : ℕ`. An admissible list `s` consists of maps
`Fin 3 → ℕ`; every coordinate lies in `Set.Icc 1 n`; and `s` is pairwise under
the relation saying that two distinct coordinates increase strictly.
**Inference.** Delta-unfold the provider's `maximalLength`, `IsIncreasing₂`,
`lt₂`, and local notation `F`; this produces exactly the claim-owned root in
`Proof.lean`, without introducing any replacement declaration.
**Output.** The goal is the supremum of admissible list lengths at most `n²`.
**Formal anchor.** `Statement.lean#statement_bidirectional_crosswalk`.
**Downstream uses.** Establishes the types consumed by N1–N6.
**Exceptional cases.** `n=0` and `n=1` remain in the same quantified root.
**Trust boundary.** Frozen source bytes establish provenance; Master must
independently recompute elaborated-expression identity.

<a id="fragment-pigeonhole-space"></a>
## Fragment N1 — finite pigeonhole space

**Hypotheses.** Assume an admissible list has length strictly greater than
`n²`.
**Inference.** Map a position `k` to `(s[k] 0, s[k] 1)` and use the range
hypothesis to show that this pair belongs to
`Finset.Icc 1 n ×ˢ Finset.Icc 1 n`. This product contains exactly `n²` pairs,
strictly fewer than the positions.
**Output.** A finite map from a larger domain into a smaller target.
**Formal anchor.** `Proof.lean#proof_exists_equal_first_two`, definitions of
`f`, `t`, `htCard`, and `hf`.
**Downstream uses.** N2 applies finite pigeonhole to this map.
**Exceptional cases.** If an interval is empty, `hf` itself exposes the
impossibility of a nonempty bounded list; the cardinal argument is still valid.
**Trust boundary.** Cardinal arithmetic and interval membership are discharged
by Mathlib; Master replays them at trust zero.

<a id="fragment-collision"></a>
## Fragment N2 — collision extraction

**Hypotheses.** The map of N1 sends every list position into the smaller finite
product.
**Inference.** Apply `Finset.exists_ne_map_eq_of_card_lt_of_maps_to`; project
equality of ordered pairs with `Prod.fst` and `Prod.snd`.
**Output.** Distinct indices `i,j` satisfying `s[i] 0 = s[j] 0` and
`s[i] 1 = s[j] 1`.
**Formal anchor.** `Proof.lean#proof_exists_equal_first_two`, final two proof
steps.
**Downstream uses.** N4 orients these indices and invokes N3.
**Exceptional cases.** No ordering of `i,j` is assumed at this stage.
**Trust boundary.** Only the stated finite pigeonhole theorem and congruence
projections are used.

<a id="fragment-local-contradiction"></a>
## Fragment N3 — equal coordinates forbid two increases

**Hypotheses.** Triples `a,b` agree at coordinates zero and one.
**Inference.** Exhaust the three possibilities for each of two distinct
indices. Any distinct pair contains zero or one, where equality contradicts
the asserted strict inequality; equal indices contradict distinctness.
**Output.** It is impossible for `a` to be strictly smaller than `b` in two
distinct coordinates.
**Formal anchor.**
`Proof.lean#proof_not_two_increases_of_equal_first_two`.
**Downstream uses.** N4 contradicts the pairwise relation in either index
orientation.
**Exceptional cases.** All nine ordered pairs of coordinates are covered by
`fin_cases`; none is silently excluded.
**Trust boundary.** The finite case split and irreflexivity of `<` are kernel
checked by Master.

<a id="fragment-pairwise-contradiction"></a>
## Fragment N4 — orient and contradict pairwise increase

**Hypotheses.** N2 gives distinct positions with equal first two coordinates;
the list is pairwise two-increasing.
**Inference.** Linear order makes either `i<j` or `j<i`. In the first case,
`List.pairwise_iff_get` supplies the forbidden relation from `s[i]` to `s[j]`;
in the second it supplies the reverse relation, and the coordinate equalities
are symmetrized. N3 contradicts either relation.
**Output.** An admissible list cannot have length greater than `n²`.
**Formal anchor.** `Proof.lean#proof_maximalLength_le`, from the collision
through both branches of `lt_or_gt_of_ne`.
**Downstream uses.** N5 turns the pointwise length bound into a supremum bound.
**Exceptional cases.** Both possible orders of unequal positions are explicit.
**Trust boundary.** Pairwise lookup is a Mathlib theorem; no transitivity of
the two-coordinate relation is assumed.

<a id="fragment-supremum"></a>
## Fragment N5 — supremum composition

**Hypotheses.** The set contains lengths of exactly the admissible lists.
**Inference.** The empty list supplies length zero and proves nonemptiness.
For an arbitrary member, unpack its witnessing list and use N1–N4 to rule out
length greater than `n²`. Apply `csSup_le` to the resulting uniform bound.
**Output.** The exact claim-owned theorem
`proof_maximalLength_le (n) : sSup {...} ≤ n²`.
**Formal anchor.** `Proof.lean#proof_maximalLength_le` in full.
**Downstream uses.** This is the machine root audited by N6 and the release
candidate.
**Exceptional cases.** The empty-list witness and the contradiction proof are
valid for every natural `n`, including zero and one.
**Trust boundary.** No provider proof term is imported; Master must compile
this root from source with trust zero.

<a id="fragment-transport"></a>
## Fragment N6 — bidirectional transport and audit

**Hypotheses.** The frozen source statement and claim-owned statement are
compared after delta-unfolding the four provider-local surface constructs.
**Inference.** Their propositions are syntactically identical at the expanded
surface, so each direction is the identity proof. The audit file states both
directions independently.
**Output.** `audit_source_to_target` and `audit_target_to_source`, plus the
crosswalk equivalence.
**Formal anchor.** `Audit.lean` and
`Statement.lean#statement_bidirectional_crosswalk`.
**Downstream uses.** Semantic-environment audit and Master acceptance.
**Exceptional cases.** Transport is quantified over all `n`; no special case
or hypothesis is changed.
**Trust boundary.** Textual delta-expansion is worker evidence only. Master
must compare elaborated expressions and reject any semantic substitution.
