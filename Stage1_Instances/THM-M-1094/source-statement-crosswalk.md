# Source-statement crosswalk

## Candidate primary sources

- A. N. Kolmogorov, "Ueber die analytischen Methoden in der Wahrscheinlichkeitsrechnung",
  *Mathematische Annalen* 104 (1931), 415-458. This is the historical primary paper candidate for
  the differential equations of transition probabilities. Its exact backward-equation number,
  hypotheses, notation, and any errata have not yet been checked against an immutable scan.
- E. B. Dynkin, *Markov Processes*, volumes I-II, Springer (1965), the chapters on transition
  functions and infinitesimal operators. This is a classical proof-source candidate, but the exact
  volume, theorem/page, translation wording, and errata remain to be audited.

These entries are discovery anchors, not `H0` evidence. The statement phase must select and inspect
one exact theorem rather than reconstruct missing assumptions from the theorem name.

## Crosswalk

| Repository phrase | Intended source component | Required Lean component | Intake status |
|---|---|---|---|
| "evolution equation for transition probabilities" | differentiable time evolution of a Markov transition law | time-indexed transition operator, kernel, matrix, or density plus derivative | included; representation open |
| backward equation | generator acts on the initial-state variable | generator action in `x`, or the checked operator-equivalent form | included; convention open |
| infinitesimal generator | limit of short-time transition evolution on a domain | concrete operator and generator-domain predicate | required; encoding open |
| Markov transition family | positivity, total mass, measurability, and composition | concrete Markov kernel/semigroup structure | included; state space open |
| initial condition | identity or Dirac transition at zero time | checked `P_0 = id` encoding | included |
| regularity | justifies the derivative and generator interchange | explicit continuity, domain, integrability, and boundary assumptions | required; exact list open |

## Existing Lean boundary

No legacy priority slot or target-specific Lean file is recorded for `THM-M-1094`. The related
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_216.lean` for `THM-M-1092` is only discovery
evidence. Its `BackwardEquation` is an intended shape over freely supplied generator data, while
its terminal conclusion stores that equation as a field. Its checked kernel-power theorem is
discrete-time Chapman-Kolmogorov substrate, not the continuous-time backward equation.

All candidate imports, declarations, terminal bodies, and toolchain facts must be audited afresh in
the pinned rev-5.6 environment. Before `H0`, an independent reviewer must verify the selected source
scan, equation/theorem and page, every hypothesis and notation convention, errata, and every row of
the source-to-Lean mapping.
