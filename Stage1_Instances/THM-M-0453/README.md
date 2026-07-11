# THM-M-0453 rev-5.6 intake

This directory is the rev-5.6 `planned` dossier for the target labelled "Selmer group". The
repository gloss, "the Selmer group of an elliptic curve", names a mathematical object rather than
a proposition. It does not select a prime or isogeny, base field, local conditions, or a theorem
about the resulting group. Historical metadata status is discovery input only.

## Scope map

| Surface | Candidate scope | Intake boundary |
|---|---|---|
| Global object | an elliptic curve `E` over a global field `K` | neither `K` nor a model/category for `E` is fixed |
| Descent datum | multiplication by an integer/prime, or an isogeny `phi : E -> E'` | the source does not choose one |
| Local conditions | kernel of the global-to-local restriction map into local cohomology quotients | places, completions, cohomology, and Kummer maps are unspecified |
| Common theorem candidates | exact descent sequence, finiteness, or a rank bound | none may be inferred from the object label |
| Lean target | a concrete definition plus a proposition about it | no repo-local or mathlib declaration was found by the intake search |
| Foundations | Lean 4 kernel with pinned mathlib and an audited classical/choice profile | exact profile and dependency closure remain open |

## Intake verdict

The exact human claim cannot be frozen without inventing or substituting mathematics. The
provisional root vector is `[H4, M4, R4]`; the first failed gate is exact source-statement
identification. Lifecycle remains `planned`, and the theorem is not complete. The dependent work is
listed in `task_dag.json`; none receives proof credit from this intake.

The commands in `validation.md` establish target membership, repository consistency, structured
artifact syntax, and local reference integrity only. No Lean theorem or kernel result is claimed.
