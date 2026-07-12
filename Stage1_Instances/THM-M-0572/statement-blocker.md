# Exact-statement gate: blocked

Item: `S56-M-0572-STATEMENT`  
Base revision: `9898022a0eed3cf9fb3c55a6affb6176224f33cf`

## Decision

The exact Lean 4 target cannot be truthfully frozen from the accepted intake. The repository record
names only the families index theorem and paraphrases it as an index theorem for a fiber bundle.
The intake intentionally leaves open the real or complex theory, category of the base and
fibration, boundary conditions, operator class, grading, symbol model, and topological pushforward.
Those choices change both the ordered hypotheses and the type in which the terminal equality lives.

The intake identifies Atiyah and Singer, *The Index of Elliptic Operators: IV*, Annals of
Mathematics 93 (1971), 119-138, DOI `10.2307/1970756`, only as a primary-source candidate. It also
explicitly requires the statement phase to inspect a stable scan and identify the exact theorem,
page, incorporated definitions, conventions, and errata. No such source artifact or reviewed
transcription is present in the clone. Therefore selecting a familiar modern formulation would
invent the missing mathematics rather than elaborate the exact repository target.

There is also no existing repo-local Lean declaration that can supply the missing canonical
meaning. A scoped source search finds no families-index, analytic-index, or topological-index
declaration. The pinned mathlib tree contains general fiber/vector-bundle modules, but its own
`Mathlib/Analysis/Normed/Operator/Banach.lean` still records a TODO to generalize results once
mathlib has Fredholm operators. This is an API observation, not an anchor audit, and it cannot turn
an abstract equality between user-supplied index values into the families index theorem.

Section 5.1 of `Docs/Stage1_Blueprint_rev-5.6.md` requires the exact target before expression
serialization, import minimization, checked alternate encodings, and semantic mutations. With no
unique proposition to elaborate, a `lake env lean` file would necessarily test a broadened,
substituted, or vacuous statement. No such file was created, no statement receipt or expression
hash is claimed, and no `.stage1-worker-selftest.json` is emitted.

## First failed gate and retry condition

First failed gate: canonical source statement identification, before Lean statement elaboration.

To retry, an accountable source reviewer must provide or pin an inspectable edition of the primary
source and freeze the exact theorem/page, all incorporated definitions and assumptions, the
real/complex K-theory convention, operator and fibration categories, boundary behavior, symbol and
pushforward models, and any errata decision. A later statement worker can then encode that exact
claim, determine minimal imports, fingerprint the elaborated expression, and run the four required
mutation classes.

## Narrow validation evidence

Commands were run from the worker clone on 2026-07-12. No dependency update, fetch, build, or
mutation of `.lake` was performed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | exit 0; `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0572` | exit 0; rank 618, `L0`, `rework_required: true`, `lifecycle_mode: planned`, `theorem_complete: false` |
| `rg -n -i 'families index|family index|families.*index|family.*elliptic|Atiyah.*Singer.*IV|families 指标' --glob '!Docs/Stage1_Blueprint_rev-5.6.md' --glob '!Docs/Stage1_Execution_DAG_rev-5.6.json' --glob '!Docs/Stage1_Targets_rev-5.6.json' --glob '!Docs/Stage1_Blueprint_Applicable_Theorems.md' --glob '!Stage1_Instances/THM-M-0572/**' .` | exit 0 only because it finds the prose metadata/research row; it finds no candidate Lean declaration |
| `rg -n -i 'topological.?index|analytic.?index|family index|index theorem|elliptic operator|fredholm operator|K.?theory' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | exit 0; no families-index API is found; the relevant hit is the Fredholm-operator TODO described above |

Status boundary: this is an actionable statement-phase blocker only. The provisional root remains
`[H2, M4, R4]`; audit completion and theorem completion remain false.
