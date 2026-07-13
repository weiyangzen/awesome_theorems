# THM-M-0924 exact-statement gate: blocked

- Item: `S56-M-0924-STATEMENT`
- Base revision: `b243ebc0f9058ba5afafef8240b92c2dfb2edc6e`
- Base tree: `b4b092069141ac54ea1ab5a6ea946192a30ec78c`
- Attempt date: 2026-07-13 (Asia/Shanghai)
- Verdict: blocked; no statement receipt, worker `[_]`, or theorem-completion claim

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
The complete catalog claim is only the title `卢卡斯数` (Lucas numbers) and the gloss
`斐波那契数列的推广` (a generalization of the Fibonacci sequence). An object or sequence-family
name and a relationship gloss are not a truth-valued proposition. The record supplies no formula,
definition, ordered binder, hypothesis, conclusion, source locator, proof boundary, correction, or
erratum. Stage0 explicitly leaves the precise definitions and premises open, and the catalog's
`已验证` label is untrusted under rev-5.6.

The intake dossier therefore deliberately leaves `canonical_statement`, `canonical_claim`, and
the canonical Lean module, declaration, expression hash, and target environment fingerprint null.
It identifies proposition-changing choices that remain unresolved:

- the classical companion sequence `L(0) = 2`, `L(1) = 1` versus general `U_n(P,Q)` or
  `V_n(P,Q)` families;
- a recursive definition versus a recurrence property, existence-and-uniqueness theorem,
  Fibonacci relation, closed formula, divisibility law, or combinatorial interpretation;
- index and value domains, parameters, recurrence signs and orientation, ordered binders,
  hypotheses, conclusion, and all boundary cases.

Choosing the familiar classical recurrence, `Nat.fib_add_two`, or a generic
`LinearRecurrence` result would add those missing decisions. It would not elaborate the exact
received target. The neighboring Fibonacci, Cassini, and Binet targets, the legacy primitive-
divisor `U`-sequence branch, Lucas-Lehmer tests, and another recurrence identity likewise cannot
substitute for this unidentified root.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing elaborated
expression fingerprint hard blockers. With no canonical proposition, there is no honest target
for which to certify minimal imports, compile source-identity transports, or run the required
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations. Those
mutations are undefined, not passed. No `Statement.lean`, theorem declaration, assumed predicate,
weakened consequence, or broadened interface was added.

The prerequisite `S56-M-0924-INTAKE` is also only provisional worker state `[_]`. Its receipt is
unaccepted, unsigned, not content-addressed, and has no accepted receipt ID. It is stale against
the current blueprint and execution-DAG hashes. Dependency-ordered investigation is possible, but
master closure remains dependency ordered and the stale intake replay is not statement evidence.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` imports
`Mathlib.Algebra.LinearRecurrence` and `Mathlib.Data.Nat.Fib.Basic`. A fresh replay elaborated the
generic recurrence construction, solution, and uniqueness interfaces together with `Nat.fib` and
its basic recurrence. The probe's axiom diagnostics report
`[propext, Classical.choice, Quot.sound]` for the checked generic recurrence candidates and
`[propext, Quot.sound]` for `Nat.fib_add_two`.

The probe declares no canonical THM-M-0924 target, checked source transport, or proof body. Its two
imports are candidate-interface imports, not a minimal-import certificate for an absent target,
and grant no statement or proof credit. A bounded exact-phrase search of the pinned packages found
only a prose mention of Lucas sequences in `EllipticDivisibilitySequence.lean`. The repo-local
`AwesomeTheorems.Stage1.S1_M_018.lucasSequence` belongs to THM-M-0405, begins with `0,1`, models a
general first-kind `U` family, and is foreign unaccepted discovery material. These observations are
statement-feasibility evidence only, not the downstream anchor audit or a global absence theorem.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` link to canonical pinned artifacts was used read only. No dependency
update, build, clone, fetch, or other `.lake` mutation was run.

## Validation Evidence

Commands ran in this isolated worker clone on 2026-07-13 (Asia/Shanghai), from the repository root
unless another working directory is shown. Exact arguments, exits, and current input hashes are
also recorded in `statement-blocker.json`.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0924` | 0 | rank 1544; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base revision and tree appear above |
| scoped authority, dependency, and null-target inspection | 0 | intake `[_]`, statement `[ ]`, planned lifecycle, unaccepted receipt, null canonical target, and `[H5, M4, R4]` agreed |
| `python3 -B Stage1_Instances/THM-M-0924/check_intake.py` | 1 | historical intake replay stopped at `stale receipt input hash: Docs/Stage1_Blueprint_rev-5.6.md`; intake evidence was preserved rather than rewritten |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean and Lake versions agree with the fingerprint above |
| mathlib revision, tree, and status checks | 0 | pinned revision and tree above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0924/IntakeProbe.lean` | 0 | generic recurrence and Fibonacci interfaces elaborated; stdout was 1,587 bytes with SHA-256 `2860e9bc98e492ac65d7b24ca8a322694a7c4e304b20347cc1fa2738480d5429`; no target or proof body was declared |
| bounded exact-topic search in pinned packages and repo-local Lean | 0 | one pinned prose hit and the foreign legacy `U`-sequence branch; neither selects the root |
| final JSON parse, scoped blocker assertions, prohibited-declaration scan, and whitespace checks | expected results | recorded in the structured blocker and rerun after final serialization |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test packet intentionally absent because the exact-statement deliverable did not pass |

The historical intake freshness failure is independent of, and weaker than, the decisive
mathematical blocker: even the inputs captured by its original provisional receipt deliberately
freeze no truth-valued root. The intake evidence was not modified to manufacture freshness.

## Retry Condition And Status Boundary

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must
lawfully preserve and hash one immutable primary or approved authoritative source, select or
correct one truth-valued proposition, and independently approve its complete crosswalk. The
decision must fix classical `L` versus a general `U/V` family; parameters; initial values;
recurrence signs, orientation, and role; index and value domains; ordered binders; hypotheses;
conclusion; proof and translation boundary; corrections; errata; and all degenerate cases.

A fresh statement worker can then encode exactly that approved claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and execute all four mutation classes.

This is a blocked-attempt record, not completion of the statement node or any downstream node. The
root remains `[H5, M4, R4]`, with `audit_complete: false` and `theorem_complete: false`; no debt
change is proposed. Because the assigned phase is not genuinely self-tested to its completion
gate, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof credit, or master
acceptance is claimed.
