# S56-M-0545-PROOF current-base recheck

## Verdict

`blocked`; the assigned proof item remains `[ ]`. The mandatory v2 dependency
audit completed first. The authoritative target node has no direct parent,
transitive ancestor, incoming hard edge, reuse hint, or shared lemma group, so
`dependency-reuse-ledger.json` records a complete empty closure. It provides no
reusable declaration and transfers no proof credit.

No consistent positive proof term can inhabit the exact frozen target. The
earliest failure is `M0545-S-BOUNDARY`: `IsExact D 0 e` requires a natural
number `j` satisfying `j + 1 = 0`, while `HasUniqueDecomposition 0 omega`
requires an exact summand. The placeholder-free declaration
`not_hodgeDecompositionTarget_degreeZero` therefore proves
`Not HodgeDecompositionTarget.{0, 0, 0, 0}`.

There is also an independent realization-interface failure. The four
realization fields are unconstrained propositions and impose no laws on the
operators. `not_hodgeDecompositionTarget` specializes to scalar forms with
zero exterior derivative and codifferential and identity Laplacian; the
degree-one form `1` cannot decompose. These checked negations refute only the
overbroad frozen Lean encoding, not the mathematical Hodge decomposition
theorem.

No positive proof body, proof receipt, closed obligation, composition
certificate, or `.stage1-worker-selftest.json` was created. A self-test packet
would falsely claim that the assigned positive proof phase passed.

## Dependency audit

The ledger uses schema `stage1-dependency-reuse-ledger/1.1`, repository
revision `6bf9ee93a322e7d25cf9249226222095f95d1cff`, graph SHA-256
`73e99d2276c8ba9fec8f89ed41b712308d7f5667e95ba8185e49f1f5bfd40eca`,
and context SHA-256
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.
All five source-ID lists, `inspections`, `reuse_decisions`, and
`unresolved_compatibility_obligations` are empty. The executable scheduler
validator accepted this exact empty closure.

## Failed gate and retry

The first failed gate is `S56-5.1-EXACT-TARGET-CONSISTENCY` at
`M0545-S-BOUNDARY`. The actionable reopen set is
`S56-M-0545-STATEMENT`, `M0545-S-BOUNDARY`, `M0545-S-REALIZATION`, and
`M0545-ROOT`.

Positive proof work can resume only after an authorized statement revision
models the zero exact summand without demanding a natural predecessor and
replaces the unconstrained realization propositions with concrete pinned
definitions or source-justified, noncircular law-bearing structures. The
corrected target needs a new accepted expression fingerprint, followed by
fresh statement, anchor-audit, obligation-tree, and proof phases in dependency
order.

The frozen graph's remaining root cut set is `M0545-S-REALIZATION`,
`M0545-A-COMPLETION`, `M0545-A-D`, `M0545-A-ADJOINT`,
`M0545-A-LAPLACIAN`, `M0545-A-ELLIPTIC`, `M0545-A-GREEN`,
`M0545-L-CLOSED-RANGES`, and `M0545-S-BOUNDARY`.

## Scoped validation

All commands ran in this worker clone against the existing pinned Lake
artifacts. The automation-provided untracked `Formalizations/Lean/.lake`
symlink was reused read-only. No `lake update`, `lake build`, dependency
clone/fetch, network operation, or `.lake` mutation ran. Lean outputs were
written only in a fresh `/tmp` directory and removed afterward.

| Command | Exit | Exact result |
|---|---:|---|
| Isolated `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, v2 theorem DAG, execution skill present)`; same graph-discovery isolation as the v2 validator. |
| Isolated `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | `check_stage1_theorem_dag_v2: ok (1546 theorems, 10822 legacy states preserved, 2 hard edges, 5 reuse hints, 310 shared groups, acyclic)`; the new ledger and blocker JSON were temporarily moved outside graph discovery because this worker may not regenerate the protected graph, then restored byte-for-byte. |
| Isolated `python3 scripts/stage1_execution_cron.py --validate-only --workers 0` | 0 | `validate-only: ok`; 10,822 items, 1,546 targets, 3,218 `[_]`, and 7,604 `[ ]`; same graph-discovery isolation as the v2 validator. |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0545` | 0 | Rank 105; lane `frontier_deep_formalization_debt`; lifecycle `planned`; theorem incomplete. |
| Scheduler `validate_dependency_reuse_ledger(...)` with the exact graph and base | 0 | `PASS empty dependency reuse ledger: 068170c7...c5c` |
| Direct post-artifact standard, v2 graph, and cron structural checks | 1 | All stop at `checked-in theorem DAG differs from a fresh deterministic generation`: fresh discovery inventories the mandatory new ledger/blocker JSON, while this worker is prohibited from regenerating the protected graph. The graph file remains byte-identical to the scheduler base; integration must reconcile discovery after merge. |
| `python3 Stage1_Instances/THM-M-0545/check_anchor_audit.py` | 0 | Target boundary, five candidate rows, 11 Lean probes, and pinned mathlib revision agree. |
| `python3 Stage1_Instances/THM-M-0545/check_obligation_tree.py` | 0 | 17 obligations and 132 typed edges passed; denominator `52a39eb0...9896e`; root remains open at `M4`. |
| Isolated `lake env lean --trust=0 -t0` replay | 0 | Exact statement and both universe-zero refutations elaborated; each `#print axioms` reported `[propext, Classical.choice, Quot.sound]`. |
| Three independent read-only analyses | 0 | All confirmed the empty dependency closure and/or both statement defects; one separately passed a trust-zero replay. This is corroboration, not release-grade independent verification. |
| Pinned mathlib search for Hodge decomposition, Hodge Laplacian, codifferential, or coexact APIs | 1 | Expected no-match result: no exact analytic Hodge-decomposition closure was found. |
| Prohibited-proof-escape scan of owned Lean sources | 1 | Expected no-match result: zero prohibited constructs were found. |
| `python3 -m json.tool` plus inline identity/base/hash/ledger assertions | 0 | Both JSON files parse; blocker identity, base/tree, unfinished boundary, changed paths, 15 immutable input hashes, empty dependency closure, and self-test absence agree. |
| `git diff --check` plus three new-file checks | 0 | No whitespace diagnostics. |

Exact primary replay, run from the repository root:

```bash
set -uo pipefail
tmp=$(mktemp -d /tmp/thm-m-0545-proof-6bf9ee93-slot10-replay.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-0545/Statement.lean "$tmp/Statement.lean"
cp Stage1_Instances/THM-M-0545/ProofBoundaryCountermodel-2026-07-15.lean \
  "$tmp/ProofBoundaryCountermodel.lean"
cp Stage1_Instances/THM-M-0545/ProofCountermodel-2026-07-14.lean \
  "$tmp/ProofCountermodel.lean"
lean_path=$(cd Formalizations/Lean && \
  timeout --foreground --kill-after=5s 60s lake env printenv LEAN_PATH)
cd Formalizations/Lean
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 \
  LEAN_PATH="$lean_path" timeout --foreground --kill-after=5s 600s \
  lake env lean --trust=0 -t0 --root="$tmp" \
  -o "$tmp/Statement.olean" "$tmp/Statement.lean" \
  >"$tmp/statement.log" 2>&1
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 \
  LEAN_PATH="$tmp:$lean_path" timeout --foreground --kill-after=5s 600s \
  lake env lean --trust=0 -t0 --root="$tmp" \
  "$tmp/ProofBoundaryCountermodel.lean" >"$tmp/boundary.log" 2>&1
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 \
  LEAN_PATH="$tmp:$lean_path" timeout --foreground --kill-after=5s 600s \
  lake env lean --trust=0 -t0 --root="$tmp" \
  "$tmp/ProofCountermodel.lean" >"$tmp/realization.log" 2>&1
sha256sum "$tmp/Statement.olean" "$tmp/statement.log" \
  "$tmp/boundary.log" "$tmp/realization.log"
wc -c "$tmp/Statement.olean" "$tmp/statement.log" \
  "$tmp/boundary.log" "$tmp/realization.log"
```

The replay ran from `2026-07-16T04:46:07+08:00` through
`2026-07-16T04:50:03+08:00`; the path probe and all three Lean invocations
exited `0`. Hashes and sizes were:

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `Statement.olean` | 347208 | `0cb3c19973217747cb7ee91bb25171d50212bdef10d4246cd1d5ccc952cb1bce` |
| `statement.log` | 5758 | `afcc4739ad6536f2f83577f6076cdcd38cbb3c15d867ddadac48cc5e417227a9` |
| `boundary.log` | 495 | `a3e7a99920e583bc2f934ad400af951ae9989b24410e7d7c68d18ae89a0c9f62` |
| `realization.log` | 439 | `ea27796c6b2205a152959ad24901f96ca03213689439e9530ab83b4ddaff6e60` |

Both exact axiom reports were `[propext, Classical.choice, Quot.sound]`.
Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake
`5.0.0-src+98dc76e`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`.

The paired JSON artifact binds the current immutable base, v2 context, task
and obligation IDs, source hashes, environment, commands, outputs, trust
result, failure boundary, and retry condition. It is fresh negative nonrelease
evidence, not a positive proof receipt.
