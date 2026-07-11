# THM-M-0393 validation-phase execution

Item: `S56-M-0393-VALIDATION`

Base revision: `518315d81e5e2006972fb32b395e2a3a91d55b92`

Validation timestamp: `2026-07-11T19:38:51Z`

The validation phase reran the only proof-phase body, the finite-choice subclaim
inside `M0393-N1`. `Validation.lean` reconstructs the identical proposition
independently without importing `Proof.lean`. `check_validation.py` separately
checks the frozen input hashes, proof-receipt scope, all 17 registry identities,
proof-graph reachability, open compositions and root, dependency pins, and local
placeholder policy.

All commands ran from the repository root unless a working directory is shown.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0393
  exit 0: execution rank 6; planned; theorem_complete=false

python3 Stage1_Instances/THM-M-0393/validate_obligation_tree.py
  exit 0: 17 obligations, 16 proof edges, 6 workflow tasks; root M4/open

(cd Formalizations/Lean && lake env lean \
  ../../Stage1_Instances/THM-M-0393/Proof.lean)
  exit 0: finite_pow_divisors depends on propext, Classical.choice, Quot.sound

(cd Formalizations/Lean && lake env lean \
  ../../Stage1_Instances/THM-M-0393/Validation.lean)
  exit 0: independent_finite_pow_divisors has the identical proposition and
  depends on propext, Classical.choice, Quot.sound

python3 Stage1_Instances/THM-M-0393/check_validation.py
  exit 0: independent M0393-N1 finite-choice replay passed; root H3/M4/R3 open

(cd Formalizations/Lean && lake env lean \
  ../../Stage1_Instances/THM-M-0393/Statement.lean)
  exit 1: the pre-existing evalBinary definition depends on a noncomputable
  instance but is not marked noncomputable

python3 -m json.tool \
  Stage1_Instances/THM-M-0393/validation-receipt.json >/dev/null
  exit 0

rg -n '\b(sorry|admit)\b|^[[:space:]]*(axiom|unsafe)\b' \
  Stage1_Instances/THM-M-0393/{Proof,Validation}.lean
  exit 1 with empty output: pass, no prohibited local declaration or placeholder

git diff --check -- Stage1_Instances/THM-M-0393 .stage1-worker-selftest.json
  exit 0 with no output
```

No update, build, fetch, clone, or network operation was performed. The existing
pinned Lean 4.29.0 toolchain and canonical `.lake` reuse were not modified.

This is truthful validation of a partial lemma, not successful root validation.
The first failed node gate is the proof dependency: the gcd-to-power bridge, 16
other obligations, all composition certificates, and the exact Thue root remain
open. The statement replay defect also remains explicitly recorded rather than
being repaired during validation. This worker did not perform an empty-cache
cold build, offline archive restoration, supply-chain bundle, or separately
provisioned signed verification. `audit_complete=false` and
`theorem_complete=false`; the root vector remains `[H3, M4, R3]`.
