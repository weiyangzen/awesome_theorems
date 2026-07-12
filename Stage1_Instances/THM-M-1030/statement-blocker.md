# Exact-statement gate: blocked

Item: `S56-M-1030-STATEMENT`

## Decision

The exact Lean 4 target cannot yet be truthfully elaborated. The intake freezes a theorem family,
not one source-exact proposition. The primary Dubins-Schwarz paper is identified as Dubins and
Schwarz, "On Continuous Martingales," *PNAS* 53 (1965), 913-916,
DOI `10.1073/pnas.53.5.913`, but the repository contains no stable copy or transcription of its
theorem. A metadata check confirmed the paper identity and pages; attempts to retrieve the article
body through PNAS/PMC returned an access-denied page rather than the primary text. Thus none of the
following non-equivalent choices can be frozen from inspected source evidence:

- continuous local martingale versus continuous martingale and the exact filtration conditions;
- almost-surely unbounded quadratic variation versus the finite-terminal-value extension theorem;
- the definition and `>`/`>=` convention for the inverse bracket clock;
- pathwise equality outside one null set, indistinguishability, or per-time almost-sure equality;
- Brownian motion on the original space versus an extension and its time-changed filtration.

Selecting the unbounded-bracket textbook variant by preference would therefore substitute a
nearby theorem for the unidentified source target. Section 5 of the rev-5.6 standard forbids that.

## Lean boundary checked

`StatementProbe.lean` elaborates the closest independent substrate in the pinned environment:
filtrations, stopping times and stopped processes, martingales, adapted/predictable processes,
Gaussian processes and laws, and independent increments. Its four imports are needed to expose
those separate interfaces. This does not supply or identify a continuous-local-martingale,
quadratic-variation, inverse-clock, or canonical Brownian-motion definition.

The legacy `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_223.lean` is not an exact target. Its
`ContinuousLocalMartingaleData` accepts `inverseQuadraticVariation`,
`quadraticVariationUnbounded`, and `terminalValueConvention` as unconstrained `Prop` fields, and
`StatementShape` merely assumes their conjunction. It neither defines the bracket/inverse
relationship nor fixes the source equality and extension conventions. Crediting it would broaden
the caller-supplied hypotheses and is expressly excluded by the intake scope map.

## Validation record

Base revision: `2f58f2b8e57dc8637559b8e90ecc72cc391f498a`.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1030` | exit 0; rank 223, L0/rework_required, planned, theorem_complete false |
| `lake env lean ../../Stage1_Instances/THM-M-1030/StatementProbe.lean` (from `Formalizations/Lean`) | exit 0; all nine substrate checks elaborated |
| `lake env lean AwesomeTheorems/Stage1/S1_M_223.lean` (from `Formalizations/Lean`) | exit 0; legacy discovery artifact elaborated, without proving its `StatementShape` |
| `git diff --check -- Stage1_Instances/THM-M-1030` | exit 0; no output |

Environment: Lean `4.29.0`, mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, using the existing canonical `.lake` artifacts. No
dependency update, clone, fetch, or build was performed.

## Gate result and retry condition

First failed gate: section 5 exact statement identity. With no canonical expression, an elaborated
expression hash and meaningful removed-hypothesis/domain/binder-scope/boundary mutations cannot be
produced. Machine debt remains `M4`. Retry after an authoritative primary-source transcription or
explicit source decision freezes one formulation and all conventions above, and after concrete
Lean definitions encode the bracket and inverse relation rather than accepting them as opaque
propositions.

The assigned statement phase is not self-tested as complete, so no
`.stage1-worker-selftest.json` is emitted. No proof, audit completion, or theorem completion is
claimed.
