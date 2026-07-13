# THM-M-0978 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog entry
`Hoeffding inequality`. The repository places it in enumerative combinatorics, gives only the
gloss `concentration of sums of bounded random variables`, attributes it to Wassily Hoeffding in
1963, and labels it `verified`. Under rev-5.6 that label is untrusted inventory metadata, not an
exact proposition, source review, or proof receipt.

The catalog contains a second record, `THM-M-0994`, with the Chinese transliteration of the same
name, the same author, year, and literal gloss. That probability-theory target has a legacy slot
and extensive current artifacts, but neither category nor earlier scheduling allocates the shared
mathematics to this ID. Its artifacts and the historical `S1_M_274.lean` wrapper are discovery
inputs only. This intake records the duplicate identity instead of importing another target's
statement or proof state.

A stable North Carolina State University repository scan of Hoeffding's paper, *Probability
Inequalities for Sums of Bounded Random Variables*, was inspected. Theorem 2, printed page 6,
equation (2.10), gives the one-sided upper-tail bound for the average of independent random
variables with possibly unequal pointwise bounds. The proof appears in Section 3 on printed pages
12-13. This is a strong primary-source lead, but the catalog does not cite it or select among the
paper's several inequalities. Exact source-to-catalog selection, correction and errata review,
pointwise versus almost-sure transport, average versus centered-sum normalization, boundary cases,
duplicate-ID allocation, and independent review remain open. Thus the human status is `H1`, not
`H0`.

Pinned mathlib exposes exact-topic Hoeffding and Hoeffding-lemma declarations, authenticated by
`IntakeProbe.lean`. They are usable formal candidates, so the provisional machine status is `M3`,
but no canonical target, checked source transport, or proof-body credit is accepted at intake. The
provisional root vector is `[H1, M3, R4]`.

`instance.json` is the planned scope authority, while `task-dag.json` keeps all six downstream
phases open. No canonical proposition, H0, M0, R0, accepted execution state, audit completion,
theorem completion, or master acceptance is claimed.
