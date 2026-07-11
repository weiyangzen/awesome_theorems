# THM-M-1049 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the Stroock-Varadhan
martingale problem. The manifest's short description, "martingale
characterization of diffusion processes", names a theorem family rather than
one theorem with fixed hypotheses. Accordingly, intake freezes the full scope
that must be disambiguated by the statement phase; it does not silently choose
a weaker finite-state or discrete-time result.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| State space | Continuous paths in `R^d`, with their canonical process and natural filtration | Path-space and filtration encodings are not yet selected |
| Local characteristics | A second-order diffusion operator `L` determined by drift `b` and covariance `a` | Regularity, ellipticity, and boundedness hypotheses must be pinned to the selected primary theorem |
| Martingale problem | For each admissible test function `f`, `f(X_t) - f(X_0) - integral_0^t Lf(X_s) ds` is a martingale | Test-function class and integrability/localization conventions remain open |
| Characterization | Existence/uniqueness in law for the diffusion is expressed through existence/well-posedness of the martingale problem | Whether the intended root is an equivalence, an implication, or the well-posedness theorem is unresolved |
| Degenerate cases | Initial laws versus point starts; stopped/local problems; degenerate covariance | None may be discarded until the source theorem is identified |
| Formal system | Lean 4, pinned mathlib, and any target-local definitions needed for continuous-time martingales | Exact imports, toolchain fingerprint, and TCB profile belong to later phases |

The manifest-required finite-state or discrete-time lemmas are admissible
partial verification only. They cannot substitute for the continuous-path
Stroock-Varadhan root.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H2, M4, R3]`. The first
failed theorem gate is exact source/statement identification: the repository
metadata does not specify an edition, theorem number, coefficient assumptions,
or direction of the claimed characterization. The dependent statement phase
must resolve that ambiguity from a primary source before elaborating Lean.
No proof, machine closure, or theorem completion is claimed.

## Validation

The exact intake checks and their results are recorded in `validation.md`.
They establish target membership, repository-standard consistency, JSON
syntax, and dossier integrity only.
