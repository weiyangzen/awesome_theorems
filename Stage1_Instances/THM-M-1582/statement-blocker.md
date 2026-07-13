# Exact-statement gate: blocked

Item: `S56-M-1582-STATEMENT`

Theorem: `THM-M-1582`

Base revision: `c2e294becadae6ce784f27ee69f2e8dbf57e0b30` (tree
`3f567e7f76b189432b73444354070c0ff75925b9`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1582-INTAKE` has provisional worker
state `[_]` in the authoritative execution DAG, not master-accepted state `[x]`. Rev-5.6 section
10.2 permits this dependency-ordered attempt, but the intake receipt is non-content-addressed,
declares `accepted: false`, and has no accepted receipt ID. Master acceptance remains required
before any eventual accepted statement transition.

Independently, the statement deliverable cannot be completed from the received repository record.
The catalog gives only the title `Kolmogorov复杂度`, Andrey Kolmogorov, the year 1963, and the gloss
`对象的最小描述长度` (an object's minimum description length). It supplies no bibliography,
definition chain, truth-valued conclusion, object or program domain, computation model, interpreter,
encoding, complexity convention, ordered binder, hypothesis, additive-constant policy, or boundary
case. Stage0 explicitly leaves the precise definitions and premises open, and rev-5.6 treats its
`已验证` label as untrusted.

The inspected primary-source lead does not authorize silently choosing a proposition. Kolmogorov's
1965 paper *Three Approaches to the Definition of the Concept "Quantity of Information"*, Section
3, defines conditional shortest-program complexity for partial recursive description methods and
proves existence of an asymptotically optimal method `A`: for every method `phi`, a constant
`C_phi`, independent of `x` and `y`, bounds `K_A(y | x)` by `K_phi(y | x) + C_phi`. The catalog
does not cite or select that theorem. Its 1963 date instead matches *On Tables of Random Numbers*,
which the 1965 paper describes as an incomplete precursor to the mature complexity treatment.

A bare shortest-description definition, the 1965 optimal-description theorem, bounded-difference
invariance, noncomputability, upper-semicomputability, and an incompressibility counting theorem
have different binders, conclusions, and proof obligations. Plain, prefix-free, conditional,
unconditional, machine-specific, and resource-bounded complexity also give inequivalent targets.
Selecting any one from mathematical familiarity would invent, narrow, broaden, or substitute the
received target.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing elaborated
expression fingerprint hard blockers. There is therefore no honest canonical expression for which
minimal imports, fixed elaboration context, checked transports, or removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations can be certified. Those mutations
are undefined, not passed. The provisional root vector remains `[H5, M4, R4]`; `H5` classifies the
catalog wording as not one stable proposition and does not refute Kolmogorov's published results.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated using the pinned environment. Its direct imports
expose generic encoding, partial-recursive code/evaluation, and finite Turing-machine interfaces.
All nine checks pass. This is real substrate validation, but the probe defines no complexity
function, universal description method, canonical target, checked source-model transport, or proof
body. Its imports cannot be certified minimal for an absent target and receive no statement or
proof credit.

A bounded exact-topic search found only the probe disclaimer in the owned/repo-local Lean scope and
no match in pinned mathlib. Other occurrences of "Kolmogorov" concern probability, stochastic
processes, or topology rather than shortest-program complexity. This is narrow
statement-feasibility evidence, not the downstream immutable anchor audit or a global absence
claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No `lake update`, `lake build`, dependency
clone or fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran from this worker clone on 2026-07-13 (`Asia/Shanghai`) unless another working
directory is stated. Exact argument arrays and results are also recorded in
`statement-blocker.json`.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1582` | 0 | rank 1204; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| initial `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| authority and intake `sha256sum` inventory | 0 | exact hashes are recorded in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean --version`; `lake --version` | 0 | pinned Lean and Lake versions recorded above |
| mathlib revision/tree and package-status checks | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-1582/IntakeProbe.lean` | 0 | nine adjacent interfaces elaborated; stdout SHA-256 `e43d09fc44386892c23f6db5bd140eb7f84df8ba348dafcf72d6a3695714f4ed`; empty stderr; no canonical target declared |
| bounded exact-topic searches recorded in `statement-blocker.json` | 0/1 | repo-local output contained only the probe disclaimer; pinned mathlib returned expected no-match exit 1 |
| `python3 -B Stage1_Instances/THM-M-1582/check_intake.py` | 1 | historical intake checker first fails because it expects intake `[ ]`; current authority records provisional `[_]` and one attempt |
| prohibited Lean construct scan over the owned `*.lean` file | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, axiom, bodyless declaration, or unsafe declaration |
| JSON, scoped blocker invariants, final-newline, and whitespace checks | 0 | identity, null target/imports, four undefined mutations, unchanged debt, false completion flags, exact path scope, and absent self-test agree |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The intake checker is frozen to intake-time authority hashes, the original `[ ]` DAG state, and its
nine-file intake inventory. The integration lane subsequently recorded intake `[_]`; this statement
attempt also adds two owned blocker artifacts. The checker is therefore historical and fails before
it could serve as current statement evidence. It was neither edited nor represented as passing.

## Retry Condition And Status Boundary

Accountable reviewers must preserve and hash lawful immutable primary or approved authoritative
sources, reconcile the 1963 precursor with the 1965 theorem and neighboring records, select and
independently approve one exact truth-valued proposition, and transcribe every incorporated
definition, ordered binder, hypothesis, conclusion, proof boundary, translation, correction,
erratum, and boundary case. They must freeze the computation model, object/program domains,
encoding and pairing, partiality and no-description convention, complexity variant, universality
condition, and allowed dependency of additive constants. The integration lane must also
master-accept refreshed intake evidence.

A later statement run can then encode only that claim, minimize its pinned imports, serialize and
hash the elaborated expression and environment, compile every credited transport, and execute all
four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete` and `theorem_complete` remain false;
no debt-vector change is proposed. Because the statement deliverable did not pass, no
`.stage1-worker-selftest.json`, statement receipt, node receipt, worker `[_]`, master acceptance,
statement fingerprint, or proof credit is claimed.
