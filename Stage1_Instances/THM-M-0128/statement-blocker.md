# Statement-phase blocker

Item: `S56-M-0128-STATEMENT`  
Theorem: `THM-M-0128`  
Base revision: `b11e1f5a1a404420eee7320a845fdb9df48bec0c`

## Verdict

The exact-statement gate is blocked, so this node is not self-tested as
complete. No `.stage1-worker-selftest.json` is issued.

The accepted intake prose asks for the CM-special-point form of Shimura
reciprocity: an Artin action from the reflex field must agree with the action
induced by the reflex norm. The intake and source crosswalk explicitly leave
all of the following root-relevant choices unresolved:

- an exact primary-source theorem/page and its hypotheses;
- CM type and reflex-field/reflex-norm representations;
- the idele versus idele-class domain;
- arithmetic versus geometric Artin normalization;
- canonical-model, level, special-point, and left/right action data;
- equality versus orbit formulation.

These are mathematical binders and conventions, not implementation details.
Choosing them here would invent missing mathematics and could broaden, narrow,
or reverse the intended theorem. Encoding them as arbitrary types/functions or
as `Prop` fields would only reproduce the legacy placeholder boundary rejected
by `intake.json` and `scope-map.md`; assuming the compatibility equation as a
field would make the target circular.

The pinned mathlib checkout provides object-model anchors for CM fields and
adeles. `StatementProbe.lean` elaborates those anchors with only the two direct
imports. A repository-local scan found no declaration for a CM type, reflex
field/reflex norm, idele class, or Shimura special-point reciprocity target in
the pinned Mathlib sources. Thus the anchors do not determine an exact root
expression.

## Commands and results

All commands ran in this worker clone on 2026-07-12. No dependency update,
fetch, clone, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard is consistent: 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0128` | 0 | rank 46, planned, L0/rework-required, theorem incomplete |
| `lake env lean ../../Stage1_Instances/THM-M-0128/StatementProbe.lean` from `Formalizations/Lean` | 0 | `NumberField.IsCMField` and `NumberField.AdeleRing` elaborated |
| `lake env lean --version` from `Formalizations/Lean` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `rg -n 'structure CMType|def CMType|ReflexField|reflex.*[Nn]orm|IdeleClass|Shimura' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 1 | no matching pinned Mathlib declaration |
| `git diff --check -- Stage1_Instances/THM-M-0128` | 0 | no whitespace errors |

## First failed gate

`exact canonical statement`: an exact source theorem and its convention
crosswalk are not frozen, and the pinned Lean environment lacks the semantic
APIs needed to recover those missing choices. The next valid action is a source
and convention audit that fixes those choices, followed by implementation (or
a pinned import) of the required CM/reflex/Shimura object model. Until then the
intake root vector remains `[H2, M4, R4]`; no statement elaboration, proof,
audit completion, or theorem completion is claimed.
