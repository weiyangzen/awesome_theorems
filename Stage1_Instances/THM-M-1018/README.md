# THM-M-1018 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the Levy inversion formula. The short source
label "characteristic-function inversion" is not precise enough to select a unique formal theorem,
so the standard interval-mass formulation is frozen as the intended human claim, subject to the
statement-phase source and elaboration checks recorded below.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | Recover `mu ((a,b])` from its characteristic function at continuity points `a < b` | The displayed formula is provisional until a primary-source pinpoint and exact Lean type are checked |
| Objects | A Borel probability measure `mu` on `Real`; real endpoints `a < b` | Random-variable presentations are transports, not additional roots |
| Hypotheses | `mu {a} = 0` and `mu {b} = 0` (equivalently, endpoint continuity) | Equivalence of the two presentations needs a checked measure-theoretic bridge |
| Transform | `phi(t) = integral x, exp (I * t * x) dmu` | Sign convention must be fixed consistently with the inversion kernel |
| Limit | Symmetric truncated integral over `[-T,T]`, with `T -> +infinity` | Integral measurability, the removable value at `t = 0`, and limit topology remain statement obligations |
| Boundary cases | Atoms at endpoints, `a = b`, reversed endpoints, and alternate half-open intervals | Excluded from the root and retained as mutation probes |
| Foundations | Lean 4 kernel, pinned mathlib measure/integration/complex-analysis APIs | Exact imports, toolchain, axioms, and transitive closure remain open |

The scope does not silently substitute the characteristic-function uniqueness theorem, a density
inversion theorem, or Fourier inversion for integrable densities. Those are related results with
different hypotheses and conclusions.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H2, M4, R3]`. `H2` records that a standard
mathematical formulation has been identified but no primary edition/page/errata receipt has been
accepted. `M4` records that no exact Lean declaration or elaborated expression has yet been frozen.
The first failed gate is the exact source-statement gate. No proof or theorem-completion credit is
claimed.

## Validation

The commands and results in `validation.md` establish target membership, repository-standard
consistency, JSON syntax, and dossier-local structure only.

The subsequent statement-phase artifact `Statement.lean` freezes and kernel-elaborates the exact
interval-mass target with one direct pinned mathlib import. `statement-validation.md` records its
normalization, checked binder-explicit transport, mutation probes, environment fingerprint, and
successful narrow Lean command. This is statement evidence only; H0, proof closure, and theorem
completion remain unclaimed.
