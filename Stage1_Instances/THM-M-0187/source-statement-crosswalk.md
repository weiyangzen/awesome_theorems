# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md` supplies the Chinese title, Aleksandr Aleksandrov attribution,
the year 1942, and the statement `常高斯曲率闭曲面的唯一性` ("uniqueness of closed surfaces of
constant Gaussian curvature"). `Docs/Stage0_Blueprint.md` repeats those fields but leaves precise
definitions, assumptions, proof route, axioms, and artifacts open. Its `已验证` value is untrusted
metadata under rev-5.6 and supplies neither a source receipt nor a proof term.

The name, attribution/year, and gloss point toward different classical results. Accordingly, this
intake does not invent an exact citation or choose a theorem by resemblance.

## Discovery-only source candidates

- H. Liebmann's classical work on closed surfaces of constant Gaussian curvature is the historical
  source family that most closely matches the repository gloss. An immutable edition, exact title,
  theorem/page, assumptions, and any modern translation must be located and reviewed.
- A. D. Aleksandrov's uniqueness theorems for closed convex surfaces are a candidate family for the
  supplied attribution and period. The exact 1942 work and proposition must be inspected to decide
  whether the intended data are intrinsic metric, curvature measure, or another convex-surface
  invariant.
- A. D. Aleksandrov's moving-planes theorem for compact embedded constant-mean-curvature
  hypersurfaces is a candidate for the familiar English theorem name, but it is not admissible
  without correcting both the curvature notion and historical locator.

These are search leads only, not pinpoint primary sources and not `H0` evidence. No theorem/page,
edition wording, assumption list, errata record, or independent review is claimed here.

## Crosswalk

| Repository field | Candidate mathematical meaning | Required Lean component | Intake status |
|---|---|---|---|
| "closed surface" | compact without boundary; possibly also connected and embedded | concrete manifold/surface model, compactness, boundary, connectedness, immersion/embedding | unresolved |
| "constant Gaussian curvature" | pointwise constant intrinsic/extrinsic Gaussian curvature, likely positive in the spherical rigidity result | curvature definition, differentiability, quantified constant and sign conventions | wording preserved; exact hypotheses open |
| "uniqueness" | sphere classification, congruence up to rigid motion, or uniqueness from prescribed intrinsic data | exact equality/isometry/congruence relation and ordered quantifiers | unresolved |
| "Aleksandrov / 1942" | a convex-surface existence or uniqueness result | exact source theorem and convexity/data interfaces | candidate attribution; locator open |
| `已验证` | repository status label | no source proof or kernel object | no credit |

## Lean discovery boundary

A bounded repository and pinned-mathlib text search found no theorem-specific artifact for
`THM-M-0187` and no declaration recognizable by the candidate theorem names. The `Aleksandrov`
hits in existing Stage1 modules concern Monge-Ampere weak solutions, not this surface-rigidity
target. This observation is intake discovery only; it is not an exhaustive immutable candidate or
provenance audit and does not establish absence from Lean projects generally.

Before `H0`, an independent reviewer must select and inspect an immutable primary edition, record
the exact theorem/page and translation, map every assumption and conclusion, inspect errata, and
resolve the attribution/gloss conflict. Before statement credit, that approved proposition must be
mapped row by row to an elaborated Lean expression without changing its curvature notion, global
scope, regularity, convexity, or uniqueness relation.
