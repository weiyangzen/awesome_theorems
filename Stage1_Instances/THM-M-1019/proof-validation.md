# S56-M-1019-PROOF worker evidence

Date: `2026-07-12`. Base revision: `3f073e2861f931ee300acf7ebf3221bed31879bf`.

## Implemented proof

`Proof.lean` imports the exact `Statement` frozen by the statement phase. Its root declaration
introduces the two real measures and all three unchanged hypotheses, installs the explicit
probability proofs as local instances, and applies the pinned terminal proof body
`MeasureTheory.Measure.ext_of_charFun`. Lean checks the declaration at exactly
`Stage1Instances.THM_M_1019.Statement`.

The proof contains no `sorry`, `admit`, `sorryAx`, axiom declaration, or unsafe declaration. Lean
reports only `propext`, `Classical.choice`, and `Quot.sound`. This closes the exact root proof body
for the assigned proof node, provisionally pending master acceptance. It does not close the
downstream transitive-trust, hermetic, independent-validation, human-source, readability, or
release gates, and it does not claim theorem completion.

## Commands and exact results

No Lake update/build, dependency clone/fetch, or `.lake` mutation was performed. The narrow Lean
recipe created only a temporary directory beneath `Formalizations/Lean` and removed it on exit.

```text
$ python3 Docs/tools/check_stage1_standard.py
check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)
exit 0

$ python3 scripts/stage1_target.py check
stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)
exit 0

$ python3 scripts/stage1_target.py show THM-M-1019
exit 0: execution rank 495; baseline L0; planned; theorem_complete=false

$ python3 Stage1_Instances/THM-M-1019/check_obligation_tree.py
PASS THM-M-1019 obligation tree: 22 obligations, 28 typed edges
registry denominator sha256: 17f0c58272add1e5613ab46a92938da2ef6c36b45c7b9f012ebbad2a5c5b522f
root closure: open (M1); no proof or theorem completion claimed
exit 0 (expected frozen architecture-phase status)

$ python3 Stage1_Instances/THM-M-1019/check_anchor_audit.py
check_anchor_audit: ok (target fingerprint, pin/tree, source identity, 3 candidates)
exit 0

$ python3 Stage1_Instances/THM-M-1019/check_statement.py
exit 0: all four mutations killed; expression SHA-256 9e3e6807774912fde69809f88fb4928406a4241c5c3df6ff4bbacfe0c92e3d69; mathlib pin 8a178386ffc0f5fef0b77738bb5449d50efeea95

$ TMP=$(mktemp -d Formalizations/Lean/.m1019-proof.XXXXXX); trap 'rm -rf "$TMP"' EXIT
$ cp Stage1_Instances/THM-M-1019/{Statement,Proof}.lean "$TMP/"
$ cd Formalizations/Lean
$ lake env lean -o "../../$TMP/Statement.olean" "../../$TMP/Statement.lean"
$ LEAN_PATH="$(cd ../.. && pwd)/$TMP:$(lake env printenv LEAN_PATH)" lake env lean "../../$TMP/Proof.lean"
exit 0: characteristicFunctionUniqueness has exact type Statement; axioms are [propext,
Classical.choice, Quot.sound]

$ rg -n '\b(sorry|admit|sorryAx)\b|^[[:space:]]*(axiom|unsafe)[[:space:]]' Stage1_Instances/THM-M-1019/Proof.lean
no output; exit 1 (expected clean scan)

$ git diff --check -- Stage1_Instances/THM-M-1019 .stage1-worker-selftest.json
no output; exit 0
```

Validated source hashes:

```text
61b3cfa9d1141ace957b50415d2aaece5a4855001879b8f33e1f66c821137527  Statement.lean
ccc11648e4159ff445154b7c694f23a8b26ad235841f1ac3579cbf0bd643b147  Proof.lean
b8e8cf0ef459b8879ff56b5fac089e17f3e75ff428e18f1332015a42a184f4d6  obligation-registry.json
```
