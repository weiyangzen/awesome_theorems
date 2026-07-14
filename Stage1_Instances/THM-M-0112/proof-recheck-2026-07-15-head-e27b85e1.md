# THM-M-0112 proof-phase recheck at current base

Item: `S56-M-0112-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `e27b85e1503047c5e4bd8d5410b6fba5c4dda896`

Base tree: `29c625431b9c241bce6286123205defcbd1e7f7e`

Worker automation clone: `slot13`.

The tracked owned path was clean at preflight. The only pre-existing worktree entry was the
automation-provided untracked `Formalizations/Lean/.lake` symlink to the canonical pinned dependency
cache. This packet is nonrelease evidence.

## Verdict

`blocked`. A placeholder-free positive proof of the exact frozen target cannot exist in this
consistent Lean environment. The repo-local declaration

```text
Stage1Instances.THMM0112.Proof.not_weakTopologicalLefschetzTarget :
  Not (Stage1Instances.THMM0112.WeakTopologicalLefschetzTarget.{0, 0})
```

kernel-checks at trust level zero against a fresh temporary `Statement.olean`. Any positive
universe-polymorphic proof would specialize to universes `(0, 0)` and contradict it.

The countermodel takes `X := PUnit`, discrete `Y := Bool`, and complex dimension two. It makes all
five opaque premise proposition fields `True`, with constant inclusion and constant `piMap`. The
target then demands injectivity in degree zero because `0 < 2 - 1`; the two path components of
`Bool` are distinct, but the constant map identifies them. Lean reports only `propext`,
`Classical.choice`, and `Quot.sound` for the refutation.

This refutes the frozen abstract encoding, not the mathematical Lefschetz hyperplane theorem.
`piMapIsInducedByInclusion : Prop` carries no law relating `piMap` to `inclusion`, and the other
geometric fields are also unconstrained propositions. Adding the missing semantics during this
proof-only phase would change the statement fingerprint. Assuming either conclusion package would
instead be circular.

The pinned `Mathlib.Topology.Homotopy.HomotopyGroup` substrate also has no native
`HomotopyGroup.map` for an inclusion-induced map; its module header still lists path-induced maps as
a TODO. This interface gap precedes the deeper analytification, relative-homotopy, and Morse work.

No positive proof body, proof receipt, graph closure, or accepted debt change was added. The item
stays `[ ]`, lifecycle stays `planned`, and the accepted root vector stays `[H1, M3, R3]`. This
packet proposes `[H5, M5, R3]` only as a diagnosis for independent master review. Audit completion,
theorem completion, validation, release, and master acceptance are not claimed. Because the assigned
phase is incomplete, `.stage1-worker-selftest.json` is deliberately absent.

## Failed Gate And Retry

The first failed gate is exact-target consistency at `M0112-S-INTERFACE`, before the relative-
homotopy and Morse implementation obligations. The frozen graph's root cut set remains
`M0112-B-BELOW` plus `M0112-B-EDGE`, but repair must start by reopening
`S56-M-0112-STATEMENT`, replacing `M0112-S-INTERFACE`, and rechecking `M0112-ROOT`.

Ten unresolved proof recheck attempts now exist while the authoritative DAG still records zero
attempts and no child nodes. Under blueprint section 10.2, the master/scheduler must reconcile the
attempt count and reopen or split the item instead of scheduling another identical proof-only retry.
This worker did not edit the DAG or generated checklist.

Retry only after replacing the opaque stand-ins with native complex-geometric constructions or
noncircular semantic laws tying `piMap` to the actual inclusion-induced homotopy map, accepting a
new exact-statement fingerprint and obligation-registry version, and rerunning the statement,
anchor-audit, obligation-tree, and proof phases.

## Validation

All completed checks used the existing pinned Lake artifacts. No `lake update`, `lake build`,
dependency clone/fetch, network access, or `.lake` mutation was performed. The isolated Lean replay
created objects only under `/tmp` and removed them. A before/after metadata digest of the
dereferenced dependency cache was identical; this is not a content digest.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0112` | 0 | Rank 35; planned lifecycle; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0112/check_statement.py` | 0 | Exact expression elaborated and all four structural mutations were killed. |
| `python3 Stage1_Instances/THM-M-0112/check_anchor_audit.py` | 0 | Three pinned substrate candidate families checked; terminal result is open. |
| `python3 Stage1_Instances/THM-M-0112/check_obligation_tree.py` | 0 | 13 obligations and 31 typed edges passed; root remains open M3. |
| Isolated trust-zero `lake env` Lean recipe below | 0 | Exact statement and refutation elaborated; the negative declaration reports `[propext, Classical.choice, Quot.sound]`. |
| Prohibited-token scan over `Proof.lean` | 1 | Expected no-match exit; no proof escape occurs. |
| Pinned-source terminal/API search | 1 | Expected no-match exit; no exact terminal candidate or named bridge API was found. |
| `git diff --check -- Stage1_Instances/THM-M-0112` plus `git diff --no-index --check /dev/null <new-file>` for each new artifact | 0 / expected 1 | No whitespace diagnostics; exit 1 from each no-index check denotes an added file. |
| `test ! -e .stage1-worker-selftest.json` | 0 | No completion manifest exists for the blocked proof phase. |

Exact isolated Lean recipe, run from the repository root:

```bash
set -euo pipefail
before=$(find -L Formalizations/Lean/.lake -type f \
  -printf '%p\t%s\t%T@\n' | LC_ALL=C sort | sha256sum | cut -d' ' -f1)
tmp=$(mktemp -d /tmp/thm-m-0112-proof-head-e27b85e1.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-0112/Statement.lean "$tmp/Statement.lean"
cp Stage1_Instances/THM-M-0112/Proof.lean "$tmp/Proof.lean"
lean=$(cd Formalizations/Lean && lake env which lean)
lean_path=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
cd "$tmp"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 600 \
  "$lean" --trust=0 -t0 -o Statement.olean Statement.lean
LEAN_NUM_THREADS=1 LEAN_PATH=.:"$lean_path" timeout 600 \
  "$lean" --trust=0 -t0 Proof.lean
cd - >/dev/null
after=$(find -L Formalizations/Lean/.lake -type f \
  -printf '%p\t%s\t%T@\n' | LC_ALL=C sort | sha256sum | cut -d' ' -f1)
test "$before" = "$after"
```

The adjacent JSON binds this blocker to the current base, source hashes, frozen registry, typed
graph, toolchain, dependency revisions, exact commands, and change-impact set. It is not a proof
receipt.
