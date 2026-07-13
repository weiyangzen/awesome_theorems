# THM-M-0005 proof-phase recheck

Item: `S56-M-0005-PROOF`  
Intent: `prove`  
Base revision: `3bb4cb3ae15dff8b48c93242019edec3bf858e48`  
Base tree: `8e911f5a101bd92eb0951794fa0d9a3c0c3a2ddc`  
Recheck date: 2026-07-14 (Asia/Shanghai)

## Verdict

`blocked`. No placeholder-free proof body or eligible pinned import closes any new root-critical
mathematical obligation. The item remains `[ ]`; the root remains `[H1, M3, R3]`, and no audit,
theorem-completion, release, receipt-acceptance, or master-acceptance claim is made.

The exact root is `AwesomeTheorems.Stage1.THM_M_0005.KunnethFormula`: for every commutative PID it
requires one coherent family of PID-coefficient Kunneth short exact sequences for all spaces and
degrees, including the specified tensor and `Tor_1` summand maps and naturality in both spaces. The
local `assemble_sequence` declaration consumes all ten structure fields, and `root_compose`
consumes an already constructed family. Re-elaboration confirms their types, but neither supplies
chain projectivity, Eilenberg-Zilber, algebraic Kunneth exactness, or a transport to the exact root.

## Failed Gate

The first unavailable proof cut is `M0005-CHAIN-FREE` together with `M0005-EZ-MAP`. Pinned mathlib
and the existing `flt-regular` package provide singular-homology, `Tor`, tensor-complex, and
short-exact infrastructure, but no placeholder-free singular-chain projectivity package or
Eilenberg-Zilber/Alexander-Whitney product comparison. Consequently `M0005-EZ-EQUIV`,
`M0005-EZ-NAT`, the algebraic Kunneth maps/exactness/naturality, the direct-sum transports, the
component equations, topological naturality, assembly, and the root remain open.

Fresh exhaustive Sourcegraph searches, including archived repositories and forks, found the same
single Lean repository as the prerequisite audit: `facebookresearch/atlas-lean` at immutable commit
`34ffed396f376454c1a9b297f3fd74c5c801fb50`. Its `Section25.lean` and
`EilenbergZilber.lean` still contain `sorry` in every root-critical route. The repository's current
`HEAD` and `main` still resolve to that commit. The candidate also remains inexact: its topological
surface is universe zero, and it lacks the frozen tensor/Tor component equations and full packaged
two-variable naturality. Importing or wrapping it would fail both the trust and exact-target gates.

The complete remaining cut set and content hashes are recorded in
`proof-blocker-2026-07-14.json`. Resume only after local placeholder-free bodies for the frozen
chain-projectivity, Eilenberg-Zilber, and algebraic Kunneth packages and all transports are present,
or after a compatible immutable proof can be pin/import/checked without changing the dependency
lock. Because the assigned positive proof phase is incomplete, `.stage1-worker-selftest.json` is
deliberately absent.

## Validation

All checks ran in this worker clone and reused the automation-provided canonical `.lake` symlink
read-only. No `lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was run.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0005` | 0 | Rank 100; planned hard-mathlib lane; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0005/check_obligation_tree.py` | 0 | 18 obligations and 51 typed edges passed; denominator `563eac89...a762`; root remains open at `M3`. |
| isolated `lake env lean` recipe below | 0 | The exact target and both conditional composition declarations elaborated. No mathematical premise was closed. |
| `rg -n --pcre2 '\b(?:sorry\|admit\|axiom)\b\|sorryAx\|unsafe' Stage1_Instances/THM-M-0005 --glob '*.lean'` | 1 | No prohibited construct in the owned Lean sources; exit 1 is ripgrep's no-match result. |
| local semantic searches over pinned mathlib, `Archive`, and `flt-regular` | 0 | Support-only homology, tensor, `Tor`, and exactness hits; no Kunneth or product-comparison proof body. |
| Sourcegraph streaming searches for Kunneth/Kuenneth and EilenbergZilber/AlexanderWhitney with `archived:yes fork:yes` | 0 | Exhaustive results contained one repository, `atlas-lean@34ffed39...fb50`; its relevant bodies contain `sorry`. |
| `git ls-remote https://github.com/facebookresearch/atlas-lean.git refs/heads/main HEAD` | 0 | `HEAD` and `main` both resolve to `34ffed396f376454c1a9b297f3fd74c5c801fb50`. |
| `python3 -m json.tool Stage1_Instances/THM-M-0005/proof-blocker-2026-07-14.json` | 0 | Structured blocker syntax passed after creation. |
| `git diff --check -- Stage1_Instances/THM-M-0005` | 0 | No whitespace errors after creation. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent. |

The isolated Lean recipe, run from the repository root, placed all output under `/tmp`:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0005
tmp=$(mktemp -d /tmp/thm-m-0005-proof-recheck.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cp "$target/KunnethStatement.lean" "$tmp/KunnethStatement.lean"
cp "$target/ObligationTree.lean" "$tmp/ObligationTree.lean"
cd "$tmp"
LEAN_PATH="$lean_path" "$lean" --trust=0 -R "$tmp" -o "$tmp/KunnethStatement.olean" \
  "$tmp/KunnethStatement.lean"
LEAN_PATH="$tmp:$lean_path" "$lean" --trust=0 "$tmp/ObligationTree.lean"
```

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; `lake-manifest.json` SHA-256
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

This is fresh, target-specific negative evidence. It is not a proof receipt and does not satisfy
`S56-M-0005-PROOF`.
