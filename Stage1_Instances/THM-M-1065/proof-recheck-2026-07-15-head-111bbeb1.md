# THM-M-1065 proof recheck at `111bbeb1`

Item: `S56-M-1065-PROOF`

Date: `2026-07-15T06:55:53+08:00`

Base revision: `111bbeb1a210ae4e8525a4342012921ab60e466f`

Base tree: `8f705aa79622bf1e9be0665ae1254313df21b4f6`

## Verdict

`blocked`. `Proof.lean` now implements a kernel-checked common product-space construction for the
two iid marginal families, but no eligible proof body was implemented or found for the exact target
`Stage1Instances.THM_M_1065.KMTStrongApproximationTarget`. The new body is useful substrate without
root proof credit; no complete frozen obligation is claimed newly closed, the root vector remains
`[H2, M4, R4]`, and `theorem_complete=false`.

The target requires, for every centered variance-one real probability law with a two-sided
exponential moment, one probability-space coupling of iid increments with that law and iid
standard Gaussian increments. Positive law-dependent constants must give a uniform exponential
tail for the maximum partial-sum discrepancy through every positive `n` and every `x >= 0`.

The pre-existing checked local bodies are statement or interface facts, not a KMT construction:

- `target_iff_expandedSourceShape` directly expands the canonical definition;
- `discrepancyEvent_one` proves only the `n = 1` event identity;
- `ObligationTree.kmtTarget_iff_couplingData` repacks an already complete witness package without
  constructing it.

Pinned mathlib contains `ProbabilityTheory.exists_hasLaw_indepFun` and `exists_iid`, so it can put
standalone iid input-law and Gaussian families on a common product carrier. That independent
product construction is not the required KMT coupling: it provides neither the dependent
finite-block construction nor the logarithmic maximal-discrepancy estimate. The current bounded
repository and pinned-package search found no exact terminal proof candidate.

`Proof.lean` makes that boundary executable rather than merely descriptive. It indexes an infinite
product by `Sum Nat Nat`, assigns `mu` to the left coordinates and the standard Gaussian law to the
right coordinates, and restricts the coordinate family's joint independence to each summand. The
theorem `exists_commonIIDSequences` gives one probability carrier, both prescribed marginal laws,
and independence within each sequence. It intentionally has no constants or discrepancy field.
Its axiom report is exactly `propext`, `Classical.choice`, and `Quot.sound`.

The first unavailable root-relevant construction is `M1065-C-SPACE`; the substantive
`M1065-L-BLOCK-COUPLING` and `M1065-L-MAXIMAL-TAIL` packages are also absent. Assuming any one of
them, or substituting a terminal-time or asymptotic invariance theorem, would violate the frozen
target and the placeholder policy. The conservative root cut therefore remains those three nodes.

The prerequisite artifacts are self-tested but still await master acceptance: the target-local
structured task DAG continues to mark `STATEMENT`, `ANCHOR_AUDIT`, and `OBLIGATION_TREE` open. This
proof-only worker did not edit that authority or the generated scheduler projections.

At least five prior integrated proof-blocker/recheck ticks are present for this same unsplit item.
Section 10.2 of the rev-5.6 standard requires splitting an obligation after five unresolved
execution ticks. The scheduler still reports `attempts=0` and `children=[]`; only the master may
repair that scheduling state. Reassigning the whole KMT root again cannot truthfully manufacture
the missing mathematics.

Because the positive proof phase did not pass, `.stage1-worker-selftest.json` is deliberately
absent and the item remains `[ ]`.

## Validation

All Lean checks reused the automation-provided pinned Lake artifacts read-only. No `lake update`,
`lake build`, dependency clone/fetch, or `.lake` mutation was performed. The untracked `.lake`
symlink makes this nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1065` | 0 | rank 507; planned hard-mathlib-anchor-and-wrapper lane; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1065/check_statement.py` | 0 | expression digest `b257ceb1...cebd0`; all four registered mutations distinguished |
| `python3 Stage1_Instances/THM-M-1065/check_anchor_audit.py` | 0 | pinned substrate verified; no exact terminal candidate credited |
| `python3 Stage1_Instances/THM-M-1065/check_obligation_tree.py` | 0 | 18 obligations and 75 typed edges passed; denominator `d5e21a3a...91ac2`; root open M4 |
| `cd Formalizations/Lean && LEAN_NUM_THREADS=1 timeout 600 lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-1065/Statement.lean` | 0 | exact target, expansion, and `n = 1` body checked; only unused-variable mutation lints |
| same command for `ObligationTree.lean` | 0 | conditional witness/root equivalence checked; no witness constructed |
| same command for `AnchorAudit.lean` | 0 | substrate declarations and negative completion certificate checked |
| isolated `Statement.lean -> Proof.lean` replay at `--trust=0 -t0` | 0 | `exists_commonIIDSequences` checked; axioms exactly `propext`, `Classical.choice`, `Quot.sound` |
| pinned-package topical Lean source scan | 1 | expected no-match result; no KMT or strong-approximation source found |
| owned Lean prohibited-construct scan | 1 | expected no-match result; no prohibited proof device found |
| pinned revision, tree, and package-status checks | 0 | mathlib `8a178386...ea95`, tree `bdc39a31...1c2b`, clean package worktree |
| blocker JSON, invariant, source-hash, absent-selftest, and whitespace checks | 0 | structured evidence agreed with the current snapshot; no whitespace errors |

The final structured artifact also records exact commands, source hashes, environment identity,
open-state invariants, and whitespace checks.

## Retry condition

Resume only with dependency-legal child assignments for the frozen common-space KMT construction,
quantitative finite-block coupling, and exponential maximal-tail proof, or with an immutable
compatible Lean 4 proof that can be pinned, exact-type checked, and provenance-audited without
changing the dependency lock.

This is current-base owned blocker evidence, not a proof receipt. It does not satisfy
`S56-M-1065-PROOF`, close a frozen obligation or the root, change scheduler state, or claim audit
completion, theorem completion, validation, release, receipt acceptance, or master acceptance.
