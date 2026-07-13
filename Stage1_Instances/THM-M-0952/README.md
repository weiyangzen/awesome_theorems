# THM-M-0952 rev-5.6 intake

`THM-M-0952` is the combinatorics catalog item "Elekes theorem." The catalog supplies the
attribution Gyorgy Elekes, the year 1997, and only the gloss "a lower bound for sumsets and product
sets," plus an untrusted `verified` label. Those fields identify the theorem family but do not
freeze its domain, hypotheses, exponent, constant, quantifiers, or boundary cases.

## Intake result

This dossier records a fail-closed `planned` instance. The matching primary paper is Gyorgy Elekes,
"On the number of sums and products," *Acta Arithmetica* 81.4 (1997), 365-367, DOI
`10.4064/aa-81-4-365-367`. Its Theorem 1 on printed page 365 states that an absolute constant
`c > 0` exists such that every `n`-element finite subset `A` of the nonzero reals satisfies
`c * n^(5/4) <= max(|A + A|, |A * A|)`. The proof on page 366 reduces the result to the stated
Szemeredi-Trotter incidence bound. This is a strong source candidate, but the repository does not
cite or adopt it, no corrections or errata search has been accepted, and no independent reviewer
has approved the source-to-statement mapping. Intake therefore does not promote it to the canonical
claim or to `H0`.

## Formal boundary

Pinned mathlib expresses finite real sumsets, product sets, cardinalities, maxima, and real powers.
`IntakeProbe.lean` elaborates those adjacent interfaces and a proposition-valued candidate target
shape only. A bounded local search found no named Elekes, Szemeredi-Trotter, or exact sum-product
lower-bound declaration. These observations are discovery inputs, not the later exhaustive anchor
audit and not proof evidence.

The planned root vector is `[H1, M3, R4]`: a complete published proof and an exact candidate
statement are located, but source adoption, premise mapping, correction status, encoding decisions,
and independent review remain open; only adjacent Lean interfaces and an unproved candidate shape
elaborate; and no source-faithful readable proof reconstruction is accepted. All six downstream
tasks remain open. Neither audit completion nor theorem completion is claimed.

