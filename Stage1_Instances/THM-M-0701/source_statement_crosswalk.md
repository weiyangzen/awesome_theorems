# Source-statement crosswalk

| Claim component | Repository or primary-source anchor | Lean target | Intake assessment |
|---|---|---|---|
| Target name | `Docs/Stage0_Blueprint.md`, `THM-M-0701`: “归结原理” | none | Names a family of resolution results, not a proposition |
| Repository description | Same record: “自动定理证明的方法” | none | Describes a method; supplies no domains, hypotheses, or conclusion |
| Attribution and date | Same record: John Alan Robinson, 1965 | none | Consistent with the historical paper, but does not identify a theorem within it |
| Primary-source candidate | J. A. Robinson, “A Machine-Oriented Logic Based on the Resolution Principle,” *Journal of the ACM* 12(1) (1965), 23-41, DOI `10.1145/321250.321253` | none | Discovery anchor only; no immutable copy, pinpoint theorem/premise mapping, or errata review is accepted |
| Local soundness candidate | Resolution-rule consequence theorem | unresolved | A possible component, not selected by the repository wording |
| Refutation-completeness candidate | Propositional or first-order empty-clause derivability from unsatisfiability | unresolved | Likely historical intent, but multiple non-equivalent scopes remain |
| Lifting candidate | Ground-to-first-order resolution lifting | unresolved | Candidate bridge; not evidence for an exact root |

## Crosswalk verdict

There is no exact source statement to crosswalk to Lean. In particular, the
historical paper title cannot be promoted into a chosen theorem statement.
The source owner must provide a stable edition and pinpoint result, then map
every definition and premise to the selected formal target. Errata and later
corrections must also be checked before `H0` is possible.

No human proof status, machine statement identity, alternate-encoding bridge,
or theorem-completion credit is claimed by this document.
