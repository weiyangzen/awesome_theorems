# Source-statement crosswalk

## Primary source anchor

Clifford S. Gardner, John M. Greene, Martin D. Kruskal, and Robert M. Miura, "Method for Solving
the Korteweg-de Vries Equation," *Physical Review Letters* 19 (1967), 1095-1097,
DOI `10.1103/PhysRevLett.19.1095`, is the historical primary publication anchor. It introduces the
scattering-data method and reconstruction route. Its compact physics presentation must not be
silently upgraded into a modern existence-and-uniqueness theorem with unstated function spaces.

The statement phase must inspect a stable copy and a rigorous primary theorem source for the full
analytic hypotheses, recording edition, theorem/page, assumptions, and errata. Until that audit and
independent review, this anchor supports `H2`, not `H0`.

## Crosswalk

| Repository/source phrase | Mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| inverse scattering transform | direct data followed by inverse reconstruction | typed direct/inverse scattering maps | included; domains open |
| KdV equation solution | reconstructed potential satisfies the normalized PDE | differentiability plus pointwise/weak KdV predicate | included; normalization open |
| associated Schrodinger problem | spectral problem for the Lax operator | self-adjoint operator and spectral/scattering interfaces | included; API open |
| time evolution of scattering data | explicitly evolved continuous and discrete data | evolution map and preservation obligations | included; conventions open |
| reconstruction | Marchenko-type integral equation recovers the potential | existence, uniqueness, and recovery theorem | included; formal encoding open |
| prescribed initial data | reconstructed solution agrees at initial time | initial-value equality in the frozen function space | included; topology open |

## Evidence boundary

The Stage0 and generated Stage1 labels `verified` are untrusted metadata. No repo-local Lean module,
external Lean closure, or exact theorem declaration has been identified at intake. Candidate search
belongs to anchor audit after exact statement elaboration. Before `H0`, a reviewer must approve the
source theorem/page, every hypothesis and normalization, the conclusion, errata search, and each
source-to-Lean row.
