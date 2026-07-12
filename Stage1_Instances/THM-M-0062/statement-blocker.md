# Exact-statement gate: blocked

Item: `S56-M-0062-STATEMENT`

Theorem: `THM-M-0062`

Base revision: `bdb4ee4eb79433800f3b28633d046959f18b57e9` (tree
`8a7b02bd1c876c4f44ab2e5863e71534155c2629`).

## Decision

The statement item remains `[ ]`. Rev-5.6 section 10.2 permits this provisional later-node
inspection while concurrency is enabled even though prerequisite `S56-M-0062-INTAKE` is only
worker state `[_]`; master closure would still remain dependency ordered. The decisive blocker is
the intake's deliberately unresolved exact source statement, described below. Separately, its
provisional receipt declares `accepted: false`, is not content-addressed, has no accepted receipt
ID, and fails replay at the current revision because its recorded blueprint hash is stale. Those
receipt conditions would also have to be repaired before eventual master acceptance.

Independently, the exact-statement gate cannot pass from the received claim. The repository gives
only the label "Sylow theorems" and the gloss "existence, conjugacy, and counting of p-subgroups in
finite groups." It supplies no definition of a `p`-subgroup, ordered binders, formula, precise
counting bundle, normalizer convention, boundary cases, theorem passage, proof boundary, errata
disposition, translation, or source reviewer.

The intake inspected L. Sylow, *Theoremes sur les groupes de substitutions*, *Mathematische
Annalen* 5 (1872), Theorems I-II on printed pages 586-587, from the Zenodo 2329278 scan with
SHA-256 `92a14121c0b0344aefeb9a8ba8a78d685443d5f97dc8bb3663144cab830415bf`.
Those passages support maximal-prime-power existence, conjugacy, a count congruent to one modulo
the prime, and a transformation/normalizer factor. But the intake explicitly leaves the historical
finite-substitution-group to arbitrary-finite-group transport, notation reconstruction, exact
modern counting clauses, corrections/errata, translation, complete premise/proof mapping, and
independent source approval open.

Material choices therefore remain unresolved:

- maximality among `p`-subgroups versus cardinality equal to the largest prime power dividing
  `|G|`, and the checked directions relating them;
- `Finite G` versus `Fintype G`, explicit primality versus a `Fact` instance, universes, coercions,
  ordered binders, and quantifier order;
- existence as `Nonempty (Sylow p G)`, an exact-order subgroup, or a conjunction with transport;
- conjugacy of exact-order subgroups, equality after the conjugation action, or a transitivity
  predicate;
- whether counting includes congruence only, divisibility by a Sylow index, equality with a
  normalizer index, or all three clauses; and
- the cases where the prime does not divide the group order, the trivial group, a finite
  `p`-group, and a normal/unique Sylow subgroup.

These alternatives are closely related but not definitionally the same proposition. Selecting a
convenient modern bundle without the intake-required independent source approval would invent or
substitute the canonical claim. Sections 5 and 5.1 of the rev-5.6 standard make that ambiguity and
a missing expression fingerprint hard blockers. There is consequently no honest canonical target
whose imports can be certified minimal or whose required semantic mutations can be credited.
The root vector remains `[H1, M3, R4]`.

## Pinned Lean boundary

The existing `IntakeProbe.lean` was re-elaborated with the pinned toolchain. Its sole import,
`Mathlib.GroupTheory.Sylow`, exposes compatible candidates for all three branches:

- `Sylow.nonempty`, `Sylow.exists_subgroup_card_pow_prime`, and
  `Sylow.card_eq_multiplicity`;
- `Sylow.isPretransitive_of_finite` and `MulAction.exists_smul_eq`; and
- `card_sylow_modEq_one`, `Sylow.card_dvd_index`, and
  `Sylow.card_eq_index_normalizer`.

Representative calls elaborate under `[Group G] [Finite G]` and a prime, and the imported
candidates report axioms `[propext, Classical.choice, Quot.sound]`. A bounded repo-local and pinned
mathlib search found no separate `THM-M-0062` canonical declaration. This is real API feasibility
evidence only. The probe deliberately defines no combined target, checked source transport,
expression fingerprint, proof wrapper, terminal-body audit, or M0 evidence. Its import therefore
cannot be certified minimal for the absent canonical target.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No update, build, clone, fetch, or
dependency mutation was run.

## Validation record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0062` | 0 | rank 1023; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base identifiers appear above |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| pinned mathlib revision/tree and package-status checks | 0 | revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0062/IntakeProbe.lean` | 0 | ten adjacent definitions/declarations checked, five axiom sets printed, and six representative existence, conjugacy, and counting calls elaborated; no canonical target declared |
| bounded exact-target search in repo-local Lean and pinned mathlib | 0 | only the intake probe and mathlib's general Sylow module were found; no target-specific canonical expression |
| `python3 -B Stage1_Instances/THM-M-0062/check_intake.py` | 1 | intake replay stops at `stale receipt input hash: Docs/Stage1_Blueprint_rev-5.6.md` |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0062/statement-blocker.json` plus scoped blocker invariants | 0 | identity, dependency state, null target/imports, unchanged vector, four undefined mutations, false completion flags, and no-self-test boundary agree |
| per-file `git diff --no-index --check /dev/null` for both new blocker files; `git diff --check -- Stage1_Instances/THM-M-0062` | 0 diagnostics | no whitespace diagnostics; each no-index command exits 1 only because the file is new |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The intake receipt recorded blueprint SHA-256 `bcbce90f...1c1d72` and execution-DAG SHA-256
`0f01e506...23bfcd0`; current authority is `f4c68355...431a1` and
`8ba2d907...48160`. This statement run records that stale evidence rather than rewriting the
intake receipt, instance manifest, target-local DAG, generated checklist, or authoritative DAG.

## Retry condition and status boundary

Accountable source reviewers must preserve an immutable source edition, transcribe and independently approve the
exact historical-to-modern target, settle every incorporated definition, ordered binder,
hypothesis, conclusion, counting clause, normalizer convention, transport, boundary case,
correction, erratum, and translation decision, and identify the reviewed statement passage. A
future statement worker can then encode that same claim, minimize pinned imports, serialize and
hash its elaborated expression and environment, compile every credited transport, and execute the
four required mutation classes. The integration lane must also revalidate and master-accept the
intake dependency before it can accept the future statement node.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
