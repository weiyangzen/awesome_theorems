# THM-M-0021 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the Brauer-Siegel theorem. The
repository supplies only the gloss "asymptotic estimates of number-field class numbers," attributes
it to Richard Brauer and Carl Siegel, and dates it 1945. That identifies a theorem family, but it
does not determine a truth-valued proposition.

In particular, the catalog does not choose a family or sequence of number fields, the degree and
discriminant growth condition, a normal/Galois restriction, the class-number/regulator expression,
the discriminant normalization, or the filter and limit convention. This intake preserves those
choices for source review rather than silently adopting a familiar formulation. The duplicated
catalog record has identical six-field metadata and supplies no additional mathematical detail.

The source crosswalk records the repository passages and two uninspected primary-source leads.
Edition, pinpoint theorem/page, assumptions, corrections, errata, and independent review remain
open, so no `H0` credit is claimed. `IntakeProbe.lean` checks only that adjacent pinned mathlib APIs
for number fields, class numbers, regulators, discriminants, and filters elaborate. It states no
Brauer-Siegel proposition and provides no proof or downstream anchor-audit credit.

Lifecycle is `planned`; the provisional root vector is `[H1, M4, R4]`. The canonical mathematical
statement and Lean expression remain null, and every downstream phase remains open. No accepted
proof state, statement fingerprint, audit completion, theorem completion, or master acceptance is
claimed. Exact self-test commands and boundaries are recorded in `validation.md` and the
provisional `intake-receipt.json`.
