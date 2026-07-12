# Statement-phase blocker

Item: `S56-M-0360-STATEMENT`  
Validation date: 2026-07-12 (Asia/Shanghai)  
Base revision: `7780ee2963f599a6bf06f39a12c6fddb7eafc914`

## Verdict

The exact Lean 4 target cannot be truthfully frozen from the available source record. The
repository supplies only the label "Herz-Stein theorem", the gloss "Hardy-space multipliers", an
attribution to Carl Herz and Elias Stein, and the year 1968. It supplies no bibliographic title,
theorem number, page, verbatim claim, or definitions. These fields do not determine the ambient
space, Hardy-space model, exponent range, multiplier condition, normalization, conclusion, or
constant dependencies.

Repository-wide source search found no additional local statement. A bibliographic search for
Carl Herz's works around 1968 returned *Lipschitz Spaces and Bernstein's Theorem on Absolutely
Convergent Fourier Transforms* (DOI `10.1512/iumj.1969.18.18024`), not a paper matching the supplied
Hardy-space multiplier description or a joint Herz-Stein source. The previously identified 1974
Herz paper *Generalisations de la notion des classes Hp de Hardy* also disagrees with the supplied
year and has not been established as the intended theorem. Search results are discovery evidence,
not a substitute for an inspected primary theorem.

Per the rev-5.6 hard-stop rule, inventing a convenient Fourier-multiplier proposition or replacing
the unresolved claim with a nearby mathlib declaration is forbidden. Therefore no canonical Lean
declaration, elaborated-expression hash, or statement receipt is emitted. The existing
`IntakeProbe.lean` remains only an API discovery probe and is not statement evidence.

## Validation evidence

Commands were run from the repository root. The pre-existing untracked
`Formalizations/Lean/.lake` entry is the canonical pinned artifact link and was not modified.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups and exactly 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0360` | 0 | rank 853, `L0 / rework_required`, planned, theorem incomplete |
| `rg -n -i 'Herz.?Stein\|Hardy.space.*multiplier\|multiplier.*Hardy.space' . --glob '!Formalizations/Lean/.lake/**' --glob '!Docs/Stage1_Blueprint_rev-5.6.md' --glob '!Docs/Stage1_Execution_DAG_rev-5.6.json' --glob '!Docs/Stage1_Targets_rev-5.6.json'` | 0 | only the existing THM-M-0360 intake dossier and generic Stage0 metadata matched; no exact local source statement was found |
| OpenAlex author/work query for Carl Herz, publication dates 1960-01-01 through 1980-12-31 | 0 | the 1968 result was the unrelated Lipschitz/Bernstein paper; no matching joint 1968 Herz-Stein Hardy-space multiplier source appeared |
| `git status --short` | 0 | before this artifact, only `?? Formalizations/Lean/.lake` was present |

No `lake env lean` statement check is possible: there is no source-faithful proposition to
elaborate. This is a mathematical identity blocker, not a missing Lean dependency.

## Retry condition and status boundary

Retry only after locating and inspecting an immutable primary source that resolves the attribution
and provides a numbered theorem (or exact page), definitions, assumptions, exponent/dimension
range, normalization, conclusion, constants, and relevant errata. The next attempt must transcribe
that theorem, crosswalk every binder and hypothesis, elaborate it with minimal pinned imports, and
mutation-test its statement boundaries.

First failed gate: exact human statement and source-identity freeze. Current vector remains
`H3 / M4 / R4`; audit completion and theorem completion remain false. This phase is blocked and is
not self-tested, so no `.stage1-worker-selftest.json` is created.
