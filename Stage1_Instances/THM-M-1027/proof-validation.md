# THM-M-1027 proof-phase validation

Item: `S56-M-1027-PROOF`. Base revision:
`3bb9672e70fb05a3e2a6743d8dcfb6b86161e0cb`.

This phase adds real Lean bodies for ordered increment-variance normalization,
the zero-start consequence of the zero-variance Gaussian law, coherent witness
assembly, and exact conditional root composition. It does not assert or assume
the unavailable Brownian construction. The remaining machine cut is
`M1027-X-EXTERNAL`: the pinned `RemyDegenne/brownian-motion` source at commit
`fdcef67f41b51b7635b3c2d08eb61768604f8f74` is not in the local Lake closure.

## Narrow validation evidence

Commands ran from the worker clone on 2026-07-12. Existing canonical pinned
`.lake` artifacts were reused. No update, build, dependency clone, fetch, or
dependency mutation was run.

```text
cd Stage1_Instances/THM-M-1027
LEAN_PATH="$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH)" \
  ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 lake env lean \
  -o Statement.olean Statement.lean
  exit 0; exact target elaborated

LEAN_PATH=".:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH)" \
  ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 lake env lean \
  -o ObligationTree.olean ObligationTree.lean
  exit 0; conditional witness-to-root composition elaborated

LEAN_PATH=".:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH)" \
  ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 lake env lean Proof.lean
  exit 0; all five proof-phase declarations elaborated
  each #print axioms report: [propext, Classical.choice, Quot.sound]

python3 Stage1_Instances/THM-M-1027/check_proof.py
  exit 0: PASS; local Brownian adapter bodies close; external construction remains

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets pass

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-1027
  exit 0: rank 218, planned, hard_mathlib_anchor_and_wrapper, theorem incomplete

rg -n '^\\s*(sorry|admit|axiom)(\\s|$)|by\\s+sorry|:=\\s+sorry' \
  Stage1_Instances/THM-M-1027 --glob '*.lean'
  exit 1: no prohibited declaration or placeholder found
```

The proof phase is provisionally self-tested, but the root stays `M3` and
theorem completion remains false. Master acceptance and all later validation
and release gates remain required.
