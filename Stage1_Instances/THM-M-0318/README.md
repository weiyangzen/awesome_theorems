# THM-M-0318 rev-5.6 intake

This directory is the `planned` intake dossier for the Schauder fixed-point theorem. The intended
human claim is the compact-convex form: a continuous self-map of a nonempty compact convex subset
of a real normed vector space has a fixed point. This is narrower and more precise than the Stage0
phrase "a fixed-point theorem on Banach spaces" and does not silently substitute Banach's
contraction theorem or the finite-dimensional Brouwer theorem.

`Statement.lean` now freezes and elaborates that compact-convex claim as
`Stage1Instances.THM_M_0318.SchauderFixedPointTarget`, with a checked direct expansion, structural
mutations, and empty/singleton boundary checks. The exact expression and environment fingerprint
are recorded in `statement.json`. The primary 1930 paper's exact theorem text, page-level anchor,
terminology, and errata remain uninspected, so this statement evidence does not upgrade source
fidelity to `H0`.

`anchor-audit.json` records the immutable candidate inventory. Pinned mathlib has checked
contraction and interval fixed-point results but no Schauder root. The audited external Brouwer
project covers only finite-dimensional spaces at a different toolchain and mathlib pin. Thus the
anchor audit does not change the root's machine status.

The provisional root vector is `[H2, M3, R4]`. The statement node is self-tested pending master
acceptance, and the anchor-audit node is independently self-tested pending master acceptance. No
source fidelity (`H0`), proof, full audit completion, or theorem completion is claimed.

The obligation-tree phase now freezes 12 canonical obligations in `obligation-registry.json` and
separate typed proof, refinement, provenance, evidence, trust, documentation, and workflow graphs
in `typed-graphs.json`. `ObligationTree.lean` checks the exact parent composition from abstract
approximation and compact-limit engines. The principal open cut set is the finite-net and
barycentric construction, locally pinned Brouwer integration, compactness extraction, and the
continuity limit. This architecture evidence does not close those hypotheses or the root.
