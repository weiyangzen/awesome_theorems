# THM-M-1596 exact-statement gate: blocked

Item: `S56-M-1596-STATEMENT`

Base revision: `bd81d4853a030765585ef6fed4310484ceb1e458` (tree
`fb92fc7476bff9a2ce8c20f1d7be34c6655ca6b4`). Attempt date: 2026-07-13
(`Asia/Shanghai`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1596-INTAKE` is provisional worker state
`[_]`, not master-accepted state `[x]`. The intake receipt is unaccepted and non-content-addressed,
has no accepted receipt ID, and binds an older repository revision and older blueprint and
execution-DAG hashes. Rev-5.6 section 10.2 permits this dependency-ordered provisional attempt, but
master closure remains dependency ordered.

Independently and decisively, the exact-source-statement gate fails. The complete repository record
is the title `密码学` (`cryptography`), attribution to many mathematicians in the twentieth century,
and the gloss `现代密码学` (`modern cryptography`). It provides no citation, truth-valued proposition,
primitive or protocol, algorithms, message/key/randomness spaces, security parameter,
computational and adversarial model, security experiment, probability or advantage, hardness
assumption, ordered binders, hypotheses, conclusion, reduction, asymptotic convention, proof
boundary, correction history, or boundary cases. Stage0 explicitly leaves the precise definitions
and premises and every formal field open. The catalog's `已验证` label is untrusted metadata.

Modern cryptography contains materially different theorem families: functional correctness of a
scheme, game-based security under an assumption, pseudorandomness and one-wayness constructions,
zero-knowledge and secure-computation results, amplification and composition theorems, and
impossibility or lower-bound results. These require different syntax, algorithms, games,
probability models, assumptions, quantifier orders, and conclusions. The repository selects none
of them. RSA, Diffie-Hellman, elliptic-curve cryptography, zero knowledge, and homomorphic
encryption also have separate neighboring targets. Selecting a famous representative theorem, a
trivial encryption/decryption round trip, or an omnibus conjunction would invent, narrow,
broaden, or substitute proposition-changing mathematics.

Sections 5 and 5.1 of the rev-5.6 standard make statement ambiguity and a missing expression
fingerprint hard blockers. There is no honest canonical Lean expression whose imports can be
certified minimal. The elaborated expression and environment fingerprints, checked alternate
transports, and required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case
mutations are undefined, not passed. No `Statement.lean`, theorem declaration, proof body,
weakened special case, broadened interface, axiom, or placeholder was added. The vector remains
`[H5, M4, R4]`; this classification does not refute correctly stated cryptographic theorems.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` re-elaborates with two direct imports:

- `Mathlib.Computability.TuringMachine.Computable`
- `Mathlib.Probability.Distributions.Uniform`

Its six checks expose finite uniform probability distributions and abstract Turing-machine
polynomial-time interfaces. They define no cryptographic primitive, game, adversary, advantage,
canonical target, checked transport, or proof body. The probe imports therefore cannot be certified
minimal for an absent target and receive no statement or proof credit.

A bounded lexical search of pinned mathlib and repository-local Lean found only the probe's own
disclaimer and unrelated uses of words such as “indistinguishable,” “decrypting,” and
“decipherability.” It located no source-selected cryptography declaration. This is discovery-only
feasibility evidence, not the downstream immutable anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided canonical `.lake` symlink was
used read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation
was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1596` | 0 | rank 1216; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| `git blame -L 11756,11761 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| authority, source, intake, probe, toolchain, lockfile, and relevant mathlib `sha256sum` checks | 0 | exact current hashes are preserved in `statement-blocker.json` |
| `python3 -B Stage1_Instances/THM-M-1596/check_intake.py` | 1 | historical intake replay stops because it expects authoritative intake state `[ ]`, while integration records provisional `[_]`; the original intake-only inventory also becomes historical after this phase |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| mathlib `git rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1596/IntakeProbe.lean` | 0 | six adjacent APIs elaborated; stdout SHA-256 `0f7c39ac3acae54d8f5b6232ce53213e48a59f8383571979e5587d36155737f9`; no canonical target or proof body |
| bounded cryptography target-pattern search over pinned mathlib, repo-local Lean, and the owned target | 0 | only unrelated lexical matches and the probe disclaimer; output SHA-256 `bc038ead2f3e659365f1b9bbcb88f170790b95d29c651d2014f29e3e50f1ccb7` |
| prohibited-construct scan over owned Lean files | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |

Final JSON, invariant, whitespace, scoped-change, and absent-self-test checks are recorded in the
structured blocker beside this report. The historical intake checker is frozen to intake-time
authority inputs and its original artifact inventory. This run records that limitation instead of
rewriting the intake checker, receipt, instance, task DAG, generated blueprint, or authoritative
execution DAG to manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must first master-accept refreshed intake evidence. Accountable reviewers
must then correct, redirect, or split the field label; lawfully preserve and hash one immutable
primary or approved authoritative source; select and independently approve one exact truth-valued
proposition; and freeze every primitive, algorithm, space, computational and adversarial model,
security experiment, probability and advantage, assumption, ordered binder, hypothesis,
conclusion, reduction, asymptotic convention, correction, proof boundary, neighboring-target
boundary, and degenerate case.

A fresh statement worker can then encode precisely that reviewed claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof
credit, or master acceptance is claimed.
