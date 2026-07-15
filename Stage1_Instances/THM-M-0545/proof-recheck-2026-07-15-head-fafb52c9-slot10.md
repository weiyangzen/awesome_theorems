# THM-M-0545 proof-phase recheck at base fafb52c9

Item: `S56-M-0545-PROOF`

Intent: `prove`

Recheck date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `fafb52c91501fd02290f6e2aa8dbf6af59184135`

Base tree: `368a5490da1afb0cfd49518532085ec2146ce1e6`

## Verdict

`blocked`. No positive proof body can consistently inhabit the exact frozen
Lean target. The placeholder-free declaration

```text
Stage1Instances.THMM0545.not_hodgeDecompositionTarget_degreeZero :
  Not Stage1Instances.THMM0545.HodgeDecompositionTarget.{0, 0, 0, 0}
```

kernel-checks at trust level zero against a freshly elaborated temporary
`Statement.olean`. Any universe-polymorphic proof of the requested target
would specialize to universes `(0, 0, 0, 0)` and contradict this declaration.

The first defect is at the frozen degree boundary. `IsExact D 0 e` requires a
natural number `j` satisfying `j + 1 = 0`, so it is empty, while
`HasUniqueDecomposition` requires an exact summand at every degree, including
zero. `ProofBoundaryCountermodel-2026-07-15.lean` proves
`not_isExact_zero`, `no_degreeZeroDecomposition`, and the exact root
refutation above.

There is a second independent defect. `HodgeDecompositionTarget` quantifies
over every `HodgeAnalyticData`, while `realizesSmoothComplexForms` and
`realizesHodgeOperators` are unconstrained propositions. The checked
`ProofCountermodel-2026-07-14.lean` assigns `Complex` to every form space,
sets the exterior derivative and codifferential to zero, sets the Laplacian to
the identity, and makes all four proposition fields true. At degree one the
form `1` cannot be the sum of the forced-zero harmonic, exact, and coexact
parts, yielding a separate exact root refutation.

These declarations refute only the overbroad abstract encoding, not the
mathematical Hodge decomposition theorem. No positive proof body, proof
receipt, composition certificate, or frozen obligation was added or closed.
The proof item remains `[ ]`; lifecycle remains `planned`; the recorded root
vector remains `[H3, M4, R4]`. `[H3, M5, R4]` is only a fail-closed diagnosis
proposed for master reconciliation. Audit completion and theorem completion
remain false.

Because the assigned phase is incomplete, `.stage1-worker-selftest.json` is
deliberately absent.

## Failed Gate And Retry

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

## Scoped Validation

All commands ran in this worker clone against the existing pinned Lake
artifacts. The automation-provided untracked `Formalizations/Lean/.lake`
symlink was reused read-only. No `lake update`, `lake build`, dependency
clone/fetch, network operation, or `.lake` mutation ran. Lean outputs and logs
were written only in a fresh `/tmp` directory and removed afterward.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0545` | 0 | Rank 105; lane `frontier_deep_formalization_debt`; lifecycle `planned`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0545/check_anchor_audit.py` | 0 | `ok: target boundary, five candidate rows, 11 Lean probes, and pinned mathlib revision agree` |
| `python3 Stage1_Instances/THM-M-0545/check_obligation_tree.py` | 0 | 17 obligations and 132 typed edges passed; denominator `52a39eb0...9896e`; root remains open at `M4`. |
| `timeout 30s lake env printenv LEAN_PATH` from `Formalizations/Lean` | 0 | Resolved the existing pinned project, dependency, and toolchain Lean libraries. |
| Isolated `lake env lean --trust=0 -t 0` replay below | 0 | Exact statement and both universe-zero refutations elaborated; each `#print axioms` reported `[propext, Classical.choice, Quot.sound]`. |
| Two parallel read-only proof analyses | 0 | Both independently reproduced the obstruction and a trust-zero countermodel replay. This is corroboration, not release-grade independent verification. |
| Pinned mathlib search for Hodge decomposition, Hodge Laplacian, codifferential, or coexact APIs | 1 | Expected no-match result: no exact analytic Hodge-decomposition closure was found. |
| Prohibited-proof-escape scan of owned Lean sources | 1 | Expected no-match result: zero prohibited constructs were found. |
| `git status --short --untracked-files=all` before edits | 0 | Only the automation-provided `?? Formalizations/Lean/.lake` symlink was present. |
| `python3 -m json.tool` plus inline identity/base/hash assertions | 0 | Structured blocker JSON is valid; identity, current base/tree, incomplete-state boundary, changed paths, and 13 input hashes agree. |
| `git diff --check` plus two new-file checks | 0 | No whitespace diagnostics; new-file checks returned only their expected difference exits. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion manifest is absent because the positive proof phase is blocked. |

Exact primary replay, run from the repository root:

```bash
set -uo pipefail
start=$(TZ=Asia/Shanghai date --iso-8601=seconds)
tmp=$(mktemp -d /tmp/thm-m-0545-proof-fafb52c9-slot10.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-0545/Statement.lean "$tmp/Statement.lean"
cp Stage1_Instances/THM-M-0545/ProofBoundaryCountermodel-2026-07-15.lean \
  "$tmp/ProofBoundaryCountermodel.lean"
cp Stage1_Instances/THM-M-0545/ProofCountermodel-2026-07-14.lean \
  "$tmp/ProofCountermodel.lean"
lean_path=$(cd Formalizations/Lean && timeout 30s lake env printenv LEAN_PATH)
cd Formalizations/Lean
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 \
  LEAN_PATH="$lean_path" timeout 300s lake env lean --trust=0 -t 0 \
  --root="$tmp" -o "$tmp/Statement.olean" "$tmp/Statement.lean" \
  >"$tmp/statement.log" 2>&1
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 \
  LEAN_PATH="$tmp:$lean_path" timeout 300s lake env lean --trust=0 -t 0 \
  --root="$tmp" "$tmp/ProofBoundaryCountermodel.lean" \
  >"$tmp/boundary.log" 2>&1
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 \
  LEAN_PATH="$tmp:$lean_path" timeout 300s lake env lean --trust=0 -t 0 \
  --root="$tmp" "$tmp/ProofCountermodel.lean" \
  >"$tmp/realization.log" 2>&1
sha256sum "$tmp/Statement.olean" "$tmp/statement.log" \
  "$tmp/boundary.log" "$tmp/realization.log"
wc -c "$tmp/Statement.olean" "$tmp/statement.log" \
  "$tmp/boundary.log" "$tmp/realization.log"
```

The replay ran from `2026-07-15T19:03:24+08:00` through
`2026-07-15T19:03:48+08:00`; the path probe and all three Lean invocations
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

The paired JSON artifact binds the current immutable base, task and obligation
IDs, source hashes, environment, commands, outputs, trust result, failure
boundary, and retry condition. It is fresh negative nonrelease evidence, not a
positive proof receipt.
