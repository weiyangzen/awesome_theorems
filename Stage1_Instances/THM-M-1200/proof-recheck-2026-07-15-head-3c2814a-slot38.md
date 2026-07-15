# THM-M-1200 proof-phase blocker at 3c2814a (slot38)

Item: `S56-M-1200-PROOF`. Date: 2026-07-15. Base revision:
`3c2814a370c2fee02158ca79aa44a48e411c4d18`; base tree:
`e1bd7e27bd922b779322c089410a471b6a1535f0`.

## Verdict

`blocked`; state remains `[ ]`. No positive proof body exists for the exact
frozen target. The tracked placeholder-free declaration

```lean
Stage1Instances.THM_M_1200.Counterexample.not_rankineHugoniotTarget :
  Not Stage1Instances.THM_M_1200.RankineHugoniotTarget
```

kernel-refutes it. `ContDiff Real top` is analytic order `omega` in the pinned
calculus API, not smooth order `infinity`. Analytic uniqueness plus compact
support forces every admissible test function to be zero. Thus every interface
defect vanishes, while `f = 0`, `uL = 0`, `uR = 1`, and `s = 1` make the jump
law false.

`ProofRefutation.lean` adds a checked negative proof-phase certificate:

```lean
Stage1Instances.THM_M_1200.not_nonzeroTracePackage :
  Not Stage1Instances.THM_M_1200.NonzeroTracePackage
```

It exposes, rather than conceals, that the nonzero-test construction needed by
the frozen architecture cannot exist. It earns no positive root proof credit.
The first failed gate is rev-5.6 section 5.1 / `M1200-S-BOUNDARIES`; the
minimal frozen root cut is `M1200-C-TEST`. The prerequisite
`S56-M-1200-OBLIGATION_TREE` also remains provisional `[_]`.

The repair belongs to the statement phase: use smooth
`(infinity : WithTop ENat)`, publish a new exact-expression fingerprint, and
freshly audit and freeze every dependent artifact. Substituting that repaired
theorem here would violate this worker's assigned proof scope.

## Validation

No command updated, built, cloned, fetched, or otherwise mutated `.lake`.
Lean commands used `lake --offline env lean`, read the automation-provided
canonical pinned artifacts, and wrote generated output only under `/tmp`.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups and 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-1200` | 0 | Rank 394; planned; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1200/check_obligation_tree.py` | 0 | `PASS`: 14 obligations, 54 typed edges, denominator `9915c444...c54931`; root remains M4/open. |
| Isolated pinned Lean `--trust=0 -t0` recipe below | 0 | Statement, countermodel, and negative proof-phase certificate elaborated; every printed axiom set was `[propext, Classical.choice, Quot.sound]`. |
| Prohibited-token scan below | 1 | Expected no-match: no prohibited proof device or declaration. |
| Structured JSON/hash check below | 0 | `PASS current-base blocker invariants and source hashes`. |
| Scoped `git diff --check --no-index` checks | 0 | No whitespace error in any new owned artifact. |
| `test ! -e .stage1-worker-selftest.json` | 0 | No false completion packet was emitted. |

The isolated Lean recipe was:

```bash
set -euo pipefail
root=$PWD
tmp=$(mktemp -d /tmp/thm-m-1200-slot38.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp "$root/Stage1_Instances/THM-M-1200/Statement.lean" "$tmp/Statement.lean"
cp "$root/Stage1_Instances/THM-M-1200/Counterexample.lean" "$tmp/Counterexample.lean"
cp "$root/Stage1_Instances/THM-M-1200/ObligationTree.lean" "$tmp/ObligationTree.lean"
cp "$root/Stage1_Instances/THM-M-1200/ProofRefutation.lean" "$tmp/ProofRefutation.lean"
cd "$root/Formalizations/Lean"
lean=$(lake --offline env which lean)
base_lean_path=$(lake --offline env printenv LEAN_PATH | tr ':' '\n' | \
  rg -v '^.*/Formalizations/Lean/\.lake/build/lib/lean$' | paste -sd: -)
LEAN_NUM_THREADS=1 LEAN_PATH="$base_lean_path" \
  timeout --foreground --kill-after=10s 600 \
  "$lean" --trust=0 -t0 -R "$tmp" \
  -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base_lean_path" \
  timeout --foreground --kill-after=10s 600 \
  "$lean" --trust=0 -t0 -R "$tmp" \
  -o "$tmp/Counterexample.olean" "$tmp/Counterexample.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base_lean_path" \
  timeout --foreground --kill-after=10s 600 \
  "$lean" --trust=0 -t0 -R "$tmp" \
  -o "$tmp/ObligationTree.olean" "$tmp/ObligationTree.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base_lean_path" \
  timeout --foreground --kill-after=10s 600 \
  "$lean" --trust=0 -t0 -R "$tmp" \
  -o "$tmp/ProofRefutation.olean" "$tmp/ProofRefutation.lean"
sha256sum "$tmp/Statement.olean" "$tmp/Counterexample.olean" \
  "$tmp/ObligationTree.olean" "$tmp/ProofRefutation.olean"
```

Output SHA-256 values:

| Output | SHA-256 |
|---|---|
| `Statement.olean` | `74f5f45b992141e003cee16879671aea16eb7e14174374070dd37062f35276b0` |
| `Counterexample.olean` | `3f4ccc8963bc2e801b8d2ed33909e9ed67d34503008f3b210ae96049791b6485` |
| `ObligationTree.olean` | `c3ab556b8209466f1dcbf67faeec45834fa5bd9d242dc797b05f1f221a844044` |
| `ProofRefutation.olean` | `1ae262cb2c3a2a9c6657721427154adb08f87bd9eac9ad9f0ffd571917cf8d08` |

The prohibited-token scan was:

```bash
rg -n --pcre2 \
  '\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b|^[[:space:]]*(?:axiom|unsafe|opaque|extern|external|constant)[[:space:]]' \
  Stage1_Instances/THM-M-1200 --glob '*.lean'
```

The structured check validated JSON syntax; item, target, base revision and
tree; blocked state; incomplete root/audit/theorem flags; absence of accepted
receipts and self-test; and SHA-256 hashes for all inputs named in the JSON.

Thirty-three proof-recheck JSON records predate this one. File count is not
scheduler-tick evidence. The master must reconcile actual ticks and split or
redirect after five unresolved executions. Do not retry this unchanged proof
item; resume only after the corrected statement and invalidated prerequisites
are dependency-order reaccepted, or after explicit counterexample/barrier
redirection.

This is durable blocker evidence, not a completion receipt. No scheduler
authority, frozen predecessor, dependency, or unrelated target was changed.
`.stage1-worker-selftest.json` is deliberately absent because the assigned
positive proof phase is not genuinely complete.
