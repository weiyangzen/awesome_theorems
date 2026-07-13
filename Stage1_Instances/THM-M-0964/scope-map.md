# Scope map

## Preserved theorem family

The target remains the classical finite-set Hilton-Milner theorem: an extremal result for a uniform
pairwise-intersecting family whose members do not all contain one common point. The catalog's phrase
"maximum size" is compatible with, but does not choose among, these claims:

1. **Bound only.** For a nontrivial intersecting family `F` of `k`-subsets of an `n`-element set,
   bound `|F|` by
   `choose (n - 1) (k - 1) - choose (n - k - 1) (k - 1) + 1`.
2. **Sharp maximum.** Add the Hilton-Milner construction: one `k`-set `C` plus every `k`-set that
   contains a fixed point outside `C` and intersects `C`.
3. **Extremizer classification.** Classify equality up to a permutation of the ground set, with a
   second extremal type when `k = 3`.
4. **Original-paper theorem package.** Select the exact numbered theorem, definitions, endpoints,
   subsidiary clauses, and proof boundary from the complete 1967 article rather than a modern
   eponymous restatement.

Intake records the common bound as a candidate only. Statement work must select one claim after
primary-source and independent review.

## Candidate parameter and encoding map

| Component | Candidate shape | Decision still required |
|---|---|---|
| ground set | `Fin n` | abstract finite type versus canonical `[n]` model and checked transport |
| member | `Finset (Fin n)` | subset convention and coercions |
| family | `Finset (Finset (Fin n))` | duplicate-free family versus indexed/source family |
| uniformity | `Set.Sized k` | exact binder order and positivity implications |
| intersecting | `Set.Intersecting` | all-pair non-disjointness versus distinct-pair convention |
| nontriviality | empty total intersection via `Set.sInter` | empty family convention and equivalence with "not contained in a star" |
| range | candidate `2 <= k` and `2 * k < n` | primary endpoints, especially `k <= n / 2` and `n = 2k` |
| bound | natural-number binomial difference plus one | subtraction grouping and source convention |
| equality | absent from probe | whether maximum attainment and one or two isomorphism types belong to root |

## Statement-freeze decisions

The statement phase must resolve all of the following before assigning an expression fingerprint:

- exact primary edition, theorem locator, incorporated definitions, corrections, and errata;
- upper bound alone versus existential attainment versus full equality classification;
- `2 <= k`, `k <= n / 2`, `k < n / 2`, or an equivalent integer range;
- whether the `n = 2k` boundary is in scope and what "nontrivial maximum" means there;
- whether the exceptional `k = 3` equality family is root-critical;
- family-as-set, family-as-finset, or indexed family semantics and duplicate handling;
- empty-total-intersection versus not-contained-in-a-full-star, with a checked equivalence on the
  selected domain;
- ordinary pairwise intersection versus distinct-pair intersection;
- `Fin n` versus an arbitrary finite ground type and all transports;
- exact `Nat.choose` and truncated subtraction expression, including parenthesization;
- whether isomorphism means a ground-set permutation and how it is encoded in Lean.

## Degenerate and boundary cases

These cases are open, not silently excluded:

- `k = 0`, `k = 1`, `k = 2`, and the exceptional equality structure at `k = 3`;
- `n = 0`, `n < 2k`, `n = 2k`, and the first strict-range values;
- empty and singleton families;
- a family containing the empty set;
- a family whose total intersection is empty only vacuously under an empty-family convention;
- families with a common point but not the full star;
- equality versus strict inequality and multiple extremizers;
- natural subtraction under out-of-range parameters.

## Excluded substitutions

None of the following may close this target:

- `THM-M-0822` Erdős-Ko-Rado, which permits trivial stars and has a larger bound;
- `THM-M-0962` Frankl-Wilson or `THM-M-0963` Ray-Chaudhuri-Wilson modular/L-intersection bounds;
- `THM-M-0965` Ahlswede-Khachatrian complete `t`-intersection or `THM-M-0966`
  Kruskal-Katona shadow bounds;
- a Hilton-Milner analogue for multisets, permutations, partitions, graphs, vector spaces,
  projective spaces, exterior algebras, cross-intersection, or degree bounds;
- a numerical instance, asymptotic weakening, assumed extremal construction, or empirical search;
- `Finset.erdos_ko_rado`, generic set-family APIs, or the local proposition definition presented as
  a Hilton-Milner proof;
- the theorem name, catalog `已验证` label, citation, DOI, secondary prose, or URL presented as H0 or
  kernel evidence.

## Neighbor boundaries

- `THM-M-0822` is the ordinary intersecting-family maximum. Hilton-Milner adds the proposition-
  changing nontriviality restriction and a second-best bound.
- `THM-M-0963` constrains the set of possible pairwise intersection sizes rather than the common
  intersection of the entire family.
- `THM-M-0965` is a complete `t`-intersection theorem with a different parameter family and
  extremal classification.
- `THM-M-0966` may supply shadow machinery but is not the requested conclusion.

## Stable identity boundary

Pre-dedup Stage0 history used `THM-M-0964` for Vosper and `THM-M-0992` for Hilton-Milner. Current
rev-5.6 authority uses `THM-M-0964` for Hilton-Milner. All evidence must bind ID plus theorem name,
Hilton/Milner attribution, 1967 date, and the nontrivial-intersecting-family gloss.
