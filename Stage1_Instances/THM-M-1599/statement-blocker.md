# Exact-statement gate: blocked

Item: `S56-M-1599-STATEMENT`

Theorem: `THM-M-1599`

Base revision: `c2e294becadae6ce784f27ee69f2e8dbf57e0b30` (tree
`3f567e7f76b189432b73444354070c0ff75925b9`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1599-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. Rev-5.6 section 10.2 permits this dependency-ordered
attempt, so pending master acceptance did not prevent the investigation. The intake receipt is
non-content-addressed, declares `accepted: false`, has no accepted receipt ID, and deliberately
leaves the canonical mathematical statement and Lean target null. Master acceptance remains
required before any eventual accepted statement transition.

Independently, the exact-statement gate cannot pass from the authoritative repository record. It
supplies only the title `椭圆曲线密码学` (elliptic-curve cryptography), the attribution Victor
Miller/Neal Koblitz, the year 1985, and the gloss `基于椭圆曲线的密码` (cryptography based on
elliptic curves). It contains no cited proposition, formula, definition chain, ordered binder,
hypothesis, conclusion, proof boundary, correction history, or boundary case. Stage0 explicitly
leaves the precise definitions and premises open, and the catalog's `已验证` label is untrusted under
rev-5.6.

The inspected primary source family confirms rather than resolves this ambiguity. Miller's paper
proposes an elliptic-curve Diffie-Hellman analogue and discusses discrete logarithms, arithmetic,
parameters, implementation, performance, and security heuristics. Koblitz's paper discusses
elliptic analogues of multiple public-key systems, probabilistic plaintext embedding, parameter
questions, and a separate theorem and corollary about nonsmooth cyclic-subgroup orders. The
catalog cites neither passage and selects none of these materially different claims.

The repository therefore does not decide whether the root is honest-output agreement for ECDH,
encryption/decryption correctness, signature correctness, a security reduction, a hardness claim,
a parameter theorem, an algorithmic correctness or complexity theorem, or another proposition. It
also fixes no finite field, curve, subgroup, base point, scalar convention, key or message space,
randomness, algorithm, adversary, experiment, assumption, resource model, quantifier order,
conclusion, computation policy, or failure semantics. Selecting ECDH, EC ElGamal, ECDSA, ECIES,
ECDLP, CDH, DDH, a group-law identity, or a toy curve would invent, narrow, broaden, or substitute
mathematics rather than elaborate the exact received target.

Sections 5 and 5.1 of the rev-5.6 standard make statement ambiguity and a missing expression
fingerprint hard blockers. There is consequently no honest canonical expression for which minimal
imports, checked transports, or the required removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations can be certified. Those mutations are undefined,
not passed. The vector remains `[H5, M4, R4]`. No `Statement.lean`, theorem declaration, axiom,
placeholder, weakened special case, or broadened interface was added.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` re-elaborates in the pinned environment. Its sole
direct import, `Mathlib.AlgebraicGeometry.EllipticCurve.Projective.Point`, exposes generic
Weierstrass curves, ellipticity, projective points, their additive commutative group instance, and
the projective conversion. All five checks pass; the group instance reports the axioms `propext`,
`Classical.choice`, and `Quot.sound`.

This is real substrate validation, but the probe defines no finite cryptographic subgroup,
cryptosystem, correctness relation, security experiment, adversary, hardness assumption,
canonical target, checked transport, or proof body. Its import therefore cannot be certified
minimal for an absent canonical statement. The axiom report grants no target statement or proof
credit.

A bounded lexical search of pinned mathlib and repository-local Lean found no elliptic-curve
cryptosystem, ECDH, ECDSA, ECIES, ElGamal, or discrete-logarithm declaration under the recorded
terms. The only hit was an irrelevant English word in a list-permutation docstring. This is
discovery-only feasibility evidence, not the downstream immutable anchor audit or a global absence
claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No `lake update`, `lake build`, dependency
clone or fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1599` | 0 | rank 1219; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| scoped catalog, Stage0, manifest, blueprint, skill, and intake inspection | 0 | confirmed the topic-family gloss, multiple inequivalent source results, null intake target, and absence of an approved proposition selection |
| `sha256sum` over authority, source, intake, probe, toolchain, manifest, and relevant pinned mathlib inputs | 0 | exact current hashes are recorded in `statement-blocker.json`; historical intake authority hashes were not rewritten |
| `python3 -B Stage1_Instances/THM-M-1599/check_intake.py` | 1 | the historical intake checker freezes its pre-integration authority state as `[ ]` with attempts `0`, while the current DAG records provisional `[_]` with attempts `1`; its nine-file inventory is also historical after this phase |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1599/IntakeProbe.lean` | 0 | five generic curve/point APIs elaborated; the group-instance axiom report is `[propext, Classical.choice, Quot.sound]`; complete stdout SHA-256 `752e249ce4e086caed93deca03ece8606dddf47ca35d53fdaec8ed41d8576bc0`; no canonical target or proof body |
| bounded exact-topic search in pinned mathlib and repo-local Lean | 0 | only an irrelevant docstring word matched; no target declaration was located under the recorded terms |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-1599/statement-blocker.json` and scoped blocker assertions | 0 | JSON parsed; identity, open blocked state, null target/imports, unchanged H5/M4/R4 vector, four undefined mutations, completion flags, two-file scope, and absent self-test agree |
| `git diff --check -- Stage1_Instances/THM-M-1599` plus per-added-file no-index checks | 0 aggregate | no whitespace diagnostics; raw no-index commands returned only the expected new-file difference status 1 |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The historical intake checker is frozen to its original authority bytes and nine-file intake
inventory. Integration subsequently changed the generated blueprint and execution DAG. Adding
these statement artifacts also makes that inventory historical. This statement run records the
limitation instead of rewriting the intake checker, receipt, instance, task DAG, generated
blueprint, or authoritative execution DAG to manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must master-accept refreshed intake evidence before accepting any later
statement transition. Accountable reviewers must preserve and hash one lawful immutable primary
or authoritative source, select and independently approve one exact truth-valued elliptic-curve
cryptography proposition, and transcribe every incorporated definition, ordered binder,
hypothesis, conclusion, proof boundary, correction, erratum, computation policy, and boundary case
while preserving neighboring-target ownership.

A fresh statement run can then encode precisely that source-selected claim, minimize pinned
imports, serialize and hash its elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
