# THM-M-0113 proof-phase blocker at `b73dae2e`

Item: `S56-M-0113-PROOF`

Recheck date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `b73dae2e6741a0be1f316d748a37f487a671cca4`

Base tree: `d582d50d420e2a27b4fb21ed0abea58cee03184f`

## Verdict

`blocked`. A positive proof body cannot inhabit the exact frozen target. The
existing placeholder-free declaration

```text
Stage1Instances.THMM0113.not_hodgeDecompositionTarget :
  Not Stage1Instances.THMM0113.HodgeDecompositionTarget.{0, 0, 0, 0}
```

kernel-checks at trust level zero against a freshly elaborated
`Statement.olean`.

`HodgeData.isKahler` is an unconstrained proposition. It does not connect the
geometric hypothesis to the independently chosen `cohomology` family or
`hodgePiece` submodules. The checked countermodel takes the zero-dimensional
compact complex manifold `Fin 0 -> Complex`, sets `isKahler := True`, uses
`Complex` in every cohomological degree, and makes every Hodge piece bottom.
Complex conjugation satisfies the additive, conjugate-linear, and involutive
fields. In degree zero, the target would force the supremum of bottom
submodules to be top and hence force `1 = 0`.

This refutes the frozen Lean encoding, not the mathematical Hodge
decomposition theorem. Repairing, strengthening, or narrowing the statement
inside this proof item would substitute a different theorem. The anchor audit
also supplies no exact positive pinned theorem to import: its mathlib and
external candidates are supporting infrastructure or different statements.

The assigned item remains `[ ]`. The negative theorem gives no positive root
or obligation closure, proof receipt, state transition, audit completion,
theorem completion, validation completion, release, or master-acceptance
credit. `.stage1-worker-selftest.json` is deliberately absent because the
requested positive proof phase is not complete.

## Failed Gate And Retry

The first failed gate is
`S56-5.1-EXACT-TARGET-CONSISTENCY / M0113-S-DATA`. Replace the disconnected
`isKahler` proposition and arbitrary cohomology/Hodge-piece fields with native
definitions tied to the compact complex manifold, or add noncircular
law-bearing hypotheses sufficient to derive the intended conclusion. Repair
the statement mutation tests, publish a new statement fingerprint, and
freshly freeze and accept the statement, anchor audit, obligation registry,
and typed graphs before resuming positive proof work. The other legal route is
to redirect the assignment explicitly to the checked counterexample target.

The frozen positive graph still lists `M0113-A-DR`, `M0113-A-DOL`,
`M0113-A-ELL`, `M0113-K-ID`, and `M0113-C-CHAIN` as its analytic cut set, but
the earlier `M0113-S-DATA` defect blocks entry to that architecture. The
registry remains open at M4; this packet proposes only an M5 classification
for the false backend target and does not change the H4 classification of the
intended mathematical theorem. The prerequisite
`S56-M-0113-OBLIGATION_TREE` is provisional `[_]`, not master-accepted, which
independently prevents dependency-legal proof acceptance.

There were already 49 tracked structured proof rechecks at worker start while
the task authority still records `attempts: 0` and no children. These files
are repeated-dispatch evidence, not an authoritative attempt counter. The
rev-5.6 five-unresolved-tick rule requires routing this work to statement
repair or an explicit redirected child rather than dispatching the unchanged
positive root again. This worker did not edit scheduler authority.

## Validation

All Lean checks used the existing automation-provided symlink to canonical
pinned Lake artifacts. No dependency update, build, clone, fetch, network
operation, or `.lake` mutation was performed. Generated Lean output was
confined to a fresh directory under `/tmp` and removed by an exit trap. The
untracked `.lake` symlink makes this nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0113` | 0 | Rank 25; lifecycle `planned`; baseline `L0/rework_required`; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0113/check_anchor_audit.py` | 0 | `ok: target boundary, four candidate rows, 12 Lean probes, and pinned mathlib revision agree` |
| `python3 Stage1_Instances/THM-M-0113/check_obligation_tree.py` | 0 | `PASS`: 26 obligations and 49 typed edges; denominator `e509c192...cbd5`; root remains M4 with five analytic cut-set leaves. |
| Isolated trust-zero Lean recipe below | 0 | The statement and countermodel elaborated. Axioms were exactly `[propext, Classical.choice, Quot.sound]`; combined output SHA-256 `539fbb6d...331b1f9`; `Statement.olean` SHA-256 `94fe8a21...d975e0`. |
| Scoped prohibited-declaration scan | 1 | Expected no-match: no `sorry`, `admit`, `sorryAx`, `native_decide`, bodyless declaration, unsafe declaration, `implemented_by`, or `extern` occurs in the owned Lean sources. |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 at commit `98dc76e...` and Lake `5.0.0-src+98dc76e`. |
| Lake-manifest package status scan | 0 | All 11 package worktrees were clean at their exact recorded revisions; mathlib was `8a178386...a95`. |
| `python3 -m json.tool Stage1_Instances/THM-M-0113/proof-recheck-2026-07-15-head-b73dae2e-slot2.json >/dev/null` | 0 | The blocker packet is valid JSON. |
| Current-base invariant assertions | 0 | Item/base identity, hashes, open state, negative kernel result, empty receipt sets, and deliberate self-test absence agree. |
| Scoped whitespace checks | 0 | The two owned-path additions have no whitespace errors. |
| Per-file `git diff --no-index --check /dev/null <artifact>` | 1 | Expected content-difference status with empty output for each new artifact; no whitespace diagnostic occurred. |
| `test ! -e .stage1-worker-selftest.json` | 0 | No completion packet exists for this blocked proof phase. |

The isolated Lean recipe was:

```bash
set -euo pipefail
tmp=$(mktemp -d /tmp/thm-m-0113-proof-recheck-headb73dae2e-slot2.XXXXXX)
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
| Countermodel declaration and axiom report | `ee6378a7e948bc9267ee992aaa0355f1d6717185bddfcf0c3ac7099bd90b2d4c` |
| Concatenated kernel output | `539fbb6d2ea328fe07b99cddf2e5b4ee88fda234d3e19983d73f7e244331b1f9` |
| `Statement.olean` | `94fe8a2182ea2776a7f9972ca82cd7c88b50fb2f57091d6527a82eb178d975e0` |

The scoped source scan was:

```bash
rg -n --pcre2 \
  '\b(?:sorry|admit|sorryAx|native_decide)\b|^[[:space:]]*(?:axiom|constant|opaque|unsafe)[[:space:]]|implemented_by|extern[[:space:]]' \
  Stage1_Instances/THM-M-0113 --glob '*.lean'
```

Its exit code `1` is the expected no-match result. Lean's printed axiom
dependency report is the trust evidence for the negative declaration. The
structured companion records the checked input hashes, exact environment,
commands, debt boundary, failed gate, and retry condition.

This is a durable blocker report, not a proof receipt. Because the assigned
positive phase is not genuinely self-tested as complete, no worker self-test
manifest is written.
