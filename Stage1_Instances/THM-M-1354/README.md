# THM-M-1354 rev-5.6 intake

`THM-M-1354` is the ordinary-differential-equations catalog item `特征指数`
(`characteristic exponent`). The repository supplies only the gloss `周期系统的特征值`
(`eigenvalues of periodic systems`), Gaston Floquet, the year 1883, and an untrusted `verified`
label. Those fields identify a classical Floquet spectral family, not one binder-complete theorem.

## Intake result

This dossier creates a fail-closed `planned` instance and preserves the ambiguity. In periodic
linear-system terminology, characteristic multipliers can mean eigenvalues of a monodromy matrix,
whereas characteristic exponents can mean numbers `mu` satisfying `exp(T * mu) = rho`, or
eigenvalues of a constant exponent/logarithm matrix in a Floquet decomposition. Exponents are
generally nonunique because of logarithm branches. The catalog does not distinguish these objects
and states no proposition about existence, correspondence, invariance, solution representation,
multiplicity, or stability.

The adjacent catalog targets are material boundaries: `THM-M-1352` names Floquet theory,
`THM-M-1353` names a fundamental-matrix Floquet theorem, and `THM-M-1355` names linear-system
stability. None is imported or substituted here.

## Source and formal boundary

Floquet's 1883 paper was identified from Numdam and Crossref metadata as a matching historical
source-family lead. The catalog does not cite it, and no numbered proposition, incorporated
definitions, proof boundary, translation, errata record, or independent review has been admitted.
The source metadata therefore supplies discovery context only, not `H0` evidence.

`IntakeProbe.lean` elaborates only adjacent pinned periodicity, ODE, matrix-exponential,
characteristic-polynomial, spectrum, and eigenvalue APIs. A bounded exact-topic search found no
Floquet or characteristic-exponent declaration in pinned mathlib or repository-local Lean. This is
intake discovery, not the exhaustive anchor audit and not proof of absence from external projects.

The canonical mathematical statement and Lean expression remain null. The provisional root vector
is `[H5, M4, R4]`: `H5` classifies the received catalog wording as not yet a stable proposition; it
does not say that standard Floquet mathematics is false or open. No exact usable formal artifact or
source-faithful reconstruction is identified. All six downstream tasks remain open. No `H0`,
`M0`, `R0`, accepted proof state, audit completion, theorem completion, or master acceptance is
claimed.
