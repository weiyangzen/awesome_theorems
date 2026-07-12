# Lean 4 anchor audit

## Scope and immutable environment

This audit compares the frozen declaration
`Stage1Instances.THM_M_1108.CanonicalStatement` with repo-local Lean sources, the complete source
tree of the pinned mathlib checkout at commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, and public Lean 4 discovery results inspected on
2026-07-12. The Lean toolchain is `v4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`. No dependency was fetched or updated.

The search vocabulary covered the named theorem and authors, Tracy--Widom, Painleve,
Hastings--McLeod, Airy, longest/increasing subsequences, random permutations, Young tableaux, and
Robinson--Schensted. Repo-local and pinned-mathlib searches found no declaration matching the
theorem, its limiting distribution, or its permutation asymptotic.

## Candidate inventory

| Pinned module / declaration | Exact type role | Audit decision |
|---|---|---|
| `Mathlib.Data.Fintype.Perm`: `Equiv.Perm`, `Fintype.card_perm` | finite permutation carrier and cardinality | infrastructure only; no LIS law or limit |
| `Mathlib.Combinatorics.Young.SemistandardTableau`: `YoungDiagram`, `SemistandardYoungTableau` | diagram/tableau data | infrastructure only; no RSK or LIS/first-row bridge found |
| `Mathlib.Probability.CDF`: `ProbabilityTheory.cdf`, `cdf_eq_real` | CDF of a real probability measure | infrastructure only; no Tracy--Widom construction or BDJ convergence |
| `Mathlib.Probability.Distributions.Poisson.PoissonLimitThm`: `binomial_tendsto_poissonPMFReal_atTop` | a genuine distributional-limit analogue | not reusable: binomial-to-Poisson masses have the wrong models and limit |

`AnchorCandidates.lean` elaborates every declaration named above against the pinned environment.
None has the type of `CanonicalStatement`, and none supplies a terminal proof body for it.

## External Lean 4 discovery

Sourcegraph public global code search returned zero Lean matches for `TracyWidom`, `Tracy-Widom`,
`Painleve`, `Baik`, `longest increasing subsequence`, and `Hastings--McLeod`. Its reported default
excluded archived repositories and forks. GitHub's public repository search API likewise returned
zero repositories for `Tracy-Widom Lean`, `Painleve language:Lean`, and
`longest increasing subsequence Lean`. GitHub code search was not used as evidence because its API
requires authentication in this environment.

These services are discovery aids, not exhaustive immutable archives. Because they yielded no
candidate repository, there is no external revision, module, declaration, toolchain, dependency
graph, license, proof-body provenance, placeholder scan, or axiom profile to pin and validate.
The truthful result is therefore an empty external-candidate inventory, not a claim that no Lean
formalization can exist anywhere.

## Classification and boundary

No exact mathlib theorem and no credible external Lean 4 theorem-level candidate was found. The
human theorem is known, but the frozen Lean target has no machine closure, so its current debt is
`formalization_debt` and its machine status remains `not_repo_local_closed` (`M4`). This audit does
not establish `H0`, `R0`, audit completion, proof completion, or theorem completion.

## Validation record

Base revision: `84447940cf503cb83cb4fd16670216427c19bf18`.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1108` | exit 0; rank 548, planned, L0/rework_required, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; exact manifest revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| pinned-tree `rg` searches recorded above | exit 0/expected no-match; no theorem-level anchor found |
| Sourcegraph and GitHub API searches recorded above | exit 0; zero public discovery matches/repositories |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1108/AnchorCandidates.lean)` | exit 0; all seven pinned candidate declarations elaborated with the expected types |
| `python3 -m json.tool Stage1_Instances/THM-M-1108/anchor-audit.json` | exit 0 |
| scoped Python anchor-audit assertions | exit 0; `anchor audit invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1108 .stage1-worker-selftest.json` | exit 0; no output |

Validation is node-scoped and nonrelease. It reuses the clone's pre-existing `.lake` link and does
not mutate pinned artifacts.
