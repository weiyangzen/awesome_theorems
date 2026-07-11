# Source-statement crosswalk

| Claim component | Human source candidate | Lean candidate | Intake assessment |
|---|---|---|---|
| A unique solution of a time-homogeneous SDE is Markov | B. Oksendal, *Stochastic Differential Equations: An Introduction with Applications*, Springer, chapter on diffusion processes and the Markov property | none identified | Primary textbook candidate located; edition-specific theorem/page, exact assumptions, and corrections remain to be audited |
| Restart solution at deterministic time from its current state | same theorem/proof family; also I. Karatzas and S. Shreve, *Brownian Motion and Stochastic Calculus*, Springer, SDE chapter | future restart/flow bridge | Candidate proof mechanism only; no source node or formal declaration is credited |
| Future Brownian increments are independent of the past | standard Brownian independent-increments result used by the Markov proof | mathlib probability/Brownian APIs require later search | A general ingredient is not an exact root anchor |
| Equality of restarted and original solutions | pathwise uniqueness/uniqueness-in-law theorem, depending on the chosen solution formulation | no exact declaration identified | The uniqueness notion is a material premise and cannot be weakened silently |
| Conditional expectation and transition-kernel formulations agree | standard regular-conditional-law/Markov-kernel theory on suitable measurable state spaces | mathlib conditional expectation and kernel APIs require later search | Transport is open and depends on measurability and state-space hypotheses |
| Strong Markov property | textbook strong-Markov theorem for diffusions, under additional regularity/usual conditions | none identified | Stronger neighboring theorem; excluded from root unless independently frozen and proved |

The repository source label `已验证` and gloss `SDE解的马尔可夫性质` do
not identify a precise proposition and receive no proof or source-fidelity
credit. In particular, existence without uniqueness does not imply that every
chosen solution is Markov, and a time-dependent coefficient generally produces
a time-inhomogeneous Markov family (or requires adjoining time to the state).

No `H0` claim is made. The source-audit phase must record an immutable edition,
pinpoint theorem and page, every premise and convention, an errata/correction
search, and independent review before selecting the canonical source statement.

