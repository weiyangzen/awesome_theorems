# THM-M-0002 proof-phase validation

## Implemented proof

`Proof.lean` imports the exact `FiveLemmaTarget` frozen in `Statement.lean`. The canonical wrapper
constructs `Mono (app' phi 2)` from the left truncation with
`mono_of_epi_of_mono_of_mono`, constructs `Epi (app' phi 2)` from the right truncation with
`epi_of_epi_of_epi_of_mono`, and applies `isIso_of_mono_of_epi`. Thus the proof exposes the two
branches and truncation transports frozen by the obligation architecture instead of substituting a
narrower theorem or merely citing the upstream five-lemma wrapper.

The source has no `sorry`, `admit`, new axiom, unsafe declaration, or changed target. Lean reports
only `propext`, `Classical.choice`, and `Quot.sound`. This closes the proof-phase root provisionally,
pending master acceptance. Validation and release are separate nodes, so theorem completion is not
claimed.

## Commands and results

Commands ran from base revision `7f37aede8deed3f04e9935b15aa37bf42ecd950e` on 2026-07-12
(receipt timestamp `2026-07-11T23:12:05Z` UTC).

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0002
  exit 0: execution rank 97; planned; theorem_complete=false

cd Formalizations/Lean &&
  bash ../../Stage1_Instances/THM-M-0002/check_proof.sh
  exit 0: isolated Statement.olean and Proof elaboration passed; the wrapper
  reports propext, Classical.choice, and Quot.sound

python3 Stage1_Instances/THM-M-0002/check_proof.py
  exit 0: exact frozen target, both truncation branches, both four lemmas, and
  final Mono/Epi composition found; prohibited source-token scan passed

cd Formalizations/Lean && lake env lean --version
  exit 0: Lean 4.29.0, commit 98dc76e3c0a9b856c9b98726b713fb04fab16740

git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD
  exit 0: 8a178386ffc0f5fef0b77738bb5449d50efeea95
```

No update, build, clone, fetch, or mutation of `.lake` was performed. The isolated `.olean` was
deleted by the command trap.
