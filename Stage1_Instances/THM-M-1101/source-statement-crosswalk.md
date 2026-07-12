# Source-statement crosswalk

## Repository metadata

`Docs/researches/math_theorems.md` records only Metropolis/Hastings, 1970, and "MCMC's basic
algorithm". `Docs/Stage0_Blueprint.md` repeats that gloss and explicitly leaves definitions,
hypotheses, proof, axioms, and machine artifacts open. Its `已验证` field is untrusted intake
metadata under rev-5.6 and is not `H0` or kernel evidence.

## Identified primary-source candidates

- W. K. Hastings, "Monte Carlo Sampling Methods Using Markov Chains and Their Applications",
  *Biometrika* 57(1) (1970), 97-109, DOI `10.1093/biomet/57.1.97`.
- N. Metropolis, A. W. Rosenbluth, M. N. Rosenbluth, A. H. Teller, and E. Teller, "Equation of
  State Calculations by Fast Computing Machines", *The Journal of Chemical Physics* 21(6) (1953),
  1087-1092, DOI `10.1063/1.1699114`.

The first article's title, author, journal coordinates, date, and DOI were checked against the
Crossref publisher deposit during intake. The second is recorded to prevent the repository's joint
attribution from erasing the symmetric-proposal predecessor; its content was not inspected here.
Neither paper's exact theorem/equation, definitions, assumptions, proof, edition image, or errata
was reviewed. These are `H1` discovery anchors, not an `H0` source crosswalk.

## Crosswalk

| Repository/source phrase | Mathematical component potentially intended | Required Lean component | Intake status |
|---|---|---|---|
| "Metropolis-Hastings" | Hastings generalization of an accept/reject chain | target measure, proposal kernel, acceptance function, stay-put mass | family identified; exact construction open |
| "algorithm" | transition-generation procedure | mathematical kernel versus executable sampler interface | representation and computation boundary open |
| "MCMC" | Markov chain used for sampling | Markov property, initial law, iterated kernel | included context; quantifiers open |
| "basic" | commonly a correctness argument | one exact detailed-balance/invariance/convergence proposition | conclusion unidentified |
| Metropolis/Hastings | 1953 predecessor and 1970 generalization | source revision and checked specialization relation | bibliographic candidates only |
| `已验证` | repository screening label | accepted source-review or kernel receipt | no credit |

## Lean and source boundary

Pinned mathlib contains `ProbabilityTheory.Kernel.IsReversible` and a theorem that a reversible
Markov kernel leaves a measure invariant in `Mathlib/Probability/Kernel/Invariance.lean`. This is
relevant infrastructure only. It does not construct a Metropolis-Hastings kernel, discharge its
detailed-balance calculation, or identify which source conclusion is the root. No formal candidate
is accepted at intake.

Before `H0`, an independent reviewer must inspect stable copies of the selected primary result,
record exact section/equation/theorem and page, map every definition and assumption, check errata
and the 1953-to-1970 scope difference, and approve the canonical statement mapping. Machine closure
is a separate downstream question requiring an elaborated exact expression and terminal proof-body
evidence.

