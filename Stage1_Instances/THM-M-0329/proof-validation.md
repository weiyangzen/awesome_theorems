# THM-M-0329 proof-phase validation

Item: `S56-M-0329-PROOF`. Date: `2026-07-12`. Base revision:
`230f719da7724afb27c761dcb8c62a327557fe63`.

`Proof.lean` supplies both explicit premises of the frozen composition theorem.
`rieszPackage` uses the pinned real-Hilbert-space Riesz equivalence;
`operatorPackage` binds the pinned mathlib Lax-Milgram continuous equivalence;
`laxMilgram` then applies `ObligationTree.root_of_packages` and has exactly the
frozen `LaxMilgramTarget` type. There is no new premise, weakened target,
placeholder, or axiom declaration.

The proof bodies are self-tested, but this proof-phase receipt is provisional.
Source, transitive trust/provenance, hermetic validation, independent review,
release, and master-acceptance gates remain outside this assigned phase. Thus
this artifact does not claim theorem completion.

## Commands and exact results

Commands ran from the worker clone and reused its canonical pinned `.lake`
artifacts. No update, build, clone, or fetch was run.

```text
cd Stage1_Instances/THM-M-0329
LP="$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH)"
LEAN_PATH="$LP" ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 lake env lean -o Statement.olean Statement.lean
LEAN_PATH=".:$LP" ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 lake env lean -o ObligationTree.olean ObligationTree.lean
LEAN_PATH=".:$LP" ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 lake env lean Proof.lean
rm -f Statement.olean ObligationTree.olean
  exit 0
  rieszPackage: [propext, Classical.choice, Quot.sound]
  operatorPackage: [propext, Classical.choice, Quot.sound]
  laxMilgram: [propext, Classical.choice, Quot.sound]

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups; 1546 uniform-L0 Lean 4 targets

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0329
  exit 0: rank 822; planned; theorem_complete false

python3 Stage1_Instances/THM-M-0329/check_obligation_tree.py
  exit 0: PASS; 17 obligations, 67 typed edges
  registry denominator sha256: 852bdc59e2ed4e06290a11ef592640475a71292a1111e2a19947e149f3ce0308

rg -n '\b(sorry|admit|sorryAx)\b|(^|[^[:alnum:]_])axiom[[:space:]]|proof_wanted' \
  Stage1_Instances/THM-M-0329/{Statement,ObligationTree,Proof}.lean
  exit 1 as expected: no matches
```

Validated source hashes:

```text
1aa92764d82d20fcb1db4ea2fbfe11c9ee932431bfa9147fb59a50678409d5e6  Statement.lean
78dddf2b05f888cafcc30af6f5a7f4e0511407acaef09f8220c94d438f3f1aa8  ObligationTree.lean
79a98b2715a1267fe542abb837e419f7a25312c4f2b4afb5442831a057b6f562  Proof.lean
```
