# Source-statement crosswalk

## Primary-source candidates

The repository label most directly traces to Gerard 't Hooft, "Dimensional Reduction in Quantum
Gravity" (1993), arXiv `gr-qc/9310026`, and Leonard Susskind, "The World as a Hologram",
*Journal of Mathematical Physics* 36 (1995), 6377-6396, DOI `10.1063/1.531249`. These formulate
the principle and motivation, but intake has not identified in them a theorem with a source-exact
Lean-ready quantifier structure.

Juan Maldacena, "The Large N Limit of Superconformal Field Theories and Supergravity",
*Advances in Theoretical and Mathematical Physics* 2 (1998), 231-252, arXiv
`hep-th/9711200`, is a primary candidate for the AdS/CFT branch. It presents a conjectured duality
and limits/examples, not by citation alone a proof of an unconditional holographic principle.
Stable copies, exact pages/equations, referenced definitions, version differences, and errata must
be inspected during statement/source audit. Bibliographic identification is not H0.

## Crosswalk

| Repository phrase | Source component to select | Required Lean component | Intake status |
|---|---|---|---|
| holographic principle | one model-specific proposition, not the slogan | one closed `Prop` with explicit binders | family frozen; exact proposition open |
| quantum gravity in a bulk region | a fixed bulk theory/regime and admissible states | typed bulk model and hypotheses | included; model open |
| boundary theory | a fixed CFT/operator algebra and boundary geometry | typed boundary model and state/observable class | included; model open |
| encoded by the boundary | source-defined dictionary/equivalence/reconstruction | explicit map plus injectivity, inverse, or observable equality | meaning open |
| entropy/area | specified bound or asymptotic formula with constants | geometric area, entropy, units, hypotheses, equality/error notion | optional branch; normalization open |
| correlator agreement | specified operators, states, and approximation regime | well-typed correlators and exact/asymptotic equality | optional branch; regime open |

## Evidence boundary

The Stage0 words "quantum gravity and boundary theory" and status "partially verified" are
untrusted discovery metadata. The legacy Lean module supplies no accepted source correspondence or
terminal holography proof. H0 requires edition/theorem-or-equation/page/assumption/errata mapping and
independent review. M-credit requires an exact elaborated target and later inspection of real proof
bodies and their transitive trust closure at immutable revisions.
