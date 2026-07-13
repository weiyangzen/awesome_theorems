# Exact-statement gate: blocked

Item: `S56-M-0624-STATEMENT`

Theorem: `THM-M-0624`

Base revision: `d05520867fab3367a9b61b9544c3e12241204f54` (tree
`fb2cfc62077d5b53e9938632cd6361dd60872067`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0624-INTAKE` has provisional state `[_]`
and an unaccepted worker receipt. More importantly, no independently approved exact proposition is
available from which to elaborate the canonical Lean 4 target.

The repository catalog gives the Nagata-Smirnov family name and only the gloss "necessary and
sufficient conditions for a topological space to be metrizable." It omits the conditions,
definitions, ordered binders, separation convention, equivalence packaging, proof boundary, and
boundary cases. Stage0 explicitly leaves these fields open, and the catalog's verified-status label
is untrusted under rev-5.6.

This attempt located and inspected primary sources that narrow, but do not remove, the ambiguity:

- Nagata 1950, Theorem I on p. 93, says that a regular space is metrizable exactly when it satisfies
  beta-countability. The definition immediately above uses an open basis consisting of countably
  many neighborhood-finite open coverings. The following remark says the covering property is not
  essential because the whole carrier can be adjoined to each non-covering family.
- Nagata 1957, Theorem 2 on p. 129, explicitly attributes the result to Smirnov and Nagata and says
  that a regular space is metrizable exactly when it has an open basis that is a countable union of
  locally finite collections of open sets.

These are not yet one source-frozen Lean proposition. Neither theorem locator defines historical
"regular" in a way already crosswalked to mathlib's deliberately non-Hausdorff `RegularSpace`.
Thus `RegularSpace` plus `T2Space`, `T3Space`, and a theorem quantified under a regularity instance
are candidate packagings with different elaborated types whose equivalence needs a checked
transport. The transport from the 1950 beta-countability definition to the 1957
sigma-locally-finite-basis definition, including removal of the per-layer covering condition, also
has not been checked and independently approved.

Choosing one without recording the source decision and checked equivalences would leave statement
identity unsupported and could change the received proposition. There is therefore no canonical
expression on which to certify minimal imports, serialize an expression and environment
fingerprint, compile alternate transports, or execute removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations. Those gates are undefined, not passed. No
statement, Lean declaration, import claim, or proof body was added. The root remains `[H1, M4,
R4]`; audit and theorem completion are false.

## Source Evidence

The inspected 1950 version of record is:

`https://ocu-omu.repo.nii.ac.jp/record/2007914/files/DB-M-001-02-04.pdf`

Its observed PDF SHA-256 is
`8b5a50269cb0c1b6d50711f91805040e89eacc155495e06c274f8794de47fd63`.
The inspected later restatement is:

`https://www.jstage.jst.go.jp/article/pjab1945/33/3/33_3_128/_pdf`

Its observed PDF SHA-256 is
`6e19e13ed5c7e84a6609bee3bdefc07459811c988b3a740765a3f79697c94885`.
These files were downloaded only to `/tmp` for inspection and were not vendored into the worker
clone. Primary inspection is source-discovery evidence, not an accepted H0 crosswalk or statement
receipt. No accountable second reviewer, accepted transcription, definition chain, translation,
correction or errata disposition, or source-to-Lean approval exists.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` imports `Mathlib.Topology.LocallyFinite`,
`Mathlib.Topology.Metrizable.Basic`, and `Mathlib.Topology.Separation.Regular`. It re-elaborates the
seven adjacent interfaces `PseudoMetrizableSpace`, `MetrizableSpace`, `RegularSpace`, `T2Space`,
`T3Space`, `IsTopologicalBasis`, and `LocallyFinite`. It declares no target or proof body.

`Mathlib.Topology.Metrizable.Basic` appears to expose all of that prospective vocabulary through
transitive imports. A plausible family layer is indexed by a subtype and tested by `LocallyFinite`;
the literal 1950 version would additionally require every layer to cover the carrier. These are
feasibility observations only. No import can be called minimal, and no candidate expression can be
credited, until reviewers freeze the exact source claim.

A bounded search found no packaged Nagata-Smirnov declaration or sigma-locally-finite-basis
predicate in repo-local Lean or pinned mathlib. That is discovery evidence rather than the later
anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided `.lake` link to canonical
pinned artifacts was used read-only. No update, build, clone, fetch, or dependency mutation ran.

## Validation Evidence

Commands ran in this isolated worker clone on 2026-07-13 (`Asia/Shanghai`). Lean commands ran from
`Formalizations/Lean`; all other commands ran from the repository root unless noted otherwise.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0624` | 0 | rank 1318, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| pre-edit `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the pre-existing automation `.lake` link was untracked; the base revision and tree are recorded above |
| catalog, Stage0, manifest, DAG, blueprint, skill, intake, and primary-source inspection | 0 | the catalog omits the conditions; the primary formulations and unresolved definition transports are recorded above; the canonical Lean target and fingerprints remain null |
| SHA-256 over authority, intake, toolchain, pinned-mathlib, and primary-source inputs | 0 | exact digests are recorded in `statement-blocker.json` |
| `lake env lean --version` and `lake --version` | 0 | Lean and Lake agree with the pinned environment above |
| pinned mathlib revision, tree, and worktree inspection | 0 | revision and tree agree with the fingerprint; the package worktree is clean |
| `lake env lean ../../Stage1_Instances/THM-M-0624/IntakeProbe.lean` | 0 | all seven adjacent APIs elaborated; no canonical target or proof body was declared; stdout SHA-256 `0c5f934a170759179259fed811f5f0d497d3fc29f4f17418d94eca76c50d61e1` |
| `python3 -B Stage1_Instances/THM-M-0624/check_intake.py` after adding this pair | 1 | the historical intake-only checker stops at its exact nine-file inventory; before these additions it passed for planned `H1/M4/R4` with six open tasks; this phase does not rewrite historical intake evidence |
| bounded exact-topic search in repo-local and pinned-mathlib Lean | 0 | the only match was the owned probe comment; no declaration or packaged predicate matched; discovery evidence only |
| `python3 -m json.tool Stage1_Instances/THM-M-0624/statement-blocker.json` and scoped blocker assertions | 0 | identity, open blocked state, null target/imports, four undefined mutations, unchanged vector, false completion flags, exact change scope, and absent self-test agree |
| prohibited-construct scan over owned Lean files | 1 | expected no-match: no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| scoped whitespace and final-newline checks | 0 | both added blocker artifacts passed |
| `test ! -e .stage1-worker-selftest.json` | 0 | no self-test manifest exists because the exact-statement deliverable is blocked |

The existing intake checker passed before this later phase's two artifacts were added. It owns a
closed intake-only inventory and now stops at that historical inventory assertion. This statement
phase does not rewrite the checker, intake receipt, task DAG, generated blueprint, or authoritative
execution DAG to manufacture continuing agreement after adding the blocker report.

## Retry Condition And Status Boundary

The integration lane must accept the intake dependency through a valid receipt. Accountable
reviewers must preserve and hash the primary sources, independently approve the exact theorem
transcription and every incorporated definition, settle the historical regular-space convention,
select the 1950 beta-countability or 1957 sigma-locally-finite-basis packaging, prove every credited
transport including removal of any per-layer covering requirement, and freeze the ordered binders,
assumptions, conclusion, proof boundary, corrections, errata, and boundary cases.

A later statement worker can then encode that same approved claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and run all four mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
