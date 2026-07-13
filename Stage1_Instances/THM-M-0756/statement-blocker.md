# Exact-statement gate: blocked

Item: `S56-M-0756-STATEMENT`

Theorem: `THM-M-0756`

Base revision: `adc87f8ea24dcc7c5e2668c0a5ede0ca5c5f0f55` (tree
`3c83596059f716cde0d50a5f6b390ada6ca7c8e1`).

## Decision

The statement item remains `[ ]`. The authoritative repository source gives only the title
`超算术理论` ("hyperarithmetic theory") and the complete gloss `超算术集合的理论` ("the theory
of hyperarithmetic sets"). It supplies no bibliography, definition, ordered binders, hypotheses,
truth-valued conclusion, proof boundary, correction history, or theorem variant. The prerequisite
intake therefore correctly leaves the canonical human claim and Lean target null. It has only
provisional worker state `[_]`, not master-accepted state `[x]`.

Hyperarithmetic theory can be presented using iterated jumps, effective transfinite recursion,
lightface definability, relative computability, or checked equivalences among such presentations.
Those choices require a recursive-ordinal notation system or well-order convention, coding and
parameter policies, successor and limit rules, and an exact domain such as subsets of naturals,
predicates, relations, coded functions, or reals. A definition package, characterization, closure
theorem, presentation equivalence, boundedness result, separation theorem, strictness theorem, or
properness theorem is not interchangeable with any other one. Selecting a familiar result from
mathematical memory would invent or substitute proposition-changing mathematics.

Consequently there is no exact expression whose imports can be certified minimal, no elaborated
expression or environment fingerprint, and no source-approved alternate encoding. The required
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations are undefined,
not passed. Rev-5.6 sections 5 and 5.1 make statement ambiguity and missing fingerprints hard
blockers before proof evidence may be inspected. No `Statement.lean`, theorem declaration, statement
receipt, or proof body was created.

The root vector remains `[H5, M4, R4]`. Here `H5` records that the supplied target is not a stable
proposition; it does not deny standard theorems about hyperarithmetic sets. Neither the statement
node nor any downstream node is complete.

## Source Boundary

`Docs/researches/math_theorems.md:5570-5575` is the complete target-bearing catalog record. All six
lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains a
title, Stephen Kleene attribution, year 1955, topic gloss, importance, and an explicitly untrusted
`已验证` label, but no source locator or proposition. `Docs/Stage0_Blueprint.md:20650-20675` repeats
the gloss while leaving definitions, premises, proof route, dependencies, alternate forms, axioms,
machine status, and artifacts open.

The intake's possible lightface descriptive-set-theoretic characterization is only a candidate
family. Choosing it, closure under effective transfinite recursion, or another established result
would silently decide the target's mathematical strength and conventions. The adjacent targets for
the arithmetical hierarchy, analytical hierarchy, Turing degrees, admissible ordinals, and
alpha-recursion theory cannot supply those decisions.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with its three direct imports:

```lean
import Mathlib.Computability.Halting
import Mathlib.Computability.TuringDegree
import Mathlib.SetTheory.Ordinal.Basic
```

It checked twelve adjacent partial-recursive, predicate, oracle-computability, Turing-reduction,
well-founded-recursion, and ordinal interfaces. This confirms that the pinned infrastructure is
available. It does not define hyperarithmetic sets, select a recursive-ordinal notation system,
state a canonical target, compile a transport, or prove the scheduled theorem. These imports are
therefore probe imports, not certified minimal imports for an absent target.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read only. No update, build, clone, fetch, or dependency
mutation was run.

## Validation Record

Validation ran on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0756` | 0 | rank 1342; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| scoped inspection of the blueprint, skill, guidelines, target manifest/entry, execution DAG, catalog and Stage0 records, and complete intake dossier | 0 | the catalog does not select one source-complete proposition; intake deliberately leaves the canonical statement, binders, imports, expression hash, and canonical environment fingerprint open |
| `git blame -L 5570,5575 -- Docs/researches/math_theorems.md` | 0 | all six catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0, x86_64 Linux, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release; Lake `5.0.0-src+98dc76e` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and `status --short` | 0 | pinned revision/tree above; no status output; dependency worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0756/IntakeProbe.lean` | 0 | twelve adjacent interfaces elaborated; no target, transport, or proof body declared; stdout SHA-256 `1cf99ee982f4d99308c45d5778010f75148c605d806fcd342b59e98732df4a00`; stderr was empty |
| bounded `rg` search for hyperarithmetic declarations in pinned mathlib and shared Lean source | 1 | expected no-match exit; no exact-topic declaration found; bounded discovery only, not an anchor audit |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0756-statement-pycache python3 -m py_compile Stage1_Instances/THM-M-0756/check_intake.py` | 0 | historical intake validator compiled without creating an owned generated file |
| `python3 -B Stage1_Instances/THM-M-0756/check_intake.py` | 1 | historical intake replay stops because it expects intake state `[ ]`, while integration now records provisional `[_]`; it was not edited or represented as statement evidence |
| `python3 -m json.tool Stage1_Instances/THM-M-0756/statement-blocker.json` and scoped invariant check | 0 | identity, dependency state, null target/imports, unchanged vector, four undefined mutations, false completion flags, and absent self-test packet agree |
| prohibited-construct scan over owned Lean files | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-0756` plus per-new-file `git diff --no-index --check` diagnostics inspection | 0 | no whitespace diagnostics; `git diff --no-index` ordinary new-file difference exits were handled separately |
| `test ! -e .stage1-worker-selftest.json` | 0 | no self-test packet because the exact-statement deliverable did not pass |

The historical intake checker is bound to the intake-time authoritative DAG state and exact
intake-only inventory. It is preserved as historical evidence rather than rewritten to make this
failed statement attempt pass.

## Retry Condition And Status Boundary

The integration lane must first master-accept the intake. Accountable reviewers must preserve and
hash a lawful immutable primary or approved authoritative source, select and independently approve
one exact proposition, and transcribe every incorporated definition, ordered binder, hypothesis,
conclusion, proof boundary, correction, erratum, and boundary case. They must also fix the object
domain, hierarchy or characterization presentation, recursive-ordinal notation or well-order
convention, coding and parameter policy, successor and limit rules, and theorem strength.

A fresh statement worker can then encode precisely that source model, minimize pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport, and
execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. `audit_complete: false` and `theorem_complete: false`; no debt-vector change is
proposed. Because the exact-statement deliverable did not pass, no `.stage1-worker-selftest.json`,
statement receipt, worker `[_]`, proof credit, or master acceptance is claimed.
