# Exact-statement gate: blocked

Item: `S56-M-0754-STATEMENT`

Theorem: `THM-M-0754`

Base revision: `67d32ab26aba14b674ae8a1b919e6935812190c3` (tree
`8a1d264cf3331992fbbc3a4fffca285af0b88929`).

## Decision

The statement item remains `[ ]`. The authoritative repository source gives only the title
`算术层次` ("arithmetical hierarchy") and the complete gloss `算术集合的层次` ("the hierarchy of
arithmetical sets"). It supplies no bibliography, definition, ordered binders, hypotheses,
truth-valued conclusion, proof boundary, correction history, or theorem variant. The prerequisite
intake therefore correctly leaves the canonical human claim and Lean target null. It has only
provisional worker state `[_]`, not master-accepted state `[x]`.

An arithmetical hierarchy can classify formulas, predicates, relations, or subsets of naturals.
Its levels depend on the arithmetic language and intended model, the base-level and indexing
convention, treatment of bounded quantifiers, parameters and tuple coding, and the chosen
syntactic, semantic, or computability presentation. A theorem about its definition, closure,
normal form, presentation equivalence, completeness, strictness, properness, or non-collapse is
not interchangeable with any other one. Selecting one from mathematical familiarity would invent
or substitute proposition-changing mathematics.

Consequently there is no exact expression whose imports can be certified minimal, no elaborated
expression or environment fingerprint, and no approved alternate encoding. Removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations are undefined rather than
passed. This is the section 5 exact-statement hard blocker. The root vector remains
`[H5, M4, R4]`; statement, audit, proof, and theorem completion are false.

## Pinned Lean boundary

The existing `IntakeProbe.lean` was re-elaborated with its two direct imports:

- `Mathlib.Computability.Halting`
- `Mathlib.ModelTheory.Complexity`

It checks ten generic first-order formula-complexity and computability interfaces, including
`BoundedFormula.IsUniversal`, `BoundedFormula.IsExistential`, `PrimrecPred`, `ComputablePred`, and
`REPred`. The probe exited successfully, with stdout SHA-256
`13987fcb9e10d9e39f2576f455276e17ed191062fedcdfdceb7458863324b058` and empty-stderr SHA-256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

Those interfaces neither define hierarchy levels nor classify sets in a source-selected standard
model. A bounded exact-topic search found no matching declaration in pinned mathlib or the
repo-local Lean project. This is adjacent API and feasibility evidence only, not a canonical
statement, minimal-import claim, anchor audit, or proof.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided canonical `.lake` symlink
was used read-only. No dependency update, build, clone, fetch, or other `.lake` mutation was run.

## Validation record

Commands ran from this worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0754` | 0 | rank 1340; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | before editing, only the automation-provided `.lake` symlink was untracked; the base revision and tree are recorded above |
| inspect the target manifest, execution node, repository source, Stage0 projection, intake dossier, and source provenance | 0 | the scheduled root is a topic-only label; the source supplies no unique proposition |
| `git blame -L 5556,5561 -- Docs/researches/math_theorems.md` | 0 | all six catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short`; `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | package worktree clean; pinned mathlib revision and tree recorded above |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0754/IntakeProbe.lean` | 0 | ten adjacent generic interfaces elaborated; output hashes recorded above; no target, transport, or proof body declared |
| `rg -n -i 'arithmetical hierarchy\|arithmetic hierarchy\|ArithmeticalHierarchy\|ArithmeticHierarchy' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems -g '*.lean'` | 1 (expected) | bounded local search found no exact-topic declaration; this is not a global absence claim |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0754-pycache python3 -m py_compile Stage1_Instances/THM-M-0754/check_intake.py` | 0 | historical intake validator compiled without writing an owned generated file |
| `python3 -B Stage1_Instances/THM-M-0754/check_intake.py` | 1 | historical intake checker failed closed because it expects the intake execution item at its original `[ ]`, while integration now records provisional `[_]`; it is not statement evidence and was not changed |
| scoped prohibited-declaration scan over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0754/statement-blocker.json` and scoped `jq -e` invariants | 0 | blocker JSON and its null-target, unchanged-vector, false-completion, undefined-mutation, and no-self-test boundaries agree |
| whitespace checks for `Stage1_Instances/THM-M-0754` | 0 | no whitespace diagnostics; new files were also checked individually with `git diff --no-index --check` |
| `test ! -e .stage1-worker-selftest.json` | 0 | no worker self-test packet because the assigned statement deliverable did not pass |

## Retry condition and status boundary

The integration lane must master-accept the intake before an accepted dependent transition.
Accountable reviewers must also lawfully preserve and hash an immutable primary or approved
authoritative source, select and independently approve one exact proposition, and transcribe every
incorporated definition, ordered binder, hypothesis, conclusion, proof boundary, correction,
erratum, and boundary convention. In particular, they must fix the classified objects, arithmetic
language and intended model, formula and coding scheme, parameter policy, level-zero and
alternation conventions, hierarchy presentation, and exact theorem strength.

A later statement run can then encode only that approved claim, minimize its pinned imports,
serialize the elaborated expression and environment, compile all credited transports, and execute
all four mutation classes. This blocker is the assigned phase's truthful result, not completion of
the node or any downstream task. No statement receipt, worker `[_]`, accepted receipt, proof
credit, audit completion, or theorem completion is claimed, and no `.stage1-worker-selftest.json`
is emitted.
