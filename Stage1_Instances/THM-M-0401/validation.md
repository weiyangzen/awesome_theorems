# Statement validation

Base revision: `ca5213c506afa21d64fb8f2481ac658887786c6e`.

The validation uses the existing pinned `.lake` dependency artifacts. It does not update, fetch, or otherwise mutate dependencies.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups; 1546 uniform-L0 Lean 4 targets
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets; ranks 1..1546; all L0/rework_required
python3 scripts/stage1_target.py show THM-M-0401
  exit 0: execution rank 14; planned; theorem_complete=false
(cd Formalizations/Lean && lake env lean --version)
  exit 0: Lean 4.29.0; commit 98dc76e3c0a9b856c9b98726b713fb04fab16740
(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0401/Statement.lean)
  exit 0: exact target and iff elaborated; all four guarded mutation failures observed; fully explicit target printed
python3 -m json.tool Stage1_Instances/THM-M-0401/instance.json
  exit 0
git diff --check -- Stage1_Instances/THM-M-0401 .stage1-worker-selftest.json
  exit 0
```

The Lean output is preserved canonically in `normalized-expression.txt`. The check covers statement elaboration only. It does not inspect a proof body, establish source fidelity, close an obligation tree, or support theorem completion.

After that successful check, a replay found that the shared canonical mathlib `.olean` tree had disappeared from the symlinked `.lake` directory and failed with `unknown module prefix 'Mathlib'`. No dependency command was run and no replacement artifact was fetched. The successful scoped elaboration above is the worker self-test evidence; fresh master replay requires restoration of the canonical pinned artifacts.
