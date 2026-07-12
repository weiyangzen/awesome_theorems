# Exact-statement gate: blocked

Item: `S56-M-0077-STATEMENT`

Theorem: `THM-M-0077`

Base revision: `3815f6945257af057dfb5e6b6dfe2be5b6f451d9` (tree
`21a4f0ff758e83ab68c05b7741cdc4720f95cb1c`).

## Decision

The statement item remains `[ ]`. Its prerequisite intake is only provisional worker state `[_]`:
the intake receipt declares `accepted: false`, is not content-addressed, and has no accepted receipt
ID. Provisional statement inspection is still useful under concurrent scheduling, but master
closure remains dependency ordered. The decisive blocker is independent of that receipt state: the
intake deliberately leaves the exact mathematical statement and formal target null.

The repository gives only the existence gloss "Hall subgroups in finite solvable groups." It does
not say what collection of primes `pi` ranges over, define a Hall `pi`-subgroup, give ordered
binders, choose a finite-group encoding, settle boundary cases, or identify an exact primary-source
proposition. The intake identifies P. Hall's 1928 article *A Note on Soluble Groups*, pages 98-105,
DOI `10.1112/jlms/s1-3.2.98`, but no immutable primary text, theorem/page locator, incorporated
definitions, literal proposition, proof mapping, correction or errata review, or independent source
approval is present.

Material choices therefore remain unresolved:

- `pi` as `Set Nat`, a predicate, `Finset Nat`, or support normalized to the group order;
- a Hall predicate expressed through prime divisors of subgroup order and index, a largest
  `pi`-divisor factorization, or coprimality plus enough data to retain the chosen support;
- `Finite G` versus `Fintype G`, universes, typeclass order, explicit hypotheses, binder order, and
  coercions;
- empty `pi`, all primes, irrelevant primes, the trivial group, and the `bot`/`top` subgroup cases;
  and
- which implications or equivalences among the candidate encodings are part of the target.

These formulations are related but are not interchangeable without checked transports. In
particular, bare coprimality of subgroup order and index can lose the selected `pi`, while adding
the familiar conjugacy and containment branches would broaden the repository's existence-only
gloss. Selecting one convenient proposition now would invent or substitute a target. Sections 5
and 5.1 of the rev-5.6 standard make statement ambiguity and a missing expression fingerprint hard
blockers. There is consequently no honest canonical target whose imports can be minimized or whose
four semantic mutation classes can be credited. The root vector remains `[H1, M4, R4]`.

## Pinned Lean boundary

The existing `IntakeProbe.lean` was re-elaborated with the pinned toolchain. It authenticates
`IsSolvable`, `isSolvable_def`, and three Hall-adjacent facts:

- `Sylow.card_coprime_index`, a one-prime special case;
- `IsZGroup.coprime_commutator_index`, restricted to finite Z-groups; and
- `Subgroup.exists_right_complement'_of_coprime`, which starts from a normal Hall subgroup and
  constructs a complement.

The representative terms elaborate under their stated finite-group contexts. The three imported
facts report axioms `[propext, Classical.choice, Quot.sound]`. A bounded search found no separate
repository-local general Hall-`pi` existence declaration for finite solvable groups. This is real
API feasibility evidence only. The probe deliberately defines no canonical target, checked source
transport, expression fingerprint, proof wrapper, or target proof. Its three imports cannot be
called minimal for an absent canonical target.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided `.lake` symlink was used
read-only. No update, build, clone, fetch, or dependency mutation was run.

## Validation

Commands ran from the repository root on 2026-07-13 Asia/Shanghai unless another working directory
is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0077` | 0 | rank 1025, planned, no legacy slot, legacy artifacts unaccepted, theorem completion false |
| `git rev-parse HEAD 'HEAD^{tree}'` and initial `git status --short --untracked-files=all` | 0 | base revision/tree above; only the automation-provided untracked `Formalizations/Lean/.lake` existed |
| `cd Formalizations/Lean && lake env lean --version` and `lake --version` | 0 | Lean and Lake agree with the pinned environment above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision/tree above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0077/IntakeProbe.lean` | 0 | five interfaces and three representative terms elaborated; output 910 bytes, 11 lines, SHA-256 `29d1c04fb9c791cea5e6773b3a9a59dc88967ce30706ada84f8bcabcbb09b30a` |
| bounded `rg` over repo-local Lean and pinned mathlib | 0 | the intake probe and special Hall-adjacent comments matched; no general target declaration was located |
| `python3 -B Stage1_Instances/THM-M-0077/check_intake.py` | 1 | the historical checker expects intake authority state `[ ]`; current authority records provisional `[_]` |
| `python3 -m json.tool Stage1_Instances/THM-M-0077/statement-blocker.json` and scoped blocker assertions | 0 | blocker syntax, identity, null target/imports, four undefined mutations, unchanged vector, false completion flags, exact change scope, and absent self-test agree |
| prohibited-construct scan over owned Lean | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, axiom, constant, opaque, or unsafe declaration |
| `git diff --check` plus new-file whitespace checks | 0 aggregate | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | no self-test manifest exists because the assigned statement deliverable is blocked |

The intake checker is an intake-only historical validator. It froze the earlier authoritative `[ ]`
state, while current execution authority records the provisional intake proposal as `[_]`. This
statement attempt does not rewrite the intake checker, receipt, task DAG, blueprint, or authoritative
execution DAG to manufacture agreement.

## Retry condition

The integration lane must master-accept current intake evidence. Accountable reviewers must then
preserve and hash an immutable primary edition, locate and independently approve the exact
existence proposition, and freeze every incorporated definition, `pi` convention, binder,
hypothesis, conclusion, support condition, boundary case, correction, erratum, and translation
decision.

A later statement worker can then encode exactly that claim, minimize its pinned imports, serialize
and hash the elaborated expression and environment, compile every credited transport, and run the
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations.

This is a blocked-attempt record, not completion of the statement node or any downstream node.
`audit_complete` and `theorem_complete` remain false. Because the assigned phase is not genuinely
self-tested to its completion gate, no `.stage1-worker-selftest.json`, statement receipt, worker
`[_]`, or master acceptance is claimed.
