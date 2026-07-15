# THM-M-1041 proof-phase recheck at current base

Item: `S56-M-1041-PROOF`

Intent: `prove`

Recorded at: `2026-07-15T16:40:00+08:00` (`Asia/Shanghai`)

Base: commit `4159121c921a2115d1a9b787f70ff42d5fdb065e`, tree
`757644fd493543777f2596dd3848271a30848539`.

## Verdict

`blocked`; no state change.

The exact frozen target remains
`Stage1Instances.THM_M_1041.HilleYosidaContractionTarget`, expression SHA-256
`e6e5f0cbc4d61e4b3ac869fe7b01d4e0d28e3c558c1dea897c29871891f7768d`.
The root vector remains `[H2, M4, R4]`, lifecycle remains `planned`, and
`theorem_complete=false`.

No placeholder-free proof body for either frozen direction package exists in
the repository or pinned dependency closure. `ObligationTree.lean` contains
only the checked conditional composition
`root_of_directionPackages : ForwardPackage -> ConversePackage ->
HilleYosidaContractionTarget`; it constructs neither premise. The smallest
open root cut is therefore unchanged:

```text
M1041-F-ASSEMBLE
M1041-C-ASSEMBLE
```

The first unavailable forward leaf is `M1041-F-CLOSED`; independently, the
first unavailable converse leaf is `M1041-C-YOSIDA-APPROX`. The full missing
proof surface still includes generator closedness and density, a
Laplace/Bochner resolvent with both inverse laws and the contraction bound,
and the Yosida-approximation semigroup construction with laws, strong
continuity, contraction, and exact generator identification.

The proof-relevant statement, obligation architecture, anchor audit, manifest,
and toolchain files are unchanged since the last integrated recheck. A fresh
search across every pinned package source found no terminal Hille--Yosida or
strongly-continuous-semigroup generator theorem. The audited external
`mrdouglasny/hille-yosida` revision
`680e9499ee866763e737c8d888c1248684ced667` remains only a partial forward
anchor outside the pinned closure: it lacks closedness, density, the left
inverse, and the converse. A bounded live remote query reported `main` at that
same revision. The project was not fetched or integrated, and it receives no
proof credit.

Assuming either direction package, weakening the equivalence, or replacing
the analytic definitions with abstract proposition fields would add an
unproved premise or prove a substituted theorem, so those routes were
rejected. This artifact is blocker evidence, not a proof receipt. Because the
assigned phase is incomplete, `.stage1-worker-selftest.json` is deliberately
absent.

## Validation

All commands ran in this worker clone. The initial owned path was clean, with
only the automation-provided untracked `Formalizations/Lean/.lake` link. No
`lake update`, `lake build`, dependency clone or fetch, or `.lake` mutation
ran. The narrow Lean object was written to a fresh `/tmp` directory and
removed on exit.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1041` | 0 | Rank 234; lifecycle `planned`; `theorem_complete=false`. |
| `python3 Stage1_Instances/THM-M-1041/check_statement.py` | 0 | Exact expression SHA-256 `e6e5f0cbc4d61e4b3ac869fe7b01d4e0d28e3c558c1dea897c29871891f7768d`; all three structural mutations killed; toolchain and mathlib pin matched. |
| `python3 Stage1_Instances/THM-M-1041/check_anchor_audit.py` | 0 | `anchor audit invariant check: ok` |
| `python3 Stage1_Instances/THM-M-1041/check_obligation_tree.py` | 0 | 21 obligations and 56 typed edges passed; denominator `b9ebe90e50ff8cf0a0979d0e155ad58c2918a48cc3236e22f76fac67a6b39c42`; root and both direction packages remain `M4`. |
| Direct pinned `lean --trust=0 -t0` replay below | 0 | The exact `Statement.lean` and conditional `ObligationTree.lean` elaborated; temporary `Statement.olean` SHA-256 was `e2a26c6ee6807a3deaeb3c3cdc46e1802e989fba1e463a7ca46712689748caca`; `root_of_directionPackages` reports `[propext, Classical.choice, Quot.sound]`. |
| Pinned-package topical search below | 1 | Expected no-match across all pinned package sources. |
| Scoped prohibited-token scan below | 1 | Expected no-match in owned Lean sources. This lexical scan is supporting evidence only. |
| `git diff --quiet 63a9ed9c...HEAD -- <proof-relevant inputs>` | 0 | Statement, obligation architecture, audit input, manifest, and toolchain files are unchanged since the last integrated recheck. |
| `timeout --foreground 20 git ls-remote https://github.com/mrdouglasny/hille-yosida.git refs/heads/main` | 0 | `main` reports `680e9499ee866763e737c8d888c1248684ced667`, matching the audited revision; the project was not fetched or integrated. |

Exact narrow Lean replay, run from the repository root:

```bash
set -euo pipefail
repo=$PWD
lean_root=$repo/Formalizations/Lean
target=$repo/Stage1_Instances/THM-M-1041
tmp=$(mktemp -d /tmp/thm-m-1041-proof-head-4159121c-slot48.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
mathlib=$lean_root/.lake/packages/mathlib
lean=$(cd "$mathlib" && lake env which lean)
lake_path=$(cd "$mathlib" && lake env printenv LEAN_PATH)
cache_path=$(find "$lean_root/.lake/packages" -type d \
  -path '*/.lake/build/lib/lean' -print | sort | paste -sd:)
lean_path="$cache_path:$lake_path:$lean_root/.lake/build/lib/lean"
cd "$target"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" \
  timeout --foreground 600 "$lean" --trust=0 -t0 --root="$target" \
    -o "$tmp/Statement.olean" Statement.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
  timeout --foreground 600 "$lean" --trust=0 -t0 --root="$target" \
    ObligationTree.lean
```

Pinned-package search:

```bash
rg -n -i \
  'Hille.?Yosida|HilleYosida|Yosida|strongly continuous semigroup|C.?0 semigroup|infinitesimal generator|ContractionSemigroup' \
  Formalizations/Lean/.lake/packages --glob '*.lean'
```

Scoped prohibited-token scan:

```bash
rg -n -i \
  '\b(sorry|admit|sorryAx|unsafe|oracle)\b|(^|[^A-Za-z])(axiom|opaque)[[:space:]]' \
  Stage1_Instances/THM-M-1041 --glob '*.lean'
```

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake
`5.0.0-src+98dc76e`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`.

## Retry Condition

Resume after placeholder-free implementations of all children needed for both
frozen direction packages are available in the pinned closure, or after an
immutable compatible exact Lean 4 proof is pinned/imported and passes
exact-type, provenance, placeholder, axiom, composition, and trust checks.
