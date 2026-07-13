# Exact-statement gate: blocked

Item: `S56-M-1581-STATEMENT`

Theorem: `THM-M-1581`

Base revision: `db6914155f1f63e835364b89ba0a3b25f1d7f936` (tree
`a5488edccb2687c4ff0bbdccf4650e06b2e45337`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1581-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. Rev-5.6 section 10.2 permits this
dependency-ordered attempt, so pending acceptance did not prevent the investigation. The intake
receipt is non-content-addressed, declares `accepted: false`, has no accepted receipt ID, and
deliberately leaves the canonical mathematical statement and Lean target null. Its recorded
blueprint and execution-DAG hashes are also older than the current authority files. Master
acceptance of refreshed intake evidence remains necessary before any eventual accepted statement
transition.

Independently, the exact-statement gate cannot pass from the authoritative repository record. It
supplies the family title `香农无噪声编码定理` (Shannon noiseless coding theorem), Claude Shannon,
the year 1948, and only the gloss `数据压缩的极限` (the limit of data compression). It supplies no
citation, source or channel model, entropy definition, code class, loss criterion, rate or length
observable, ordered binders, hypotheses, conclusion, proof boundary, correction history, or
boundary cases. Stage0 explicitly leaves the precise definitions and premises open, and the
catalog's `已验证` label is untrusted under rev-5.6. The gloss is not a binder-complete proposition.

The intake's primary-source inspection identifies a strong candidate, not an adopted canonical
statement. Shannon's 1948 Part I, Section 9, Theorem 9 concerns a source with entropy rate `H` and a
constrained noiseless channel of capacity `C`: nonsingular encoding can approach average
source-symbol rate `C / H`, and no greater average rate is possible. Transcribing that theorem
would require the paper's finite-state ergodic source, constrained-channel, duration, transducer,
entropy-rate, average-rate, nonsingularity, delay, direct/converse, and limiting conventions.

That historical result is not interchangeable with a finite `D`-ary expected-length prefix or
uniquely-decodable inequality, an asymptotic exact-lossless block theorem, or a typical-set
almost-lossless theorem with vanishing error. The candidates change domains, hypotheses, error
policy, quantifier order, boundary behavior, and conclusion. The repository does not select one,
and the related Stage0 record `THM-C-0361` supplies only another gloss, not accepted duplicate
identity or statement authority. Choosing a familiar formulation would invent, narrow, broaden,
or replace mathematics rather than elaborate the exact received target.

Sections 5 and 5.1 of the rev-5.6 standard make statement ambiguity and a missing expression
fingerprint hard blockers. There is no honest canonical expression for which a minimal import set,
checked alternate transport, or the required removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations can be certified. Those mutations are undefined,
not passed. No `Statement.lean`, theorem declaration, axiom, placeholder, weakened special case, or
broadened interface was added.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` re-elaborates in the pinned environment. Its three
direct imports expose eight adjacent probability-mass, scalar entropy-function,
uniquely-decodable-code, and Kraft-McMillan interfaces. All checks pass. The probe defines no source
entropy, expected code length, encoder or decoder, constrained-channel capacity, canonical target,
checked transport, or proof body. Its imports therefore cannot be certified minimal for an absent
canonical statement.

A bounded lexical search of pinned mathlib and repository-local Lean found no target declaration
under source-coding, noiseless-coding, Shannon source/noiseless, expected-code-length, or related
entropy/code-length terms. This is discovery-only feasibility evidence, not the downstream
immutable anchor audit or a global absence claim.

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
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1581` | 0 | rank 1203; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| scoped catalog, Stage0, manifest, blueprint, skill, guidelines, and intake inspection | 0 | confirmed the sparse compression-limit gloss, inequivalent candidate formulations, explicit null canonical target, and unresolved proposition choices |
| `sha256sum` over authority, source, intake, probe, toolchain, manifest, and relevant pinned mathlib inputs | 0 | exact current hashes are recorded in `statement-blocker.json`; historical intake files were not rewritten |
| `python3 -B Stage1_Instances/THM-M-1581/check_intake.py` | 1 | historical intake replay stops at its assertion that intake authority is `[ ]`; the current authoritative DAG records provisional `[_]`, and its original nine-file inventory is intentionally historical after this phase |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-1581/IntakeProbe.lean` | 0 | eight adjacent APIs elaborated; stdout SHA-256 `83e26cac5ff39f0a997aa57747b4742981d9dc7cae21286ea9f0cda504553b7f`; no canonical target or proof body |
| bounded exact-topic search in pinned mathlib and repository-local Lean | 1 | expected no-match result; no target declaration was located under the bounded terms |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-1581/statement-blocker.json` | 0 | the finalized structured blocker parsed as valid JSON |
| scoped statement-blocker invariant assertions | 0 | item and theorem identity, open blocked state, null target and imports, unchanged H1/M4/R4 vector, four undefined mutations, false completion flags, exact two-file change scope, and absent self-test agree |
| `git diff --check -- Stage1_Instances/THM-M-1581` plus per-added-file `git diff --no-index --check /dev/null <file>` | 0 for the scoped check; expected new-file status 1 with empty output for each no-index check | no whitespace diagnostics in either blocker artifact |
| `test ! -e .stage1-worker-selftest.json` | 0 | worker self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The historical intake checker is frozen to its original authority state and intake-only artifact
inventory. This statement run records that limitation instead of rewriting the intake checker,
receipt, instance, task DAG, generated blueprint, or authoritative execution DAG to manufacture
agreement. Final JSON, invariant, whitespace, and absent-self-test checks are recorded in the
structured blocker beside this report.

## Retry Condition And Status Boundary

Accountable reviewers must preserve and hash one lawful immutable primary or authoritative source
edition, select or correct one truth-valued proposition, and independently approve a crosswalk of
every incorporated definition, ordered binder, hypothesis, conclusion, proof boundary, correction,
erratum, and degenerate case. They must decide between historical Shannon Theorem 9 and the modern
finite expected-length, exact-lossless block, or almost-lossless formulations; fix source and code
models, entropy and units, length or rate observable, quantifier order, direct/converse content,
integer and limiting conventions, and all zero/empty boundary cases; and reconcile `THM-C-0361`
without borrowing its state. The integration lane must also master-accept refreshed intake evidence
before accepting a future statement transition.

A fresh statement worker can then encode precisely that reviewed claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
