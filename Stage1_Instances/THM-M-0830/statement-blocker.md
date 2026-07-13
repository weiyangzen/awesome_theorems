# Exact-statement gate: blocked

Item: `S56-M-0830-STATEMENT`

Theorem: `THM-M-0830`

Base revision: `748243faadc15828fb087059337fd05b7be9fdeb` (tree
`e46d642646f80980838b6f016f5d69b817bd464d`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
That record gives the family label `Push-Relabel algorithm`, the Goldberg/Tarjan attribution and
1988 date, and only the gloss `the push-relabel algorithm for maximum flow`. It supplies no
truth-valued conclusion, theorem locator, definition boundary, ordered binders, hypotheses,
correction or errata status, or independent source approval. Stage0 explicitly leaves the precise
definitions and premises open, and rev-5.6 treats the catalog's `verified` label as untrusted.

The inspected Goldberg-Tarjan paper contains several materially different results in the named
family:

- Theorem 3.4 gives conditional maximum-flow correctness if the generic preflow algorithm
  terminates with finite distance labels.
- Theorem 3.11 gives termination and an `O(n^2 m)` bound on basic push/relabel operations.
- Theorem 4.5 gives an `O(n^3)` running-time bound for FIFO scheduling on the paper's sequential
  implementation, relying on a concrete refinement and cost boundary.

The catalog does not select one of these results or an exact composite. The distinct `THM-C-0099`
survey row's `O(V^3)` wording is neighboring scope evidence, not authority to redefine this target.
Choosing correctness, termination, generic operation complexity, FIFO complexity, or a conjunction
would therefore make an unapproved proposition-selection decision and invent the missing target.

Even after a root is selected, the source-to-Lean decision must freeze the finite directed-network
model, capacity and flow carriers, source/sink and edge conventions, flow/preflow/excess/residual
definitions, initialization, valid labels, push/relabel/discharge transitions, scheduling and tie
semantics, termination and output relation, maximality bridge, cost model, asymptotic variables, and
all degenerate cases. None of these choices is presently approved.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing elaborated
expression fingerprint hard blockers. The intake correctly leaves the canonical mathematical
claim, Lean module and expression, minimal imports, and expression/environment fingerprints null at
`[H1, M4, R4]`. Without a canonical target, credited transports and the required
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations are undefined,
not passed. No `Statement.lean`, axiom, placeholder, assumed algorithm theorem, restricted variant,
or generated substitute was introduced.

The prerequisite `S56-M-0830-INTAKE` is provisional worker state `[_]`, not master-accepted `[x]`.
Its mutable receipt declares `accepted: false`, is not content-addressed, and has no accepted receipt
ID. Section 10.2 permits this dependency-ordered blocker attempt, but master acceptance remains a
separate prerequisite for any future accepted statement transition.

Accordingly, dependency freshness revalidation and master acceptance are the first overall failed
completion gate. Exact source-statement identity and result selection are the first intrinsic
statement gate and would still block this phase independently after the dependency is accepted.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates in the pinned environment. Its three direct imports
expose directed adjacency, quiver paths and additive path weights, and finite sums. All six checks
pass. The probe defines no flow network, preflow, residual network, push/relabel transition system,
execution, maximum-flow predicate, cost model, canonical target, checked transport, or proof body.
Its imports are substrate imports, not a minimal import set for an absent target, and receive no
statement or proof credit.

A bounded case-insensitive search of repository-local and pinned-mathlib Lean sources found no
push-relabel, preflow, maximum-flow, flow-network, or residual-network formal artifact. This is
statement-feasibility evidence only, not the downstream immutable anchor audit or a claim of global
absence.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` link to canonical pinned artifacts was used read-only. No `lake update`,
`lake build`, dependency clone or fetch, or other `.lake` mutation was run.

## Validation Evidence

Commands ran in this worker clone on 2026-07-13 (`Asia/Shanghai`), from the repository root unless
a different working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0830` | 0 | rank 1388, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; the base revision and tree are recorded above |
| scoped manifest, blueprint, skill, catalog, Stage0, intake, and primary-source crosswalk inspection | 0 | only an algorithm-family gloss is authoritative; the non-equivalent result and modeling choices remain open |
| `sha256sum` over current authority, source, intake, toolchain, Lake manifest, and pinned mathlib inputs | 0 | current fingerprints are recorded in `statement-blocker.json`; historical intake evidence was not rewritten |
| `python3 -B Stage1_Instances/THM-M-0830/check_intake.py` | 1 | the historical intake checker freezes pre-integration authority state `[ ]`; current execution authority records intake `[_]`, so this phase records rather than rewrites that evidence |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean and Lake agree with the pinned environment above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree agree with the fingerprint; the package worktree is clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0830/IntakeProbe.lean` | 0 | all six adjacent APIs elaborated; complete stdout SHA-256 `7f8302396e027e3c9077952def8d61138e3ff7bb1aadec85485a62e8662b71a9`; no canonical target was declared |
| bounded exact-topic search in repository-local and pinned-mathlib Lean sources | 1 | expected no-match result; discovery only, not an anchor audit |
| prohibited Lean construct scan over the owned path | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, axiom, bodyless declaration, opaque declaration, or unsafe declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0830/statement-blocker.json >/dev/null` | 0 | structured blocker is valid JSON |
| `program=$(jq -r '.validation_invariant_program' Stage1_Instances/THM-M-0830/statement-blocker.json) && jq -e "$program" Stage1_Instances/THM-M-0830/statement-blocker.json >/dev/null` | 0 | identity, blocked open state, null target/imports, unchanged vector, four undefined mutations, false completion flags, exact two-file change scope, and absent self-test agree; the program is preserved in `validation_invariant_program` |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-0830/statement-blocker.json` and the same command for `statement-blocker.md` | 1 each (expected new-file difference) | no whitespace diagnostics; exit 1 records only that each untracked file differs from `/dev/null` |
| `git diff --check -- Stage1_Instances/THM-M-0830` | 0 | no tracked whitespace diagnostics; the preceding no-index commands cover the untracked blocker files |
| `test ! -e .stage1-worker-selftest.json` | 0 | the self-test manifest is absent because the exact-statement deliverable did not pass |

## Retry Condition

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must
preserve and hash a lawful immutable primary or approved authoritative source, select and
independently approve one exact proposition, and transcribe every incorporated definition, ordered
binder, hypothesis, conclusion, proof boundary, correction, erratum, and boundary case. They must
freeze the network and capacity representation, push-relabel variant, execution and scheduling
semantics, output relation, complexity model, and source-to-Lean mapping.

A fresh statement worker can then encode precisely that source-selected claim, minimize pinned
imports, serialize and hash its elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This is a blocked-attempt record, not completion of the statement node or any downstream node. The
root remains `[H1, M4, R4]`, with `audit_complete: false` and `theorem_complete: false`; no debt
change is proposed. Because the assigned phase is not genuinely self-tested to its completion gate,
no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or master acceptance is claimed.
