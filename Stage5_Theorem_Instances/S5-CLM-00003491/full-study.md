# Full study

## Statement identity

Frozen declaration: `Arxiv.«1609.08688».maximalLength_ge_of_isSquare` at revision `2270d31e8dd611521f979de6d86da364930b7669`. The target proposition is its delta expansion: `F n` becomes the natural supremum of lengths; `IsIncreasing₂` becomes list pairwise; and `lt₂` becomes existence of two distinct increasing coordinates. No hypothesis is removed.

## Construction

Let `q = n.sqrt`. For every `a,b,c < q`, use

`(a*q+b+1, a*q+c+1, b*q+c+1)`.

There are exactly `q^3` entries. If the first differing index is `a`, coordinates zero and one increase; if it is `b`, zero and two increase; if it is `c`, one and two increase. The elementary block inequality `x*q+y+1 < x'*q+y'+1` for `y<q` and `x<x'` supplies the strict comparisons. Each coordinate lies between one and `q^2=n`.

## Supremum boundary

The definition uses `sSup` on naturals, so boundedness is proved explicitly. For `n≥2`, a list longer than `n^2` repeats its first two coordinate values, contradicting pairwise two-coordinate increase in either index order. For `n=0`, no triple is admissible; for `n=1`, all triples are constant and a pairwise list has length below two. Therefore the candidate-length set is bounded, and `le_csSup` yields the theorem.

## Trust and downstream use

The provider's `sorryAx` proves nothing here. All proof steps reside in the claim-owned Lean files. Proof and Audit are self-contained for direct provider-native elaboration, and Audit reconstructs its root rather than importing or invoking another claim-owned theorem. Stage6 aliases `S6-CLM-00008151` and `S6-VAR-00007039` consume the accepted theorem only after canonical Master recomputation and trust-zero compilation.
