# THM-M-1469 rev-5.6 intake

`THM-M-1469` is the numerical-analysis catalog item "adaptive finite element method." The
repository gives only the gloss "adaptivity based on a posteriori error estimates," attributes it
to Ivo Babuška and Werner Rheinboldt in 1978, and attaches an untrusted `verified` label. A method
name and a design principle identify a theorem family, not a truth-valued proposition with ordered
binders, hypotheses, and a conclusion.

## Intake result

This directory records a fail-closed `planned` instance. It does not silently choose among
reliability or efficiency of an estimator, estimator equivalence, marking success, estimator
reduction, contraction, convergence, quasi-optimal rates, computational complexity, or correctness
of one adaptive loop. Each requires materially different differential equations, spaces, meshes,
estimators, refinement and marking rules, constants, and conclusions that the catalog does not
supply.

The 1978 paper by Babuška and Rheinboldt, *Error Estimates for Adaptive Finite Element
Computations*, is an unusually close bibliographic lead: its title, authors, year, journal, volume,
issue, and pages align with the catalog metadata. Crossref metadata was inspected, but the primary
article body was unavailable through the inspected endpoint. No theorem passage, complete premises,
proof, correction record, or independently reviewed source mapping was admitted. The lead therefore
cannot select a canonical root or establish `H0`.

## Formal boundary

`IntakeProbe.lean` elaborates adjacent pinned coercive-form, finite-dimensional projection, and
nested-projection convergence APIs. A bounded topic search found no adaptive-FEM, residual-
estimator, or source-identical declaration in pinned mathlib or the repo-local Lean tree. One
unrelated fixed-point theorem uses the phrase "a posteriori" and is expressly excluded. These are
intake discovery observations, not the downstream anchor audit or proof evidence.

The canonical human statement and Lean expression remain null. The provisional vector is
`[H5, M4, R4]`: the catalog method gloss is not yet a stable proposition; no source-identical usable
formal artifact is credited; and no proof reconstruction can attach to an unfrozen root. All six
downstream tasks remain open. Neither audit completion nor theorem completion is claimed.
