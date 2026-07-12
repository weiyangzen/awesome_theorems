# Source-statement crosswalk

Item: `S56-M-0159-INTAKE`.

## Repository record

`Docs/Stage0_Blueprint.md` describes `THM-M-0159` as the compatibility conditions for the
fundamental forms of a surface, assigns the year 1857, and attributes the equations collectively to
Gauss, Codazzi, and Mainardi. `Docs/researches/math_theorems.md` repeats the name and attribution.
The target manifest carries the untrusted label `已验证`. These records identify a theorem family,
but provide no formula, hypotheses, source edition, page, convention, or formal declaration.

## Source candidates requiring inspection

- Manfredo P. do Carmo, *Differential Geometry of Curves and Surfaces*, the chapter on intrinsic
  geometry of surfaces and the Gauss and Mainardi-Codazzi equations.
- Michael Spivak, *A Comprehensive Introduction to Differential Geometry*, volume III, the
  treatment of the fundamental equations of surface theory.

These are stable modern proof-source candidates, not accepted primary-source evidence. Exact
edition, theorem/page, displayed formula, assumptions, errata, and historical provenance remain to
be inspected. Consequently this intake assigns `H1`, not `H0`.

## Component crosswalk

| Repository/source phrase | Frozen intended component | Required Lean component | Intake assessment |
|---|---|---|---|
| surface | smooth two-manifold immersed in oriented Euclidean `R^3` | manifold, immersion, tangent maps, Euclidean metric | intended domain fixed; exact model open |
| first fundamental form | metric induced by the immersion | pullback/induced Riemannian metric and Levi-Civita connection | included; API and binders open |
| second fundamental form | normal component of the ambient derivative | local unit normal, shape operator or symmetric covariant `2`-tensor | included; sign convention open |
| compatibility conditions | identities necessarily satisfied by the induced pair | conjunction of exact Gauss and Codazzi propositions | necessity direction fixed; no converse credit |
| Gauss equation | intrinsic curvature equals a quadratic expression in `h` | Riemann curvature tensor and tensor contractions/evaluation | slot and curvature signs open |
| Codazzi-Mainardi equation | covariant derivative of `h` is symmetric in its first two inputs | covariant derivative of a covariant tensor | exact regularity and API open |

## Statement boundary

The phrase "compatibility conditions" is sometimes used inside the fundamental theorem of surface
theory, where an abstract metric and second form satisfying Gauss-Codazzi are sufficient for a local
immersion. That converse has additional domain, regularity, topology, and uniqueness qualifications
and belongs to adjacent target `THM-M-0160`; it is excluded from this root unless a later source
audit proves that the catalogue intended the biconditional and the target is formally re-frozen by
the authorized lane.

Before `H0`, an independent reviewer must verify an immutable source edition, formula and page,
every hypothesis and convention, errata, and a row-by-row source-to-Lean map. Before any machine
credit, the statement phase must elaborate the exact conjunction and mutation-test omission of
immersion, metric induction, normal compatibility, and either equation.
