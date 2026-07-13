# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:7155-7160` supplies exactly the Chinese title
`Bennett不等式`, George Bennett, 1962, the gloss `随机变量和的尾概率`, importance `高`, and status
`已验证`. The same six-field record is duplicated at lines 7280-7285. Git blame places both uncited
records at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. Neither record contains a
bibliography, formula, domains, definitions, hypotheses, constants, proof boundary, corrections,
reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:26713-26738` repeats the gloss while explicitly leaving the formal
system, logical foundation, precise definitions and premises, proof route, dependencies,
equivalent statements, axioms, machine status, and artifact links open. The rev-5.6 manifest keeps
`已验证` only as untrusted metadata, assigns rank 1514, and resets the target to
`L0 / rework_required` with no accepted legacy artifacts.

The manifest category `组合数学 / 计数组合` disagrees with the probability subject matter and the
duplicate source record's placement. Intake preserves the manifest authority while recording this
as a source-classification issue; it does not change target ownership or meaning.

## Human source lead

Crossref metadata was inspected for DOI `10.1080/01621459.1962.10482149` and identifies:

- George Bennett, *Probability Inequalities for the Sum of Independent Random Variables*;
- *Journal of the American Statistical Association*, volume 57, issue 297;
- March 1962, pages 33-45; and
- DOI `10.1080/01621459.1962.10482149`.

The metadata matches the catalog author, year, theorem name, and gloss. Semantic Scholar also
identified the same DOI, title, author, and year, but reported no open-access PDF or abstract.
Publisher and JSTOR requests were access-blocked, so the article text was not inspected. The
catalog does not cite the article. Consequently this is a bibliographic `E5` source-family lead,
not an admitted primary statement/proof record and not `H0` evidence.

Before `H0`, an accountable reviewer must lawfully preserve an immutable edition, pinpoint the
exact theorem and incorporated definitions by page or stable locator, map every premise and
conclusion, identify dependent results and the proof boundary, audit corrections and errata,
resolve the catalog category and duplicate-record provenance, and approve the crosswalk
independently.

## Candidate clause crosswalk

No exact source text was admitted during intake. The table records questions, not a canonical
statement.

| Catalog or source-family phrase | Prospective mathematical component | Prospective Lean surface | Intake status |
|---|---|---|---|
| "sum of independent random variables" | a finite or countable indexed family on a probability space | `Measure`, a finite index type or `Finset`, and `iIndepFun` | index, measurability, integrability, and independence conventions open |
| "tail probability" | an upper, lower, two-sided, or maximal tail event | a measurable set and `μ.real` or `μ` comparison | event direction, strictness, centering, codomain, and threshold domain open |
| Bennett boundedness premise | one-sided or absolute almost-sure bounds, common or individual | an `Eventually` inequality under `ae μ` | exact premise and constants open |
| variance or moment input | exact variance sum or an admitted proxy | `ProbabilityTheory.variance` and a finite sum | definition and inequality direction open |
| Bennett rate | a source-defined exponential rate function | `Real.exp`, `Real.log`, arithmetic, and a totalized boundary encoding | formula, normalization, and zero-case extension open |
| George Bennett / 1962 | historical and proof provenance | source record and future obligation crosswalk | matching bibliographic lead only; no admitted statement or proof |
| `已验证` | untrusted inventory label | no Lean declaration or receipt | explicitly rejected as evidence |

## Pinned formal candidate boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the representative
interfaces checked by `IntakeProbe.lean` are:

- `ProbabilityTheory.mgf` and `ProbabilityTheory.cgf`;
- `ProbabilityTheory.measure_ge_le_exp_mul_mgf` and
  `ProbabilityTheory.measure_ge_le_exp_cgf`, generic Chernoff upper-tail bounds;
- `ProbabilityTheory.iIndepFun.mgf_sum`, the finite independent-sum MGF product identity; and
- `ProbabilityTheory.IndepFun.variance_sum`, the independent finite-sum variance identity.

These are generic ingredients, not a Bennett-specific MGF lemma or terminal tail theorem. A
bounded search for `Bennett`, the theorem title, and representative aliases found only a legacy
Bernstein planning record that explicitly lists Bennett as absent, plus this dossier's own
disclaimers. No source-identical Bennett declaration was located. The result is bounded discovery
evidence only: statement identity, exhaustive search, exact body provenance, transitive trust,
placeholder and unsafe closure, and machine classification belong to later phases.

## Statement gate

The statement phase must first admit the exact source proposition, decide every boundary in
`scope-map.md`, and elaborate only that proposition with minimal pinned imports, fixed options and
contexts, a serialized expression and environment fingerprint, checked alternate transports, and
the four required mutation classes. Until then the canonical statement, module, declaration or
expression, expression hash, and canonical-target environment fingerprint remain null.
