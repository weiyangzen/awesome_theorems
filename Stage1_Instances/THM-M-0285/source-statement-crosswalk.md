# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:2048-2053` supplies exactly the title
`波雷尔-坎泰利引理`, attribution to Emile Borel and Francesco Cantelli, the year 1909, the gloss
`无穷事件列的发生概率` ("the probability of an infinite sequence of events"), importance "high,"
and status `已验证`. Git history attributes all six uncited lines to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The same six-line record is duplicated at lines
7406-7411. Neither occurrence contains a bibliography, theorem locator, formula, ordered binders,
hypotheses, proof boundary, correction history, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:7873-7901` repeats the gloss while explicitly leaving the formal system,
foundation, exact definitions and premises, proof route, dependencies, alternate formulations,
axioms, machine status, and artifact links open. The rev-5.6 target manifest retains `已验证` only
as untrusted metadata and resets the target to `L0 / rework_required`.

No primary mathematical source was admitted during intake. In particular, the year and joint
attribution do not decide which historical Borel or Cantelli result, edition, theorem, definitions,
or modern combined formulation the catalog intends. A familiar textbook statement reconstructed
from memory would not satisfy the rev-5.6 `H0` source contract.

## Clause crosswalk

| Catalog component | Candidate mathematical reading | Pinned Lean surface | Intake assessment |
|---|---|---|---|
| "infinite sequence of events" | a sequence `s : Nat -> Set Omega` and its infinitely-often/limsup event | `Filter.limsup s Filter.atTop` | sample space, measurability, filter encoding, and exact event statement open |
| "probability" | measure-zero conclusion from a convergent series (first lemma) | `MeasureTheory.measure_limsup_atTop_eq_zero` | exact-topic candidate; source does not select this direction |
| "probability" | measure-one conclusion from divergence plus mutual independence (second lemma) | `ProbabilityTheory.measure_limsup_eq_one` | exact-topic candidate; adds measurability, independence, and probability-space content absent from the gloss |
| infinitely many occurrences | almost every point belongs to only finitely many events | `MeasureTheory.ae_finite_setOf_mem` | alternate first-lemma encoding only; no checked target transport frozen |
| generalized conditional form | limsup membership iff divergence of predictable conditional sums almost everywhere | `MeasureTheory.ae_mem_limsup_atTop_iff` | Levy generalization; explicit non-substitute unless selected by an accepted source |
| `已验证` | untrusted inventory label | source review and kernel receipts would be required | no H or M credit |

## Pinned Lean boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`:

- `Mathlib.MeasureTheory.OuterMeasure.BorelCantelli` provides
  `MeasureTheory.measure_limsup_atTop_eq_zero`: for a natural-number-indexed family under an
  `OuterMeasureClass`, a non-infinite `ENNReal` total measure implies a zero-measure limsup.
- `Mathlib.Probability.BorelCantelli` provides
  `ProbabilityTheory.measure_limsup_eq_one`: measurable mutually independent events with infinite
  total measure have limsup measure one; the independence interface supplies the probability
  measure instance used by the theorem.
- `Mathlib.Probability.Martingale.BorelCantelli` provides
  `MeasureTheory.ae_mem_limsup_atTop_iff`, Levy's generalized conditional form.

The intake probe elaborates these declarations and reports the axioms of the two customary
endpoints. This authenticates candidate interfaces only. It does not establish which expression is
source-identical, certify minimal imports for an absent target, inspect terminal proof provenance,
freeze a discovery denominator, or confer proof credit.

## Source gate

Before leaving `H1`, accountable reviewers must preserve a lawful immutable primary or
authoritative source edition, identify the exact theorem and incorporated definitions, decide first
versus second versus paired scope, map every domain, binder, hypothesis, convergence/divergence
condition, independence condition, limsup encoding, conclusion, and boundary case, audit corrections
and historical attribution, and independently approve fidelity to `THM-M-0285`.

Only after that source decision may the statement phase select minimal imports, freeze an
elaborated expression and environment fingerprint, compile checked alternate encodings, and run the
required removed-hypothesis, changed-domain, binder-scope, and boundary-case mutations.
