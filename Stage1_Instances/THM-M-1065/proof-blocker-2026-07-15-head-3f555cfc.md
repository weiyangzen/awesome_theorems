# THM-M-1065 proof blocker at `3f555cfc`

Item: `S56-M-1065-PROOF`

Date: `2026-07-15T06:41:41+08:00`

Base revision: `3f555cfc0879cb7c42e83d6bcf7b9e3e09997e58`

Base tree: `e8837f7e0722548e2b35e901d9d974797097635e`

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
construct standalone iid families. It does not contain a dependent KMT block coupling or the
logarithmic maximal-discrepancy tail estimate. A current bounded search of the pinned package
closure again found no KMT or strong-approximation Lean declaration.

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
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1065` | 0 | rank 507; planned hard-mathlib-anchor-and-wrapper lane; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1065/check_statement.py` | not accepted | overlapping invocations were stopped after direct target elaboration passed; no diagnostic was emitted and temporary files were removed |
| `python3 Stage1_Instances/THM-M-1065/check_anchor_audit.py` | 0 | pinned substrate verified; no exact terminal candidate credited |
| `python3 Stage1_Instances/THM-M-1065/check_obligation_tree.py` | 0 | 18 obligations and 75 typed edges passed; denominator `d5e21a3a...91ac2`; root open M4 |
| `cd Formalizations/Lean && LEAN_NUM_THREADS=1 timeout 120 lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-1065/Statement.lean` | 0 | exact target, expansion, and `n = 1` boundary body checked; only unused-variable mutation lints |
| `cd Formalizations/Lean && LEAN_NUM_THREADS=1 timeout 120 lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-1065/ObligationTree.lean` | 0 | conditional witness/root equivalence checked; no witness constructed |
| `cd Formalizations/Lean && LEAN_NUM_THREADS=1 timeout 180 lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-1065/AnchorAudit.lean` | 0 | substrate declarations and the negative terminal-candidate certificate checked |
| pinned-package topical Lean source scan | 1 | expected no-match result; no KMT or strong-approximation proof source found |
| owned Lean prohibited-construct scan | 1 | expected no-match result; no prohibited proof construct occurs in the owned Lean sources |
| pinned revision, tree, and package-status checks | 0 | mathlib `8a178386...ea95`, tree `bdc39a31...1c2b`, clean package worktree |
| blocker JSON parse and scoped invariant assertions | 0 | identity, current base/tree, open root, empty proof-credit arrays, exact cut set, and absent self-test agreed |
| scoped new-file and worktree whitespace checks | 0 | both fresh blocker artifacts and the owned delta had no whitespace errors |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test deliberately absent because the proof phase is blocked |

The current checkout is Lean `4.29.0` at commit `98dc76e3...`, with toolchain file SHA-256
`651c8acc...b1d2` and Lake manifest SHA-256 `321626c8...2d81`. Frozen source hashes are
`7f3b249e...edaf1` (`Statement.lean`), `9aa9a38f...b5873` (`ObligationTree.lean`),
`79eb5a4c...27a7b44` (registry), `dcb4876d...1c325c` (typed graphs), and
`ecb5d943...493d27` (anchor audit).

## Retry Condition

Resume only after implementing the frozen common-space KMT construction, quantitative finite-block
coupling, and exponential maximal-tail packages without placeholders, or after locating an
immutable compatible Lean 4 proof that can be pinned, exact-type checked, and provenance-audited
without changing the dependency lock.

This is current-base owned blocker evidence, not a proof receipt. It does not satisfy
`S56-M-1065-PROOF`, propose scheduler state, or support audit completion, theorem completion,
validation, release, or master acceptance.
