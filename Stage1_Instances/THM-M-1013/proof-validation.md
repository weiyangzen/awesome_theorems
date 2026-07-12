# S56-M-1013-PROOF worker evidence

Date: `2026-07-12`. Base revision: `6f53a31f8e3774a09182794cbac7edc5c7a286df`.

## Implemented proof

`Proof.lean` imports the exact `StatementShape` frozen in `Statement.lean`. It closes the forward
branch with pinned mathlib's continuous mapping theorem. It closes the reverse branch by taking
the scalar characteristic-function convergence at frequency one, applying the locally proved
projection identity, and invoking pinned mathlib's Levy characteristic-function criterion. The
root theorem `Stage1Instances.THM_M_1013.Proof.cramerWold` consumes both branches and has exactly
the frozen type, including the `d = 0` case.

There is no `sorry`, `admit`, `sorryAx`, new axiom, or unsafe declaration. Lean reports only
`[propext, Classical.choice, Quot.sound]` for the local identity, both implications, and the root.
This is provisional self-test evidence for the assigned proof node. The frozen obligation-tree
artifact still truthfully reports its pre-proof `M3` boundary; only downstream validation/master
reconciliation may update authoritative state. Human-source acceptance, readable reconstruction,
full provenance/trust review, independent validation, release, and theorem completion are not
claimed.

## Commands and exact results

No Lake update/build, dependency fetch/clone, or `.lake` mutation was performed. The existing
worker `.lake` is a symlink to the canonical pinned artifacts. The Lean recipe built only a
temporary `Statement.olean` under `Formalizations/Lean` and removed the directory on exit.

```text
$ python3 Docs/tools/check_stage1_standard.py
check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)
exit 0

$ python3 scripts/stage1_target.py check
stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)
exit 0

$ python3 scripts/stage1_target.py show THM-M-1013
exit 0: execution rank 292; baseline L0; planned; theorem_complete=false

$ cd Formalizations/Lean
$ TMP=$(mktemp -d ./.m1013-proof.XXXXXX); trap 'rm -rf "$TMP"' EXIT
$ cp ../../Stage1_Instances/THM-M-1013/{Statement,Proof}.lean "$TMP/"
$ lake env lean -o "$TMP/Statement.olean" "$TMP/Statement.lean"
$ LEAN_PATH="$TMP:$(lake env printenv LEAN_PATH)" lake env lean "$TMP/Proof.lean"
exit 0: the exact root and all three supporting declarations elaborated; every axiom report was
[propext, Classical.choice, Quot.sound]

$ python3 Stage1_Instances/THM-M-1013/check_proof.py
PASS THM-M-1013 proof: forward and reverse branches close exact StatementShape
exit 0

$ python3 Stage1_Instances/THM-M-1013/check_obligation_tree.py
PASS THM-M-1013 obligation tree: 14 obligations, 36 typed edges
registry denominator sha256: 41873784159809cc09371822dc5121c17dbfa74bf6613c734eb709a9babfc970
root closure: open (M3); proof execution and release gates remain downstream
exit 0 (expected frozen architecture-phase status)

$ rg -n '\b(sorry|admit|sorryAx)\b|^[[:space:]]*(axiom|unsafe)[[:space:]]' Stage1_Instances/THM-M-1013/Proof.lean
no output; exit 1 (expected clean scan)

$ git diff --check -- Stage1_Instances/THM-M-1013 .stage1-worker-selftest.json
no output; exit 0

$ git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD
8a178386ffc0f5fef0b77738bb5449d50efeea95
exit 0

$ cd Formalizations/Lean && lake env lean --version
Lean 4.29.0, commit 98dc76e3c0a9b856c9b98726b713fb04fab16740
exit 0
```

Validated SHA-256 values:

```text
76a798216239a16d9ea0fa55d2dd69c41f1e757de9c99deae69f2e9462076c0b  Statement.lean
f9bfee6551a02d20ac436a70282f914a2ba49f3e41ea0e17a38d9d9a409de8ec  ObligationTree.lean
0eed5f1306be5125db5cb59a25c1bd71fe66601f6876a6be7de52dad2806e84a  obligation-registry.json
a06c23901f366aa546d16a566c244533748a910582cb101acb860e61b5b9e4f1  Proof.lean
```
