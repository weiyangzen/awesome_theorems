# Statement gate blocker

Item: `S56-M-0121-STATEMENT`  
Theorem: `THM-M-0121`  
Verdict: blocked; no exact canonical Lean target is claimed.

## First failed gate

The accepted source identity is insufficient to select one mathematical proposition. The repository
supplies only the label "Mori rationality theorem," the gloss "rationality of Fano varieties," an
attribution to Shigefumi Mori, and the year 1988. It supplies no primary-source theorem/page, exact
wording, definition chain, assumptions, conclusion convention, correction history, or independent
review.

The intake correctly distinguishes materially different candidates: the minimal-model-program
rationality theorem for a nef threshold; existence of rational curves or uniruledness for Fano
varieties; and rational connectedness of smooth projective Fano varieties. These are not alternate
notations for one proposition. They require different fields, geometric objects, divisor and
singularity data, binders, hypotheses, and conclusions. The unqualified reading that every Fano
variety is birationally rational is false, so it cannot be adopted as a literal normalization.

Consequently rev-5.6 sections 5 and 5.1 block the statement before elaboration. There is no honest
canonical declaration, minimal import set, normalized expression hash, checked alternate transport,
or removed-hypothesis/domain/binder/boundary mutation suite. Choosing a candidate here would invent,
broaden, weaken, or substitute mathematics. The prerequisite intake also remains worker-provisional
`[_]`, not master-accepted `[x]`, so no accepted statement transition is dependency-legal.

## Lean boundary checked

`StatementProbe.lean` uses the sole direct import
`Mathlib.AlgebraicGeometry.RationalMap` and elaborates the closest pinned substrate:
`Scheme.RationalMap`, `Scheme.RationalMap.domain`, and
`Scheme.RationalMap.equivFunctionField`. This proves only that scheme rational maps are available
after a source claim is selected. It is not the canonical target and receives no statement or proof
credit.

The historical module `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_040.lean` also elaborates,
but its `MoriRationalityStatementShape` takes both its hypothesis and conclusion as arbitrary
predicate parameters. The module explicitly leaves the reading and required APIs unresolved; using
it would substitute a generic interface for the requested theorem.

The environment is Lean `4.29.0` (commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`) with mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The existing canonical `.lake` artifact was used
read-only. No update, build, clone, fetch, or dependency mutation was performed.

## Validation evidence

Base revision: `f6e50868cea6cdee270b34c9bb111940d2f16305` (tree
`6af4a41a0e2a894d1dfc7f55703e4822b584dd6b`). Commands ran from the worker clone on 2026-07-15.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard consistency passed: 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | Manifest passed: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0121` | 0 | Rank 40, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0121/StatementProbe.lean` | 0 | Three adjacent rational-map interfaces elaborated; no canonical target or proof body was declared |
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_040.lean` | 0 | Legacy generic interface elaborated; this is negative boundary evidence, not exact-target evidence |
| word-bounded exact-topic search over pinned `Mathlib/AlgebraicGeometry` | 1 | Expected no-match exit; no Fano, uniruledness, rational-connectedness, nef-threshold, or Mori-rationality declaration was found |
| import-deletion probe for `Scheme.RationalMap` | 1 | Expected failure; without `Mathlib.AlgebraicGeometry.RationalMap` the identifier is unknown, so the sole import is necessary for the boundary probe only |
| `python3 -m json.tool Stage1_Instances/THM-M-0121/statement-blocker.json >/dev/null` | 0 | Structured blocker is valid JSON |
| prohibited-token search over the owned Lean probe | 1 | Expected no-match exit; no proof escape or bodyless declaration token was found |
| `git diff --check -- Stage1_Instances/THM-M-0121` | 0 | No whitespace errors |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short --untracked-files=all` | 0 | Empty output; the pinned mathlib package remained clean |

## Retry condition

An accountable reviewer must admit an immutable primary or authoritative edition and exact
theorem/page, select the source reading, transcribe every definition, binder, hypothesis, and
conclusion, resolve corrections and errata, and approve an assumption crosswalk. A later statement
run can then encode that exact claim using pinned concrete APIs, determine its minimal imports,
serialize its expression and environment fingerprints, and run all required mutations and checked
transports.

Until then, lifecycle remains `planned`, root debt remains `[H3, M4, R4]`, and statement acceptance,
audit completion, proof, and theorem completion are false. No `.stage1-worker-selftest.json` is
emitted because the assigned statement deliverable did not pass its completion gate.
