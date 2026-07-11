# S56-M-0083-PROOF worker evidence

Date: `2026-07-12`

Base revision: `1f93d74fbfd640b2ed20c70526609c84eb603b35`.

## Implemented proof

`Proof.lean` proves the exact target frozen in `Statement.lean`. The forward
direction turns the supplied object, element, and family of bijections into an
`IsRepresentedBy` witness using `isRepresentedBy_iff`, then applies
`IsRepresentable.iff_exists_isRepresentedBy`. The reverse direction extracts
that witness, expands its `map_bijective` field for every test object, and the
root theorem composes the two implications without changing any binder,
universe, variance, hypothesis, or conclusion.

Lean reports `[propext]` for the represented-by adapters and `[propext,
Classical.choice, Quot.sound]` for both directions and the root. The source has
no `sorry`, `admit`, `sorryAx`, new `axiom`, or `unsafe` declaration. This is
provisional proof-node evidence pending master acceptance. It does not claim
validation, release, H0, R0, hermetic replay, independent verification, audit
completion, or theorem completion.

## Commands and exact results

All commands ran inside this worker clone. No Lake update, build, fetch, clone,
network access, or dependency mutation was performed.

```text
$ python3 Docs/tools/check_stage1_standard.py
check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)
exit 0

$ python3 scripts/stage1_target.py check
stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)
exit 0

$ python3 scripts/stage1_target.py show THM-M-0083
execution rank 139; baseline L0; rework_required true; planned; theorem_complete false
exit 0

$ (cd Formalizations/Lean && bash ../../Stage1_Instances/THM-M-0083/check_proof.sh)
representedBy_of_universalElement and universalElement_of_representedBy reported
[propext]; forward, reverse, and representableFunctorTarget reported
[propext, Classical.choice, Quot.sound]
exit 0

$ python3 Stage1_Instances/THM-M-0083/check_proof.py
PASS THM-M-0083 proof source: two exact directions and root composition present
exit 0

$ python3 Stage1_Instances/THM-M-0083/check_obligation_tree.py
PASS THM-M-0083 obligation tree: 11 obligations, 30 typed edges
registry denominator sha256: 7b39d289b02d6b5e59b40043779eee5c5556875db249c4b7e440e43a0c859e96
root candidate: kernel checked (M0-W), master acceptance and later release gates open
exit 0

$ python3 Stage1_Instances/THM-M-0083/check_statement.py
four frozen mutations killed; expression sha256
1319e132e2f2c66360cf15565db7a1f4acf3623597a87f92753765c02d714a19
exit 0

$ rg -n '\b(sorry|admit|sorryAx)\b|^[[:space:]]*(axiom|unsafe)\b' \
    Stage1_Instances/THM-M-0083/Proof.lean
no output
exit 1 (expected clean scan)

$ git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD
8a178386ffc0f5fef0b77738bb5449d50efeea95
exit 0

$ (cd Formalizations/Lean && lake env lean --version)
Lean 4.29.0, commit 98dc76e3c0a9b856c9b98726b713fb04fab16740
exit 0
```

Validated SHA-256 values:

```text
c5cba3b345c94fdb2519438f71a52b96408d8551e75d37e1aaeb3a7e00fe8580  Statement.lean
e1eae363a2479550665c589239c60ac353244ad8cb3b213243f4071a4f6f5e53  ObligationTree.lean
86e994c7d408d35c79705f81760150eaea7cd4a77e81d7cb8ff17de0c95f5a17  obligation-registry.json
ab65d7b81589d3f0273bc457c95ae2c3593ca21a75f041ee2e27ed3af38ea0c1  Proof.lean
```

Known open gates outside this phase are node-specific human-source and readable
review, transitive provenance and trust closure, hermetic replay, freshness,
independent validation, and master acceptance.
