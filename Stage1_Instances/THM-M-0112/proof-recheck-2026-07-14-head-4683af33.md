# THM-M-0112 proof-phase recheck at current base

Item: `S56-M-0112-PROOF`

Recheck date: 2026-07-14 (Asia/Shanghai)

Base revision: `4683af33601abf1185b47caafb86ccd3ddc30158`

Base tree: `9b49ee18fec214315592ea125d7049e4ea668740`

The tracked owned path was clean at preflight. The only pre-existing worktree entry was the
automation-provided untracked `Formalizations/Lean/.lake` symlink to the canonical pinned dependency
cache; its link target and classification are recorded in the adjacent JSON. This makes the run
nonrelease evidence.

## Verdict

`blocked`. The exact frozen Lean target has no consistent positive proof body. The existing
placeholder-free declaration

```text
Stage1Instances.THMM0112.Proof.not_weakTopologicalLefschetzTarget :
  Not (Stage1Instances.THMM0112.WeakTopologicalLefschetzTarget.{0, 0})
```

kernel-checks at trust level zero against a fresh temporary `Statement.olean`. Any
universe-polymorphic positive proof would specialize to universes `(0, 0)` and contradict this
declaration.

The countermodel takes `X := PUnit`, discrete `Y := Bool`, and complex dimension two. It makes the
five opaque geometric proposition fields `True`, with constant inclusion and constant `piMap`. The
target then demands injectivity in degree zero because `0 < 2 - 1`; however, the two path components
of `Bool` are distinct and the constant map identifies them. Lean reports only `propext`,
`Classical.choice`, and `Quot.sound` for this refutation.

This refutes the frozen abstract encoding, not the mathematical Lefschetz hyperplane theorem.
`piMapIsInducedByInclusion : Prop` provides no law relating `piMap` to `inclusion`, and the other
geometric fields are likewise unconstrained propositions. Adding the required semantics in this
proof phase would change the frozen target; assuming either conclusion package would be circular.

No positive proof body, proof receipt, or frozen-obligation closure was added. The proof item remains
`[ ]`, lifecycle remains `planned`, and the accepted root vector remains `[H1, M3, R3]`; `M5` is only
the proposed machine diagnosis for the refutable encoding. Audit completion, theorem completion,
validation, release, and master acceptance are not claimed. `.stage1-worker-selftest.json` is
deliberately absent because the assigned proof phase is not complete.

## Failed Gate And Retry

The first failed gate is exact-target consistency at `M0112-S-INTERFACE`, before the later
relative-homotopy and Morse obligations. The remaining root cut set is
`S56-M-0112-STATEMENT`, `M0112-S-INTERFACE`, and `M0112-ROOT`.

Retry only after reopening the statement phase, replacing the opaque stand-ins with native
complex-geometric constructions or noncircular semantic laws tying `piMap` to the actual
inclusion-induced homotopy map, accepting a new exact-statement fingerprint and obligation-registry
version, and rerunning the statement, anchor-audit, obligation-tree, and proof phases.

## Validation

All checks ran in this worker clone against the existing pinned Lake artifacts. The automation-
provided untracked `Formalizations/Lean/.lake` symlink was reused read-only. No `lake update`,
`lake build`, dependency clone/fetch, network access, or `.lake` mutation was performed. Temporary
Lean objects were created under `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0112` | 0 | Rank 35; planned lifecycle; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0112/check_statement.py` | 0 | Canonical expression SHA-256 `1daee7f6...654`; all four mutations were distinguished. |
| `python3 Stage1_Instances/THM-M-0112/check_anchor_audit.py` | 0 | Three pinned substrate candidate families checked; no terminal candidate exists. |
| `python3 Stage1_Instances/THM-M-0112/check_obligation_tree.py` | 0 | 13 obligations and 31 typed edges passed; denominator `5d119562...7df7f4`; the predecessor graph still records the root as open M3. |
| Isolated trust-zero `lake env lean` recipe below | 0 | Exact statement and refutation elaborated; the negative declaration has the exact type above and reports `[propext, Classical.choice, Quot.sound]`. |
| `rg -n '\\b(sorry\|admit\|sorryAx\|native_decide)\\b\|^[[:space:]]*(axiom\|unsafe\|external)[[:space:]]' Stage1_Instances/THM-M-0112/Proof.lean` | 1 | Expected no-match exit; no prohibited proof escape occurs. |
| `python3 -m json.tool Stage1_Instances/THM-M-0112/proof-recheck-2026-07-14-head-4683af33.json` | 0 | Current-base structured blocker record is valid JSON. |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-0112/proof-recheck-2026-07-14-head-4683af33.json` and the same command for the adjacent Markdown | 1 each | Expected added-file status; neither command reported a whitespace error. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The incomplete proof phase emitted no completion manifest. |

Exact isolated Lean recipe, run from the repository root:

```bash
set -euo pipefail
tmp=$(mktemp -d /tmp/thm-m-0112-proof-recheck.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-0112/Statement.lean "$tmp/Statement.lean"
cp Stage1_Instances/THM-M-0112/Proof.lean "$tmp/Proof.lean"
lean=$(cd Formalizations/Lean && lake env which lean)
lean_path=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
cd "$tmp"
LEAN_PATH="$lean_path" "$lean" --trust=0 -t0 -o Statement.olean Statement.lean
LEAN_PATH=.:"$lean_path" "$lean" --trust=0 -t0 Proof.lean
```

The bound source and environment hashes are recorded in the adjacent JSON artifact. This is fresh,
nonrelease blocker evidence, not a proof receipt.
