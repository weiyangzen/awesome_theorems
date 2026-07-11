# THM-M-0403 proof-phase validation

## Implemented bodies

`Proof.lean` supplies real local proof bodies for the one-term branch, the
complete two-term branch, and its index-injectivity argument. It also checks
the exact binder-level composition from a terminal finite-zero-set theorem to
the canonical `SchlickeweiEvertseStatement`.

The terminal ESS finite-rank multiplicative-group theorem is not present in
the pinned Lean closure and is not postulated here. The composition theorem
keeps it as an explicit premise. The arity-at-least-three induction step,
scalar extension, group-equation reduction, degeneracy split, proper-subsum
construction, and their composition remain open. Consequently no frozen
obligation is marked closed, the root remains `M4`, and theorem completion is
not claimed.

## Commands and results

Commands ran from base revision
`b38353d62a9d55f41b9a0f70eb889ff9af6a9fe9` on 2026-07-12 (validation
timestamp `2026-07-11T19:41:03Z` UTC).

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0403
  exit 0: execution rank 16; planned; theorem_complete=false

cd Formalizations/Lean &&
  bash ../../Stage1_Instances/THM-M-0403/check_proof.sh
  exit 0: Statement.lean and Proof.lean elaborated; every printed proof
  declaration reports only propext, Classical.choice, and Quot.sound

cd Formalizations/Lean && lake env lean --version
  exit 0: Lean 4.29.0, commit 98dc76e3c0a9b856c9b98726b713fb04fab16740

git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD
  exit 0: 8a178386ffc0f5fef0b77738bb5449d50efeea95

rg -n '\b(sorry|admit)\b|^[[:space:]]*axiom\b|^[[:space:]]*unsafe\b' \
  Stage1_Instances/THM-M-0403/Proof.lean
  exit 1 with empty output: pass, no prohibited declaration or placeholder

python3 -m json.tool Stage1_Instances/THM-M-0403/proof-receipt.json >/dev/null
  exit 0: proof receipt is valid JSON

git diff --check -- Stage1_Instances/THM-M-0403 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

The check script uses temporary local `.olean` files and removes them on exit.
No update, build, clone, fetch, or mutation of `.lake` was performed. This is
a truthful partial proof-phase result pending master acceptance; validation
and release remain separate downstream items.
