# Exact-statement elaboration blocker

Item: `S56-M-0375-STATEMENT`

Base revision: `562c428c3d520ab42bba305174b7cad9409d7c0b`

## Verdict

The exact Lean 4 target cannot be truthfully selected from the repository's source record. The
statement phase is blocked and no canonical proposition, declaration, expression hash, mutation
result, or statement-completion receipt is claimed.

The complete repository claim is the title `restriction theorem`, the attribution Elias Stein,
the year 1986, and the gloss "restriction of the Fourier transform to a surface". It does not fix:

- the surface, its dimension, or its measure;
- the Fourier-transform convention and underlying scalar field;
- the input function class and treatment of almost-everywhere representatives;
- the source and target exponents or endpoint policy;
- the norm inequality, constant dependence, or restriction/extension orientation; or
- a bibliographic work, edition, theorem number, page, assumptions, or errata record.

These choices change the mathematical proposition. In particular, choosing the Stein-Tomas sphere
estimate would be a substantive narrowing rather than elaboration of the recorded text. The source
inventory reinforces the ambiguity by listing a distinct, partially solved `Fourier restriction
conjecture` immediately afterward with the identical gloss. No repository artifact resolves the
two entries into an exact proposition.

## Minimal-import check

The existing `IntakeProbe.lean` elaborates with the three pinned imports below:

```lean
import Mathlib.Analysis.Fourier.FourierTransform
import Mathlib.MeasureTheory.Constructions.HaarToSphere
import Mathlib.MeasureTheory.Function.LpSeminorm.Basic
```

This checks only the availability of possible Fourier, sphere-measure, measure, and `Lp` APIs. It
is not an exact-target elaboration and provides no statement or proof credit.

## Validation record

Commands were run from the repository root unless a working directory is shown.

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `15` assurance groups and `1546` uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `1546` unique targets, ranks `1..1546`, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0375` | 0 | rank `867`, lifecycle `planned`, legacy artifacts unaccepted, theorem completion false |
| `git status --short` | 0 | only `?? Formalizations/Lean/.lake`; this is the clone's canonical shared artifact and was not modified |
| `git rev-parse HEAD` | 0 | `562c428c3d520ab42bba305174b7cad9409d7c0b` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0375/IntakeProbe.lean)` | 0 | all seven API checks elaborated under the pinned environment |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `rg -n 'restriction theorem\|restriction 定理\|傅里叶变换在曲面上的限制' Docs Stage1_Instances/THM-M-0375` | 0 | found only metadata/gloss repetitions and the fail-closed intake dossier; no exact proposition or pinpoint source |

## First failed gate

The rev-5.6 target-freeze gate fails at exact human-claim identification. The actionable unblocker
is an independently reviewable primary or authoritative source passage that selects one theorem and
fixes every parameter above. Only then can this phase encode that proposition, minimize imports,
elaborate it, fingerprint the expression and environment, and mutation-test its boundaries.

Because that input is absent, `.stage1-worker-selftest.json` is intentionally not written. This
file is blocker evidence only and is not a node-specific completion receipt or master acceptance.
