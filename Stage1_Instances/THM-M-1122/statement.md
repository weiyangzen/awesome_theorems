# Statement freeze

Item: `S56-M-1122-STATEMENT`

`Statement.lean` freezes Theorem 1.3 of Oded Schramm, *Scaling limits of loop-erased random walks
and uniform spanning trees*, Israel J. Math. 118 (2000), 221-288, pp. 226-227 (arXiv
`math/9904022`, pp. 6-7). Conditional on Conjecture 1.2, the curve obtained from equations
(1.1)-(1.3), driven by circle Brownian motion at time `-2t`, has the same distribution as the LERW
scaling limit from `0` to the boundary of the unit disk.

## Encoding boundary

The pinned library has measure laws but no target-ready LERW scaling-limit or radial Loewner API.
Those source-specific objects are therefore explicit parameters, with `isUniformCircleBrownian`
owning Brownian motion begun from the uniform circle law and `loewnerSolution` owning the
full equations, normalization, trace construction, and adjoining of `{0}`. This does not assume the
conclusion: the conclusion remains `IdentDistrib sigma lerwScalingLimit`. `NegativeTime` fixes
`t <= 0`, and the source constant `-2t` is visible in the target.

The direct import is only `Mathlib.Probability.IdentDistrib`. The canonical declaration is
`Stage1Instances.THM_M_1122.SchrammLoewnerEvolutionTarget`; it is a `def : Prop`, not a proof.
`target_iff_expanded` checks the expanded transport. Mutations record that dropping Conjecture 1.2
or changing the Brownian time scale changes the proposition.

This statement gate does not claim a Loewner definition, a proof of Conjecture 1.2, Theorem 1.3,
modern chordal SLE characterization, source-review acceptance, or theorem completion.
