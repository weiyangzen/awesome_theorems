# THM-M-1065 proof recheck at `fb0fd5be`

Item: `S56-M-1065-PROOF`

Date: `2026-07-15T05:30:16+08:00`

Base revision: `fb0fd5be494d0813177dbdc959ec911d69a72015`

Base tree: `f6d39faae5fb024a71ee786e7a6b017d335841cd`

## Verdict

`blocked`. No eligible proof body was implemented or found for the exact target
`Stage1Instances.THM_M_1065.KMTStrongApproximationTarget`. No frozen obligation was newly closed,
the root vector remains `[H2, M4, R4]`, and `theorem_complete=false`.

The target requires, for every centered variance-one real probability law with a two-sided
exponential moment, one probability-space coupling of iid increments with that law and iid
standard Gaussian increments. Positive law-dependent constants must give a uniform exponential
tail for the maximum partial-sum discrepancy through every positive `n` and every `x >= 0`.

The checked local bodies are boundary and interface results, not KMT:

- `target_iff_expandedSourceShape` is only the definitional expansion of the statement;
- `discrepancyEvent_one` proves only the `n = 1` event identity;
- `ObligationTree.kmtTarget_iff_couplingData` only repacks an already complete witness package.

Pinned mathlib supplies `HasLaw`, `iIndepFun`, Gaussian laws, product measures, and
`ProbabilityTheory.exists_iid`. Those APIs can construct standalone iid families, but they do not
construct a dependent KMT coupling or prove its logarithmic maximal-discrepancy tail. The bounded
repository, pinned-source, and prerequisite external searches found no exact terminal candidate.

The first unavailable frozen construction is `M1065-C-SPACE`. The substantive
`M1065-L-BLOCK-COUPLING` and `M1065-L-MAXIMAL-TAIL` packages are also absent. Independent product
coupling does not supply their estimate, `X = Y` cannot meet the arbitrary input and Gaussian
marginals, and a generic probability bound cannot decay for every unbounded `x`. Assuming any of
these packages, or substituting a terminal-time or asymptotic theorem, would violate the frozen
target and placeholder policy.

The canonical conjunction does not separately require `MeasurableSet (DiscrepancyEvent ...)`,
although the frozen architecture records event measurability as `M1065-L-EVENT-MEAS`. Mathlib
measures arbitrary sets by outer measure, so this mismatch supplies no known trivial proof. It is
retained as a statement/source audit concern and receives no proof credit.

Because the assigned positive proof phase is incomplete, `.stage1-worker-selftest.json` is
deliberately absent and the item remains `[ ]`.

## Validation

All accepted checks reused the automation-provided pinned Lake artifacts read-only. No
`lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was performed. The
untracked `.lake` symlink makes this nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1065` | 0 | rank 507; planned hard-mathlib-anchor-and-wrapper lane; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1065/check_anchor_audit.py` | 0 | pinned substrate verified; no exact terminal candidate credited |
| `python3 Stage1_Instances/THM-M-1065/check_obligation_tree.py` | 0 | 18 obligations and 75 typed edges passed; denominator `d5e21a3a...91ac2`; root open M4 |
| direct pinned `lake env lean --trust=0` elaboration of `Statement.lean` | 0 | exact target, expansion, and boundary body checked; only unused-variable linter warnings |
| direct pinned `lake env lean --trust=0` elaboration of `ObligationTree.lean` | 0 | conditional witness/root equivalence checked; no witness constructed |
| `python3 Stage1_Instances/THM-M-1065/check_statement.py` | interrupted | no diagnostic under severe shared-host Lean contention; temporary file/process removed; direct statement elaboration passed |
| pinned mathlib topical source scan | 1 | expected no-match exit; no KMT or strong-approximation source found |
| owned Lean prohibited-construct scan | 1 | expected no-match exit; no `sorry`, `admit`, axiom/constant/opaque escape, `sorryAx`, `unsafe`, `implemented_by`, or `native_decide` |
| pinned revision, tree, and package-status checks | 0 | mathlib `8a178386...ea95`, tree `bdc39a31...1c2b`, clean package worktree |
| JSON parse, source-hash, and blocker invariant assertions | 0 | current base, unchanged vector, empty proof-credit arrays, open flags, exact cut set, and absent manifest agree |
| per-new-file and scoped whitespace checks | 0 aggregate | both fresh files differ from `/dev/null` and have no whitespace diagnostics |
| `git diff --check -- Stage1_Instances/THM-M-1065 .stage1-worker-selftest.json` | 0 | no whitespace errors |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion manifest deliberately absent |

The proof-relevant hashes, full command results, environment identity, unchanged debt vector, and
failure boundary are recorded in `proof-recheck-2026-07-15-head-fb0fd5be.json`.

## Retry Condition

Resume after implementing the frozen common-space KMT construction, quantitative finite-block
coupling, and exponential maximal-tail packages without placeholders, or after locating an
immutable compatible Lean 4 proof that can be pinned, exact-type checked, and provenance-audited
without changing the dependency lock.

This is a fresh owned blocker artifact, not a proof receipt. It does not satisfy
`S56-M-1065-PROOF`, propose scheduler state, or support audit completion, theorem completion,
validation, release, or master acceptance.
