# THM-M-0469 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the metadata label
"Zhang-Sarnak theorem" (`张寿武-萨纳克定理`). The repository's source row describes it only as a
1999 proof of the Bogomolov conjecture. That description does not uniquely identify a theorem or a
primary publication, so this intake deliberately does not invent a formal statement.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Metadata identity | The exact repository label, people, year, and one-line claim | These fields are discovery metadata, not a verified citation |
| Intended mathematics | A possible Bogomolov-type lower-bound/equidistribution theorem for subvarieties of abelian varieties | Ambient field, polarization, height, special subvarieties, and conclusion are unresolved |
| Human source | Locate a joint Zhang-Sarnak primary source, or correct the attribution through the master data process | No joint paper or pinpoint theorem is asserted here |
| Lean target | A future exact encoding after source disambiguation | Module, declaration, binders, and imports are intentionally unset |
| Foundations | Lean 4 kernel plus a later pinned mathlib environment | Exact classical-choice, quotient, and TCB profiles remain open |
| Proof architecture | Definitions, source theorem, reductions, and proof leaves | Obligation freezing belongs to a later dependent phase |

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H4, M4, R4]`. The first failed gate is source
identity: the supplied name and summary do not determine a unique mathematical proposition. Under
the rev-5.6 fail-closed rule, statement work must not substitute a familiar Bogomolov theorem for
the named target. The theorem is not complete and no historical `已验证` label receives proof
credit.

The structured scope is in `intake.json`; the source ambiguity and the exact questions that must be
resolved are recorded in `source_statement_crosswalk.md`. Validation in `validation.md` covers only
manifest consistency, JSON syntax, dossier references, and prohibited-token scanning.
