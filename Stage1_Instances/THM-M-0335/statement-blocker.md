# Statement-phase blocker

Item: `S56-M-0335-STATEMENT`  
Theorem: `THM-M-0335`  
Worker base revision: `106084d7f6343f3046dfb9e108503edbcdc86191`

## Gate decision

The exact Lean 4 target cannot yet be elaborated truthfully. The repository record supplies only
the gloss `子因子的指标值` ("index values of subfactors"). The intake identifies Jones's 1983
paper and the conventional value-set formula, but it has not independently pinpointed the exact
source theorem, definitions, assumptions, endpoint convention, or whether the selected claim is
only the restriction on possible values or also realizes every listed value. Choosing those
details here would silently select a broader or substituted theorem.

There is also no source-faithful formal domain in the pinned library on which to state the claim.
The narrow source search found the basic `WStarAlgebra` and concrete `VonNeumannAlgebra` APIs, but
no type `II_1` factor predicate, admissible subfactor inclusion, or Jones-index definition. Defining
an ad hoc structure with an `index` field, or assuming the desired classification as a structure
field, would not encode Jones index and is explicitly excluded by the intake scope map.

Consequently there is no canonical Lean expression to serialize or fingerprint. Removed-hypothesis,
changed-domain, changed-binder-scope, and boundary mutation tests would test an invented encoding,
not the exact theorem. The rev-5.6 section 5.1 statement gate therefore fails before any proof or
anchor evidence may receive credit. `IntakeProbe.lean` was re-elaborated solely to confirm that the
pinned Lean environment and the nearby von Neumann algebra APIs are available; it is not a target.

## Exact validation record

Validation date: `2026-07-12` (`Asia/Shanghai`). The existing canonical `.lake` artifacts were used
read-only. No update, build, clone, or fetch command was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets; ranks 1..1546; all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0335` | 0 | rank 828; planned; legacy artifacts unaccepted; theorem_complete false |
| `rg -n -i 'jones[ _-]?(index\|basic construction)\|subfactor\|type[ _-]?ii.?1\|finite factor' Formalizations/Lean/.lake/packages/mathlib/Mathlib -g '*.lean'` | 0 | only an unrelated monoidal-category comment mentioning subfactor literature; no target-domain API found |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0335/IntakeProbe.lean)` | 0 | five nearby von Neumann algebra declarations elaborated; no canonical Jones-index target asserted |
| `python3 -m json.tool Stage1_Instances/THM-M-0335/instance.json` | 0 | intake JSON is syntactically valid |
| `python3 -m json.tool Stage1_Instances/THM-M-0335/task-dag.json` | 0 | task DAG JSON is syntactically valid |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0335 -g '*.lean'` | 1 | expected no-match exit; no prohibited placeholder or axiom found |

## Required unblocker and status boundary

The first source unblocker is an immutable, independently inspected passage that freezes the exact
theorem and all definitions, hypotheses, endpoints, degenerate cases, and the
restriction-versus-realization boundary. The formal unblocker is a source-faithful Lean interface
for type `II_1` factors, admissible inclusions, and Jones index (or a fully checked construction of
that interface). Only then can minimal imports be selected and the required expression fingerprint
and four mutation classes be produced.

This statement node remains `[ ]`, blocked at `M4`. The root remains `[H1, M4, R4]`, with
`audit_complete: false` and `theorem_complete: false`. No worker self-test manifest is emitted,
because the assigned statement deliverable did not pass its gate.
