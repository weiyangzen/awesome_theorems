# THM-M-0406 proof-phase recheck at 823dfcd5

Item: `S56-M-0406-PROOF`

Intent: `prove`

Base revision: `823dfcd5e231e84436ac3d88948d8e669c168fdb`

Base tree: `a87f5f99350f49ddeb9d7df23dc6e0fe6fe3011f`

Recheck date: 2026-07-14 (Asia/Shanghai)

## Verdict

`blocked`. No consistent positive proof body exists for the exact frozen Lean
target. `SurfaceData.curve` is an unconstrained type, so the existing
placeholder-free countermodel chooses `curve := Empty`. It also chooses
`boundaryDivisor := Fin 4`, selects every component, uses unit weights and
intersection numbers, and makes every required geometric proposition true.
Thus every premise holds, while the conclusion would produce an inhabitant of
`Empty`.

The declaration

```text
Stage1Instances.THMM0406.not_corvajaZannierTheoremOne :
  Not (Stage1Instances.THMM0406.CorvajaZannierTheoremOne.{0, 0} (k := Rat))
```

kernel-checks at trust level zero against the current pinned closure. Its axiom
report is exactly `[propext, Classical.choice, Quot.sound]`. This refutes the
frozen abstract encoding, not the mathematical Corvaja--Zannier theorem.

`SurfaceDegeneracyEngine` in `ObligationTree.lean` is definitionally the same
refutable proposition. Its conditional adapter therefore supplies no positive
proof body. Adding a curve-existence premise, changing `SurfaceData`, or
proving only a realizable specialization would weaken or substitute the frozen
target and is outside this proof item.

The root remains `[H1, M5, R3]`; the remaining root cut is
`M0406-S-DEFINITIONS` and `M0406-ROOT`. No source, axiom, placeholder, unsafe
declaration, substituted theorem, or unpinned dependency was added.

## Failed Gate

The first failed gate is `M0406-S-DEFINITIONS` / exact-target consistency.
Positive proof work can resume only after an authorized statement-phase repair
provides intrinsic, noncircular geometric semantics that rule out this model,
followed by accepted replacement statement and obligation-registry versions
and renewed anchor-audit and obligation-tree gates. Merely assuming
`Nonempty X.curve` or the desired conclusion is not a source-faithful repair.

The proof item stays `[ ]`. No proof receipt, audit completion, theorem
completion, validation, release, scheduler transition, or master acceptance is
claimed. Because the assigned positive phase is not genuinely self-tested as
complete, `.stage1-worker-selftest.json` remains absent.

## Validation

All checks ran in this worker clone with the existing pinned Lake closure. The
automation-provided untracked `Formalizations/Lean/.lake` symlink was reused
read-only. No `lake update`, `lake build`, dependency clone/fetch, network
access, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0406` | 0 | Rank 19; lifecycle `planned`; baseline `L0/rework_required`; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0406/check_obligation_tree.py` | 0 | Fourteen obligations and 26 typed edges passed; denominator `46deb9e2...d90a7`; the frozen predecessor graph still records root open `M4`. |
| `python3 Stage1_Instances/THM-M-0406/check_anchor_audit.py` | 0 | Six candidates with immutable pins and substrate witnesses passed; no proof-bearing root candidate exists. |
| Isolated `lake env lean --trust=0 -t0` recipe below | 0 | The exact statement and countermodel refutation elaborated; both countermodel declarations report exactly `[propext, Classical.choice, Quot.sound]`. Statement-output SHA-256: `0f59d3486b6464922278f83f5e3871c79e0c2e7964d1e3a8a412f16e567b385b`; proof-output SHA-256: `942b7cc706eaa0b7aa1143e3ecfba1f8387659e19954b5b978ea77b98188a1f8`. |
| `rg -n '\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*axiom\b\|^[[:space:]]*unsafe\b' Stage1_Instances/THM-M-0406 --glob '*.lean'` | 1 | Expected no-match result: no prohibited construct in the owned Lean sources. |
| `cd Formalizations/Lean && lake env lean --version && git -C .lake/packages/mathlib rev-parse HEAD` | 0 | Lean `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| `python3 -m json.tool Stage1_Instances/THM-M-0406/proof-recheck-2026-07-14-head-823dfcd5.json` | 0 | Fresh structured blocker record is valid JSON. |
| `git diff --check -- Stage1_Instances/THM-M-0406` | 0 | No whitespace errors in the owned-path delta. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent because the positive proof phase is blocked. |

Exact isolated Lean recipe, run from the repository root:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0406
tmp=$(mktemp -d /tmp/thm-m-0406-head823dfcd5.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cd "$target"
LEAN_PATH="$lean_path" "$lean" --trust=0 -t0 \
  -o "$tmp/Statement.olean" Statement.lean >"$tmp/statement.log" 2>&1
LEAN_PATH="$tmp:$lean_path" "$lean" --trust=0 -t0 \
  Proof.lean >"$tmp/proof.log" 2>&1
sha256sum "$tmp/statement.log" "$tmp/proof.log"
```

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. Exact bound source hashes,
commands, output summaries, failed gate, retry condition, and changed paths are
recorded in `proof-recheck-2026-07-14-head-823dfcd5.json`.

This is fresh, target-specific negative kernel evidence. It is not a proof
receipt and does not satisfy `S56-M-0406-PROOF`.
