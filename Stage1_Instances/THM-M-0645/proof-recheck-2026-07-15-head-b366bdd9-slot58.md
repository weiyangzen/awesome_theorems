# THM-M-0645 Proof-Phase Recheck

Item: `S56-M-0645-PROOF`

Intent: `prove`

Recorded at: `2026-07-15T19:56:28+08:00`

Base revision: `b366bdd9f72217b5465ccd19133760b911ed0b58`

Base tree: `987b635fe76400c0818b485a6e5fc7a7067311e4`

## Verdict

`blocked`. A positive proof body cannot truthfully close the exact frozen target because the
placeholder-free module `Counterexample.lean` kernel-checks

```text
Stage1Instances.THM_M_0645.not_completenessTarget :
  Not Stage1Instances.THM_M_0645.CompletenessTarget
```

This refutes only the frozen custom calculus, not Goedel's mathematical completeness theorem.
`Provable` specializes `Derivation`'s free-variable type to `Empty`, while `Derivation.allIntro`
requires an explicit eigenvariable `x : alpha`. Universal introduction is therefore impossible in
a closed derivation. A structural induction proves that every closed derivation preserves
`proofInvariant`, where every universal formula is false. The closed symbol-free sentence
`forall x, x = x` is nevertheless valid in every nonempty structure and is not provable, so it
refutes the exact root.

`Proof.lean` contains real but conditional proof bodies. `builder_of_countermodel` requires an
explicit `CountermodelProperty` premise, and `completenessTarget_of_countermodel` composes that
conditional result with the exact-root wrapper. Neither declaration constructs the premise or
closes the positive root. The pinned mathlib revision has semantic compactness results, but no
syntactic validity-to-derivability theorem for this target-local calculus. An external theorem for a
different calculus cannot consistently transport to this kernel-refuted target.

The first failed gate is exact-target truth and consistency at `M0645-D-CALCULUS`. The proof item
remains `[ ]`, lifecycle remains `planned`, and the authoritative root vector remains
`[H2, M4, R4]`; this recheck records only an `M5` proof-phase diagnosis. It closes no obligation and
claims no audit, validation, release, theorem completion, receipt, or master acceptance. The four
predecessors are scheduler-projected `[_]`, not master-accepted `[x]`. Because the positive proof
deliverable is incomplete, `.stage1-worker-selftest.json` is deliberately absent.

## Current-Base Validation

All checks ran inside this worker clone. The automation-provided `.lake` symlink and existing pinned
packages were reused without `lake update`, `lake build`, clone, fetch, network access, or dependency
mutation. The four Lean sources and every generated Lean artifact were copied to a disposable
`/tmp` directory, replayed through `lake env lean`, and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets at ranks 1 through 1546 and the uniform L0/rework-required baseline passed. |
| `python3 scripts/stage1_target.py show THM-M-0645` | 0 | Rank 691; planned `hard_statement_first_partial_verification` lane; theorem incomplete. |
| `timeout --foreground --kill-after=5s 300s python3 Stage1_Instances/THM-M-0645/check_statement.py` | 0 | Canonical expression hash matched; all four structural mutations were distinguished; pinned toolchain and mathlib revision matched. |
| Isolated four-module `lake env lean --trust=0 -t0` replay below | 0 | `Statement`, `ObligationTree`, `Proof`, and `Counterexample` elaborated in dependency order. |
| Comment-stripped proof-device and diagnostic scan in that replay | 0 | No prohibited proof device or `sorryAx`; the exact negation uses only `propext`, `Classical.choice`, and `Quot.sound`. |
| `python3 Stage1_Instances/THM-M-0645/check_obligation_tree.py` | 0 | 15 obligations and 43 typed edges passed; denominator `ade5c7f4...7fc01`; predecessor root remains open M4. |
| `python3 Stage1_Instances/THM-M-0645/check_anchor_audit.py` | 0 | Anchor receipt `d61ebc24...1506` and pinned mathlib revision passed. |
| Three independent read-only audits, including an independent replay and pinned-library search | 0 | All identified the `Empty` eigenvariable defect; no exact positive candidate exists. |
| `python3 -m json.tool` plus source-hash and fail-closed assertions on the companion record | 0 | The record parsed; source hashes matched; verdict/state stayed `blocked`/`[ ]`; all completion fields stayed false. |
| `git diff --check -- Stage1_Instances/THM-M-0645` and a direct trailing-whitespace scan | 0 | No whitespace errors. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest is absent as required. |

Exact successful replay command from the worker root:

```bash
set -euo pipefail
root=$PWD
target=$root/Stage1_Instances/THM-M-0645
lean_dir=$root/Formalizations/Lean
tmp=$(mktemp -d /tmp/thm-m-0645-headb366bdd9-slot58-replay.XXXXXX)
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
rg -F "Stage1Instances.THM_M_0645.completenessTarget_of_countermodel" "$tmp/Proof.out"
sha256sum "$tmp"/{Statement,ObligationTree,Proof,Counterexample}.olean \
  "$tmp"/{Proof,Counterexample}.out
```

The explicit `LEAN_PATH` puts the copied target modules before existing compiled dependencies and
excludes the project build output, preventing an unrelated top-level `ObligationTree.olean` from
being selected.

| Artifact | SHA-256 |
|---|---|
| `Statement.olean` | `25eb67ade92875261cb4dafa5ae9075c3fe28e1e657ac763d2b7624430e04024` |
| `ObligationTree.olean` | `6c98e1bb9243a0930eae92822ff4d7a1043165662164476f7c47f7b0894bc614` |
| `Proof.olean` | `7c54139cf4e0d1fc38e44d2f6c1cca225e2fd83bd46dc35daa60ab86b344e7ce` |
| `Counterexample.olean` | `8dcfbde337211b11b3eb525b6f3cc2a5a191f3abfd60fc7d312725382d300c32` |
| `Proof.out` | `bfd3e14def163e4418a27cd1c1890dbe8e26ff0cf2c2589ff3631541c48b5e2b` |
| `Counterexample.out` | `80fb95cd6ab7948cfd7822889b590175b38af7d6180dd61103cbc634e37f48c1` |

## Retry Condition

Do not resume positive proof work against the current target. An authorized statement-phase repair
must first replace the unusable universal-introduction interface with a source-faithful
eigenvariable or context-extension rule and kernel-check derivability of quantified equality in the
empty language. The integration lane must then accept a new statement fingerprint, publish an
append-only obligation-registry delta, and rerun statement mutation tests, anchor audit, obligation
tree, and proof execution in dependency order.

## Status Boundary

This is fresh negative kernel evidence for `S56-M-0645-PROOF`, not a positive proof receipt. It
does not satisfy the assigned item or support a provisional state, audit completion, validation,
release, theorem completion, or master-acceptance claim.
