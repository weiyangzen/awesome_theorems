# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` names `Marcus-Spielman-Srivastava定理`, attributes it (incompletely)
to Adam Spielman and Nikhil Srivastava, dates it to 2013, and gives only `卡迪生-辛格问题的正解`
("a positive solution of the Kadison-Singer problem"). Stage0 repeats that wording. The rev-5.6
manifest preserves `已验证` solely as `source_status_untrusted`; it supplies no formula, hypotheses,
theorem number, page, proof boundary, or formal artifact.

The repository also contains a second record with the same displayed theorem name, `THM-M-0886`,
whose gloss is existence of bipartite Ramanujan graphs. That is a different MSS result and is not a
permitted interpretation of this target.

## Inspected primary source

Adam W. Marcus, Daniel A. Spielman, and Nikhil Srivastava, *Interlacing Families II: Mixed
Characteristic Polynomials and the Kadison-Singer Problem*, arXiv:1306.3969v4 (14 April 2014),
published in *Annals of Mathematics* 182 (2015), 327-350. The intake inspected the immutable arXiv
v4 PDF. Its abstract says that the paper proves Weaver's `KS2` and an Anderson paving formulation,
both connected to a positive Kadison-Singer solution. Pages 1-3 contain Question 1.1, Conjectures
1.2 and 1.3, Theorem 1.4, and Corollary 1.5.

This inspection establishes a primary source and the ambiguity boundary, not `H0`: an exact root,
all reductions, page-level proof-node crosswalk, errata check, and independent review remain open.

## Crosswalk

| Source location | Mathematical statement | Candidate Lean surface | Intake status |
|---|---|---|---|
| Question 1.1, p. 2 | every pure state on diagonal `D` in `B(l2)` has a unique pure-state extension | operator algebras, states, purity, extension | candidate endpoint; substantial API audit open |
| Conjecture 1.2 (`KS2`), p. 2 | universal constants partition a tight complex frame into two norm-controlled parts | finite complex inner-product spaces and finite sums | candidate endpoint; constants and norm encoding open |
| Conjecture 1.3, p. 2 | zero-diagonal self-adjoint matrices admit uniformly norm-small diagonal pavings | Hermitian matrices, diagonal projections, operator norm | candidate endpoint |
| Theorem 1.4, p. 3 | independent finitely supported random vectors with isotropic expectation and bounded expected squared norm have a positive-probability spectral bound | finite probability, expectation, rank-one operators, operator norm | primary machine-facing candidate |
| Corollary 1.5, p. 3 | a tight finite frame with squared norms bounded by `delta` admits an `r`-partition with explicit bound | `Finset`, partitions, inner products, Hermitian operators | primary machine-facing candidate |
| text after Cor. 1.5 | `r = 2`, `delta = 1/18` implies `KS2` with `eta = 18`, `theta = 2` | checked specialization and rescaling | implication obligation if included |
| introduction, pp. 2-3 | projection paving/Anderson paving reductions yield Kadison-Singer | operator-algebraic bridge theorems | source boundary; cannot be assumed silently |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, `IntakeProbe.lean`
checks basic APIs for inner products, Hermitian matrices, matrix-vector multiplication, finite sums,
finite cardinality, and pairwise predicates. A bounded repository and pinned-mathlib name search for
`Kadison`, `Weaver`, `MixedCharacteristicPolynomial`, `Interlacing`, and `paving` found no target-
named declaration. This is intake discovery only, not the later immutable anchor audit and not proof
that no differently named formalization exists.
