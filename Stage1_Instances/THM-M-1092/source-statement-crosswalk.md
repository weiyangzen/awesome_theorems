# Source-statement crosswalk

## Candidate primary sources

- A. N. Kolmogorov, "Uber die analytischen Methoden in der Wahrscheinlichkeitsrechnung",
  *Mathematische Annalen* 104 (1931), 415-458. This is the historical primary paper candidate.
  Its precise equation numbering, hypotheses, and the distinction between density and transition
  probability formulations have not yet been inspected against a stable scan.
- E. B. Dynkin, *Markov Processes*, volumes I-II, Springer (1965), the transition-function and
  infinitesimal-operator chapters. This is a classical proof-source candidate; exact volume,
  theorem/page, edition/translation wording, and errata remain to be audited.

These are discovery anchors, not `H0` evidence. The statement phase must select a stable edition and
exact theorem rather than reconstruct assumptions from the theorem name or from the legacy wrapper.

## Crosswalk

| Repository phrase | Intended source component | Required Lean component | Intake status |
|---|---|---|---|
| "transition density differential equations" | differentiable transition law/density | Markov kernel or density family plus derivative | included; representation open |
| backward equation | generator acts on initial-state/test-function side | generator domain and left action | included; convention open |
| forward equation | generator/adjoint acts on terminal-state/distribution side | right action or adjoint on measures/densities | included; adjoint hypotheses open |
| Markov transition family | positivity, mass, measurability, semigroup law | concrete kernel/semigroup structure | included; state space open |
| initial condition | identity/Dirac transition at zero time | checked `P 0 = id` encoding | included |
| regularity | permits the asserted derivatives and interchange steps | explicit continuity, domain, and integrability assumptions | required; exact list open |

## Existing Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_216.lean` records useful candidate object models,
mathlib substrate, and a prior search ledger. Its `KolmogorovConclusion` stores the two equations as
fields and `StatementShape` concludes that supplied package, so it does not prove the source result.
Its discrete-time kernel-power wrapper establishes Chapman-Kolmogorov substrate only. All searches,
imports, declaration types, terminal bodies, and toolchain facts must be repeated at the pinned
rev-5.6 environment during anchor audit.

Before `H0`, an independent reviewer must verify the selected source edition, theorem/equation and
page, all assumptions, notation conventions, errata, and every row of the source-to-Lean mapping.
