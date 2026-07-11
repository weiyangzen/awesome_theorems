# THM-M-1310 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the Einstein field equation. The repository
source calls it the "fundamental equation of general relativity," but an equation by itself is a
definition/model law rather than a proposition with a proof. This intake therefore does not invent
a theorem or treat the historical `已验证` label as proof evidence.

## Scope map

| Surface | Intended scope | Boundary at intake |
|---|---|---|
| Mathematical object | A Lorentzian metric `g`, its Ricci tensor and scalar curvature, the Einstein tensor `G = Ric - (1/2) R g`, and a symmetric stress-energy tensor `T` | Dimension, differentiability, signature, index placement, and curvature signs are not frozen |
| Field equation | `G + Λ g = κ T`, with `κ = 8πG_N/c^4` in conventional physical units | Units and constants must be explicit; the source's 1915 equation did not contain the modern cosmological term |
| Candidate proposition | Equivalence of expanded and Einstein-tensor forms after all tensors and conventions are defined | Candidate only; the statement phase must choose a genuine proposition and elaborate it |
| Special regimes | Vacuum (`T = 0`), zero cosmological constant, and trace-reversed forms | Specializations/equivalences only, not silently substituted roots |
| Exclusions | Local/global Cauchy existence, uniqueness, stability, singularities, and empirical correctness | These are separate results, including neighboring `THM-M-1311` and `THM-M-1312` |
| Foundations | Lean 4 kernel with a pinned mathlib environment | Differential-geometric tensor infrastructure, imports, toolchain, and trust profile remain open |

The unresolved equation-versus-theorem mismatch is a statement-phase gate, not permission to prove
a tautological wrapper. The structured claim boundary is in `intake.json`, and the historical and
modern notations are separated in `source_statement_crosswalk.md`.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M4, R3]`. The first failed theorem gate is
exact statement eligibility: no proposition, ordered binders, convention profile, or canonical Lean
expression has yet been accepted. No theorem completion or machine-proof credit is claimed.

## Validation

The commands in `validation.md` check manifest membership, repository-standard consistency, JSON
syntax, and dossier structure only. Master acceptance and every dependent phase remain outstanding.
