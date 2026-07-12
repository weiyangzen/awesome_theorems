# THM-M-0984 proof-phase validation

Item: `S56-M-0984-PROOF`. Base revision:
`5e4c113b5fdd950714aacb1c46886e07431e3cd5`.

`Proof.lean` supplies the real proof body for the frozen
`M0984-L-TERMINAL` obligation. It applies pinned mathlib declaration
`ProbabilityTheory.strong_law_ae` with the exact integrability, pairwise
independence, and identical-distribution hypotheses, then uses the frozen
`root_of_terminal` composition certificate to prove `ObligationTree.Root`.
No premise, binder, codomain, measure, or almost-everywhere conclusion is
weakened or substituted.

Validation ran in the worker clone on 2026-07-12. Existing pinned Lake
artifacts and toolchain `leanprover/lean4:v4.29.0` were reused. No update,
build, dependency clone/fetch, or `.lake` mutation was performed.

```text
cd Stage1_Instances/THM-M-0984
LEAN_PATH="$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH)" \
  ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 lake env lean \
    -o Statement.olean Statement.lean
LEAN_PATH=".:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH)" \
  ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 lake env lean \
    -o ObligationTree.olean ObligationTree.lean
LEAN_PATH=".:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH)" \
  ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 lake env lean Proof.lean
  combined exit 0
  terminalStrongLaw axioms: [propext, Classical.choice, Quot.sound]
  strongLawRoot axioms: [propext, Classical.choice, Quot.sound]
rm -f Statement.olean ObligationTree.olean
  exit 0

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets passed
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-0984
  exit 0: rank 264, planned, theorem_complete false
python3 Stage1_Instances/THM-M-0984/check_proof.py
  exit 0: exact terminal and frozen-root composition bodies present
rg forbidden proof tokens Stage1_Instances/THM-M-0984/Proof.lean
  exit 1 with empty output: pass, no placeholder, bodyless axiom, or unsafe declaration
sha256sum Stage1_Instances/THM-M-0984/Proof.lean
  exit 0: 00acf210d8546cb6e11f1ed7cbadf91af7c58ec85c552b4dbb68d967fd600f30
git diff --check -- Stage1_Instances/THM-M-0984 .stage1-worker-selftest.json
  exit 0; no output
```

The frozen modern target's machine proof cut set is closed by this phase,
pending master acceptance. This does not resolve `M0984-X-SOURCE`: the terse
source row still does not establish that this modern Banach-valued theorem is
the intended historical Borel 1909 theorem. Human-source/readability review,
hermetic and independent validation, release, and theorem completion remain
open and are not claimed.
