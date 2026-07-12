# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:9873-9878` supplies exactly the title `特征指数`, Gaston
Floquet, 1883, the gloss `周期系统的特征值`, importance `high`, and status `已验证`. Git history
places all six uncited fields in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:36831-36856` repeats the metadata but explicitly leaves the precise
definitions and premises, proof route, dependencies, equivalent forms, axiom policy,
machine-checked state, and artifact links open. The rev-5.6 manifest preserves `已验证` only as
untrusted metadata and resets the target to `L0 / rework_required`.

The catalog contains no bibliography, equation, finite-dimensional or scalar-field choice,
periodic-system model, monodromy definition, binder, hypothesis, conclusion, incorporated
definition, proof boundary, correction history, or reviewer. It therefore does not identify a
stable proposition.

## Literal crosswalk

| Repository element | Material interpretations | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| `特征指数` | characteristic/Floquet exponent | complex scalar plus source-defined exponent predicate | title names an object, not a theorem |
| `周期系统` | periodic linear ODE, scalar higher-order equation, or another periodic system | `Function.Periodic`, coefficient and solution model | system and assumptions absent |
| `特征值` | monodromy multiplier, exponent-matrix eigenvalue, or loosely translated exponent | matrix spectrum, characteristic polynomial, eigenvalue predicates | multiplier/exponent distinction absent |
| Floquet / 1883 | historical source family | immutable edition, page/proposition, definitions, proof and errata map | paper metadata identified; exact mapping open |
| `已验证` | untrusted inventory label | reviewed human source and kernel receipt would be required | no H or M credit |

The title-to-gloss mismatch is proposition-changing. If `特征值` means monodromy eigenvalues, the
object is usually a characteristic multiplier. If it means an exponent, a logarithm convention and
the relation `exp(T * mu) = rho` must be fixed. Translating either choice into the other without a
source-selected statement and checked transport would broaden or substitute the target.

## Historical source-family lead

Numdam landing-page metadata and Crossref identify G. Floquet, "Sur les equations differentielles
lineaires a coefficients periodiques," *Annales scientifiques de l'Ecole normale superieure*,
series 2, volume 12 (1883), pages 47-88, DOI `10.24033/asens.220`. This matches the repository's
author, year, and subject family.

The catalog does not cite this paper. Intake obtained bibliographic metadata but did not admit a
complete stable scan or select a numbered passage. No incorporated definitions, assumptions,
conclusion, proof boundary, translation, correction or errata history, or independent review is
credited. The lead is discovery evidence only, not `H0`.

## Candidate component crosswalk

| Candidate component | Prospective pinned Lean surface | Missing source decision |
|---|---|---|
| positive period and periodic coefficient | `Function.Periodic A T` plus an order premise | system, regularity, field, dimension, and period policy |
| fundamental matrix and monodromy | matrix-valued integral curve, invertibility, normalization, one-period value | multiplication orientation, base time, and exact transition definition |
| characteristic multiplier | `spectrum` or a matrix characteristic-polynomial root | spectral encoding and multiplicity convention |
| characteristic exponent | scalar `mu` with a source-defined exponential relation | logarithm existence, branch equivalence, and field |
| exponent matrix | `NormedSpace.exp` applied to a constant matrix | Floquet factorization and matrix-logarithm source theorem |
| solution representation | exponential scalar factor times a periodic vector function | exact solution, periodicity, and generalized-eigenvector conditions |
| stability consequence | multiplier modulus or exponent real part | separately owned `THM-M-1355` unless explicitly included by the selected source |

The API probe authenticates generic names and types only. No row is a canonical statement,
checked transport, proof body, or `M0` result.

## Neighbor target crosswalk

`Docs/researches/math_theorems.md:9859-9864` separately records `THM-M-1352` as Floquet theory.
Lines 9866-9871 separately record `THM-M-1353` as the Floquet theorem concerning a fundamental
solution matrix. Lines 9880-9885 separately record `THM-M-1355` as stability of linear systems.
Adjacency is evidence for keeping these scopes separate; it is not a checked implication or shared
proof credit.

## Source and statement gate

Before ordinary theorem-proof execution, accountable reviewers must select or correct one stable
truth-valued proposition, preserve an immutable primary source, transcribe every incorporated
definition, ordered binder, hypothesis, conclusion, spectral and branch convention, proof boundary,
and correction state, reconcile the neighbor scopes, and independently approve the mapping. The
statement phase must then freeze minimal imports, the elaborated expression and environment
fingerprint, checked alternate transports, and removed-hypothesis, changed-domain, binder-scope, and
boundary mutations.

Until then, `H5` records that the received catalog wording is not a stable proposition. It does not
refute standard Floquet multiplier or exponent results. The canonical mathematical and Lean targets
remain null, and the downstream anchor audit remains open.
