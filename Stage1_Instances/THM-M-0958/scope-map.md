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

The statement phase selects the exact arXiv-v1 equation (5) formula above as the canonical
quantitative scale. It expands `Omega` using the paper's own definition and uses the one-based
extremal-function conclusion as the root.

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

These choices are now resolved by `Statement.lean`: the canonical root is the one-based extremal
inequality; `Finset.Ico 1 (n + 1)` represents `{1, ..., n}`; `SourceProgressionFree` is checked
equivalent to `ThreeAPFree`; `c`, `N`, then `n` are the ordered binders; the cardinality is coerced
to `Real`; every logarithm is `Real.logb 2`; the construction witness and zero-based Roth number
are credited only through checked iff witnesses; and the relative comparison is not part of the
root.

The SODA and journal bodies still require full comparison and independent source review. That is
H1 source-assurance debt, not an unresolved Lean statement encoding.

## Boundary cases

- `n = 0`, `1`, and `2`, where logarithms or the notion of a nontrivial triple need special care.
- Values below the asymptotic threshold and the source's remark that a sufficiently small universal
  constant can absorb finite cases.
- The empty set, singleton sets, two-element sets, and all of the ambient interval.
- Constant triples, repeated endpoints, and triples whose average is not integral.
- One-based versus zero-based intervals, including the translation by one.
- Positivity of the real lower-bound expression and conversion of a real inequality to a natural
  cardinality claim.

The asymptotic root asserts only indices satisfying `0 < N` and `N <= n`. Thus `n = 0`, `1`, `2`,
and other small values may lie below the threshold, while the threshold value itself is included.
The totalized Lean scale and source interval at `n = 0` and `n = 1` are separately checked. No
floor or ceiling is introduced in the real-cardinality inequality.

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

The canonical Lean expression and two checked alternate encodings are frozen in `Statement.lean`
and `statement.json`. The anchor discovery protocol, obligation registry, and proof state remain
downstream and open.
