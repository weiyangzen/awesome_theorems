# Anchor-audit validation record

Item: `S56-M-0152-ANCHOR_AUDIT`  
Base revision: `0091960f0657f8228ab5c8e3ca414cefd6c90931`

## Result

The audit is bound to the frozen expression
`Stage1Instances.THM_M_0152.TheoremaEgregiumTarget`, statement file hash
`411162ea...058d`, and mathlib revision `8a178386...e95`. The local exact artifact is a
proposition definition, not a proof. Pinned mathlib supplies Frechet-calculus, cross-product, and
Riemannian-metric substrate, but its source has no Gaussian-curvature, sectional-curvature,
Riemann-curvature, fundamental-form, or Theorema-Egregium declaration.

The strongest external anchor found is
`qinz1yang/differential-geometry@0f6734e222fd5e0b86c1ff02c2f5abde4c65e163`. Its
`metricRm04Std_pullback` proves intrinsic Riemann-curvature naturality for a pullback metric under
a global diffeomorphism, and its adjacent API defines sectional curvature. This is not the frozen
target: the latter uses regular parametrized surfaces, a local coordinate equivalence, and an
extrinsic `(LN-M^2)/(EG-F^2)` formula. No Gauss-equation bridge or local wrapper joining those
encodings was located. The candidate is not in the pinned dependency closure, and its tree also
contains unrelated proof placeholders, so neither integration nor transitive trust is credited.

The exact root therefore remains `M4`. Candidate C03 is an immutable `M3` anchor only, not `M1`:
it has not been independently built and axiom-audited, and does not prove the exact statement.
Negative results are bounded to the recorded terms and search surfaces, not a claim of global
nonexistence.

## Commands and results

Commands ran on 2026-07-12 in this worker clone. Existing pinned `.lake` artifacts were used; no
dependency update, build, clone, or fetch was performed.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0152/AnchorAudit.lean` | 0 | all eight pinned mathlib substrate declarations elaborated |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0152/Statement.lean` | 0 | exact frozen target and definitional transport re-elaborated |
| `python3 Stage1_Instances/THM-M-0152/check_anchor_audit.py` | 0 | target hashes, manifest pin, installed mathlib HEAD, probes, candidates, and M4 boundary agreed |
| exact-term `rg` over `Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | no Gaussian/sectional/Riemann curvature, fundamental-form, or Egregium declaration; exit 1 is expected no-match |
| GitHub repository API searches for `Gaussian curvature language:Lean` and `Theorema Egregium Lean` | 0 | both complete responses had `total_count=0`; response SHA-256 `08c082fd...600b2` |
| GitHub repository API search for `differential geometry language:Lean` | 0 | eight repositories returned; complete response SHA-256 `31e21cbd...4cf8` |
| GitHub commit/tree/raw-source inspection of `qinz1yang/differential-geometry@0f6734e...e163` | 0 | immutable commit, Lean 4.29.0, mathlib v4.29.0, Apache-2.0, exact modules/declarations, source hashes, and placeholder boundary recorded |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard valid with 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0152` | 0 | rank 651, planned, L0/rework-required, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-0152 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Open integration gate

Reopen upon finding an immutable exact theorem or a Gauss-equation bridge sufficient to connect
the intrinsic external candidate to the frozen extrinsic local target. Any such candidate still
requires exact-type normalization, pin/import/check evidence, transitive dependency and axiom
closure, placeholder and unsafe/oracle scans, license review, and a checked local wrapper.

