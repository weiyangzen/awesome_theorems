# Anchor audit validation

Item: `S56-M-0342-ANCHOR_AUDIT`  
Base revision: `c9694802ae049af37973e49a65f11b833135333f`

## Result

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` contains an exact usable
candidate in `Mathlib.Analysis.Fourier.LpSpace`: `MeasureTheory.Lp.norm_fourier_eq`. The local
probe introduces the frozen target's `n`, `f`, and `hf`, then closes the same norm equality by
applying that declaration to `hf.toLp f`. The construction anchor
`MeasureTheory.Lp.fourierTransformₗᵢ` and companion `MeasureTheory.Lp.inner_fourier_eq` were also
type-checked on the frozen Euclidean domain.

The source module defines the isometry by `LinearEquiv.extendOfIsometry`, using dense Schwartz
embeddings and `SchwartzMap.norm_fourier_toL2_eq`; `norm_fourier_eq` is then the isometry's
`norm_map`. The checked axiom report for all three declarations is exactly `propext`,
`Classical.choice`, and `Quot.sound`. A source scan found no `sorry`, `admit`, bodyless `axiom`, or
`unsafe` token in `LpSpace.lean` or the searched Fourier modules.

No additional candidate was found among the repository Lean files or already pinned packages.
Public exact-symbol searches were attempted but were not conclusive: GitHub code search returned
HTTP 401 without authentication and grep.app returned HTTP 429. This is recorded as a search
limitation, not as evidence that no external candidate exists. No dependency update, fetch, clone,
or `.lake` mutation was performed.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0342` | 0 | rank 835; planned; theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg` exact declarations in pinned mathlib and repository Lean files | 0 | norm, isometry, and inner-product anchors located; one legacy local usage found but not credited |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0342/AnchorAudit.lean` | 0 | exact norm probe and inner-product specialization elaborated; three axiom reports printed |
| placeholder/axiom/unsafe `rg` scan of pinned `LpSpace.lean` and Fourier modules | 1 (expected) | no prohibited token matched |
| `python3 -m json.tool Stage1_Instances/THM-M-0342/anchor-audit.json` | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0342` | 0 | no whitespace errors |

## Status boundary

This phase truthfully establishes a pinned, exact-type mathlib anchor and its immediate body and
axiom provenance. It does not promote machine state: the defensible result is an `M0-W` candidate
pending downstream obligation, transitive trust/provenance, proof, and master-acceptance gates.
`H1` remains because the historical primary-source passage and normalization crosswalk are open;
`R3` remains because no accepted readable proof reconstruction exists. `audit_complete=false` and
`theorem_complete=false`.
