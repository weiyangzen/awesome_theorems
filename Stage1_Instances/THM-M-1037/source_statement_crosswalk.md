# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Strong solution | B. Oksendal, *Stochastic Differential Equations: An Introduction with Applications*, 6th ed., Springer (2003), Chapter 5, section 5.2 | a structure fixing the stochastic basis, initial variable, Brownian driver, adapted process, and integral equation | Bibliographic anchor located; exact definition/page and edition text require primary-source verification |
| Weak solution | I. Karatzas and S. E. Shreve, *Brownian Motion and Stochastic Calculus*, 2nd ed., Springer (1991), Chapter 5, section 5.3 | an existential structure whose stochastic basis and Brownian driver are witness data | Bibliographic anchor located; precise assumptions and definition numbering require primary-source verification |
| Strong implies weak | Forget the requirement that the solution be measurable with respect to the prescribed noise/initial data while retaining the same witness | candidate `StrongSolutionData.toWeakSolutionData` in historical `S1_M_230.lean` | Plausible definitional bridge, but the historical fields abstract the stochastic integral and equation as propositions; it is not an accepted exact source formalization |
| Existence/uniqueness relations | Yamada-Watanabe results distinguish weak existence, pathwise uniqueness, and strong existence | none in this intake | Explicitly excluded from this target unless a primary source proves that this is the intended manifest claim |

The repository's legacy description is `SDE解的不同概念` (different concepts of SDE solutions).
That is a topic, not a truth-valued theorem statement. It does not specify coefficients, state and
noise dimensions, filtration completion, initial-condition convention, solution equality, or
whether the intended result is a definition, implication, existence theorem, or equivalence.
Consequently this intake does not invent an exact claim.

The statement phase must first select and verify a primary-source edition and pinpoint definition
or proposition. It must then record all assumptions, check errata, serialize the normalized Lean
expression, and mutation-test the distinction between prescribed-noise measurability and witness
probability-space data. The adjacent manifest item `THM-M-1038` is Yamada-Watanabe, which is further
evidence against silently substituting that theorem here.

Discovery links (not immutable evidence receipts):

- Oksendal book DOI: <https://doi.org/10.1007/978-3-642-14394-6>
- Karatzas-Shreve book DOI: <https://doi.org/10.1007/978-1-4612-0949-2>

No `H0` or exact-statement claim is made. Edition files/hashes, pinpoint pages, assumption mapping,
errata search, and independent review remain open.

