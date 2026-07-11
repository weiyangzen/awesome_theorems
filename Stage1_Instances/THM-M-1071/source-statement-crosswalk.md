# Source-statement crosswalk

## Candidate sources

- Kiyosi Ito, "On stochastic processes (Infinitely divisible laws of probability)," *Japanese
  Journal of Mathematics* 18 (1942), 261-301. This is a historical primary-source candidate. The
  exact result number, original hypotheses, terminology, and later corrections require inspection
  of a stable scan; the citation is not accepted `H0` evidence.
- David Applebaum, *Levy Processes and Stochastic Calculus*, second edition, Cambridge University
  Press, 2009, Theorem 2.4.16 ("The Levy-Ito decomposition"). This is a modern proof and statement
  candidate. Its page, premise-level mapping, edition errata, and relation to the historical source
  remain to be independently checked.
- Ken-iti Sato, *Levy Processes and Infinitely Divisible Distributions*, Cambridge Studies in
  Advanced Mathematics 68, Cambridge University Press, 1999, Chapter 4. This is a convention and
  cross-check candidate, not yet a pinpoint proof record for this dossier.

These records are discovery anchors. Intake does not infer an exact statement from the theorem name
or elevate the repository's historical status label.

## Crosswalk

| Repository phrase | Intended source component | Required Lean component | Intake status |
|---|---|---|---|
| Levy process | cadlag process starting at zero with stationary independent increments | process, filtration, laws, and increment predicates | included; encoding open |
| deterministic drift | truncation-dependent finite-variation linear term | vector parameter and time scaling | included; convention open |
| Brownian part | centered Gaussian continuous component with covariance | multidimensional Brownian process and covariance operator | included; API open |
| small jumps | compensated integral on the cutoff neighborhood of zero | jump measure, compensator, stochastic integral, limiting construction | included; convergence open |
| large jumps | uncompensated Poisson integral outside the cutoff | Poisson random measure and finite-activity integral | included; API open |
| decomposition | equality of the original process with the four components | pathwise equality/indistinguishability for all times | included; equality mode open |
| independence | independence of Gaussian and jump components, with disjoint jump regions | independence of processes/random measures | included; exact source premises open |

## Evidence boundary

The pinned repository toolchain is Lean `v4.29.0` and the manifest pins mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, but no mathlib checkout or declaration was inspected or
credited in this intake. The statement and anchor-audit phases must record exact modules,
declaration types, revisions, placeholders, axioms, and terminal proof provenance. Before `H0`, a
reviewer must verify a stable edition, theorem/page, assumptions, definitions, corrections, and the
row-by-row source-to-Lean map.
