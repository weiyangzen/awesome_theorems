# Scope map

## Preserved theorem family

The title, author, year, and catalog gloss identify Elekes's 1997 finite real sum-product lower
bound: a finite set of nonzero real numbers cannot have both its pairwise sumset and pairwise
product set too small. This family boundary does not itself accept one canonical proposition.

## Candidate source proposition

Elekes, *Acta Arithmetica* 81.4 (1997), Theorem 1 on printed page 365, states that there is a
positive absolute constant `c` such that, for every `n`-element set `A`,

```text
c * n^(5/4) <= max(|A + A|, |A * A|).
```

The paper's opening convention makes `A` a finite subset of the nonzero reals, sets `n = |A|`, and
defines `A + A` and `A * A` using all ordered pairs from `A`. This is the candidate mathematical
root, not an accepted canonical claim.

## Decisions required at statement freeze

1. Admit and independently review an immutable edition of the paper, its incorporated definitions,
   theorem locator, proof boundary, correction history, and any errata.
2. Fix the finite-set encoding: a mathematical finite subset as `Finset Real`, or a finite `Set`
   with a checked cardinality transport. Duplicates must not enter through a list or multiset.
3. Preserve the ambient domain `Real` and the source's nonzero-element condition. A theorem over
   positive reals, integers, rationals, a field, or an abstract ring is not automatically identical.
4. Fix `A + A` and `A * A` as pairwise image sets, not sums or products of the elements. Confirm the
   pointwise `Finset` encoding and the equality with explicit `Finset.image2` forms by checked
   transports if both receive credit.
5. Fix the ordered quantifiers: one absolute `c > 0` works uniformly for every finite nonzero-real
   set, rather than allowing a constant depending on `A` or `n`.
6. Fix the exact real-valued interpretation of `n^(5/4)`, all natural-to-real cardinality casts,
   and the non-strict inequality direction.
7. Decide whether the source convention includes the empty set. The displayed theorem permits the
   vacuous `n = 0` reading, while the proof enumerates `a_1, ..., a_n` and invokes incidence
   parameters described as positive integers. Any restriction to nonempty sets needs a source or a
   checked boundary derivation, not silent insertion.
8. Check singleton sets, sets containing zero, negative elements, repeated sums/products, and the
   use of ordered versus unordered pairs. Nonzero is material to distinctness of the proof's lines.

## Proof-family boundary

The paper's proof on page 366 constructs `n^2` affine functions
`f_(j,k)(x) = a_j * (x - a_k)`. Each graph contains at least `n` points of
`P = (A + A) x (A * A)`. Applying its Proposition 1, a Szemeredi-Trotter incidence estimate, yields
`|A + A| * |A * A| >= C^(-1/2) n^(5/2)`, from which the maximum bound follows. These named steps are
source-crosswalk inputs only. No obligation registry, leaf ledger, composition certificate, or Lean
proof is frozen during intake.

## Explicit exclusions

- The Erdős-Szemeredi conjectural `n^(2-o(1))` bound, or any later Solymosi improvement.
- A finite-field, integer-only, rational-only, positive-real, or abstract-ring theorem substituted
  for the source's finite nonzero-real theorem without a checked relationship.
- The weak generic cardinality facts `|A| <= |A+A|` or `|A| <= |A*A|` as the `5/4` result.
- A statement that assumes an incidence bound crafted to contain the desired conclusion without
  exposing the Szemeredi-Trotter bridge and its hypotheses as later obligations.
- A constant chosen after `A`, a fixed-size computation, or an asymptotic statement with
  unspecified quantifier conversion presented as the exact uniform theorem.
- `THM-M-0385` (Bourgain sum-product), `THM-M-0953` (Solymosi), the catalog's untrusted verified
  label, or the intake probe used as source-statement or proof credit.

