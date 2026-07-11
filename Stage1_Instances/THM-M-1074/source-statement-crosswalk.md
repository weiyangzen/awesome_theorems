# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` names "compound Poisson process," attributes it nonspecifically
to many mathematicians in the twentieth century, and gives only "a generalization of the Poisson
process" as its statement. `Docs/Stage0_Blueprint.md` repeats this metadata and leaves definitions
and assumptions open. These records establish target provenance but not one theorem, a human proof,
or a machine-checked result. Their `已验证` label is untrusted under rev-5.6.

## Candidate mathematical sources

- J. F. C. Kingman, *Poisson Processes*, Oxford Studies in Probability 3, Clarendon Press (1993).
  This is a modern monograph candidate for the marked/compound Poisson construction; the exact
  chapter, proposition, hypotheses, and edition corrections require direct inspection.
- David Applebaum, *Levy Processes and Stochastic Calculus*, second edition, Cambridge University
  Press (2009). This is a modern candidate for the compound-Poisson example and its Levy-process
  characterization; the exact numbered result, conventions, and errata require direct inspection.

These are discovery anchors, not `H0` evidence. Intake does not claim that either source packages
all rows below into one theorem.

## Crosswalk

| Repository/source phrase | Intended mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "compound Poisson process" | random sum driven by Poisson arrivals | time-indexed random variables and a finite sum through `N_t` | family included; encoding open |
| "Poisson process" | rate-`lambda` counting process | concrete counting-process law and increment properties | included; API open |
| "compound" | iid random jump sizes independent of arrivals | identically distributed sequence plus joint independence | included; state space open |
| process characterization | stationary independent increments and `X_0 = 0` | process-level independence and equality-in-law statements | source-scope decision open |
| marginal law | Poisson mixture of convolution powers of the mark law | distributions, convolution, pushforward, and infinite mixture | source-scope decision open |
| characteristic function | `exp(lambda*t*(phi_Y(u)-1))` | expectation/integral of complex exponential and formula equality | source-scope decision open |

## Lean and evidence boundary

A repository and available pinned-mathlib text search for `compound Poisson`, `CompoundPoisson`, and
`PoissonProcess` returned no theorem-specific declaration during intake. This bounded negative search
is not the precommitted formal-candidate audit and establishes only that no obvious local anchor was
found. The anchor phase must inspect the pinned library by relevant probability, independence,
finite-sum, convolution, and characteristic-function APIs and must audit credible external Lean 4
projects at immutable revisions.

Before `H0`, an independent reviewer must select and inspect a stable source edition, record exact
theorem/page, definitions, every hypothesis and conclusion, proof boundaries, and errata, and approve
a row-by-row mapping to the elaborated Lean target. If no source supports a unique substantive
proposition matching this family, the statement phase must report that blocker rather than silently
choosing a narrower theorem.
