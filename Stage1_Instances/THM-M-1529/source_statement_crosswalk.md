# Source-statement crosswalk

| Source surface | Exact content | Proposition-level assessment |
|---|---|---|
| `Docs/Stage0_Blueprint.md`, `THM-M-1529` | Name `杨-米尔斯理论`; content `非阿贝尔规范场论`; proposed in 1954; definitions, assumptions, proof, date, and dependencies all `待补充` | A theory/topic description, not a truth-valued statement |
| `Docs/Stage1_Blueprint.md`, `S1-M-197` | Repeats the name/content and proposes axiomatic statements, operator/space definitions, spectral or variational sublemmas, and special-parameter cases | A menu of possible formalization work; it does not select a root theorem |
| `Docs/Stage1_Targets_rev-5.6.json` | Metadata status `已验证`, lane `hard_mathlib_anchor_and_wrapper`, lifecycle `planned` | Membership/scheduling metadata only; explicitly untrusted and no proof credit |
| Clay Yang-Mills and mass gap | A distinct candidate commonly associated with the phrase "Yang-Mills" | Not adopted: the repository has a separate `杨-米尔斯存在性与质量间隙` record, and substituting it here would broaden/change this target |
| Classical or ASD Yang-Mills results | Possible theorems about equations, critical connections, or (anti-)self-dual fields | Not adopted: each requires model-specific hypotheses absent from the source record |

## Missing statement map

| Required component | Source value | Gate consequence |
|---|---|---|
| Gauge group/representation | absent | domains cannot be frozen |
| Base geometry and dimension | absent | connection, curvature, Hodge star, and analytic spaces are undetermined |
| Classical/Euclidean/Lorentzian/quantum regime | absent | the mathematical object and foundation boundary are undetermined |
| Regularity and boundary/finite-action assumptions | absent | quantifiers and hypotheses cannot be written |
| Claimed conclusion | absent | there is no proposition to elaborate |

The source label `已验证` cannot repair these omissions. Intake therefore stops before source
research, Lean anchor credit, transports, mutation tests, or proof architecture. A later statement
phase may proceed only after the retry condition in `intake.json` is met and independently reviewed.
