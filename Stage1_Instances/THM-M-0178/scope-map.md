# Scope map

## Included subject

- A Bochner/Weitzenbock identity relating a geometric Laplacian on differential forms or tensor
  fields to the rough connection Laplacian plus a curvature endomorphism.
- The specialization to harmonic sections, followed by a pointwise or integrated identity.
- A curvature sign hypothesis and the source-prescribed consequence, such as parallelness,
  vanishing, or a restriction on harmonic forms or Betti numbers.
- Compactness, boundary, orientation, regularity, dimension, degree, and connectedness assumptions
  exactly when required by the selected source theorem.

## Decisions required before statement freeze

"Bochner technique" can refer to several distinct results. The statement phase must select one
literal source theorem and fix whether the subject is harmonic one-forms, harmonic `p`-forms,
vector fields, or another bundle section; whether curvature means Ricci curvature or the full
Weitzenbock curvature operator; and whether the conclusion is parallelness, vanishing, or a Betti
number bound. It must also fix Laplacian and curvature sign conventions, inner-product normalization,
the integration measure, and all boundary terms.

## Explicit exclusions

- A generic slogan that positive curvature makes harmonic forms vanish.
- Bochner's theorem on positive-definite functions or Bochner integration in Banach spaces.
- A theorem assuming the desired Weitzenbock identity or vanishing conclusion as structure data.
- Substitution of the easier harmonic-function maximum principle for a theorem about forms.
- Credit from the manifest's untrusted `已验证` label or from adjacent differential-geometric APIs.

The later Lean statement must expose concrete manifold, Riemannian metric, differential-form or
bundle-section, connection, Laplacian, curvature, harmonicity, and integration interfaces. If the
pinned library lacks any of these, the statement phase must record the precise API blocker rather
than introduce uninterpreted replacements.
