# THM-M-0113 proof-phase recheck at `a1ba351e`

Item: `S56-M-0113-PROOF`

Recheck date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `a1ba351e42fd9eefe315119ef09c0b958358bb8e`

Base tree: `eed1b90627305460f9cee46277fc7c0cb235d1df`

## Verdict

`blocked`. No legal positive proof body can inhabit the exact frozen target.
The existing placeholder-free declaration

```text
Stage1Instances.THMM0113.not_hodgeDecompositionTarget :
  Not Stage1Instances.THMM0113.HodgeDecompositionTarget.{0, 0, 0, 0}
```

kernel-checks at trust level zero against a freshly elaborated
`Statement.olean`.

The statement's `HodgeData.isKahler` field is an unconstrained proposition and
does not relate the geometric hypothesis to the independently chosen
`cohomology` family or `hodgePiece` submodules. The countermodel takes the
zero-dimensional compact complex manifold `Fin 0 -> Complex`, sets
`isKahler := True`, interprets every cohomology space as `Complex`, and makes
every Hodge piece bottom. Complex conjugation supplies the additive,
conjugate-linear, and involutive laws. In degree zero, the target would force
the supremum of bottom submodules to be top and hence force `1 = 0`.

This refutes the frozen Lean encoding, not the mathematical Hodge
decomposition theorem. Repairing, strengthening, or narrowing the target in
this proof item would be a forbidden theorem substitution. The positive
obligation registry therefore cannot receive closure credit from the negative
declaration. The pinned mathlib snapshot also has no exact positive Hodge
decomposition declaration to import; its nearby manifold, harmonic-function,
and algebraic Kahler-differential infrastructure cannot inhabit this target.

The assigned item remains `[ ]`. No positive proof receipt, state transition,
audit completion, theorem completion, validation completion, release, or
master-acceptance claim is made. No `.stage1-worker-selftest.json` is written
because the requested proof phase is not genuinely complete.

## Failed Gate And Retry

The first failed gate is
`S56-5.1-EXACT-TARGET-CONSISTENCY / M0113-S-DATA`. Replace the disconnected
`isKahler` proposition and arbitrary cohomology/Hodge-piece fields with native
definitions tied to the compact complex manifold, or add noncircular
law-bearing hypotheses sufficient to derive the intended conclusion. Then
publish a new statement fingerprint, repair the mutation evidence, and freshly
freeze and accept the statement, anchor audit, obligation registry, and typed
graphs before resuming positive proof work. Alternatively, redirect the item
explicitly to the checked counterexample target.

The current frozen graph cut set remains `M0113-A-DR`, `M0113-A-DOL`,
`M0113-A-ELL`, `M0113-K-ID`, and `M0113-C-CHAIN`; the earlier statement defect
blocks entry to that proof architecture. The prior registry projection remains
open at M4, while this recheck proposes M5 backend-target blocker evidence
without changing the H4 status of the intended mathematical theorem or any
predecessor state. The prerequisite obligation-tree item remains provisional
`[_]`, rather than master-accepted, which independently prevents a legal proof
completion claim.

There were already 48 tracked structured blocker rechecks before this run,
while the authoritative proof item still records zero attempts and no
children. Those files are evidence of repeated dispatch, not an authoritative
attempt ledger. Under the rev-5.6 split rule, the scheduler should stop
redispatching the unchanged root and route it to statement repair or an
explicitly redirected counterexample task. This worker did not edit scheduler
authority.

## Validation

All checks ran in this worker clone using the existing symlink to the canonical
pinned Lake artifacts. No `lake update`, `lake build`, dependency clone/fetch,
network action, or `.lake` mutation was performed. Lean output was confined to
a fresh directory under `/tmp` and removed after validation. The pre-existing
untracked `.lake` symlink makes this nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0113` | 0 | Rank 25; lifecycle `planned`; baseline `L0/rework_required`; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0113/check_anchor_audit.py` | 0 | Target boundary, four candidate rows, 12 Lean probes, and pinned mathlib revision agree. |
| `python3 Stage1_Instances/THM-M-0113/check_obligation_tree.py` | 0 | `PASS`: 26 obligations and 49 typed edges; denominator `e509c192...cbd5`; the prior positive root remains open at M4. |
| Isolated `lake env lean` recipe below | 0 | The statement and countermodel elaborated at trust level zero. Lean reported axioms exactly `[propext, Classical.choice, Quot.sound]`; combined output SHA-256 `539fbb6d...331b1f9`; `Statement.olean` SHA-256 `94fe8a21...d975e0`. |
| Scoped prohibited-declaration scan | 1 | Expected no-match: no `sorry`, `admit`, `sorryAx`, `native_decide`, bodyless declaration, unsafe declaration, `implemented_by`, or `extern` occurs in the owned Lean sources. |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 at commit `98dc76e...` and Lake `5.0.0-src+98dc76e`. |
| Package checkout status scan | 0 | All 11 manifest package Git worktrees were clean at their recorded revisions; mathlib was `8a178386...a95`. |
| Structured JSON and invariant checks | 0 | Current-base identity, input hashes, kernel result, open state, empty receipt lists, and deliberate self-test absence agree. |
| Scoped whitespace checks | 0 | Tracked diff and both owned-path additions have no whitespace errors. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The incomplete proof phase emitted no worker-completion packet. |

The isolated Lean recipe was:

```bash
set -euo pipefail
tmp=$(mktemp -d /tmp/thm-m-0113-proof-recheck-heada1ba351e-slot2.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-0113/Statement.lean "$tmp/Statement.lean"
cp Stage1_Instances/THM-M-0113/Proof.lean "$tmp/Proof.lean"
base_path=$(cd Formalizations/Lean && timeout 600 lake env printenv LEAN_PATH)
lean_bin=$(cd Formalizations/Lean && timeout 600 lake env which lean)
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 \
  LEAN_PATH="$base_path" timeout --foreground 600 "$lean_bin" \
  --trust=0 -t0 --root="$tmp" -o "$tmp/Statement.olean" \
  "$tmp/Statement.lean" >"$tmp/statement-output.txt" 2>&1
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 \
  LEAN_PATH="$tmp:$base_path" timeout --foreground 600 "$lean_bin" \
  --trust=0 -t0 --root="$tmp" "$tmp/Proof.lean" \
  >"$tmp/proof-output.txt" 2>&1
cat "$tmp/statement-output.txt" "$tmp/proof-output.txt"
sha256sum "$tmp/statement-output.txt" "$tmp/proof-output.txt" \
  "$tmp/Statement.olean"
cat "$tmp/statement-output.txt" "$tmp/proof-output.txt" | sha256sum
```

The output hashes were:

| Output | SHA-256 |
|---|---|
| Elaborated target print | `483a37eb70184d0596b11301c4e15018629fd00bbd8a601fdc6ad7691dcd7e84` |
| Countermodel declaration and axioms | `ee6378a7e948bc9267ee992aaa0355f1d6717185bddfcf0c3ac7099bd90b2d4c` |
| Concatenated kernel output | `539fbb6d2ea328fe07b99cddf2e5b4ee88fda234d3e19983d73f7e244331b1f9` |
| `Statement.olean` | `94fe8a2182ea2776a7f9972ca82cd7c88b50fb2f57091d6527a82eb178d975e0` |

The scoped prohibited-declaration scan was:

```bash
rg -n --pcre2 \
  '\b(?:sorry|admit|sorryAx|native_decide)\b|^[[:space:]]*(?:axiom|constant|opaque|unsafe)[[:space:]]|implemented_by|extern[[:space:]]' \
  Stage1_Instances/THM-M-0113 --glob '*.lean'
```

Its exit code was `1`, the expected no-match result. Lean's printed axiom
dependency report is the kernel-derived trust evidence for the countermodel.
The structured artifact records all checked input hashes, package revisions,
commands, debt boundaries, retry conditions, and freshness rules.

This is durable blocker evidence, not a proof receipt. Because the assigned
positive proof phase is not genuinely self-tested as complete,
`.stage1-worker-selftest.json` is deliberately absent.
