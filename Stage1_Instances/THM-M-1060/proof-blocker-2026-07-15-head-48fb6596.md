# THM-M-1060 proof-phase execution at 48fb6596

Item: `S56-M-1060-PROOF`

Execution date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `48fb6596b1844f4183c411142415d872ff21e842`

Base tree: `eb8dfff0e90b5ce5b11ac2096777060d62874064`

## Verdict

`no_state_change`; the exact root remains blocked. This execution adds three placeholder-free proof bodies to
`Proof.lean`: arbitrary one-time marginal extraction, its exact Gaussian-law
specialization, and a finite-dimensional bridge from the frozen
`IsWienerMeasure` predicate to mathlib's `IsGaussianProcess` interface. They
materially advance the Wiener-normalization branch, but no body proves an LDP
bound, goodness of the rate, or the exact target
`Stage1Instances.THM_M_1060.SchilderTarget`.

The lifecycle remains `planned`, the root vector remains
`[H2, M3, R4] -> [H2, M3, R4]`, and no frozen obligation is closed. The new
bodies are partial work on `M1060-N-WIENER`; they do not satisfy that node's
full increment, covariance, and path-law output.

## Implemented Bodies

| Declaration | Checked contribution | Open boundary |
|---|---|---|
| `oneTimeVarianceAndLaw` | derives the variance and law of an arbitrary one-time path marginal directly from `IsWienerMeasure` | no joint increment or LDP conclusion |
| `oneTimeLaw` | identifies the marginal exactly as `gaussianReal 0 t` | no path-space estimate |
| `isGaussianProcess_of_isWienerMeasure` | proves every finite restricted coordinate vector is Gaussian by checking all continuous linear functionals against the frozen finite-dimensional laws | Gaussianity alone supplies no Schilder/LDP theorem |

All three declarations elaborate at trust level zero and report exactly
`propext`, `Classical.choice`, and `Quot.sound`; there is no `sorryAx` or
unreviewed axiom. The Gaussian-process bridge is a real normalization result,
not an assumed analytic terminal package. Because the frozen node also
requires increment, covariance, and usable path-law facts for the selected
polygonal proof, no full obligation or receipt is claimed.

## Failed Gate And Remaining Cut

The first failed implementation gate remains `M1060-N-WIENER`: a complete
increment/covariance/path-law package has not yet been derived. More
decisively, the pinned closure contains no finite Gaussian LDP, Brownian
exponential modulus estimate, exponential-equivalence transfer, exact
Cameron-Martin rate identification, lower-semicontinuity proof, or compact-
sublevel proof.

The frozen implementation cut is `M1060-L-GAUSSIAN`, `M1060-L-MODULUS`,
`M1060-L-EXP-EQUIV`, `M1060-L-RATE-ID`, `M1060-L-RATE-LSC`, and
`M1060-L-SUBLEVEL-BOUND`. The immediate semantic terminal frontier remains
`M1060-T-LOWER`, `M1060-T-UPPER`, and `M1060-T-GOOD`. Conditional conjunction
composition in `ObligationTree.lean` does not inhabit these packages.

## Validation

All commands ran in this worker clone using the automation-provided existing
`.lake` symlink to canonical pinned artifacts. No `lake update`, `lake build`,
dependency clone/fetch, network access, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1060` | 0 | rank 503; planned; L0/rework-required; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1060/check_obligation_tree.py` | 0 | 21 obligations and 83 typed edges passed; denominator `32d2df11...b2a3f74`; recorded root open |
| `bash Stage1_Instances/THM-M-1060/check_proof.sh` | 0 | both isolated elaboration stages succeeded; all eight partial bodies elaborated; every printed axiom set is exactly `propext`, `Classical.choice`, and `Quot.sound` |
| `python3 Stage1_Instances/THM-M-1060/check_proof.py` | 0 | ownership, source hashes, frozen inputs, pins, receipt, blocker, open-root boundary, dirty paths, and worker packet agreed |
| `cd Formalizations/Lean && lake env lean --trust=0 ../../Stage1_Instances/THM-M-1060/Statement.lean` | 0 | exact canonical target elaborated and printed |
| `cd Formalizations/Lean && lake env lean --trust=0 ../../Stage1_Instances/THM-M-1060/ObligationTree.lean` | 0 | both conditional composers elaborated at their frozen signatures |
| token-anchored prohibited-device scan over owned `*.lean` | 1 | expected no-match exit; no `sorry`, `admit`, axiom declaration, unsafe/oracle, or equivalent prohibited construct |
| pinned-mathlib topical scan for Schilder/LDP/Cameron-Martin/exponential equivalence/Laplace principle | 0 | one unrelated AddCircle documentation hit; no probabilistic terminal declaration |
| `git diff --check -- Stage1_Instances/THM-M-1060` | 0 | no whitespace errors |

The final source hashes are `d2bfdc20...04581a` for `Statement.lean`,
`cb01f4a6...add05` for `obligation-registry.json`, and
`9d5626f0...f2069` for `Proof.lean`. The toolchain is Lean 4.29.0 commit
`98dc76e3...16740`; pinned mathlib is `8a178386...ea95`.

## Retry And Status Boundary

Resume by completing `M1060-N-WIENER` and implementing the frozen analytic
packages without placeholders, or by identifying an immutable compatible Lean
4 Schilder proof that can be pinned, exact-type checked, and provenance-
audited without changing the dependency lock.

This is a `[_]` proposal for self-tested partial proof work plus fresh
nonrelease blocker evidence. It does not
satisfy `S56-M-1060-PROOF`, change scheduler/DAG state, close the root, or
claim audit completion, theorem completion, validation, release, receipt
acceptance, or master acceptance. `.stage1-worker-selftest.json` records only
the checked partial contribution; proof-phase completion remains false.
