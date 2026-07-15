# THM-M-0113 proof-phase blocker at `40af576c`

Item: `S56-M-0113-PROOF`

Recheck date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `40af576c997f512b8937d4c32a8b459dbb3c18a1`

Base tree: `9cf2d30df293b11ef79f6e4d662549b26a7bdf95`

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
the mutation-failure evidence, publish a new statement fingerprint, and
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

There were already 50 tracked structured proof rechecks at worker start while
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
| `python3 Stage1_Instances/THM-M-0113/check_obligation_tree.py` | 0 | `PASS`: 26 obligations and 49 typed edges; denominator `e509c192...cbd5`; the positive root remains M4 with five analytic cut-set leaves. |
| Isolated trust-zero Lean recipe below | 0 | Statement and countermodel elaborated. Axioms were exactly `[propext, Classical.choice, Quot.sound]`; combined output SHA-256 `539fbb6d...331b1f9`; `Statement.olean` SHA-256 `94fe8a21...d975e0`. |
| Scoped prohibited-declaration scan | 1 | Expected no-match: no `sorry`, `admit`, `sorryAx`, `native_decide`, bodyless declaration, unsafe declaration, `implemented_by`, or `extern` occurs in the owned Lean sources. |
| `cd Formalizations/Lean && ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 timeout --foreground 30 lake env lean --version && timeout --foreground 30 lake --version` | 0 | Lean 4.29.0 at commit `98dc76e...`; Lake `5.0.0-src+98dc76e`. |
| Lake-manifest package status scan | 0 | All 11 package revisions matched the manifest and all tracked worktrees were clean; mathlib was `8a178386...a95`. |
| Pinned mathlib bounded Hodge search | 1 | Expected no-match for the audited analytic Hodge-decomposition declaration and phrase set. |
| `python3 -m json.tool Stage1_Instances/THM-M-0113/proof-recheck-2026-07-15-head-40af576c-slot2.json >/dev/null` | 0 | The blocker packet is valid JSON. |
| Current-base blocker invariant assertions | 0 | Item/base identity, hashes, open state, negative kernel result, empty receipts, and deliberate self-test absence agree. |
| Scoped tracked and new-file whitespace checks | 0 | Both owned-path additions have no whitespace errors. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The incomplete proof phase emitted no worker-completion packet. |

The isolated replay used the required `lake env` entry point to resolve the
pinned Lean executable and compiled import path, then ran trust-zero Lean only
against copies in `/tmp`:

```bash
set -u
ROOT=$PWD
LEAN_ROOT=$ROOT/Formalizations/Lean
TMP=$(mktemp -d /tmp/thm-m-0113-proof-recheck-slot2.XXXXXX)
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
The package scan parsed `Formalizations/Lean/lake-manifest.json` and checked
the exact revision plus tracked cleanliness of every listed checkout. The
bounded mathlib search read only revision `8a178386...a95` and returned the
expected no-match.

The checked input SHA-256 values are:

| Input | SHA-256 |
|---|---|
| `Statement.lean` | `73010040e7a16c02d00bfa95db270e2370440f433e8c3519e5e2ab429cd236dd` |
| `Proof.lean` | `b05f2ef3eef236e026930097803c614d53eeaba65d5fa936b0293a7c4879ec6f` |
| `ObligationTree.lean` | `c9fe3593539b1a3d221496ad45c3b5a9cfcd1355b3875f7b42d4012337273a95` |
| `statement.json` | `38fed31b8341e67729ae2f638edb595361a099a7b7ecbaa0f1e336d0b342ac22` |
| `statement-receipt.json` | `934e53f36ca1e94d2e2911467ca1e9787fda6717e5be54da52e125605f22aae0` |
| `obligation-registry.json` | `c8f592dd2961e08782a241355e0eaf2f1d6841b8e66b325bab5d07c936847f2d` |
| `typed-graphs.json` | `31b91ed2b0c42702819148e6ab02e222e06f801bd0e1cc9e81788d26f2606e34` |
| `anchor-audit.json` | `96d93459b27f3a95357e041e0a9cf589d849ef5066894551e646b5dbb5027795` |
| `Formalizations/Lean/lake-manifest.json` | `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81` |
| `Formalizations/Lean/lean-toolchain` | `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2` |
| `Docs/Stage1_Execution_DAG_rev-5.6.json` | `bf98316a3e75bfade3a1449efae47007b405bb6645765847e89c89d660f5356f` |

This is current-base durable blocker evidence, not a proof receipt. Because
the assigned positive proof phase is not genuinely self-tested as complete,
`.stage1-worker-selftest.json` is deliberately absent.
