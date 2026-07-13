# Scope map

## Preserved catalog scope

This intake preserves exactly the point-set-topology family named by the catalog: a sequence in a
compact metric space has a convergent subsequence. Importance "high" and status `已验证` are
inventory metadata, not source or kernel evidence.

One conventional carrier formulation, recorded only as a resolution candidate, has:

- a type `X` carrying a metric and compact-space structure;
- a sequence `x : Nat -> X`;
- a selector `phi : Nat -> Nat` with `StrictMono phi`; and
- a point `a : X` such that `x \circ phi` tends to `a` along `Filter.atTop`.

The set formulation instead fixes a metric ambient type, a set `s`, `IsCompact s`, and membership
of every `x n` in `s`, and concludes that the limit lies in `s`. No source decision currently
selects either form or a checked relationship between them.

## Proposition-changing decisions

The statement phase must freeze all of the following from an admitted source and then elaborate and
mutation-test the result:

1. Compact metric carrier versus compact subset of a metric ambient space.
2. `MetricSpace`, `PseudoMetricSpace`, another uniform/first-countable encoding, and all universes
   and typeclass assumptions. A first-countable compact-space theorem is a generalization, not an
   automatic replacement for the metric wording.
3. Natural-number indexing and a strictly increasing selector versus another subsequence object.
4. Exact convergence topology, composition orientation, ordered binders, and whether limit
   membership in a compact subset is explicit.
5. Whether empty carriers or empty compact sets are excluded, vacuous, or impossible under the
   chosen quantifier order.
6. Foundation, classical-choice, TCB, computation, platform, freshness, source-edition, theorem
   locator, translation, correction, errata, and independent-review policies.

## Boundary and mutation cases

Constant, periodic, finite-range, eventually constant, and nonconvergent sequences with convergent
subsequences remain inside the intended family. A compact-set formulation must resolve `s = empty`
and make membership assumptions and limit membership explicit. A compact-carrier formulation must
resolve the empty type and the fact that a supplied sequence already witnesses nonemptiness.

Required downstream mutations include removing compactness, changing the carrier to an arbitrary
metric space, weakening strict monotonicity of the selector, changing binder scope so the limit or
selector is fixed before the sequence, and demanding convergence of the original sequence. No
unique limit choice, rate, computable selector, monotone selected values, or finite selector is in
the received gloss.

## Duplicate and substitution exclusions

- `THM-M-0264` owns the real-analysis statement that every bounded sequence has a convergent
  subsequence. Its scope, proof, and receipts are not inherited.
- `SeqCompactSpace.tendsto_subseq` assumes sequential compactness; without a checked compact-metric
  bridge it cannot replace the requested root.
- `isCompact_iff_isSeqCompact` is an equivalence theorem, not by itself the requested extraction
  statement.
- Heine-Borel, bounded-sequence extraction in a proper space, total boundedness plus completeness,
  cluster-point existence, or special cases over `Real` or `Real^n` may become dependencies or
  checked transports but cannot substitute for this target.
- A premise or structure that already stores the desired subsequence, an API name, a successful
  `#check`, or the untrusted `已验证` label supplies no proof credit.

## Formal boundary

Pinned mathlib module `Mathlib.Topology.Sequences` exposes direct compactness interfaces. The intake
therefore records `M3`, not `M4`. However, no minimal root import, canonical Lean expression,
environment fingerprint, checked metric specialization or carrier/set transport, statement
mutation, terminal proof-body provenance, dependency closure, or accepted trust profile is frozen.
The bounded search and probe are intake discovery only, not the later exhaustive anchor audit.
