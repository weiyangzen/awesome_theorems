# Source-statement crosswalk

## Candidate primary sources

- Joseph Liouville, "Note sur l'integration des equations differentielles de la Dynamique,"
  *Journal de Mathematiques Pures et Appliquees* 20 (1855), 137-138. This is a historical source
  candidate for integration by commuting first integrals; its precise relationship to the modern
  geometric statement still requires inspection.
- V. I. Arnold, *Mathematical Methods of Classical Mechanics*, 2nd edition, Springer (1989), the
  section on integrable systems and action-angle variables. This is the candidate source for a
  stable modern statement; exact theorem/page, translation wording, hypotheses, and errata remain
  to be inspected.

These are discovery anchors, not `H0` evidence. Selection and row-by-row verification are downstream
work; no statement details are inferred merely from the theorem name.

## Crosswalk

| Repository phrase | Intended component | Required Lean component | Intake status |
|---|---|---|---|
| "completely integrable Hamiltonian system" | `n` independent commuting integrals on a `2n`-dimensional phase space | symplectic manifold, smooth functions, Poisson bracket, differential independence | family included; conventions open |
| regular common level | fiber at a regular value/component | common level set and rank/linear-independence predicate | included; encoding open |
| invariant torus | compact connected regular component preserved by flows | invariant submanifold and diffeomorphism to an `n`-torus | included; exact conclusion open |
| action-angle variables | canonical coordinates near the regular torus | symplectic local chart and normal-form equations | included only if selected source supports it |
| integrability by quadratures | reconstruction of motion | explicit flow/quadrature conclusion | not yet included; source decision required |

## Existing-source boundary

The repository metadata supplies only a short topic label, says that many mathematicians are the
source, and leaves assumptions and proof history open. It cannot identify one exact proposition.
The Stage1 prose narrows the topic to completely integrable Hamiltonian systems but still does not
fix a theorem. Consequently `H0`, an exact Lean statement, and proof credit remain unavailable.

Before `H0`, an independent reviewer must verify a stable edition, theorem/page, definitions,
assumptions, coefficient/regularity conventions where applicable, errata, and every source-to-Lean
row. The statement phase must reject rather than weaken the target if that inspection does not
support the frozen theorem family.
