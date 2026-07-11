# Source-statement crosswalk

## Candidate sources

- E. B. Dynkin, *Markov Processes*, volumes I-II, Springer (1965), for the generator/martingale
  characterization tradition. Exact edition, theorem, page, hypotheses, and translation wording
  have not been inspected.
- D. W. Stroock and S. R. S. Varadhan, *Multidimensional Diffusion Processes*, Springer (1979),
  for martingale problems and well-posedness/Markov consequences. This may instead correspond to
  the adjacent diffusion-specific `THM-M-1049`; no theorem from it is adopted here.
- S. N. Ethier and T. G. Kurtz, *Markov Processes: Characterization and Convergence*, Wiley
  (1986), Chapter 4, as a modern stable source candidate. Exact theorem/page and errata remain open.

These are discovery anchors only, not `H0` evidence. The repository metadata says "1969" and names
Stroock/Varadhan but gives no bibliographic item or theorem, so it cannot disambiguate the target.

## Crosswalk

| Repository phrase | Mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| martingale problem | compensated test-function process | process, operator, time integral, martingale predicate | included; conventions open |
| Markov process | law with conditional transition property | filtration/conditional-law Markov predicate | included; exact strength open |
| characterization | implication or equivalence via well-posedness | typed theorem relating solution laws and Markov property | included; direction open |
| proposed in 1969 | historical attribution | inspected bibliographic evidence | unverified metadata |
| "verified" | alleged formal status | exact Lean declaration and proof provenance | no acceptable evidence located at intake |

## Statement gate

Before statement acceptance, a reviewer must inspect a fixed source edition, record theorem and
page, definitions and errata, and map every quantifier and hypothesis to the canonical Lean target.
The chosen theorem must remain distinct from `THM-M-1049`. If the repository wording cannot select
one non-substituted theorem, the statement phase must remain blocked rather than manufacture one.
