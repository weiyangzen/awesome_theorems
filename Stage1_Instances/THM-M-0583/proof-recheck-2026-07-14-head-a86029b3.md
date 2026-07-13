# THM-M-0583 proof phase blocked at `a86029b3`

Item: `S56-M-0583-PROOF`

Intent: `prove`

Recheck date: `2026-07-14` (`Asia/Shanghai`)

Base revision: `a86029b30f12acc3537f70ab1c167cc25702c09b`

Base tree: `ab12055e811b574338987391b59b010338c120d2`

## Verdict

`blocked`. No placeholder-free retained Lean 4 proof body in the pinned
dependency closure inhabits the exact frozen target. The target is the
substantive four-dimensional topological Poincare theorem: every compact
Hausdorff boundaryless topological four-manifold homotopy equivalent to the
standard four-sphere is homeomorphic to it.

The owned theorem `canonicalRoot_of_freedmanTopologicalCore` is not such a
body. Its premise `FreedmanTopologicalCore` is definitionally identical to the
complete root, and its body returns that premise unchanged. It checks only the
exact adapter and closes none of the 16 frozen obligations.

Pinned mathlib records the generalized theorem only as
`proof_wanted ContinuousMap.HomotopyEquiv.nonempty_homeomorph_sphere`.
Batteries elaborates `proof_wanted` under `withoutModifyingEnv`, so the
temporary declaration is discarded rather than retained as an axiom or proof.
A trust-zero retained-environment probe confirmed that this name and both
three-dimensional marker names are unknown constants after import.

The fresh local search and prerequisite immutable audit found no eligible
body. The Lean Millennium candidate proves dimension zero only. The Formal
Conjectures dimension-four candidate and atlas-lean's Freedman-shaped
candidate contain `sorry`; neither is eligible or pinned. No assumption,
axiom, placeholder, weakened or smooth substitute, moving dependency, or fake
certificate was introduced.

The first failed gate is `M0583-X-FREEDMAN-CORE`: terminal proof-body
availability. The remaining machine-critical cut set is:

1. `M0583-R-HOMOTOPY-DATA`
2. `M0583-C-TOPOLOGICAL-MODEL`
3. `M0583-L-DISK-EMBEDDING`
4. `M0583-L-SURGERY`
5. `M0583-L-S-COBORDISM`
6. `M0583-C-HOMEOMORPHISM`
7. `M0583-X-FREEDMAN-CORE`

The proof item remains `[ ]`, the root remains `[H2, M2, R4]`, and theorem
completion remains false. Because this positive proof phase is not genuinely
self-tested as complete, `.stage1-worker-selftest.json` is deliberately
absent.

## Validation

All commands ran in this worker clone. The automation-provided untracked
symlink to the canonical pinned `.lake` artifacts was reused read-only. No
`lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was
performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0583` | 0 | Rank 116; planned lifecycle; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0583/check_obligation_tree.py` | 0 | 16 obligations, 32 typed edges, seven graph kinds; denominator `910aad119639e1751b6f8c0ad6d04f98a030acdc0e00c951cd46f6efff18cccd`; root open M2. |
| `python3 Stage1_Instances/THM-M-0583/check_anchor_audit.py` | 0 | Pinned mathlib remained source-only; immutable external candidates remained dimension-zero-only or `sorry`; root M2. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`. |
| `cd Formalizations/Lean && lake env lean --trust=0 ../../Stage1_Instances/THM-M-0583/Statement.lean` | 0 | Exact target elaborated; output SHA-256 `b467d3431963ce2e77d133f3818e41376649e745d8a97d2237906bb8aacf3e82`. |
| Same trust-zero recipe on `ObligationTree.lean` | 0 | Conditional adapter elaborated; output SHA-256 `a7ad922a09ab779a88c07b6f2c3ec3c2759b5282929abe5660d71794e2395d5d`; axioms `[propext, Classical.choice, Quot.sound]`. |
| Same trust-zero `lake env lean --stdin` with the import and three `#check_failure` marker probes | 0 | All marker names were unknown constants; output SHA-256 `21a44249da79341e3436a9ace33b985a0c9994709bab8fbe0c3b808155e1d2c2`. |
| Scoped retained-source search over the owned dossier, legacy Lean, pinned mathlib, and pinned `flt-regular` | 0 | Only statement/interface definitions, audit strings, and mathlib's `proof_wanted` marker matched; no terminal proof body was found. |
| Prohibited-construct scan over owned Lean sources | 1 | Expected no-match: no `sorry`, `admit`, bodyless `axiom`, `sorryAx`, `unsafe`, `implemented_by`, or `external`. |
| `python3 ../../Stage1_Instances/THM-M-0583/check_statement.py` from `Formalizations/Lean` | 0 | Canonical statement and four structural mutations elaborated; all mutations were distinguished. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` plus package-scoped status | 0 | Revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`, clean. |
| `git -C Formalizations/Lean/.lake/packages/flt-regular rev-parse HEAD HEAD^{tree}` plus package-scoped status | 0 | Revision `56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`, tree `32c9eace926573a9981787ae97643e520353c893`, clean. |

## Retry Condition

Resume only after placeholder-free local implementations of the seven open
machine obligations, or after discovery and approved pinning of an
independently audited licensed immutable Lean 4 proof with a compatible
dependency lock and exact kernel-checked transport to the canonical target.

This is current-base blocker evidence, not a proof receipt, provisional state,
audit or theorem completion claim, release decision, or master acceptance.
