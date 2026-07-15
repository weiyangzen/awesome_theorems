# THM-M-0113 proof-phase escalation at `bf612698`

Item: `S56-M-0113-PROOF`

Recheck date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `bf6126986da025eabca097776ede0ba9484bbf71`

Base tree: `98c8e9b005d8d255ee3e05a1c34a449daf02a5a5`

## Verdict

`blocked`. No legal positive proof body can inhabit the unchanged frozen
target. The existing placeholder-free declaration

```text
Stage1Instances.THMM0113.not_hodgeDecompositionTarget :
  Not Stage1Instances.THMM0113.HodgeDecompositionTarget.{0, 0, 0, 0}
```

kernel-checks at trust level zero against a freshly elaborated
`Statement.olean`. Any universe-polymorphic positive proof of the canonical
target would specialize to this exact refuted instance.

`HodgeData.isKahler` is an unconstrained proposition. It does not relate the
geometric hypothesis to the independently chosen `cohomology` family or
`hodgePiece` submodules. The countermodel uses the zero-dimensional compact
complex manifold `Fin 0 -> Complex`, sets `isKahler := True`, interprets every
cohomology space as `Complex`, and makes every Hodge piece bottom. Complex
conjugation supplies the additive, conjugate-linear, and involutive laws. In
degree zero, the target would force the supremum of bottom submodules to be
top, hence force `1 = 0`.

This refutes the frozen Lean encoding, not the mathematical Hodge
decomposition theorem. Strengthening or narrowing the proposition inside this
proof item would substitute a different theorem. The negative declaration
therefore gives no positive root proof credit.

The assigned item remains `[ ]`. No proof receipt, item-state transition,
audit completion, theorem completion, validation completion, release, or
master-acceptance claim is made. `.stage1-worker-selftest.json` is deliberately
absent because the requested positive proof phase is not complete.

## Failed Gate

The first failed gate is
`S56-5.1-EXACT-TARGET-CONSISTENCY / M0113-S-DATA`. The immediate cut set is
the statement defect itself. The frozen positive graph also records analytic
leaves `M0113-A-DR`, `M0113-A-DOL`, `M0113-A-ELL`, `M0113-K-ID`, and
`M0113-C-CHAIN`, but execution cannot truthfully enter that architecture while
the root interface admits the checked countermodel.

The prerequisite `S56-M-0113-OBLIGATION_TREE` remains provisional `[_]`, not
master-accepted, so dependency-legal positive proof acceptance is
independently unavailable.

At worker start, the target already contained 37 structured proof recheck
pairs, while the scheduler authority still recorded `attempts: 0` and no
children. The tracked file count is not an authoritative tick counter, but it
shows repeated dispatch far beyond the standard's five-unresolved-tick split
threshold. Another unchanged positive-root dispatch cannot make proof
progress. Integration must reconcile the execution ledger and route a
statement repair or explicit counterexample-target redirection through the
prerequisite chain.

## Validation

All credited checks used the existing pinned toolchain and read-only symlink
to canonical Lake artifacts. No `lake update`, `lake build`, clone, fetch,
network access, or `.lake` mutation occurred. Lean output was confined to a
fresh directory under `/tmp` and removed by a shell trap. The pre-existing
untracked `.lake` symlink makes this nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0113` | 0 | Rank 25; lifecycle `planned`; baseline `L0/rework_required`; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0113/check_anchor_audit.py` | 0 | `ok: target boundary, four candidate rows, 12 Lean probes, and pinned mathlib revision agree` |
| `python3 Stage1_Instances/THM-M-0113/check_obligation_tree.py` | 0 | `PASS`: 26 obligations and 49 typed edges; denominator `e509c192...cbd5`; the frozen positive root remains M4. |
| Isolated `lake env lean` recipe below | 0 | Statement and countermodel elaborated at trust level zero. Lean printed the exact negation and axioms `[propext, Classical.choice, Quot.sound]`. Statement-output SHA-256 `483a37eb...7e84`; proof-output SHA-256 `ee6378a7...2d4c`; `Statement.olean` SHA-256 `94fe8a21...75e0`. |
| Scoped prohibited-declaration scan | 1 | Expected no-match: no placeholder, bodyless declaration, unsafe declaration, `implemented_by`, or `extern` occurs; the axiom report contains no `sorryAx`. |
| Lake-manifest package checkout scan | 0 | All 11 tracked package worktrees were clean at their recorded revisions; mathlib was `8a178386...a95`. |

The isolated Lean recipe, run from the repository root, was:

```bash
set -euo pipefail
ROOT=$PWD
LEAN_ROOT=$ROOT/Formalizations/Lean
TMP=$(mktemp -d /tmp/thm-m-0113-final-recheck-headbf612698-slot8.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
cp Stage1_Instances/THM-M-0113/Statement.lean "$TMP/Statement.lean"
cp Stage1_Instances/THM-M-0113/Proof.lean "$TMP/Proof.lean"
BASE_PATH=$(cd "$LEAN_ROOT" && timeout --foreground 600 \
  lake env printenv LEAN_PATH)
(cd "$LEAN_ROOT" && \
  ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 \
  LEAN_PATH="$BASE_PATH" timeout --foreground 600 lake env lean \
  --trust=0 -t0 --root="$TMP" -o "$TMP/Statement.olean" \
  "$TMP/Statement.lean" >"$TMP/statement-output.txt" 2>&1)
(cd "$LEAN_ROOT" && \
  ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 \
  LEAN_PATH="$TMP:$BASE_PATH" timeout --foreground 600 lake env lean \
  --trust=0 -t0 --root="$TMP" "$TMP/Proof.lean" \
  >"$TMP/proof-output.txt" 2>&1)
cat "$TMP/statement-output.txt" "$TMP/proof-output.txt"
sha256sum "$TMP/statement-output.txt" "$TMP/proof-output.txt" \
  "$TMP/Statement.olean"
```

Two earlier diagnostic invocations receive no validation credit. One exited
before producing captured output. The other used invalid Lean syntax
`-o=<path>`; Lean attempted to create a filename beginning with `=` and exited
1. The credited recipe above uses the valid two-argument form `-o <path>` and
exited 0 for both modules.

The scoped prohibited-declaration scan was:

```bash
rg -n --pcre2 \
  '\b(?:sorry|admit|sorryAx|native_decide)\b|^[[:space:]]*(?:axiom|constant|opaque|unsafe)[[:space:]]|implemented_by|extern[[:space:]]' \
  Stage1_Instances/THM-M-0113 --glob '*.lean'
```

Its exit code was 1, the expected no-match result. Two independent read-only
audits also found no exact theorem in pinned mathlib and independently
confirmed the countermodel. Nearby declarations such as `extDeriv_extDeriv`,
`harmonicOnNhd_const`, `Sheaf.H`, `KaehlerDifferential.D`, and `iSupIndep` are
support-only and cannot prove the exact target.

## Retry Condition

Do not reschedule the unchanged positive root. Replace the disconnected
`isKahler` proposition and arbitrary cohomology/Hodge-piece fields with native
definitions tied to the compact complex manifold, or add noncircular
law-bearing hypotheses. Then publish a new statement fingerprint and freshly
freeze and accept the statement, anchor audit, obligation registry, and typed
graphs before proof execution resumes. Alternatively, explicitly redirect
this item to the checked counterexample target.
