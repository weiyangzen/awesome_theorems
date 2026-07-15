# THM-M-1200 proof-phase blocker at `c45766a` (slot28)

Item: `S56-M-1200-PROOF`

Date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `c45766a10a075c90791ad416bdb458018dabecd3`

Base tree: `20be1341815f84b94b5d6d02af21db6bc5a31c3f`

## Verdict

`blocked`; the assigned state remains `[ ]`. No positive Lean proof can
inhabit the exact frozen target because the tracked, placeholder-free
declaration

```lean
Stage1Instances.THM_M_1200.Counterexample.not_rankineHugoniotTarget :
  Not Stage1Instances.THM_M_1200.RankineHugoniotTarget
```

kernel-checks at trust level zero. The frozen statement requires
`ContDiff Real top phi`. In the pinned calculus API this is analytic order
`omega`, not smooth order `infinity`. Analytic uniqueness and compact support
force every admissible test function to be zero. Thus every interface defect
vanishes, while `f = 0`, `uL = 0`, `uR = 1`, and `s = 1` make the requested
jump law false.

The tracked proof-phase barrier

```lean
Stage1Instances.THM_M_1200.not_nonzeroTracePackage :
  Not Stage1Instances.THM_M_1200.NonzeroTracePackage
```

also kernel-checks. It proves that the construction assumed by the conditional
composition theorem cannot exist for the frozen test class. Neither negative
declaration is a positive proof receipt.

The first failed gate is rev-5.6 section 5.1 / `M1200-S-BOUNDARIES`. The
minimal frozen root cut is `M1200-C-TEST`, and the invalidated/open chain is
`M1200-S-BOUNDARIES`, `M1200-C-TEST`, and `M1200-ROOT`. In addition, the
prerequisite `S56-M-1200-OBLIGATION_TREE` is only provisional `[_]`, not
master-accepted `[x]`.

Repair belongs to the statement phase: replace the analytic outer `top` with
smooth `(infinity : WithTop ENat)`, issue a new statement fingerprint, and
freshly audit, freeze, and accept the dependent artifacts. Doing that in this
proof worker would substitute a different theorem and violate the assigned
phase boundary.

## Validation

All credited commands ran in this automation clone against the existing
canonical pinned Lean artifacts. No command updated, built, cloned, fetched,
or otherwise mutated `.lake`. Lean outputs were confined to a fresh temporary
directory under `/tmp`, which was removed after the check.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1200` | 0 | Rank 394; lifecycle `planned`; baseline L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1200/check_statement.py` | 0 | Expression SHA-256 `b77d79ed6acc61642c8288a004f1023d65a71367415ac90fd6a6c5e8af77ca93`; all four structural mutations distinguished; pins matched. |
| `python3 Stage1_Instances/THM-M-1200/check_obligation_tree.py` | 0 | `PASS`: 14 obligations, 54 typed edges, denominator `9915c4444fa19015a1a5aa3413871c87dafe1aeafb0ef4ab8540cacc01c54931`; root and nonzero-trace construction remain M4/open. |
| Isolated pinned Lean recipe below | 0 | Exact statement, countermodel, conditional composition, and proof barrier elaborated with `--trust=0 -t0`; printed axiom sets were exactly `[propext, Classical.choice, Quot.sound]`. |
| Prohibited-token scan below | 1 | Expected no-match: no prohibited proof device or declaration occurs in the owned Lean sources. |
| Parse every owned `*.json` with `python3 -m json.tool` | 0 | Every pre-existing JSON artifact parsed before this report was written. |
| `cd Formalizations/Lean && lake --offline env lean --version && lake --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release; Lake `5.0.0-src+98dc76e`. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | Mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`. |
| Structured evidence and source-hash assertions | 0 | `PASS current-base blocker invariants and source hashes`. |
| Explicit new-file whitespace checks | 0 | No whitespace error in either owned artifact. |
| `test ! -e .stage1-worker-selftest.json` | 0 | No completion packet exists for the blocked phase. |

The isolated Lean recipe was:

```bash
set -euo pipefail
root=$PWD
tmp=$(mktemp -d /tmp/thm-m-1200-head-c45766a-slot28.XXXXXX)
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

The final structured evidence check parsed this JSON, required the current
base revision and tree, checked the blocked/open booleans and empty receipt
sets, recomputed every recorded source hash, and asserted that the worker
self-test manifest was absent. Because ordinary `git diff --check` omits
untracked files, each new artifact was also checked explicitly with
`git diff --check --no-index /dev/null <path>`; exit `1` meant a clean new-file
diff and was normalized to success.

Thirty-seven proof-recheck JSON/Markdown pairs predate this report. Their file
count does not establish scheduler tick identity. The master must reconcile
actual attempts against the five-tick split threshold, but the checked
refutation independently means positive work must not retry this unchanged
target.

This is durable current-base blocker evidence, not completion. No theorem
source, predecessor artifact, scheduler authority, dependency, or unrelated
target changed. `.stage1-worker-selftest.json` is deliberately absent because
the assigned positive proof phase is not genuinely self-tested.
