# Source-statement crosswalk

## Repository source record

`Docs/researches/math_theorems.md` attributes `THM-M-0582` to Grigori Perelman, dates it to 2002,
and describes it only as "a proof of the geometrization conjecture." `Docs/Stage0_Blueprint.md`
repeats that summary while leaving definitions, hypotheses, proof route, axioms, and formal
artifacts open. The rev-5.6 manifest calls its `已验证` label untrusted. These metadata identify the
topic, but do not fix an exact theorem or establish source fidelity or machine proof.

## Candidate primary sources

- William P. Thurston, *Three-Dimensional Geometry and Topology*, volume 1, edited by Silvio Levy,
  Princeton Mathematical Series 35, Princeton University Press (1997). This is a primary
  exposition of the geometric program and model geometries; the exact conjecture/theorem location
  and conventions have not been inspected in this intake.
- Grigori Perelman, "The entropy formula for the Ricci flow and its geometric applications,"
  arXiv:math/0211159 (2002).
- Grigori Perelman, "Ricci flow with surgery on three-manifolds," arXiv:math/0303109 (2003).
- Grigori Perelman, "Finite extinction time for the solutions to the Ricci flow on certain
  three-manifolds," arXiv:math/0307245 (2003).

The Perelman preprint series is primary proof evidence, but this intake has not yet selected an
exact terminal formulation or mapped every proof component across the three papers. The references
therefore support only `H1`, not `H0`. Later source work must inspect immutable versions, locate the
relevant statements and pages/sections, resolve subsequent corrections or clarifications, and
obtain independent review. A secondary reconstruction may help navigation but cannot replace the
primary-source crosswalk.

## Crosswalk

| Repository/source phrase | Frozen mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "three-manifold" | closed, connected, orientable manifold of dimension three | concrete manifold structures and dimension witness | included; category and binder encoding open |
| prime decomposition | split reducible `M` into prime factors and reconstruct by connected sum | embedded spheres, cutting/capping, connected sum, existence/uniqueness | included; API open |
| JSJ decomposition | cut irreducible factors along incompressible tori | embedded incompressible tori, finite disjoint family, cut pieces | included; exact canonicality clause open |
| eight geometries | locally homogeneous models for each geometric piece | definitions of the eight model geometries and geometric structures | included; equivalence conventions open |
| "geometrization" | every resulting piece is geometric | complete/finite-volume quotient or locally homogeneous metric predicate | included; boundary formulation open |
| Perelman proof | Ricci flow, singularity analysis, surgery, long-time behavior, extinction | analytic flow/surgery objects and a checked classification bridge | proof route identified; formal APIs open |
| exceptional cases | spherical, Seifert-fibered, graph-manifold, and reducible behavior as required | explicit branches composing to the universal result | included in principle; source partition open |

## Lean discovery boundary

The repository contains no target-owned legacy module for `THM-M-0582`. The adjacent historical
module `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_128.lean` concerns Perelman's theorem and
imports mathlib's Poincare-conjecture surface. It explicitly models geometrization with an abstract
`GeometrizationPackage` whose fields stand for prime decomposition, JSJ decomposition, Thurston
pieces, Ricci flow with surgery, and the final implication. That package assumes rather than
defines or proves the terminal content, so it is discovery evidence only.

The later anchor-audit phase must repeat repository, pinned-mathlib, and credible external Lean 4
searches at immutable revisions and record exact declarations, types, bodies, axioms, provenance,
and dependency feasibility. This intake does not claim that the historical negative search proves
that no formalization exists.

Before the statement gate can close, an inspected source formulation must be mapped row by row to
one canonical Lean proposition. The map must account for reducible and exceptional cases,
orientability and boundary conventions, the exact meaning of "geometric," and checked transports
between any decomposition and Ricci-flow formulations.
