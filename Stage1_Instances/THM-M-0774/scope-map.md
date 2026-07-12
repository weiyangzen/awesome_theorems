# Scope map

## Provisional included claim

- A type `alpha` equipped with a partial order.
- Nonemptiness of `alpha`, either explicit or derivable from the chain-bound premise, according to
  the selected source statement.
- A hypothesis that every chain in `alpha` has an upper bound in `alpha`.
- Existence of an element `m : alpha` maximal for the order: any `a` with `m <= a` equals `m`.

This is the conventional theorem family suggested by the repository label. It is a provisional
scope, not a reconstruction of an inspected primary theorem.

## Decisions required at statement freeze

The next phase must select an inspected primary edition and freeze whether chains may be empty;
whether upper bounds must lie in the whole poset or a distinguished subset; whether nonemptiness is
an independent premise; the exact definitions of chain, upper bound, and maximality; universe and
binder order; and whether the conclusion supplies a maximal element globally or one above a given
starting element. It must test the empty-poset boundary and distinguish maximal from greatest.

The likely Lean vocabulary is `PartialOrder`, `Set`, `IsChain`, `BddAbove`, and `IsMax`. Pinned
mathlib's `Mathlib.Order.Zorn` and declaration `zorn_le` are discovery candidates only. Exact type,
axioms, provenance, and source identity belong to later statement and anchor-audit phases.

## Explicit exclusions

- The false unconditional claim that every partial order has a maximal element, such as the
  integers with their usual order.
- Existence of a greatest element (`IsGreatest`) as a substitute for a maximal element (`IsMax`).
- A result only for finite posets.
- Hausdorff's maximal-chain principle, the well-ordering theorem, or Tukey's lemma as the canonical
  target merely because they are choice-equivalent.
- A subset-relative Zorn theorem or an extension-above-a-starting-point theorem unless the selected
  source explicitly fixes that form and checked transports preserve the repository claim.
- The repository label `已验证` or a discovered theorem name as proof evidence.
