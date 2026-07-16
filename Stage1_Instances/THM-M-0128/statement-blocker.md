# Statement-phase blocker

Item: `S56-M-0128-STATEMENT`  
Theorem: `THM-M-0128`  
Base revision: `dae1951609072752d49d111bf00e78e4512f2d14`

Rechecked: `2026-07-17` (`Asia/Shanghai`)

## Verdict

The exact-statement gate is blocked, so this node is not self-tested as
complete. `.stage1-worker-selftest.json` hands off the self-tested negative
assessment only; its `[_]` is unfinished worker state, not phase acceptance.
The HEAD contract roles are now present as `statement.json`, `Statement.lean`,
`source-statement-crosswalk.md`, and `statement-receipt.json`;
`check_statement.py` emits the required typed negative semantic result. Those
artifacts cannot support `[x]` while the exact-target gate is blocked.
The validator did not exist at this worker base, so scheduler replay cannot
select it until integration lands these owned artifacts on a new immutable
base; this does not weaken the earlier mathematical blocker.

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
adeles. `Statement.lean` elaborates those anchors with only the two direct
imports and deliberately declares no target. A repository-local scan found no
declaration for a CM type, reflex field/reflex norm, idele class, or Shimura
special-point reciprocity target in the pinned Mathlib sources. Thus the
anchors do not determine an exact root expression.

The v2 theorem node has no direct hard parent, transitive hard ancestor, hard
edge, reuse hint, or shared group. `dependency-reuse-ledger.json` records this
exact empty closure at graph digest
`3d32f808e2914b338c459d52651b69731f0979a90a720f98bc0f31a577e2bafa`
and context digest
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.
No parent acceptance or proof credit is transferred.

## Commands and results

The current commands ran in this worker clone on 2026-07-17. No dependency update,
fetch, clone, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0128/Statement.lean` from `Formalizations/Lean` | 0 | the two substrate types elaborated; no canonical declaration was made |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0128/check_statement.py` | 0 | one typed JSON object reported `status=blocked`, `phase_accepted=false`, and failed gate `S02-EXACT-TARGET...` |
| schema-1.1 ledger validation against the exact graph and base | 0 | empty direct/transitive parent and reuse context accepted |
| JSON parsing, semantic-output parsing, prohibited-token scan, and `git diff --check` | 0 | structured negative artifacts are internally consistent and clean |
| `python3 Docs/tools/check_stage1_standard.py` | 1, expected worker-local drift | new target-owned evidence changes fresh theorem-DAG inventory; this worker cannot edit the generated DAG |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 1, same expected drift | deterministic generation sees `Statement.lean`, `statement.json`, and `statement-receipt.json`; master integration must regenerate the read-only projection after merge |

## First failed gate

`S02-EXACT-TARGET.exact_source_statement_identity_and_convention_selection`:
an exact source theorem and its convention
crosswalk are not frozen, and the pinned Lean environment lacks the semantic
APIs needed to recover those missing choices. The next valid action is a source
and convention audit that fixes those choices, followed by implementation (or
a pinned import) of the required CM/reflex/Shimura object model. Until then the
intake root vector remains `[H2, M4, R4]`; no statement elaboration, proof,
audit completion, or theorem completion is claimed.
