# THM-M-1306 rev-5.6 intake

This is the `planned` intake for the metadata label "Chemin theorem". The repository's only claim
is the Chinese phrase `Euler方程的解析性` ("analyticity of the Euler equations"), attributed to
Jean-Yves Chemin and dated 1990. That phrase does not uniquely determine a theorem. The intake
therefore freezes the ambiguity rather than silently choosing a nearby persistence, propagation,
spatial-analyticity, or Lagrangian-analyticity result.

## Scope map

| Surface | Intended scope | Open boundary |
|---|---|---|
| Equation | Incompressible Euler is suggested by the label | Dimension, spatial domain, boundary conditions, Eulerian/Lagrangian formulation, and solution notion are absent |
| Analytic object | Some analyticity property of a solution or flow | Analyticity in space, time, labels, trajectories, or an analytic/Gevrey class is not distinguished |
| Input assumptions | Initial data and a solution existence interval are necessarily relevant | Regularity, divergence-free condition, pressure normalization, topology, and lifespan are absent |
| Output | Persistence or emergence of analyticity is a plausible family | Radius estimates, loss/growth laws, and endpoint/breakdown behavior are absent |
| Human source | A result attributed to Jean-Yves Chemin around 1990 | No title, edition, theorem number, page, assumptions, or errata record is supplied |
| Lean surface | Lean 4 is the required backend | No exact `Prop`, import, PDE model, or candidate declaration is identified |

These omissions are mathematically material: choosing values for them would substitute a theorem.
The dependent statement phase must first identify a primary source and bind every row above to a
pinpoint theorem before elaborating Lean.

## Intake verdict

Lifecycle remains `planned`; the provisional root vector is `[H4, M4, R4]`. The first failed gate
is exact source-statement identification, before the Lean statement gate. The historical
`已验证` label is explicitly untrusted metadata and provides no human or machine proof credit.
The theorem is not complete.

## Validation

The commands and results in `validation.md` establish target membership, standard consistency,
JSON syntax, and dossier-local structural checks only. They do not validate a theorem statement.
