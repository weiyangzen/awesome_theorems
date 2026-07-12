# THM-M-1384 rev-5.6 intake

`THM-M-1384` is the ordinary-differential-equations catalog item `Sturm-Liouville理论`
(`Sturm-Liouville theory`). The repository supplies only the gloss `二阶线性边值问题`
(`second-order linear boundary-value problem`), attributes it to Jacques Sturm and Joseph
Liouville, gives the date 1836, and labels it `已验证`. That label is untrusted metadata under
rev-5.6.

## Intake result

This directory is a fail-closed `planned` dossier. A theory and a class of boundary-value problems
do not identify one truth-valued theorem. The catalog does not select the differential expression,
regular or singular setting, interval, coefficient assumptions, solution semantics, boundary
conditions, or conclusion. Possible conclusions include solvability, a Green representation,
self-adjointness, spectral reality or discreteness, eigenfunction completeness, comparison,
separation, oscillation, or a checked conjunction. Selecting any one would add proposition-changing
mathematics rather than transcribe the received record.

Sturm's 1836 memoir, NIST DLMF Section 1.13(viii), the Encyclopedia of Mathematics entry
`Sturm-Liouville problem` at immutable revision 55171, and Teschl's modern Sections 5.3-5.6 were
inspected as source-family discriminators. They distinguish general equations, regular and singular
problems, boundary-condition regimes, transformations, spectral results, and oscillation results.
The catalog cites none of them and selects no proposition within them. The original memoir is
Sturm-authored and reports an earlier Academy reading, so the catalog's joint attribution and date
also require an independent historical review.

## Formal boundary

`IntakeProbe.lean` elaborates adjacent pinned derivative, ODE, eigenvalue, symmetric-operator,
compact-operator, spectrum, and Rayleigh-quotient APIs. None defines the source-selected
Sturm-Liouville expression, operator domain, boundary conditions, or theorem. The probe provides no
statement, source, anchor-audit, or proof credit.

The canonical mathematical statement and Lean expression remain null. The provisional root vector
is `[H5, M4, R4]`: the received wording is not a stable proposition, no exact usable formal artifact
is identified, and no source-faithful reconstruction can attach to an unfrozen root. All six
downstream tasks remain open. No `H0`, `M0`, `R0`, accepted proof state, audit completion, theorem
completion, or master acceptance is claimed.
