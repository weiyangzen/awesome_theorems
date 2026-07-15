# THM-M-0645 Proof-Phase Recheck

Item: `S56-M-0645-PROOF`

Intent: `prove`

Recorded at: `2026-07-15T18:19:01+08:00`

Base revision: `97cd9c492d95baa9b55d2d8b341844107f07e686`

Base tree: `bdd31de5f2fcd38078e4b5793b400a8105a3b8ba`

## Verdict

`blocked`. No positive proof body can truthfully close the exact frozen target because the
placeholder-free module `Counterexample.lean` kernel-checks

```text
Stage1Instances.THM_M_0645.not_completenessTarget :
  Not Stage1Instances.THM_M_0645.CompletenessTarget
```

The defect is in the frozen custom calculus, not Goedel's mathematical completeness theorem.
`Provable` specializes `Derivation`'s free-variable type to `Empty`, while
`Derivation.allIntro` requires an explicit eigenvariable `x : alpha`. Universal introduction is
therefore impossible in a closed derivation. A structural induction over every constructor proves
that closed derivations preserve `proofInvariant`, under which every universal formula is false.
The universe-polymorphic symbol-free sentence `forall x, x = x` is nevertheless valid in every
nonempty structure, violates the invariant, and is not provable. Instantiating the exact root with
that language and sentence gives the checked negation above.

The existing `Proof.lean` declarations are real but conditional. `builder_of_countermodel` requires
an explicit `CountermodelProperty` premise, and `completenessTarget_of_countermodel` merely composes
that conditional result with the frozen root wrapper. Neither declaration constructs the premise
or closes the positive root. A pinned mathlib or external completeness theorem cannot transport to
this false target in a consistent environment.

The first failed gate is exact-target truth and consistency at `M0645-D-CALCULUS`, before Henkin or
term-model proof execution. The proof item remains `[ ]`, the lifecycle remains `planned`, and the
authoritative root vector remains `[H2, M4, R4]`; this recheck only confirms an `M5` proof-phase
diagnosis. No obligation, receipt, audit, validation, release, theorem completion, or master
acceptance is claimed. Because the assigned positive proof phase is incomplete,
`.stage1-worker-selftest.json` is deliberately absent.

The scheduler projects the four predecessors as worker-self-tested `[_]`, not master-accepted
`[x]`. The target-local registry still reports an `M4` root with `M0645-T-CLASSICAL` as its cut set
because it predates the refutation. Neither projection supplies proof credit; this proof worker does
not rewrite predecessor state.

## Current-Base Validation

All checks ran inside this worker clone. The automation-provided `.lake` symlink and existing pinned
packages were reused read-only. No update, build, clone, fetch, network operation, or `.lake`
mutation was performed. The four Lean sources and all generated outputs were copied to disposable
`/tmp` directories and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets at ranks 1 through 1546 and the uniform L0/rework-required baseline passed. |
| `python3 scripts/stage1_target.py show THM-M-0645` | 0 | Rank 691; planned `hard_statement_first_partial_verification` lane; theorem incomplete. |
| `cd Formalizations/Lean && timeout --foreground --kill-after=5s 30s env -u LEAN_PATH lake env lean --version` | 0 | Lean 4.29.0 at commit `98dc76e3...ab16740`. |
| `timeout --foreground --kill-after=5s 300s python3 Stage1_Instances/THM-M-0645/check_statement.py` | 0 | All four statement mutations were killed; canonical expression hash and pinned mathlib revision matched. |
| Initial isolated replay wrapper plus an inapplicable `rg -F` declaration-type assertion | 1 | All four Lean modules elaborated, but the assertion expected a type line not emitted by the source's `#print axioms` commands; no evidence is credited to this wrapper. |
| Corrected isolated four-module `lake env lean --trust=0 -t0` replay below | 0 | `Statement`, `ObligationTree`, `Proof`, and `Counterexample` elaborated in dependency order. |
| Comment-stripped proof-device and diagnostic scan in that replay | 0 | No prohibited proof device or `sorryAx`; audited axiom sets use only `propext`, `Classical.choice`, and `Quot.sound`. |
| `python3 Stage1_Instances/THM-M-0645/check_obligation_tree.py` | 0 | 15 obligations and 43 typed edges passed; denominator `ade5c7f4...7fc01`; predecessor root remains open M4. |
| `python3 Stage1_Instances/THM-M-0645/check_anchor_audit.py` | 0 | Anchor receipt `d61ebc24...1506` and pinned mathlib revision passed. |
| Two independent read-only audits/replays | 0 | Both identified the `Empty` eigenvariable defect and independently elaborated the exact negation in the pinned environment. |
| Structured JSON, source-hash, and fail-closed assertions | 0 | The blocker record parsed; all frozen source hashes matched; verdict/state remained `blocked`/`[ ]`; all completion fields remained false. |
| `git diff --check -- Stage1_Instances/THM-M-0645` plus new-file whitespace scan | 0 | No whitespace errors. |
| `test ! -e .stage1-worker-selftest.json` | 0 | No completion self-test manifest exists. |

Exact successful replay command from the worker root:

```bash
set -euo pipefail
root=$PWD
target=$root/Stage1_Instances/THM-M-0645
lean_dir=$root/Formalizations/Lean
tmp=$(mktemp -d /tmp/thm-m-0645-head97cd9c49-slot50.XXXXXX)
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
  "$tmp"/{Proof,Counterexample}.out
```

| Artifact | SHA-256 |
|---|---|
| `Statement.olean` | `25eb67ade92875261cb4dafa5ae9075c3fe28e1e657ac763d2b7624430e04024` |
| `ObligationTree.olean` | `6c98e1bb9243a0930eae92822ff4d7a1043165662164476f7c47f7b0894bc614` |
| `Proof.olean` | `7c54139cf4e0d1fc38e44d2f6c1cca225e2fd83bd46dc35daa60ab86b344e7ce` |
| `Counterexample.olean` | `8dcfbde337211b11b3eb525b6f3cc2a5a191f3abfd60fc7d312725382d300c32` |
| `Proof` output | `bfd3e14def163e4418a27cd1c1890dbe8e26ff0cf2c2589ff3631541c48b5e2b` |
| `Counterexample` output | `80fb95cd6ab7948cfd7822889b590175b38af7d6180dd61103cbc634e37f48c1` |

The environment used pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). `#print axioms` reported exactly
`propext`, `Classical.choice`, and `Quot.sound` for `not_completenessTarget`.

## Retry Condition

Positive proof work may resume only after an authorized statement-phase repair replaces the
unusable universal-introduction interface with a source-faithful eigenvariable or context-extension
rule. The repaired calculus must derive the quantified empty-language equality boundary. The
integration lane must then accept a new statement fingerprint, publish an append-only obligation
registry delta, and rerun statement mutation testing, anchor audit, obligation-tree construction,
and proof execution in dependency order.

This current-base evidence changes no scheduler state and does not satisfy
`S56-M-0645-PROOF`.
