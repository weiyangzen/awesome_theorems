# Source-statement crosswalk

## Repository record and candidate sources

The repository inventory supplies only the title "random matrices and integrable systems," the
attribution "many mathematicians," the twentieth century, and the gloss "the connection between
random matrices and integrable systems." Its `已验证` field is untrusted metadata under rev-5.6. It
contains no ensemble, observable, equation, quantifiers, hypotheses, or conclusion and therefore
does not identify an exact proposition.

Two primary-publication candidates illustrate distinct precise readings:

- Mark Adler and Pierre van Moerbeke, "Matrix integrals, Toda symmetries, Virasoro constraints, and
  orthogonal polynomials," *Duke Mathematical Journal* 80 (1995), 863-911. This is a candidate for
  a matrix-integral/Toda/tau-function target.
- Craig A. Tracy and Harold Widom, "Level-spacing distributions and the Airy kernel,"
  *Communications in Mathematical Physics* 159 (1994), 151-174. This is a candidate for a
  gap-probability/Fredholm-determinant/integrable-equation target, but it must not be silently
  substituted for the repository's separate Tracy-Widom target.

These citations are discovery anchors only. This intake has not inspected an immutable copy to
approve an exact theorem/equation/page, all definitions and assumptions, proof boundaries, or
errata. Neither candidate earns `H0`, and choosing between them is part of the statement gate.

## Crosswalk

| Repository/source phrase | Mathematical component to freeze | Required Lean component | Intake status |
|---|---|---|---|
| random matrix | exact field, symmetry class, size, probability law, and potential | measurable matrix-valued random variable or finite-dimensional density | unresolved |
| matrix integral / partition function | integration domain, base measure, normalization, and finiteness | integrable measurable density and normalized real/complex quantity | candidate observable |
| deformation | exact time variables and deformed weight/potential | parameterized measure or integral with differentiability hypotheses | unresolved |
| integrable system | Toda hierarchy, Painleve equation, or another named system | concrete recurrence/ODE/PDE predicate with conventions | unresolved |
| "connection" | equality, recurrence, differential identity, or limiting correspondence | exact proposition and ordered binders | not supplied by metadata |
| tau function | source definition and normalization | concrete function satisfying the selected hierarchy identities | Adler-van Moerbeke candidate only |
| level/gap probability | ensemble, interval, scaling, and determinant formula | measurable event/CDF and concrete determinant or equivalent encoding | Tracy-Widom candidate only |
| asymptotics | finite-size identity versus scaling limit | exact filter, topology, and convergence predicate | unresolved |

## Human and machine boundary

A limited repository search located neighboring Lean-facing dossiers and legacy modules about
random matrices, Tracy-Widom phenomena, and integrable-system interfaces, but no target-specific
artifact for `THM-M-1561`. Those neighboring artifacts cannot select or prove this proposition.
Exhaustive pinned-mathlib and external Lean searches belong to anchor audit after the exact statement
is frozen.

Before `H0`, an independent reviewer must inspect the selected immutable primary edition, pinpoint
the theorem or displayed identities and pages, map every definition and assumption, check errata,
and approve each source-to-Lean row. Before statement credit, the selected claim must elaborate
without replacing a concrete ensemble by an assumed interface or weakening an identity into an
informal association.
