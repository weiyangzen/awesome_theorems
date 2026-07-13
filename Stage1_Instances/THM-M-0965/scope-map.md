# Scope map

## Preserved theorem family

The target must remain the classical Ahlswede-Khachatrian theorem for uniform finite-set families.
For natural parameters `n`, `k`, and `t`, the source works with families of `k`-subsets of an
`n`-element ground set such that every two members intersect in at least `t` elements. It maximizes
the family cardinality over this class.

For an integer `i >= 0`, the standard candidate family consists of the `k`-subsets `F` satisfying

```text
|F intersect [t + 2i]| >= t + i.
```

The sharp cardinality claim says that every uniform `t`-intersecting family is no larger than the
largest feasible candidate family. The primary paper also classifies every optimizer, up to a
permutation of the ground set, with two adjacent candidate types possible on transition boundaries.

## Candidate roots not selected

1. **Sharp upper bound only.** Every uniform `t`-intersecting family has cardinality at most the
   maximum cardinality of the canonical candidate families.
2. **Maximum equality.** Define the extremal function `M(n,k,t)` and prove it equals that maximum.
3. **Full optimizer classification.** Add that every maximum family is isomorphic to the unique
   active candidate family, or to either adjacent candidate family at an equality boundary.
4. **Piecewise source theorem.** State the source's rational transition inequalities and its
   low-`n` whole-layer branch exactly, rather than using a finite maximum over candidates.

The catalog's word `完整刻画` can plausibly denote either the complete extremal-number formula or
the stronger optimizer classification. Intake does not silently choose among them.

## Decisions required at statement freeze

- Freeze ordered binders and exact constraints, including whether `1 <= t <= k <= n` includes all
  equality cases and how impossible or empty parameter regimes are expressed.
- Freeze the ground set as `Fin n` or an abstract finite type, and the family as a `Finset` or a
  finite `Set`; prove transports for every credited alternate encoding.
- Freeze `t`-intersection semantics. The source quantifies all member pairs; a distinct-pair
  predicate is equivalent only after using uniformity and `t <= k`.
- Define the canonical candidate family with a chosen initial segment or an arbitrary subset of
  cardinality `t + 2i`, and define isomorphism under ground-set permutations if classification is
  included.
- Freeze the feasible index set. The source prints `0 <= i <= floor((n-t)/2)`, while nonempty
  candidates also interact with `t + i <= k`; a Lean maximum needs an explicit finite domain.
- Decide whether the conclusion is only a cardinality inequality, equality of an extremal function,
  existence of an attaining candidate, or the complete equality-case classification.
- Transcribe the source's transition inequalities using exact rational arithmetic and review the
  equality boundary between indices `r` and `r+1`; do not rely on OCR glyphs.
- Resolve the low-parameter branch `n <= 2*k - t`, where the full uniform layer is
  `t`-intersecting, along with `t = 0`, `k = 0`, `n = 0`, `k > n`, and natural subtraction.
- Freeze foundation, TCB, computation, mutation, freshness, and source-correction policies after
  the proposition is selected.

## Explicit exclusions

- Ordinary Erdos-Ko-Rado (`t = 1`), Hilton-Milner, Kruskal-Katona, Frankl-Wilson, or
  Ray-Chaudhuri-Wilson substituted for the complete intersection root.
- The unrelated Ahlswede-Zhang identity, the complete nontrivial-intersection theorem, weighted or
  biased-measure variants, cross-intersecting families, Hamming schemes, partitions, permutations,
  or infinite families.
- Only the large-`n` `t`-star regime, the `4m` special case, one fixed parameter triple, an
  asymptotic estimate, or a finite computation.
- A definition, structure, or hypothesis that assumes the extremal bound, maximizing candidate,
  optimizer classification, or desired proof.
- The catalog's untrusted `已验证` label, a citation, source theorem name, API `#check`, or adjacent
  mathlib theorem used as proof or completion credit.

No canonical expression, statement fingerprint, checked transport, obligation registry, discovery
protocol, accepted proof state, or completion claim is frozen at intake.
