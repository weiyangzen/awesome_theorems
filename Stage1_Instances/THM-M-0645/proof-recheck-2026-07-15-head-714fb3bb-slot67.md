# THM-M-0645 Proof-Phase Recheck

Item: `S56-M-0645-PROOF`

Intent: `prove`

Recheck date: `2026-07-15T13:39:58+08:00`

Base revision: `714fb3bb6a070c2f659ece069f1a7219f9c045a0`

Base tree: `2c99a78c5fa247aebc885f31e6818fc029f17a60`

## Verdict

`blocked`. No positive proof body can truthfully close the exact frozen target because its
negation is already kernel checked. `Counterexample.lean` proves, without placeholders,

```text
Stage1Instances.THM_M_0645.not_completenessTarget :
  Not Stage1Instances.THM_M_0645.CompletenessTarget
```

`Provable` specializes `Derivation` to the free-variable type `Empty`, while
`Derivation.allIntro` requires an explicit eigenvariable `x : alpha`. Universal introduction is
therefore impossible in a closed derivation. A structural invariant proves that every remaining
constructor preserves a syntactic interpretation in which universal formulas are false. The
symbol-free sentence `forall x, x = x` is semantically valid, violates that invariant, and is not
provable. Instantiating the exact root with this language and sentence yields the checked negation.

This diagnoses only the defective custom calculus and target frozen in `Statement.lean`. It does
not refute Goedel's mathematical completeness theorem. The proof node remains `[ ]`, the root is
not closed, and no `.stage1-worker-selftest.json` is written.

## Proof Boundary

The existing `Proof.lean` bodies are real but conditional. `builder_of_countermodel` converts an
explicit `CountermodelProperty` premise into `CompletenessDerivationBuilder`, and
`completenessTarget_of_countermodel` composes it with the exact-root wrapper. Neither declaration
inhabits `CountermodelProperty`; both are consistent with the checked negation and supply no
positive root closure.

The first failed gate is exact-target truth/consistency at `M0645-D-CALCULUS`, before Henkin or
term-model proof execution. The predecessor graph retains its open `M4` state because this worker
does not rewrite earlier authority; the proof evidence diagnoses an `M5` statement/calculus
mismatch.

## Validation

Preflight and structural commands run from the worker root:

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0645` | 0 | rank 691; planned; L0/rework-required; theorem incomplete |
| `cd Formalizations/Lean && env -u LEAN_PATH lake env lean --version` | 143 | the requested Lake route produced no output and was terminated while the shared incomplete `flt-regular` package triggered concurrent fetch attempts; this worker did not fetch, update, build, clone, repair, or otherwise mutate `.lake` |
| `python3 Stage1_Instances/THM-M-0645/check_obligation_tree.py` | 0 | 15 obligations and 43 typed edges passed; predecessor root remains open `M4` |
| `python3 Stage1_Instances/THM-M-0645/check_anchor_audit.py` | 0 | pinned mathlib revision and anchor receipt hash passed |

Because the Lake route was unavailable, a narrow nonrelease replay invoked the executable pinned
by `lean-toolchain` and used only already-existing compiled dependency directories. All outputs
were confined to a fresh `/tmp` directory and removed. The project build directory was excluded to
avoid unrelated top-level module collisions.

```bash
set -euo pipefail
root=$PWD
target=$root/Stage1_Instances/THM-M-0645
lake_root=$root/Formalizations/Lean/.lake
lean=$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean
paths=()
for p in "$lake_root"/packages/*/.lake/build/lib/lean; do
  test -d "$p" && paths+=("$p")
done
paths+=("$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/lib/lean")
lean_path=$(IFS=:; printf '%s' "${paths[*]}")
tmp=$(mktemp -d /tmp/thm-m-0645-head714fb3bb.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp "$target"/{Statement,ObligationTree,Proof,Counterexample}.lean "$tmp"/
for mod in Statement ObligationTree Proof Counterexample; do
  LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 "$lean" \
    --trust=0 -t0 -R "$tmp" -o "$tmp/$mod.olean" "$tmp/$mod.lean" \
    >"$tmp/$mod.out" 2>&1
done
```

`Statement`, `ObligationTree`, `Proof`, and `Counterexample` each exited 0 under `--trust=0`.
A comment-stripped scan found no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`,
`unsafe`, `extern`, `implemented_by`, or `native_decide` proof device. Output checks found no
error or sorry diagnostic. Every audited declaration had an axiom set contained in `propext`,
`Classical.choice`, and `Quot.sound`; `not_completenessTarget` used exactly those three.

| Artifact | SHA-256 |
|---|---|
| `Statement.olean` | `25eb67ade92875261cb4dafa5ae9075c3fe28e1e657ac763d2b7624430e04024` |
| `ObligationTree.olean` | `6c98e1bb9243a0930eae92822ff4d7a1043165662164476f7c47f7b0894bc614` |
| `Proof.olean` | `7c54139cf4e0d1fc38e44d2f6c1cca225e2fd83bd46dc35daa60ab86b344e7ce` |
| `Counterexample.olean` | `8dcfbde337211b11b3eb525b6f3cc2a5a191f3abfd60fc7d312725382d300c32` |
| `Proof` output | `bfd3e14def163e4418a27cd1c1890dbe8e26ff0cf2c2589ff3631541c48b5e2b` |
| `Counterexample` output | `80fb95cd6ab7948cfd7822889b590175b38af7d6180dd61103cbc634e37f48c1` |

The replay used Lean 4.29.0 commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, executable SHA-256
`3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). No dependency-manager mutation command was run.

## Retry Condition

Positive proof work may resume only after an authorized statement-phase repair replaces the
unusable universal-introduction interface with a source-faithful eigenvariable or context-extension
rule. The repaired calculus must derive the quantified empty-language equality boundary. The
integration lane must then accept a new statement fingerprint, publish an append-only registry
delta, and rerun statement mutation testing, anchor audit, obligation-tree construction, and proof
execution in dependency order.

This current-base report is negative nonrelease evidence only. It changes no scheduler state and
claims no proof completion, audit completion, validation, release, theorem completion, receipt
acceptance, or master acceptance.
