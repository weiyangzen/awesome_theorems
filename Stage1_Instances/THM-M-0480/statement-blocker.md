# Exact-statement gate: blocked

Item: `S56-M-0480-STATEMENT`

Theorem: `THM-M-0480` (prime number theorem)

Base revision: `db4b8793e70ce8af74c9c9490acfa50aa3684d5e` (tree
`6434a20532ae7c523ad293e67a6228ab384bfb8a`).

## Decision

The exact Lean 4 target cannot yet be truthfully selected. The statement item remains `[ ]`.
Its prerequisite `S56-M-0480-INTAKE` has provisional worker state `[_]`, not master-accepted state
`[x]`; its receipt is unaccepted and non-content-addressed. Rev-5.6 permits dependency-ordered
inspection of provisional work, but not dependency closure.

The independent statement blocker is mathematical identity. The complete repository claim is only
the uncited formula `pi(x) ~ x/ln(x)`. It does not determine:

- whether `pi` counts primes below or at most an endpoint;
- a natural sequence or real-variable domain, or the associated `atTop` filter;
- casts, a floor or ceiling extension, negative real inputs, or values between integers;
- the logarithm convention, grouping, and behavior at zero and one;
- `Asymptotics.IsEquivalent`, a ratio limit, a normalized limit, or another asymptotic relation; or
- ordered binders, credited alternate forms, checked transports, and boundary cases.

These omissions change the proposition. The intake records a Hadamard bibliographic lead, but no
immutable source proposition and incorporated definitions have been pinpointed, transcribed,
crosswalked through the proof and errata boundary, and independently approved. No de la Vallee
Poussin pinpoint is recorded. Choosing a familiar natural-sequence, real-floor, theta/psi, ratio,
or normalized encoding now would invent or substitute proposition-changing clauses.

There is therefore no approved expression whose imports can be certified minimal, no credited
alternate form for a checked transport, and no meaningful removed-hypothesis, changed-domain,
changed-binder-scope, or boundary-case mutation suite. Those four outputs are undefined, not
passed. The root vector remains `[H1, M3, R4]`; no debt change is proposed.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` imports `Mathlib.NumberTheory.Chebyshev`. Against
pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, it elaborates:

- `Nat.primeCounting`, its divergence, `Real.log`, and `Filter.atTop`;
- `Asymptotics.IsEquivalent` and its eventual-nonzero ratio characterization;
- `Chebyshev.theta` and `Chebyshev.psi`;
- a prime-counting identity, an integral little-o estimate, a remainder Big-O estimate, and an
  eventual one-sided upper bound.

The three representative theorem reports use `propext`, `Classical.choice`, and `Quot.sound`.
This is real kernel-checked interface evidence, but it does not select the source proposition,
declare a canonical target, supply the missing theta asymptotic, certify minimal imports for an
absent target, or provide terminal PNT proof credit. A bounded repo-local and pinned-mathlib search
located adjacent definitions, reductions, estimates, prerequisites, and legacy metadata, but no
terminal PNT declaration was located or credited in that searched closure. This is not an
exhaustive downstream anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided `.lake` link was used
read-only. No `lake update`, `lake build`, dependency clone or fetch, or other dependency mutation
was performed.

## Validation Record

Commands ran in this isolated worker clone on 2026-07-13 (`Asia/Shanghai`). Lean commands ran from
`Formalizations/Lean`; all other commands ran from the repository root unless noted.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0480` | 0 | rank 1361; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base revision and tree appear above |
| `git blame -L 3525,3530 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog fields originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| pinned mathlib `git rev-parse HEAD 'HEAD^{tree}' 'HEAD:Mathlib/NumberTheory/Chebyshev.lean'` and package status | 0 | pinned revision, tree, and Chebyshev source blob recorded in `statement-blocker.json`; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0480/IntakeProbe.lean` | 0 | twelve interfaces, reductions, and estimates elaborated; stdout 1693 bytes, 21 lines; SHA-256 `e5559811951d4811a494a093255f44500cd9247a6bfb3dcca02cb8dcb30980e1` |
| bounded exact-topic search over repo-local and pinned-mathlib Lean | 0 | adjacent definitions, reductions, estimates, prerequisites, and legacy metadata found; no terminal PNT declaration located or credited in the searched closure |
| pre-edit `LC_ALL=C TZ=UTC python3 -B Stage1_Instances/THM-M-0480/check_intake.py` | 0 | `intake invariant check: ok (THM-M-0480 planned; H1/M3/R4; six open tasks)` |
| post-edit `LC_ALL=C TZ=UTC python3 -B Stage1_Instances/THM-M-0480/check_intake.py` | 1 | expected historical-checker boundary: line 239 rejects the two statement files because it freezes the predecessor's intake-only inventory |
| `python3 -m json.tool Stage1_Instances/THM-M-0480/statement-blocker.json` plus scoped semantic assertions | 0 | valid JSON; identity, blocked state, null target/imports, unchanged vector, undefined mutations, false completion flags, exact two-file scope, and absent self-test agree |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-0480` plus per-new-file no-index checks | 0; 1 each | no whitespace diagnostics; both no-index exits are only the expected new-file differences |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The intake checker freezes the predecessor's intake-only owned-file inventory. Once these two
statement blocker files exist, a post-edit replay is expected to stop at that historical inventory
assertion. This statement phase records the boundary rather than rewriting the intake checker or
receipt to manufacture agreement.

The scoped semantic assertions also verify that no statement receipt, expression fingerprint,
proof body, accepted state, debt change, audit completion, or theorem completion is claimed.

## Retry Condition And Status Boundary

Accountable reviewers must preserve and hash an immutable primary or approved authoritative source,
select and independently approve one exact PNT proposition, and transcribe every incorporated
definition, ordered binder, hypothesis, conclusion, proof boundary, correction, erratum,
translation choice, and boundary case. The decision must fix prime-counting and its endpoint, the
domain and filter, floor and casts, logarithm, asymptotic relation, alternate forms, and transports.

The integration lane must also revalidate and master-accept the intake dependency. A fresh statement
worker can then encode exactly that approved claim, minimize its pinned imports, serialize and hash
the elaborated expression and environment, compile every credited transport, and execute all four
required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement item or any
downstream item. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof
credit, or master acceptance is claimed.
