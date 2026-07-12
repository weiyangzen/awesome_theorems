# THM-M-0987 validation phase

Item: `S56-M-0987-VALIDATION`. Base revision:
`592758f4f7e1dc72b9862272624df38bd92621c2`.

Validation ran in the worker clone on 2026-07-12. It reused the canonical
pinned Lake artifacts and did not update, build, fetch, clone, or otherwise
mutate `.lake`. The exact proof root, its checked final composition, the
terminal mathlib theorem, and a separately transcribed exact target all reached
the Lean kernel. Every printed declaration reported only `propext`,
`Classical.choice`, and `Quot.sound`; none reported `sorryAx`.

```text
python3 Stage1_Instances/THM-M-0987/check_validation.py
  exit 0
  ok: exact frozen root, proof composition, and independent exact transcription kernel-replayed
  ok: observed axioms are propext, Classical.choice, and Quot.sound; no sorryAx
  ok: frozen hashes, denominator, recipe, placeholder policy, and clean pinned mathlib passed
  blocked: frozen state predates proof closure; cold hermetic and distinct-runner gates remain open

python3 Stage1_Instances/THM-M-0987/check_proof.py
python3 Stage1_Instances/THM-M-0987/check_obligation_tree.py
python3 Docs/tools/check_stage1_standard.py
python3 scripts/stage1_target.py check
python3 scripts/stage1_target.py show THM-M-0987
python3 -m json.tool Stage1_Instances/THM-M-0987/validation-phase-spec.json
python3 -m json.tool Stage1_Instances/THM-M-0987/validation-receipt.json
git diff --check -- Stage1_Instances/THM-M-0987 .stage1-worker-selftest.json
  all exit 0
```

The validator invokes the pinned Lean executable obtained through `lake env`
and copies all four modules into a fresh temporary directory under
`Formalizations/Lean`; temporary `.olean` files are removed afterward. The
environment is Lean 4.29.0 commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740` and clean mathlib commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The terminal source is
`Mathlib/Probability/CentralLimitTheorem.lean`, SHA-256
`4b42bad9589ec3772fe0e884ad70789c89fd0c11566d980f3df1c862bbc7f03d`.

This is truthful nonrelease validation, not full rev-5.6 release evidence. The
frozen typed graph predates proof closure and still records M3, so master
reconciliation is required. The shared warm cache is not an empty-cache cold
hermetic/offline replay. The independent transcription ran in the same clone
and cache, so it is not a second independently provisioned verifier. Complete
transitive provenance, TCB/SBOM closure, accepted H0/R0 reviews, deterministic
signed receipts, release, and master acceptance remain open. No E0/E1, M0,
audit completion, theorem completion, or release is claimed.
