# S56-M-0086-PROOF worker evidence

Date: `2026-07-12`. Base revision: `f36169f19d5994091ea3dc506080032ff3f5321b`.

## Implemented proof

`Proof.lean` imports the exact target frozen by `Statement.lean`. It supplies separate wrappers for
the three frozen terminal obligations using the pinned declarations `freyd_mitchell`,
`has_injective_coseparator`, and `has_projective_separator`, then constructs
`CanonicalStatement.{v, u}` from those wrappers without changing a binder, hypothesis, universe, or
conclusion. Lean reports `[propext, Classical.choice, Quot.sound]` for every wrapper and the root.
The proof source contains no `sorry`, `admit`, `sorryAx`, new axiom, or unsafe declaration.

This self-tests the assigned proof phase pending master acceptance. The obligation-tree validator
continues to print its frozen architecture-phase boundary (`M1` and an open three-lemma cut set);
that historical artifact is intentionally not rewritten by this worker. Validation must reconcile
the new proof evidence. Source/readability, full trust/provenance, hermetic replay, independent
validation, release, audit completion, and theorem completion remain unclaimed.

## Commands and exact results

No Lake update/build/fetch/clone or dependency mutation was performed. The local two-step Lean
command creates `Statement.olean` only in the owned target directory and removes it immediately.

Three superseded setup attempts failed before the final narrow recipe: direct elaboration from
`Formalizations/Lean` could not resolve the target-local `Stage1_Instances` module prefix (exit 1);
running from the target directory without `ELAN_TOOLCHAIN` found no default toolchain (exit 1); and
adding the toolchain without the pinned Lake `LEAN_PATH` could not resolve `Mathlib` (exit 1). These
failures changed no dependency or `.lake` artifact. The final recipe below explicitly supplies both
the pinned toolchain and Lake search path and is the validated recipe of record.

```text
$ python3 Docs/tools/check_stage1_standard.py
check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)
exit 0

$ python3 scripts/stage1_target.py check
stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)
exit 0

$ python3 scripts/stage1_target.py show THM-M-0086
exit 0: execution rank 134; baseline L0; rework_required true; planned; theorem_complete false

$ cd Stage1_Instances/THM-M-0086
$ LEAN_DEPS="$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH)"
$ LEAN_PATH="$LEAN_DEPS" ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 lake env lean -o Statement.olean Statement.lean
$ LEAN_PATH=".:$LEAN_DEPS" ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 lake env lean Proof.lean
$ rm -f Statement.olean
exit 0: exact statement and proof elaborated; all four proof declarations report
[propext, Classical.choice, Quot.sound]

$ python3 Stage1_Instances/THM-M-0086/check_proof.py
PASS THM-M-0086 proof source: three pinned branches compose to CanonicalStatement
exit 0

$ python3 Stage1_Instances/THM-M-0086/check_obligation_tree.py
PASS THM-M-0086 obligation tree: 19 obligations, 42 typed edges
registry denominator sha256: 3ef5a22e409dfe80fa0504d68038c05507040538a88d010910b121fc3c5a986d
root remains open at M1; frozen cut set: L-EMBED, L-INJECTIVE, L-PROJECTIVE
exit 0 (expected frozen architecture-phase boundary)

$ rg -n '\b(sorry|admit|sorryAx)\b|^[[:space:]]*(axiom|unsafe)[[:space:]]' Stage1_Instances/THM-M-0086/Proof.lean
no output; exit 1 (expected clean scan)

$ git diff --check -- Stage1_Instances/THM-M-0086 .stage1-worker-selftest.json
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
98e2fce9832b23421c3084e1e7d3dfa84f1465fd700ab66a5eacf386b7c626f1  Statement.lean
d949d44c5a011b0ad00a1dee413ecca466af1dea4e679424f70c00b875d15587  ObligationTree.lean
af09f8198e3ad5dd51c9d35eef14f42a451a4e8cbd33a0360946aeb1da259190  obligation-registry.json
897b7480d54dbb19c3a53734199f4d67cee50b726ee3772b9c229894489b22d7  Proof.lean
```
