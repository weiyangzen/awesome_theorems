# THM-M-0955 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-0955`, the catalog entry
named `Bose-Chowla定理` (Bose-Chowla theorem). The repository gives only the gloss `Sidon集的构造`
("construction of Sidon sets"), attributes it to Bose and Chowla, dates it to 1960, and marks it
`已验证`. Those fields identify an additive-combinatorics construction family, not a proposition
with fixed domains, binders, hypotheses, and a conclusion. The verified label is untrusted metadata
and supplies no source or proof credit.

Publisher and Crossref records identify R. C. Bose and S. Chowla, *Theorems in the additive theory
of numbers*, Commentarii Mathematici Helvetici 37 (1962), 141-147, DOI
`10.1007/BF02566968`. The publisher summary says that the paper extends earlier results on
difference sets and `B_2` sequences. This is a strong primary-source identity lead, but the full
theorem text was not available in the inspected subscription preview. Its 1962 publication date
also conflicts with the catalog's unexplained 1960 date. No exact theorem, definitions, proof
passage, correction history, or independent source review is admitted at intake.

The name can refer to a `B_2`/Sidon construction or to a more general `B_h` construction. Even the
common `B_2` reading leaves proposition-changing choices: cyclic group versus integer interval,
the order of the ambient group, prime versus prime-power parameters, set size, ordered versus
unordered representations, repeated summands, and an existence versus explicit-construction
conclusion. Intake does not choose a remembered textbook version or silently merge these variants.

Pinned mathlib supplies adjacent Freiman, additive-energy, finite-field, and cyclic-group APIs.
`IntakeProbe.lean` authenticates those interfaces only. A bounded search found no Sidon,
Bose-Chowla, or `B_h` construction declaration in pinned mathlib or repository Lean sources. The
provisional vector is `[H1, M4, R4]`: an authoritative bibliographic lead is known but the exact
source statement remains unaudited; no usable source-identical formal artifact is credited; and no
source-faithful readable proof exists.

`instance.json` is the structured scope authority, and `task-dag.json` keeps all six downstream
phases open. No canonical proposition, H0, M0, R0, accepted execution state, audit completion,
theorem completion, or master acceptance is claimed.
