# Exact-statement gate: blocked

Item: `S56-M-0758-STATEMENT`

Theorem: `THM-M-0758`

Base revision: `adc87f8ea24dcc7c5e2668c0a5ede0ca5c5f0f55` (tree
`3c83596059f716cde0d50a5f6b390ada6ca7c8e1`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
That record supplies only `可计算枚举度` (computably enumerable degrees), an attribution to many
twentieth-century mathematicians, and the gloss `c.e.度的结构` (the structure of the c.e. degrees).
It contains no truth-valued proposition, source locator, definition chain, ordered binders,
hypotheses, conclusion, proof boundary, corrections, errata, or boundary cases. Stage0 explicitly
leaves the formal system, precise definitions and premises, proof route, dependencies, alternate
forms, axioms, machine state, and artifacts open. The catalog value `已验证` is untrusted metadata.

The prerequisite intake correctly classifies this topic-only root as `[H5, M4, R4]` and leaves its
canonical human claim and Lean target null. Standard c.e.-degree structure theory contains many
inequivalent claims: existence and induced-order facts, joins, density, splitting, cupping,
incomparability, jumps and lowness, definability, and automorphism results. The record also does
not choose whether enumerability is represented by predicates, sets, enumerators, partial-function
domains, or indices; whether degrees use Turing, many-one, one-one, or another reducibility; or
whether a c.e. degree is a subtype of Turing degrees or a separately constructed quotient.

Selecting any familiar result or representation would therefore invent proposition-changing
mathematics. It could also duplicate the separately scheduled Post, Friedberg-Muchnik, general
Turing-degree, join, or jump targets. In particular, mathlib's `ManyOneDegree` cannot silently
replace c.e. Turing degrees merely because it already has upper-semilattice structure.

Consequently there is no exact expression whose imports can be certified minimal, no canonical
expression or environment fingerprint, and no approved alternate encoding. Removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations are undefined rather than passed.
Because `H5` blocks ordinary theorem-proof execution, an accountable target decision must redirect
the record to one corrected stable proposition before a later statement attempt. No
`Statement.lean`, axiom, placeholder, broadened interface, or substituted special case was added.

## Pinned Lean boundary

The existing `IntakeProbe.lean` was re-elaborated with these direct imports:

- `Mathlib.Computability.Halting`
- `Mathlib.Computability.Reduce`
- `Mathlib.Computability.TuringDegree`

It checks ten adjacent computable-enumerability, Turing-reducibility, Turing-degree,
many-one-degree, order, and upper-semilattice interfaces plus two prospective representation
shapes. The check exited successfully, with stdout SHA-256
`411cccb60b25f7b4febb3b277686e5b22f684cfec1c7641fedd67d800adf9ce3` and empty-stderr SHA-256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

Those imports and declarations are adjacent substrate only. The probe neither defines c.e. Turing
degrees nor states a structural theorem, and its imports cannot be certified minimal for an absent
canonical target. A bounded exact-topic search over pinned mathlib and repo-local Lean found no
matching c.e.-degree declaration; the unrelated phrase `source_degree` was the only textual match.
This is local feasibility evidence, not the later immutable anchor audit or a global absence claim.

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
| `python3 scripts/stage1_target.py show THM-M-0758` | 0 | rank 1344; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | before editing, only the automation-provided `.lake` symlink was untracked; the base revision and tree are recorded above |
| inspect the target manifest, execution node, repository record, Stage0 projection, full intake dossier, and source provenance | 0 | the scheduled root is a topic-only label; no unique source proposition or formal target exists |
| `git blame -L 5584,5589 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short`; `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | package worktree clean; pinned mathlib revision and tree recorded above |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0758/IntakeProbe.lean` | 0 | twelve adjacent API and shape checks elaborated; output hashes recorded above; no canonical target or proof body declared |
| bounded exact-topic `rg` search over pinned mathlib, repo-local Lean, and the target probe | 0 only for unrelated `source_degree` text | no c.e.-degree declaration was located; discovery-only result, not a global absence claim |
| `python3 -B Stage1_Instances/THM-M-0758/check_intake.py` | 1 | historical intake replay is stale against the integration-updated blueprint hash; it is not statement evidence and was not changed |
| scoped prohibited-declaration scan over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0758/statement-blocker.json` and scoped blocker invariant assertions | 0 | structured blocker identity, null target/imports, unchanged vector, false completion flags, undefined mutations, and no-self-test boundary agree |
| whitespace checks for the two new blocker artifacts | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | no worker self-test packet because the assigned statement deliverable did not pass |

## Retry condition and status boundary

The integration lane must refresh and master-accept the prerequisite intake evidence against the
current authorities. Accountable reviewers must also lawfully preserve and hash an immutable
primary or approved authoritative source, select and independently approve one exact proposition,
and transcribe every incorporated definition, ordered binder, hypothesis, conclusion, proof
boundary, correction, erratum, and boundary convention. They must fix the c.e. representation,
reducibility, degree construction, order or operation, exact structural result, uniformity and
coding conventions, and ownership boundary with neighboring targets, then explicitly redirect the
current `H5` topic record to that corrected stable proposition.

A later statement run can then encode only that approved claim, minimize its pinned imports,
serialize the elaborated expression and environment, compile all credited transports, and execute
all four mutation classes. This blocker is the assigned phase's truthful result, not completion of
the node or any downstream task. The statement item remains `[ ]`; audit and theorem completion are
false. No statement receipt, worker `[_]`, accepted receipt, proof credit, or master acceptance is
claimed, and no `.stage1-worker-selftest.json` is emitted.
