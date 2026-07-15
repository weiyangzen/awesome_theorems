# Proof blocker recheck at current base

Item: `S56-M-0645-PROOF`

Theorem: `THM-M-0645`

Intent: `prove`

Verdict: `blocked`

Base revision: `87ffd1cab865c5d4e1f6828412182c2069c87fde`

Base tree: `1e71f8f4783308aa84ff239895dc79aa41cdffcc`

## Exact blocker

The assigned positive proof cannot be implemented truthfully for the frozen target. In
`Statement.lean`, `Provable` specializes `Derivation`'s free-variable type to `Empty`, while
`Derivation.allIntro` requires an explicit eigenvariable of that type. Universal introduction is
therefore unusable in every closed derivation.

`Counterexample.lean` gives a real, placeholder-free kernel refutation of the exact target. It
proves that every derivable sentence satisfies `proofInvariant`, in which every universal formula
is false, and then exhibits the symbol-free sentence `forall x, x = x`: the sentence is valid in
every nonempty structure but is not derivable. The exported declaration has exact type

```text
Stage1Instances.THM_M_0645.not_completenessTarget :
  Not Stage1Instances.THM_M_0645.CompletenessTarget
```

`Proof.lean` contains genuine conditional proof bodies, but they retain
`CountermodelProperty` as an explicit premise and do not construct it. They cannot close a target
whose negation is kernel checked. Pinned mathlib has no syntactic completeness proof for this
custom calculus, and the audited external Foundation result uses a different calculus and
toolchain; it cannot consistently be transported to the refuted target.

The first failed gate is exact-target truth and calculus consistency at `M0645-D-CALCULUS`. The
proof-phase diagnosis is `M5`, but this worker does not rewrite predecessor statement, registry,
graph, task, or debt authority. The item remains `[ ]`; no obligation, accepted receipt, audit,
validation, release, theorem completion, or master acceptance is claimed. Because the requested
positive proof phase is not complete, `.stage1-worker-selftest.json` is deliberately absent.

## Current-base validation

All commands ran in the worker clone. The automation-provided `.lake` symlink and existing pinned
package artifacts were reused without `lake update`, `lake build`, clone, fetch, network access,
or dependency mutation. Lean sources and outputs lived only in a disposable `/tmp` directory and
were deleted on exit.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets and the uniform L0/rework-required baseline passed. |
| `python3 scripts/stage1_target.py show THM-M-0645` | 0 | Rank 691, planned lifecycle, theorem incomplete. |
| `timeout --foreground --kill-after=5s 300s python3 Stage1_Instances/THM-M-0645/check_statement.py` | 0 | Expression hash `76fbce83...7c7ea68` matched and all four structural mutations were distinguished. |
| Isolated four-module `lake env lean --trust=0 -t0` replay below | 0 | `Statement`, `ObligationTree`, `Proof`, and `Counterexample` elaborated in dependency order. |
| Comment-stripped proof-device and Lean-diagnostic scans | 0 | No prohibited proof device and no `sorryAx`; the exact negation uses only `propext`, `Classical.choice`, and `Quot.sound`. |
| `python3 Stage1_Instances/THM-M-0645/check_obligation_tree.py` | 0 | 15 obligations and 43 typed edges passed; the predecessor registry remains open at M4. |
| `python3 Stage1_Instances/THM-M-0645/check_anchor_audit.py` | 0 | Anchor receipt `d61ebc24...1506` and pinned mathlib revision passed. |
| Three independent read-only reviews | 0 | All confirmed the `Empty` eigenvariable defect and exact kernel-checked negation; one also checked an independent importing consumer. |
| `git diff --quiet feeafa8d...87ffd1ca --` followed by the nine semantic target paths | 0 | The current semantic inputs are byte-identical to the preceding slot48 recheck base. |
| `python3 -m json.tool Stage1_Instances/THM-M-0645/proof-recheck-2026-07-15-head-87ffd1ca-slot48.json` | 0 | The structured blocker packet parsed successfully. |
| No-diagnostic `git diff --no-index --check /dev/null <artifact>` loop; `test ! -e .stage1-worker-selftest.json` | 0 | Both new artifacts have no whitespace errors and the prohibited success manifest is absent. |

Exact successful replay command:

```bash
set -euo pipefail
root=$PWD
target=$root/Stage1_Instances/THM-M-0645
lean_dir=$root/Formalizations/Lean
tmp=$(mktemp -d /tmp/thm-m-0645-head87ffd1ca-slot48.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp "$target"/{Statement,ObligationTree,Proof,Counterexample}.lean "$tmp"/
base_path=$(cd "$lean_dir" && {
  for path in .lake/packages/*/.lake/build/lib/lean; do
    test -d "$path" && realpath "$path"
  done
  lean=$(env -u LEAN_PATH lake env which lean)
  realpath "$(dirname "$(dirname "$lean")")/lib/lean"
} | paste -sd:)
for mod in Statement ObligationTree Proof Counterexample; do
  (
    cd "$lean_dir"
    LEAN_NUM_THREADS=1 timeout --foreground --kill-after=5s 300s \
      env -u LEAN_PATH lake env env LEAN_PATH="$tmp:$base_path" \
      lean --trust=0 -t0 -R "$tmp" -o "$tmp/$mod.olean" "$tmp/$mod.lean"
  ) >"$tmp/$mod.out" 2>&1
done
for source in "$tmp"/{Statement,ObligationTree,Proof,Counterexample}.lean; do
  perl -0777 -pe 's!/\-.*?\-/!!gs; s/--[^\n]*//g' "$source"
done >"$tmp/scoped-stripped.lean"
! rg -n '\b(sorry|admit|sorryAx|axiom|constant|opaque|unsafe|extern|implemented_by|native_decide)\b' \
  "$tmp/scoped-stripped.lean"
! rg -n 'declaration uses .sorry|sorryAx' "$tmp"/*.out
rg -F "'Stage1Instances.THM_M_0645.not_completenessTarget' depends on axioms: [propext, Classical.choice, Quot.sound]" \
  "$tmp/Counterexample.out"
rg -F 'Stage1Instances.THM_M_0645.completenessTarget_of_countermodel' "$tmp/Proof.out"
sha256sum "$tmp"/{Statement,ObligationTree,Proof,Counterexample}.olean \
  "$tmp"/{Statement,ObligationTree,Proof,Counterexample}.out
```

| Artifact | SHA-256 |
|---|---|
| `Statement.olean` | `25eb67ade92875261cb4dafa5ae9075c3fe28e1e657ac763d2b7624430e04024` |
| `ObligationTree.olean` | `6c98e1bb9243a0930eae92822ff4d7a1043165662164476f7c47f7b0894bc614` |
| `Proof.olean` | `7c54139cf4e0d1fc38e44d2f6c1cca225e2fd83bd46dc35daa60ab86b344e7ce` |
| `Counterexample.olean` | `8dcfbde337211b11b3eb525b6f3cc2a5a191f3abfd60fc7d312725382d300c32` |
| `Statement` output | `80b80b2744011d9ae27ea98f08ab5102c3cd0ed979091ae7b7adba4179c88e37` |
| `ObligationTree` output | `ac9cf82f5caed589ebd1d642f3860f4fd0e4ecd2adf07afcf36d603e6f363357` |
| `Proof` output | `bfd3e14def163e4418a27cd1c1890dbe8e26ff0cf2c2589ff3631541c48b5e2b` |
| `Counterexample` output | `80fb95cd6ab7948cfd7822889b590175b38af7d6180dd61103cbc634e37f48c1` |

The replay used Lean 4.29.0 commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740` and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`).

## Retry condition

Positive proof work can resume only after an authorized statement-phase repair replaces the
unusable universal-introduction interface with a source-faithful rule that works for closed
sentences and derives the quantified equality boundary. The integration lane must accept the new
statement fingerprint, publish an append-only obligation-registry delta, and rerun statement,
anchor-audit, obligation-tree, and proof phases in dependency order.

This evidence changes no scheduler state and does not satisfy `S56-M-0645-PROOF`.
