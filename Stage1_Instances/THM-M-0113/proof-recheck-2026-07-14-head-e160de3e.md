# THM-M-0113 proof-phase recheck at `e160de3e`

Item: `S56-M-0113-PROOF`

Recheck date: `2026-07-14` (`Asia/Shanghai`)

Base revision: `e160de3efab9257518f9bda57545182c2c72e155`

Base tree: `762bcfd6b010e582efebfcac2285095967248cb2`

The start tree was nonrelease-dirty only because of the automation-provided
untracked `Formalizations/Lean/.lake` symlink. The tracked patch was empty
(`e3b0c442...b855`), the NUL-terminated untracked path-list hash was
`e127a939...a25`, and the symlink-target byte hash was `e8714e9e...9826`.
All 11 manifest package Git worktrees were clean at their recorded manifest
revisions.

## Verdict

`blocked`. No legal positive proof body can inhabit the exact frozen target.
The existing placeholder-free declaration

```text
Stage1Instances.THMM0113.not_hodgeDecompositionTarget :
  Not Stage1Instances.THMM0113.HodgeDecompositionTarget.{0, 0, 0, 0}
```

kernel-checks again at trust level zero against a freshly elaborated
`Statement.olean`.

The statement's `HodgeData.isKahler` field is an unconstrained proposition and
does not relate the geometric hypothesis to the independently chosen
`cohomology` family or `hodgePiece` submodules. The countermodel takes the
zero-dimensional compact complex manifold `Fin 0 -> Complex`, sets
`isKahler := True`, interprets every cohomology space as `Complex`, and makes
every Hodge piece bottom. Complex conjugation supplies the required additive,
conjugate-linear, and involutive laws. In degree zero, the target would force
the supremum of bottom submodules to be top, and hence force `1 = 0`.

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
law-bearing hypotheses sufficient to construct the intended objects and
derive the theorem. Then publish a new statement fingerprint and freshly
freeze and accept the statement, anchor audit, obligation registry, and typed
graphs before resuming positive proof work. Alternatively, redirect the item
explicitly to the checked counterexample target.

The earliest statement defect is `M0113-S-DATA`. The checked definitional
expansion at `M0113-S-TRANSPORT` is not refuted. Because this proof worker may
not rewrite the frozen registry, its authoritative remaining root cut set
stays `M0113-A-DR`, `M0113-A-DOL`, `M0113-A-ELL`, `M0113-K-ID`, and
`M0113-C-CHAIN`. This recheck proposes M5 exact-target blocker evidence without
altering that predecessor state. A repaired statement would require a fresh
statement fingerprint and a newly frozen proof architecture before any of
those analytic branches could receive proof credit. The prerequisite
obligation-tree item is still provisional rather than master-accepted.

## Validation

All checks ran in this worker clone using the existing symlink to the canonical
pinned Lake artifacts. No `lake update`, `lake build`, dependency clone/fetch,
network action, or `.lake` mutation was performed. Lean output was confined to
a fresh directory under `/tmp`, removed by a shell trap. The pre-existing
untracked `.lake` symlink makes this nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0113` | 0 | Rank 25; lifecycle `planned`; baseline `L0/rework_required`; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0113/check_obligation_tree.py` | 0 | `PASS`: 26 obligations and 49 typed edges; denominator `e509c192...cbd5`; the prior positive root remains open at M4. |
| `python3 Stage1_Instances/THM-M-0113/check_anchor_audit.py` | 0 | Target boundary, four candidate rows, 12 Lean probes, and pinned mathlib revision agree. |
| Isolated `lake env lean` recipe below | 0 | The exact statement and countermodel elaborated at trust level zero. Lean reported axioms exactly `[propext, Classical.choice, Quot.sound]`; output SHA-256 `539fbb6d2ea328fe07b99cddf2e5b4ee88fda234d3e19983d73f7e244331b1f9`; `Statement.olean` SHA-256 `94fe8a2182ea2776a7f9972ca82cd7c88b50fb2f57091d6527a82eb178d975e0`. |
| Scoped prohibited-declaration scan shown below | 1 | Expected no-match result: no prohibited Lean declaration token occurs in the owned Lean sources. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| Manifest package revision and cleanliness audit | 0 | All 11 package Git worktrees were clean and matched the revisions recorded in the structured blocker packet. |
| `python3 -m json.tool Stage1_Instances/THM-M-0113/proof-recheck-2026-07-14-head-e160de3e.json >/dev/null` | 0 | The current-base blocker packet is valid JSON. |
| Current-base blocker invariant assertions | 0 | Item/base identity, open state, source hashes, negative kernel result, axiom list, empty receipts, and deliberate self-test absence agree. |
| `git diff --check -- Stage1_Instances/THM-M-0113` | 0 | No scoped tracked whitespace error. The new reports were checked separately as untracked files. |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-0113/proof-recheck-2026-07-14-head-e160de3e.json; code=$?; test $code -eq 1` | 0 | The expected new-file difference produced no whitespace diagnostic. |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-0113/proof-recheck-2026-07-14-head-e160de3e.md; code=$?; test $code -eq 1` | 0 | The expected new-file difference produced no whitespace diagnostic. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The incomplete proof phase emitted no worker-completion packet. |

The isolated Lean recipe, run from `Formalizations/Lean`, was:

```bash
set -euo pipefail
tmp=$(mktemp -d /tmp/thm-m-0113-proof-recheck-heade160de3e.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp ../../Stage1_Instances/THM-M-0113/Statement.lean "$tmp/Statement.lean"
cp ../../Stage1_Instances/THM-M-0113/Proof.lean "$tmp/Proof.lean"
base_path=$(timeout 600 lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 timeout 600 lake env lean --trust=0 -t 0 \
  --root="$tmp" -o "$tmp/Statement.olean" "$tmp/Statement.lean" \
  >"$tmp/kernel-output.txt" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base_path" timeout 600 \
  lake env lean --trust=0 -t 0 --root="$tmp" "$tmp/Proof.lean" \
  >>"$tmp/kernel-output.txt" 2>&1
cat "$tmp/kernel-output.txt"
sha256sum "$tmp/kernel-output.txt" "$tmp/Statement.olean"
```

The scoped prohibited-declaration scan was:

```bash
rg -n --pcre2 '^\s*(?:sorry|admit|axiom)(?:\s|$)|sorryAx|^\s*unsafe\s' \
  Stage1_Instances/THM-M-0113 --glob '*.lean'
```

Its exit code was `1`, the expected no-match result. The scan is additional
defense; Lean's printed axiom dependency report is the kernel-derived trust
evidence for the checked countermodel.

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

This is durable blocker evidence, not a proof receipt. Because the assigned
positive proof phase is not genuinely self-tested as complete,
`.stage1-worker-selftest.json` is deliberately absent.
