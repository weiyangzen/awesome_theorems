# Scope map

## Preserved repository scope

The mathematical catalog fixes only the title `Gilbert-Varshamov界`, attribution
`Gilbert/Varshamov`, year 1952, and gloss `码的存在性下界`. A second computer-science catalog row
uses the same title and gloss but dates the family 1952-57. Together they identify a coding-theory
existence-lower-bound family, not one binder-complete theorem.

The intake preserves that narrow family boundary: existence of a sufficiently large block code
with a prescribed minimum Hamming distance. It does not yet choose binary versus q-ary, nonlinear
versus linear, finite versus asymptotic, or an exact inequality.

## Proposition-changing decisions

An approved statement run must select all of the following from an immutable reviewed source:

- the alphabet: binary, an arbitrary finite alphabet of cardinality `q`, or a finite field;
- whether a code is an arbitrary subset of words, a linear subspace, or an equivalence class;
- the exact word type, block length `n` or `D`, distance parameter `d` or correction radius `k`,
  and the definition of minimum distance for empty and singleton codes;
- the admissible ranges for alphabet size, length, distance, dimension, relative distance, and rate;
- whether the conclusion concerns an explicit code, the maximum size `A_q(n,d)`, a linear
  dimension, or an asymptotic rate function;
- the Hamming-ball volume convention, especially whether the summation ends at `d - 1`, `2k`, or
  another source-specific radius and how truncated natural subtraction is avoided;
- strict versus non-strict inequalities, floors or ceilings, divisibility, logarithm base, entropy
  normalization, limits or limsups, and endpoint conventions;
- classical finite-choice or maximality use versus a constructive selection procedure; and
- the ordered binders, exact conclusion, and every zero-length, empty-alphabet, zero-distance,
  overlarge-distance, and singleton boundary case.

These choices change the proposition. They form a resolution ledger, not an asserted statement.

## Candidate families not credited

- Gilbert's finite binary theorem: a maximal set of length-`D` binary words with pairwise distance
  at least `2k + 1` yields a lower bound involving the binary Hamming-ball volume through `2k`.
- A modern finite q-ary nonlinear formulation such as a lower bound for `A_q(n,d)` by total word
  count divided by a radius-`d - 1` Hamming-ball volume.
- A Varshamov linear q-ary theorem obtained by selecting parity-check columns and deriving a
  source-specific dimension or cardinality bound.
- An asymptotic corollary expressed with q-ary entropy, relative distance, and code rate.
- Binary specializations or rounded integer forms of any of these statements.

No family above is selected, conjoined, asserted, or credited at intake. In particular, the name
"Gilbert-Varshamov" does not authorize replacing the historical finite binary theorem with the
more convenient modern q-ary or asymptotic form.

## Neighbor and duplicate boundaries

- `THM-M-1585` separately owns the broad coding-theory topic.
- `THM-M-1586` owns the Hamming sphere-packing upper bound, which appears alongside Gilbert's lower
  bound but is not this target.
- `THM-M-1587` owns the Singleton bound, and `THM-M-1589` owns linear codes as a topic. Their future
  definitions and proof evidence cannot be imported by name.
- Stage0 record `THM-C-0372` repeats the Gilbert-Varshamov title and gloss in a computer-science
  projection, with the date 1952-57. It is outside the 1546-target rev-5.6 manifest. Its likely
  duplicate identity requires integration review, but it grants no target, statement, or proof
  credit here.
- Hamming, Plotkin, Johnson, Elias, MRRW, algebraic-geometric, quantum, list-decoding, rank-metric,
  and constrained-system bounds are excluded unless an accepted source explicitly relates an
  encoding to the selected root.

The intake also excludes defining a structure whose field assumes the desired lower bound,
postulating a code of the requested size, checking only small numeric instances, or treating the
catalog's untrusted `已验证` label as evidence.

## Boundary cases

The statement phase must decide `q = 0` and `q = 1`; `n = 0`; `d = 0` and `d = 1`; `d > n`;
`k = 0`; `2k >= D`; zero- and full-dimensional linear codes; empty and singleton codes; empty
finite sums and products; natural-number subtraction at zero; division and rounding when a ball
volume does not divide the ambient word count; entropy endpoints; and whether the asymptotic
relative distance is below `1 - 1/q` or another exact source range.

## Formal boundary

No canonical Lean expression is frozen. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, `Mathlib.InformationTheory.Hamming` supplies
`hammingDist`, its metric wrapper `Hamming`, triangle and cardinality bounds, while core libraries
supply finite function cardinality and binomial coefficients. The intake probe authenticates that
substrate only. A bounded repo-local and pinned-mathlib search found no exact Gilbert/Varshamov
occurrence and no code-size or minimum-distance API suitable as a root theorem. This is not an
exhaustive anchor audit or an absence theorem.
