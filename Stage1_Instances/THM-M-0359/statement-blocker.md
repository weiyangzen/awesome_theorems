# Exact-statement gate: blocked

Item: `S56-M-0359-STATEMENT`  
Theorem: `THM-M-0359`  
Base revision: `7780ee2963f599a6bf06f39a12c6fddb7eafc914`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
That record supplies only the title "Mihlin multiplier theorem" and the gloss "L^p boundedness of
singular multipliers". It leaves the precise definitions and assumptions explicitly open. It also
attributes the result to Sigurdur Helgason, whereas the standard theorem name refers to S. G.
Mikhlin; this unresolved discrepancy makes the metadata unsuitable as a source statement.

Several inequivalent propositions fit the gloss. In particular, sources use different derivative
cutoffs, pointwise versus annular Sobolev hypotheses, scalar versus operator-valued symbols, and
qualitative bounded-extension versus quantitative norm conclusions. The record fixes neither the
Euclidean dimension nor the exponent range, Fourier normalization, treatment of frequency zero,
dense initial domain, derivative convention, bound constant, endpoint policy, or ordered binders.
Selecting any familiar variant would therefore invent or substitute mathematics rather than
elaborate the assigned theorem.

Consequently there is no canonical expression to serialize or hash, no sound minimal-import claim,
and no meaningful removed-hypothesis, changed-domain, changed-binder-scope, or boundary-case
mutation test. The rev-5.6 statement gate fails at canonical human-claim identity, before proof
evidence may be inspected.

## Pinned Lean boundary

`IntakeProbe.lean` imports `Mathlib.Analysis.Distribution.FourierMultiplier` and
`Mathlib.MeasureTheory.Function.LpSpace.Basic`. It checks mathlib's Fourier multiplier maps on
Schwartz functions and tempered distributions, temperate growth, and basic `L^p` APIs. The probe
re-elaborates successfully, but those declarations neither state a Mihlin derivative criterion nor
provide the claimed `L^p` bounded extension. A scoped pinned-mathlib search found no occurrence of
`Mihlin` or `Mikhlin`. These are interface and discovery observations only, not canonical-statement
or proof credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The existing `.lake` artifacts were used read-only;
no update, build, clone, fetch, or dependency mutation was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0359` | 0 | rank 852, planned, legacy artifacts unaccepted, theorem incomplete |
| `rg -n -i 'THM-M-0359|mihlin|mikhlin|mihlin\u4e58\u5b50|\u5947\u5f02\u4e58\u5b50\u7684L\\^p' Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md Stage1_Instances/THM-M-0359` | 0 | found only the underspecified repository metadata and intake records; Stage0 marks exact definitions and assumptions open |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision recorded above |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | `651c8acc...b1d2` and `321626c8...2d81` |
| `rg -n -i 'mihlin|mikhlin' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 1 | expected no-match exit; no name-specific theorem was found |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0359/IntakeProbe.lean)` | 0 | all eight infrastructure checks elaborated; no canonical theorem target asserted |
| `rg -n '\\b(sorry|admit)\\b|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0359 -g '*.lean'` | 1 | expected no-match exit; no prohibited placeholder or axiom found |

## Retry condition and status boundary

An accountable reviewer must preserve and hash an immutable primary-source edition, transcribe one
exact theorem with all incorporated definitions and assumptions, resolve the attribution, dispose
of errata, and independently approve the mapping. A later statement run can then encode that exact
claim, minimize pinned imports, fingerprint the elaborated expression, check alternate transports,
and execute all four required mutation classes.

This statement node remains `[ ]`, with machine debt `M4`. The root remains `[H3, M4, R4]`;
`audit_complete` and `theorem_complete` remain false. The assigned phase is not genuinely
self-tested, so no `.stage1-worker-selftest.json` is emitted.
