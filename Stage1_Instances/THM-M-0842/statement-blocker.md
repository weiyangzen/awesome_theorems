# THM-M-0842 exact-statement gate: blocked

- Item: `S56-M-0842-STATEMENT`
- Base revision: `fb0baac89ea0633612be3b47448464b4b8e4bef7`
- Base tree: `018557070da18ea1733a82de81a238750c59aa84`
- Attempt date: 2026-07-13 (Asia/Shanghai)
- Verdict: blocked; no statement receipt, worker `[_]`, or theorem-completion claim

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
The complete received mathematical wording is the label `Simonovits稳定性` (Simonovits stability),
the attribution to Miklos Simonovits in 1968, and the gloss `极值图的稳定性` (stability of extremal
graphs). The catalog supplies no formula, theorem number, definitions, ordered binders,
hypotheses, conclusion, proof boundary, correction, erratum, reviewer, or formal declaration. Its
`已验证` label is untrusted under rev-5.6.

The intake identifies one primary paper but deliberately does not select a proposition. The source
contains materially different candidates:

- a general stability framework for graph properties;
- Theorem 7, with finite-family and extremal-graph assumptions inherited from Theorem 6;
- Theorem 8(a), excluding a balanced complete multipartite blow-up and deleting edges to obtain a
  `d`-chromatic graph;
- the common modern arbitrary-forbidden-graph, two-sided edit-distance formulation; and
- a clique-only deletion-to-`d`-partite formulation, with later quantitative strengthenings.

These candidates differ in the forbidden object or family, chromatic offset, edge threshold,
quantifier dependencies, integer rounding, strictness, and deletion-only versus two-sided editing
and relabeling. Selecting a familiar or convenient variant would invent, narrow, broaden, or
substitute proposition-changing mathematics rather than elaborate the received target.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing elaborated
expression fingerprint hard blockers. The intake correctly leaves `canonical_statement`, the Lean
module and expression, target imports, expression hash, and canonical-target environment
fingerprint null at `[H1, M4, R4]`. Therefore minimal target imports, credited alternate
transports, and the removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case
mutations are undefined, not passed. No `Statement.lean`, assumed stability predicate, axiom,
placeholder, weakened special case, or broadened theorem was introduced.

The prerequisite `S56-M-0842-INTAKE` is only provisional worker state `[_]`. Its receipt declares
`accepted: false`, is not content-addressed, supplies no accepted receipt ID, and has no master
acceptance. That independently prevents an accepted statement transition.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` uses the three direct imports
`Mathlib.Combinatorics.SimpleGraph.Extremal.Turan`,
`Mathlib.Combinatorics.SimpleGraph.DeleteEdges`, and
`Mathlib.Combinatorics.SimpleGraph.Coloring`. A fresh team worker ran the narrow pinned command and
it exited 0. The exact stdout SHA-256 was
`23224afd70049a352ae3f71cc5c6696b3a82a874a601a79f6d259e4cda4fbb2e`; no stderr was observed.
Two duplicate local attempts issued concurrently against the shared canonical artifact store were
stopped after remaining blocked in uninterruptible I/O, and no result is claimed from those
duplicates.

The probe names adjacent interfaces such as `SimpleGraph.CliqueFree`, `Colorable`, `turanGraph`,
`IsTuranMaximal`, `extremalNumber_top`, `deleteEdges`, and `edgeFinset_deleteEdges`. It declares no
Simonovits proposition, checked source transport, or proof body. Its imports cannot be certified as
minimal imports for an absent canonical target and receive no statement or proof credit.

A bounded topic search over repository-local and pinned-mathlib Lean sources found only unrelated
uses of “stability” and generic symmetric-difference APIs, not a target-level Simonovits structural
stability declaration. This is discovery-only evidence, not the downstream anchor audit or a
global absence claim.

The pinned environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` link points to canonical pinned artifacts and was not modified. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was run.

## Validation Evidence

Commands ran in this isolated worker clone on 2026-07-13 (Asia/Shanghai). Exact arguments, exits,
result summaries, and current input hashes are also preserved in `statement-blocker.json`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0842` | 0 | rank 1399, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base revision and tree appear above |
| reads of the standard, skill, target manifest entry, catalog, Stage0 projection, DAG, and complete intake dossier | 0 | confirmed provisional dependency, null target, distinct source variants, and unresolved proposition-defining inputs |
| current `sha256sum` over authority, source, intake, toolchain, lockfile, and relevant pinned mathlib files | 0 | current hashes are recorded in the structured blocker |
| `lake --version`; mathlib revision/tree/status checks | 0 | expected pinned Lake and clean mathlib worktree passed |
| `lake env lean ../../Stage1_Instances/THM-M-0842/IntakeProbe.lean` | 0 | fresh team-worker replay elaborated all nine named adjacent APIs; stdout SHA-256 `23224afd...fbb2e`; no target or proof body was declared |
| bounded topic search in pinned mathlib and repository-local Lean | 0 with unrelated matches | no exact target-level Simonovits structural stability declaration was credited |
| `python3 -B Stage1_Instances/THM-M-0842/check_intake.py` | 1 | historical intake checker expects its original authoritative intake item; integration has changed that item from `[ ]` to `[_]`, so this phase records rather than rewrites the historical evidence |
| `python3 -m json.tool Stage1_Instances/THM-M-0842/statement-blocker.json` and scoped `jq -e` invariants | 0 | valid JSON; identity, null target/imports, four undefined mutations, unchanged vector, false completion fields, two-file scope, and blocked state agree |
| wrapped prohibited-construct scan over owned Lean | 0 | inner search returned the expected no-match exit 1; no `sorry`, `admit`, `sorryAx`, axiom, constant, opaque, or unsafe declaration |
| scoped tracked/untracked whitespace checks | 0 | no whitespace diagnostics in either blocker artifact |
| `test ! -e .stage1-worker-selftest.json` | 0 | no self-test packet because the exact-statement gate failed |

A blocked run does not turn these artifact checks into a statement-node self-test.

## Retry Condition And Status Boundary

The integration lane must master-accept fresh intake evidence bound to current authority.
Accountable reviewers must preserve and hash one immutable primary or approved authoritative
source, select and independently approve one exact proposition, and transcribe every incorporated
definition, ordered binder, hypothesis, conclusion, dependency, correction, erratum, and boundary
case. They must fix the forbidden object or family, chromatic parameter, vertex domain, exact edge
threshold, strictness and casts, quantifier order, rounding, edit or deletion relation,
relabeling, and normalization.

A fresh statement attempt can then encode precisely that approved claim, prove its pinned direct
imports minimal, serialize and hash the elaborated expression and environment, compile every
credited transport, and run all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; the root stays `[H1, M4, R4]`;
`audit_complete: false` and `theorem_complete: false`; no debt change is proposed. Because the
exact-statement deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt,
worker `[_]`, or master acceptance is claimed.
