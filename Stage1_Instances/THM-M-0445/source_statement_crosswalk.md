# Source-statement crosswalk

## Repository wording

The repository catalog identifies the target name as the Rubin-Kolyvagin theorem, attributes it to
Karl Rubin and Victor Kolyvagin, gives 1991, and supplies only the gloss `椭圆曲线的BSD` (BSD for
elliptic curves). The Stage0 record leaves the exact definitions, premises, conclusion, proof route,
dependencies, axioms, machine status, and artifact links open. No admitted source gives a work,
edition, theorem number, page, curve class, rank hypothesis, nonvanishing condition, conclusion,
correction, or errata disposition.

## Candidate clauses

| Candidate clause | Evidence | Statement disposition |
|---|---|---|
| elliptic curves over `Q` | legacy discovery artifact only | plausible domain; not source-admitted |
| analytic rank at most one | legacy discovery artifact only | not source-admitted |
| equality of analytic and Mordell-Weil ranks | legacy discovery artifact only | not source-admitted |
| finiteness of the Tate-Shafarevich group | legacy discovery artifact only | not source-admitted |
| Heegner point or Euler/Kolyvagin-system hypotheses | target name and legacy discovery artifact only | exact branch and hypotheses unresolved |
| CM/Iwasawa-theoretic hypotheses | target name and legacy discovery artifact only | exact Rubin specialization unresolved |
| full BSD leading-term formula | broad BSD gloss only | stronger candidate not selected by the source |
| rank-zero, rank-one, bad-reduction, and vanishing boundary cases | no exact repository wording | boundary policy unresolved |

The legacy file `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_091.lean` explicitly describes
`StatementShape` and `FullBSDStatementShape` as abstract statement-shape boundaries. Its arbitrary
numeric and proposition fields stand in for the missing elliptic-curve L-function, Mordell-Weil
rank, Tate-Shafarevich group, Euler/Kolyvagin systems, and Selmer-control APIs. Under the uniform L0
rework rule it is discovery input, not source or exact-target authority.

## Competing interpretations

The gloss does not distinguish a low-analytic-rank rank-and-finiteness consequence from full BSD,
nor Kolyvagin's Heegner-point/Euler-system route from Rubin's CM/Iwasawa-theoretic route. These have
different hypotheses and conclusions. Combining both branches as conjunctive hypotheses, using
arbitrary `Prop` fields, or choosing whichever conclusion is easiest to encode would substitute a
different proposition.

## Required resolution

The statement gate requires one admitted primary or approved-authoritative passage with a stable
edition, theorem/page locator, incorporated definitions, exact ordered assumptions and conclusion,
proof boundary, correction and errata disposition, exact translation, and independent review. That
decision must fix the base field and curve hypotheses, analytic-rank and L-function normalization,
the relevant Rubin or Kolyvagin inputs, Mordell-Weil-rank and Tate-Shafarevich conventions, the BSD
strength claimed, and degenerate cases. Until then the canonical human statement, Lean target,
expression fingerprint, credited transports, and mutations remain null or unexecutable.

This crosswalk is a truthful blocker record. It supplies no H0, exact-statement, proof, audit, or
theorem-completion credit.
