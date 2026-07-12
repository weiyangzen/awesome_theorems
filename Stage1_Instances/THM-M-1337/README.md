# THM-M-1337 rev-5.6 intake

This is the fail-closed `planned` dossier for Gronwall's inequality. The repository catalog gives
only Thomas Gronwall, the year 1919, and the phrase "integral form of a differential inequality."
It supplies no formula, domain, ordered binders, assumptions, conclusion, or source locator. The
catalog label `已验证` is untrusted metadata and supplies no human-source or machine-proof credit.

The familiar name covers several materially different statements: scalar integral inequalities,
norm-valued estimates, differential or right-Dini-derivative forms, constant- and
variable-coefficient bounds, and versions with additive forcing. This intake records those choices
without selecting one from memory. In particular, the derivative/right-slope results in pinned
mathlib are real discovery candidates, but they are not silently substituted for the catalog's
integral-form wording.

## Intake artifacts

- `instance.json` is the structured planned instance and assurance boundary.
- `scope-map.md` records the admissible theorem family, proposition-changing decisions, boundary
  cases, and explicit exclusions.
- `source-statement-crosswalk.md` maps the repository wording, historical bibliographic candidate,
  and pinned Lean candidates without upgrading any of them to an exact target.
- `task-dag.json` leaves all six downstream rev-5.6 phases open.
- `IntakeProbe.lean` checks only that relevant pinned mathlib declarations elaborate.
- `validation.md` and `intake-receipt.json` record bounded worker checks and their limits.

## Status boundary

The proposed root vector is `[H1, M3, R4]`: the named classical theorem family and a plausible 1919
source are identifiable, but no theorem/page premise crosswalk or independent source review is
accepted; pinned mathlib exposes usable nearby statement interfaces, but no canonical target,
checked transport, provenance, or proof credit is frozen; and no readable proof reconstruction has
been audited. There is no accepted proof state, audit completion, theorem completion, or master
acceptance.
