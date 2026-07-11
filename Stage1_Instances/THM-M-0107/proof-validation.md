# THM-M-0107 proof-phase validation

Item: `S56-M-0107-PROOF`

Base revision: `e7581f4284278d4bd47fe4031297b242386a9bc4`

## Implemented bodies

`Proof.lean` pins the mathlib proof of `IsOpenImmersion f.toNormalization`,
pins `f.toNormalization_fromNormalization`, and checks exact assembly of the
frozen existential root from those bodies and an explicit finiteness premise.
This closes the open-factor, equation, and conditional terminal-composition
units for this proof phase.

The root is not closed. The pinned relative normalization is integral, but the
configured dependency closure does not provide `IsFinite f.fromNormalization`
under the frozen hypotheses. `M0107-L-FINITE` and its
`M0107-L-INTEGRAL-TO-FINITE` bridge remain the root cut set. The conditional
assembly theorem does not assert or conceal that premise.

## Commands and results

Commands ran in the worker clone on 2026-07-12 (Asia/Shanghai), with receipt
timestamp `2026-07-11T20:13:23Z`. Existing pinned `.lake` artifacts were reused;
no update, build, clone, fetch, or dependency mutation was run.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0107
  exit 0: execution rank 31; planned; theorem_complete=false

cd Formalizations/Lean
tmp=$(mktemp -d ./.m0107-proof.XXXXXX)
cp ../../Stage1_Instances/THM-M-0107/{Statement,Proof}.lean "$tmp/"
lake env lean -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_PATH="$tmp:$(lake env printenv LEAN_PATH)" lake env lean "$tmp/Proof.lean"
  exit 0: all three declarations elaborated; each axiom report contained only
  propext, Classical.choice, and Quot.sound

python3 Stage1_Instances/THM-M-0107/check_proof.py
  exit 0: required bodies, explicit finite premise, and placeholder scan passed

python3 Stage1_Instances/THM-M-0107/check_obligation_tree.py
  exit 0: 29 obligations and 30 typed edges passed; finite-envelope cut set open

git diff --check -- Stage1_Instances/THM-M-0107 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

This is self-test evidence for the proof phase only. Validation and release
receipts, source/readability closure, independent verification, master
acceptance, and theorem completion remain unclaimed.
