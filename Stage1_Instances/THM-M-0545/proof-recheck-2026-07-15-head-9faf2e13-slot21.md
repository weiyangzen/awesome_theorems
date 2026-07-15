# THM-M-0545 proof-phase recheck at base 9faf2e13

Item: `S56-M-0545-PROOF`

Intent: `prove`

Recheck date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `9faf2e13566ce7ad1047f54337157387eaed48bf`

Base tree: `438505eefd23e6c86d2100b87e98212be6fd8675`

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
refutation above independently of the operator laws.

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
remain false. The predecessor obligation-tree item is worker-provisional
`[_]`, not master-accepted.

Because the assigned phase is incomplete, `.stage1-worker-selftest.json` is
deliberately absent.

## Failed Gate And Retry

The first failed gate is `S56-5.1-EXACT-TARGET-CONSISTENCY` at
`M0545-S-BOUNDARY`. The actionable reopen set is
`S56-M-0545-STATEMENT`, `M0545-S-BOUNDARY`, `M0545-S-REALIZATION`, and
`M0545-ROOT`.

Positive proof work can resume only after an authorized statement revision
repairs the degree-zero decomposition encoding and replaces the unconstrained
realization propositions with concrete pinned definitions or source-justified,
noncircular law-bearing structures. The corrected target needs a newly
accepted expression fingerprint, followed by fresh statement, anchor-audit,
obligation-tree, and proof phases in dependency order.

The frozen graph's remaining root cut set is `M0545-S-REALIZATION`,
`M0545-A-COMPLETION`, `M0545-A-D`, `M0545-A-ADJOINT`,
`M0545-A-LAPLACIAN`, `M0545-A-ELLIPTIC`, `M0545-A-GREEN`,
`M0545-L-CLOSED-RANGES`, and `M0545-S-BOUNDARY`.

## Scoped Validation

All commands ran in this worker clone against the existing pinned Lake
artifacts. The automation-provided untracked `Formalizations/Lean/.lake`
symlink was reused read-only. No `lake update`, `lake build`, dependency
clone/fetch, network operation, or `.lake` mutation ran. Temporary Lean
objects and logs were created in a fresh `/tmp` directory and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0545` | 0 | Rank 105; baseline `L0`; lifecycle `planned`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0545/check_anchor_audit.py` | 0 | Target boundary, five candidates, 11 Lean probes, and pinned mathlib revision agree. |
| `python3 Stage1_Instances/THM-M-0545/check_obligation_tree.py` | 0 | 17 obligations and 132 typed edges passed; denominator `52a39eb0...9896e`; root remains open at `M4`. |
| `timeout 30s bash -c 'cd Formalizations/Lean && lake env printenv LEAN_PATH'` | 0 | Resolved the existing pinned project, dependency, and toolchain Lean paths. |
| Isolated `lake env lean --trust=0 -t 0` replay below | 0 | The exact statement and both universe-zero refutations elaborated; each axiom report was `[propext, Classical.choice, Quot.sound]`. |
| Independent read-only isolated replay | 0 | A Lean-analysis worker separately elaborated the same statement and both refutations with matching hashes and axiom reports; corroborating nonrelease evidence only. |
| `rg -n -i 'hodge decomposition\|harmonic form\|hodge laplacian\|codifferential' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | Expected no-match exit; no analytic Hodge-decomposition anchor was found in pinned mathlib. |
| `rg -n --pcre2 '<rev-5.6 prohibited-proof-escape pattern>' Stage1_Instances/THM-M-0545 --glob '*.lean'` | 1 | Expected no-match exit; no prohibited proof escape was found. |
| `python3 -m json.tool Stage1_Instances/THM-M-0545/proof-recheck-2026-07-15-head-9faf2e13-slot21.json` | 0 | Structured blocker JSON is valid. |
| Inline Python blocker identity and source-hash assertions | 0 | Current base/tree, incomplete-state boundary, changed paths, and 13 input hashes agree. |
| `git diff --check -- Stage1_Instances/THM-M-0545` | 0 | No tracked-diff whitespace diagnostics. |
| `git diff --no-index --check /dev/null <new artifact>` for both new files | 1 each | Expected new-file difference exits; zero diagnostic bytes for each file. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion manifest is absent because the proof phase is blocked. |

The isolated replay ran from `2026-07-15T20:36:18+08:00` through
`2026-07-15T20:36:47+08:00`. All three Lean invocations exited `0`.
`Statement.olean` was 347208 bytes with SHA-256
`0cb3c19973217747cb7ee91bb25171d50212bdef10d4246cd1d5ccc952cb1bce`.
The 5758-byte statement log had SHA-256
`afcc4739ad6536f2f83577f6076cdcd38cbb3c15d867ddadac48cc5e417227a9`.
The 495-byte degree-zero proof log had SHA-256
`a3e7a99920e583bc2f934ad400af951ae9989b24410e7d7c68d18ae89a0c9f62`.
The 439-byte realization proof log had SHA-256
`ea27796c6b2205a152959ad24901f96ca03213689439e9530ab83b4ddaff6e60`.

Replay recipe, run from the repository root:

```bash
set -uo pipefail
tmp=$(mktemp -d /tmp/thm-m-0545-proof-9faf2e13-slot21.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-0545/Statement.lean "$tmp/Statement.lean"
cp Stage1_Instances/THM-M-0545/ProofBoundaryCountermodel-2026-07-15.lean \
  "$tmp/ProofBoundaryCountermodel.lean"
cp Stage1_Instances/THM-M-0545/ProofCountermodel-2026-07-14.lean \
  "$tmp/ProofCountermodel.lean"
lean_path=$(cd Formalizations/Lean && timeout 30s lake env printenv LEAN_PATH)
cd "$tmp"
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 \
  LEAN_PATH="$lean_path" timeout 300s lake env lean --trust=0 -t 0 \
  --root="$tmp" -o Statement.olean Statement.lean > statement.log 2>&1
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 \
  LEAN_PATH="$tmp:$lean_path" timeout 300s lake env lean --trust=0 -t 0 \
  --root="$tmp" ProofBoundaryCountermodel.lean > boundary.log 2>&1
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 \
  LEAN_PATH="$tmp:$lean_path" timeout 300s lake env lean --trust=0 -t 0 \
  --root="$tmp" ProofCountermodel.lean > realization.log 2>&1
sha256sum Statement.olean statement.log boundary.log realization.log
wc -c Statement.olean statement.log boundary.log realization.log
```

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake
`5.0.0-src+98dc76e`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`.

The paired JSON artifact binds the current immutable base, task and obligation
IDs, source hashes, environment, commands, outputs, trust result, failure
boundary, and retry condition. It is negative nonrelease evidence, not a
positive proof receipt.
