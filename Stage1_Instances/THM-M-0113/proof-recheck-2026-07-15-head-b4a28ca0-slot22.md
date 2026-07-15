# THM-M-0113 proof-phase recheck at `b4a28ca0`

Item: `S56-M-0113-PROOF`

Recheck date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `b4a28ca0ddecda7bf1bcfb2e0309f6596caf75bf`

Base tree: `2fd84e6cf7daf8b6696416d97e3fbb9576042ba1`

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
this proof item would be a forbidden theorem substitution. The existing
positive obligation registry therefore cannot receive closure credit from the
negative declaration.

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
publish a new statement fingerprint and freshly freeze and accept the
statement, anchor audit, obligation registry, and typed graphs before resuming
positive proof work. Alternatively, redirect the item explicitly to the
checked counterexample target.

The frozen positive graph still records the analytic cut set `M0113-A-DR`,
`M0113-A-DOL`, `M0113-A-ELL`, `M0113-K-ID`, and `M0113-C-CHAIN`, but the
earlier statement defect `M0113-S-DATA` blocks entry to that proof
architecture. The prior registry projection remains open at M4; this recheck
proposes M5 for the frozen formal target, while the human-source classification
of the intended Hodge theorem remains H4 in the current registry.

The prerequisite `S56-M-0113-OBLIGATION_TREE` remains provisional `[_]`, not
master-accepted, so dependency-legal proof acceptance is independently
unavailable. The scheduler records `attempts: 0` even though the target already
contained 26 structured proof rechecks at worker start. Another unchanged-
target proof dispatch cannot create positive proof progress; integration must
repair or explicitly redirect the statement chain and reconcile the task
counter.

## Validation

The target checks used the existing canonical pinned Lake artifacts read only.
No `lake update`, `lake build`, dependency clone/fetch, network action, or
intentional `.lake` write was performed. Lean output was confined to a fresh
directory under `/tmp` and removed after validation. The pre-existing
untracked `.lake` symlink makes this nonrelease evidence.

The prescribed project-root Lake preflight failed because the shared
`flt-regular` checkout has an unresolvable `HEAD` at
`refs/heads/.invalid`. The manifest-pinned commit object
`56161b6e...1a27` is present, but this worker did not fetch, repair, or check it
out. The narrow kernel check invoked `lake env lean` from the fresh `/tmp`
validation directory, with `ELAN_TOOLCHAIN` selecting the pinned toolchain and
`LEAN_PATH` containing only pre-existing compiled Lake artifacts.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0113` | 0 | Rank 25; lifecycle `planned`; baseline `L0/rework_required`; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0113/check_anchor_audit.py` | 0 | `ok: target boundary, four candidate rows, 12 Lean probes, and pinned mathlib revision agree` |
| `python3 Stage1_Instances/THM-M-0113/check_obligation_tree.py` | 0 | `PASS`: 26 obligations and 49 typed edges; denominator `e509c192...cbd5`; the positive root remains open at M4. |
| Isolated `lake env lean` recipe below | 0 | The exact statement and countermodel elaborated at trust level zero. Lean reported axioms exactly `[propext, Classical.choice, Quot.sound]`; statement-output SHA-256 `483a37eb...7e84`; proof-output SHA-256 `ee6378a7...2d4c`; `Statement.olean` SHA-256 `94fe8a21...75e0`. |
| Scoped prohibited-declaration scan | 1 | Expected no-match: no prohibited declaration or placeholder occurs in the owned Lean sources; Lean's axiom report contains no `sorryAx`. |
| Project-root `timeout --foreground 30 lake env lean --version` | 1 | Lake reported that `flt-regular` could not resolve `HEAD`; no repair was attempted. |
| `git -C .../mathlib rev-parse HEAD` | 0 | Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| `git -C .../flt-regular cat-file -e 56161b6e...1a27^{commit}` | 0 | The manifest-pinned commit object is present despite the unresolvable checkout `HEAD`. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The incomplete proof phase emitted no worker-completion packet. |

The isolated Lean recipe, run from the repository root, was:

```bash
set -u
tmp=$(mktemp -d /tmp/thm-m-0113-proof-recheck-slot22.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
root=$PWD/Formalizations/Lean
path=$root/.lake/packages/batteries/.lake/build/lib/lean:$root/.lake/packages/Qq/.lake/build/lib/lean:$root/.lake/packages/aesop/.lake/build/lib/lean:$root/.lake/packages/proofwidgets/.lake/build/lib/lean:$root/.lake/packages/LeanSearchClient/.lake/build/lib/lean:$root/.lake/packages/plausible/.lake/build/lib/lean:$root/.lake/packages/importGraph/.lake/build/lib/lean:$root/.lake/packages/mathlib/.lake/build/lib/lean:$root/.lake/build/lib/lean
cp Stage1_Instances/THM-M-0113/Statement.lean "$tmp/Statement.lean"
cp Stage1_Instances/THM-M-0113/Proof.lean "$tmp/Proof.lean"
(cd "$tmp" &&
  ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 \
    LEAN_PATH="$path" timeout --foreground 600 lake env lean \
    --trust=0 -t0 --root="$tmp" -o "$tmp/Statement.olean" \
    "$tmp/Statement.lean" >"$tmp/statement-output.txt" 2>&1)
(cd "$tmp" &&
  ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 \
    LEAN_PATH="$tmp:$path" timeout --foreground 600 lake env lean \
    --trust=0 -t0 --root="$tmp" "$tmp/Proof.lean" \
    >"$tmp/proof-output.txt" 2>&1)
cat "$tmp/statement-output.txt" "$tmp/proof-output.txt"
sha256sum "$tmp/statement-output.txt" "$tmp/proof-output.txt" \
  "$tmp/Statement.olean"
```

The scoped prohibited-declaration scan was:

```bash
rg -n --pcre2 \
  '\b(?:sorry|admit|sorryAx|native_decide)\b|^[[:space:]]*(?:axiom|constant|opaque|unsafe)[[:space:]]|implemented_by|extern[[:space:]]' \
  Stage1_Instances/THM-M-0113 --glob '*.lean'
```

Its exit code was `1`, the expected no-match result. Lean's printed axiom
dependency report is the kernel-derived trust evidence for the countermodel.

The checked input SHA-256 values are recorded in the companion JSON packet.
This is current-base durable blocker evidence, not a proof receipt. Because the
assigned positive proof phase is not genuinely self-tested as complete,
`.stage1-worker-selftest.json` is deliberately absent.
