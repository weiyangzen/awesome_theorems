# THM-M-0525 proof-phase validation

Item: `S56-M-0525-PROOF`. Base revision:
`6314a9f02e14ddacbf77779c85633968d5646a99`.

`Proof.lean` closes the frozen exact target without premises. It instantiates the conditional
composition theorem with mathlib's quotient-level `trans_assoc`, `refl_trans`, and `symm_trans`
proofs. This constructs the forward-concatenation group specified by `Statement.lean`; it does not
silently reuse mathlib's reverse-composition `FundamentalGroup` multiplication.

Validation ran in the worker clone on 2026-07-12. The canonical pinned `.lake` artifacts were
reused read-only through the existing symlink. No update, build, clone, or fetch was run.

```text
$ TOOLCHAIN="$(cat Formalizations/Lean/lean-toolchain)"
$ LEAN_BASE="$(cd Formalizations/Lean && lake env printenv LEAN_PATH)"
$ cd Stage1_Instances/THM-M-0525
$ ELAN_TOOLCHAIN="$TOOLCHAIN" LEAN_PATH="$LEAN_BASE" lake env lean -o Statement.olean Statement.lean
$ ELAN_TOOLCHAIN="$TOOLCHAIN" LEAN_PATH=".:$LEAN_BASE" lake env lean -o ObligationTree.olean ObligationTree.lean
$ ELAN_TOOLCHAIN="$TOOLCHAIN" LEAN_PATH=".:$LEAN_BASE" lake env lean Proof.lean
exit 0
'THM_M_0525.statement_proof' depends on axioms:
  [propext, Classical.choice, Quot.sound]
$ rm -f Statement.olean ObligationTree.olean
exit 0

$ python3 Docs/tools/check_stage1_standard.py
exit 0: ok; 15 assurance groups, 1546 uniform-L0 targets
$ python3 scripts/stage1_target.py check
exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required
$ python3 scripts/stage1_target.py show THM-M-0525
exit 0: rank 582, planned, theorem_complete false
$ python3 Stage1_Instances/THM-M-0525/check_obligation_tree.py
exit 0: PASS; 10 obligations, 38 typed edges, frozen denominator hash matched
$ rg -n '\b(sorry|admit|sorryAx)\b|(^|[^[:alnum:]_])axiom[[:space:]]' \
    Stage1_Instances/THM-M-0525/{Statement,ObligationTree,Proof}.lean
exit 1: expected no-match result
$ git diff --check -- Stage1_Instances/THM-M-0525 .stage1-worker-selftest.json
exit 0; no output
```

Validated source hashes:

```text
a7d309a1eb09fa8b4f03b47b46b79de3f210149d3473f9639ee11a4d55d1bb0e  Statement.lean
3f6d3e0ca2328e5272d36d0da2d62c649ae6f25f789285612ab0e526b3519972  ObligationTree.lean
815ddb3ab950034954ac1fd6245d1d88924b8fe793870cf1f0515489e4b014c0  Proof.lean
```

The obligation-tree validator intentionally reports its frozen pre-proof observation (`open
(M2); conditional composition only`); worker rules forbid rewriting the prior-phase registry or
item state. The new unconditional `statement_proof` is the proof-phase evidence for master review.
This is not a release or theorem-completion claim: trust/provenance, hermetic replay, freshness,
readability, and independent validation remain assigned to later gates.
