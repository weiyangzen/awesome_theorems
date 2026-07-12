# Source-statement crosswalk

## Repository source record

`Docs/researches/math_theorems.md` records Eugene Wigner, 1955, the phrase "eigenvalue distributions
of random matrices," high importance, and the label `已验证`. `Docs/Stage0_Blueprint.md` repeats
these fields but leaves exact definitions, hypotheses, proof route, axioms, and formal artifacts
open. The rev-5.6 manifest deliberately records the old label as `source_status_untrusted`.

Consequently, the repository wording is neither an exact human theorem nor evidence of a Lean
proof. The old `已验证` label supplies no H0, M0, or completion credit.

## Candidate primary-source leads

- Eugene P. Wigner, "Characteristic Vectors of Bordered Matrices With Infinite Dimensions,"
  *Annals of Mathematics* 62 (1955), 548-564. This matches the repository attribution and year and
  is the first historical source to inspect. Exact internal theorem, hypotheses, notation, and
  errata have not been verified here.
- Freeman J. Dyson, "Statistical Theory of the Energy Levels of Complex Systems. I," *Journal of
  Mathematical Physics* 3 (1962), 140-156, together with Parts II and III. This is a historical
  lead for ensemble and eigenvalue-statistics formulations, not a selected root statement.
- Madan Lal Mehta, *Random Matrices*, Academic Press. A fixed edition could provide a stable modern
  formulation and notation cross-check, but edition, theorem/page, assumptions, and errata remain
  uninspected.

These are discovery leads only. A later source audit must bind an immutable edition, exact
theorem/page, assumptions, proof boundary, and errata, and must independently review the choice.

## Crosswalk

| Repository component | Possible source meanings | Required Lean surface | Intake result |
|---|---|---|---|
| "random matrix" | a measurable finite matrix, or a size-indexed ensemble | probability law, matrix scalar field and symmetry, dimension index | unresolved |
| "eigenvalues" | unordered multiset, ordered real tuple, or empirical counting measure | self-adjoint spectrum and multiplicity-aware enumeration | unresolved |
| "distribution" | joint finite-size density, empirical measure, expectation, or limiting law | exact measurable statistic and probability/pushforward measure | unresolved |
| Wigner, 1955 | historical global-spectrum work | pinpoint proposition and exact normalization | candidate source only |
| `已验证` | untrusted metadata label | accepted kernel receipt and complete provenance/trust closure | rejected as proof evidence |

## Gate to the exact statement

The first hard gate is unique proposition selection. A reviewer must inspect an exact primary
statement, justify why it belongs to this umbrella target rather than `THM-M-1105`, `THM-M-1106`,
`THM-M-1107`, or `THM-M-1109`, and crosswalk every hypothesis, conclusion, convention, and
degenerate case. The resulting Lean expression must then elaborate under pinned imports and pass
the required statement mutations. Until that happens the human status is at most `H1`, the machine
status is `M4`, and no canonical Lean expression or proof is claimed.
