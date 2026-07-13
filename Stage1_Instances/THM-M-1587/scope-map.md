# Scope map

## Preserved repository scope

The mathematical catalog fixes only the title `Singleton界`, Richard Singleton, year 1964, and
gloss `MDS码的界`. A computer-science catalog row repeats the title, author, and year with
the gloss `MDS码的Singleton界`. Together these identify the classical coding-theory
Singleton-bound family, not one binder-complete theorem.

The intake preserves that family boundary: an upper bound relating block-code size or linear-code
dimension to block length and minimum Hamming distance, with MDS codes occupying an equality case.
It does not select an unrestricted q-ary inequality, a linear finite-field specialization, an
equality characterization, or an existence or length theorem about MDS codes.

## Proposition-changing decisions

An approved statement run must select all of the following from an immutable reviewed source:

- whether the alphabet is an arbitrary finite type of cardinality `q` or a finite field;
- whether a code is an arbitrary finite set of words or a linear subspace;
- the coordinate carrier and block-length convention, including whether words use `Fin n`;
- the exact definition of minimum distance and its value for empty and singleton codes;
- the admissible ranges for alphabet size `q`, length `n`, distance `d`, and linear dimension `k`;
- whether the conclusion is `|C| <= q^(n-d+1)`, `k <= n-d+1`, `d <= n-k+1`, an equivalent form
  avoiding truncated subtraction, or an equality characterization of MDS;
- whether logarithms, floors, ceilings, cardinal powers, or divisibility assumptions occur;
- the puncturing/deletion map and the exact hypothesis making it injective;
- whether code nonemptiness, positive distance, field finiteness, or coordinate-count inequalities
  are hypotheses rather than consequences; and
- ordered binders, coercions, strictness, and every zero-length, empty-alphabet, empty-code,
  singleton-code, zero-distance, and overlarge-distance boundary.

These choices change the proposition. They form a resolution ledger, not an asserted statement.

## Candidate families not credited

- The unrestricted q-ary bound for a code `C` in length-`n` words with minimum distance `d`,
  commonly expressed as `|C| <= q^(n-d+1)` under source-specific range conventions.
- The linear finite-field specialization for an `[n,k,d]_q` code, commonly expressed as
  `k <= n-d+1` or `d <= n-k+1`.
- The definition or characterization of a maximum distance separable code as a linear code meeting
  the Singleton inequality with equality.
- A nonlinear equality case, an MDS existence theorem, classification of trivial MDS codes, or the
  MDS length conjecture.
- Binary specializations and reformulations using logarithms, puncturing cardinalities, natural
  subtraction, or integer rounding.

No family above is selected, conjoined, asserted, or credited at intake. In particular, `MDS` in
the received gloss does not authorize turning an upper bound for all codes into only the equality
case, an existence theorem, or the MDS conjecture.

## Neighbor and duplicate boundaries

- `THM-M-1585` separately owns the broad coding-theory topic.
- `THM-M-1586` owns the Hamming sphere-packing bound; it is a different upper bound.
- `THM-M-1588` owns the Gilbert-Varshamov existence lower bound, and `THM-M-1589` owns linear codes
  as a topic. Their definitions or future evidence cannot be inherited by name.
- `THM-M-1592` owns Reed-Solomon codes, which furnish MDS examples but do not replace the bound.
- Stage0 record `THM-C-0371` repeats the Singleton topic in a computer-science projection. The
  rev-5.6 target set is mathematics-only and does not contain this record; it was not one of the 55
  screened-out mathematics records. Its likely duplicate identity requires integration review,
  but it grants no target, statement, or proof credit here.
- Plotkin, Johnson, Elias, Hamming, Gilbert-Varshamov, generalized Singleton, rank-metric, quantum,
  locally recoverable, and network-coding bounds are excluded unless a checked source transport
  relates one to the selected root.

The intake also excludes defining a code structure whose fields assume the desired inequality,
assuming injectivity of a puncturing map without deriving it from distance, checking only finite
examples, or treating the catalog's untrusted `已验证` label as evidence.

## Boundary cases

The statement phase must decide `q = 0` and `q = 1`; `n = 0`; `d = 0` and `d = 1`; `d > n` and
`d = n + 1`; `k = 0` and `k > n`; empty and singleton arbitrary codes; zero and full-dimensional
linear codes; the zero ring versus a nontrivial finite field; puncturing zero or all coordinates;
natural-number subtraction at zero; the value of `0^0`; logarithm bases; and whether the MDS
equality definition includes trivial codes.

## Formal boundary

No canonical Lean expression is frozen. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, `Mathlib.InformationTheory.Hamming` supplies
`hammingDist`, equality and coordinatewise-map facts, and an upper bound by coordinate count.
Core finite libraries supply function-space cardinality and injective-cardinality inequalities.
The intake probe authenticates that substrate only. A bounded repo-local and pinned-mathlib search
found no fixed-length block-code/minimum-distance/Singleton/MDS API or terminal code-bound theorem.
Mathlib's variable-length uniquely-decodable-code machinery is a different model and grants no
target credit. This is not an exhaustive anchor audit or an absence theorem.
