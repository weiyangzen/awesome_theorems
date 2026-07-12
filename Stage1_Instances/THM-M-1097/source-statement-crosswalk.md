# Source-statement crosswalk

## Repository source boundary

`Docs/researches/math_theorems.md` records Sean Meyn and Richard Tweedie, the year 1993, and only the
phrase "stability of Markov chains". `Docs/Stage0_Blueprint.md` repeats that phrase while leaving the
definitions, hypotheses, proof route, axioms, and machine artifacts open. Its `已验证` label is
explicitly untrusted under rev-5.6. These records identify a body of theory, not an exact theorem.

## Candidate primary source

- Sean P. Meyn and Richard L. Tweedie, *Markov Chains and Stochastic Stability*, Springer-Verlag,
  1993 (first edition). This is the primary monograph candidate matching the repository authors and
  year. The exact chapter, theorem number, page, definitions, edition wording, correction history,
  and errata have not been inspected in this intake.

The later second edition (Cambridge University Press, 2009) may help resolve notation and
corrections, but it may not silently replace the 1993 source. The statement phase must choose one
numbered theorem and record any cross-edition differences. This bibliographic locator is discovery
evidence only, not `H0` evidence.

## Crosswalk

| Repository/source phrase | Provisional mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "Markov chain" | general-state-space time-homogeneous chain | measurable space and Markov transition kernel with iterates | included; exact model open |
| "stability" | recurrence, invariant measure, or convergence property | one source-defined predicate or bound | ambiguous; exact conclusion open |
| Meyn-Tweedie | drift/minorization framework | Lyapunov function, kernel drift, small/petite set | likely family components; theorem open |
| irreducibility | source-specific `psi`-irreducibility/Harris hypothesis | reference measure and reachability predicate | hypothesis and encoding open |
| invariant law | invariant probability and possibly uniqueness | probability measure and kernel invariance | inclusion depends on selected theorem |
| convergence | total variation or weighted norm, possibly geometric | measure/kernel distance and quantified rate | inclusion depends on selected theorem |
| `已验证` | repository screening label | accepted source review or kernel receipt | no credit |

## Required source and machine audit

Before `H0`, an independent reviewer must inspect a stable edition, record theorem/page and all
referenced definitions, verify every hypothesis and conclusion, check errata and cross-edition
changes, and approve a row-by-row mapping to the canonical Lean expression. In particular, the
review must not conflate positive recurrence, positive Harris recurrence, ergodicity, geometric
ergodicity, and existence of an invariant probability.

No repo-local or external Lean declaration is accepted at intake. The later anchor audit must search
the pinned mathlib revision and credible Lean 4 projects, then record exact modules and declaration
types, immutable revisions, unresolved proof holes, added axioms, terminal proof bodies, and
dependency feasibility.
A negative repository name search at intake is not a formal-candidate audit.
