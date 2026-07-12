# THM-M-0529 validation-phase evidence

Item: `S56-M-0529-VALIDATION`  
Date: `2026-07-12` (Asia/Shanghai)  
Base: `a5b577acd0418260193c05708c0413b040e312a1`

The exact proof root was replayed with pinned Lean 4.29.0 and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. `Validation.lean` does not import `Proof.lean`; it
independently reconstructs the frozen proposition and closes it by explicitly installing the
`TopCat.isoOfHomeo` hom isomorphism and applying `Functor.map_isIso`. Both axiom reports contain
only `propext`, `Classical.choice`, and `Quot.sound`, with no `sorryAx`.

## Commands

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets pass. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets, ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-0529` | 0 | Rank 586, planned, theorem incomplete. |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0529/Proof.lean` | 0 | Exact root and composition elaborate; only the accepted foundation axioms are reported. |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0529/Validation.lean` | 0 | Independent exact-type reconstruction elaborates with the same axiom set. |
| `python3 Stage1_Instances/THM-M-0529/check_validation.py` | 0 | Frozen inputs, seven-node denominator, proof boundary, pins, provenance hashes, trust output, and placeholder scan pass. |
| `python3 -m json.tool` on validation spec, receipt, and self-test manifest | 0 | JSON syntax passes. |
| `git diff --check -- Stage1_Instances/THM-M-0529 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

The worker reused the pre-existing canonical pinned `.lake` symlink without updating or modifying
it. Consequently this is narrow, real kernel and provenance validation, not an empty-cache hermetic
rebuild. The separately implemented probe also ran in the same checkout and shared cache, so it is
not a distinct signed independent-runner attestation. `validation-receipt.json` records these failed
release gates explicitly. No theorem completion or release is claimed.
