# Source-statement crosswalk

## Repository source boundary

`Docs/researches/math_theorems.md` attributes the label to Gaspard Monge and Andre-Marie Ampere,
dates it to 1807, and supplies only `完全非线性椭圆方程` (fully nonlinear elliptic equation). This is
a classification, not a theorem statement. No work, edition, page, theorem, assumptions, or errata
are provided. The historical names/date are discovery leads only and earn no human-proof status.

## Component crosswalk

| Metadata component | Missing mathematical choice | Required Lean surface | Intake state |
|---|---|---|---|
| "Monge-Ampere equation" | real `det D^2 u = f` or complex equation | coordinate Hessian/determinant or complex differential forms | open |
| "elliptic" | convex/admissible solution and positivity cone | explicit convexity or ellipticity predicate | open |
| domain | Euclidean domain or complex manifold | typed domain, topology, dimension | absent |
| solution | classical, Alexandrov, viscosity, pluripotential | exact solution predicate plus bridges | absent |
| data | density, measure, potential, boundary values | functions/measures and quantitative assumptions | absent |
| theorem conclusion | existence, uniqueness, estimate, or regularity | one proposition with explicit binders | absent |

## Discovery anchors, not accepted sources

The repository contains related legacy modules `S1_M_148.lean` through `S1_M_150.lean` for
Caffarelli regularity and `S1_M_130.lean` for a complex continuity-method package. Their own prose
describes missing terminal PDE infrastructure or package assumptions. They may guide later API
discovery, but they neither identify the intended THM-M-1179 proposition nor supply proof credit.

First actionable gate: inspect an actual primary mathematical source, select one exact theorem with
a page/theorem pinpoint, transcribe every hypothesis and conclusion, check definitions and errata,
and obtain independent approval of the source-to-Lean row mapping. Until then H0 and a canonical
formal target are unavailable.
