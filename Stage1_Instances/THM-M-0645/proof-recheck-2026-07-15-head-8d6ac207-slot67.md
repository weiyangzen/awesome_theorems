# THM-M-0645 Proof-Phase Recheck

## Verdict

`S56-M-0645-PROOF` remains **blocked** at source revision
`8d6ac2078d37dc107d80c38c020de01c6f9affce` (tree
`a9332226f35fa562b7dbbe9feab5f5a2da80d013`). No positive proof body was added,
no obligation was closed, and no worker self-test manifest was written.

The exact frozen target is false. `Provable` specializes `Derivation` to
`alpha := Empty`, but `Derivation.allIntro` requires an explicit eigenvariable
`x : alpha`. Consequently a closed derivation cannot introduce a universal
quantifier. `Counterexample.lean` proves the exact negation

```lean
Stage1Instances.THM_M_0645.not_completenessTarget :
  Not Stage1Instances.THM_M_0645.CompletenessTarget
```

using the valid symbol-free sentence `forall x, x = x`. This refutes only the
custom calculus and target frozen in `Statement.lean`; it does not refute
Goedel's mathematical completeness theorem.

`Proof.lean` contains checked conditional composition through
`CountermodelProperty`, but supplies no inhabitant of that premise. Since the
opposite of the requested root is kernel checked, filling the positive root
would require an inconsistency, a placeholder, an unauthorized statement
change, or another prohibited proof device.

The current-base source fingerprints are:

| Source | SHA-256 |
|---|---|
| `Statement.lean` | `cda4391afd39e771c67afa1f235a6088c6cd3e33c8d507ebdcc96a7b0ebf78ee` |
| `ObligationTree.lean` | `0efca597afbd578a8802ab95c43b5abecfc80cd4462db4d900c4169ae89b2f06` |
| `Proof.lean` | `915966ace314adb06364d50f98faa7e60fa7bf6af379992d0760533bba760822` |
| `Counterexample.lean` | `31462210a7e30d89b3a2e11c9e8c8458778cf1e2d11d935a25edd3a77b7dceb6` |

## Current-Base Validation

Preflight and structural checks:

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0645` | 0 | rank 691; planned; L0/rework-required; theorem incomplete |
| `cd Formalizations/Lean && env -u LEAN_PATH lake env lean --version` | 1 | shared `flt-regular` checkout could not resolve `HEAD`; no fetch, build, update, clone, or repair was attempted |
| `python3 Stage1_Instances/THM-M-0645/check_statement.py` | 1 | same missing shared `flt-regular` artifact, before target elaboration |
| `python3 Stage1_Instances/THM-M-0645/check_obligation_tree.py` | 0 | 15 obligations and 43 typed edges passed; predecessor root remains open M4 |
| `python3 Stage1_Instances/THM-M-0645/check_anchor_audit.py` | 0 | pinned mathlib revision and receipt hash passed |
| JSON parse, receipt-invariant assertions, and whitespace checks | 0 | fresh JSON parsed; item/base/verdict/state/path boundaries matched; no whitespace errors |
| scoped `git status` and `test ! -e .stage1-worker-selftest.json` | 0 | only the two fresh target-owned reports were added by this worker; completion manifest is absent |

After the required `lake env lean` route failed, the following narrow fallback
used the executable pinned by `lean-toolchain` and only already-existing
compiled dependency directories. It excluded the project build directory to
avoid unrelated top-level module collisions and wrote all new `.olean` files
under a fresh temporary directory.

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
tmp=$(mktemp -d /tmp/thm-m-0645-slot67.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp "$target"/{Statement,ObligationTree,Proof,Counterexample}.lean "$tmp"/
for mod in Statement ObligationTree Proof Counterexample; do
  LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 "$lean" \
    --trust=0 -t0 -R "$tmp" -o "$tmp/$mod.olean" "$tmp/$mod.lean" \
    >"$tmp/$mod.out" 2>&1
done
```

All four modules exited 0. A comment-stripped source scan found none of
`sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, `unsafe`, `extern`,
`implemented_by`, or `native_decide`. Output scans found no error or sorry
diagnostic. `#print axioms` reported only `propext`, `Classical.choice`, and
`Quot.sound` for the exact negation and the other checked declarations.

| Artifact | SHA-256 |
|---|---|
| `Statement.olean` | `25eb67ade92875261cb4dafa5ae9075c3fe28e1e657ac763d2b7624430e04024` |
| `ObligationTree.olean` | `6c98e1bb9243a0930eae92822ff4d7a1043165662164476f7c47f7b0894bc614` |
| `Proof.olean` | `7c54139cf4e0d1fc38e44d2f6c1cca225e2fd83bd46dc35daa60ab86b344e7ce` |
| `Counterexample.olean` | `8dcfbde337211b11b3eb525b6f3cc2a5a191f3abfd60fc7d312725382d300c32` |
| `Proof` output | `bfd3e14def163e4418a27cd1c1890dbe8e26ff0cf2c2589ff3631541c48b5e2b` |
| `Counterexample` output | `80fb95cd6ab7948cfd7822889b590175b38af7d6180dd61103cbc634e37f48c1` |

The fallback used Lean 4.29.0 commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, executable SHA-256
`3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf`,
and pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`
(tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`). This is narrow,
nonrelease blocker evidence, not a replacement for the unavailable pinned Lake
route or any rev-5.6 release gate.

## First Failed Gate

Exact-target truth and consistency at `M0645-D-CALCULUS`: the frozen
universal-introduction rule is unusable for closed derivations, and the exact
positive root is kernel-refuted.

Positive proof work can resume only after an authorized statement-phase repair
provides a source-faithful eigenvariable or context-extension rule, derives the
quantified equality boundary, accepts a new statement fingerprint, and
regenerates every downstream obligation and graph artifact in dependency order.

This report changes no scheduler state and claims no proof completion, audit
completion, validation, release, theorem completion, receipt acceptance, or
master acceptance.
