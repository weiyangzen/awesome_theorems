# Source-statement crosswalk

| Claim component | Human source anchor | Lean target candidate | Intake assessment |
|---|---|---|---|
| Closed simply connected 3-manifold is homeomorphic to the 3-sphere | G. Perelman, *Ricci flow with surgery on three-manifolds* (2003), arXiv:math/0303109, especially the introduction's reduction to finite extinction together with the surgery program | No canonical declaration selected | Primary proof-program source located, but exact premise-to-node and correction audit is open: `H1` |
| Finite extinction needed for the simply connected case | G. Perelman, *Finite extinction time for the solutions to the Ricci flow on certain three-manifolds* (2003), arXiv:math/0307245, theorem stated in the introduction | Future extinction obligation family | Pinpoint theorem, hypotheses, and dependence on earlier surgery results require detailed audit |
| Analytic foundation for Ricci flow and no local collapsing | G. Perelman, *The entropy formula for the Ricci flow and its geometric applications* (2002), arXiv:math/0211159 | Future analytic dependency nodes | Dependency source only, not itself the Poincare conclusion |
| Domain | Closed, connected topological 3-manifold without boundary | Universe-polymorphic `M` with mathlib manifold/topology structures | Exact structure, compactness convention, and boundary representation are deferred to statement work |
| Simple connectedness | Trivial fundamental group / every loop contracts | A mathlib simple-connectedness predicate to be identified | Competing encodings must be compared and transported by checked lemmas |
| Conclusion | Homeomorphic to the standard 3-sphere | `Nonempty (M ≃ₜ sphere ...)` or the exact available equivalent | Sphere model, dimension indexing, and topology must be frozen by elaboration |

The root is the topological Poincare statement, not the broader geometrization theorem and not merely
a homology-sphere characterization. The connectedness hypothesis is retained explicitly even where
a selected simple-connectedness API might imply it. Compactness plus absence of boundary expresses
"closed"; the statement phase must mutation-test both components rather than silently folding them
into prose.

Discovery links (not immutable evidence receipts):

- Perelman 2002: <https://arxiv.org/abs/math/0211159>
- Perelman surgery paper: <https://arxiv.org/abs/math/0303109>
- Perelman finite extinction paper: <https://arxiv.org/abs/math/0307245>

No `H0` or machine-closure claim is made. Source audit must capture immutable files and hashes,
map every root premise to exact pages/theorems, inspect revisions and published corrections, and
obtain independent review. Statement work must then select a minimal pinned import set, elaborate
the exact expression, and check all credited encoding transports before proof evidence is observed.
