# Source-statement crosswalk

## Primary-source chain

- Grigori Perelman, "The entropy formula for the Ricci flow and its geometric applications",
  arXiv:`math/0211159` (2002), especially the no-local-collapsing and Ricci-flow foundations.
- Grigori Perelman, "Ricci flow with surgery on three-manifolds", arXiv:`math/0303109` (2003),
  supplying the surgery program toward geometrization.
- Grigori Perelman, "Finite extinction time for the solutions to the Ricci flow on certain
  three-manifolds", arXiv:`math/0307245` (2003), supplying the extinction result relevant to the
  simply-connected case.

These are primary discovery anchors, not yet immutable H0 receipts. Perelman's papers form an
argument chain rather than a single conveniently matching formal theorem declaration. The source
audit must pin versions, locate every invoked result, check corrections, and map a reviewed
exposition's derivation without replacing primary evidence.

## Crosswalk

| Repository phrase | Intended mathematical content | Lean-side consequence | Intake disposition |
|---|---|---|---|
| "Perelman's theorem" | not a unique conventional theorem name | cannot infer an exact declaration from the title alone | narrowed using legacy gloss |
| "proof of the Poincare conjecture" | three-dimensional Poincare conjecture | quantify over an explicitly modeled 3-manifold and conclude a homeomorphism with `S^3` | root subject identified |
| "closed" | compact and without boundary, normally Hausdorff | selected manifold API may encode these separately | freeze later |
| "simply connected" | path connected plus trivial fundamental group, with convention variance | choose a precise mathlib predicate/equivalence | freeze later |
| Perelman paper conclusions | analytic/smooth Ricci-flow and surgery results | requires checked bridges to the topological root | open source crosswalk |

## Fidelity boundary

The canonical claim in `instance.json` is a human-scope paraphrase, not an exact quotation. Before
H0, reviewers must identify a stable theorem/corollary formulation, record page or theorem labels
and all conventions, reconcile orientability and connectedness, check errata and accepted
expository dependencies, and approve every source-to-root implication. No generalized
geometrization statement or finite-extinction lemma alone may be credited as the requested root.
