# THM-M-1200 proof-phase current-base blocker recheck

Item: `S56-M-1200-PROOF`. Execution rank: 394. Phase: `proof`.
Base revision: `5343398eefd7ea3748a59578603c5dccbc1b69a0`.
Base tree: `b4809c2e77398eb355161e0220715730a1354bef`.
Recorded on 2026-07-16 in the Stage1 rev-5.6 slot36 worker clone.

## Verdict

`blocked`. The exact frozen positive target cannot be proved. Fresh trust-zero
elaboration checks the existing placeholder-free declarations

```lean
Stage1Instances.THM_M_1200.Counterexample.not_rankineHugoniotTarget :
  Not Stage1Instances.THM_M_1200.RankineHugoniotTarget

Stage1Instances.THM_M_1200.not_nonzeroTracePackage :
  Not Stage1Instances.THM_M_1200.NonzeroTracePackage
```

The statement requires `ContDiff Real top phi`. Pinned mathlib explicitly
distinguishes the outer `top : WithTop ENat`, denoted analytic order `omega`,
from the coerced inner `top : ENat`, denoted smooth order `infinity`.
`contDiff_omega_iff_analyticOnNhd` confirms the analytic interpretation.
Analytic uniqueness and compact support force every admissible `phi` to be
zero, so `InterfaceDefectVanishes` holds for every jump coefficient.
Specializing the frozen target to `f = 0`, `uL = 0`, `uR = 1`, and `s = 1`
would then require the false equation `1 = 0`.

This refutes only the frozen analytic-test encoding, not the mathematical
Rankine-Hugoniot theorem with smooth compactly supported tests. Replacing the
regularity order here would substitute a different target and invalidate the
dependent audit and obligation artifacts. The conditional composition theorem
also cannot close the root because its `NonzeroTracePackage` premise is
kernel-refuted.

The assigned item remains `[ ]`. No positive proof body, root closure, proof
receipt, audit completion, theorem completion, validation completion, release
decision, or master acceptance is claimed. `.stage1-worker-selftest.json` is
deliberately absent because the requested positive proof phase is not genuinely
self-tested as complete.

## Failed Gate And Retry

The prerequisite `S56-M-1200-OBLIGATION_TREE` remains provisional `[_]`, not
accepted `[x]`, so dependency-ordered proof acceptance is unavailable.
Independently, the first semantic failure is rev-5.6 section 5.1 exact-target
consistency at `M1200-S-BOUNDARIES`: analytic compact support collapses the test
class to zero and makes the universal target false. The minimal root cut is
`M1200-C-TEST`; the invalidated or open chain is `M1200-S-BOUNDARIES`,
`M1200-C-TEST`, and `M1200-ROOT`. This recheck proposes blocker classification
`[H5, M5, R3]` from provisional `[H3, M4, R3]` and changes no authority state.

Positive work requires an authorized statement-phase repair using
`ContDiff Real ∞ phi` after `open scoped ContDiff`, equivalently
`ContDiff Real ((⊤ : ENat) : WithTop ENat) phi`; a versioned or transitively
unfolded statement fingerprint; an order-sensitive mutation test; and freshly
frozen and accepted statement, anchor-audit, registry, and typed-graph
artifacts. The alternative is explicit scheduler redirection to the checked
counterexample or barrier target.

There were 49 JSON and 49 Markdown proof-recheck records before this handoff;
this is the 50th pair, and the structured blocker count is 51 when
`proof-blocker.json` is included. File counts are not private scheduler tick
evidence. The authoritative assignment still says `attempts: 0`; the master
must reconcile actual attempts against the five-tick split rule. Regardless of
that accounting, the checked refutation forbids another positive proof attempt
against the unchanged target.

## Validation

All credited commands ran from this worker clone. They reused the existing
canonical pinned `.lake` artifacts read-only. No `lake update`, `lake build`,
dependency clone/fetch, network operation, or dependency mutation was run.
Lean outputs lived only in a fresh `/tmp` directory removed by a trap.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups and all 1546 uniform-L0 targets. |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets at ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-1200` | 0 | Rank 394; planned L0/rework-required; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1200/check_statement.py` | 0 | Expression SHA-256 `b77d79ed6acc61642c8288a004f1023d65a71367415ac90fd6a6c5e8af77ca93`; four structural mutations killed. |
| `python3 Stage1_Instances/THM-M-1200/check_obligation_tree.py` | 0 | 14 obligations and 54 typed edges passed; root and nonzero-trace construction remain open at M4. |
| Isolated pinned `lake env lean --trust=0 -t0` recipe below | 0 | Statement, countermodel, conditional composition, and package refutation elaborated; axiom sets were exactly `propext`, `Classical.choice`, and `Quot.sound`. |
| Prohibited-token scan below | 1 | Expected no-match: no prohibited proof device or declaration in scoped Lean sources. |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake `5.0.0-src+98dc76e`. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | Mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`. |
| Structured artifact check below | 0 | `PASS current-base THM-M-1200 blocker invariants and source hashes`. |
| Scoped whitespace checks below | 0 | No whitespace errors in the two new owned artifacts. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Incomplete proof phase correctly emitted no completion packet. |

The isolated Lean recipe was:

```bash
set -euo pipefail
repo=$PWD
canonical=$(readlink -f Formalizations/Lean/.lake)
packages=$canonical/packages
mathlib=$packages/mathlib
lean_bin=$(cd "$mathlib" && timeout --foreground --kill-after=10s 90 lake env which lean)
toolchain_lib=$(realpath "$(dirname "$lean_bin")/../lib/lean")
base_path=$toolchain_lib
for package in "$packages"/*; do
  if [ -d "$package/.lake/build/lib/lean" ]; then
    base_path="$base_path:$package/.lake/build/lib/lean"
  fi
done
tmp=$(mktemp -d /tmp/thm-m-1200-proof-head-5343398e-slot36.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
for module in Statement Counterexample ObligationTree ProofRefutation; do
  cp "$repo/Stage1_Instances/THM-M-1200/$module.lean" "$tmp/$module.lean"
done
cd "$mathlib"
for module in Statement Counterexample ObligationTree ProofRefutation; do
  if [ "$module" = Statement ]; then
    module_path="$base_path"
  else
    module_path="$tmp:$base_path"
  fi
  LEAN_PATH="$module_path" LEAN_NUM_THREADS=1 \
    timeout --foreground --kill-after=10s 600 \
    lake env lean --trust=0 -t0 -R "$tmp" \
      -o "$tmp/$module.olean" "$tmp/$module.lean" \
      >"$tmp/$module.log" 2>&1
done
cat "$tmp/Statement.log" "$tmp/Counterexample.log" \
  "$tmp/ObligationTree.log" "$tmp/ProofRefutation.log" >"$tmp/kernel.log"
cat "$tmp/kernel.log"
sha256sum "$tmp/Statement.olean" "$tmp/Counterexample.olean" \
  "$tmp/ObligationTree.olean" "$tmp/ProofRefutation.olean" "$tmp/kernel.log"
```

Fresh SHA-256 output hashes:

| Output | SHA-256 |
|---|---|
| `Statement.olean` | `74f5f45b992141e003cee16879671aea16eb7e14174374070dd37062f35276b0` |
| `Counterexample.olean` | `3f4ccc8963bc2e801b8d2ed33909e9ed67d34503008f3b210ae96049791b6485` |
| `ObligationTree.olean` | `c3ab556b8209466f1dcbf67faeec45834fa5bd9d242dc797b05f1f221a844044` |
| `ProofRefutation.olean` | `1ae262cb2c3a2a9c6657721427154adb08f87bd9eac9ad9f0ffd571917cf8d08` |
| Combined kernel log | `a91296be37b65fbe52ab3ec716c621079391b7ba096adb37d520cacf83b37aa0` |

The prohibited-token scan was:

```bash
rg -n --pcre2 \
  '\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b|^[[:space:]]*(?:axiom|unsafe|opaque|extern|external|constant)[[:space:]]' \
  Stage1_Instances/THM-M-1200 --glob '*.lean'
```

The auxiliary structured check parsed this JSON, bound it to `HEAD` and
`HEAD^{tree}`, checked the exact negative and open-state invariants, verified
source hashes and 50/51 record counts, and required the root self-test manifest
to stay absent. Its result is recorded here; unlike the complete Lean recipe
above, its inline assertion script is not claimed as a durable validation
recipe.

Whitespace validation ran:

```bash
git diff --check -- Stage1_Instances/THM-M-1200 \
  .stage1-worker-selftest.json
git diff --check --no-index /dev/null \
  Stage1_Instances/THM-M-1200/proof-recheck-2026-07-16-head-5343398e-slot36.json
git diff --check --no-index /dev/null \
  Stage1_Instances/THM-M-1200/proof-recheck-2026-07-16-head-5343398e-slot36.md
```

The two no-index commands normally exit 1 for a newly added file; the wrapper
accepted that exit only after each command printed no whitespace error.

This is durable blocker evidence, not a completion receipt. It changes no Lean
source, frozen predecessor, scheduler authority, dependency artifact, or
unrelated target.
