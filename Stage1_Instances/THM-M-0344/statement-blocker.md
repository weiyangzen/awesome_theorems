# Exact-statement gate: blocked

Item: `S56-M-0344-STATEMENT`  
Theorem: `THM-M-0344`  
Base revision: `bd0d227173ac95971603f633607751754850337e`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
Its entire mathematical wording is `函数与其傅里叶变换不能同时集中` ("a function and its
Fourier transform cannot both be concentrated"). Stage0 explicitly leaves the precise definitions
and hypotheses open. The metadata value `已验证` is untrusted inventory metadata, not a source
statement or kernel receipt.

The phrase is compatible with inequivalent theorem families, including a variance or second-moment
lower bound, a support-size or simultaneous-support rigidity theorem, a quantitative mass
concentration inequality, and an entropic uncertainty inequality. These alternatives require
different function spaces, hypotheses, Fourier normalizations, constants, conclusions, and
boundary cases. Even within the variance reading, the record does not select `ℝ` versus `ℝ^n`,
integrable/Sobolev versus Schwartz functions, centered versus uncentered moments, normalization of
the nonzero function, the Fourier kernel and its `2π` convention, or the treatment of infinite
moments and equality cases.

Selecting the familiar Heisenberg variance inequality would therefore substitute a nearby theorem,
not elaborate the exact repository target. It would also risk conflating this harmonic-analysis
entry with the separately catalogued quantum-mechanical Heisenberg uncertainty entries. Selecting
Hardy's uncertainty principle is expressly excluded because it is the distinct target
`THM-M-0345`.

Consequently there is no canonical human proposition from which to derive a minimal import, ordered
Lean binders, an elaborated expression fingerprint, checked alternate transports, or meaningful
removed-hypothesis, changed-domain, binder-scope, and boundary mutations. Section 5.1 of the
rev-5.6 blueprint fails at exact source-statement identity before proof evidence may be inspected.
Machine state remains `M4`; statement and theorem completion are false.

## Pinned Lean boundary

The existing `IntakeProbe.lean` imports `Mathlib.Analysis.Fourier.LpSpace` and checks the ordinary
Fourier integral, real Fourier character, `L2` Fourier isometry and norm preservation, and Schwartz
Fourier compatibility. It re-elaborates successfully in the pinned environment. These declarations
show that several candidate encodings have Fourier infrastructure; none defines "concentrated" or
selects a canonical uncertainty proposition. The probe is not a target statement and receives no
statement or proof credit.

A narrow source search of pinned mathlib found no declaration text explicitly naming a Fourier or
Heisenberg uncertainty principle. This limited result is not the later immutable anchor audit. No
`sorry`, `admit`, or `axiom` occurs in the target's Lean source.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The existing canonical `.lake` link and artifacts were
used read-only. No update, build, clone, fetch, or dependency mutation was run.

## Validation evidence

Commands ran in this worker clone on `2026-07-12` (`Asia/Shanghai`).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0344` | 0 | rank 837; planned; legacy artifacts unaccepted; theorem incomplete |
| `rg -n -C 5 'THM-M-0344\|不确定性原理\|函数与其傅里叶变换不能同时集中' Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md Docs/Stage1_Targets_rev-5.6.json` | 0 | only the underspecified catalogue and Stage0 records were found; exact definitions and assumptions remain open |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at the commit above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | hashes `651c8acc...b1d2` and `321626c8...2d81`, recorded in the JSON blocker |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision above |
| `rg -n -i 'uncertainty principle\|heisenberg uncertainty\|uncertainty.*fourier\|fourier.*uncertainty' Formalizations/Lean/.lake/packages/mathlib/Mathlib -g '*.lean'` | 1 | no matching declaration text; no-match exit is expected and does not claim an exhaustive anchor audit |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0344/IntakeProbe.lean)` | 0 | all five Fourier API checks elaborated; no canonical theorem asserted |
| `rg -n '\b(sorry|admit)\b|^[[:space:]]*axiom\b' Stage1_Instances/THM-M-0344 -g '*.lean'` | 1 | expected no-match exit; no prohibited placeholder or axiom found |
| `python3 -m json.tool Stage1_Instances/THM-M-0344/statement-blocker.json` | 0 | structured blocker is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0344` | 0 | no whitespace errors |

## Retry condition and status boundary

An accountable source reviewer must preserve and hash an immutable primary or standard source,
select and transcribe one exact proposition with a theorem/section and page locator, audit errata,
and independently approve the source-statement crosswalk. The selection must freeze the ambient
space, function class, Fourier convention, exact concentration functional, ordered quantifiers,
hypotheses, constant and conclusion, zero/infinite/boundary behavior, and equality cases. A later
statement worker can then encode that same proposition using real Lean definitions, minimize its
pinned imports, serialize and hash the elaborated expression, check any alternate transports, and
run all four required mutation classes.

This is the first failed gate, not completion of the statement node or any downstream node. The
root remains `[H3, M4, R4]`, with `audit_complete: false` and `theorem_complete: false`. The assigned
phase is not genuinely self-tested, so no `.stage1-worker-selftest.json` is emitted.
