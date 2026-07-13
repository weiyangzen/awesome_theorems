# THM-M-0925 exact-statement gate: blocked

- Item: `S56-M-0925-STATEMENT`
- Base revision: `c79ae75db8880483f10bba17c9bc9dd91a9febcf`
- Base tree: `375fa18a4f8afa63bb51d8b05fb4c804f3bb1240`
- Attempt date: 2026-07-13 (Asia/Shanghai)
- Verdict: blocked; no statement receipt, worker `[_]`, or theorem-completion claim

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
The complete catalog claim is only the title `斐波那契数列` (Fibonacci sequence) and the gloss
`递推序列的经典例子` (a classic example of a recursive sequence). An object name and an example
description are not a truth-valued proposition. The record supplies no formula, definition,
ordered binder, hypothesis, conclusion, source locator, proof boundary, correction, or erratum.
Stage0 explicitly leaves the precise definitions and premises open, and the catalog's `已验证`
label is untrusted under rev-5.6.

The intake dossier therefore deliberately leaves `canonical_statement`, `canonical_claim`, and
the canonical Lean module, declaration, expression hash, and target environment fingerprint null.
It identifies proposition-changing choices that remain unresolved:

- zero-based `Nat.fib` versus Fibonacci's historically shifted rabbit-count sequence;
- a recursive definition versus a recurrence property, an existence-and-uniqueness theorem, or a
  combinatorial counting theorem;
- natural indices and values versus integer, stream, semiring-valued, or other encodings;
- initial values, recurrence orientation, ordered binders, and every boundary case.

Choosing `Nat.fib_add_two` because it is familiar would add all of those missing decisions. It
would not elaborate the exact received target. The neighboring Lucas, Cassini, and Binet targets,
the legacy primitive-divisor toy branch, a computed value, and another Fibonacci identity likewise
cannot substitute for this unidentified root.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing elaborated
expression fingerprint hard blockers. With no canonical proposition, there is no honest target for
which to certify minimal imports, compile source-identity transports, or run the required removed-
hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations. Those mutations are
undefined, not passed. No `Statement.lean`, theorem declaration, assumed predicate, weakened
consequence, or broadened interface was added.

The prerequisite `S56-M-0925-INTAKE` is also only provisional worker state `[_]`. Its receipt is
unaccepted, unsigned, not content-addressed, and has no accepted receipt ID. Rev-5.6 section 10.2
permits this dependency-ordered investigation, but master closure remains dependency ordered.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` imports `Mathlib.Data.Nat.Fib.Basic`. A fresh replay
elaborated these candidate interfaces:

```lean
Nat.fib : Nat -> Nat
Nat.fib_zero : Nat.fib 0 = 0
Nat.fib_one : Nat.fib 1 = 1
Nat.fib_two : Nat.fib 2 = 1
Nat.fib_add_two : Nat.fib (n + 2) = Nat.fib n + Nat.fib (n + 1)
Nat.fib_add_one : n != 0 -> Nat.fib (n + 1) = Nat.fib (n - 1) + Nat.fib n
```

The direct axiom diagnostics report no axioms for `fib_zero` and `fib_one`, and `propext` plus
`Quot.sound` for `fib_add_two` and `fib_add_one`. The probe declares no canonical THM-M-0925 target,
checked source transport, or proof body. Its import is therefore a candidate-interface import, not
a minimal-import certificate for an absent canonical target, and it grants no statement or proof
credit.

A bounded search also found the expected pinned Fibonacci module, Zeckendorf material, and the
foreign legacy `S1_M_018.lean` Fibonacci/Lucas toy branch. These are adjacent formal surfaces, not
evidence selecting the catalog root. This search is statement-feasibility evidence only, not the
downstream anchor or terminal-proof-body audit.

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
| `python3 scripts/stage1_target.py show THM-M-0925` | 0 | rank 1466; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base revision and tree appear above |
| scoped authority/null-target assertions | 0 | rank, dependency states, planned lifecycle, unaccepted intake receipt, null canonical target, and `[H5, M3, R4]` agreed |
| `python3 -B Stage1_Instances/THM-M-0925/check_intake.py` | 1 | historical intake replay stops at `stale receipt input hash: Docs/Stage1_Blueprint_rev-5.6.md`; the intake receipt records an older authority snapshot and was not rewritten |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean and Lake versions agree with the fingerprint above |
| mathlib revision, tree, and status checks | 0 | pinned revision and tree above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0925/IntakeProbe.lean` | 0 | six candidate interfaces and five definition/axiom diagnostics elaborated; 557 output bytes; SHA-256 `10f449b124ae0d7866e7c819768d0685597064a31c1080fa8abafe4697c47ace` |
| bounded Fibonacci search over the owned path, pinned `Mathlib/Data/Nat/Fib`, and repo-local Lean | 0 | found candidate and adjacent interfaces plus a foreign legacy toy branch; no root selection is inferred |
| final JSON parse, scoped blocker assertions, prohibited-declaration scan, and whitespace checks | expected results | recorded in the structured blocker and rerun after final serialization |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test packet intentionally absent because the exact-statement deliverable did not pass |

The historical intake freshness failure is independent of, and weaker than, the decisive
mathematical blocker: even the inputs captured by its original provisional receipt deliberately
freeze no truth-valued root. The intake evidence was preserved rather than modified to manufacture
freshness.

## Retry Condition And Status Boundary

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must
lawfully preserve and hash one immutable primary or approved authoritative source, select or
correct one truth-valued proposition, and independently approve its complete crosswalk. The
decision must fix the sequence definition or counting model, index and value domains, zero- versus
one-based convention, initial values, recurrence role and orientation, ordered binders, hypotheses,
conclusion, proof and translation boundary, corrections, errata, and all degenerate cases.

A fresh statement worker can then encode exactly that approved claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and execute all four mutation classes.

This is a blocked-attempt record, not completion of the statement node or any downstream node. The
root remains `[H5, M3, R4]`, with `audit_complete: false` and `theorem_complete: false`; no debt
change is proposed. Because the assigned phase is not genuinely self-tested to its completion
gate, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof credit, or master
acceptance is claimed.
