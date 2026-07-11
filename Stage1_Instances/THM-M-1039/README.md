# THM-M-1039 rev-5.6 intake

This is the `planned` rev-5.6 instance for the Markov property of solutions of
stochastic differential equations. The repository gloss "SDE solutions are
Markov" is not by itself a theorem: the equation, coefficient regularity,
solution concept, filtration, uniqueness hypothesis, and precise Markov
conclusion all matter. This intake freezes the conventional time-homogeneous
Itô-SDE theorem family without pretending those choices have already been
encoded in Lean.

The intended root says that a well-posed time-homogeneous Itô SDE driven by
Brownian motion has a Markov solution family, with transition kernel determined
by the solution started from each state. Strong Markov, time-inhomogeneous,
weak-solution, and martingale-problem variants are related branches, not silent
substitutes for that root.

The mathematical boundary is in `scope-map.md`, structured intake data is in
`intake.json`, the source relationship is in `source-statement-crosswalk.md`,
and the downstream open phases are in `task-dag.json`.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M4, R3]`. The first
failed gate is exact source-statement identification: no primary-source
edition/page/theorem and full premise crosswalk has yet been accepted. The Lean
statement gate is independently open. No theorem completion or kernel evidence
is claimed.

