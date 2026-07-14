# THM-M-1111 proof-phase recheck at current base

Item: `S56-M-1111-PROOF`

Intent: `prove`

Date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `a1a7e939e58f103f5ff5d23af51437fa8658aa04`

Base tree: `d881fd9641fa3e5f3ebe5082b35672981e90adcf`

## Verdict

`blocked`. No positive proof body can consistently inhabit the current frozen target. The exact
proposition quantifies over an arbitrary `FourMomentSemantics`, but the structure supplies no laws
for `powerBound` or the other semantic fields. The existing placeholder-free declaration

```text
Stage1Instances.THM_M_1111.not_taoVuFourMomentTarget_counterSemantics :
  Not (Stage1Instances.THM_M_1111.TaoVuFourMomentTarget
    Stage1Instances.THM_M_1111.counterSemantics)
```

was replayed at Lean trust level zero. Its admissible instance uses `Unit` for both carrier families,
makes every target hypothesis predicate true, makes both expected statistics zero, and makes
`powerBound` constantly `-1`. After choosing `epsilon = 1/2`, `k = C = C' = 1`,
`n = 2 * (N + 1)`, and the single bulk index `N + 1`, the target conclusion becomes `0 <= -1`.
Lean reports only `propext`, `Classical.choice`, and `Quot.sound` for this refutation.

This countermodel refutes only the frozen abstract encoding, not the Tao--Vu Four Moment Theorem.
The checked declaration `taoVuFourMomentTarget_of_comparisonPackage` is also not a positive result:
`FourMomentComparisonPackage S` is definitionally the root, so the declaration merely transports
an explicit open premise to that same root. It implements none of the frozen analytic obligations.

No positive proof body, proof receipt, or obligation closure was added. The proof item remains
`[ ]`; lifecycle remains `planned`; the later typed-graph root remains `[H2, M3, R3]`. The intake
manifest still says `[H1, M4, R4]`, and the older blocker says `M4`; integration must reconcile these
stale projections. Classifying the refutable encoding as `M5` is proposed for integration review,
but this worker does not edit authoritative state. Proof-phase completion, root closure, audit
completion, validation, release, theorem completion, and master acceptance are all false. Because
the assigned phase is incomplete, `.stage1-worker-selftest.json` is deliberately absent.

## Failed Gate And Retry

The first failed gate is exact-target consistency at `M1111-S-DEFS`. The predecessor graph records
`M1111-T-TELESCOPE` as the remaining root cut, but no analytic subtree can prove a universally
quantified target that includes the checked counterinstance. The actionable cut therefore begins at
`S56-M-1111-STATEMENT`, `M1111-S-DEFS`, and `M1111-ROOT`.

Resume only after an authorized statement revision replaces the arbitrary interface with a fixed,
source-faithful model of random Hermitian matrices or adds noncircular source-justified laws that
rule out the countermodel and support the comparison estimate. Accept a new target fingerprint,
refreeze the anchor audit and obligation registry, and rerun all downstream phases before attempting
a positive proof.

## Validation

All checks ran in this worker clone against the existing pinned Lake artifacts. The
automation-provided untracked `Formalizations/Lean/.lake` symlink was reused read-only. No
`lake update`, `lake build`, dependency clone/fetch, network access, or `.lake` mutation was
performed. Temporary Lean objects were created under `/tmp` and removed by a shell trap.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1111` | 0 | Rank 551; planned lifecycle; hard-mathlib lane; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1111/check_statement.py` | 0 | Required target fragments and structural mutations passed; statement SHA-256 `1b569042...68ebc`. |
| `python3 Stage1_Instances/THM-M-1111/check_obligation_tree.py` | 0 | 19 obligations and 46 typed edges passed; denominator `cf7ead85...6d54`; root remains open M3. |
| Isolated trust-zero `lake env lean` recipe below | 0 | The exact statement, checked countermodel, and conditional composition elaborated; both checked declarations report `[propext, Classical.choice, Quot.sound]`. |
| `rg -n --pcre2 '\\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\\b|^[[:space:]]*(?:axiom|opaque|constant|unsafe|external)[[:space:]]' Stage1_Instances/THM-M-1111 --glob '*.lean'` | 1 | Expected no-match exit; no prohibited proof escape occurs in owned Lean source. |
| `python3 -m json.tool Stage1_Instances/THM-M-1111/proof-recheck-2026-07-15-head-a1a7e939.json` | 0 | The structured current-base blocker record is valid JSON. |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-1111/proof-recheck-2026-07-15-head-a1a7e939.json` | 1 | Expected new-file difference with no whitespace diagnostic. |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-1111/proof-recheck-2026-07-15-head-a1a7e939.md` | 1 | Expected new-file difference with no whitespace diagnostic. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The incomplete proof phase emitted no completion manifest. |

Exact isolated Lean recipe, run from the repository root:

```bash
set -euo pipefail
root=$PWD
tmp=$(mktemp -d /tmp/thm-m-1111-proof-recheck.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-1111/Statement.lean "$tmp/Statement.lean"
cp Stage1_Instances/THM-M-1111/ProofBlocker.lean "$tmp/ProofBlocker.lean"
cp Stage1_Instances/THM-M-1111/ObligationTree.lean "$tmp/ObligationTree.lean"
cd "$root/Formalizations/Lean"
lean_path=$(lake env printenv LEAN_PATH)
lean=$(lake env which lean)
cd "$tmp"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 180 "$lean" --trust=0 -t0 -R "$tmp" \
  -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 180 "$lean" --trust=0 -t0 -R "$tmp" \
  -o "$tmp/ProofBlocker.olean" "$tmp/ProofBlocker.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 180 "$lean" --trust=0 -t0 -R "$tmp" \
  -o "$tmp/ObligationTree.olean" "$tmp/ObligationTree.lean"
```

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`); `lake-manifest.json` SHA-256
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Status Boundary

This is durable current-base blocker evidence, not a positive proof receipt. It changes only the
assigned target-owned directory and does not satisfy `S56-M-1111-PROOF`. It claims no validation,
release, master acceptance, audit completion, or theorem completion.
