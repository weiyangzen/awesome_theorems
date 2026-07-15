# THM-M-1200 proof-phase blocker recheck

Item: `S56-M-1200-PROOF`

- Base revision: `ebfa067f2385ca03cc0a0eeecf151993a994962c`
- Base tree: `4d482bdb45ec4ff17c128d712608f7c7eea1ffc8`
- Recorded: 2026-07-15 (`Asia/Shanghai`)
- Worker clone: Stage1 rev-5.6 slot37

## Verdict

`blocked`; the item stays `[ ]`. No positive proof body can inhabit the exact
frozen target. The placeholder-free declaration

```text
Stage1Instances.THM_M_1200.Counterexample.not_rankineHugoniotTarget :
  Not Stage1Instances.THM_M_1200.RankineHugoniotTarget
```

kernel-checks at trust level zero. The frozen predicate requires
`ContDiff Real top phi`. Its order type is `WithTop ENat`; the outer `top` is
the analytic order `omega`, whereas the intended smooth order is
`(top : ENat)` coerced into `WithTop ENat`. Analytic uniqueness and compact
support force every admissible test function to be zero. Hence every interface
defect vanishes, including at `f = 0`, `uL = 0`, `uR = 1`, and `s = 1`, while
the target's jump law becomes the false equality `1 = 0`.

The conditional composition theorem
`rankineHugoniotTarget_of_nonzeroTracePackage` cannot supply positive root
closure: `ProofRefutation.lean` kernel-checks
`not_nonzeroTracePackage : Not NonzeroTracePackage`. These negative
declarations concern only the frozen analytic-test encoding, not the
mathematical Rankine-Hugoniot theorem with smooth compactly supported tests.

## Failed Gates And Retry

The first workflow gate fails because prerequisite
`S56-M-1200-OBLIGATION_TREE` remains provisional `[_]`, not master-accepted
`[x]`. Independently, the first semantic failure is rev-5.6 section 5.1 exact
target consistency at `M1200-S-BOUNDARIES`. The minimal root cut is
`M1200-C-TEST`; the invalidated or open chain is `M1200-S-BOUNDARIES`,
`M1200-C-TEST`, and `M1200-ROOT`. This supports proposed `[H5, M5, R3]`
blocker classification, not M0 closure.

An authorized repair must return to the statement phase, use smooth
`(top : ENat)` coerced into `WithTop ENat`, add an order-sensitive mutation,
and version or transitively fingerprint the changed predicate. The statement,
anchor audit, obligation registry, and typed graphs must then be freshly
accepted in dependency order. The other legal route is explicit redirection
to the checked counterexample or barrier target. Either route is outside this
proof worker's authority; changing the statement here would substitute the
assigned theorem.

There were 46 pre-existing `proof-recheck-*.json` records (and the same number
of Markdown records), plus `proof-blocker.json`. Record count is not scheduler
tick identity. The master must reconcile its tick ledger and apply the
five-unresolved-tick split rule. Positive proof work must not retry this
unchanged target.

## Validation

All credited commands ran in this worker clone with the existing pinned Lean
toolchain and canonical compiled dependencies. No `lake update`, `lake build`,
dependency clone/fetch, network action, or `.lake` mutation was run. Fresh Lean
outputs lived only in a temporary directory under `/tmp`, which was removed.
The automation-provided untracked `.lake` symlink makes this nonrelease
evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups and 1546 uniform-L0 targets. |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-1200` | 0 | Rank 394; planned; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1200/check_statement.py` | 0 | Expression SHA `b77d79ed...ca93`, pinned Lean/mathlib, and four killed structural mutations. |
| `python3 Stage1_Instances/THM-M-1200/check_obligation_tree.py` | 0 | `PASS`: 14 obligations and 54 typed edges; denominator `9915c444...c54931`; root and construction remain M4. |
| Isolated pinned `lake --offline env lean --trust=0` recipe below | 0 | Statement, exact countermodel, conditional composition, and package refutation elaborated. Axiom reports contain exactly `[propext, Classical.choice, Quot.sound]`; no `sorryAx`. |
| Direct pinned Lean `--deps` over the temporary `ProofRefutation.lean` | 0 | `Counterexample.olean` and `ObligationTree.olean` resolved from the fresh temporary directory. |
| Scoped prohibited-token scan over owned Lean sources | 1 | Expected no-match: no prohibited proof device or declaration. |
| Pinned version and revision checks | 0 | Lean 4.29.0 commit `98dc76e...`; Lake `5.0.0-src+98dc76e`; mathlib `8a178386...`; flt-regular `56161b6e...`. |
| Structured evidence and source-hash check | 0 | `PASS current-base blocker invariants and source hashes`. |
| Scoped and explicit new-file whitespace checks | 0 | No whitespace errors. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion manifest correctly absent. |

The isolated Lean recipe was:

```bash
set -euo pipefail
repo=$PWD
canonical=$(readlink -f Formalizations/Lean/.lake)
packages=$canonical/packages
mathlib=$packages/mathlib
lean_bin=$(cd "$mathlib" && timeout 90 lake env which lean)
toolchain_lib=$(realpath "$(dirname "$lean_bin")/../lib/lean")
lean_path=$toolchain_lib
for package in "$packages"/*; do
  if [ -d "$package/.lake/build/lib/lean" ]; then
    lean_path="$lean_path:$package/.lake/build/lib/lean"
  fi
done
tmp=$(mktemp -d /tmp/thm-m-1200-proof-head-ebfa067f-slot37.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
for module in Statement Counterexample ObligationTree ProofRefutation; do
  cp "$repo/Stage1_Instances/THM-M-1200/$module.lean" "$tmp/$module.lean"
done
cd "$mathlib"
for module in Statement Counterexample ObligationTree ProofRefutation; do
  path=$lean_path
  if [ "$module" != Statement ]; then path="$tmp:$lean_path"; fi
  LEAN_PATH="$path" LEAN_NUM_THREADS=1 \
    timeout --foreground --kill-after=10s 600 \
    lake --offline env lean --trust=0 -t0 -R "$tmp" \
      -o "$tmp/$module.olean" "$tmp/$module.lean" \
      >"$tmp/$module.log" 2>&1
done
cat "$tmp"/{Statement,Counterexample,ObligationTree,ProofRefutation}.log \
  >"$tmp/kernel.log"
cat "$tmp/kernel.log"
sha256sum "$tmp"/{Statement,Counterexample,ObligationTree,ProofRefutation}.olean \
  "$tmp/kernel.log"
LEAN_PATH="$tmp:$lean_path" "$lean_bin" --deps -R "$tmp" \
  "$tmp/ProofRefutation.lean"
```

Fresh output hashes:

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

This is durable blocker evidence, not a positive proof receipt. It changes no
Lean source, predecessor artifact, scheduler authority, dependency, or
unrelated target. `.stage1-worker-selftest.json` is deliberately absent
because the requested proof phase is not genuinely complete.
