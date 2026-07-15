# THM-M-0645 Proof-Phase Recheck

Item: `S56-M-0645-PROOF`

Intent: `prove`

Base revision: `57d8d01796f84ffc9de9adf1f5d0723555e7babb`

Base tree: `cdea5b3fad713816ee6c9ed6aae7a10f9009a18e`

## Verdict

`blocked`. No positive proof body was added, no obligation was closed, and no
`.stage1-worker-selftest.json` was written.

The exact frozen target is false. `Provable` specializes `Derivation` to
`alpha := Empty`, while `Derivation.allIntro` requires an explicit eigenvariable
`x : alpha`. Universal introduction is therefore impossible in a closed sentence derivation.
`Counterexample.lean` gives the placeholder-free exact countertheorem

```lean
Stage1Instances.THM_M_0645.not_completenessTarget :
  Not Stage1Instances.THM_M_0645.CompletenessTarget
```

It uses the universe-polymorphic symbol-free sentence `forall x, x = x`, proves that sentence
valid in every nonempty structure, and proves it nonderivable by induction on the frozen
derivation calculus. This refutes only the custom calculus and target in `Statement.lean`, not
Goedel's mathematical completeness theorem.

`Proof.lean` contains real conditional bodies for classical contraposition and exact-root
composition, but both depend on an explicit `CountermodelProperty` premise. They neither inhabit
that premise nor close the positive root. Adding an unconditional positive body while the exact
negation is checked would require inconsistency, a placeholder, a changed statement, or another
prohibited device.

## Narrow Validation

The required Lake route was attempted first and failed before elaboration:

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0645` | 0 | rank 691; planned; L0/rework-required; theorem incomplete |
| `cd Formalizations/Lean && timeout --foreground --kill-after=5s 30s env -u LEAN_PATH lake env lean --version` | 1 | shared `flt-regular` checkout could not resolve `HEAD`; no fetch, update, build, clone, removal, or repair was attempted |
| `timeout --foreground --kill-after=5s 30s python3 Stage1_Instances/THM-M-0645/check_statement.py` | 1 | same missing shared artifact before target elaboration |
| `python3 Stage1_Instances/THM-M-0645/check_obligation_tree.py` | 0 | 15 obligations and 43 typed edges passed; predecessor root remains open M4 |
| `python3 Stage1_Instances/THM-M-0645/check_anchor_audit.py` | 0 | pinned mathlib revision and anchor receipt passed |

After the required route failed, this narrow nonrelease fallback used the executable pinned by
`lean-toolchain` and only already-existing compiled dependencies. All generated files were confined
to a fresh temporary directory and removed:

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
tmp=$(mktemp -d /tmp/thm-m-0645-proof-57d8d017-slot67.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp "$target"/{Statement,ObligationTree,Proof,Counterexample}.lean "$tmp"/
for mod in Statement ObligationTree Proof Counterexample; do
  LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
    timeout --foreground --kill-after=10s 300s "$lean" \
    --trust=0 -t0 -R "$tmp" -o "$tmp/$mod.olean" "$tmp/$mod.lean" \
    >"$tmp/$mod.out" 2>&1
done
```

All four modules exited 0. A comment-stripped scan found none of `sorry`, `admit`, `sorryAx`,
`axiom`, `constant`, `opaque`, `unsafe`, `extern`, `implemented_by`, or `native_decide`.
Output checks found no error or sorry diagnostic. Axiom sets for the conditional proof bodies and
countertheorem declarations were subsets of `propext`, `Classical.choice`, and `Quot.sound`.

| Artifact | SHA-256 |
|---|---|
| `Statement.olean` | `25eb67ade92875261cb4dafa5ae9075c3fe28e1e657ac763d2b7624430e04024` |
| `ObligationTree.olean` | `6c98e1bb9243a0930eae92822ff4d7a1043165662164476f7c47f7b0894bc614` |
| `Proof.olean` | `7c54139cf4e0d1fc38e44d2f6c1cca225e2fd83bd46dc35daa60ab86b344e7ce` |
| `Counterexample.olean` | `8dcfbde337211b11b3eb525b6f3cc2a5a191f3abfd60fc7d312725382d300c32` |
| `Proof` output | `bfd3e14def163e4418a27cd1c1890dbe8e26ff0cf2c2589ff3631541c48b5e2b` |
| `Counterexample` output | `80fb95cd6ab7948cfd7822889b590175b38af7d6180dd61103cbc634e37f48c1` |

Lean reported version 4.29.0 at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; the executable hash was
`3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf`. The reused mathlib
checkout was pinned at `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`.

## First Failed Gate

Exact-target truth and consistency at `M0645-D-CALCULUS`: the frozen universal-introduction rule
is unusable for closed derivations, and the exact positive root is kernel-refuted.

Positive proof work can resume only after an authorized statement-phase repair makes universal
introduction usable for closed sentences, derives the quantified equality boundary, accepts a new
statement fingerprint, and regenerates every downstream obligation and graph artifact in
dependency order.

This report changes no scheduler state and claims no proof completion, audit completion,
validation, release, theorem completion, receipt acceptance, or master acceptance.
