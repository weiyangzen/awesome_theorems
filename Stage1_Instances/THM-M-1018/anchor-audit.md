# Anchor audit

Item: `S56-M-1018-ANCHOR_AUDIT`  
Audit date: 2026-07-12  
Base revision: `7ed5103bae419111bef3d397f525a727b98670d3`

## Audit boundary

This phase audits Lean 4 candidates for the exact interval-mass proposition in
`Statement.lean`. It does not substitute characteristic-function uniqueness,
Levy convergence, density inversion, or Fourier inversion under integrability
hypotheses. The manifest pins Lean `v4.29.0` and mathlib commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; the installed mathlib checkout
reports that exact immutable revision and was not changed.

## Pinned and repository-local inventory

| Candidate | Exact module and declaration | Result |
|---|---|---|
| Characteristic-function definition | `Mathlib.MeasureTheory.Measure.CharacteristicFunction.Basic`, `charFun_apply_real` | Confirms mathlib's positive exponential convention. Definition/normalization substrate only. |
| Symmetric characteristic-function integral | `Mathlib.MeasureTheory.Measure.IntegralCharFun`, `integral_charFun_Icc` | Rewrites an unweighted interval integral as a sinc integral. It does not contain the endpoint kernel, interval mass, or limiting conclusion. |
| Tail bound | same module, `measureReal_abs_gt_le_integral_charFun` | Controls a symmetric tail by an integral of `1 - charFun`; it is not an inversion equality. |
| Characteristic-function extensionality | `Mathlib.MeasureTheory.Measure.CharacteristicFunction.Basic`, `Measure.ext_of_charFun` | Proves equality of finite measures from equality of their characteristic functions. This is the uniqueness theorem excluded by the frozen target, not an inversion formula. |
| Fourier inversion | `Mathlib.Analysis.Fourier.Inversion`, `MeasureTheory.Integrable.fourierInv_fourier_eq` and `Continuous.fourierInv_fourier_eq` | Applies to functions whose Fourier transform is integrable. A general probability measure need not have a density or an integrable characteristic function, so no wrapper to the exact root follows. |

`AnchorAudit.lean` kernel-checks these seven representative interfaces at the
pinned revision. A case-insensitive scan of every pinned `Mathlib/**/*.lean`
source found Levy convergence and Levy-Prokhorov material but no declaration
named or documented as Levy inversion. A broader semantic scan found the
adjacent results above and no occurrence combining `charFun` with `Ioc` or an
interval-mass inversion limit. The repository-wide Lean scan outside this
target likewise found no Levy inversion implementation. The local
`LevyInversionTarget` is a proposition definition without a proof body and
receives statement evidence only.

## External Lean 4 search

On 2026-07-12, GitHub repository-metadata searches for `Levy inversion Lean`,
`characteristic function Lean theorem prover`, and `probability characteristic
function Lean4` each returned `total_count: 0` with
`incomplete_results: false`. Anonymous GitHub code search returned HTTP 401,
and grep.app returned HTTP 429; these surfaces are recorded as unavailable and
are not counted as negative evidence. No credible external candidate was
discovered, so there is no external revision or proof body to pin, audit, or
integrate. No dependency was fetched, installed, or added to `.lake`.

## Classification and boundary

No terminal or near-terminal Lean proof of the exact frozen target was found.
The exact root therefore remains open with `M3 / formalization_debt`; this is
not repository-local integration debt because no external closure is known.
The useful route exposed by mathlib starts with Fubini/integral identities and
approximation of the half-open interval kernel, not the stronger density
Fourier inversion theorem. This audit does not establish `H0`, proof closure,
an obligation tree, full audit completion, or theorem completion. Its scoped
candidate inventory is self-tested pending master acceptance.

## Validation receipt

Commands ran from the worker clone on 2026-07-12. The Lean commands used the
existing canonical pinned `.lake` artifacts.

| Command | Exit | Result |
|---|---:|---|
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | returned the exact manifest pin `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -ni --glob '*.lean' 'levy.*inversion\|lévy.*inversion\|inversion.*levy\|charFun.*Ioc\|Ioc.*charFun' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 1 | expected no-match result |
| `lake env lean ../../Stage1_Instances/THM-M-1018/AnchorAudit.lean` from `Formalizations/Lean` | 0 | all seven nearby pinned declarations elaborated and printed |
| `lake env lean ../../Stage1_Instances/THM-M-1018/Statement.lean` from `Formalizations/Lean` | 0 | the exact frozen statement, transport, and mutation probes still elaborated |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets passed |
| `python3 scripts/stage1_target.py show THM-M-1018` | 0 | rank 494, planned, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1018/anchor-audit.json` | 0 | structured audit parsed |
| `git diff --check -- Stage1_Instances/THM-M-1018 .stage1-worker-selftest.json` | 0 | no whitespace errors |
