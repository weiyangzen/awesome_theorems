# THM-M-0112 proof-phase recheck at current base

Item: `S56-M-0112-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `f6e50868cea6cdee270b34c9bb111940d2f16305`

Base tree: `6af4a41a0e2a894d1dfc7f55703e4822b584dd6b`

Worker automation clone: `slot1`.

The tracked owned path was clean at preflight. The only persistent pre-existing worktree entry was
the automation-provided untracked `Formalizations/Lean/.lake` symlink to the canonical pinned
dependency cache. Transient validator sources and isolated Lean outputs were removed. This packet
is nonrelease evidence.

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
`piMapIsInducedByInclusion : Prop` carries no law relating `piMap` to `inclusion`, and the four
geometric fields are also unconstrained propositions. Adding the missing semantics during this
proof-only phase would change the statement fingerprint. Assuming either conclusion package would
instead be circular.

The pinned `Mathlib.Topology.Homotopy.HomotopyGroup` substrate has no native general map for an
inclusion-induced map. No pinned terminal weak Lefschetz theorem, analytification bridge, or
relative-homotopy API was found.

No positive proof body, proof receipt, graph closure, or accepted debt change was added. The item
stays `[ ]`, lifecycle stays `planned`, and the accepted root vector stays `[H1, M3, R3]`. This
packet proposes `[H1, M5, R3]` only as a diagnosis for independent master review: the formal target
is refuted, but the countermodel does not refute the mathematical theorem. Audit completion,
theorem completion, validation, release, and master acceptance are not claimed. Because the
assigned phase is incomplete, `.stage1-worker-selftest.json` is deliberately absent.

## Failed Gate And Retry

The first failed gate is exact-target consistency at `M0112-S-INTERFACE`, before the relative-
homotopy and Morse implementation obligations. The frozen graph's root cut set remains
`M0112-B-BELOW` plus `M0112-B-EDGE`, but repair must start by reopening
`S56-M-0112-STATEMENT`, replacing `M0112-S-INTERFACE`, and rechecking `M0112-ROOT`.

Forty-two prior unresolved proof recheck pairs already existed at preflight while the authoritative
DAG still recorded zero attempts and no child nodes. Under blueprint section 10.2, this packet is a
forty-third repeated blocker record; the master/scheduler must reconcile the attempt count and
reopen or split the item instead of scheduling another identical proof-only retry. This worker did
not edit the DAG or generated checklist.

Retry only after replacing the opaque geometric stand-ins with faithful native complex-geometric
constructions, tying `piMap` to the actual inclusion-induced homotopy map, accepting a new exact-
statement fingerprint and obligation-registry version, and rerunning statement, anchor-audit,
obligation-tree, and proof phases.

## Validation

All completed checks used the existing pinned Lake artifacts. No `lake update`, `lake build`,
dependency clone/fetch, network access, or `.lake` mutation was performed. The isolated Lean replay
created objects only under `/tmp` and removed them. A before/after metadata digest of the
dereferenced dependency cache was identical; this is not a content digest.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0112` | 0 | Rank 35; planned lifecycle; theorem incomplete. |
| `lake env lean --version` from `Formalizations/Lean` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`. |
| `python3 Stage1_Instances/THM-M-0112/check_statement.py` | 0 | Exact expression elaborated; all four structural mutations were killed; expression SHA-256 is `1daee7f6...eb654`. |
| `python3 Stage1_Instances/THM-M-0112/check_anchor_audit.py` | 0 | Three pinned substrate candidate families checked; terminal result is open. |
| `python3 Stage1_Instances/THM-M-0112/check_obligation_tree.py` | 0 | 13 obligations and 31 typed edges passed; root remains open M3. |
| Isolated trust-zero `lake env` Lean replay from `/tmp` | 0 | Exact statement and refutation elaborated; the negative declaration reports `[propext, Classical.choice, Quot.sound]`; dependency-cache metadata stayed unchanged. |
| Prohibited-token scan over `Proof.lean` | 1 | Expected no-match exit; no proof escape occurs. |
| Pinned-source terminal/API search | 1 | Expected no-match exit; no exact terminal candidate or named missing bridge API was found. |
| `test ! -e .stage1-worker-selftest.json` | 0 | No completion self-test manifest exists for the blocked proof phase. |
| `python3 -m json.tool` on the adjacent JSON | 0 | The blocker packet is valid JSON. |
| Scoped packet consistency and source-hygiene checks | 0 | Base/tree and source hashes match; completion claims are false; 43 record pairs exist; self-test is absent; no whitespace or source-hygiene diagnostics were emitted. |

Exact successful isolated Lean recipe, run from the repository root:

```bash
set -euo pipefail
cache=$(readlink -f Formalizations/Lean/.lake)
cache_sig() {
  find "$cache" -path "$cache/.lake" -prune -o -type f \
    -printf '%P\t%s\t%T@\n' 2>/dev/null | LC_ALL=C sort | sha256sum | cut -d' ' -f1
}
before=$(cache_sig)
tmp=$(mktemp -d /tmp/thm-m-0112-proof-head-f6e50868-slot1.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-0112/Statement.lean "$tmp/Statement.lean"
cp Stage1_Instances/THM-M-0112/Proof.lean "$tmp/Proof.lean"
lean=$(cd Formalizations/Lean && lake env which lean)
lean_path=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
(
  cd "$tmp"
  LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 600 \
    "$lean" --trust=0 -t0 -o Statement.olean Statement.lean
  LEAN_NUM_THREADS=1 LEAN_PATH=.:"$lean_path" timeout 600 \
    "$lean" --trust=0 -t0 -o Proof.olean Proof.lean
)
after=$(cache_sig)
test "$before" = "$after"
```

The temporary object hashes were
`f869a1057c46e20107dd3464966d1b86c9d534d61224242ff1fc9576dffb2a77` for
`Statement.olean` and `5d11e1de5da347e936936bf2c5b4e965306a7639f98ee54404d58dfcd0173b82`
for `Proof.olean`. The dependency-cache metadata digest was
`9542907fada35628f062eb0a68beebfe2036ea2d57ed5803b937bdb48b6e7d78` before and after.

The adjacent JSON binds this blocker to the current base, source hashes, frozen registry, typed
graph, toolchain, dependency revisions, exact commands, and change-impact set. It is not a proof
receipt.
