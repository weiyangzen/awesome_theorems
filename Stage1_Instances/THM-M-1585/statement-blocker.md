# Exact-statement gate: blocked

Item: `S56-M-1585-STATEMENT`

Theorem: `THM-M-1585`

Base revision: `e179b2be594419aa5fb33c3862f73491fdaf113e` (tree
`8c1da8dad4712804811f550b583129e7b73effdc`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1585-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. Rev-5.6 permits a dependency-ordered provisional
attempt, so that pending acceptance did not prevent this assessment. The intake receipt is
non-content-addressed, declares `accepted: false`, has no accepted receipt ID, and intentionally
leaves the canonical mathematical statement and formal target null. Master acceptance remains
required before any future accepted statement transition.

Independently, the exact-statement gate cannot pass. The repository record supplies only the title
`编码理论` (`coding theory`), attribution to many mathematicians, the 20th century, and the gloss
`纠错码的理论` (`the theory of error-correcting codes`). Those fields identify a discipline, not a
truth-valued proposition. They supply no primary source, theorem or page locator, code or channel
model, alphabet or field, ordered binders, hypotheses, conclusion, proof boundary, corrections,
or boundary cases. Stage0 repeats the gloss while explicitly leaving the precise definitions and
premises, proof route, dependencies, alternate forms, axioms, machine status, and artifact links
open. The catalog's `已验证` label is untrusted under rev-5.6.

Coding theory contains materially different theorem families, including packing and existence
bounds, algebraic code constructions, unique-decipherability results, decoder-correctness
guarantees, enumerator identities, and asymptotic rate-distance or channel-coding results. The
repository separately owns many of these as neighboring targets. Selecting the Hamming,
Singleton, or Gilbert-Varshamov bound; a linear, cyclic, BCH, Reed-Solomon, LDPC, Turbo, or Polar
code theorem; Kraft-McMillan; or a Shannon coding theorem would invent, narrow, broaden, or
substitute mathematics rather than elaborate the received target.

The open choices change the proposition itself: alphabet or field; block-code, variable-length,
channel, or asymptotic model; code and decoder representation; distance, rate, probability, and
error conventions; finite or limiting regime; quantifier order; exact conclusion; and empty,
singleton, zero-length, zero-distance, endpoint, ambiguity, tie, and nonexistence cases. No choice
can be frozen from the supplied source record.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing expression
fingerprint hard blockers. There is therefore no honest canonical expression for which minimal
imports, checked alternate transports, or removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations can be certified. Those mutation checks are
undefined, not passed. The root vector remains `[H5, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates in the pinned environment. Its two direct imports
expose generic Hamming-space, uniquely-decodable-source-code, and Kraft-McMillan interfaces. All
nine API checks and three axiom reports pass. This is real feasibility validation, but the probe
defines no error-correcting-code model, canonical proposition, checked transport, or proof body.
Its imports therefore cannot be certified minimal for an absent target and receive no statement
or proof credit.

A bounded lexical search of pinned mathlib and repository-local Lean found only generic Hamming
and source-code documentation plus unrelated coding-theory mentions. It found no declaration for
a general theorem called coding theory. This is discovery-only evidence, not the downstream
immutable anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No update, build, clone, fetch, or
dependency mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1585` | 0 | rank 1207; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| scoped repository source, Stage0, taxonomy, target manifest, blueprint, execution DAG, skill, guidelines, and intake-dossier inspection | 0 | confirmed the umbrella topic, null intake target, neighboring theorem families, and absence of an approved exact source-selected root |
| `sha256sum` over current authority, source, intake, probe, toolchain, and pinned-library inputs | 0 | exact current hashes are recorded in `statement-blocker.json`; historical intake hashes were not rewritten |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1585/IntakeProbe.lean` | 0 | nine adjacent APIs elaborated; stdout SHA-256 `a62fc48c...a51a2`; no canonical target or proof body |
| bounded coding-theory search in pinned mathlib and repo-local Lean | 0 | generic Hamming/source-code and unrelated mentions only; no canonical umbrella declaration; discovery-only evidence |
| `python3 -B Stage1_Instances/THM-M-1585/check_intake.py` | 1 | historical intake replay stops at its stale pre-integration blueprint hash; its original nine-file inventory is also intentionally historical after this phase |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-1585/statement-blocker.json` and scoped blocker assertions | 0 | JSON syntax, current input hashes, identity, null target/imports, unchanged vector, four undefined mutations, completion flags, two-file scope, and absent self-test agree |
| `git diff --check -- Stage1_Instances/THM-M-1585` plus no-index checks for both new files | 0 aggregate | no whitespace diagnostics; no-index exit 1 was only the expected new-file difference |

The intake checker is frozen to its original authority bytes and nine-file intake inventory.
Integration subsequently changed the generated blueprint and execution DAG. Adding these statement
artifacts also makes that inventory historical. This statement run records the limitation instead
of rewriting the intake checker, receipt, instance, task DAG, generated blueprint, or authoritative
execution DAG to manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must master-accept the intake before accepting any later statement
transition. Accountable reviewers must also preserve and hash an immutable primary or
authoritative source, select and independently approve one exact coding-theory proposition, and
transcribe every incorporated definition, convention, ordered binder, hypothesis, conclusion,
proof boundary, correction, erratum, computation policy, and degenerate case while preserving all
neighboring-target boundaries.

A fresh statement run can then encode precisely that source-selected claim, minimize pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
