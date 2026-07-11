# THM-M-1187 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the source entry named "parabolic
equations". It freezes what the repository actually says without inventing a single theorem from
a broad class of PDEs. The historical `已验证` label is untrusted metadata and supplies no proof
credit.

## Scope map

| Surface | In scope | Intake boundary |
|---|---|---|
| Source claim | "heat equation and its generalizations" | A topic description, not a quantified proposition |
| PDE family | heat equation and unspecified parabolic generalizations | order, coefficients, domain, data, and solution concept are absent |
| Candidate result kinds | existence, uniqueness, regularity, estimates, or qualitative properties | the source selects none of them |
| Neighbor separation | not the maximum principle (`THM-M-1188`), Schauder regularity (`THM-M-1189`), or L-p theory (`THM-M-1190`) | those are separate repository records and cannot be substituted |
| Lean surface | Lean 4 + pinned mathlib | no exact declaration/expression can truthfully be chosen yet |
| Foundations | Lean kernel profile to be fixed with an exact target | no logical or computational principle is credited |

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H4, M4, R4]`. The intake is complete as a
truthful scope freeze, but the downstream statement phase is blocked on source disambiguation: the
available source gives a subject heading rather than a theorem with hypotheses and a conclusion.
No theorem completion, source fidelity, Lean elaboration, or kernel proof is claimed.

The structured record is `intake.json`; the precise source crosswalk and disambiguation questions
are in `source_statement_crosswalk.md`; commands and results are in `validation.md`.
