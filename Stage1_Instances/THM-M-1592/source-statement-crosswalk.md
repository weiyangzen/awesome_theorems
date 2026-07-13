# Source-statement crosswalk

## Repository record

| Catalog component | Repository evidence | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| Target identity | `Docs/researches/math_theorems.md`: `Reed-Solomon码` | Future canonical namespace and declaration | Stable UID and subject only |
| Attribution and date | Reed/Solomon, 1960 | Provenance metadata | Consistent with the primary bibliographic lead, but not a theorem locator |
| Literal claim | `MDS码` | No expression | A noun phrase naming a property/family, not a proposition |
| Source status | `已验证` | No receipt | Explicitly untrusted metadata; no H or M credit |
| Exact premises and result | Marked `待补充` in Stage0 | Ordered binders, hypotheses, conclusion | Absent; canonical statement remains null |
| Proof and formal artifact | Marked `待补充` in Stage0 | Proof body, wrapper, or pinned dependency | Absent |

The computer-science corpus separately says `MDS码的构造` and generated Stage0 item
`THM-C-0381`. Stage0's retention priority does not merge nonidentical records, and the item is not
in the Stage1 Lean target set. It is contextual duplicate evidence only; its extra word
`的构造` cannot be imported into `THM-M-1592` without an explicit scope decision.

## Primary-source lead

Crossref metadata identifies I. S. Reed and G. Solomon, "Polynomial Codes Over Certain Finite
Fields," *Journal of the Society for Industrial and Applied Mathematics* 8(2), June 1960, pages
300-304, DOI `10.1137/0108018`. The observed Crossref response has SHA-256
`616d333004a925aed3c11126c9e922296fb1b71724c0911bb36332077cba7440`. Semantic Scholar independently
matches the title, DOI, year, and a closed-access status.

This is a bibliographic discovery lead, not H0 evidence. The repository does not cite it, the
publisher PDF endpoint returned HTTP 403 in this worker environment, and no lawful local immutable
paper snapshot, page-by-page statement transcription, assumptions, proof dependencies, errata
decision, or independent source review was available. Bibliographic pages 300-304 locate the paper,
not a specific proposition inside it. The intake therefore does not claim that the catalog's terse
`MDS码` wording is source-identical to any particular modern Reed-Solomon theorem.

## Source-family alternatives

| Candidate mathematical component | Prospective Lean target surface | Intake assessment |
|---|---|---|
| Polynomial evaluation at distinct finite-field points | A degree-bounded polynomial subspace and an evaluation linear map into a finite Pi type | Plausible construction family; exact field, indices, point model, and cutoff are not selected |
| Evaluation injectivity and message dimension/cardinality | Root-count or Vandermonde argument plus rank/dimension/cardinality facts | Distinct parameter theorem; not automatically an MDS theorem |
| At least `n-k+1` pairwise Hamming distance | Difference polynomial, distinct roots, Hamming support count | Plausible lower-bound family; binder order and endpoint conventions remain open |
| Exact minimum distance `n-k+1` | Lower bound plus a matching codeword or a Singleton-bound upper bridge | Familiar MDS theorem family, but neither exact source statement nor upper-bound dependency is selected |
| Equality in the Singleton bound | A source-selected code/dimension/distance definition and checked equivalence to explicit parameters | `MDS` interpretation candidate; no accepted transport exists |
| Correction of a bounded number of errors/erasures | Distance-to-unique-decoding bridge or a specified decoder-correctness theorem | A consequence or algorithm theorem, not interchangeable with the MDS root |
| Generalized, extended, shortened, punctured, or projective variants | Different evaluation domains, multipliers, coordinate extensions, and parameters | Materially different targets requiring explicit source authority |

## Pinned Lean discovery surface

| Pinned module/declaration | Possible role | Credited status |
|---|---|---|
| `Mathlib.InformationTheory.Hamming`: `hammingDist`, `hammingNorm`, `Hamming` | Word distance and weight substrate | API availability only |
| `Mathlib.Algebra.Polynomial.Roots`: `Polynomial.card_roots'` | Bound the number of roots of a polynomial by its natural degree | Generic algebraic substrate only |
| `Mathlib.LinearAlgebra.Vandermonde`: `Matrix.vandermonde`, `Matrix.det_vandermonde`, `Matrix.det_vandermonde_ne_zero_iff` | Evaluation-matrix and distinct-point injectivity substrate | Generic matrix facts only |
| `Matrix.eval_matrixOfPolynomials_eq_vandermonde_mul_matrixOfPolynomials` | Relate evaluations of bounded-degree polynomials to a Vandermonde matrix | Adjacent feasibility API; no code or MDS theorem |

A bounded case-insensitive search of pinned mathlib and repo-local Lean for `Reed-Solomon`,
`maximum distance separable`, `MDS code`, `evaluation code`, and `polynomial code` returned no
match. A negative lexical search is not an exhaustive formal-candidate audit and cannot prove that
no relevant theorem exists under another encoding. `IntakeProbe.lean` merely authenticates the
generic APIs above at the pinned revisions.

## Required source acceptance

Before the statement phase can pass, accountable reviewers must admit an immutable primary source,
select exactly one proposition, and record its edition, stable identifier, theorem/equation/section
and page locator, exact ordered premises and conclusion, incorporated definitions, proof boundary,
dependencies, errata/correction status, and translation decisions. The crosswalk must then map every
field, parameter, evaluation, polynomial-degree, code, distance, MDS, boundary, and any decoding
convention to the Lean target and check alternate encodings in the credited directions. Until then
the expression fingerprint remains null, human status is at most `H1`, and no machine or
theorem-completion claim is legal.
