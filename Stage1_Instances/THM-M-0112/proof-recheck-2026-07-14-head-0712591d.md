# THM-M-0112 proof-phase recheck at current base

Item: `S56-M-0112-PROOF`

Recheck date: 2026-07-14 (Asia/Shanghai)

Base revision: `0712591ddaea6a40a0dc6482670e6129e727f5df`

Base tree: `03a643bf6bd4f35f0d1d6c036afab8b41aa88401`

The tracked owned path was clean at preflight. The only pre-existing worktree entry was the
automation-provided untracked `Formalizations/Lean/.lake` symlink to the canonical pinned dependency
cache. Its exact target and classification are recorded in the adjacent JSON. This is nonrelease
evidence.

## Verdict

`blocked`. A placeholder-free positive proof of the exact frozen target cannot exist in this
consistent Lean environment. The existing declaration

```text
Stage1Instances.THMM0112.Proof.not_weakTopologicalLefschetzTarget :
  Not (Stage1Instances.THMM0112.WeakTopologicalLefschetzTarget.{0, 0})
```

kernel-checks at trust level zero against a fresh temporary `Statement.olean`. A positive
universe-polymorphic proof would specialize to universes `(0, 0)` and contradict it.

The checked countermodel takes `X := PUnit`, discrete `Y := Bool`, and complex dimension two. It
makes all five opaque premise proposition fields `True`, with constant inclusion and constant
`piMap`. The target then demands injectivity in degree zero because `0 < 2 - 1`; the two path
components of `Bool` are distinct, but the constant map identifies them. Lean reports only
`propext`, `Classical.choice`, and `Quot.sound` for the refutation.

This refutes the frozen abstract encoding, not the mathematical Lefschetz hyperplane theorem.
`piMapIsInducedByInclusion : Prop` carries no law relating `piMap` to `inclusion`, and the other
geometric fields are also unconstrained propositions. Adding their missing semantics during this
proof-only phase would change the accepted statement fingerprint. Assuming either conclusion
package would instead be circular.

No positive proof body, proof receipt, or frozen-obligation closure was added. The proof item stays
`[ ]`, lifecycle stays `planned`, and the predecessor root vector stays `[H1, M3, R3]`; `M5` is only
the proposed diagnosis of the refutable encoding. Audit completion, theorem completion, validation,
release, and master acceptance are not claimed. Because the assigned phase is not complete,
`.stage1-worker-selftest.json` is deliberately absent.

## Failed Gate And Retry

The first failed gate is exact-target consistency at `M0112-S-INTERFACE`, before the relative-
homotopy and Morse obligations. The frozen root cut set remains `M0112-B-BELOW` plus
`M0112-B-EDGE`, but repair must start by reopening `S56-M-0112-STATEMENT`, replacing
`M0112-S-INTERFACE`, and rechecking `M0112-ROOT`.

Retry only after replacing the opaque stand-ins with native complex-geometric constructions or
noncircular semantic laws tying `piMap` to the actual inclusion-induced homotopy map, accepting a
new exact-statement fingerprint and obligation-registry version, and rerunning the statement,
anchor-audit, obligation-tree, and proof phases.

## Validation

All checks used the existing pinned Lake artifacts. No `lake update`, `lake build`, dependency
clone/fetch, network access, or `.lake` mutation was performed. The isolated Lean replay created
objects only under `/tmp` and removed them. A before/after metadata digest of the dereferenced
dependency cache was identical and is recorded in the JSON artifact.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0112` | 0 | Rank 35; planned lifecycle; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0112/check_statement.py` | 0 | Exact expression `1daee7f...eb654` elaborated; all four mutations were distinguished. |
| `python3 Stage1_Instances/THM-M-0112/check_anchor_audit.py` | 0 | Three pinned substrate candidate families checked; no terminal candidate exists. |
| `python3 Stage1_Instances/THM-M-0112/check_obligation_tree.py` | 0 | 13 obligations and 31 typed edges passed; denominator `5d119562...7df7f4`; root remains open M3. |
| Isolated trust-zero `lake env lean` recipe below | 0 | Exact statement and refutation elaborated; the negative declaration reports `[propext, Classical.choice, Quot.sound]`. |
| `rg -n --pcre2 '\b(?:sorry|admit|sorryAx|native_decide)\b|^[[:space:]]*(?:axiom|unsafe|external)\b|implemented_by' Stage1_Instances/THM-M-0112/Proof.lean` | 1 | Expected no-match exit; no prohibited proof escape occurs. |
| `python3 -m json.tool Stage1_Instances/THM-M-0112/proof-recheck-2026-07-14-head-0712591d.json` | 0 | The blocker record is valid JSON. |
| `git diff --check -- Stage1_Instances/THM-M-0112` | 0 | No whitespace error. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The incomplete proof phase emitted no completion manifest. |

Exact isolated Lean recipe, run from the repository root:

```bash
set -euo pipefail
before=$(find -L Formalizations/Lean/.lake -type f -printf '%p\t%s\t%T@\n' | sha256sum | cut -d' ' -f1)
tmp=$(mktemp -d /tmp/thm-m-0112-proof-head-0712591d.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-0112/Statement.lean "$tmp/Statement.lean"
cp Stage1_Instances/THM-M-0112/Proof.lean "$tmp/Proof.lean"
lean=$(cd Formalizations/Lean && lake env which lean)
lean_path=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
cd "$tmp"
LEAN_PATH="$lean_path" "$lean" --trust=0 -t0 -o Statement.olean Statement.lean
LEAN_PATH=.:"$lean_path" "$lean" --trust=0 -t0 Proof.lean
cd - >/dev/null
after=$(find -L Formalizations/Lean/.lake -type f -printf '%p\t%s\t%T@\n' | sha256sum | cut -d' ' -f1)
test "$before" = "$after"
```

The adjacent JSON binds this nonrelease blocker evidence to the source, registry, environment, and
current base. It is not a proof receipt.
