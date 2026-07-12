# THM-M-1385 rev-5.6 intake

`THM-M-1385` is the ordinary-differential-equations catalog item "Sturm comparison theorem."
The repository supplies only the gloss "comparison of zeros of solutions," attributes the result
to Jacques Sturm, gives the year 1836, and labels it `verified`. The label is untrusted metadata,
and the gloss is not a binder-complete proposition.

## Intake result

This directory is a fail-closed `planned` dossier. It preserves the recognizable comparison-
theorem family without selecting a convenient textbook variant. The catalog does not select the
differential-equation normal form, coefficient regularity and positivity assumptions, interval and
endpoint conventions, what it means to solve the equations, the full global comparison versus the
local consecutive-zero corollary, zero multiplicity, or the exact existence and location result.

Sturm's original 1836 memoir was inspected in the NUMDAM scan. Section XII, journal pages 125-126,
gives a global zero-count and ordered-zero comparison for two self-adjoint equations under
`G'' >= G'`, positive `K'` and `K''`, `K'' <= K'`, and an initial logarithmic-flux inequality.
Section XVI, pages 135-136, removes the endpoint-ratio condition and says every pair of consecutive
zeros of `V'` contains at least one zero of `V''`; it also gives the reverse at-most-one property.
The catalog gloss does not choose between those roots or a checked normalized form. Complete proof
mapping, translation, errata review, and independent source review remain open.

An immutable Encyclopedia of Mathematics entry entitled "Sturm theorem" was also inspected. It
states the different polynomial root-counting theorem using Sturm series and attributes that result
to an 1829 publication. It therefore cannot be substituted for this 1836 ODE item.

## Formal boundary

`IntakeProbe.lean` elaborates adjacent pinned real ODE, derivative, interval, and zero APIs. A
bounded exact-topic search found no Sturm comparison declaration in repo-local Lean or pinned
mathlib. Those observations are intake discovery only, not the downstream anchor audit.

The canonical mathematical statement and Lean expression remain null. The provisional vector is
`[H1, M4, R4]`: an established theorem family and source leads are known, but exact source mapping
and statement selection remain open; no exact formal artifact is credited; and no source-faithful
readable proof can attach to an unfrozen root. All six downstream tasks remain open. No accepted
state, audit completion, theorem completion, or master acceptance is claimed.
