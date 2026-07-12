# THM-M-1199 exact-statement gate: blocked

Item: `S56-M-1199-STATEMENT`  
Base revision: `61ca1390cc0fcf06937f303c775c22372db31ad7`

## Decision

The exact Lean 4 target cannot be truthfully frozen or elaborated from the accepted intake and the
repository source record. The entire mathematical wording is "shock waves of conservation-law
equations" (`守恒律方程的激波`). This names a broad theory, not a proposition with fixed binders,
hypotheses, and conclusion. No primary source, edition, theorem/page locator, exact transcription,
definition reference, convention ledger, or errata decision is present.

Materially inequivalent readings include a Rankine-Hugoniot jump law, existence for a Riemann
problem, formation of shocks from smooth data, entropy admissibility, uniqueness, propagation, and
stability. The repository does not fix scalar versus system, space dimension, flux and its
regularity or convexity/hyperbolicity, weak-solution and trace definitions, initial/boundary data,
shock geometry, admissibility condition, time range, solution class, conclusion, or degenerate
cases. Selecting any of these would invent mathematics absent from the source. In particular,
substituting adjacent target `THM-M-1200` (Rankine-Hugoniot) or `THM-M-1201` (entropy condition)
would broaden or replace this target rather than elaborate it exactly.

The scoped repository search found only the terse source row and its generated metadata. The
pinned mathlib source search found no textual candidate for shock-wave, Rankine-Hugoniot, entropy-
solution, or scalar-conservation-law declarations. That negative search is boundary evidence only;
it is not the downstream anchor audit and cannot resolve the missing human claim.

First failed gate: rev-5.6 exact source-statement identification, before canonical Lean
elaboration. The node remains open at `M4`. There is no canonical declaration, expression
fingerprint, minimal exact-target import set, checked alternate transport, or meaningful
removed-hypothesis/domain/binder-scope/boundary mutation suite. No statement acceptance, proof
credit, audit completion, or theorem completion is claimed.

## Required unblock

An accountable source reviewer must select one immutable primary-source theorem and record its
edition, exact theorem/page locator, definitions, full premise-to-conclusion transcription,
conventions, and errata. The review must freeze the equation and domains, state and flux spaces,
regularity and structural assumptions, weak/admissible solution notion, ordered binders,
conclusion, and boundary cases, while explaining why that theorem faithfully represents this
repository item rather than `THM-M-1200` or `THM-M-1201`. Only then can a statement worker encode
and elaborate the exact target and minimize its pinned imports.

## Narrow validation evidence

Commands ran in this worker clone on 2026-07-12. Lean inspection reused the existing canonical
pinned `.lake` artifacts. No `lake update`, build, fetch, clone, or dependency mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1199` | 0 | rank 393, planned, `hard_mathlib_anchor_and_wrapper`, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | SHA-256 `651c8acc...b1d2` and `321626c8...2d81` |
| `rg -n -i 'shock wave\|shockwave\|rankine.?hugoniot\|entropy solution\|scalar conservation law' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | no textual matches in pinned mathlib source |
| `rg -n -i '激波理论\|守恒律方程的激波\|shock wave theory\|shock waves? of conservation' Docs Formalizations/Lean/AwesomeTheorems Stage1_Instances --glob '!Stage1_Instances/THM-M-1199/**'` | 0 | only the terse source record and generated target/blueprint metadata; no exact statement or formal artifact |

The assigned statement phase is blocked rather than genuinely self-tested, so no
`.stage1-worker-selftest.json` is emitted.
