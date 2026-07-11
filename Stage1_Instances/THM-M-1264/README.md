# THM-M-1264 rev-5.6 intake

This is a `planned` dossier for the source label "Variational methods for PDE" (`PDE的变分方法`).
The repository source does not contain a mathematical proposition. It gives no functional, space,
equation, boundary data, assumptions, or conclusion. Consequently there is no truthful canonical
Lean target at intake, and selecting a familiar theorem from the subject would broaden or substitute
the assigned claim.

## Scope map

| Surface | Source supplies | Required before statement phase can close |
|---|---|---|
| Mathematical object | PDE and variational-method topic only | exact PDE/operator, domain, coefficients, data, and boundary conditions |
| Variational object | none | functional, admissible space, topology, and differentiability/coercivity assumptions |
| Claimed result | none | exact quantified conclusion: existence, equivalence, uniqueness, or regularity |
| Formal target | Lean 4 is the queue backend | ordered binders, universes, definitions, imports, and declaration type |
| Human source | attribution only to "many mathematicians" | theorem-bearing primary source with edition/page/theorem and assumptions |
| Machine evidence | untrusted Stage0 label `已验证` | exact elaboration, mutation checks, proof provenance, and kernel validation |

Potential theorem families such as Euler-Lagrange equivalence, direct-method existence, weak
solutions, and minimax critical points are discovery categories only. None is adopted as the root.
The structured absence and prohibited substitutions are frozen in `intake.json`; the source-field
crosswalk is in `source_statement_crosswalk.md`.

## Intake verdict

Lifecycle remains `planned`, with conservative root vector `[H4, M4, R4]`. The first failed gate is
exact human statement identification. The remaining root cut set is: recover an authoritative exact
claim; identify its primary source; then freeze domains, hypotheses, conclusion, and a Lean target.
The theorem is not complete.

## Validation

The commands and results in `validation.md` establish target membership, standard consistency, JSON
syntax, and dossier-local structural assertions only. They provide no mathematical or Lean proof
credit.
