# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6910-6915` contains the complete originating record: the title
`Green-Tao-Ziegler定理`, attribution `Green/Tao/Ziegler`, year 2006, gloss
`线性方程组在素数中的解`, importance `高`, and status `已验证`. All six lines originate at
repository commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The Stage0 projection repeats the
gloss but explicitly leaves precise definitions, premises, proof path, axioms, and formal artifacts
open. Repository provenance does not establish a source-faithful proposition.

## Primary source family, not credited as H0

Ben Green and Terence Tao, *Linear Equations in Primes*, arXiv `math/0606088` (submitted
2006-06-04; v2 dated 2008-04-22), later Annals of Mathematics 171 (2010), 1753-1850, DOI
`10.4007/annals.2010.171.1753`, is the strongest title/year/gloss match. The inspected arXiv v2
PDF has 84 pages, 960744 bytes, and SHA-256
`4cc772cfa6f2f9fa2af82d07b6323669c8150ac1911e83a245cc667f956500f5`.

Its Main Theorem states the generalized Hardy-Littlewood conjecture for affine-linear systems of
complexity at most `s`, conditional on `GI(s)` and `MN(s)`. Corollary 1.7 gives an unconditional
complexity-at-most-two case. Theorem 1.8 gives a von-Mangoldt-weighted consequence for integer
matrices and solutions of `Ax = b`; an unweighted prime-count analogue is mentioned but left to the
reader. Corollary 1.9 gives a qualitative existence result under local solvability. These are
distinct propositions. The paper has only Green and Tao as authors, so it does not by itself
explain the catalog's three-author name.

Ben Green, Terence Tao, and Tamar Ziegler, *An Inverse Theorem for the Gowers
`U^{s+1}[N]`-Norm*, arXiv `1009.3998`, proves the remaining inverse-Gowers input. The inspected
current v5 PDF is dated 2026-04-23, has 116 pages, 983529 bytes, and SHA-256
`24b5b74b1c4f31986bfc75955f8528e81753efc0c45bd99bc23fee58171a4711`. Its Theorem 1.3
proves `GI(s)` for `s >= 3` and the introduction identifies the finite-complexity prime application.
This is a later dependency/result package, not a 2006 three-author paper whose statement is fixed by
the catalog. Its revision history and corrections must be audited before source acceptance.

Pierre-Yves Bienvenu, *A Higher-Dimensional Siegel-Walfisz Theorem*, arXiv `1607.06625v1`,
later Acta Arithmetica 179 (2017), 79-100, DOI `10.4064/aa8600-10-2016`, is a useful secondary
discriminator: its introduction calls the unconditional bounded affine-form asymptotic the
Green-Tao-Ziegler theorem and explains that Green and Tao's theorem relied on conjectures later
resolved by Green-Tao and Green-Tao-Ziegler. The inspected 20-page PDF has 280361 bytes and
SHA-256 `440ab085d68922005e9a4824ce32eae5a8d27e293e6fc8dd8105304593effdee`.
This clarifies the compound name, but a later secondary restatement cannot choose the catalog root
or supply H0 evidence.

All three PDFs were temporary remote observations and were not added to the repository. They identify a
credible proved source family and pinpoint the ambiguity, supporting provisional `H1`. The catalog
still does not select one root, source revision, incorporated-definition chain, correction policy,
or proof boundary, and no independent source review is admitted. Therefore neither source lead is
H0 evidence.

## Phrase-to-statement crosswalk

| Repository/source phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| `Green-Tao-Ziegler定理` | later three-author inverse theorem plus prime-pattern consequence | exact composition and source revisions | family lead only |
| `2006` | Green-Tao preprint date | edition and authorship decision | conflicts with three-author label |
| `线性方程组` | matrix equations or systems of affine-linear forms | domains, dimensions, rank/complexity, coefficient bounds | encoding open |
| `在素数中的解` | weighted asymptotic, prime-point count, or qualitative existence | prime predicate/weight, range, multiplicity, exact conclusion | result open |
| finite complexity | exclusion of affinely dependent binary systems | exact complexity predicate and hypotheses | definition mapping open |
| `GI(s)` and `MN(s)` | conditional premises in the 2006 theorem, later proved inputs | root hypotheses or dependency nodes | conditionality open |
| local/global factors | singular product and archimedean density | exact finite products/limits/measures and convergence | normalization open |
| `已验证` | untrusted inventory label | no source or proof credit | explicitly rejected |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the probe checks
`Nat.Prime`, `Nat.primeCounting`, the arithmetic-function von Mangoldt definition and basic
identities, and generic `AffineMap`/`LinearMap` types. Mathlib also contains results toward primes in
arithmetic progressions, but no source-identical finite-complexity system theorem was located.

A bounded name/content search of repository-local Lean and pinned mathlib found no declaration
named for Green, Tao, Ziegler, linear equations in primes, the relevant generalized Hardy-
Littlewood result, or the needed inverse-Gowers/nilsequence package. This is a scoped intake search,
not an exhaustive external anchor audit or an absence proof. The adjacent APIs neither identify the
catalog root nor supply a proof body.
