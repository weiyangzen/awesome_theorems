# THM-M-0113 proof-phase blocker recheck

Item: `S56-M-0113-PROOF`

Base revision: `fc1568a2997ca815b767b8cc172f3d4d339bf3b9`

Verdict: `blocked`

## Result

The required positive proof body cannot be implemented for the exact frozen
Lean proposition. The existing placeholder-free declaration

```lean
Stage1Instances.THMM0113.not_hodgeDecompositionTarget :
  Not Stage1Instances.THMM0113.HodgeDecompositionTarget.{0, 0, 0, 0}
```

kernel-checks at trust level zero against a freshly elaborated
`Statement.olean`.

`HodgeData.isKahler` is an unconstrained proposition and does not relate the
geometric hypothesis to the independently chosen `cohomology` family or
`hodgePiece` submodules. The countermodel takes the zero-dimensional compact
complex manifold `Fin 0 -> Complex`, sets `isKahler := True`, interprets every
cohomology space as `Complex`, and makes every Hodge piece bottom. Complex
conjugation supplies the additive, conjugate-linear, and involutive laws. In
degree zero, the target would force the supremum of bottom submodules to be
top and hence force `1 = 0`.

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

The statement mutation gate also remains defective: the recorded fixtures do
not show all required non-equivalence failures, and the fixture named
`MutationRemovedCompactness` still assumes `[CompactSpace M]`. Any statement
repair must correct and rerun those mutation checks before proof evidence is
inspected.

The frozen positive graph still records the analytic cut set `M0113-A-DR`,
`M0113-A-DOL`, `M0113-A-ELL`, `M0113-K-ID`, and `M0113-C-CHAIN`, but the
earlier statement defect `M0113-S-DATA` blocks entry to that proof
architecture. The prior registry projection remains open at M4; this recheck
proposes only M5 backend-target blocker evidence. It does not change the H4
status of the intended mathematical theorem or alter predecessor state.

The prerequisite `S56-M-0113-OBLIGATION_TREE` remains provisional `[_]`. That
does not bar provisional proof preparation, but master acceptance must remain
dependency ordered. More decisively, the positive proposition is refuted.
The target contained 34 structured proof rechecks at worker start while the
scheduler still records `attempts: 0` and no children. Another unchanged proof
dispatch cannot create positive progress. Downstream leaf splitting also
cannot repair this upstream statement defect; integration must redirect or
repair the statement chain and reconcile the execution counter.

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
| `python3 Stage1_Instances/THM-M-0113/check_anchor_audit.py` | 0 | Target boundary, four candidate rows, 12 Lean probes, and pinned mathlib revision agree. |
| `python3 Stage1_Instances/THM-M-0113/check_obligation_tree.py` | 0 | `PASS`: 26 obligations and 49 typed edges; denominator `e509c192...cbd5`; the positive root remains open at M4. |
| `cd Formalizations/Lean && ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 timeout --foreground 30 lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| Isolated trust-zero Lean recipe below | 0 | The exact statement and countermodel elaborated. Lean reported axioms exactly `[propext, Classical.choice, Quot.sound]`; statement output SHA-256 `483a37eb...7e84`; proof output SHA-256 `ee6378a7...2d4c`; `Statement.olean` SHA-256 `94fe8a21...75e0`. |
| Scoped prohibited-declaration scan | 1 | Expected no-match: no prohibited declaration or placeholder occurs in the owned Lean sources; Lean's axiom report contains no `sorryAx`. |
| Lake-manifest package checkout scan | 0 | All 11 package Git worktrees were clean at their recorded revisions. |
| Pinned mathlib analytic-Hodge search | 1 | Expected bounded no-match for the audited analytic Hodge-decomposition declaration/phrase set. |
| `python3 -m json.tool Stage1_Instances/THM-M-0113/proof-recheck-2026-07-15-head-fc1568a2-slot5.json >/dev/null` | 0 | The completed packet is valid JSON. |
| Current-base blocker invariant assertions | 0 | Item/base identity, source hashes, DAG state, negative kernel result, empty accepted receipts, and deliberate self-test absence agree. |
| `git diff --check -- Stage1_Instances/THM-M-0113` | 0 | The scoped diff has no whitespace errors. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The incomplete proof phase emitted no worker-completion packet. |

The isolated replay used the required `lake env` entry point to resolve the
pinned Lean executable and compiled import path, then ran trust-zero Lean only
against copies in `/tmp`:

```bash
set -u
ROOT=$PWD
LEAN_ROOT=$ROOT/Formalizations/Lean
TMP=$(mktemp -d /tmp/thm-m-0113-proof-recheck-slot5.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
cp Stage1_Instances/THM-M-0113/Statement.lean "$TMP/Statement.lean"
cp Stage1_Instances/THM-M-0113/Proof.lean "$TMP/Proof.lean"
cd "$LEAN_ROOT"
PINNED_LEAN_PATH=$(timeout --foreground 600 lake env printenv LEAN_PATH)
PINNED_LEAN=$(timeout --foreground 600 lake env which lean)
cd "$TMP"
LEAN_NUM_THREADS=1 LEAN_PATH="$PINNED_LEAN_PATH" \
  timeout --foreground 600 "$PINNED_LEAN" --trust=0 -t 0 \
  --root="$TMP" -o "$TMP/Statement.olean" "$TMP/Statement.lean" \
  >"$TMP/statement-output.txt" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$PINNED_LEAN_PATH" \
  timeout --foreground 600 "$PINNED_LEAN" --trust=0 -t 0 \
  --root="$TMP" "$TMP/Proof.lean" >"$TMP/proof-output.txt" 2>&1
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
| `Docs/Stage1_Execution_DAG_rev-5.6.json` | `55e3d7ddd258116fe5968cadce4363c87b20c19ed480b40ed3ec94b43a4b63ef` |

This is current-base, durable blocker evidence, not a proof receipt. Because
the assigned positive proof phase is not genuinely self-tested as complete,
`.stage1-worker-selftest.json` is deliberately absent.
