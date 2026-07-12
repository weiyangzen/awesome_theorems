# Source-statement crosswalk

## Supplied repository evidence

The authoritative target manifest supplies the Chinese name `KPZ方程`, category
`其他重要领域 / 数学物理`, and the explicitly untrusted source status `已验证`. The Stage0 record
adds only the authors Kardar/Parisi/Zhang, the year 1986, and the gloss `随机表面生长`; it marks
precise definitions, premises, proof route, dependencies, axioms, and machine artifacts as open.
The research catalogue repeats the same metadata. None is an exact theorem statement.

## Primary discovery anchor

Mehran Kardar, Giorgio Parisi, and Yi-Cheng Zhang, "Dynamic Scaling of Growing Interfaces",
*Physical Review Letters* **56** (1986), 889-892, DOI
`10.1103/PhysRevLett.56.889`, is the primary historical source candidate for the equation. This
citation identifies the model's origin; it has not been admitted as `H0`, and this intake does not
claim that the article states the later mathematical existence, uniqueness, or renormalized-solution
theorem intended by the repository.

## Crosswalk

| Repository component | Source-side meaning | Required Lean component | Intake status |
|---|---|---|---|
| `KPZ方程` | stochastic nonlinear surface-growth model | a concrete stochastic evolution equation | subject identified; exact equation conventions open |
| Kardar/Parisi/Zhang, 1986 | historical model origin | bibliographic provenance only | primary discovery anchor identified |
| `随机表面生长` | physical interpretation of a height field | typed state space and stochastic process | gloss only; not a proposition |
| `已验证` | catalogue label | no corresponding declaration or receipt | untrusted; zero proof credit |
| theorem conclusion | absent from repository wording | exact `Prop` with ordered binders | blocked |
| proof/source assumptions | absent from repository wording | domains, noise, data, solution and renormalization hypotheses | blocked |

## Identity blocker and retry condition

"The KPZ equation" can denote the model definition, a well-posedness theorem for a selected
solution concept, a Cole-Hopf construction in one space dimension, approximation/renormalization
convergence, or a universality statement. These claims are inequivalent. In particular, the
separately scheduled `THM-M-1564` covers KPZ universality and must not be folded into this target.

An accountable source review must select an immutable source and exact theorem/page, record all
assumptions and relevant errata, and state why that theorem is the repository's intended claim.
Independent review must then approve a row-by-row source-to-Lean mapping. Only afterward can the
statement phase freeze a canonical expression and assess mathlib or external Lean candidates.
