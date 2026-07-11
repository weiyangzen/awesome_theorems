# THM-M-1527 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for Maxwell's equations. It does not inherit proof
credit from the source label `已验证`. At intake, the repository source supplies only the phrase
"the fundamental equations of electromagnetism"; that phrase is not yet a single mathematical
theorem.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | Equivalence of the four SI vacuum Maxwell equations with the differential-form system `d F = 0`, `d (star F) = J` after conventions are fixed | A provisional target family, not an elaborated Lean proposition |
| Model | Smooth oriented time-oriented four-dimensional Lorentzian manifold; electromagnetic 2-form `F`; current 3-form `J` | Signature, units, Hodge-star signs, regularity, and local/global hypotheses remain to be frozen |
| 3+1 statement | Gauss-electric, Gauss-magnetic, Faraday, and Ampere-Maxwell equations | Requires a chosen foliation and checked component decomposition |
| Consequences | Charge conservation and vacuum wave equations | Separate downstream theorems, not part of root completion |
| Exclusions | Experimental adequacy, constitutive laws in matter, boundary/interface conditions, monopole extensions, and numerical solvers | No empirical claim is admitted as a Lean theorem |
| Foundations | Lean 4 kernel and pinned mathlib differential geometry/analysis interfaces | Exact toolchain, imports, TCB, and dependency fingerprint remain open |

The scope follows the blueprint's physical-entry rule: only a mathematical consequence or
equivalence inside an explicitly axiomatized model is eligible. `intake.json` records the ordered
open choices. `source_statement_crosswalk.md` prevents the four equations, their covariant form,
and their consequences from being silently substituted for one another.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H2, M4, R3]`. The first failed theorem gate is
exact statement identification: the source wording does not determine units, geometry, sign
conventions, hypotheses, or even whether the intended claim is an axiom system, an equivalence, or
a derived theorem. The dependent statement phase must resolve these choices rather than inventing
proof credit. The theorem is not complete.

## Validation

On base revision `594dbb735284e7b81f51ce813a9c3200fd55f610`, the commands in `validation.md`
establish manifest membership, standard consistency, JSON syntax, and dossier hygiene only. No
Lean declaration or kernel result is claimed.
