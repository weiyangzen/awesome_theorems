# Scope map

## Included result family

- The positive resolution of the Kadison-Singer problem obtained by Marcus, Spielman, and
  Srivastava through interlacing families and mixed characteristic polynomials.
- A source-selected endpoint: the pure-state extension question, Weaver's `KS2`, Anderson paving,
  MSS Theorem 1.4, or MSS Corollary 1.5.
- Every implication needed to justify calling that endpoint a positive Kadison-Singer solution, if
  the operator-algebraic endpoint rather than a finite-dimensional MSS theorem is selected.
- Exact complex/real scalar fields, dimensions, norm conventions, constants, probability model,
  and boundary cases appearing in the selected source statement.

## Statement-freeze decisions

The primary paper states several related but non-identical propositions. The statement phase must
choose exactly one canonical root. In particular, MSS Theorem 1.4 is an existence-with-positive-
probability bound for independent finitely supported random vectors in `C^d`; Corollary 1.5 is a
deterministic partition bound; Weaver `KS2` and Anderson paving are consequences; and the original
Kadison-Singer question concerns unique pure-state extension from diagonal operators on `l2`.

The freeze must decide whether the historical reductions to Kadison-Singer are proof obligations or
merely source context. It must also specify binder order and handle `d = 0`, `m = 0`, `r = 0`,
`epsilon = 0`, finite support and independence, matrix/operator norm identification, and the paper's
strict positive-probability conclusion.

## Explicit exclusions

- The MSS bipartite Ramanujan-graph theorem, which is the separate record `THM-M-0886`.
- A theorem only about real-rooted/interlacing polynomials without the selected result's composition.
- The adjacent `THM-M-0338` Kadison-Singer record as a license to duplicate or inherit its scope.
- A finite-dimensional partition theorem silently relabeled as the pure-state extension theorem.
- An abstract package that assumes the desired partition, paving, or extension as structure data.
- The repository label `已验证` as human-source or kernel-proof evidence.

No canonical Lean target is frozen during intake because the repository gloss leaves the endpoint
and equivalence boundary underdetermined.
