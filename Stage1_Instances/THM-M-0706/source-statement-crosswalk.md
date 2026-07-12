# Source-statement crosswalk

## Available repository sources

`Docs/researches/math_theorems.md` supplies the title, Church/Turing attribution, 1936 date, gloss
`可计算性的等价定义`, and `已验证`. `Docs/Stage0_Blueprint.md` repeats that record but leaves exact
definitions, assumptions, proof route, equivalent forms, axioms, and machine artifacts open.
Separately, `Docs/researches/cs_theorems.md` gives the conventional broader wording "all
intuitively computable functions are computable by a Turing machine" and marks it `不可形式化`.
Thus repository provenance establishes a topic and an unresolved scope conflict, not a unique
proposition or proof status.

## Candidate primary-source boundaries

- Alonzo Church, "An Unsolvable Problem of Elementary Number Theory", *American Journal of
  Mathematics* 58(2) (1936), 345-363, DOI `10.2307/2371045`, introduces effective calculability via
  lambda-definability/recursiveness and proves formal results around that identification. Exact
  theorem text, definitions, page-level assumptions, and corrections require inspection before it
  can define this target.
- A. M. Turing, "On Computable Numbers, with an Application to the Entscheidungsproblem",
  *Proceedings of the London Mathematical Society* s2-42(1) (1937), 230-265, DOI
  `10.1112/plms/s2-42.1.230` (received 1936), defines machine computability and argues its adequacy;
  its appendix sketches equivalence with lambda-definability. The appendix's exact strength and
  dependence on Church's formalism must be audited rather than paraphrased as a blanket biconditional.

These are candidate primary boundaries, not an `H0` crosswalk. No edition, pinpoint theorem/page,
assumption set, errata check, or independent review has yet been accepted.

## Crosswalk

| Repository/source phrase | Mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "equivalent definitions of computability" | equality/equivalence of two specified formal function classes | two typed computability predicates over fixed domains | models and domains open |
| Church formalism | lambda-definability or general recursiveness under exact historical definitions | syntax, substitution/evaluation or recursive-function closure | encoding open |
| Turing formalism | machine-computable partial or total numerical functions | machine configurations, step semantics, halting/output relation | encoding open |
| "equivalent" | both directions, possibly via effective code translations | two implications plus checked semantic-preservation bridges | strength open |
| "intuitively computable" | pre-formal notion of effective procedure | no non-circular formal predicate supplied | hard boundary for exact statement |
| Church-Turing thesis | adequacy claim connecting the informal notion to a formal model | cannot receive kernel proof merely by defining the informal side | distinct from model equivalence |
| `已验证` / `不可形式化` | conflicting inventory metadata | no kernel evidence | no proof credit |

## Source and machine boundary

No theorem-specific Lean declaration is identified by this intake. That narrow fact is not the
dependency-ordered anchor audit and does not establish absence from mathlib or external projects.
Before `H0`, an independent reviewer must inspect stable copies, pinpoint the exact formal theorem
and pages, definitions, assumptions, proof boundary, errata, and its relationship to the informal
thesis. Before statement credit, the approved formal components must map to one elaborated Lean
expression, and any alternate model/class formulation needs a checked equality, `Iff`, or the
precisely claimed implications.
