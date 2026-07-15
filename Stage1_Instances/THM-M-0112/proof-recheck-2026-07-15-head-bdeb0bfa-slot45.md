# THM-M-0112 proof-phase recheck at current base

Item: `S56-M-0112-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `bdeb0bfae66ccfe8b672776c61bc4c74a25bef3d`

Base tree: `440ac842583ec6b7aa7be989ba908e8b745978b9`

Worker automation clone: `slot45`.

The tracked owned path was clean at preflight. The only persistent pre-existing worktree entry was
the automation-provided untracked `Formalizations/Lean/.lake` symlink to the canonical pinned
dependency cache. Validator temporaries and isolated Lean object files were removed. This is
nonrelease evidence.

## Verdict

`blocked`. No placeholder-free positive proof of the exact frozen target can exist in this
consistent Lean environment. The repo-local declaration

```text
Stage1Instances.THMM0112.Proof.not_weakTopologicalLefschetzTarget :
  Not (Stage1Instances.THMM0112.WeakTopologicalLefschetzTarget.{0, 0})
```

kernel-checks at trust level zero against a fresh temporary `Statement.olean`. Any positive
universe-polymorphic proof would specialize to universes `(0, 0)` and contradict this declaration.

The countermodel takes `X := PUnit`, discrete `Y := Bool`, and complex dimension two. It makes all
five opaque premise proposition fields `True`, with constant inclusion and constant `piMap`. The
target then demands injectivity in degree zero because `0 < 2 - 1`; the two path components of
`Bool` are distinct, but the constant map identifies them. Lean reports only `propext`,
`Classical.choice`, and `Quot.sound` for the refutation.

This refutes the frozen abstract encoding, not the mathematical Lefschetz hyperplane theorem.
`piMapIsInducedByInclusion : Prop` supplies no law relating `piMap` to `inclusion`, and the four
geometric fields are likewise unconstrained propositions. Repairing those semantics during this
proof-only phase would change the frozen statement fingerprint. Assuming either conclusion package
would instead be circular.

No positive proof body, proof receipt, graph closure, or accepted debt change was added. The item
stays `[ ]`, lifecycle stays `planned`, and the accepted root vector stays `[H1, M3, R3]`. This
packet proposes `[H1, M5, R3]` only as a diagnosis for independent master review. Audit completion,
theorem completion, validation, release, and master acceptance are not claimed. Because the
assigned phase is incomplete, `.stage1-worker-selftest.json` is deliberately absent.

## Failed Gate And Retry

The first failed gate is exact-target consistency at `M0112-S-INTERFACE`, before the relative-
homotopy and Morse implementation obligations. The frozen graph's recorded root cut set remains
`M0112-B-BELOW` plus `M0112-B-EDGE`, but positive execution must first reopen
`S56-M-0112-STATEMENT`, replace `M0112-S-INTERFACE`, accept a corrected target fingerprint and
registry version, and rerun statement, anchor-audit, obligation-tree, and proof phases.

Forty-nine prior matched proof-recheck packet pairs already existed at preflight while the
authoritative DAG still recorded `attempts: 0` and no children. Under blueprint section 10.2, this
is another repeated unresolved tick. The master/scheduler must reconcile the attempts and split or
redirect the oversized item; this proof worker did not edit authoritative state.

## Validation Evidence

All validation reused the existing pinned toolchain and dependency artifacts. No `lake update`,
`lake build`, dependency clone/fetch, or network operation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0112` | 0 | Rank 35; lifecycle `planned`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0112/check_statement.py` | 0 | Exact expression elaborated; four mutations killed; expression SHA-256 `1daee7f6...eb654`. |
| `python3 Stage1_Instances/THM-M-0112/check_anchor_audit.py` | 0 | Three pinned substrate families checked; zero external terminal candidates; terminal remains open. |
| `python3 Stage1_Instances/THM-M-0112/check_obligation_tree.py` | 0 | 13 obligations and 31 typed edges passed; denominator `5d119562...7df7f4`; root remains M3. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`. |
| Isolated `/tmp` trust-zero Lean replay below | 0 | Exact target and negation elaborated; only `propext`, `Classical.choice`, and `Quot.sound`; dependency-cache metadata unchanged. |
| Prohibited-token scan over `Proof.lean` | 1 | Expected no-match exit; no proof escape found. |
| Pinned-source terminal/API search | 1 | Expected no-match exit; no terminal theorem or named missing bridge API found. |
| `test ! -e .stage1-worker-selftest.json` | 0 | No false completion self-test exists. |
| `python3 -m json.tool` on the adjacent JSON | 0 | The current-base blocker packet is valid JSON. |
| Direct and Git whitespace checks over both new files | 0 | No whitespace diagnostic. |
| Inline packet-consistency check | 0 | Current HEAD/tree and eight source hashes match; fail-closed claims hold; 50 packet pairs; self-test absent. |

Exact successful isolated Lean recipe, run from the repository root:

```bash
set -euo pipefail
cache=$(readlink -f Formalizations/Lean/.lake)
cache_sig() {
  find "$cache" -path "$cache/.lake" -prune -o -type f \
    -printf '%P\t%s\t%T@\n' 2>/dev/null | LC_ALL=C sort | sha256sum | cut -d' ' -f1
}
before=$(cache_sig)
tmp=$(mktemp -d /tmp/thm-m-0112-proof-head-bdeb0bfa-slot45.XXXXXX)
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
  sha256sum Statement.olean Proof.olean
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
