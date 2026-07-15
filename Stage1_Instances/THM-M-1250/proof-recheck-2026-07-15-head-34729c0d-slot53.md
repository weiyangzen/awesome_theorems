# THM-M-1250 proof-phase recheck at current base

Item: `S56-M-1250-PROOF`

Date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `34729c0dff13ac1d1a2781d9c1ea4bf7c6a35398`

Base tree: `dde7f823b850641fc7dade0380327b6ac013ac07`

## Verdict

`blocked`. The exact frozen target is false, so no legal positive proof body
can inhabit it. `Counterexample.lean` adds the placeholder-free declaration

```text
Stage1Instances.THM_M_1250.Counterexample.not_schwartzSpaceCharacterization :
  Not Stage1Instances.THM_M_1250.SchwartzSpaceCharacterization
```

The frozen `IsSchwartzFunction` writes `ContDiff Real top` without fixing the
order type. It therefore elaborates as the analytic order `omega`, not the
infinitely differentiable order `infinity` used by `SchwartzMap.smooth'`.
The counterexample constructs a nonzero compactly supported smooth real bump
on `Fin 1 -> Real`, maps it into `Complex`, and bundles it with
`HasCompactSupport.toSchwartzMap`. If the frozen characterization held, that
function would be analytic. Analytic uniqueness and compact support would then
force it to be zero, contradicting its value `1` at the origin.

This refutes only the erroneous frozen analytic characterization, not the
classical Schwartz-space characterization with smooth order `infinity`.
Correcting the statement during the proof item would substitute a different
theorem. The earlier `ProofBlocker.lean` reverse-package theorem remains valid
partial work, but no forward package or positive root proof exists.

The prerequisite `S56-M-1250-OBLIGATION_TREE` remains provisional `[_]`, not
master-accepted `[x]`. Independently, its positive graph is invalidated as a
proof route because `M1250-F-SMOOTH` claims the non-existent projection from
smooth order `infinity` to analytic order `omega`. No proof receipt, state
transition, audit completion, validation, release, or theorem completion is
claimed.

## Validation

No `lake update`, `lake build`, dependency clone/fetch/checkout, network
action, or `.lake` repair was performed. The required root-project command was
attempted first:

```text
cd Formalizations/Lean &&
lake env lean --trust=0 ../../Stage1_Instances/THM-M-1250/ProofBlocker.lean
```

It exited `1` before Lean started because the pre-existing pinned
`flt-regular` checkout cannot resolve `HEAD`. The automation-provided `.lake`
symlink was left untouched.

The smallest available real corroboration used `lake env lean` from the
intact pinned mathlib subproject. `LEAN_PATH` was assembled read-only from the
eight existing package build directories; `Statement.lean` and
`Counterexample.lean` were copied into a fresh temporary directory under
`Formalizations/Lean`, elaborated at trust level zero, and removed. The exact
recipe was:

```bash
set -u
root=$PWD
target=$root/Stage1_Instances/THM-M-1250
lean_root=$root/Formalizations/Lean
mathlib=$lean_root/.lake/packages/mathlib
lean_path=$(find -L "$lean_root/.lake/packages" \
  -path '*/.lake/build/lib/lean' -type d -print | sort | paste -sd:)
tmp=$(mktemp -d "$lean_root/.thm-m-1250-proof-34729c0d-slot53.XXXXXX")
trap 'rm -rf "$tmp"' EXIT
cp "$target/Statement.lean" "$tmp/Statement.lean"
cp "$target/Counterexample.lean" "$tmp/Counterexample.lean"
(
  cd "$mathlib"
  LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 300 \
    lake env lean --root="$lean_root" --trust=0 -t0 \
      -o "$tmp/Statement.olean" "$tmp/Statement.lean" \
      >"$tmp/statement.log" 2>&1
  LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 \
    lake env lean --root="$lean_root" --trust=0 -t0 \
      "$tmp/Counterexample.lean" >"$tmp/counterexample.log" 2>&1
  cat "$tmp/counterexample.log"
)
```

It exited `0`. The exact refutation and its analytic-support lemma both
reported axioms `[propext, Classical.choice, Quot.sound]`, with no `sorryAx`.
The fresh `Statement.olean` SHA-256 was
`768c685c215d1d65c564c5ff20053d328cbc83c9cf43e8ad2d0fdf4464ad96b9`;
the statement and countertheorem output SHA-256 values were respectively
`2f7f47d31193d167181eab4606af44bc6d2ad6f1eac751581414659b479f5faa`
and `478b93b48893d7ff76281bafdb7c20ee9464a9758d85b4081a5fc788c5d67ed4`.
The pinned environment was Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, and mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). This is current negative
kernel evidence, but the broken root Lake environment and untracked cache
symlink make it nonrelease evidence rather than a proof-completion receipt.

Other exact outcomes:

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1250` | 0 | Rank 430; lifecycle planned; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1250/check_obligation_tree.py` | 0 | 15 obligations and 30 typed edges passed structurally; positive root remains open. |
| Prohibited-construct scan over owned Lean files | 1, expected | No `sorry`, `admit`, `sorryAx`, `native_decide`, `implemented_by`, declared axiom, unsafe, opaque, extern, or constant. |
| `test ! -e .stage1-worker-selftest.json` | 0 | No completion manifest exists. |

## Retry Condition

The first failed gate is exact canonical statement correctness at
`M1250-F-SMOOTH`. Reopen `S56-M-1250-STATEMENT`, replace the ambiguous order
with `((top : ENat) : WithTop ENat)` (the scoped `infinity` order), rerun
expression identity and mutation tests, and publish a versioned anchor audit,
obligation registry, and typed-graph delta for the corrected fingerprint.
Those prerequisites must then receive master acceptance before another proof
attempt. The pinned `flt-regular` checkout must also be restored without
fetching a moving revision before required root-project validation.

The remaining workflow cut set is `S56-M-1250-STATEMENT`. Because this
positive proof phase is blocked rather than self-tested complete,
`.stage1-worker-selftest.json` is deliberately absent and the item remains
`[ ]`.
