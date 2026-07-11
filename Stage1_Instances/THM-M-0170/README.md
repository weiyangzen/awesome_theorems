# THM-M-0170 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the smooth Nash isometric embedding theorem.
It does not inherit proof credit from the Stage0 label `已验证` or the legacy Stage1 slot.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | Every smooth, finite-dimensional Riemannian manifold admits a smooth isometric embedding into some finite-dimensional Euclidean space | The Euclidean dimension bound and exact Lean object model remain statement-phase work |
| Manifold conventions | Hausdorff, second-countable smooth manifolds without boundary; positive-definite smooth metric | Non-second-countable spaces, boundary/corners, pseudo-Riemannian metrics, and infinite dimension are excluded |
| Embedding conclusion | A smooth embedding whose pullback of the Euclidean metric is the given metric | Immersions, topological embeddings without metric preservation, and approximate embeddings do not close the root |
| Variants | Compact/noncompact branches and explicit dimension bounds | Bounds are supporting refinements, not silently part of the frozen existential root |
| Nearby theorem | Nash-Kuiper `C^1` embedding theorem | Explicitly excluded: it has different regularity and hypotheses |
| Formal system | Lean 4 plus pinned mathlib | Exact imports, structures, toolchain, and foundation profile remain open |

The canonical claim, ordered mathematical parameters, exclusions, and provisional formal target are
recorded in `intake.json`. `source-statement-crosswalk.md` separates the 1956 smooth theorem from
the 1954 `C^1` theorem. The dependent phases are represented by `task-dag.json`; no downstream
phase or proof closure is credited here.

## Statement gate

`Statement.lean` freezes the exact Lean target using only
`Mathlib.Geometry.Manifold.Riemannian.Basic`. Unlike the legacy statement shape, isometry means
pointwise preservation of the Riemannian inner products by `mfderiv`, not preservation of the
induced global distance. `statement.json` records the expression and environment fingerprints,
ordered binders, checked serialization, and four negative mutation fixtures.

This is statement elaboration only. It contains no Nash witness and gives no theorem-completion
credit.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M3, R3]`. The first failed theorem gate is
the Lean statement gate: no exact Lean expression, environment fingerprint, checked transport, or
mutation suite exists. The theorem is not complete.

## Validation

On base revision `43b8783c62005322690acf2bed800ea3acbd76c6`, the commands in `validation.md`
establish target membership, repository-standard consistency, JSON syntax, and dossier-local
integrity only. No Lean kernel result is claimed.
