# THM-M-0545 proof-phase recheck at base b366bdd9

Item: `S56-M-0545-PROOF`

Intent: `prove`

Recheck date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `b366bdd9f72217b5465ccd19133760b911ed0b58`

Base tree: `987b635fe76400c0818b485a6e5fc7a7067311e4`

## Verdict

`blocked`. No positive proof body can consistently inhabit the exact frozen
Lean target. The placeholder-free declarations

```text
Stage1Instances.THMM0545.not_hodgeDecompositionTarget_degreeZero :
  Not Stage1Instances.THMM0545.HodgeDecompositionTarget.{0, 0, 0, 0}
Stage1Instances.THMM0545.not_hodgeDecompositionTarget :
  Not Stage1Instances.THMM0545.HodgeDecompositionTarget.{0, 0, 0, 0}
```

both kernel-check at trust level zero against a freshly elaborated temporary
`Statement.olean`. Any universe-polymorphic proof of the requested positive
target would specialize to universes `(0, 0, 0, 0)` and contradict either
declaration.

The first and operator-independent defect is at degree zero. The frozen
predicate `IsExact D 0 e` requires a natural number `j` with `j + 1 = 0`, so
it is empty. Nevertheless, `HasUniqueDecomposition` requires an exact summand
for every degree, including zero. The boundary countermodel checks this fact
and specializes the universal root to the compact zero-dimensional Euclidean
Riemannian manifold.

A second independent defect is that `realizesSmoothComplexForms` and
`realizesHodgeOperators` are unconstrained proposition fields. They impose no
laws on the supplied form spaces or operators. Scalar forms with zero exterior
derivative and codifferential and identity Laplacian satisfy all four explicit
proposition hypotheses but cannot decompose the degree-one form `1`.

These declarations refute only the frozen abstract encoding, not the
mathematical Hodge decomposition theorem. No positive proof body, proof
receipt, composition certificate, or frozen obligation was added or closed.
The proof item remains `[ ]`; the recorded root vector remains
`[H3, M4, R4]`, with `[H3, M5, R4]` only a fail-closed diagnosis proposed for
master reconciliation. Audit completion, validation, release, theorem
completion, and master acceptance remain false. The predecessor
obligation-tree item remains worker-provisional (`[_]`) and is not
master-accepted.

Because the assigned proof phase is incomplete,
`.stage1-worker-selftest.json` is deliberately absent.

## Failed Gate And Retry

The first failed gate is `S56-5.1-EXACT-TARGET-CONSISTENCY` at
`M0545-S-BOUNDARY`. The actionable reopen set is
`S56-M-0545-STATEMENT`, `M0545-S-BOUNDARY`, `M0545-S-REALIZATION`, and
`M0545-ROOT`.

The frozen graph's remaining root cut set is `M0545-S-REALIZATION`,
`M0545-A-COMPLETION`, `M0545-A-D`, `M0545-A-ADJOINT`,
`M0545-A-LAPLACIAN`, `M0545-A-ELLIPTIC`, `M0545-A-GREEN`,
`M0545-L-CLOSED-RANGES`, and `M0545-S-BOUNDARY`. Repairing the statement
invalidates that graph and requires it to be refrozen.

Positive proof work can resume only after an authorized statement revision
repairs the degree-zero exact-summand convention and replaces the opaque
realization propositions with concrete pinned definitions or source-justified,
noncircular law-bearing structures. The corrected target must receive a newly
accepted expression fingerprint, followed by fresh statement, anchor-audit,
obligation-tree, and proof phases in dependency order. Repeating positive
proof search against the current fingerprint is not an actionable retry.

## Scoped Validation

All commands ran in this worker clone against the existing pinned Lake
artifacts. The automation-provided untracked `Formalizations/Lean/.lake`
symlink was reused read-only. No `lake update`, `lake build`, dependency
clone/fetch, network operation, or `.lake` mutation ran. Lean outputs and logs
were written only in a fresh `/tmp` directory.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0545` | 0 | Rank 105; lane `frontier_deep_formalization_debt`; lifecycle `planned`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0545/check_anchor_audit.py` | 0 | `ok: target boundary, five candidate rows, 11 Lean probes, and pinned mathlib revision agree` |
| `python3 Stage1_Instances/THM-M-0545/check_obligation_tree.py` | 0 | 17 obligations and 132 typed edges passed; denominator `52a39eb0...9896e`; root remains open at `M4`. |
| Isolated `lake env lean --trust=0 -t0` recipe below | 0 | Exact statement and both universe-zero refutations elaborated; both `#print axioms` reports were `[propext, Classical.choice, Quot.sound]`. |
| Pinned mathlib Hodge API search | 1 | Expected no-match result: no analytic Hodge-decomposition, Hodge-Laplacian, codifferential, or coexact closure was found. |
| Prohibited proof-escape scan of owned Lean sources | 1 | Expected no-match result: zero prohibited constructs were found. |
| `python3 -m json.tool` plus inline identity/base/hash assertions | 0 | Structured blocker JSON is valid; identity, base/tree, unfinished state, changed paths, and all 13 input hashes agree. |
| `git diff --check` plus two new-file checks | 0 | No whitespace diagnostics; new-file checks returned only their expected difference exits. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The completion manifest is absent because the proof phase is blocked. |

Exact isolated Lean recipe, run from the repository root:

```bash
set -uo pipefail
start=$(TZ=Asia/Shanghai date --iso-8601=seconds)
tmp=$(mktemp -d /tmp/thm-m-0545-proof-b366bdd9-slot23.XXXXXX)
cp Stage1_Instances/THM-M-0545/Statement.lean "$tmp/Statement.lean"
cp Stage1_Instances/THM-M-0545/ProofBoundaryCountermodel-2026-07-15.lean \
  "$tmp/ProofBoundaryCountermodel.lean"
cp Stage1_Instances/THM-M-0545/ProofCountermodel-2026-07-14.lean \
  "$tmp/ProofCountermodel.lean"
lean_path=$(cd Formalizations/Lean && timeout 30s lake env printenv LEAN_PATH)
lean_bin=$(cd Formalizations/Lean && lake env which lean)
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 \
  LEAN_PATH="$lean_path" timeout --foreground 600 "$lean_bin" \
  --trust=0 -t0 --root="$tmp" -o "$tmp/Statement.olean" \
  "$tmp/Statement.lean" > "$tmp/statement.log" 2>&1
statement_exit=$?
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 \
  LEAN_PATH="$tmp:$lean_path" timeout --foreground 600 "$lean_bin" \
  --trust=0 -t0 --root="$tmp" "$tmp/ProofBoundaryCountermodel.lean" \
  > "$tmp/boundary.log" 2>&1
boundary_exit=$?
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 \
  LEAN_PATH="$tmp:$lean_path" timeout --foreground 600 "$lean_bin" \
  --trust=0 -t0 --root="$tmp" "$tmp/ProofCountermodel.lean" \
  > "$tmp/realization.log" 2>&1
realization_exit=$?
sha256sum "$tmp/Statement.olean" "$tmp/statement.log" \
  "$tmp/boundary.log" "$tmp/realization.log"
wc -c "$tmp/Statement.olean" "$tmp/statement.log" \
  "$tmp/boundary.log" "$tmp/realization.log"
exit $(( statement_exit != 0 || boundary_exit != 0 || realization_exit != 0 ))
```

The replay ran from `2026-07-15T19:49:37+08:00` through
`2026-07-15T19:50:48+08:00`; all three Lean invocations exited `0`.
The statement object was 347208 bytes with SHA-256
`0cb3c19973217747cb7ee91bb25171d50212bdef10d4246cd1d5ccc952cb1bce`.
The statement log was 5758 bytes with SHA-256
`afcc4739ad6536f2f83577f6076cdcd38cbb3c15d867ddadac48cc5e417227a9`.
The boundary proof log was 495 bytes with SHA-256
`a3e7a99920e583bc2f934ad400af951ae9989b24410e7d7c68d18ae89a0c9f62`.
The realization proof log was 439 bytes with SHA-256
`ea27796c6b2205a152959ad24901f96ca03213689439e9530ab83b4ddaff6e60`.
Both exact trust results were:

```text
[propext, Classical.choice, Quot.sound]
```

Three read-only parallel inspections independently found the same
degree-zero contradiction, and two independently replayed the refutation with
the pinned toolchain. This is corroborating nonrelease evidence, not
independently provisioned release evidence.

Pinned environment: Linux `7.0.0-27-generic` `x86_64`; Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake
`5.0.0-src+98dc76e`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`.

The paired JSON artifact binds the task and obligation IDs, current immutable
base, source hashes, environment, command results, trust output, failure
boundary, and retry condition. This is fresh negative nonrelease evidence,
not a positive proof receipt.
