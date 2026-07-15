# THM-M-0112 proof-phase recheck at current base

Item: `S56-M-0112-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `1f996d0ba7939acd26bf231689a91751d276bb8c`

Base tree: `ae0448c57d503bd89b62f8f4b753e689abe77e83`

Worker automation clone: `slot5`.

At preflight the tracked owned path was clean. The sole pre-existing worktree entry was the
automation-provided untracked `Formalizations/Lean/.lake` symlink to the canonical dependency
cache. The cache's `flt-regular` checkout has `HEAD` set to the invalid ref
`refs/heads/.invalid`; consequently the top-level `lake env lean` entry point and both Lean-backed
target validators stop before Lean starts. This worker did not repair, update, build, clone, or
manually fetch `.lake`. The attempted Lake entry points may nevertheless run Lake's own dependency
resolution before failing, and the shared canonical cache was concurrently used by other workers;
its `FETCH_HEAD` metadata was observed changing. Therefore this run makes no cache-nonmutation or
immutable-cache claim. The narrow trust-zero replay below used `lake env lean` from the already
pinned mathlib checkout, existing compiled package paths, and temporary outputs under `/tmp`, which
were removed. This packet is blocker evidence, not release evidence.

## Verdict

`blocked`. A placeholder-free positive proof of the exact frozen target cannot exist in this
consistent Lean environment. The existing repo-local declaration

```text
Stage1Instances.THMM0112.Proof.not_weakTopologicalLefschetzTarget :
  Not (Stage1Instances.THMM0112.WeakTopologicalLefschetzTarget.{0, 0})
```

elaborates under `--trust=0` against a freshly generated temporary `Statement.olean`. Any positive
universe-polymorphic proof would specialize to universes `(0, 0)` and contradict this declaration.

The countermodel takes `X := PUnit`, discrete `Y := Bool`, and complex dimension two. It makes all
five opaque premise proposition fields `True`, with constant inclusion and constant `piMap`. The
target then requires injectivity in degree zero because `0 < 2 - 1`; the two path components of
`Bool` are distinct, but the constant map identifies them. Lean reports only `propext`,
`Classical.choice`, and `Quot.sound` for the refutation.

This refutes the frozen abstract encoding, not the mathematical Lefschetz hyperplane theorem.
`piMapIsInducedByInclusion : Prop` supplies no law connecting `piMap` to `inclusion`, and the four
geometric fields are also unconstrained propositions. Adding their missing semantics in this
proof-only phase would change the statement fingerprint. Assuming either desired conclusion package
would instead be circular.

The pinned source search found no terminal weak Lefschetz theorem, analytification bridge, or
relative-homotopy API. No positive proof body, proof receipt, graph closure, or accepted debt change
was added. The item remains `[ ]`, lifecycle remains `planned`, and the accepted root vector remains
`[H1, M3, R3]`. This packet proposes `[H5, M5, R3]` only as a diagnosis for independent master
review. Audit completion, theorem completion, validation, release, and master acceptance are not
claimed. Because the assigned phase is incomplete, `.stage1-worker-selftest.json` is deliberately
absent.

## Failed Gate And Retry

The first failed gate is `S56-5.1-EXACT-TARGET-CONSISTENCY / M0112-S-INTERFACE`, before the
relative-homotopy and Morse implementation obligations. The frozen graph's root cut set remains
`M0112-B-BELOW` plus `M0112-B-EDGE`, but repair must start by reopening
`S56-M-0112-STATEMENT`, replacing `M0112-S-INTERFACE`, and rechecking `M0112-ROOT`.

Twenty-seven prior unresolved proof recheck pairs already existed at preflight, while the
authoritative DAG still records zero proof attempts and no child nodes. Under blueprint section
10.2 this is the twenty-eighth repeated blocker record; the master/scheduler must reconcile the
attempt count and reopen or split the item rather than schedule another identical proof-only retry.
This worker did not edit the DAG or generated checklist.

Retry only after replacing the opaque geometric stand-ins with faithful complex-geometric
constructions, tying `piMap` to the actual inclusion-induced homotopy map, accepting a new exact-
statement fingerprint and obligation-registry version, and rerunning the statement, anchor-audit,
obligation-tree, and proof phases. Independently, restore the manifest-pinned `flt-regular` checkout
artifact so the top-level `lake env lean` entry point can run offline without dependency mutation.

## Validation

No `lake update`, `lake build`, explicit dependency clone/fetch, network command, or `.lake` repair
was requested or run. The failing Lake entry points may have attempted automatic dependency
resolution, and the shared cache had concurrent external activity, so this packet cannot attest
that the cache stayed unchanged. The narrow target replay passed through `lake env lean`; it does
not repair the broken top-level dependency checkout and is not presented as release or full-project
validation.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0112` | 0 | Rank 35; planned lifecycle; theorem incomplete. |
| `lake env lean --version` from `Formalizations/Lean` | 1 | Lake stopped because `.lake/packages/flt-regular` could not resolve `HEAD`; Lean was not invoked. |
| `python3 Stage1_Instances/THM-M-0112/check_statement.py` | 1 | Its internal `lake env lean` hit the same invalid `flt-regular` `HEAD` before elaboration. |
| `python3 Stage1_Instances/THM-M-0112/check_anchor_audit.py` | 1 | Its internal `lake env lean` hit the same invalid `flt-regular` `HEAD` before elaboration. |
| `python3 Stage1_Instances/THM-M-0112/check_obligation_tree.py` | 0 | 13 obligations and 31 typed edges passed; root remains open M3. |
| Isolated `/tmp` trust-zero replay via `lake env lean` from the pinned mathlib checkout | 0 | The exact statement and its negation elaborated; the negative declaration reports `[propext, Classical.choice, Quot.sound]`. |
| Prohibited-token scan over `Proof.lean` | 1 | Expected no-match exit; no proof escape occurs. |
| Pinned-source terminal/API search | 1 | Expected no-match exit; no exact terminal candidate or named bridge API was found. |
| `test ! -e .stage1-worker-selftest.json` | 0 | No completion self-test manifest exists for the blocked proof phase. |

Exact narrow diagnostic recipe, run from the repository root:

```bash
set -euo pipefail
root=$PWD
tmp=$(mktemp -d /tmp/thm-m-0112-proof-head-1f996d0b-slot5.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-0112/Statement.lean "$tmp/Statement.lean"
cp Stage1_Instances/THM-M-0112/Proof.lean "$tmp/Proof.lean"
mathlib=$(readlink -f Formalizations/Lean/.lake/packages/mathlib)
lean_path=$(find -L "$root/Formalizations/Lean/.lake/packages" -type d \
  -path '*/.lake/build/lib/lean' -print | LC_ALL=C sort | paste -sd: -)
cd "$mathlib"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 600 lake env lean \
  -R "$tmp" --trust=0 -t0 -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 600 lake env lean \
  -R "$tmp" --trust=0 -t0 -o "$tmp/Proof.olean" "$tmp/Proof.lean"
```

The temporary statement object had SHA-256
`f869a1057c46e20107dd3464966d1b86c9d534d61224242ff1fc9576dffb2a77`; the temporary proof object
had SHA-256 `5d11e1de5da347e936936bf2c5b4e965306a7639f98ee54404d58dfcd0173b82`.
The adjacent JSON binds the blocker to the current base, source hashes, frozen registry, typed
graph, manifest pins, exact commands, and change-impact set. It is not a proof receipt.
