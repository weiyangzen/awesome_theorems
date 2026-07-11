# THM-M-0398 proof-phase validation

## Implemented bodies

`Proof.lean` implements the elementary constant-normalization part of the
frozen proof interface. `finite_exceptional_mono_constant` proves that
finiteness for a constant `C` descends to any `C' <= C`, using positivity of
the normalized rational denominator. The module also rechecks the exact
constant-one composition from `FiniteExceptionalWithConstant` to the
canonical `ThueSiegelRoth` root.

These are real proof bodies, but neither constructs nor assumes Roth's
auxiliary polynomial, index/nonvanishing theorem, upper and lower estimates,
or the terminal uniform finiteness engine. Obligations `M0398-N1`,
`M0398-C1`, `M0398-C2`, `M0398-L1` through `M0398-L4`, and the root remain
open. Root status stays `M3`; theorem completion is not claimed.

## Commands and results

Commands ran from base revision
`5e34bb84b4b5122c40ec88ebb411d9499433e123` on 2026-07-12 (validation
timestamp `2026-07-11T19:48:20Z` UTC).

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0398
  exit 0: execution rank 11; planned; theorem_complete=false

cd Formalizations/Lean &&
  bash ../../Stage1_Instances/THM-M-0398/check_proof.sh
  exit 0: Statement, ObligationTree, and Proof elaborated in an isolated
  temporary directory; both new declarations report only propext,
  Classical.choice, and Quot.sound

python3 Stage1_Instances/THM-M-0398/check_obligation_tree.py
  exit 0: 15 obligations and 29 typed edges passed; root explicitly open M3

cd Formalizations/Lean && lake env lean --version
  exit 0: Lean 4.29.0, commit 98dc76e3c0a9b856c9b98726b713fb04fab16740

git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD
  exit 0: 8a178386ffc0f5fef0b77738bb5449d50efeea95

rg -n '\b(sorry|admit)\b|^[[:space:]]*axiom\b|^[[:space:]]*unsafe\b' \
  Stage1_Instances/THM-M-0398/Proof.lean
  exit 1 with empty output: pass, no prohibited declaration or placeholder

python3 -m json.tool Stage1_Instances/THM-M-0398/proof-receipt.json >/dev/null
  exit 0: proof receipt is valid JSON

git diff --check -- Stage1_Instances/THM-M-0398 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

No update, build, clone, fetch, or mutation of `.lake` was performed. The
temporary `.olean` files were removed by the command trap. This is truthful
partial proof execution pending master acceptance; validation and release are
separate downstream phases.
