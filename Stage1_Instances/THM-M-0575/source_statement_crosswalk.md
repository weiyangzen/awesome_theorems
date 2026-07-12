# Source-statement crosswalk

The repository source record identifies Raoul Bott, the year 1959, and only the phrase "periodicity
of K-theory." That wording is not an exact mathematical proposition. The crosswalk below records
discovery anchors and the decisions still required; it deliberately makes no `H0` claim.

| Claim component | Human source anchor | Intended formal surface | Intake assessment |
|---|---|---|---|
| Original stable periodicity theorem | R. Bott, *The stable homotopy of the classical groups*, Annals of Mathematics (2) 70 (1959), 313-337 | Stable unitary-group/loop-space formulation | Primary original source candidate consistent with the recorded author and year; exact theorem/page, hypotheses, and modern notation crosswalk remain unaudited |
| Complex K-theory period two | M. F. Atiyah, *K-Theory*, W. A. Benjamin, 1967, periodicity chapter | Bott multiplication or double suspension in reduced complex topological K-theory | Standard source candidate for the selected provisional root; edition, theorem/page, space category, and convention transcription remain open |
| Root operation | Multiplication/external product with the complex Bott class | `BP-BOTT` and `BP-INVERT` | The class, degree/sign convention, and proof that its action is invertible must be identified from the selected source |
| Naturality | Functoriality of the periodicity isomorphism in the admitted class of spaces | `BP-NAT` | Expected part of the K-theory theorem, but not inferred as accepted from the abbreviated repository wording |
| Double-suspension form | Periodicity expressed through two suspensions of reduced K-theory | `BP-TRANSPORT` | Candidate equivalent encoding only; requires source convention alignment and a checked Lean transport |
| Real period eight | Real topological `KO` periodicity | Excluded from `BP-ROOT` | Mathematically related Bott periodicity, but a distinct theorem and not a permitted substitute for complex period two |

Discovery identifiers (not immutable evidence receipts):

- Bott 1959 DOI: <https://doi.org/10.2307/1970106>
- Atiyah's 1967 monograph bibliographic record: *K-Theory*, W. A. Benjamin, New York.

The statement phase must first choose and transcribe one exact primary formulation, including the
category of spaces, reduced/unreduced convention, degree direction, and naturality content. It must
then select a Lean representation, elaborate it with pinned imports, fingerprint the expression,
and check every credited transport. Until edition/file hashes, pinpoint theorem/page mapping,
assumption and errata audits, and independent review exist, the human status remains `H1`.

The pinned repo-local mathlib source was searched at intake for case-insensitive `Bott`/`Bott
period`; no relevant K-theory periodicity declaration was located. This is a bounded discovery
observation, not an exhaustive anchor audit and not proof that no external Lean formalization
exists. Formal candidate classification belongs to the dependent anchor-audit phase.
