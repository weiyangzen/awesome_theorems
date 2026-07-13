# THM-M-0482 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog label
`切比雪夫估计` (Chebyshev estimates). The repository supplies only the gloss `素数分布的上下界估计`
(upper and lower estimates for the distribution of primes), an attribution to Pafnuty Chebyshev,
and the year 1850. Those data identify a classical prime-distribution result family, but not one
stable truth-valued proposition.

The wording does not choose the ordinary prime-counting function, Chebyshev's `theta`, or
Chebyshev's `psi`; an exact inequality or asymptotic formulation; constants and thresholds; a
natural or real argument; endpoint conventions; or whether the upper and lower bounds form one
conjunction. Chebyshev's 1852 *Memoire sur les nombres premiers*, presented in 1850, is a credible
primary-source lead, but no exact formula and definition package from it is admitted as the
catalog's root at intake.

The provisional catalog-target vector is `[H5, M4, R4]`. Here `H5` classifies the received wording
as not yet a stable proposition; it does not refute Chebyshev's theorems. `IntakeProbe.lean` checks
only adjacent interfaces in pinned mathlib. That library contains several upper bounds for
`theta`, `psi`, and prime counting, while its Chebyshev module explicitly lists the lower bound as
future work. These discovery observations do not select or prove the unidentified two-sided root.

`instance.json` is the structured scope authority. The scope map and source-statement crosswalk
freeze the unresolved choices, primary-source lead, formal boundary, and exclusions;
`task-dag.json` leaves all six downstream phases open. This is a self-tested worker proposal only.
No canonical statement, accepted source proof, exact formal proof body, H0, M0, R0, accepted
execution state, audit completion, theorem completion, or master acceptance is claimed.
