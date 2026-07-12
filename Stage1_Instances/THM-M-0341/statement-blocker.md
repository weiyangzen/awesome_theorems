# Statement-phase blocker

Item: `S56-M-0341-STATEMENT`  
Base revision: `230f719da7724afb27c761dcb8c62a327557fe63`

## First failed gate

The exact-source statement gate fails. The only repository source wording for `THM-M-0341` is
`傅里叶变换的逆变换` ("the inverse transform of the Fourier transform"). It supplies no domain,
codomain, transform normalization, hypotheses, inversion direction, or equality mode. Stage0 also
marks the precise definitions and prerequisites as `待补充` (to be supplied). Thus there is no exact
human claim from which the ordered binders and canonical Lean proposition can be derived without
inventing mathematics.

The pinned module `Mathlib.Analysis.Fourier.Inversion` contains the relevant candidate
`MeasureTheory.Integrable.fourierInv_fourier_eq`, with a finite-dimensional real inner-product-space
domain, complex normed codomain, integrability of both `f` and `𝓕 f`, continuity at a point, and the
pointwise conclusion `𝓕⁻ (𝓕 f) v = f v`. Selecting it would add all of those choices to the source
record. Other materially different candidates (global continuous-function equality, reverse-order
inversion, almost-everywhere or `L2` inversion, and Fourier-series inversion) remain possible. The
mathlib declaration is therefore discovery evidence, not an exact encoding of the repository claim.

No canonical declaration/expression, statement fingerprint, checked transport, or mutation result
is recorded. No `sorry`, axiom, placeholder, broadened theorem, or substituted theorem was added.
The task remains blocked, and no worker self-test manifest is emitted.

## Narrow validation evidence

The existing shared `.lake` artifact was only inspected; no dependency update, fetch, clone, or
build was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0341` | exit 0; rank 834, planned, legacy artifacts unaccepted, theorem_complete false |
| `rg -n -C 5 '傅里叶变换反演公式\|傅里叶变换的逆变换' Docs Stage0* Formalizations ...` | exit 0; only `Docs/researches/math_theorems.md` and its Stage0 projection contain the source wording; both omit an exact theorem |
| `sed -n '145,220p' Formalizations/Lean/.lake/packages/mathlib/Mathlib/Analysis/Fourier/Inversion.lean` | exit 0; inspected the four pinned pointwise/function-equality candidates and their explicit hypotheses |

## Retry condition

Provide or locate an authoritative source passage with an immutable edition and theorem/page that
fixes the domain, normalization, ordered assumptions, inversion direction, equality mode, and
boundary cases. Then crosswalk that passage to one exact Lean proposition, minimize its pinned
imports, elaborate it with `lake env lean`, and mutation-test its material assumptions.

Status boundary: this artifact establishes an actionable statement blocker only. It does not accept
the statement phase and makes no audit-completion or theorem-completion claim.
