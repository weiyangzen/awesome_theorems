# THM-M-0113 proof-phase blocker at `4b5c39ff`

Item: `S56-M-0113-PROOF`

Recheck date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `4b5c39ffcc0e35a8509d4216af53c7cdeb190c7b`

Base tree: `e569e54769b7b5aab913ec248c533231658657f0`

## Verdict

`blocked`. No legal positive proof body can inhabit the exact frozen target.
The existing placeholder-free declaration

```text
Stage1Instances.THMM0113.not_hodgeDecompositionTarget :
  Not Stage1Instances.THMM0113.HodgeDecompositionTarget.{0, 0, 0, 0}
```

kernel-checks at trust level zero against a freshly elaborated
`Statement.olean`. A universe-polymorphic positive proof of the canonical
target would specialize to this refuted instance.

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

At worker start, the target already contained 42 structured proof recheck
pairs, while the scheduler authority still recorded `attempts: 0` and no
children. The tracked file count is not an authoritative tick counter, but it
shows repeated dispatch far beyond the standard's five-unresolved-tick split
threshold. Another unchanged positive-root dispatch cannot make proof
progress. Integration must reconcile the execution ledger and route a
statement repair or explicit counterexample-target redirection through the
prerequisite chain.

## Validation

All credited Lean checks used the existing pinned toolchain and read-only
symlink to canonical Lake artifacts. No `lake update`, `lake build`, clone,
fetch, network access, or `.lake` mutation occurred. Lean output was confined
to a fresh directory under `/tmp` and removed by a shell trap. The
pre-existing untracked `.lake` symlink makes this nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0113` | 0 | Rank 25; lifecycle `planned`; baseline `L0/rework_required`; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0113/check_anchor_audit.py` | 0 | `ok: target boundary, four candidate rows, 12 Lean probes, and pinned mathlib revision agree` |
| `python3 Stage1_Instances/THM-M-0113/check_obligation_tree.py` | 0 | `PASS`: 26 obligations and 49 typed edges; denominator `e509c192...cbd5`; the frozen positive root remains M4. |
| Isolated `lake env lean` recipe below | 0 | Statement and countermodel elaborated at trust level zero. Lean printed the exact negation and axioms `[propext, Classical.choice, Quot.sound]`; kernel-output SHA-256 `539fbb6...b1f9`; `Statement.olean` SHA-256 `94fe8a21...75e0`. |
| Scoped prohibited-declaration scan | 1 | Expected no-match: no placeholder, bodyless declaration, unsafe declaration, `implemented_by`, or `extern` occurs; the axiom report contains no `sorryAx`. |
| Lake-manifest package checkout scan | 0 | All 11 package worktrees were clean at their recorded revisions; mathlib was `8a178386...a95`. |
| `git diff --check -- Stage1_Instances/THM-M-0113` | 0 | No whitespace diagnostics. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The incomplete proof phase emitted no worker-completion packet. |

The isolated Lean recipe, run from `Formalizations/Lean`, was:

```bash
set -euo pipefail
tmp=$(mktemp -d /tmp/thm-m-0113-proof-recheck-head4b5c39ff.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp ../../Stage1_Instances/THM-M-0113/Statement.lean "$tmp/Statement.lean"
cp ../../Stage1_Instances/THM-M-0113/Proof.lean "$tmp/Proof.lean"
base_path=$(timeout 600 lake env printenv LEAN_PATH)
lean_bin=$(timeout 600 lake env which lean)
LEAN_NUM_THREADS=1 LEAN_PATH="$base_path" timeout 600 \
  "$lean_bin" --trust=0 -t 0 --root="$tmp" \
  -o "$tmp/Statement.olean" "$tmp/Statement.lean" \
  >"$tmp/kernel-output.txt" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base_path" timeout 600 \
  "$lean_bin" --trust=0 -t 0 --root="$tmp" "$tmp/Proof.lean" \
  >>"$tmp/kernel-output.txt" 2>&1
cat "$tmp/kernel-output.txt"
sha256sum "$tmp/kernel-output.txt" "$tmp/Statement.olean"
```

The scoped prohibited-declaration scan was:

```bash
rg -n --pcre2 \
  '\b(?:sorry|admit|sorryAx|native_decide)\b|^[[:space:]]*(?:axiom|constant|opaque|unsafe)[[:space:]]|implemented_by|extern[[:space:]]' \
  Stage1_Instances/THM-M-0113 --glob '*.lean'
```

Its exit code was 1, the expected no-match result. Independent read-only
requirements, target, and repository-pattern audits confirmed the same
statement defect and legal blocker boundary.

## Retry Condition

Do not reschedule the unchanged positive root. Replace the disconnected
`isKahler` proposition and arbitrary cohomology/Hodge-piece fields with native
definitions tied to the compact complex manifold, or add noncircular
law-bearing hypotheses. Then publish a new statement fingerprint and freshly
freeze and accept the statement, anchor audit, obligation registry, and typed
graphs before proof execution resumes. Alternatively, explicitly redirect
this item to the checked counterexample target.
