# THM-M-0113 proof-phase recheck at `4d389eb4`

Item: `S56-M-0113-PROOF`

Recheck date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `4d389eb47e043f6f44925a418baee0d034f764ba`

Base tree: `64faabd76665273032b8cb1554b90655b5c94256`

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
earlier statement defect `M0113-S-DATA` blocks entry to that architecture. The
prior registry projection remains open at M4; this recheck proposes M5 for the
frozen formal target, while the human-source classification of the intended
Hodge theorem remains H4 in the current registry.

The prerequisite `S56-M-0113-OBLIGATION_TREE` remains provisional `[_]`, not
master-accepted, so dependency-legal proof acceptance is independently
unavailable. The scheduler records `attempts: 0` even though the target
already contained 36 structured proof rechecks at worker start. That count is
evidence of repeated dispatch, not an authoritative tick ledger, but it is far
beyond the standard's five-unresolved-tick split threshold. Another
unchanged-target proof dispatch cannot create positive proof progress;
integration must repair or explicitly redirect the statement chain and
reconcile the task counter.

## Validation

All checks ran in this worker clone using the existing symlink to the canonical
pinned Lake artifacts. No `lake update`, `lake build`, dependency clone/fetch,
network action, or `.lake` mutation was performed. Lean output was confined to
a fresh directory under `/tmp` and removed by a shell trap. The pre-existing
untracked `.lake` symlink makes this nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0113` | 0 | Rank 25; lifecycle `planned`; baseline `L0/rework_required`; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0113/check_anchor_audit.py` | 0 | `ok: target boundary, four candidate rows, 12 Lean probes, and pinned mathlib revision agree` |
| `python3 Stage1_Instances/THM-M-0113/check_obligation_tree.py` | 0 | `PASS`: 26 obligations and 49 typed edges; denominator `e509c192...cbd5`; the positive root remains open at M4. |
| `cd Formalizations/Lean && timeout --foreground 30 lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3...b16740`, Release. |
| Isolated `lake env lean` recipe below | 0 | The exact statement and countermodel elaborated at trust level zero. Lean reported axioms exactly `[propext, Classical.choice, Quot.sound]`; statement-output SHA-256 `483a37eb...7e84`; proof-output SHA-256 `ee6378a7...2d4c`; `Statement.olean` SHA-256 `94fe8a21...75e0`. |
| Scoped prohibited-declaration scan | 1 | Expected no-match: no prohibited declaration or placeholder occurs in the owned Lean sources; Lean's axiom report contains no `sorryAx`. |
| Lake-manifest package checkout scan | 0 | All 11 package Git worktrees were clean at their recorded revisions. |
| `python3 -m json.tool` and scoped blocker invariant assertions | 0 | The packet parses and its item/base identity, blocked/open state, hashes, negative kernel result, empty receipts, and deliberate self-test absence agree. |
| `git diff --check` and new-file checks | 0 | No tracked or new-file whitespace diagnostics. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The incomplete proof phase emitted no worker-completion manifest. |

The isolated Lean recipe, run from the repository root, was:

```bash
set -u
ROOT=$PWD
LEAN_ROOT=$ROOT/Formalizations/Lean
CACHE=$LEAN_ROOT/.lake
LEAN_PATH_BASE=$CACHE/packages/batteries/.lake/build/lib/lean:$CACHE/packages/Qq/.lake/build/lib/lean:$CACHE/packages/aesop/.lake/build/lib/lean:$CACHE/packages/proofwidgets/.lake/build/lib/lean:$CACHE/packages/LeanSearchClient/.lake/build/lib/lean:$CACHE/packages/plausible/.lake/build/lib/lean:$CACHE/packages/importGraph/.lake/build/lib/lean:$CACHE/packages/mathlib/.lake/build/lib/lean:$LEAN_ROOT/.lake/build/lib/lean
TMP=$(mktemp -d /tmp/thm-m-0113-proof-recheck-slot8.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
cp Stage1_Instances/THM-M-0113/Statement.lean "$TMP/Statement.lean"
cp Stage1_Instances/THM-M-0113/Proof.lean "$TMP/Proof.lean"
(cd "$TMP" &&
  ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 \
    LEAN_PATH="$LEAN_PATH_BASE" timeout --foreground 600 lake env lean \
    --trust=0 -t0 --root="$TMP" -o "$TMP/Statement.olean" \
    "$TMP/Statement.lean" >"$TMP/statement-output.txt" 2>&1)
(cd "$TMP" &&
  ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 \
    LEAN_PATH="$TMP:$LEAN_PATH_BASE" timeout --foreground 600 lake env lean \
    --trust=0 -t0 --root="$TMP" "$TMP/Proof.lean" \
    >"$TMP/proof-output.txt" 2>&1)
cat "$TMP/statement-output.txt" "$TMP/proof-output.txt"
sha256sum "$TMP/statement-output.txt" "$TMP/proof-output.txt" \
  "$TMP/Statement.olean"
```

The scoped prohibited-declaration scan was:

```bash
rg -n --pcre2 \
  '\b(?:sorry|admit|sorryAx|native_decide)\b|^[[:space:]]*(?:axiom|constant|opaque|unsafe)[[:space:]]|implemented_by|extern[[:space:]]' \
  Stage1_Instances/THM-M-0113 --glob '*.lean'
```

Its exit code was `1`, the expected no-match result. Lean's printed axiom
dependency report is the kernel-derived trust evidence for the countermodel.

The checked input SHA-256 values are:

| Input | SHA-256 |
|---|---|
| `Statement.lean` | `73010040e7a16c02d00bfa95db270e2370440f433e8c3519e5e2ab429cd236dd` |
| `Proof.lean` | `b05f2ef3eef236e026930097803c614d53eeaba65d5fa936b0293a7c4879ec6f` |
| `ObligationTree.lean` | `c9fe3593539b1a3d221496ad45c3b5a9cfcd1355b3875f7b42d4012337273a95` |
| `obligation-registry.json` | `c8f592dd2961e08782a241355e0eaf2f1d6841b8e66b325bab5d07c936847f2d` |
| `typed-graphs.json` | `31b91ed2b0c42702819148e6ab02e222e06f801bd0e1cc9e81788d26f2606e34` |
| `anchor-audit.json` | `96d93459b27f3a95357e041e0a9cf589d849ef5066894551e646b5dbb5027795` |
| `Formalizations/Lean/lake-manifest.json` | `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81` |
| `Formalizations/Lean/lean-toolchain` | `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2` |
| `Docs/Stage1_Execution_DAG_rev-5.6.json` | `53bf6c3d561c7efd021a8813137f297193e83bbe3b470000eda0ac9773b855ec` |

This is current-base, durable blocker evidence, not a proof receipt. Because
the assigned positive proof phase is not genuinely self-tested as complete,
`.stage1-worker-selftest.json` is deliberately absent.
