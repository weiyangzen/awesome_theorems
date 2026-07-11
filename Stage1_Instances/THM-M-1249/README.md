# THM-M-1249 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the metadata label "distribution theory"
(`分布理论`). The inherited Stage0 text, "the theory of generalized functions," names a subject rather
than a single proposition. This intake preserves that ambiguity rather than silently replacing it with a
convenient theorem.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Historical subject | Schwartz distributions as continuous linear functionals on a test-function space | A primary-source pinpoint and an exact theorem have not been selected |
| Candidate objects | test functions, continuous linear functionals, distributional derivatives, regular distributions | These are discovery families, not an asserted conjunction or theorem |
| Candidate Lean representation | continuous linear maps from a locally convex test-function space to the scalar field | No module, declaration, topology, scalar field, or domain dimension is frozen |
| Operations | linearity, differentiation by transposition, embedding locally integrable functions | Each could support a later exact target, but none is credited here |
| Exclusions | Schwartz space itself (`THM-M-1250`), a particular PDE existence theorem, tempered distributions unless explicitly selected | Neighboring subjects cannot be substituted for this target |
| Foundations | Lean 4 kernel with a later pinned mathlib environment | Foundation, TCB, and computation profiles remain open |

The next statement phase must resolve the subject-label ambiguity from a primary source and freeze one
literal proposition with its domains, topology, scalar field, ordered binders, hypotheses, and conclusion.
Until then, mutation tests and alternate-encoding transports are not meaningful.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H2, M4, R3]`. `H2` records that a primary
foundational source is identified but not yet pinpoint-crosswalked. `M4` records that no exact Lean
proposition can truthfully be elaborated from the supplied metadata. The first failed gate is exact
statement identification. No source label, candidate API, or historical mathematical development is
treated as kernel closure, and the theorem is not complete.

## Validation

The commands and exact results in `validation.md` establish manifest membership, rev-5.6 structural
consistency, JSON syntax, and dossier-local hygiene only. Master acceptance and all dependent phases
remain outstanding.
