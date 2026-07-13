# Source-statement crosswalk

## Repository record and duplicate provenance

`Docs/researches/math_theorems.md:7148-7153` supplies exactly the title `Bernstein inequality`,
Sergei Bernstein, 1924, the gloss "tail probability of a sum," high importance, and claimed status
`verified`. All six uncited lines originate at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. There is no work, edition, theorem/page, formula,
definition, hypothesis, proof boundary, correction history, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:26686-26711` assigns `THM-M-0979` while leaving the formal system,
foundation, exact definitions and assumptions, proof route, dependencies, equivalent forms,
axioms, machine state, and artifact links open. Its generated statement that a closed result is
known is not source evidence. Rev-5.6 therefore resets the row to `L0 / rework_required` and treats
`verified` as untrusted.

The source corpus separately contains `Bernstein inequality` at lines 7273-7278. Apart from the
translated title spelling, that block has the same proposer, year, gloss, importance, and status;
Stage0 retains it as `THM-M-0995`. The generator's exact metadata signature includes the name, so
the two spellings were not deduplicated. This explains the duplicate-looking provenance but does
not authorize a worker to collapse targets or transfer evidence.

## Inspected modern source lead

Roman Vershynin, *High-Dimensional Probability: An Introduction with Applications in Data
Science*, second edition, author-hosted PDF observed 2026-07-13, was inspected as a modern source
lead. The 341-page PDF had 5,634,501 bytes and observed SHA-256
`a5665ecf5fc833968a6493c6e3a4f6ae2137700ddbaed2fd457b5e1148bc0aac`.

- Section 2.9, printed pages 47-48, states and proves Theorem 2.9.1 for independent mean-zero
  subexponential summands, then gives weighted Corollary 2.9.2.
- Theorem 2.9.5 on printed page 49 states a variance-sensitive inequality for independent
  mean-zero summands bounded by `K`, displaying a leading factor `2` and denominator
  `sigma^2 + K*t/3`; its proof is assigned to Exercise 2.47 rather than supplied at that point.
- The notes on printed pages 49-50 say several forms appeared in Bernstein's original work and
  cite a 1924 article, a 1927 book, and a 1937 paper. Bibliography entry 38 identifies the 1924
  title as *On a modification of Chebyshev's inequality and of the error formula of Laplace* and
  records a 1933 reprint.

The PDF is a temporary discovery input, not vendored immutable evidence or an accepted source
edition. It is also not the catalog's cited source, because the catalog cites none. The historical
1924 work, reprint, translations, corrections, and errata were not inspected. This source supports
an `H1` family lead, not H0 or selection of any one candidate root.

## Clause crosswalk

| Repository component | Candidate source detail | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| Bernstein inequality | one exact member of a family of concentration inequalities | one source-faithful `Prop` with ordered binders | root not selected |
| sum | finite scalar sum, weighted sum, martingale sum, or another aggregation | `Finset` sum or source-selected encoding | absent from catalog |
| random variables | real or other codomain; common space; measurability and moment model | functions on a measured type plus exact predicates | absent from catalog |
| assumptions | independence/dependence, centering, boundedness, variance or Orlicz conditions | explicit fields or binders, never hidden in prose | absent from catalog |
| tail probability | upper, lower, or two-sided event; strictness and threshold range | measured event and `Measure.real` or checked equivalent | absent from catalog |
| constants | prefactor, exponent constant, variance term, linear term, common bound | exact real expression with boundary policy | conflicting candidate conventions |
| Sergei Bernstein, 1924 | pinpoint work, edition/reprint, exact passage, genealogy and translation | source provenance only | historical lead not inspected |
| `verified` | claimed formal state | accepted kernel declaration and receipt would be required | explicitly rejected |

## Cross-target and Lean discovery boundary

The separate `THM-M-0995` dossier selects a bounded independent centered upper-tail candidate with
prefactor `1`; its own intake crosswalk says the primary edition, pinpoint, and constants genealogy
remain open. Its `Statement.lean` elaborates that candidate, while the legacy
`S1_M_275.lean` file explicitly says no terminal Bernstein proof is claimed. Those immutable
repository artifacts are discovery evidence for possible encoding and duplicate review only. They
are neither source authority nor proof credit for `THM-M-0979`.

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the probe checks MGF,
CGF, Chernoff, sub-Gaussian-sum, independence, and variance APIs. A bounded exact-topic search found
no separately named terminal scalar Bernstein tail theorem. This is intake discovery, not an
exhaustive external anchor audit or global absence claim.

## Source gate

Before statement work can freeze a root, accountable reviewers must decide the relationship to
`THM-M-0995`, admit a lawful immutable source edition, select one exact source proposition, map
every definition, binder, premise, constant, conclusion, and boundary case, audit its genealogy,
translations, corrections, and errata, and independently approve the mapping. Only then may a
statement run freeze minimal imports, an elaborated expression and environment fingerprint,
checked alternate encodings, and the required statement mutations.
