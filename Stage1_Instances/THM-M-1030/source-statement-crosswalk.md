# Source-statement crosswalk

## Candidate primary sources

- Lester E. Dubins and Gideon Schwarz, "On Continuous Martingales," *Proceedings of the National
  Academy of Sciences of the United States of America* 53 (1965), 913-916. This is the primary
  joint paper candidate; exact theorem numbering, wording, assumptions, and corrections remain to
  be inspected from a stable scan.
- K. E. Dambis, "On the Decomposition of Continuous Submartingales," *Theory of Probability and
  Its Applications* 10 (1965), 401-410 (English translation metadata to be checked against the
  Russian original). This is an independent historical source candidate; exact edition and
  translation correspondence remain open.

These bibliographic records are discovery anchors, not `H0` evidence. The statement phase must
inspect the actual theorem and definitions, record pages/theorem identifiers and errata, and select
one normative formulation.

## Crosswalk

| Repository phrase | Intended source component | Required Lean component | Intake status |
|---|---|---|---|
| "continuous local martingale" | real process `M`, adapted and locally a martingale, with continuous paths and zero start | concrete filtration, local martingale, continuity, and `M 0 = 0` | included; exact source hypotheses open |
| "quadratic variation" | continuous increasing bracket `⟨M⟩` | constructed/characterized bracket, not caller-supplied truth | included; API open |
| "time change" | generalized inverse stopping times `T s` | infimum definition, stopping-time proof, endpoint convention | included; convention open |
| "is Brownian motion" | `B s = M (T s)` relative to the time-changed filtration | concrete standard Brownian predicate and time-changed filtration | included; formal encoding open |
| representation | `M t = B (⟨M⟩ t)` in the source's equality sense | checked inverse/composition theorem and null-set discipline | included; equality mode open |
| finite bracket | extension after `⟨M⟩∞` or an unboundedness hypothesis | terminal-time/space-extension construction or explicit divergence premise | source-dependent boundary |

## Existing Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_223.lean` is discovery evidence only. It confirms
adjacent mathlib interfaces for martingales, stopped processes, Gaussian processes, and independent
increments. Its local `ContinuousLocalMartingaleData` assumes `inverseQuadraticVariation`,
`quadraticVariationUnbounded`, and `terminalValueConvention` merely as propositions, while its
`StatementShape` assumes their conjunction before asserting Brownian motion. Thus it neither
constructs the bracket/inverse nor proves the theorem and receives no statement or proof credit.

Before `H0`, independent review must verify the selected primary text, definitions, all hypotheses,
translation/errata status, and every row of the source-to-Lean mapping. Anchor audit must separately
search the pinned mathlib revision and credible external Lean 4 projects.
