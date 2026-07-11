# THM-M-1193 rev-5.6 intake

This is the `planned` dossier for the Li-Yau differential Harnack estimate. The source label
"positive-solution gradient estimate" is not by itself a theorem: it omits the heat equation,
geometry, curvature, time interval, and normalization. This intake fixes the standard
nonnegative-Ricci-curvature scalar form; stronger lower-curvature and integrated Harnack forms are
not silently substituted.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Root | `|grad u|^2 / u^2 - (partial_t u) / u <= n / (2t)` | Exact Lean expression and sign conventions remain open |
| Geometry | Complete `n`-dimensional Riemannian manifold with `Ric >= 0` | No boundary, weighted, nonsmooth, or time-dependent metric variant |
| Solution | Positive smooth scalar solution of `partial_t u = Delta u` on `M x (0,T]` | No weak solution or heat-kernel singular initial datum |
| Parameters | `n > 0`, `T > 0`, `x in M`, and `0 < t <= T` | The singular endpoint `t = 0` is excluded |
| Equivalent notation | `|grad log u|^2 - partial_t(log u) <= n/(2t)` | Transport requires positivity and checked logarithmic calculus |
| Related results | Integrated parabolic Harnack inequality and heat-kernel bounds | Consequences only; not alternate roots |
| Foundations | Lean 4 kernel plus pinned mathlib differential geometry/analysis | Imports, analytic feasibility, axioms, and TCB fingerprint remain open |

The structured claim and exclusions are in `intake.json`; source genealogy and statement mapping
are in `source_statement_crosswalk.md`.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H2, M4, R3]`. A primary paper and standard
formula are identified, but immutable source capture, exact theorem/page premise audit, and errata
review are not accepted. No matching Lean declaration or elaborated expression has been found or
credited. The first failed theorem gate is the exact-statement gate. No proof or theorem completion
is claimed.

## Open task DAG

1. `S56-M-1193-STATEMENT`: elaborate the manifold, Ricci bound, heat equation, positivity, and
   pointwise estimate; mutation-test every assumption and boundary.
2. `S56-M-1193-ANCHOR_AUDIT`: pin primary sources and audit mathlib/external Lean candidates.
3. `S56-M-1193-OBLIGATION_TREE`: freeze all typed obligation and assurance graphs.
4. `S56-M-1193-PROOF`: supply an exact local proof or pinned/imported closure.
5. `S56-M-1193-VALIDATION`: run kernel, trust, provenance, composition, and hermetic gates.
6. `S56-M-1193-RELEASE`: independently review receipts and decide completion.

Validation in `validation.md` is structural intake evidence only.
