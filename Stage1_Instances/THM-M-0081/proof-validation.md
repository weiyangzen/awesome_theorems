# THM-M-0081 proof-phase validation

## Implemented proof

`Proof.lean` proves both directions of the exact expression frozen in `CanonicalStatement.lean`.
For reflection, it applies `Yoneda.fullyFaithful.preimageIso` to the supplied natural isomorphism.
For preservation, it applies `yoneda.mapIso` to the supplied object isomorphism. The root theorem
combines these bodies without changing the universes, variance, objects, `Nonempty` encoding, or
conclusion of the canonical target.

Lean reports only `propext`, `Classical.choice`, and `Quot.sound` in all three declarations' axiom
closures. The source has no `sorry`, `admit`, `sorryAx`, new axiom, or unsafe declaration. This is
provisional worker evidence for the proof node only. Master acceptance, validation, release, H0,
R0, hermetic replay, independent verification, and theorem completion remain unclaimed.

## Commands and results

Commands ran from base revision `0000e0790fe81ee7e79cc41fea61f3c42d65e95a` on 2026-07-12
(receipt timestamp `2026-07-11T23:43:43Z` UTC).

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0081
  exit 0: execution rank 138; planned; theorem_complete=false

cd Formalizations/Lean &&
  lake env lean ../../Stage1_Instances/THM-M-0081/Proof.lean
  exit 0: reflection, preservation, and yonedaObjectDetection elaborated;
  each #print axioms reported propext, Classical.choice, and Quot.sound

python3 Stage1_Instances/THM-M-0081/check_obligation_tree.py
  exit 0: 11 obligations and 21 typed edges passed; denominator
  f38e8efb0c7df7d14e55dc7e7e2a39d88921b21c20eda3ecfb2d6287dbbbf69d
  matched. Its expected frozen pre-proof status remains "open (M4); conditional composition only".

rg -n '\b(sorry|admit|sorryAx)\b|^[[:space:]]*axiom\b|^[[:space:]]*unsafe\b' \
  Stage1_Instances/THM-M-0081/Proof.lean
  exit 1 with empty output: pass, no prohibited source token

git diff --check -- Stage1_Instances/THM-M-0081
  exit 0: no whitespace errors

cd Formalizations/Lean && lake env lean --version
  exit 0: Lean 4.29.0, commit 98dc76e3c0a9b856c9b98726b713fb04fab16740

git -C "$(readlink -f Formalizations/Lean/.lake)/packages/mathlib" rev-parse HEAD
  exit 0: 8a178386ffc0f5fef0b77738bb5449d50efeea95
```

No update, build, clone, fetch, network access, or mutation of `.lake` was performed.
