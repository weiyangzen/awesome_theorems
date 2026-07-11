# Source-statement crosswalk

## Candidate primary source

W. Wolibner, "Un théorème sur l'existence du mouvement plan d'un fluide parfait, homogène,
incompressible, pendant un temps infiniment long", *Mathematische Zeitschrift* 37 (1933), 698-726,
is the primary candidate indicated by the repository name and two-dimensional Euler gloss. A
stable scan still must be inspected to identify the exact theorem/page, definitions, hypotheses,
and any corrections. This bibliographic identification alone is not H0.

The modern slogan "global existence for 2D Euler" is broader and less precise than the historical
statement. The statement phase may not silently replace Wolibner's domain, smoothness, boundary,
or formulation with a convenient modern torus/whole-plane theorem.

## Crosswalk

| Repository phrase | Intended source component | Required Lean component | Intake status |
|---|---|---|---|
| "Wolibner theorem" | a specific theorem in the 1933 paper | one exact theorem expression | family identified; theorem/page open |
| planar ideal fluid | source domain and homogeneous incompressible Euler motion | domain, velocity, pressure, spatial/time derivatives | included; conventions open |
| incompressibility | source divergence/volume-preservation condition | divergence-free predicate and boundary compatibility | included; encoding open |
| prescribed initial motion | source initial-data and regularity assumptions | initial trace plus concrete function-space membership | included; exact class open |
| infinitely long time | source global continuation/existence conclusion | solution quantified on the source-equivalent time domain | included; formulation open |
| classical motion | differentiability and equation satisfaction in the source sense | explicit solution predicate with regularity fields | included; exact regularity open |

## Evidence boundary

The repository supplies no accepted source excerpt or Lean declaration for this target. Before H0,
an independent reviewer must verify the stable edition, theorem and page, referenced definitions,
domain and boundary assumptions, regularity indices, uniqueness scope, and errata, then approve a
row-by-row source-to-Lean mapping. Before M-credit, the exact Lean target must elaborate; later
anchor work must inspect actual declarations and terminal proof bodies at immutable revisions.
