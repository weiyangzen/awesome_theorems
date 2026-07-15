# THM-M-1200 proof-phase blocker at 5134bae (slot38)

Item: `S56-M-1200-PROOF`. Date: 2026-07-15. Base revision:
`5134bae303d5f5104698e8c96d7af4c26306eb47`; base tree:
`54e4bd2793df37c5451b86659fbd95a83504c25a`.

## Verdict

`blocked`; state remains `[ ]`. No positive proof body can inhabit the exact
frozen target because the tracked, placeholder-free declaration

```lean
Stage1Instances.THM_M_1200.Counterexample.not_rankineHugoniotTarget :
  Not Stage1Instances.THM_M_1200.RankineHugoniotTarget
```

kernel-refutes it. The frozen `ContDiff Real top` test class uses analytic
order `omega`, not smooth order `infinity`. Analytic uniqueness plus compact
support forces every admissible test function to be zero. Every interface
defect therefore vanishes, but `f = 0`, `uL = 0`, `uR = 1`, and `s = 1` make
the requested jump law false.

The tracked proof-phase barrier

```lean
Stage1Instances.THM_M_1200.not_nonzeroTracePackage :
  Not Stage1Instances.THM_M_1200.NonzeroTracePackage
```

also kernel-checks. It exposes that the nonzero-test construction required by
the frozen obligation tree cannot exist; it earns no positive proof credit.
The conditional composition theorem assumes precisely that impossible
package. The first failed gate is rev-5.6 section 5.1 /
`M1200-S-BOUNDARIES`, the minimal frozen root cut is `M1200-C-TEST`, and the
prerequisite `S56-M-1200-OBLIGATION_TREE` remains provisional `[_]`.

Repair belongs to the statement phase: replace analytic outer `top` with
smooth `(infinity : WithTop ENat)`, publish a new expression fingerprint, and
freshly audit and freeze all dependent artifacts. Making that substitution in
this proof worker would broaden its authority and prove a different target.

## Validation

No command updated, built, cloned, fetched, or otherwise mutated `.lake`.
Lean checks used `lake --offline env` only to select the existing pinned
executable and search path. Generated artifacts stayed under `/tmp` and were
removed after validation.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups and 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-1200` | 0 | Rank 394; planned; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1200/check_statement.py` | 0 | Statement expression SHA-256 `b77d79ed...ca93`; all four structural mutations distinguished; pinned Lean and mathlib revisions matched. |
| `python3 Stage1_Instances/THM-M-1200/check_obligation_tree.py` | 0 | `PASS`: 14 obligations, 54 typed edges, denominator `9915c444...c54931`; root and nonzero-trace construction remain M4/open. |
| Isolated pinned Lean `--trust=0 -t0` recipe below | 0 | Statement, countermodel, conditional composition, and proof-phase barrier elaborated; all printed axiom sets were `[propext, Classical.choice, Quot.sound]`. |
| Prohibited-token scan below | 1 | Expected no-match: no prohibited proof device or declaration occurs in the owned Lean sources. |
| `cd Formalizations/Lean && lake --offline env lean --version && lake --version` | 0 | Lean 4.29.0 at commit `98dc76e...`; Lake `5.0.0-src+98dc76e`. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | Pinned mathlib revision `8a178386...95`, tree `bdc39a31...b2b`. |

The isolated Lean recipe was:

```bash
set -euo pipefail
root=$PWD
tmp=$(mktemp -d /tmp/thm-m-1200-head-5134bae-slot38.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp "$root/Stage1_Instances/THM-M-1200/Statement.lean" "$tmp/Statement.lean"
cp "$root/Stage1_Instances/THM-M-1200/Counterexample.lean" "$tmp/Counterexample.lean"
cp "$root/Stage1_Instances/THM-M-1200/ObligationTree.lean" "$tmp/ObligationTree.lean"
cp "$root/Stage1_Instances/THM-M-1200/ProofRefutation.lean" "$tmp/ProofRefutation.lean"
cd "$root/Formalizations/Lean"
lean=$(lake --offline env which lean)
base_lean_path=$(lake --offline env printenv LEAN_PATH | tr ':' '\n' | \
  rg -v '^.*/Formalizations/Lean/\.lake/build/lib/lean$' | paste -sd: -)
for module in Statement Counterexample ObligationTree ProofRefutation; do
  if [ "$module" = Statement ]; then
    module_path="$base_lean_path"
  else
    module_path="$tmp:$base_lean_path"
  fi
  LEAN_NUM_THREADS=1 LEAN_PATH="$module_path" \
    timeout --foreground --kill-after=10s 600 \
    "$lean" --trust=0 -t0 -R "$tmp" \
    -o "$tmp/$module.olean" "$tmp/$module.lean"
done
sha256sum "$tmp"/*.olean
```

Output SHA-256 values:

| Output | SHA-256 |
|---|---|
| `Statement.olean` | `74f5f45b992141e003cee16879671aea16eb7e14174374070dd37062f35276b0` |
| `Counterexample.olean` | `3f4ccc8963bc2e801b8d2ed33909e9ed67d34503008f3b210ae96049791b6485` |
| `ObligationTree.olean` | `c3ab556b8209466f1dcbf67faeec45834fa5bd9d242dc797b05f1f221a844044` |
| `ProofRefutation.olean` | `1ae262cb2c3a2a9c6657721427154adb08f87bd9eac9ad9f0ffd571917cf8d08` |

The exact prohibited-token scan was:

```bash
rg -n --pcre2 \
  '\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b|^[[:space:]]*(?:axiom|unsafe|opaque|extern|external|constant)[[:space:]]' \
  Stage1_Instances/THM-M-1200 --glob '*.lean'
```

The structured record binds the item, target, immutable base/tree, source and
output hashes, exact negative declarations, frozen registry, environment,
commands, debt boundary, first failed gate, and retry condition. JSON syntax,
record invariants, hashes, and whitespace are checked after this report is
written.

Thirty-four proof-recheck JSON records predate this one. File count is not
scheduler-tick evidence. The master must reconcile actual ticks and split or
redirect after five unresolved executions. Positive proof work must not retry
the unchanged false target.

This is durable blocker evidence, not a completion receipt. No scheduler
authority, predecessor, dependency, or unrelated target was changed.
`.stage1-worker-selftest.json` is deliberately absent because the assigned
positive proof phase is not genuinely complete.
