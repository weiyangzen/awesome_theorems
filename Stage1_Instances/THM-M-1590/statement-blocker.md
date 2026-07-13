# Exact-statement gate: blocked

Item: `S56-M-1590-STATEMENT`

Theorem: `THM-M-1590`

Base revision: `c2e294becadae6ce784f27ee69f2e8dbf57e0b30` (tree
`3f567e7f76b189432b73444354070c0ff75925b9`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1590-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. Rev-5.6 permits this dependency-ordered provisional
attempt, so pending acceptance did not prevent the assessment. The intake receipt is unsigned,
non-content-addressed, declares `accepted: false`, has no accepted receipt ID, and intentionally
leaves the canonical mathematical statement and Lean target null. Master acceptance remains
required before any future accepted statement transition.

Independently, the exact-statement gate cannot pass from the authoritative repository record. It
supplies only the title `循环码` (`cyclic codes`), a collective attribution, the period "20th
century," and the gloss `循环移位不变的码` ("codes invariant under cyclic shift"). This describes a
class of codes. It does not state a truth-valued proposition with ordered binders, hypotheses, and
a conclusion. Stage0 repeats the gloss while explicitly leaving precise definitions and premises
open. The catalog's `已验证` label is untrusted under rev-5.6.

Even a definition cannot be inferred exactly. The record fixes no alphabet, ring, or field; block
length or coordinate type; word and code representation; left or right shift; action by
precomposition or its inverse; arbitrary, additive, or linear code structure; or closure versus
equality as the invariance predicate. It also does not select a result about cyclic codes.
Definition-characterization, polynomial-ideal, generator-polynomial, duality, dimension, distance,
decoding, BCH, and Reed-Solomon results are materially different propositions. Selecting any of
them, or presenting shift invariance as both a premise and the desired result, would invent,
narrow, broaden, or substitute mathematics rather than elaborate the received target.

The unresolved choices include the empty and singleton alphabet, zero ring, lengths zero and one,
empty and singleton codes, zero and full linear codes, closure under one shift versus all powers,
zero and unit generator polynomials, and minimum-distance conventions. No source-approved decision
exists for any of these boundary cases.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing expression
fingerprint hard blockers. There is therefore no honest canonical expression for which imports can
be proved minimal, alternate transports can be checked, or removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations can be certified. Those mutation checks are
undefined, not passed. The root vector remains `[H5, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates in the pinned environment. Its four direct imports
expose coordinate permutations, function-space linear transport, Hamming interfaces, and
circulant-matrix interfaces. All eight API checks pass. This is real substrate validation, but the
probe declares no cyclic-code object, invariance predicate, selected proposition, canonical target,
checked transport, or proof body. Its imports cannot be certified minimal for an absent target and
receive no statement or proof credit.

A bounded lexical search of pinned mathlib and repository-local Lean found no exact cyclic-code
declaration under the recorded terms. This is discovery-only feasibility evidence, not the
downstream immutable anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No update, build, clone, fetch, or dependency
mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1590` | 0 | rank 1211; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| `git blame -L 11714,11719 -- Docs/researches/math_theorems.md` plus read-only source/dossier inspection | 0 | all six sparse catalog lines originate at commit `bcf3f9fa...`; confirmed a code-class gloss, null intake target, open proposition-changing choices, and no approved source-selected root |
| `sha256sum Docs/Stage1_Blueprint_rev-5.6.md Docs/Stage1_Targets_rev-5.6.json Docs/Stage1_Execution_DAG_rev-5.6.json skills/execute-stage1-rev56/SKILL.md Docs/Blueprint_Guidelines.md Docs/researches/math_theorems.md Docs/researches/cs_theorems.md Docs/Stage0_Blueprint.md Stage1_Instances/THM-M-1590/{README.md,instance.json,source-statement-crosswalk.md,scope-map.md,task-dag.json,intake-receipt.json,IntakeProbe.lean,check_intake.py,validation.md} Formalizations/Lean/{lean-toolchain,lake-manifest.json} Formalizations/Lean/.lake/packages/mathlib/Mathlib/{Logic/Equiv/Fin/Rotate.lean,LinearAlgebra/Pi.lean,InformationTheory/Hamming.lean,LinearAlgebra/Matrix/Circulant.lean}` | 0 | exact current hashes are recorded in `statement-blocker.json`; historical intake hashes were not rewritten |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1590/IntakeProbe.lean` | 0 | eight adjacent APIs elaborated; stdout SHA-256 `63569025...e8eedd`; no canonical target or proof body |
| bounded cyclic-code search in pinned mathlib and repo-local Lean | 1 | expected no-match result; discovery-only evidence |
| `python3 -B Stage1_Instances/THM-M-1590/check_intake.py` | 1 | historical intake replay stops at its stale pre-integration blueprint hash; its original nine-file inventory is also historical after this phase |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-1590/statement-blocker.json` plus the exact scoped `jq -e` assertion recorded in `commands_and_results` | 0 | JSON syntax, identity, null target/imports, unchanged vector, four undefined mutations, false completion flags, and two-file scope agree |
| `git diff --check -- Stage1_Instances/THM-M-1590 .stage1-worker-selftest.json`; exact byte-hygiene Python assertion and per-file `git diff --no-index --check /dev/null <file>` commands recorded in `commands_and_results` | 0 aggregate | no whitespace, final-newline, CR, NUL, or trailing-space diagnostics; each no-index exit 1 was only the expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the assigned exact-statement deliverable did not pass |

The intake checker is frozen to its original authority bytes and nine-file intake inventory.
Integration subsequently changed the generated blueprint and execution DAG. Adding these statement
artifacts also makes that inventory historical. This statement run records the limitation instead
of rewriting the intake checker, receipt, instance, task DAG, generated blueprint, or authoritative
execution DAG to manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must master-accept the intake before accepting any later statement
transition. Accountable reviewers must also preserve and hash an immutable primary or approved
authoritative source, select and independently approve one exact truth-valued cyclic-code
proposition, and transcribe every incorporated definition, convention, ordered binder, hypothesis,
conclusion, proof boundary, correction, erratum, and degenerate case while preserving neighboring
target boundaries.

A fresh statement run can then encode precisely that source-selected claim, minimize pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
