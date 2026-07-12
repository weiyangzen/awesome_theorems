# THM-M-0529 proof-phase validation

Item: `S56-M-0529-PROOF`  
Date: `2026-07-12` (Asia/Shanghai)  
Base revision: `b66051ed23f34189439dcb4870867d0d33fe9564`

## Implemented proof

`Proof.lean` closes the exact frozen proposition. `homeomorphismHomIsIso` exposes the `IsIso`
instance carried by the hom of `TopCat.isoOfHomeo e`. `integralSingularHomologyMapIsIso` then
instantiates functorial preservation for the exact degreewise integral singular-homology functor.
`homologyIsHomeomorphismInvariant` is the explicit child-to-root composition certificate.

This closes the frozen machine proof cut without weakening the domain, changing coefficients, or
replacing the map-level conclusion. It does not claim full theorem completion: human-source,
readable reconstruction, validation, independent verification, release, and master acceptance are
downstream gates.

## Exact validation

The commands below ran in the worker clone. Existing canonical pinned `.lake` artifacts were reused;
no update, build, clone, or fetch was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets pass. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets, ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-0529` | 0 | Rank 586; planned; theorem incomplete. |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0529/Statement.lean` | 0 | Frozen exact target re-elaborated. |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0529/ObligationTree.lean` | 0 | Frozen conditional composition re-elaborated. |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0529/Proof.lean` | 0 | Three proof declarations elaborated; axiom probes report only `propext`, `Classical.choice`, and `Quot.sound`. |
| `python3 Stage1_Instances/THM-M-0529/check_proof.py` | 0 | Receipt, source hash, exact declarations, obligations, and prohibited-token checks pass. |
| `git diff --check -- Stage1_Instances/THM-M-0529 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; `lean-toolchain` SHA-256
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`;
`lake-manifest.json` SHA-256
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

Status boundary: genuine self-tested proof-phase closure pending integration-lane acceptance. This
receipt supplies no validation-phase or theorem-release claim.
