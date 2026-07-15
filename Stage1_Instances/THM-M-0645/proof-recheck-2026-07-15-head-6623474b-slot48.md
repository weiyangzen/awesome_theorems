# THM-M-0645 Proof-Phase Recheck

Item: `S56-M-0645-PROOF`

Intent: `prove`

Recorded at: `2026-07-15T21:29:55+08:00`

Base revision: `6623474b775e74ea6f20e717a65bac54d45ea927`

Base tree: `d0d9fd959333b17d754206b296df2250a4efee1e`

## Verdict

`blocked`. No positive proof body can truthfully close the exact frozen target. The existing
placeholder-free module `Counterexample.lean` kernel-checks

```text
Stage1Instances.THM_M_0645.not_completenessTarget :
  Not Stage1Instances.THM_M_0645.CompletenessTarget
```

This refutes only the target-local calculus, not Goedel's mathematical completeness theorem.
`Provable` specializes `Derivation`'s free-variable type to `Empty`, but `Derivation.allIntro`
requires an explicit eigenvariable `x : alpha`. Universal introduction is therefore impossible in
a closed derivation. `proofInvariant_of_derivation` covers every derivation constructor and shows
that every closed derivation satisfies an invariant under which universal formulas are false. The
closed symbol-free sentence `forall x, x = x` is nevertheless valid in every nonempty structure,
and `reflexivitySentence_not_provable` proves it is not derivable. The exact positive root is false.

`Proof.lean` has real but conditional proof bodies. `builder_of_countermodel` requires an explicit
`CountermodelProperty`, and `completenessTarget_of_countermodel` only composes that premise with the
frozen root wrapper. Neither declaration constructs the premise or closes the positive root.
Pinned mathlib contains semantics but no syntactic completeness result for this custom calculus.
The audited Foundation theorem at revision `87d4dd68835a6c1eb8448b9c392d9ca51fe08d63`
uses Lean 4.31 and a different proof system; it is anchor-only and cannot be transported
consistently to a kernel-refuted proposition.

The first failed gate is exact-target truth/consistency at `M0645-D-CALCULUS`. The assigned proof
item stays `[ ]`, the lifecycle stays `planned`, and the authoritative root vector stays
`[H2, M4, R4]`. This recheck records an `M5` proof-phase diagnosis without rewriting predecessor
authority. It closes no obligation and claims no audit, validation, release, theorem completion,
receipt, or master acceptance. The four predecessors are scheduler-projected `[_]`, not
master-accepted `[x]`. Because the requested positive proof phase is incomplete,
`.stage1-worker-selftest.json` is deliberately absent.

The semantic inputs are byte-identical to the prior slot48 recheck at base `c4715a2b`; the
intervening integration commit added only worker evidence files for several targets. This packet
nevertheless replays all narrow gates against the current immutable base rather than inheriting the
older run.

## Current-Base Validation

All commands ran inside this worker clone. The automation-provided `.lake` symlink and existing
pinned package artifacts were reused without `lake update`, `lake build`, clone, fetch, network
access, or dependency mutation. Lean sources and generated artifacts were copied to and removed
from a disposable `/tmp` directory.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets at ranks 1 through 1546 and the uniform L0/rework-required baseline passed. |
| `python3 scripts/stage1_target.py show THM-M-0645` | 0 | Rank 691; planned `hard_statement_first_partial_verification` lane; theorem incomplete. |
| `timeout --foreground --kill-after=5s 300s python3 Stage1_Instances/THM-M-0645/check_statement.py` | 0 | Canonical expression hash `76fbce83...7c7ea68` matched; all four structural mutations were distinguished; pinned toolchain and mathlib matched. |
| Isolated four-module `lake env lean --trust=0 -t0` replay below | 0 | `Statement`, `ObligationTree`, `Proof`, and `Counterexample` elaborated in dependency order. |
| Comment-stripped proof-device and Lean-diagnostic scans in that replay | 0 | No prohibited proof device or `sorryAx`; the exact negation uses only `propext`, `Classical.choice`, and `Quot.sound`. |
| `python3 Stage1_Instances/THM-M-0645/check_obligation_tree.py` | 0 | 15 obligations and 43 typed edges passed; denominator `ade5c7f4...7fc01`; predecessor root remains open M4. |
| `python3 Stage1_Instances/THM-M-0645/check_anchor_audit.py` | 0 | Anchor receipt `d61ebc24...1506` and pinned mathlib revision passed. |
| Three independent read-only reviews, including two independent trust-zero replays and repo/mathlib analog searches | 0 | All confirmed the `Empty` eigenvariable defect, exact negation, and impossibility of exact positive closure. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest is absent as required. |

Exact successful replay command from the worker root:

```bash
set -euo pipefail
root=$PWD
target=$root/Stage1_Instances/THM-M-0645
lean_dir=$root/Formalizations/Lean
tmp=$(mktemp -d /tmp/thm-m-0645-head6623474b-slot48.XXXXXX)
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
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). `#print axioms` reported exactly
`propext`, `Classical.choice`, and `Quot.sound` for `not_completenessTarget`.

## Retry Condition

Positive proof work may resume only after an authorized statement-phase repair replaces the
unusable universal-introduction interface with a source-faithful binder/context-extension rule.
The repaired calculus must derive the quantified empty-language equality boundary. The integration
lane must then accept a new statement fingerprint, publish an append-only obligation-registry delta,
and rerun statement mutation testing, anchor audit, obligation-tree construction, and proof
execution in dependency order.

This current-base evidence changes no scheduler state and does not satisfy
`S56-M-0645-PROOF`.
