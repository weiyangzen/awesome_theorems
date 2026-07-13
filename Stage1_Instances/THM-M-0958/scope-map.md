# Scope map

## Preserved theorem family

The repository fixes target `THM-M-0958`, the name `Elkin construction`, Michael Elkin, 2011, and
the qualitative gloss `improvement of the Behrend construction`. The matching primary paper
concerns large three-term-progression-free subsets of integer intervals and improves Behrend's
asymptotic lower bound. That identifies a theorem family, not yet a binder-complete canonical
claim.

The inspected arXiv v1 candidate reports, using base-2 logarithms, a progression-free subset of
`{1, ..., n}` whose size is of order at least

```text
(log_2 n)^(1/4) * n / 2^(2 * sqrt(2) * sqrt(log_2 n)).
```

This formula is a source locator only. It is not frozen as the canonical statement during intake.

## Proposition-changing decisions

The exact-source statement phase must freeze all of the following:

1. Whether the root is stated as existence of a finite set `S` for all sufficiently large `n`, or
   as a lower bound on the extremal function `nu(n)` / `rothNumberNat n`.
2. The ambient interval `{1, ..., n}`, `[1, n + 1)`, or `range n`, including a checked translation
   and the endpoint/off-by-one convention.
3. The definition of an arithmetic triple: three distinct integers with one the average of the
   other two, or mathlib's additive equation with trivial progressions excluded by equality.
4. The ordered binders hidden by `Omega`: a positive universal real constant, a positive integer
   threshold, and every integer `n` beyond that threshold.
5. The exact real coercions and ordering between `card S : Nat` and the real-valued lower-bound
   expression.
6. The source convention that `log` is base 2, the positive-real domain of square roots and fourth
   powers, and whether an equivalent natural-log/exponential expression is credited.
7. Whether the claim includes only the asymptotic lower bound or also the relative statement that
   it improves Behrend by `Theta(sqrt(log n))`.
8. Which edition is authoritative: arXiv v1 (2008), the SODA 2010 proceedings version, or the 2011
   journal publication, and how any formula or proof changes are mapped.
9. Whether the source's construction is part of the formal target or only the existential/extremal
   conclusion.

Every alternate form needs a checked relationship witness before statement or proof credit.

## Boundary cases

- `n = 0`, `1`, and `2`, where logarithms or the notion of a nontrivial triple need special care.
- Values below the asymptotic threshold and the source's remark that a sufficiently small universal
  constant can absorb finite cases.
- The empty set, singleton sets, two-element sets, and all of the ambient interval.
- Constant triples, repeated endpoints, and triples whose average is not integral.
- One-based versus zero-based intervals, including the translation by one.
- Positivity of the real lower-bound expression and conversion of a real inequality to a natural
  cardinality claim.

No case is excluded at intake because no canonical proposition is selected.

## Explicit exclusions

- `THM-M-0957` or `Behrend.roth_lower_bound` without Elkin's quantitative improvement.
- Roth's upper-density theorem (`THM-M-0947`) or `rothNumberNat_isLittleO_id`.
- A generic claim that some progression-free set exists, without the source's quantitative bound.
- The improvement-factor comparison alone, without a source-faithful base lower bound.
- A fixed finite `n`, a finite computational search, or a numerically sampled asymptotic claim.
- Progression-free subsets of finite fields, cyclic groups, cap sets, or longer progressions.
- A hypothesis or structure that stores the desired set or lower bound.
- The catalog's untrusted verified label, the Lean API probe, or the pinned Behrend theorem used as
  target proof credit.

No canonical Lean expression, alternate encoding, discovery protocol, obligation registry, or
proof state is frozen during intake.
