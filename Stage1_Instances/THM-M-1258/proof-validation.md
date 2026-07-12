# THM-M-1258 proof-phase validation

Item: `S56-M-1258-PROOF`

Base revision: `3d70df6fcb9b415d87ecf4a29d431ea67cd23b3f`

Validation date: `2026-07-12` (Asia/Shanghai)

## Proof result

`Proof.lean` implements the exact conditional root constructor and a concrete, non-vacuous
inhabitant of the condition. For every `n` and every open `Omega`, the zero drift together with the
`n` constant coordinate fields satisfies `hormanderCondition`: each coordinate field belongs to
`GeneratedBracket` by its `square` constructor, its value is the corresponding `Pi.basisFun`, and
those basis vectors span `Euclidean n`.

This closes a valid concrete route through `M1258-L-SPAN`; it does not make the false broadened
claim that arbitrary input fields satisfy the condition. The frozen condition-valued declaration,
registry, and denominator were not changed.

## Commands and results

All commands ran from the repository root unless the command starts with `cd`.

```text
cd Stage1_Instances/THM-M-1258 && \
  LEAN_PATH="$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH)" \
  ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 lake env lean \
    -o Statement.olean Statement.lean && \
  LEAN_PATH=".:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH)" \
  ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 lake env lean Proof.lean
  exit 0
  of_pointwise_span depends on axioms:
    [propext, Classical.choice, Quot.sound]
  coordinateFields_hormanderCondition depends on axioms:
    [propext, Classical.choice, Quot.sound]

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-1258
  exit 0: execution_rank=436; lifecycle_mode=planned; theorem_complete=false

python3 Stage1_Instances/THM-M-1258/check_obligation_tree.py
  exit 0: 9 obligations, 22 typed edges, and the frozen denominator passed

rg -n "\\b(sorry|axiom|admit|unsafe)\\b" \
  Stage1_Instances/THM-M-1258/Proof.lean
  exit 1 with no output: none of the forbidden declaration/body markers occurred

git diff --check -- Stage1_Instances/THM-M-1258 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

The generated `Statement.olean` was removed after the check. The existing pinned `.lake` artifact
was reused; no update, build, clone, fetch, or dependency mutation was performed. The pre-existing
untracked `.lake` artifact makes this nonrelease evidence.

## Status boundary

This receipt supports only worker-self-tested proof-phase bodies and awaits master acceptance. It
does not close source fidelity, readable reconstruction, hermetic replay, independent validation,
`AUDIT-Z`, `THEOREM-Z`, or the later validation and release nodes. The public target remains the
condition predicate; `coordinateFields_hormanderCondition` is an honest concrete witness rather
than a substitution for a universal assertion.
