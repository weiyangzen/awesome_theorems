# THM-M-1493 source-statement crosswalk

## Repository source and provenance

The complete upstream record is `Docs/researches/math_theorems.md:10910-10915`:

| Field | Literal value | Intake meaning |
|---|---|---|
| title | `单纯形法` | names the simplex-method family |
| proposer | `George Dantzig` | historical attribution only |
| time | `1947` | source-family locator only |
| statement | `线性规划的算法` | topic/purpose gloss, not a proposition |
| importance | `高` | scheduling metadata only |
| formalization status | `已验证` | explicitly untrusted; no H/M credit |

All six lines originate in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. They contain no bibliography, edition, page,
theorem, formula, definitions, binders, assumptions, conclusion, proof, correction record, or
formal artifact. `Docs/Stage0_Blueprint.md:40594-40619` repeats the gloss while expressly leaving
the exact definitions and premises, proof route, dependencies, equivalent forms, axioms, machine
status, and artifact links open.

## Historical primary-source lead, not H0

George B. Dantzig, "Maximization of a Linear Function of Variables Subject to Linear
Inequalities," Chapter XXI, pages 339-347 in Tjalling C. Koopmans (ed.), *Activity Analysis of
Production and Allocation*, Cowles Commission Monograph 13, John Wiley & Sons, 1951.

The Cowles Foundation's author-hosted scan and contents page were inspected on 2026-07-13. The
chapter's footnote says the work stemmed from discussions in spring 1947 and that the general
simplex approach was stimulated in fall 1947. It fixes a nonnegative equality-form maximization
problem and then presents multiple distinct results:

- page 340 imposes a nondegeneracy assumption for the development;
- page 341 gives Theorems A and B about basic feasible and maximum feasible solutions;
- pages 341-343 give Theorem 1 and a finite basis-improvement process, with bounded-optimum and
  unbounded branches;
- page 344 gives Theorem 2, a sufficient optimality criterion;
- pages 345-347 give Theorem 3 and a feasibility-construction process; and
- page 347 explains the geometric origin of the term "simplex".

This is a strong historical source-family lead, but the catalog does not cite it or select a result.
The 1951 publication date also differs from the 1947 invention date in the metadata. The scan was
inspected transiently and not vendored. No edition/correction audit, exact proposition and proof
boundary, premise-by-premise mapping, or independent review is accepted, so this lead is not `H0`.

## Source-to-statement crosswalk

| Catalog/source element | Mathematical information actually fixed | Lean information required | Result |
|---|---|---|---|
| `单纯形法` | simplex-method family | exact state, transition, invariant, and result | family only; open |
| `线性规划` | finite-dimensional linear optimization topic | coefficient domain, dimensions, representation, feasibility and boundedness premises | all open |
| `算法` | some procedure is intended | initialization, pivot rule, termination/output relation, computation boundary | all open |
| George Dantzig / 1947 | historical origin | admitted immutable source and exact theorem/page mapping | lead only |
| Cowles Chapter XXI | several closely related algorithms and theorems | selection of exactly one root and incorporated assumptions | unselected source family |
| `已验证` | metadata screening claim | accepted source review or kernel receipt | no credit |

The literal gloss has no connective or conclusion whose truth Lean can check. Consequently no
ordered binder, hypothesis, conclusion, canonical expression, alternate encoding, or expression
hash can be populated truthfully at intake.

## Non-equivalent candidate statements

| Candidate | Material choices missing from the catalog | Intake decision |
|---|---|---|
| Dantzig Theorem 1 / basis improvement | equality-form data, nondegeneracy, starting feasible basis, pivot choice, finite versus unbounded branch | not selected |
| Dantzig Theorem 2 / optimality | basis representation and reduced-cost inequalities | not selected |
| Dantzig Theorem 3 / infeasibility condition | reference basis and coefficient representation | not selected |
| modern Bland termination theorem | exact tableau semantics, Bland order, invariant and termination measure | not selected |
| end-to-end solver correctness | phase I/II implementation, result type, certificates and failure semantics | not selected |
| complexity theorem | input encoding, arithmetic model, pivot rule and bound | not selected |

These claims are not interchangeable. In particular, an optimality criterion does not prove
termination, and termination of one anti-cycling rule does not prove correctness of every simplex
implementation.

## Pinned Lean substrate boundary

The pinned mathlib revision contains:

| Module/declarations | Actual role | Credit boundary |
|---|---|---|
| `...SimplexAlgorithm.Datatypes`: `DenseMatrix`, `SparseMatrix`, `Tableau` | rational meta-level data structures | definitions only |
| `...SimplexAlgorithm.SimplexAlgorithm`: `doPivotOperation`, `checkSuccess`, `choosePivots`, `runSimplexAlgorithm` | pivot loop using a documented Bland rule | implementation interface; no inspected general correctness theorem |
| `...SimplexAlgorithm.PositiveVector`: `stateLP`, `extractSolution`, `findPositiveVector` | reduces linarith certificate search to a bounded LP-like problem | special oracle problem, not arbitrary LP optimization |
| `...Oracle.SimplexAlgorithm`: `CertificateOracle.simplexAlgorithmSparse/Dense` | produces a candidate certificate for `linarith` | meta oracle; downstream proof-term checking does not identify this catalog theorem |

`IntakeProbe.lean` authenticates these pinned interfaces. A bounded exact-topic search found this
oracle family and no repo-local `THM-M-1493` target. This is intake discovery, not an exhaustive
external anchor audit, proof of absence, or proof credit.

## Source exit gate

Before statement execution, independent source and optimization reviewers must approve a lawful
immutable edition, exact theorem and proof boundary, incorporated definitions and corrections, and
a row-by-row mapping to one canonical mathematical claim. A Lean reviewer must then freeze its
minimal imports, exact expression and environment fingerprints, checked transports, and required
mutations. Until those gates pass, the truthful classification is `[H5, M4, R4]`, and all proof,
audit-completion, and theorem-completion claims remain open.
