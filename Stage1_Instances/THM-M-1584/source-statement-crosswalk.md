# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:11672-11677` supplies exactly the title
`Chaitin不可计算数`, attribution Gregory Chaitin, year 1975, gloss `Omega数的不可计算性`,
importance `high`, and status `verified`. Git history places all six uncited fields in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:43066-43091` repeats the metadata while explicitly leaving exact
definitions and premises, proof route, dependency graph, equivalent forms, axioms,
machine-checked status, and artifact links open. The rev-5.6 manifest preserves `verified` only as
untrusted metadata and resets the target to `L0 / rework_required`.

The repository has no bibliography, edition, theorem/page locator, definition of `Omega`, machine
or universality convention, ordered binders, hypotheses, conclusion, proof boundary, correction
record, or reviewer. The wording identifies a theorem family but not one stable proposition.

## Historical primary-source leads

Crossref and DBLP identify Gregory J. Chaitin, *A Theory of Program Size Formally Identical to
Information Theory*, *Journal of the ACM* 22(3) (July 1975), pages 329-340, DOI
`10.1145/321892.321894`. This matches the author and year and is a strong primary lead for the
self-delimiting program-size framework. The worker could verify bibliographic metadata but could
not lawfully inspect a complete version-of-record text: the publisher PDF returned HTTP 403 and
the discovered repository mirrors were unavailable. No assertion is made that a particular page
in this paper states the catalog root.

Crossref also identifies Gregory J. Chaitin, *Randomness and Mathematical Proof*, *Scientific
American* 232(5) (May 1975), pages 47-52, DOI `10.1038/scientificamerican0575-47`. This is another
author/year-matching primary exposition lead. Its exact Omega definition, hypotheses, conclusion,
proof boundary, and relationship to the JACM formulation were not inspected or admitted.

Both records are discovery provenance only. A bibliography, URL, and matching date do not satisfy
the rev-5.6 `H0` contract. Later book formulations may be clearer, but silently replacing the 1975
catalog provenance with a modern theorem would be a source substitution.

George Barmpalias, *Aspects of Chaitin's Omega*, arXiv:1707.08109v5 (2018), is a useful secondary
scope audit. Section 1.2, PDF pages 3-4, defines `Omega_U` for a universal self-delimiting machine
as the sum of `2^(-|sigma|)` over halting programs, emphasizes that Omega is a machine-indexed
family, and distinguishes universality from optimality. Section 2.1, PDF page 5, attributes
Martin-Lof randomness of `Omega_U` to Chaitin's 1975 JACM paper, bibliography item [39]. It also
attributes the full characterization of Omega reals to cumulative later work. This makes the 1975
paper a substantive historical lead while confirming that a modern characterization must not be
silently assigned to it. The survey is secondary evidence and supplies neither the missing exact
primary crosswalk nor `H0`.

## Component crosswalk

| Catalog component | Material interpretations | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| `Omega数` | one `Omega_U`, all universal-machine halting probabilities, or the class of Omega reals | a source-selected real-valued construction indexed by machines | quantifier scope absent |
| machine | universal prefix-free machine, optimal self-delimiting computer, or another source model | program type, partial evaluator, coding, and universality predicate | model absent |
| halting probability | product measure of the halting set or sum of `2^(-length p)` | convergent exact nonnegative series and real/NNReal transport | construction absent |
| prefix-free | domain of valid halting programs is prefix-free/self-delimiting | predicate on an infinite language, not merely finite unique decodability | convention absent |
| uncomputable | no effective two-sided approximation/name for the resulting real | selected computable-real predicate and negation | representation absent |
| 1975 | JACM technical article, Scientific American exposition, or another Chaitin source | source provenance only | exact result/edition not selected |
| `verified` | untrusted catalog label | no Lean declaration or proof body | explicitly rejected as evidence |

## Candidate roots not yet credited

| Candidate | Why it is not silently selected |
|---|---|
| For every universal prefix-free machine `U`, `Omega_U` is noncomputable | requires exact universality, prefix-free, probability, and computable-real definitions |
| For one fixed universal self-delimiting machine, its halting probability is noncomputable | repository names no machine; treating an arbitrary fixed machine as universal is invalid |
| There exists a noncomputable halting probability | weaker quantifier structure than the usual universal-machine result |
| A real is an Omega real iff it is lower semicomputable and Martin-Lof random | later characterization with materially more definitions and two implications |
| The bits of `Omega_U` are algorithmically random/incompressible | stronger or alternate conclusion requiring a checked implication to noncomputability |
| An initial segment of Omega decides bounded halting questions | a proof lemma/consequence, not automatically the catalog root |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe
checks `Nat.Partrec.Code`, its partial evaluator, halting undecidability, finite unique decodability,
and Kraft-McMillan. These APIs could support fragments of a future encoding, but they neither
define an infinite prefix-free universal machine nor a computable-real predicate or Omega theorem.

A bounded case-insensitive declaration/source search over pinned mathlib and repo-local Lean found
no exact Chaitin, halting-probability, prefix-free-machine, algorithmic-randomness, or Omega-real
target. This is a dated intake observation with a recorded query, not exhaustive external-project
discovery and not an absence proof.

## Required source admission

The statement phase must preserve and hash a lawful complete primary edition, select the precise
definition and result, transcribe every incorporated definition, ordered binder, hypothesis, and
conclusion, map the proof boundary, reconcile historical and modern terminology, audit corrections
and errata, and obtain independent source review. It must then freeze and mutation-test the same
exact Lean expression. Until that happens, the canonical mathematical and Lean targets remain null
and the source classification remains `H1`.
