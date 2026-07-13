# THM-M-0293 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog item `赫维茨定理`
(Hurwitz theorem). The repository supplies Adolf Hurwitz, the year 1903, the gloss
`傅里叶级数的绝对收敛` (absolute convergence of Fourier series), and an untrusted `已验证`
label. It does not supply a binder-complete proposition or proof evidence.

## Intake result

The attribution and year lead to Hurwitz's 1903 paper *Über die Fourierschen Konstanten
integrierbarer Funktionen*. A complete 22-page scan of the paper was inspected. It studies Fourier
coefficients of Riemann-integrable functions and proves several distinct results: a Parseval-type
identity, absolutely convergent coefficient-product series, an absolutely convergent Fourier
expansion for an indefinite integral, uniqueness up to a function "of integral zero," and a
Sturm-Hurwitz sign-change theorem. The catalog gloss does not identify which of these is the root.

In particular, the source does not state the blanket proposition that every integrable function's
own Fourier series is absolutely convergent. Selecting the indefinite-integral result, the
coefficient-product result, a later regularity criterion, or the Sturm-Hurwitz theorem would change
the proposition. The canonical human statement and Lean expression therefore remain null pending
an independently reviewed source decision.

## Source and formal boundary

The primary-work lead is Adolf Hurwitz, *Über die Fourierschen Konstanten integrierbarer
Funktionen*, *Mathematische Annalen* 57 (1903), 425-446, DOI `10.1007/BF01445179`. The inspected
GDZ scan identifies the article and includes pages 425-446. It is strong `H1` evidence, but no
complete translation, theorem selection, definition/premise/proof crosswalk, errata audit, or
independent review has been accepted.

Pinned mathlib exposes Fourier coefficients on `AddCircle`, Parseval/L2 interfaces, and
`hasSum_fourier_series_of_summable`. `IntakeProbe.lean` checks those APIs. The last theorem assumes
coefficient summability and derives uniform convergence; it does not prove the catalog's missing
absolute-summability criterion. These are useful exact-topic interfaces, not an exact source-mapped
target or accepted proof.

The provisional vector is `[H1, M3, R4]`. `instance.json` is the structured scope authority and
`task-dag.json` keeps every downstream phase open. No H0, M0, R0, accepted proof state, audit
completion, theorem completion, or master acceptance is claimed.
