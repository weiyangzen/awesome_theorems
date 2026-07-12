# THM-M-1347 rev-5.6 intake

`THM-M-1347` is the ordinary-differential-equations catalog item "center manifold theorem." The
catalog attributes it to Jack Carr in 1981 and gives only the gloss "reduction of nonhyperbolic
equilibria" plus an untrusted `verified` label. These fields identify a theorem family, not a
binder-complete proposition.

## Intake result

This dossier records a fail-closed `planned` instance. It preserves the catalog claim without
choosing among materially different center-manifold results: local manifold existence and
regularity, local invariance, the equation induced on a center manifold, asymptotic tracking,
stability transfer, or an approximation theorem. The catalog also leaves the system form, state
space, spectral splitting, regularity, locality, graph normalization, and nonuniqueness policy open.

Carr's *Applications of Centre Manifold Theory* is a strong bibliographic lead. Crossref confirms
the author, title, DOI, and 1981 metadata; Springer identifies the 1982 edition and chapters
"Introduction to Centre Manifold Theory" (pages 1-13) and "Proofs of Theorems" (pages 14-36). An
accessible two-page preview confirms that Chapter 1 treats finite-dimensional systems and motivates
dimension reduction, but it does not expose the numbered theorem statements. The repository does
not cite this edition or select one of its results. The lead is therefore not accepted as `H0`.

## Formal boundary

`IntakeProbe.lean` elaborates adjacent pinned ODE, flow-invariance, differentiability, linear
operator, invariant-submodule, and spectrum APIs. A bounded exact-topic search found no
center/centre-manifold declaration in repo-local Lean or pinned mathlib. These are discovery-only
facts, not an exhaustive anchor audit or proof of absence from external Lean projects.

The canonical mathematical statement and Lean expression remain null. The provisional vector is
`[H1, M4, R4]`: the theorem family and a primary-source lead are known, but exact source selection,
assumption mapping, errata review, and independent review remain open; no usable exact formal
artifact or source-faithful reconstruction is identified. All six downstream tasks remain open.
No accepted execution state, audit completion, theorem completion, or master acceptance is claimed.
