# THM-M-0243 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the Bohr-Mollerup theorem. The
repository supplies only the phrase `伽马函数的特征刻画` ("characterization of the Gamma
function"), the Bohr/Mollerup attribution, and the year 1922. Its `已验证` label is untrusted
metadata and gives neither a source locator nor a proposition.

The standard named theorem is recognizable: a positive function on the positive real numbers that
is log-convex, is normalized by `f(1) = 1`, and obeys `f(x + 1) = x f(x)` agrees with the Gamma
function on the positive real numbers. NIST DLMF section 5.5(iv) states this modern form, but it is a
secondary reference, not the original Bohr-Mollerup proof source. No immutable primary edition,
pinpoint theorem/page, complete premise and errata map, or independent source review is admitted.

Pinned mathlib contains the exact-topic module
`Mathlib.Analysis.SpecialFunctions.Gamma.BohrMollerup` and declaration
`Real.eq_Gamma_of_log_convex`. Its type makes the domain, positivity, log-convexity, normalization,
recurrence, and positive-domain conclusion explicit. `IntakeProbe.lean` authenticates that API and
adjacent Gamma facts at the pinned revision. This is candidate discovery only: source identity,
canonical-target selection, checked source transport, terminal proof-body provenance, and trust
closure remain downstream work.

The provisional vector is `[H1, M3, R4]`. The dossier freezes the recognizable theorem family and
every proposition-changing decision without silently equating the catalog slogan with the mathlib
declaration. All six later tasks remain open. No exact canonical statement, accepted proof state,
audit completion, theorem completion, accepted receipt, or master acceptance is claimed.

See `scope-map.md` for the included and excluded mathematical scope,
`source-statement-crosswalk.md` for source and Lean component mapping, `task-dag.json` for the open
execution route, and `validation.md` for exact self-test commands and results.
