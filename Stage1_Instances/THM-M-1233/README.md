# THM-M-1233 rev-5.6 intake

This is the `planned` intake dossier for the Beale-Kato-Majda continuation criterion. The terse
Stage0 phrase "Euler equation solution blow-up criterion" is not itself an exact theorem. The root
is therefore frozen to the original three-dimensional, whole-space incompressible Euler criterion;
nearby periodic, bounded-domain, two-dimensional, Navier-Stokes, and weak-solution results are not
substitutes.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| PDE | incompressible Euler velocity-pressure system on `R^3` | no Navier-Stokes viscosity |
| Solution | sufficiently regular classical/Sobolev solution issued from divergence-free data | exact regularity indices must be pinned from the source before elaboration |
| Time | finite maximal interval `[0,T)` | local existence and the meaning of continuation must become explicit premises |
| Diagnostic | vorticity `omega = curl u` and `integral_0^T ||omega(t)||_infinity dt` | essential supremum, measurability, and improper integral encoding remain open |
| Root conclusion | noncontinuation at `T` implies divergence of the integral; finite integral permits continuation | mere Sobolev estimates or local existence do not close the root |
| Foundations | Lean 4 kernel with versioned analysis/PDE dependencies | no suitable declaration or environment fingerprint is claimed |

The future statement phase must resolve the exact Sobolev exponent and solution predicate directly
from a pinned primary source, then elaborate that proposition without weakening maximality or the
continuation conclusion. The later obligation tree must separately represent local well-posedness,
the logarithmic velocity-gradient estimate, energy/Sobolev propagation, and continuation.

## Intake verdict

Lifecycle is `planned`; root vector is `[H1, M4, R3]`. The first open theorem gate is exact Lean
statement identity. `M4` is used because no repo-local Lean proposition for the full PDE criterion
has yet been identified. The source label `已验证` is untrusted metadata, not proof evidence.

The intake item is self-tested for structure and repository membership only. It does not complete
the theorem or any dependent phase.
