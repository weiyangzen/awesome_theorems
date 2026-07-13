# THM-M-1479 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the numerical-analysis catalog
label `Monte Carlo方法` (Monte Carlo methods). The repository supplies only the gloss
`基于随机采样的数值方法` (a numerical method based on random sampling), attributes it to
Stanislaw Ulam and John von Neumann in 1946, and labels it `已验证`. That wording identifies a
method family, not a truth-valued proposition with ordered binders, hypotheses, and a conclusion.
The verified label is untrusted metadata and supplies neither source nor proof credit.

## Intake result

The record does not select a quantity to approximate, probability space, sampling law, estimator,
sample-size convention, integrability or moment hypotheses, or conclusion. A Monte Carlo result
could concern unbiasedness, consistency by a law of large numbers, variance or mean-square error,
a central limit theorem, concentration, a finite-sample confidence bound, or an algorithm-specific
claim. These are inequivalent propositions. Choosing the sample-mean estimator, iid sampling, an
integral interpretation, or a familiar rate would invent or substitute mathematics absent from
the catalog.

Crossref metadata for Metropolis and Ulam's 1949 article "The Monte Carlo Method" is recorded as a
historical source-family lead only. Its authorship and date differ from this target's metadata, and
the repository separately owns a 1949 Metropolis/Ulam statistical-physics Monte Carlo target. No
paper text, exact theorem, assumptions, proof boundary, correction audit, or independent review is
admitted here.

## Formal boundary

`IntakeProbe.lean` elaborates adjacent pinned probability APIs for expectations, independence,
identical distributions, variance, Chebyshev bounds, and strong laws. Those interfaces can support
some future Monte Carlo encodings but do not select this target. In particular, the pinned strong
law belongs to separately cataloged law-of-large-numbers targets and cannot silently become the
Monte Carlo theorem.

The canonical human statement and Lean expression remain null. The provisional root vector is
`[H5, M4, R4]`: the received catalog wording is not yet a stable proposition; no source-identical
formal target or proof body is credited; and no readable proof can attach to an unfrozen root.
`H5` does not refute established Monte Carlo results. All six downstream tasks remain open. No
accepted state, audit completion, theorem completion, accepted receipt, or master acceptance is
claimed.
