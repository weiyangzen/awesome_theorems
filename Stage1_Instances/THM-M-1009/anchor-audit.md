# Anchor audit record

Item: `S56-M-1009-ANCHOR_AUDIT`  
Base revision: `73ef7b942ea9b981648b4c8bc90d810d9a5340a5`  
Audit date: 2026-07-12

## Target and immutable inputs

The audit compares candidates with the statement-phase declaration
`Stage1Instances.THM_M_1009.ErdosRenyiLowerBoundTarget`, expression SHA-256
`5933a50ff097d2de1336a67d4671b3caf7add728d2be6f8be22f95a0385dec1f`.
The available mathlib checkout is pinned at
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (Lean 4.29.0). No dependency was
updated, cloned, or fetched.

## Candidate classification

| Candidate | Exact source | Assessment |
|---|---|---|
| Independent second Borel-Cantelli | `Mathlib.Probability.BorelCantelli`, `ProbabilityTheory.measure_limsup_eq_one`, line 69 | Checked nearby anchor. Its independence premise and measure-one conclusion do not match the arbitrary-event pairwise-ratio lower bound. |
| Levy generalized Borel-Cantelli | `Mathlib.Probability.Martingale.BorelCantelli`, `MeasureTheory.ae_mem_limsup_atTop_iff`, line 341 | Checked nearby anchor. It is a filtration/conditional-expectation characterization, not the target inequality. |
| First Borel-Cantelli | `Mathlib.MeasureTheory.OuterMeasure.BorelCantelli`, `MeasureTheory.measure_limsup_atTop_eq_zero`, line 62 | Checked nearby anchor in the opposite, summable regime. |
| Legacy repository module | `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_289.lean` at the base revision, SHA-256 `796365fe...a867` | Audit-only artifact. It wraps the nearby anchors and explicitly leaves the terminal theorem as formalization debt. |

The first two mathlib source files have SHA-256 values `e0d1d942...500e` and
`8d5c454b...ee97`, respectively. The full hashes and mismatch explanations are
recorded in `anchor-audit.json`.

Repository-local searches covered Erdos/Renyi/Kochen/Stone spellings,
Borel-Cantelli declarations, limsup declarations, and the legacy module.
Public GitHub repository-search probes for `Kochen-Stone Lean theorem`, `Erdos
Renyi Borel Cantelli Lean`, and `BorelCantelli language:Lean` returned zero
repositories. GitHub code search was not authenticated and grep.app returned
HTTP 429, so this is a bounded discovery audit, not a proof that no external
formalization exists. No credible external Lean 4 terminal body was identified
and therefore there is nothing to pin or integrate.

## Validation

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1009/AnchorAudit.lean` | 0 | all four exact nearby declaration names and types elaborate against pinned mathlib |
| `python3 -m json.tool Stage1_Instances/THM-M-1009/anchor-audit.json >/dev/null` | 0 | structured audit is valid JSON |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -n -i 'erdos|erdős|renyi|rényi|kochen|borel.?cantelli' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems` | 0 | only nearby Borel-Cantelli infrastructure, unrelated names, and the legacy audit artifact were found |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard and 1546-target projection valid |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique uniform-L0 targets valid |
| `python3 scripts/stage1_target.py show THM-M-1009` | 0 | rank 289, planned, legacy artifacts unaccepted, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-1009` | 0 | no whitespace errors |

The anchor-audit node is self-tested, but the theorem is not proved. The root
remains `H1 / M3 / R3`; proof, human-source, obligation-tree, validation, and
release gates remain open.
