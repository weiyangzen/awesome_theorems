# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:9719-9724` records the Chinese title
`皮卡-林德勒夫定理`, attributes it to Emile Picard and Ernst Lindelof, gives the year 1894, and
states only `ODE解的存在唯一性`. `Docs/Stage0_Blueprint.md:36237-36262` repeats that gloss while
explicitly leaving exact definitions and premises, proof history, equivalent formulations, axioms,
and existing machine artifacts open. The rev-5.6 manifest retains `已验证` only as
`source_status_untrusted`.

The six catalog lines originate at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. They contain no edition, theorem/page, archival
statement, translation, assumption map, errata record, or reviewer, so they are discovery metadata
and cannot establish `H0`.

## Human-source discovery lead

Crossref and Numdam metadata identify E. Picard, "Sur la methode des approximations successives et
les equations differentielles lineaires," *Bulletin de la Societe Mathematique de France* 22
(1894), pages 52-57, DOI `10.24033/bsmf.481`. This agrees with the catalog's Picard/year metadata,
but its title concerns linear differential equations. The repository does not select it as the
source of the modern nonlinear theorem, and this intake did not obtain and inspect a complete
primary text, locate an exact theorem, map its assumptions, identify Lindelof's source, audit a
translation or errata, or obtain independent review. It is therefore a bibliographic lead only,
not `H0` evidence or a canonical statement.

## Component crosswalk

| Catalog phrase | Conventional component to resolve | Pinned Lean surface | Intake disposition |
|---|---|---|---|
| ODE | `alpha'(t) = f(t, alpha(t))` or an autonomous specialization | `HasDerivWithinAt`, `HasDerivAt` | equation, domain, and endpoint semantics open |
| solution | a curve through prescribed `(t0, x0)` on a nontrivial interval | existential curve or local-flow conclusions | regularity and interval open |
| existence | local solution for suitable continuous, spatially Lipschitz field | `IsPicardLindelof.exists_eq_forall_mem_Icc_hasDerivWithinAt` | direct family lead; not canonical root |
| uniqueness | equality of two solutions with the same initial value | `ODE_solution_unique_of_mem_Icc`, `_of_mem_Ioo`, `_univ` | separate lead; composition boundary open |
| Picard-Lindelof | successive-approximation/Cauchy-Lipschitz theorem family | `IsPicardLindelof`, `ODE.picard` | recognizable family, exact variant open |
| `已验证` | untrusted catalog status | no proposition or kernel evidence | explicitly rejected as proof credit |

## Pinned Lean discovery boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Analysis.ODE.PicardLindelof` describes local existence for time-dependent vector fields on
complete normed real vector spaces. Its `IsPicardLindelof` structure packages a spatial
Lipschitz-on-ball premise, time continuity, a norm bound, and a quantitative interval condition.
The module's differential existence theorem returns a curve with the requested initial value and
`HasDerivWithinAt` on a closed interval. The module explicitly says that it proves existence only
and refers uniqueness to `ODE_solution_unique` and related theorems in
`Mathlib.Analysis.ODE.Gronwall`.

The Gronwall module contains closed-interval, open-interval, local-eventual, and global uniqueness
forms. Combining one with the existence result requires explicit compatibility between the
Lipschitz region, curve range, interval endpoints/interior, derivative notions, continuity, and
initial condition. No such source-selected root or checked composition is credited at intake.
`IntakeProbe.lean` only confirms that these pinned interfaces elaborate.

## Required follow-up

Before statement or `H0` acceptance, a source reviewer must select an immutable primary or
authoritative edition, pinpoint the exact theorem and incorporated definitions, transcribe ordered
binders/hypotheses/conclusion, map exceptional cases and corrections, reconcile Picard and Lindelof
provenance, distinguish `THM-M-1331`, and obtain independent review. The statement phase must then
elaborate and fingerprint the exact Lean root, check alternate encodings and existence/uniqueness
composition, and run all required mutations.
