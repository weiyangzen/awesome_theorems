# Source-statement crosswalk

## Candidate primary sources

- Salomon Bochner, "Vector fields and Ricci curvature," *Bulletin of the American Mathematical
  Society* **52** (1946), 776-797. This is a historical primary candidate consistent with the
  repository's date and curvature gloss.
- Salomon Bochner, "Curvature and Betti numbers," *Annals of Mathematics* **49** (1948), 379-390.
  This is a primary candidate for the harmonic-form/curvature consequences usually associated with
  the technique.

These bibliographic records are discovery anchors only. A stable scan, exact theorem/page or
display, all assumptions, definitions, and relevant corrections have not yet been inspected, so
they are not `H0` evidence. The difference between the metadata date and the later harmonic-form
paper is itself a reason not to guess the canonical theorem.

## Crosswalk

| Repository phrase | Source-side alternatives to resolve | Required Lean component | Intake status |
|---|---|---|---|
| "Bochner technique" | method, identity, or one vanishing theorem | one exact proposition, not a method label | unresolved |
| "harmonic forms" | degree one, arbitrary degree, or bundle-valued forms | concrete form degree and harmonicity predicate | included subject; degree open |
| "curvature" | Ricci tensor or Weitzenbock curvature endomorphism | source-normalized curvature action and sign | included subject; convention open |
| relation | pointwise identity, integrated identity, parallelness, or vanishing | explicit equality/implication and hypotheses | unresolved |
| global conclusion | vanishing of forms or Betti-number restriction | Hodge-theoretic bridge if source uses it | unresolved |

## Formal boundary

No existing Lean declaration is credited at intake. Repository-wide discovery shows nearby
Riemannian-manifold substrate and repeated reports that pinned mathlib may lack concrete Ricci and
Laplace-Beltrami interfaces; that observation is neither a complete anchor audit nor evidence for
the target. The anchor-audit phase must search the exact pinned source tree after the proposition is
selected and must distinguish substrate from a terminal theorem.

Before `H0`, an independent reviewer must verify the selected source copy, theorem/display and page,
ordered assumptions, conventions, proof scope, errata, and every row of the source-to-Lean mapping.
