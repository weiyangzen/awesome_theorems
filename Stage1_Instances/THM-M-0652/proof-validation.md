# S56-M-0652-PROOF worker evidence

Date: `2026-07-12`

Base revision: `345fe5a69ba9559544340ea64c754f3fb53f2fcf`

Pinned environment:

- Lean: `4.29.0` (`98dc76e3c0a9b856c9b98726b713fb04fab16740`)
- mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`

## Proof bodies admitted

`Proof.lean` adds eight placeholder-free local proof bodies. They establish
reflexivity and transitivity of the frozen vocabulary-subset and semantic-
entailment relations, and construct exact interpolants for the two boundary
cases where either endpoint already uses only symbols common to both endpoint
sentences. The boundary conclusions use the unchanged `IsInterpolant` target,
including both vocabulary conjuncts and both entailment directions.

These are substantive leaves for `M0652-S-BOUNDARY` and
`M0652-S-DEFINITIONS`; they do not prove the general Craig theorem. The first
unresolved proof gate remains the frozen minimal root cut set:
`M0652-B-COMPLETENESS`, `M0652-T-SYNTACTIC` (including cut elimination and
Maehara extraction), and `M0652-B-SOUNDNESS`. No eligible terminal body for
that general first-order calculus was found in the pinned closure. The root
therefore remains `M3`, theorem completion is false, and master acceptance must
preserve this boundary.

## Commands and exact results

From the repository root unless the command says otherwise:

```text
$ python3 Docs/tools/check_stage1_standard.py
check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)
exit 0

$ python3 scripts/stage1_target.py check
stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)
exit 0

$ python3 scripts/stage1_target.py show THM-M-0652
manifest entry found at execution_rank 298; baseline L0; rework_required true; theorem_complete false
exit 0

$ cd Stage1_Instances/THM-M-0652 &&
  LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    /home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean \
      -o Statement.olean Statement.lean &&
  LEAN_PATH=.:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    /home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean \
      -o ObligationTree.olean ObligationTree.lean &&
  LEAN_PATH=.:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    /home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean Proof.lean
all eight new declarations elaborated; vocabulary lemmas reported no axioms;
semantic and interpolation lemmas reported only `Quot.sound`
exit 0
temporary adjacent `.olean` files removed after the check

$ python3 Stage1_Instances/THM-M-0652/check_obligation_tree.py
PASS THM-M-0652 obligation tree: 15 obligations, 36 typed edges
registry denominator sha256: 4eb4a0414633ed491ed194764d56fd06b048e59c0d4609a852845f09b68b5d15
root closure: open (M3); completeness, syntactic interpolation, and soundness remain explicit
exit 0

$ rg -n '\b(sorry|admit|sorryAx)\b|(^|[^[:alnum:]_])axiom[[:space:]]' \
    Stage1_Instances/THM-M-0652/Statement.lean \
    Stage1_Instances/THM-M-0652/ObligationTree.lean \
    Stage1_Instances/THM-M-0652/Proof.lean
no matches
exit 1 (the expected clean result for rg)
```

The direct `lake env lean ../../Stage1_Instances/THM-M-0652/Proof.lean` attempt
exited 1 because Lean cannot resolve the adjacent `ObligationTree` module from
the Lake source root. The successful scoped recipe above uses `lake env
printenv LEAN_PATH` and the already-installed pinned Lean binary; it neither
updates nor writes to the shared `.lake` dependency tree.

Source SHA-256 values during validation:

```text
0688e793479810070b0d7afe2b93ffa85bb132e80f4c79840532ae5add69d793  Stage1_Instances/THM-M-0652/Statement.lean
b930f451c31f1d5bf54da6dd149efaa3b5255ee2396671670056d7d18e233d74  Stage1_Instances/THM-M-0652/ObligationTree.lean
d2d3d50130fc9960c0c1068b501ccb8427868959aec5c964e712b53ca31261a7  Stage1_Instances/THM-M-0652/Proof.lean
```
