# Scope map

## Preserved catalog scope

The intake preserves the catalog's real-analysis sequence-selection family: a bounded sequence has
a convergent subsequence. Its category and title make a real-valued sequence the conventional
candidate, but the literal gloss does not contain the codomain or a binder-complete proposition.
An exact source proposition and independent review must authorize that choice at statement freeze.

A likely modern real-sequence encoding, not yet credited as the canonical statement, has:

- a sequence `x : Nat -> Real`;
- boundedness of `Set.range x`, ordinarily `Bornology.IsBounded (Set.range x)`;
- a strictly increasing selector `phi : Nat -> Nat`;
- a limit `a : Real`; and
- `Filter.Tendsto (x \circ phi) Filter.atTop (nhds a)`.

## Proposition-changing decisions

The statement phase must freeze all of the following from an admitted source rather than from the
name alone:

1. Whether the carrier is `Real`, finite-dimensional Euclidean space, or another proper metric
   space. A proper-metric theorem is a generalization and cannot replace the catalog root silently.
2. Whether boundedness is order boundedness, metric/bornological boundedness of the range, or an
   explicit absolute-value bound, and the checked relationship between encodings.
3. The index domain and the exact subsequence representation: a strictly increasing natural map,
   an order embedding, or another source-approved object.
4. The convergence topology, binder order, equality orientation, and whether the limit is merely in
   the carrier, in the closure of the sequence range, or in a specified containing set.
5. Whether the result assumes every term lies in one bounded set or only frequently many terms do.
6. The source edition, theorem/page, incorporated definitions, proof boundary, translation,
   correction or errata record, and independent review.
7. The foundation, classical-choice, TCB, computation, and freshness profiles for the selected
   target and minimal imports.

## Boundary and mutation cases

Constant, singleton-range, finite-range, oscillating, and boundary-valued bounded sequences remain
inside the conventional theorem. Natural-number indexing has no empty whole sequence, although a
purported selector can fail to be strictly increasing. Statement mutations must reject removal of
boundedness, a selector without order preservation, convergence of only the full sequence, a fixed
preselected limit, and any conclusion demanding that the limit be an actual range value rather
than a closure point.

No uniqueness, rate of convergence, monotonicity of selected values, computable selector, or
convergence of the original sequence is part of the catalog gloss.

## Duplicate and substitution exclusions

- `THM-M-0619` separately catalogs Bolzano-Weierstrass as convergence of a subsequence in a compact
  metric space. Its compact-space statement, status, and evidence are not inherited.
- `SeqCompactSpace.tendsto_subseq` and `IsCompact.tendsto_subseq` are compactness interfaces, not an
  automatic replacement for the bounded real-sequence root.
- Monotone convergence, Cauchy completeness, Heine-Borel, sequential compactness, and interval
  nesting may later be proof dependencies or checked transports; none is a substitute target.
- A finite-dimensional or proper-space generalization cannot broaden the root without an exact
  checked specialization and source-approved mapping.
- The untrusted `已验证` label, an API name, a successful `#check`, or a premise that already stores
  a convergent subsequence supplies no proof credit.

## Formal boundary

Pinned mathlib module `Mathlib.Topology.MetricSpace.Sequences` directly exposes
`tendsto_subseq_of_bounded`. The interface is unusually close to the catalog gloss, so the intake
records `M3`, not `M4`. Nevertheless, its extra proper-metric generality and closure-membership
conclusion do not settle the source root. Minimal imports, exact expression and environment
fingerprints, checked specialization or transport, mutation tests, terminal proof-body provenance,
and trust closure all remain downstream.
