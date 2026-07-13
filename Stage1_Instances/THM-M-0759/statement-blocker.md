# Exact-statement gate: blocked

Item: `S56-M-0759-STATEMENT`

Theorem: `THM-M-0759`

Base revision: `db4b8793e70ce8af74c9c9490acfa50aa3684d5e` (tree
`6434a20532ae7c523ad293e67a6228ab384bfb8a`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
That record supplies only the title `自动机理论` (automata theory), collective twentieth-century
attribution, and the gloss `有限自动机的理论` (the theory of finite automata). It contains no
truth-valued proposition, source locator, incorporated definitions, ordered binders, hypotheses,
conclusion, proof boundary, corrections, errata, or boundary conventions. Stage0 also leaves the
formal system, definitions and premises, proof route, dependencies, alternate forms, axioms,
machine status, and artifacts open. The catalog value `已验证` is untrusted metadata.

The prerequisite intake correctly classifies the received topic-only root as `[H5, M4, R4]` and
leaves both the canonical human claim and the Lean target null. Finite-automata theory includes
many inequivalent results: DFA/NFA and epsilon-NFA equivalences, Kleene equivalence, regular-
language closure, pumping, Myhill-Nerode, minimization, and decision procedures. Several are also
separately scheduled neighboring targets. The record does not select a machine family, an
alphabet or state type, the meaning of finiteness, words and languages, transition and acceptance
semantics, machine equality or language equivalence, or a conclusion.

Selecting a familiar theorem or conjoining the field would invent or substitute proposition-
changing mathematics. In particular, a `DFA`, `NFA`, or `εNFA` over an arbitrary state type cannot
silently be called finite; pinned mathlib uses an explicit `Fintype` assumption where finiteness is
needed. Myhill-Nerode and the pumping lemma cannot be used as this root because they are separately
owned by `THM-M-0760` and `THM-M-0761`.

Consequently, there is no exact expression whose imports can be certified minimal, no canonical
expression or environment fingerprint, and no approved alternate encoding. Removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations are undefined rather than
passed. The planned intake's proposed redirection also remains pending master acceptance. No
`Statement.lean`, axiom, placeholder, broadened interface, or substituted special case was added.

## Pinned Lean boundary

The existing discovery-only `IntakeProbe.lean` was re-elaborated with these direct imports:

- `Mathlib.Computability.EpsilonNFA`
- `Mathlib.Computability.MyhillNerode`
- `Mathlib.Computability.RegularExpressions`

It checks twenty adjacent language, DFA/NFA/epsilon-NFA, regularity, pumping, regular-expression,
and Myhill-Nerode interfaces. The check exited successfully, with 26 stdout lines and 1986 bytes,
stdout SHA-256 `caeb60e1677705ea59ba8356f3afb3284c64f37bfb34dad748e1220a0ab0c1b9`,
and empty-stderr SHA-256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

Those imports and declarations are adjacent substrate only. The probe declares no canonical
target, checked transport, or proof body, and its imports cannot be certified minimal for an
absent target. A bounded topic search over repo-local Lean and pinned mathlib found the automata
APIs and documentation already exercised by the probe, but no target-specific declaration selected
by the catalog. This is local feasibility evidence, not the later immutable anchor audit or a
global absence claim.

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
| `python3 scripts/stage1_target.py show THM-M-0759` | 0 | rank 1345; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; the base revision and tree are recorded above |
| inspect the target manifest, execution node, repository record, Stage0 projection, computer-science survey, and full intake dossier | 0 | the scheduled root is a topic-only label; no unique source proposition or formal target exists |
| `git blame -L 5591,5596 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short`; `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | package worktree clean; pinned mathlib revision and tree recorded above |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0759/IntakeProbe.lean` | 0 | twenty adjacent APIs elaborated; output hashes recorded above; no canonical target or proof body declared |
| bounded automata-topic `rg` over pinned mathlib, repo-local Lean, and this target | 0 | only adjacent automata APIs, documentation, and the probe disclaimer matched; discovery-only result |
| pre-artifact `python3 -B Stage1_Instances/THM-M-0759/check_intake.py` | 0 | planned intake, `[H5, M4, R4]` boundary, and six open tasks replayed successfully before the statement artifacts were added |
| final `python3 -B Stage1_Instances/THM-M-0759/check_intake.py` | 1 | the intake-only checker rejects any file beyond its frozen nine-file intake inventory, so it stops at line 414 after these two statement blockers appear; the historical intake artifact was not changed |
| scoped prohibited-declaration scan over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0759/statement-blocker.json` and scoped blocker invariants | 0 | structured blocker identity, null target/imports, unchanged vector, false completion flags, undefined mutations, and no-self-test boundary agree |
| whitespace checks for the two new blocker artifacts | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | no worker self-test packet because the assigned statement deliverable did not pass |

## Retry condition and status boundary

The integration lane must master-accept the prerequisite intake and its proposed target decision.
Accountable reviewers must then preserve and hash one lawful immutable primary or approved
authoritative source, select and independently approve one exact proposition, and transcribe every
incorporated definition, ordered binder, hypothesis, conclusion, proof boundary, correction,
erratum, and boundary convention. They must fix the automaton family, alphabet and state carriers,
finiteness and effectiveness conditions, word and language encodings, transition and acceptance
semantics, equality convention, exact result, and ownership boundary with neighboring targets,
then explicitly redirect the current `H5` topic record to that corrected stable proposition.

A later statement run can then encode only that approved claim, minimize its pinned imports,
serialize the elaborated expression and environment, compile all credited transports, and execute
all four mutation classes. This blocker is the assigned phase's truthful result, not completion of
the node or any downstream task. The statement item remains `[ ]`; audit and theorem completion
are false. No statement receipt, worker `[_]`, accepted receipt, proof credit, or master acceptance
is claimed, and no `.stage1-worker-selftest.json` is emitted.
