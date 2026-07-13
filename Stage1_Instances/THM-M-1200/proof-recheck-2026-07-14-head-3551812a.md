# THM-M-1200 proof-phase recheck at `3551812a`

Item: `S56-M-1200-PROOF`

Recheck date: `2026-07-14` (`Asia/Shanghai`)

Base revision: `3551812aeaf826b94804e464b34511a7bbc7f6ff`

Base tree: `6ed6612d0a642e6879579700427c67045c1a34d7`

## Verdict

`blocked`. No positive Lean proof can inhabit the exact frozen target. The
tracked, placeholder-free declaration

```text
Stage1Instances.THM_M_1200.Counterexample.not_rankineHugoniotTarget :
  Not Stage1Instances.THM_M_1200.RankineHugoniotTarget
```

kernel-checks at trust level zero against a freshly elaborated
`Statement.olean`.

The statement requires `ContDiff Real top phi`. In the pinned calculus API,
that outer `top` is the analytic order `omega`; smooth bump functions instead
have order `infinity`. Analytic uniqueness and compact support force every
admissible `phi` to be zero. Hence `InterfaceDefectVanishes` is true for every
jump coefficient. Specializing the target to `f = 0`, `uL = 0`, `uR = 1`, and
`s = 1` would require the false jump law `1 = 0`.

This refutes only the frozen analytic-test encoding, not the mathematical
Rankine-Hugoniot theorem with smooth compactly supported tests. Replacing the
outer `top` with smooth `infinity` here would substitute a repaired statement
and is outside the assigned proof phase. The conditional composition theorem
also cannot close the root: its `NonzeroTracePackage` premise is impossible
for the frozen test class.

The assigned item remains `[ ]`. No positive proof body or receipt, state
transition, audit completion, theorem completion, validation completion,
release, or master acceptance is claimed. `.stage1-worker-selftest.json` is
deliberately absent because the requested proof phase is not genuinely
complete.

## Failed Gate And Retry

The first failed gate is
`S56-5.1-EXACT-TARGET-CONSISTENCY / M1200-S-BOUNDARIES`. The invalid/open root
cut is `M1200-S-BOUNDARIES`, `M1200-C-TEST`, and `M1200-ROOT`. The tracked
registry remains open at M4; this recheck proposes H5/M5 blocker evidence
without altering predecessor state. The prerequisite obligation-tree item is
still provisional rather than master-accepted.

Retry only after an authorized statement-phase repair replaces the analytic
outer `top` with smooth `infinity`, publishes a new statement fingerprint, and
freshly freezes and accepts the statement, anchor audit, obligation registry,
and typed graphs in dependency order. Alternatively, explicitly redirect the
item to the checked counterexample target.

## Validation

All credited checks ran in this worker clone against the existing canonical
pinned sources and compiled artifacts. No `lake update`, `lake build`,
dependency clone/fetch, network action, or other `.lake` mutation command was
run. Lean output was confined to fresh directories under `/tmp` and removed
after each check. The automation-provided untracked `.lake` symlink makes this
nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1200` | 0 | Rank 394; lifecycle `planned`; baseline `L0/rework_required`; legacy artifacts unaccepted; theorem incomplete. |
| `git status --short` before this report | 0 | Only the automation-provided `?? Formalizations/Lean/.lake` symlink was present; the owned target path was clean. |
| `python3 Stage1_Instances/THM-M-1200/check_obligation_tree.py` | 0 | `PASS`: 14 obligations and 54 typed edges; denominator `9915c4444fa19015a1a5aa3413871c87dafe1aeafb0ef4ab8540cacc01c54931`; root and nonzero-trace construction open at M4. |
| Isolated pinned `lake env lean --trust=0` replays | 0 | The exact statement, checked refutation, and conditional composition elaborated. The countermodel and composition declarations reported axioms exactly `[propext, Classical.choice, Quot.sound]`. |
| `rg -n --pcre2 '\\b(?:sorry|admit|sorryAx|native_decide)\\b|^[[:space:]]*(?:axiom|unsafe|external)[[:space:]]' Stage1_Instances/THM-M-1200 --glob '*.lean'` | 1 | Expected no-match result: no prohibited Lean declaration token occurs in the owned Lean sources. |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release; Lake `5.0.0-src+98dc76e`. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`. |
| `python3 -m json.tool`, structured invariant checks, and SHA-256 assertions on the companion blocker JSON | 0 | Current-base identity, negative-result invariants, unchanged checked inputs, open-state fields, empty receipts, and deliberate self-test absence agree. |
| `git diff --check -- Stage1_Instances/THM-M-1200 .stage1-worker-selftest.json` plus new-file whitespace checks | 0 | No whitespace error in tracked or new owned artifacts. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The incomplete proof phase emitted no worker-completion packet. |

The isolated Lean recipe was:

```bash
set -eu
tmp=$(mktemp -d /tmp/thm-m-1200-slot59.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-1200/Statement.lean "$tmp/Statement.lean"
cp Stage1_Instances/THM-M-1200/Counterexample.lean "$tmp/Counterexample.lean"
cp Stage1_Instances/THM-M-1200/ObligationTree.lean "$tmp/ObligationTree.lean"
lean_bin=$(cd Formalizations/Lean && timeout 90 lake env which lean)
base_path=$(cd Formalizations/Lean && timeout 90 lake env printenv LEAN_PATH)
LEAN_PATH="$base_path" LEAN_NUM_THREADS=1 timeout 600 "$lean_bin" \
  --trust=0 -R "$tmp" -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_PATH="$tmp:$base_path" LEAN_NUM_THREADS=1 timeout 600 "$lean_bin" \
  --trust=0 -R "$tmp" "$tmp/Counterexample.lean"
LEAN_PATH="$tmp:$base_path" LEAN_NUM_THREADS=1 timeout 600 "$lean_bin" \
  --trust=0 -R "$tmp" "$tmp/ObligationTree.lean"
```

Checked input SHA-256 values:

| Input | SHA-256 |
|---|---|
| `Statement.lean` | `8e1650b86f9f8ab1917c326d938859bace727cf445182d3ae614d2eb48ae5ee7` |
| `Counterexample.lean` | `532c2f0d11e2a5b547b6bf55da3b5feee6a0ecb1bf2c5f32ad337abdfced4d95` |
| `ObligationTree.lean` | `c4eef89fd1e79a37b1733724709162544057743ff0b37f25716c2b1273c71598` |
| `obligation-registry.json` | `88f89866d3780610b8992be9d65651b3d922871fe6a571cfe957fa1e2fed2b91` |
| `typed-graphs.json` | `079f92a507df6b0330c3cdcc5629037db719e6d8b53fd674933a7429430717dc` |
| `anchor-audit.json` | `7ea5d8d3ccc31b3268381917ecd7d47ac2187c30edacf732c9acd17f8c0f402c` |
| `Formalizations/Lean/lake-manifest.json` | `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81` |
| `Formalizations/Lean/lean-toolchain` | `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2` |

This is durable blocker evidence, not a proof receipt. It changes no Lean
source, frozen predecessor artifact, scheduler authority, dependency artifact,
or unrelated target.
