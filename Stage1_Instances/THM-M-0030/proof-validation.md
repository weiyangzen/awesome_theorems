# THM-M-0030 proof-phase validation

Item: `S56-M-0030-PROOF`. Base revision:
`ebd5f75831296a8a35e7b33013b964f2baf31bb9` (tree
`d1e4bc83c803eefcd9898aac57352265a29f0658`).

## Implemented proof

`Proof.lean` installs the exact pinned `Ideal.iInf_pow_eq_bot_of_isLocalRing` theorem at the frozen
anchor interface and closes the unchanged `KrullIntersectionTarget` both directly and through the
frozen root adapter. It also installs the finite-module, Jacobson, local containment, unit, and
fixed-point bodies and consumes all seven checked child-to-parent composition interfaces. This
gives a second exact root through the locally checked frozen interfaces. It does not independently
reprove each deeper refinement hidden inside the pinned fixed-point theorem.

The deeper filtration, stable-intersection, stabilization, Nakayama, and power-induction work is
the transparent terminal route in pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, source SHA-256
`b161e2c4ce77f1224648467573dd4ba4c0ebc1ed734118e70df4cb39b33b1a72`. It is imported rather
than copied or replaced. The proof contains no `sorry`, `admit`, custom axiom, unsafe/opaque
declaration, native oracle, external code, or weakened theorem. Lean reports exactly `propext`,
`Classical.choice`, and `Quot.sound` for every pinned terminal, installed leaf, composition, and
root declaration.

## Commands and results

Validation ran on 2026-07-13 (`Asia/Shanghai`) using the automation-provided canonical `.lake`
symlink read-only. No `lake update`, `lake build`, dependency clone/fetch, network access, or
`.lake` mutation ran. The exact root and locally installed interfaces are provisionally closed;
six deeper refinement IDs are source-mapped through that transparent route but are not claimed as
individually node-closed by this receipt.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups, 41 legacy rows, 300 slots, and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0030
  exit 0: execution rank 1075, planned, L0/rework-required, theorem_complete false

bash Stage1_Instances/THM-M-0030/check_proof.sh
  exit 0: isolated Statement.olean and ObligationTree.olean were built; Proof.lean elaborated;
  all nine requested declarations were sorry-free; all 22 axiom reports were exactly
  [propext, Classical.choice, Quot.sound]

python3 -B Stage1_Instances/THM-M-0030/check_proof.py
  exit 0: exact target, frozen graph, dependency pin, transparent terminal route, receipt hashes,
  placeholder policy, status boundary, changed paths, and worker packet passed

python3 -m json.tool Stage1_Instances/THM-M-0030/proof-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0: both structured artifacts parsed

cd Formalizations/Lean && lake env lean --version
  exit 0: Lean 4.29.0, commit 98dc76e3c0a9b856c9b98726b713fb04fab16740

git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}
  exit 0: revision 8a178386...ea95, tree bdc39a31...c2b

git -C Formalizations/Lean/.lake/packages/mathlib status --short
  exit 0: empty output; pinned dependency worktree clean

rg -n '\b(sorry|admit|sorryAx|implemented_by|native_decide|extern|opaque)\b|^[[:space:]]*(axiom|constant|unsafe)[[:space:]]+' Stage1_Instances/THM-M-0030/Proof.lean
  exit 1 (expected no match): no placeholder, bodyless axiom/constant, unsafe/oracle/backend,
  opaque, native_decide, or external-code marker

git diff --check -- Stage1_Instances/THM-M-0030 .stage1-worker-selftest.json
  exit 0: no tracked whitespace diagnostics

git diff --no-index --check /dev/null <each of the six changed files>
  exit 1 for each expected new-file difference, with no whitespace diagnostics
```

## Status boundary

This is provisional proof-phase evidence and proposes `M0-W` only after master acceptance. The
authoritative accepted state remains `H1/M3/R3` with an empty accepted proof state. In particular,
`M0030-S-FOUNDATION`, the prerequisite receipt, H0/R0, complete source/provenance/trust closure,
validation, hermetic replay, independent verification, and release remain open. This worker packet
does not claim theorem completion, audit completion, or master acceptance.
