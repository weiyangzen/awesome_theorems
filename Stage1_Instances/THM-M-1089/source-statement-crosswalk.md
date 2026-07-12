# Source-statement crosswalk

## Repository sources

`Docs/researches/math_theorems.md` gives only "comparison theorem for Gaussian processes," credits
many mathematicians, dates it to the twentieth century, and labels it `已验证`. The generated
`Docs/Stage0_Blueprint.md` repeats those fields while leaving definitions, assumptions, proof
route, formal artifacts, and axioms open. The rev-5.6 manifest preserves the name and category but
explicitly treats the old status as untrusted metadata.

Consequently, none of these repository records is an exact human statement or proof source. The
`已验证` label supplies no `H0`, machine-proof, or theorem-completion credit.

## Candidate primary-source leads

- D. Slepian, "The one-sided barrier problem for Gaussian noise," *Bell System Technical Journal*
  41 (1962), 463-501, is a historical lead for covariance comparison of Gaussian maxima.
- X. Fernique, "Regularite des trajectoires des fonctions aleatoires gaussiennes," in *Ecole
  d'Ete de Probabilites de Saint-Flour IV-1974*, Lecture Notes in Mathematics 480, Springer, 1975,
  is a lead for the expected-supremum comparison commonly called Sudakov-Fernique.
- Y. Gordon, "Some inequalities for Gaussian processes and applications," *Israel Journal of
  Mathematics* 50 (1985), 265-289, is a lead for Gaussian min-max comparison inequalities.

These are discovery leads, not immutable source receipts. Exact edition, numbered theorem, page,
assumptions, proof boundary, and errata have not been inspected, and no lead has been selected as
the canonical root. The Slepian family also has its own repository target (`THM-M-1085`), which is
positive evidence that silently duplicating it here would require explicit source justification.

## Statement crosswalk

| Repository component | Possible source meanings | Required Lean surface | Intake result |
|---|---|---|---|
| "Gaussian process" | finite vector, arbitrary separable process, Banach Gaussian variable, or Gaussian array | exact index type, probability spaces/laws, codomain, and joint-Gaussian predicate | unresolved |
| "comparison" | covariance, increment-metric, convex-set, or min-max order | explicitly oriented hypothesis relations | unresolved |
| "inequality" | event probability, expected supremum, or expected/probabilistic min-max bound | exact codomain, functional, binders, and inequality direction | unresolved |
| "many mathematicians" | a theorem-family label rather than an attribution | one selected declaration mapped to one pinpoint source | unresolved |
| twentieth century | broad historical metadata | immutable edition/revision | no evidentiary value |
| `已验证` | metadata screening label | inspectable proof body and accepted kernel receipt | rejected as proof evidence |

## Gate to the statement phase

The first hard gate is named-theorem selection. A reviewer must select and inspect an exact primary
statement, justify its match to this target rather than a neighboring target, record theorem/page
and errata, and crosswalk all hypotheses, conclusions, and degenerate cases. The later formal
statement must then elaborate under pinned imports and mutation-test the comparison orientation,
removed hypotheses, changed index domain, binder scope, and boundary cases. Until those tasks pass,
the human status is at most `H1`, machine status is `M4`, and no Lean expression is claimed.
