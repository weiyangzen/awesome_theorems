# THM-M-1316: Riemannian Positive Mass Theorem

## Status

- Item: `S56-M-1316-INTAKE`
- Lifecycle: `planned`
- Root vector: `H1 / M4 / R3`
- Theorem complete: `false`
- Current requirements and task-state authority: `Docs/Stage1_Blueprint_v2.md`

This dossier freezes the intended scope for intake. The repository metadata phrase
`ADM质量非负` is not itself a source-quality theorem statement, and its historical
`已验证` label supplies no proof credit.

## Frozen Scope

The target is the three-dimensional, time-symmetric Riemannian positive mass theorem:
a complete connected asymptotically flat Riemannian 3-manifold without boundary and
with nonnegative scalar curvature has nonnegative ADM mass at each selected end, with
zero mass only for Euclidean 3-space.

The exact differentiability and asymptotic-decay assumptions remain deliberately open
until the statement phase reconciles a primary-source formulation with a Lean object
model. The rigidity clause is part of the root and must not be dropped.

## Scope Map

| Surface | Intake decision | Later gate |
|---|---|---|
| Riemannian dimension-3 theorem | Included root | Freeze exact regularity and end structure |
| ADM mass for a selected end | Included | Define chart invariance and normalization |
| Nonnegative scalar curvature | Included | Freeze pointwise/weak formulation |
| Zero-mass Euclidean rigidity | Included | Encode global isometry conclusion |
| General initial data `(M,g,K)` | Excluded | Separate theorem; no silent broadening |
| Horizons or compact boundary | Excluded | Penrose/black-hole variants are separate |
| Higher-dimensional theorem | Excluded | Dimension-specific hypotheses differ |
| Charged/asymptotically hyperbolic variants | Excluded | Separate mass notions and hypotheses |

## Open Intake DAG

1. `PM-STATEMENT`: choose an exact primary-source edition and freeze all regularity,
   decay, end, mass-normalization, and rigidity binders.
2. `PM-LEAN-SUBSTRATE`: locate or define asymptotically flat ends, ADM mass, scalar
   curvature, completeness, and Riemannian isometry in pinned Lean 4.
3. `PM-TRANSPORT`: check the time-symmetric initial-data/Riemannian transport rather
   than assuming it in prose.
4. `PM-ANCHOR`: audit mathlib and external Lean 4 candidates at immutable revisions.
5. `PM-ARCHITECTURE`: freeze typed obligation and provenance graphs before proof credit.

## Status Boundary

No Lean declaration is nominated or elaborated in this phase. No source is accepted at
`H0`, no machine closure is claimed, and the likely current debt is
`formalization_debt`. See `source_statement_crosswalk.md` and `validation.md`.
