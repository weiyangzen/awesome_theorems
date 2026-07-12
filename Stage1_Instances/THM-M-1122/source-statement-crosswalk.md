# Source-statement crosswalk

## Repository record and candidate source

The repository inventory gives the title "Schramm-Loewner evolution", Oded Schramm, the year 2000,
and the gloss "random curves of critical phenomena". Its `已验证` field is untrusted under rev-5.6.
It gives no numbered result, model, domain, normalization, assumptions, parameter, or conclusion,
so it does not identify one proposition.

The historical primary candidate matching the author and year is Oded Schramm, *Scaling limits of
loop-erased random walks and uniform spanning trees*, **Israel Journal of Mathematics** 118 (2000),
221-288, DOI `10.1007/BF02803524`. This intake records the paper only as a discovery anchor. An
immutable edition has not yet been inspected result by result, and no exact theorem/proposition,
page, hypotheses, normalization, corrections, or modern-equivalence bridge has been approved.
Consequently the characterization above receives family-level intake scope but not `H0` credit.

## Crosswalk

| Repository/source phrase | Mathematical component to freeze | Required Lean component | Intake status |
|---|---|---|---|
| "Schramm-Loewner evolution" | chordal or radial Loewner chain and normalization | domains/hulls, conformal maps, driving-function relation | family identified; variant open |
| "random curves" | curve law, topology, filtration, endpoints, and reparametrization quotient | measurable curve/hull space and probability measure | all exact choices open |
| "critical phenomena" | conditional universal characterization or a particular model limit | exact hypotheses and quantified conclusion | too broad for statement credit |
| conformal invariance | equality/covariance of transported curve laws | conformal maps and pushforward-measure equality | intended hypothesis; formulation open |
| domain Markov property | conditional law after an initial segment | filtration, stopping/deterministic times, conditional probability | intended hypothesis; formulation open |
| Brownian driving | continuous independent stationary increments and variance convention | Loewner driver law equals scaled Brownian law | intended conclusion; constants open |
| Schramm / 2000 | historical attribution | bibliographic provenance only | candidate paper identified; pinpoint review open |

## Human and machine boundary

A repository-wide text search found no existing target-specific theorem artifact for
`THM-M-1122`; only the source inventory, generated target projections, and neighboring SLE entries
were present. This intake does not perform the later exhaustive mathlib/external formal-anchor audit
and makes no assertion that pinned mathlib supplies the required Loewner-chain, conditional-law, or
Brownian-characterization interfaces.

Before `H0`, an independent reviewer must inspect an immutable primary edition, choose a pinpoint
result, map every definition and assumption, check corrections and normalization conventions, and
approve the row-by-row mapping. Before statement credit, the selected claim must map to an
elaborated Lean target without replacing the characterization by the SLE definition, assuming its
conclusion, or importing a lattice-model scaling-limit theorem.
