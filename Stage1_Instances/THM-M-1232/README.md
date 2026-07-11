# THM-M-1232 rev-5.6 intake

This directory is the `planned` intake for the entry named "Euler equations." The screened claim is
only "equations of motion of an ideal fluid." That identifies a family of mathematical models, not
a truth-valued theorem. The intake therefore preserves the source wording and refuses to choose a
nearby existence, uniqueness, regularity, derivation, or conservation theorem without source
authority.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Source identity | Leonhard Euler, 1757; ideal-fluid equations | Exact edition/page and equation-to-modern-notation audit remain open |
| Provisional model | Momentum balance `rho (partial_t u + (u dot nabla)u) = -nabla p + rho g` | A source gloss, not a Lean proposition |
| Regime choices | Compressible/incompressible; density law; body force | The screened record chooses none |
| Analytic setting | Dimension, domain, time interval, regularity, weak/classical solution, data | All are unspecified |
| Candidate conclusion | Derivation, equivalence, existence, uniqueness, conservation, or regularity | No conclusion may be selected at intake |
| Exclusions | BKM, Yudovich, and Wolibner results; thermodynamic Euler relation; Euler ODE | These are distinct records or different meanings of "Euler equation" |
| Formal surface | Lean 4 after an exact proposition is authorized | No module, declaration, or kernel evidence exists |

The neighboring Stage0 records are decisive scope evidence: BKM, Yudovich, and Wolibner are listed
as separate targets. Substituting one of them for this entry would collapse distinct claims.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H2, M4, R4]`. The first failed gate is exact
human-statement identification. The statement phase must obtain an authoritative proposition with
its regime, domains, ordered binders, assumptions, and conclusion before Lean elaboration can
truthfully begin. The theorem is not complete.

## Validation

The commands and exact results for this intake-only node are recorded in `validation.md`. They check
manifest membership, repository-standard consistency, JSON syntax, scoped references, and forbidden
proof tokens. No Lean file is introduced, so no kernel result is claimed.
