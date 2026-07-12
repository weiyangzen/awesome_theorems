# S56-M-1015-PROOF worker evidence

Date: `2026-07-12`. Base revision: `8bf50ccc24184807c5fc0171494baac953a8d9c6`.

`Proof.lean` imports the exact frozen `Statement`. Pair, sum, and product use the pinned mathlib
Slutsky bridges. The missing quotient branch is closed locally: continuity of inversion at the
nonzero constant transfers `Y_n -> c` in measure to `Y_n^-1 -> c^-1`; the product bridge then
gives `X_n * Y_n^-1 -> Z * c^-1`. The terminal theorem has the exact imported statement type.

No `sorry`, `admit`, `sorryAx`, axiom, or unsafe declaration occurs. Lean reports only
`[propext, Classical.choice, Quot.sound]` for all three declarations. This receipt is provisional
proof-node evidence, not theorem completion or downstream validation/release acceptance.

## Commands and results

```text
$ python3 Docs/tools/check_stage1_standard.py
check_stage1_standard: ok (... 1546 uniform-L0 Lean 4 targets ...); exit 0

$ python3 scripts/stage1_target.py check
stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required); exit 0

$ cd Formalizations/Lean
$ TMP=$(mktemp -d ./.m1015-proof.XXXXXX)
$ cp ../../Stage1_Instances/THM-M-1015/{Statement,Proof}.lean "$TMP/"
$ lake env lean -o "$TMP/Statement.olean" "$TMP/Statement.lean"
$ LEAN_PATH="$TMP:$(lake env printenv LEAN_PATH)" lake env lean "$TMP/Proof.lean"
exit 0; all axiom reports: [propext, Classical.choice, Quot.sound]

$ python3 Stage1_Instances/THM-M-1015/check_obligation_tree.py
PASS: 17 obligations, 38 typed edges; exit 0 (frozen pre-proof status retained)

$ rg -n '\b(sorry|admit|sorryAx)\b|^[[:space:]]*(axiom|unsafe)[[:space:]]' Stage1_Instances/THM-M-1015/Proof.lean
no output; exit 1 (expected clean scan)

$ git diff --check -- Stage1_Instances/THM-M-1015 .stage1-worker-selftest.json
no output; exit 0
```

No Lake update/build, dependency fetch, network access, or `.lake` mutation was performed.
