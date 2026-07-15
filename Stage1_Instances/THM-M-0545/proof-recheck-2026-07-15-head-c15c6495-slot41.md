# THM-M-0545 proof-phase recheck at base c15c6495

Item: `S56-M-0545-PROOF`

Intent: `prove`

Recheck date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `c15c649568664c4e58150dd755cb28f156d15ecb`

Base tree: `792c3ed97f9263da7e6a39abdce8d5e37a100368`

## Verdict

`blocked`. No positive proof body can consistently inhabit the exact frozen
Lean target. The existing placeholder-free declaration

```text
Stage1Instances.THMM0545.not_hodgeDecompositionTarget :
  Not Stage1Instances.THMM0545.HodgeDecompositionTarget.{0, 0, 0, 0}
```

kernel-checks at trust level zero against a freshly elaborated temporary
`Statement.olean`. Any universe-polymorphic proof of the requested positive
target would specialize to universes `(0, 0, 0, 0)` and contradict this
declaration.

The frozen encoding quantifies over every `HodgeAnalyticData`, but its
`realizesSmoothComplexForms` and `realizesHodgeOperators` fields are
unconstrained propositions. They impose no laws connecting the supplied form
spaces, exterior derivative, codifferential, or Laplacian to the manifold.

There is also a stronger, operator-independent boundary defect. `IsExact D 0
e` requires a natural number `j` satisfying `j + 1 = 0`, so it is empty, while
`HasUniqueDecomposition` still requires an exact summand at degree zero. The
new placeholder-free `ProofBoundaryCountermodel-2026-07-15.lean` checks
`not_isExact_zero`, `no_degreeZeroDecomposition`, and a second root refutation:

```text
Stage1Instances.THMM0545.not_hodgeDecompositionTarget_degreeZero :
  Not Stage1Instances.THMM0545.HodgeDecompositionTarget.{0, 0, 0, 0}
```

The checked countermodel specializes to the compact zero-dimensional
Euclidean Riemannian manifold. It uses `Complex` as every form space, takes the
exterior derivative and codifferential to be zero, takes the Laplacian to be
the identity, and makes all four proposition fields true. At degree one,
harmonicity forces the harmonic summand to zero and the two zero images force
the exact and coexact summands to zero. Hence the form `1` cannot equal their
sum.

This refutes the overbroad abstract encoding, not the mathematical Hodge
decomposition theorem. No positive proof body, proof receipt, composition
certificate, or frozen obligation was added or closed. The proof item remains
`[ ]`; the recorded root vector remains `[H3, M4, R4]`, with `[H3, M5, R4]`
only a fail-closed diagnosis proposed for master reconciliation. Audit
completion, validation, release, theorem completion, and master acceptance
remain false. The predecessor obligation-tree item is worker-provisional
rather than master-accepted.

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
replaces the unconstrained realization propositions with concrete pinned
definitions or source-justified, noncircular law-bearing structures that rule
out this countermodel without assuming the desired decomposition. The
corrected target must receive a newly accepted expression fingerprint,
followed by fresh statement, anchor-audit, obligation-tree, and proof phases
in dependency order.

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
| Isolated `lake env lean --trust=0 -t 0` recipe below | 0 | Exact statement and universe-zero refutation elaborated; `#print axioms` reported `[propext, Classical.choice, Quot.sound]`. |
| Separate degree-zero `lake env lean --trust=0 -t 0` replay | 0 | The new local diagnostic proof checked that `IsExact` is empty at degree zero, no degree-zero decomposition exists, and the exact universal root is false. |
| Independent read-only replay | 0 | A separate proof-analysis worker obtained the same exits, object hash, declaration, and axiom report. This is corroboration, not release-grade independent verification. |
| Pinned mathlib search for analytic Hodge APIs | 1 | Expected no-match result: no Hodge-decomposition, Hodge-Laplacian, or codifferential theorem was found in the pinned mathlib source. |
| Prohibited-proof-escape scan of owned Lean sources | 1 | Expected no-match result: zero prohibited constructs were found. |
| `python3 -m json.tool` plus inline identity/base/hash assertions | 0 | Structured blocker JSON is valid; identity, base/tree, unfinished state, changed paths, and all 13 source hashes agree. |
| `git diff --check` plus three new-file checks | 0 | No whitespace diagnostics; new-file checks returned only their expected difference exits. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion manifest is absent because the positive proof phase is blocked. |

Exact primary replay, run from the repository root:

```bash
set -uo pipefail
start=$(TZ=Asia/Shanghai date --iso-8601=seconds)
tmp=$(mktemp -d /tmp/thm-m-0545-proof-c15c6495-slot41.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-0545/Statement.lean "$tmp/Statement.lean"
cp Stage1_Instances/THM-M-0545/ProofCountermodel-2026-07-14.lean \
  "$tmp/ProofCountermodel.lean"
lean_path=$(cd Formalizations/Lean && timeout 30s lake env printenv LEAN_PATH)
cd "$tmp"
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 \
  LEAN_PATH="$lean_path" timeout 300s lake env lean --trust=0 -t 0 \
  --root="$tmp" -o Statement.olean Statement.lean > statement.log 2>&1
statement_exit=$?
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 \
  LEAN_PATH="$tmp:$lean_path" timeout 300s lake env lean --trust=0 -t 0 \
  --root="$tmp" ProofCountermodel.lean > proof.log 2>&1
proof_exit=$?
sha256sum Statement.olean statement.log proof.log
wc -c Statement.olean statement.log proof.log
exit $(( statement_exit != 0 || proof_exit != 0 ))
```

The primary replay ran from `2026-07-15T16:15:31+08:00` through
`2026-07-15T16:16:06+08:00`; both Lean invocations exited `0`. The statement
object was 347208 bytes with SHA-256
`0cb3c19973217747cb7ee91bb25171d50212bdef10d4246cd1d5ccc952cb1bce`.
The statement log was 5758 bytes with SHA-256
`afcc4739ad6536f2f83577f6076cdcd38cbb3c15d867ddadac48cc5e417227a9`.
The proof log was 439 bytes with SHA-256
`ea27796c6b2205a152959ad24901f96ca03213689439e9530ab83b4ddaff6e60`.
The exact trust result was:

```text
'Stage1Instances.THMM0545.not_hodgeDecompositionTarget' depends on axioms:
[propext, Classical.choice, Quot.sound]
```

The separate degree-zero replay ran from `2026-07-15T16:23:45+08:00`
through `2026-07-15T16:24:16+08:00`. Its Lean invocations both exited `0`;
the proof log was 495 bytes with SHA-256
`a3e7a99920e583bc2f934ad400af951ae9989b24410e7d7c68d18ae89a0c9f62`,
and its exact axiom report was again `[propext, Classical.choice, Quot.sound]`.

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake
`5.0.0-src+98dc76e`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`.

The paired JSON artifact binds the task and obligation IDs, current immutable
base, source hashes, environment, command results, trust output, failure
boundary, and retry condition. This is fresh negative nonrelease evidence,
not a positive proof receipt.
