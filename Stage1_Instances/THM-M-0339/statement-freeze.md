# Exact statement freeze

## Selected source endpoint

The canonical root for this repository record is Marcus-Spielman-Srivastava Corollary 1.5 in
*Interlacing Families II: Mixed Characteristic Polynomials and the Kadison-Singer Problem*,
arXiv:1306.3969v4, p. 3. This is the paper's exact deterministic finite-dimensional consequence,
not the distinct Ramanujan-graph result and not an unformalized assertion about pure states on
`B(l2)`. The historical implication from this corollary through Weaver KS2 to Kadison-Singer is
source context outside this root. It must be represented by separate obligations if later claimed.

## Frozen mathematical claim

For natural numbers `d`, `m`, and positive `r`, a nonnegative real `delta`, and vectors
`u_i in C^d` indexed by `Fin m`, assume

1. `sum_i u_i u_i* = I`, and
2. `norm(u_i)^2 <= delta` for every `i`.

Then the indices have an `r`-part labeled partition such that, for every part `j`,

`norm (sum_{i in S_j} u_i u_i*) <= (1 / sqrt(r) + sqrt(delta))^2`.

The source says `delta` as a square-rooted real bound; `0 <= delta` is therefore made explicit
rather than relying on an implicit convention. It says `r` is a positive integer, frozen as
`r : Nat` plus `0 < r`. It does not require nonempty parts, so a function `Fin m -> Fin r` is the
exact labeled-partition encoding. `d = 0` and `m = 0` remain allowed; under the identity-sum
hypothesis, these cases have their ordinary mathematical meaning rather than an invented exclusion.

## Lean encoding

The canonical expression is `Stage1.THM_M_0339.MSSPartitionStatement` in `Statement.lean`.
Vectors use `EuclideanSpace C (Fin d)`. The source's rank-one operator `u_i u_i*` uses
`InnerProductSpace.rankOne C (u i) (u i)`, and the matrix spectral norm uses the operator norm on
the resulting continuous linear map. This avoids a matrix/operator transport inside the root.

The sole import is `Mathlib.Analysis.InnerProductSpace.PiL2`. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, it supplies Euclidean space, finite sums, rank-one
continuous linear maps, operator norm, and real square root. No proof, axiom, or placeholder is
present: this phase freezes and elaborates a proposition only.

## Boundary

This statement does not claim MSS Theorem 1.4, the proof of Corollary 1.5, Weaver KS2, Anderson
paving, or the pure-state-extension formulation. Those remain downstream proof/source obligations.
The statement phase proposes no `H0`, `M0`, `R0`, audit completion, or theorem completion.
