# Source-statement crosswalk

## Available source record

`Docs/researches/math_theorems.md` supplies only the title "Dirichlet problem", attribution to Peter
Dirichlet, date 1850, the phrase "the boundary-value problem for Laplace's equation", importance
"high", and the untrusted label `已验证`. `Docs/Stage0_Blueprint.md` repeats this metadata and leaves
definitions, hypotheses, proof route, axioms, and machine artifacts open. No bibliography, edition,
theorem number, page, or errata record is attached.

This describes a problem family rather than one proposition. No primary-source candidate is
asserted at intake, because choosing a modern existence or uniqueness theorem would invent scope.

## Crosswalk

| Source element | Mathematical information fixed | Lean information required | Intake result |
|---|---|---|---|
| "Laplace equation" | harmonic/Laplace operator family | domain, Laplacian, solution notion | unresolved |
| "Dirichlet" | prescribed boundary values | boundary/trace API and data function | unresolved |
| "boundary-value problem" | seek a solution satisfying PDE and boundary data | exact hypotheses and conclusion | unresolved |
| Peter Dirichlet / 1850 | historical attribution metadata | none | insufficient to identify a theorem |
| `已验证` | untrusted repository label | inspectable human proof or kernel receipt | no credit |

## Statement boundary

Standard modern formulations vary sharply with domain and boundary regularity and may express
solutions classically, weakly, variationally, by harmonic measure, or by a Poisson kernel. Those are
scoping observations, not the canonical claim. The statement phase must locate a primary,
pinpointed theorem and map its topology, regularity, trace convention, uniqueness conditions, and
boundary behavior row by row before Lean elaboration. Independent review is required before `H0`.
