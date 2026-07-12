# Source-statement crosswalk

## Available repository source

`Docs/researches/math_theorems.md` records only the title, attribution to "many mathematicians",
twenty-first-century date, phrase `KPZ普适类`, importance, and `已验证`. `Docs/Stage0_Blueprint.md`
repeats those fields while leaving exact definitions, premises, proof route, equivalent forms,
axioms, and machine artifacts open. These records establish the intake phrase's repository
provenance, not a unique mathematical claim or proof status.

## Candidate primary-source boundaries

- Mehran Kardar, Giorgio Parisi, and Yi-Cheng Zhang, "Dynamic Scaling of Growing Interfaces",
  *Physical Review Letters* 56 (1986), 889-892, DOI `10.1103/PhysRevLett.56.889`, is the historical
  origin of the equation and scaling prediction. It is not by itself a rigorous blanket theorem
  establishing the modern KPZ universality class.
- Konstantin Matetski, Jeremy Quastel, and Daniel Remenik, "The KPZ fixed point",
  *Acta Mathematica* 227 (2021), 115-203, DOI `10.4310/ACTA.2021.v227.n1.a3`, is a candidate
  model-specific primary theorem source for convergence of TASEP height fluctuations to the KPZ
  fixed point. The exact theorem/page, initial-data space, topology, normalization, hypotheses, and
  corrections must be inspected before it can define the canonical claim.

The second source is a plausible rigorous representative of one universality result, not evidence
for every model called KPZ. Intake does not promote either citation to `H0`.

## Crosswalk

| Repository/source phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "KPZ universality class" | a family of models sharing `1:2:3` fluctuation scaling and limiting statistics | an explicitly bounded model predicate or one named model | phrase is not a quantified proposition |
| microscopic growth model | TASEP or another source-selected dynamics | probability space, stochastic dynamics, and height/current observable | exact model open |
| `1:2:3` scaling | source-fixed time/space/height rescaling with centering constants | indexed rescaled random functions | constants and convention open |
| universal limit | KPZ fixed point, Airy process, or Tracy-Widom marginal | constructed probability law or stochastic process | alternatives are not interchangeable |
| convergence | distributional or process convergence | weak convergence or law convergence in a fixed topology | mode and state space open |
| general initial data | a source-defined admissible initial-profile class | typed hypotheses and initial-data embedding | source restrictions open |
| `已验证` | untrusted inventory label | no kernel evidence | no proof credit |

## Source and machine boundary

No theorem-specific Lean artifact or repo-local declaration was identified by the repository intake
search. That narrow observation is not the dependency-ordered anchor audit and does not prove that
no external formalization exists. Before `H0`, an independent reviewer must verify a stable primary
source copy, pinpoint theorem/pages, all assumptions and definitions, proof boundary, errata, and
the precise relationship between the selected model-specific theorem and the broad repository
label. Before statement credit, each approved component must map to an elaborated Lean expression;
alternate limits or convergence modes require checked transports rather than prose equivalence.
