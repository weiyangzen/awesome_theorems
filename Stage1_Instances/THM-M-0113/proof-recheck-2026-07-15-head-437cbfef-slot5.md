# THM-M-0113 proof-phase recheck at `437cbfef`

Item: `S56-M-0113-PROOF`

Recheck date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `437cbfefc5829160dcb65d52dbe3c5458b187f3b`

Base tree: `849d1bfa7781d20a7428a64349372f2f43d94d2b`

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
publish a new statement fingerprint, complete the required mutation-failure
evidence, and freshly freeze and accept the statement, anchor audit,
obligation registry, and typed graphs before resuming positive proof work.
Alternatively, redirect the item explicitly to the checked counterexample
target. Do not reschedule the unchanged positive root task.

The frozen graph's prior analytic cut set is `M0113-A-DR`, `M0113-A-DOL`,
`M0113-A-ELL`, `M0113-K-ID`, and `M0113-C-CHAIN`; the newly exposed statement
defect `M0113-S-DATA` blocks entry to that proof architecture. The prior
registry projection remains open at M4. This recheck proposes M5 only for the
invalid backend target while retaining H4 for the intended mathematical
theorem; it does not alter predecessor state. The prerequisite obligation-tree
item remains provisional rather than master-accepted.

The statement mutation gate also remains failed: the existing fixtures do not
establish all required non-equivalence failures, and
`MutationRemovedCompactness` still assumes `[CompactSpace M]`. Moreover, 51
tracked JSON/Markdown blocker pairs already predate this run while the
authoritative DAG still records zero attempts and no children. Those files are
evidence of repeated scheduling, not an authoritative execution-tick ledger,
but they reinforce that repair or explicit redirection is required rather than
another unchanged proof attempt.

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
| `python3 Stage1_Instances/THM-M-0113/check_obligation_tree.py` | 0 | `PASS`: 26 obligations and 49 typed edges; denominator `e509c192...cbd5`; the prior positive root remains open at M4. |
| Isolated `lake env` Lean recipe below | 0 | The exact statement and countermodel elaborated at trust level zero. Lean reported axioms exactly `[propext, Classical.choice, Quot.sound]`; combined output SHA-256 `539fbb6d2ea328fe07b99cddf2e5b4ee88fda234d3e19983d73f7e244331b1f9`; `Statement.olean` SHA-256 `94fe8a2182ea2776a7f9972ca82cd7c88b50fb2f57091d6527a82eb178d975e0`. |
| Scoped prohibited-declaration scan | 1 | Expected no-match: no `sorry`, `admit`, `sorryAx`, `native_decide`, bodyless declaration, unsafe declaration, `implemented_by`, or `extern` occurs in the owned Lean sources. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| Package checkout status scan | 0 | All 11 Lake-manifest package Git worktrees were clean at their recorded revisions. |
| `python3 -m json.tool` on the structured packet | 0 | The current-base blocker packet is valid JSON. |
| Current-base blocker invariant assertions | 0 | Item/base identity, input hashes, negative kernel result, open state, empty receipts, and deliberate self-test absence agree. |
| Scoped `git diff --check` and added-file checks | 0 | No whitespace error occurs in either owned-path addition. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The incomplete proof phase emitted no worker-completion packet. |

The isolated Lean recipe, run from `Formalizations/Lean`, was:

```bash
set -euo pipefail
tmp=$(mktemp -d /tmp/thm-m-0113-proof-recheck-head437cbfef.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp ../../Stage1_Instances/THM-M-0113/Statement.lean "$tmp/Statement.lean"
cp ../../Stage1_Instances/THM-M-0113/Proof.lean "$tmp/Proof.lean"
base_path=$(timeout --foreground 600 lake env printenv LEAN_PATH)
lean_bin=$(timeout --foreground 600 lake env which lean)
LEAN_NUM_THREADS=1 LEAN_PATH="$base_path" timeout --foreground 600 \
  "$lean_bin" --trust=0 -t 0 --root="$tmp" \
  -o "$tmp/Statement.olean" "$tmp/Statement.lean" \
  >"$tmp/kernel-output.txt" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base_path" timeout --foreground 600 \
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

Its exit code was `1`, the expected no-match result. Lean's printed axiom
dependency report is the kernel-derived trust evidence for the countermodel.

The packet checks, run from the repository root, were:

```bash
python3 -m json.tool \
  Stage1_Instances/THM-M-0113/proof-recheck-2026-07-15-head-437cbfef-slot5.json \
  >/dev/null
git diff --check -- Stage1_Instances/THM-M-0113
git diff --no-index --check /dev/null \
  Stage1_Instances/THM-M-0113/proof-recheck-2026-07-15-head-437cbfef-slot5.json \
  >/dev/null
test "$?" -eq 1
git diff --no-index --check /dev/null \
  Stage1_Instances/THM-M-0113/proof-recheck-2026-07-15-head-437cbfef-slot5.md \
  >/dev/null
test "$?" -eq 1
test ! -e .stage1-worker-selftest.json
```

The no-index commands return `1` because each path is a new file; `--check`
reported no whitespace diagnostics. A Python invariant check parsed the JSON
and asserted the item, base revision/tree, exact source hashes, countermodel
type, trust-zero result, expected no-match placeholder scan, unchanged graph,
empty receipt lists, open completion booleans, and self-test absence.

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
| `Docs/Stage1_Execution_DAG_rev-5.6.json` | `e193ecc1cb585a15d093cd01c944884419e413dc3eb64bc4e9fcd35a2a1179e8` |

This is durable blocker evidence, not a proof receipt. Because the assigned
positive proof phase is not genuinely self-tested as complete,
`.stage1-worker-selftest.json` is deliberately absent.
