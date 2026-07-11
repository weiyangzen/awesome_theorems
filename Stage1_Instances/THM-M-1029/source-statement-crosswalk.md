# Source-statement crosswalk

## Candidate primary sources

- Paul Levy, *Processus stochastiques et mouvement brownien*, Gauthier-Villars (1948). This is the
  historical primary monograph candidate; the exact edition, theorem/page, hypotheses, and errata
  have not yet been inspected.
- Daniel Revuz and Marc Yor, *Continuous Martingales and Brownian Motion*, Springer, 3rd edition
  (1999), Chapter IV. This is a stable modern source candidate for Levy's characterization, but an
  exact proposition/page and correction check remain open.

These are discovery anchors, not `H0` evidence. The source label `已验证` in the generated legacy
metadata is explicitly untrusted and supplies no source or machine-proof credit.

## Crosswalk

| Human claim component | Intended formal component | Legacy Lean candidate | Intake assessment |
|---|---|---|---|
| filtered probability space | probability measure and filtration, with source side conditions | `Measure Ω`, `Filtration Time _` | included; usual conditions and probability assumption open |
| real continuous adapted process starting at zero | process, adaptation, path regularity, initial condition | fields of `LevyMartingaleInput` | included; a.s./pointwise convention open |
| `X` is a martingale | martingale relative to the same filtration and measure | `processMartingale` | candidate API only |
| `X_t^2 - t` is a martingale | compensated-square martingale | `quadraticMartingale` | candidate API only |
| `X` is standard Brownian motion | Gaussian increments of variance `t-s`, independent of the past, continuity, zero start | `RepoLocalBrownianMotion` / `LevyBrownianConclusion` | exact conclusion API open; no proof credit |

The historical module
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_222.lean` is discovery input. Its
`StatementShape` concludes an abstract package containing proposition fields and is explicitly
marked non-terminal. The statement phase must compare it with the inspected source, elaborate a
non-circular exact target, serialize its normalized expression, and mutation-test domains,
hypotheses, filtration dependence, and boundary cases.

Before `H0`, an independent reviewer must verify the chosen source edition and pinpoint, all
assumptions and definitions, errata, and every row of the source-to-Lean mapping.
