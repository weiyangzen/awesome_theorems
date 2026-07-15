# THM-M-0113 proof-phase recheck at `a8915398`

Item: `S56-M-0113-PROOF`

Recheck date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `a891539807529404c603663972e3ba530ae004ba`

Base tree: `0ef8cb5412fcd35d2cebb1be999cea173ed761eb`

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
contained 24 structured proof rechecks at worker start. That count is evidence
of repeated dispatch, not an authoritative tick ledger, but it is far beyond
the standard's five-unresolved-tick split threshold. Another unchanged-target
proof dispatch cannot create positive proof progress; integration must repair
or explicitly redirect the statement chain and reconcile the task counter.

## Validation

The target checks used the existing canonical pinned Lake artifacts read only.
No `lake update`, `lake build`, dependency clone/fetch, network action, or
intentional `.lake` write was performed. Lean output was confined to a fresh
directory under `/tmp` and removed after validation. The pre-existing untracked
`.lake` symlink makes this nonrelease evidence.

The prescribed project-root Lake preflight could not complete: the shared
`flt-regular` checkout has `HEAD` at `refs/heads/.invalid`. The manifest-pinned
commit object `56161b6e...1a27` is present, but this worker did not fetch,
repair, or check it out. The narrow kernel check invoked `lake env lean` from
the fresh `/tmp` validation directory, with `ELAN_TOOLCHAIN` selecting the
pinned toolchain and `LEAN_PATH` containing only pre-existing compiled Lake
artifacts.

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
| Lake-manifest package checkout scan | 0 | Ten packages are clean at their exact pinned HEAD; `flt-regular` has the pinned object and clean tracked status but unresolved `HEAD`. |
| `git -C .../mathlib rev-parse HEAD` | 0 | Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| `git -C .../flt-regular cat-file -e 56161b6e...1a27^{commit}` | 0 | The manifest-pinned commit object is present despite the invalid checkout `HEAD`. |
| `python3 -m json.tool` and scoped `jq -e` invariant assertions | 0 | The packet parses and its item/base identity, blocked state, hashes, empty receipts, and deliberate self-test absence agree. |
| `git diff --check` and new-file whitespace checks | 0 | No whitespace diagnostics. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The incomplete proof phase emitted no worker-completion packet. |

The isolated Lean recipe, run from the repository root, was:

```bash
set -u
tmp=$(mktemp -d /tmp/thm-m-0113-proof-recheck-a8915398-slot12.XXXXXX)
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
| `Docs/Stage1_Blueprint_rev-5.6.md` | `684069fbbf80dac0a7df63fa110a6814533ee9e87e30e5f3142cd0c8efeda22f` |
| `Docs/Stage1_Targets_rev-5.6.json` | `02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c` |
| `Docs/Stage1_Execution_DAG_rev-5.6.json` | `17e57a4945d1ad2c2e012315b923ac705e459d1950961297174513601efcc56e` |

This is current-base, durable blocker evidence, not a proof receipt. Because
the assigned positive proof phase is not genuinely self-tested as complete,
`.stage1-worker-selftest.json` is deliberately absent.
