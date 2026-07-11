# THM-M-0170 anchor audit

Audit date: 2026-07-12. Canonical target: `Stage1Instances.THM_M_0170.Statement` in
`Statement.lean`. This inventory is frozen against repository base revision
`046b0721abb228d13c7042349574736fe375cd97` and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (commit date 2026-03-30). It gives
no proof credit for the Nash existence claim.

## Search inventory

| Surface | Immutable scope or query | Result and classification |
|---|---|---|
| Pinned mathlib source | Full `Mathlib`, `Archive`, and `Counterexamples` trees at commit `8a178386ffc0f5fef0b77738bb5449d50efeea95`; searched case-insensitively for Nash/imbedding/embedding and Riemannian-isometric combinations | No terminal smooth Nash theorem or exact wrapper found. `Mathlib.Geometry.Manifold.Riemannian.Basic` supplies the smooth Riemannian object model and tangent metric. `Mathlib.Geometry.Manifold.WhitneyEmbedding.exists_embedding_euclidean_of_compact` is a nearby candidate only. |
| Repository-local Lean | Tracked tree at commit `046b0721abb228d13c7042349574736fe375cd97`; Nash and isometric-embedding terms | Legacy `AwesomeTheorems.Stage1.S1_M_123` at blob `46c0252068f932a5c53a93a9c6d6801764a7c635` contains statement shapes, projections, and the same Whitney wrapper, but explicitly records `not_repo_local_closed`; it has no Nash witness. |
| GitHub repository search | Public repository metadata queried on 2026-07-12 for exact `"Nash embedding"` plus Lean, `"isometric embedding"` plus Lean, and `Nash theorem language:Lean` | The exact embedding queries returned zero repositories. The Nash-theorem query returned only `KishorS-eu/FM25-gametheory`, which concerns Nash equilibria and is excluded as a name collision. GitHub unauthenticated code search required sign-in, so no claim of exhaustive public-code coverage is made. |
| grep.app | Lean-filtered exact phrase queries attempted on 2026-07-12 | Service returned HTTP 429 challenge responses. This registry is recorded as unavailable, not as negative evidence. |

The external-search result is therefore `no credible exact Lean 4 candidate located`, not
`no candidate exists`. No external URL is promoted to a machine anchor, and there is no moving
dependency fetch or unpinned source inspection in this receipt.

## Candidate assessment

### A1: pinned mathlib compact Whitney embedding

- Revision: mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- Module/declaration: `Mathlib.Geometry.Manifold.WhitneyEmbedding` /
  `exists_embedding_euclidean_of_compact`.
- Proof body: lines 136 onward of the pinned module; local source SHA-256
  `6d77ea459398c5c015f0c331040956cf28c8bc971ef59f40fffe18f1ac772845`.
- Checked type: for a compact Hausdorff smooth manifold, it produces a smooth closed embedding
  into finite-dimensional Euclidean space with injective manifold derivative.
- Exact-target gap: it assumes compactness, while the frozen target covers noncompact manifolds;
  more importantly, injectivity of `mfderiv` does not establish preservation of the Riemannian
  inner product. It cannot supply the final conjunct of
  `IsSmoothRiemannianIsometricEmbedding`.
- Trust/provenance: `AnchorAudit.lean` wraps the pinned declaration without a new premise. Lean
  reports only `propext`, `Classical.choice`, and `Quot.sound`. This validates the substrate type,
  not Nash's theorem.
- Verdict: `nearby_substrate`, not root-relevant machine closure.

### A2: pinned Riemannian manifold API

- Revision/module: the same mathlib commit,
  `Mathlib.Geometry.Manifold.Riemannian.Basic`; source SHA-256
  `423334dd30e7c05ede4ab2c0f912bcbb758856078e90a21a0d91fa3d31c1d038`.
- Relevant declarations: `Bundle.RiemannianBundle`,
  `IsContMDiffRiemannianBundle`, `mfderiv`, and the Euclidean tangent-space instances.
- Feasibility: these declarations elaborate the frozen pointwise pullback-metric condition.
  They provide definitions and analytic substrate, not an embedding construction.
- Verdict: `object_model_substrate`, with no root proof-body credit.

### A3: legacy repository artifact

- Immutable source: repository commit `046b0721abb228d13c7042349574736fe375cd97`,
  `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_123.lean`, blob
  `46c0252068f932a5c53a93a9c6d6801764a7c635`, SHA-256
  `876cfd99ce3a431993b9b27e3f162e3fed0ac839c453b0f75806a69e23269abe`.
- Mismatch: its `StatementShape` uses global `Isometry` on an assumed
  `PseudoEMetricSpace`, rather than the frozen pointwise differential metric equality. Its only
  existence theorem is candidate A1; the other theorems project fields from a hypothetical
  witness.
- Verdict: `discovery_only`; rev-5.6 forbids inherited proof credit.

## Audit verdict

Inventory classification is complete for the searched, explicitly bounded surfaces. There is no
exact mathlib or credible external Lean 4 terminal candidate to pin/import/check. Machine debt
remains `formalization_debt`, root state remains open, and `repo_local_integration_debt` is not
introduced because no external machine closure was found. The next phase must construct an
obligation tree for a new formalization; it must not treat Whitney embedding, a global metric-space
isometry, or the `C^1` Nash-Kuiper theorem as a substitute.

Status boundary: this worker audit may be proposed as `[_]` for
`S56-M-0170-ANCHOR_AUDIT` after its recorded checks pass. It does not establish `H0`, `M0`, `R0`,
theorem completion, or master acceptance.
