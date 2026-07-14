# THM-M-1065 proof blocker at `15d20dda`

Item: `S56-M-1065-PROOF`

Date: `2026-07-15T06:20:21+08:00`

Base revision: `15d20dda8662e4144f32be899edc174f7a431574`

Base tree: `b39eec687e4f172c4ce04e08a255e593a428cf95`

## Verdict

`blocked`. No eligible proof body was implemented or found for the exact target
`Stage1Instances.THM_M_1065.KMTStrongApproximationTarget`. No frozen obligation was newly closed,
the root vector remains `[H2, M4, R4]`, and `theorem_complete=false`.

The target requires, for every centered variance-one real probability law with a two-sided
exponential moment, one probability-space coupling of iid increments with that law and iid
standard Gaussian increments. Positive law-dependent constants must give a uniform exponential
tail for the maximum partial-sum discrepancy through every positive `n` and every `x >= 0`.

The checked local bodies are not KMT proof bodies:

- `target_iff_expandedSourceShape` only expands the definition;
- `discrepancyEvent_one` proves only the `n = 1` event identity;
- `ObligationTree.kmtTarget_iff_couplingData` repacks an already complete witness package without
  constructing one.

Pinned mathlib contains `ProbabilityTheory.exists_hasLaw_indepFun` and `exists_iid`, so it can
construct standalone iid families and even put independent input-law and Gaussian families on one
product carrier. That construction is not a KMT coupling: it supplies neither the dependent
finite-block coupling nor the logarithmic maximal-discrepancy estimate. Chernoff, Hoeffding, and
Doob-style tail infrastructure likewise cannot manufacture the missing coupled block estimate.
Bounded repository and pinned-package searches found no exact terminal candidate.

The first unavailable frozen construction is `M1065-C-SPACE` in its root-relevant coupled sense.
The substantive `M1065-L-BLOCK-COUPLING` and `M1065-L-MAXIMAL-TAIL` packages are also absent.
Independent product coupling does not supply their estimate, `X = Y` cannot satisfy arbitrary
input-law and Gaussian marginals, and a generic probability bound cannot decay for every unbounded
`x`. Assuming any missing package, or substituting a terminal-time or asymptotic theorem, would
violate the frozen target and placeholder policy.

The canonical target measures `DiscrepancyEvent` without a separate `MeasurableSet` premise, while
the frozen architecture records event measurability as `M1065-L-EVENT-MEAS`. Mathlib measures
arbitrary sets by outer measure, so this mismatch does not make the root trivial and receives no
proof credit.

Because the positive proof phase did not pass, `.stage1-worker-selftest.json` is deliberately
absent and the item remains `[ ]`.

## Validation

All checks reused the automation-provided pinned Lake artifacts read-only. No `lake update`,
`lake build`, dependency clone/fetch, or `.lake` mutation was performed. The untracked `.lake`
symlink makes this nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1065` | 0 | rank 507; planned hard-mathlib-anchor-and-wrapper lane; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1065/check_statement.py` | 0 | expression digest `b257ceb1...cebd0`; all four registered mutations distinguished |
| `python3 Stage1_Instances/THM-M-1065/check_anchor_audit.py` | 0 | pinned substrate verified; no exact terminal candidate credited |
| `python3 Stage1_Instances/THM-M-1065/check_obligation_tree.py` | 0 | 18 obligations and 75 typed edges passed; denominator `d5e21a3a...91ac2`; root open M4 |
| `cd Formalizations/Lean && lake env lean --trust=0 ../../Stage1_Instances/THM-M-1065/Statement.lean` | 0 | exact target, expansion, and `n = 1` boundary body checked; only unused-variable mutation lints |
| `cd Formalizations/Lean && lake env lean --trust=0 ../../Stage1_Instances/THM-M-1065/ObligationTree.lean` | 0 | conditional witness/root equivalence checked; no witness constructed |
| `cd Formalizations/Lean && LEAN_NUM_THREADS=1 timeout 600 lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-1065/AnchorAudit.lean` | 0 | substrate declarations and negative terminal-candidate certificate checked |
| pinned-package topical Lean source scan | 1 | expected no-match result; no KMT or strong-approximation proof source found |
| owned Lean prohibited-construct scan | 1 | expected no-match result; no `sorry`, `admit`, axiom/constant/opaque escape, `unsafe`, `implemented_by`, or `native_decide` |
| pinned revision, tree, and package-status checks | 0 | mathlib `8a178386...ea95`, tree `bdc39a31...1c2b`, clean package worktree |
| owned JSON parse and current blocker invariant assertions | 0 | source identities, unchanged vector, empty proof-credit arrays, exact cut set, changed paths, and absent self-test agree |
| scoped whitespace checks | 0 | no whitespace errors in the two fresh blocker artifacts or owned worker delta |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test deliberately absent because the positive proof phase is blocked |

Full commands, hashes, environment identity, and results are recorded in
`proof-blocker-2026-07-15-head-15d20dda.json`.

## Retry Condition

Resume only after implementing the frozen common-space KMT construction, quantitative finite-block
coupling, and exponential maximal-tail packages without placeholders, or after locating an
immutable compatible Lean 4 proof that can be pinned, exact-type checked, and provenance-audited
without changing the dependency lock.

This is a current-base owned blocker artifact, not a proof receipt. It does not satisfy
`S56-M-1065-PROOF`, propose scheduler state, or support audit completion, theorem completion,
validation, release, or master acceptance.
