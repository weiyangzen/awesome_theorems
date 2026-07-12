# THM-M-0772 proof-phase evidence

Item: `S56-M-0772-PROOF`  
Base revision: `b17067c5d92786b270337cbdd3bfaf74df7773f9`  
Date: 2026-07-12 (Asia/Shanghai)

## Implemented proof

`Proof.lean` gives a placeholder-free proof of the exact frozen proposition: for every
universe-polymorphic partially ordered carrier, the set `maxChain (fun x y => x <= y)` is an
inclusion-maximal chain. The terminal proof body is the already pinned mathlib declaration
`maxChain_spec` at commit `8a178386ffc0f5fef0b77738bb5449d50efeea95`; the local theorem specializes
only its relation argument and introduces no premise. A second declaration elaborates the expanded
chainhood-and-maximality encoding, guarding the statement boundary.

This closes the proof phase's machine root and imported-body cut set provisionally. It does not
claim theorem completion: master acceptance and the separate validation, source/readability,
independent replay, release, `AUDIT-Z`, and `THEOREM-Z` gates remain open.

## Commands and exact results

All commands ran in this worker clone. Existing pinned `.lake` artifacts were reused; no update,
build, dependency clone, fetch, or `.lake` mutation was performed.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: standard OK (15 assurance groups, 1546 uniform-L0 Lean 4 targets)

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0772
  exit 0: rank 580, planned, baseline L0, theorem_complete false

cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0772/Proof.lean
  exit 0: maxChain_spec, hausdorffMaximalPrinciple, and
  expandedHausdorffMaximalPrinciple all report exactly
  [propext, Classical.choice, Quot.sound]

python3 Stage1_Instances/THM-M-0772/check_proof.py
  exit 0: PASS THM-M-0772 proof: exact maximal-chain root body and receipt verified

rg -n '\b(sorry|admit|sorryAx)\b|^[[:space:]]*(axiom|unsafe)\b' \
  Stage1_Instances/THM-M-0772/Proof.lean
  exit 1 with empty output: expected clean placeholder/declaration scan

git diff --check -- Stage1_Instances/THM-M-0772 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

The proof source SHA-256 is
`0bf999635baf1239e44f83e1b4d94a9a226d481d0a185aecd4e33e2b7dc04eca`. The pinned mathlib
revision is `8a178386ffc0f5fef0b77738bb5449d50efeea95` and the Lean toolchain is
`leanprover/lean4:v4.29.0`.
