# THM-M-0476 proof-phase validation

Item: `S56-M-0476-PROOF`. Base revision:
`dc600635160cace0916df5234bf8808c39dc656d`.

## Implemented closure

`Proof.lean` installs the exact pinned `ZMod.wilsons_lemma` at the frozen explicit-prime target and
also builds an independent root through every child in the frozen proof graph. The expanded route
supplies the natural interval-factorial and cast identities, composes the representative-to-unit
bijection, classifies inverse-fixed units, cancels inverse pairs, restores negative one, coerces the
unit product into `ZMod p`, and applies the checked `Fact` transport. The direct and expanded roots
are distinct exact-type checks over shared terminal bodies, not duplicate proof credit.

The exact Wilson body is in `Mathlib/NumberTheory/Wilson.lean` lines 43-68 at mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; its source SHA-256 is
`7bd6ec0e909f037f8632e1b495f9647a61fe950f3bfe3af98a5a22914622aeb7`. The generalized unit
product body is in `Mathlib/FieldTheory/Finite/Basic.lean` lines 110-117, source SHA-256
`808bb4eddb8a4b48785e4430f944fe0827c96842dffa0c08cd21b5659bd85d44`. This proof phase proposes
`M0-W` for the exact root and 18 proof-body obligations, pending master acceptance.

## Commands and exact results

Validation ran on 2026-07-13 (Asia/Shanghai), reusing the automation-provided canonical pinned
`.lake` symlink. No `lake update`, `lake build`, dependency clone, fetch, network action, or `.lake`
mutation was performed.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and
  execution-skill presence passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0476
  exit 0: rank 1357, planned, L0/rework_required, theorem_complete=false

bash Stage1_Instances/THM-M-0476/check_proof.sh
  exit 0: isolated Statement.olean, ObligationTree.olean, and Proof elaboration passed; four pinned
  upstream declarations and nineteen local declarations were sorry-free. Every axiom report was a
  subset of [propext, Classical.choice, Quot.sound]; stdout SHA-256
  64f24732b3acba31146b7f43f81e83b6fcc45c7bed80ef61e96eb10cfdc8c68f

python3 -B Stage1_Instances/THM-M-0476/check_proof.py
  exit 0: exact source fragments, frozen graph reachability, immutable pins and source/olean hashes,
  receipt boundary, complete changed-path packet, and no-completion claim passed

python3 -B Stage1_Instances/THM-M-0476/check_obligation_tree.py
  exit 0: deterministic 26-obligation, 114-edge freeze and historical open-state boundary passed

python3 -B Stage1_Instances/THM-M-0476/check_anchor_audit.py
  exit 0: seven immutable candidate records, exact adapter, source pins, and fail-closed state passed

python3 -B Stage1_Instances/THM-M-0476/check_intake.py
  exit 0: planned dossier, empty accepted state, and open local task projection passed

rg -n -i --glob '*.lean' prohibited-proof-pattern Stage1_Instances/THM-M-0476/Proof.lean
  exit 1 with empty output: expected pass; no prohibited construct found

git diff --check -- Stage1_Instances/THM-M-0476 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

The accepted planned instance remains `[H1, M3, R4]` with empty accepted proof state until the
integration lane acts. `M0476-S-FOUNDATION`, H0, R0, full transitive provenance and trust,
hermetic replay, deterministic evidence, independent verification, validation, release, audit
completion, and theorem completion remain open. This proof receipt does not claim theorem
completion.

This worker evidence does not claim theorem completion.
