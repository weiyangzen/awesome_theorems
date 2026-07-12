# Anchor audit

Item: `S56-M-0981-ANCHOR_AUDIT`  
Repository base: `72dcbc91b366222bafc8e54d69b5bdd3e463b6cf`  
Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`

## Result

The exact target has a minimal viable route through three declarations already present in the
pinned mathlib checkout:

| Clause | Immutable candidate | Exact relationship |
|---|---|---|
| Empty event | `MeasureTheory.measure_empty` | Supplies `P empty = 0` |
| Unit mass | `MeasureTheory.IsProbabilityMeasure.measure_univ` | Supplies `P univ = 1` once the explicit premise is installed locally as an instance |
| Countable additivity | `MeasureTheory.measure_iUnion` | Its two explicit premises and conclusion match the target's disjoint measurable `Nat` family |

`AnchorAudit.lean` composes these declarations against an audit-local direct expansion of the
canonical target. Lean reports only `propext`, `Classical.choice`, and `Quot.sound` for that checked
composition, with no `sorryAx`.

The historical repository candidate
`AwesomeTheorems.Stage1.S1_M_261.statementShape_mathlib_wrapper` is statement-equivalent and its
module still elaborates at the repository base. Its source file is blob
`1f69525f06b4314a8405952d193ad674621e0ea4`, last changed at commit
`16d227cffb7cb7d9e8392b6c0ff8211e498e1330`. It imports many unrelated probability and process
modules, so the preferred route is the three declarations reachable from the statement's single
minimal import. The historical wrapper remains discovery evidence rather than proof credit.

## External-candidate boundary

Searches across all tracked Lean sources and the complete pinned mathlib source tree found no other
named exact Lean 4 formalization. Only the legacy `S1_M_261` family contains `KolmogorovAxioms`;
mathlib exposes the constituent definitions and lemmas. No separately pinned external project is
present in the clone. In accordance with the worker policy, no moving remote was cloned, fetched,
or credited. This is a complete audit of locally available immutable candidates, not a claim that
every public Lean repository has been exhaustively searched.

Exact modules, source lines/blobs, types, classifications, search queries, and dependency
feasibility are recorded in `anchor-audit.json`.

## Validation

All commands ran on 2026-07-12. Lean commands used the existing `.lake` artifacts; no dependency
operation ran.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0981/AnchorAudit.lean` from `Formalizations/Lean` | 0 | printed all three candidate types; composition elaborated; axiom report excluded `sorryAx` |
| `lake env lean AwesomeTheorems/Stage1/S1_M_261.lean` from `Formalizations/Lean` | 0 | historical candidate module elaborated at the immutable repository base |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`; 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0981` | 0 | confirmed rank 261 and `hard_mathlib_anchor_and_wrapper` lane |

The phase is self-tested pending master acceptance. The canonical root remains unproved in this
phase; obligation-tree, proof, validation, and release work remains open.
