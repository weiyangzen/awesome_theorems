# THM-M-1313 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the singularity theorem entry. The source
metadata is not itself proof evidence: its Chinese label is generic, while the listed authors and
1965 date most closely identify Penrose's 1965 gravitational-collapse theorem. This intake fixes
that interpretation provisionally and records the ambiguity rather than silently substituting a
different Hawking-Penrose theorem.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Historical referent | Penrose's 1965 incomplete-null-geodesic conclusion | Confirmation by a pinpoint primary-source audit remains open |
| Geometric setting | time-oriented Lorentzian spacetime with a noncompact Cauchy hypersurface | Exact smoothness, dimension, connectedness, and causality APIs remain statement work |
| Hypotheses | null convergence/energy condition and a closed trapped codimension-two surface | Sign conventions and formal definitions are not frozen yet |
| Conclusion | the spacetime is not future null-geodesically complete | This is incompleteness, not the existence of a curvature-divergent point |
| Exclusions | Hawking 1966 cosmological theorem, Hawking-Penrose 1970 theorem, cosmic censorship | No alternate theorem receives proof credit |
| Formalization | a future Lean 4 axiomatization of Lorentzian causal/geodesic geometry | No repo-local Lean declaration has been identified or credited at intake |

The statement must not be weakened to a finite-dimensional linear-algebra analogue or to a
pre-assumed incomplete geodesic. The dependent statement phase must settle the source ambiguity
before elaborating a canonical target.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H2, M4, R3]`. The first failed gate is exact
source-statement identification: the repository description says only "singularities in general
relativity" / "gravitational collapse necessarily produces singularities." Consequently no exact
Lean statement, proof closure, or theorem completion is claimed.

## Validation

`validation.md` records the exact local checks. They establish manifest membership, repository
standard consistency, JSON syntax, and dossier-local reference integrity only.
