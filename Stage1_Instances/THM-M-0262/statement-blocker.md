# Exact-statement gate: blocked

Item: `S56-M-0262-STATEMENT`

Theorem: `THM-M-0262`

Base revision: `bd81d4853a030765585ef6fed4310484ceb1e458` (tree
`fb92fc7476bff9a2ce8c20f1d7be34c6655ca6b4`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
That record gives only the family label "Sullivan theorem," Dennis Sullivan, the year 1985, and
the gloss "classification of rational-function dynamics." It gives no cited proposition, theorem
locator, classified object, equivalence relation or complete list of classes, ordered binders,
hypotheses, conclusion, proof boundary, correction history, or boundary cases. Stage0 explicitly
leaves the precise definitions and premises, proof route, equivalent forms, axiom profile, formal
status, and artifact links open. The catalog's verified label is untrusted metadata under rev-5.6.

Materially different familiar results fit some of those clues: stability and bifurcation results,
quasiconformal deformation or rigidity statements, classifications of periodic Fatou components,
and eventual periodicity of Fatou components. The repository selects none of them. In particular,
it separately schedules `THM-M-1434`, "Sullivan no-wandering-domain theorem," with the explicit
claim "rational functions have no wandering domains." Selecting that result here would collide
with a separate root and substitute missing mathematics rather than elaborate `THM-M-0262`.

The repository also does not fix the rational-map representation, total self-map model at poles
and infinity, degree or nonconstancy condition, Julia/Fatou-set and component conventions,
conjugacy or equivalence notion, invariants or classes, exhaustiveness or uniqueness conclusion,
or exceptional and degenerate cases. Each choice changes the proposition. Consequently the intake
correctly leaves the canonical statement, binders, hypotheses, conclusion, Lean module and
expression, target expression hash, and canonical-target environment fingerprint null at
`[H5, M4, R4]`.

Without a canonical expression, no import set can be certified minimal, no alternate encoding can
receive a checked transport, and the required removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations are undefined rather than passed. No
`Statement.lean`, axiom, placeholder, assumed classification predicate, weakened special case, or
broadened theorem was introduced.

The intake prerequisite has provisional worker state `[_]`, not master-accepted state `[x]`. Its
receipt declares `accepted: false` and has no accepted receipt ID. This allows a dependency-ordered
attempt, but master acceptance remains independently necessary before a future statement
transition can be accepted. The first substantive failure here is the missing exact source
proposition and its separation from `THM-M-1434`.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` re-elaborates in the pinned environment. Its six
direct imports expose eleven adjacent rational-function, complex, meromorphic, compactification,
component, iteration, and periodic-point interfaces. All checks pass. The probe defines neither a
total rational self-map of a selected Riemann-sphere model nor a classification predicate or
Sullivan proposition. Its successful elaboration therefore receives no statement,
minimal-import, anchor, or proof credit.

A bounded case-insensitive search in repo-local Lean and pinned mathlib found no target-specific
declaration under Sullivan, wandering-domain, rational-dynamics, Fatou-component, or
quasiconformal-deformation terms. The only repo-local match was the probe disclaimer. This is
narrow discovery evidence, not the downstream immutable anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The automation-provided
`Formalizations/Lean/.lake` link to canonical pinned artifacts was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was run.

## Validation Evidence

Commands ran in this worker clone on 2026-07-13 (`Asia/Shanghai`), from the repository root unless
a different working directory is shown.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0262` | 0 | rank 1270; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` before editing | 0 | only the automation-provided untracked `.lake` link existed; the base revision and tree are recorded above |
| `sha256sum` over authority, source, intake, probe, toolchain, manifest, and pinned import sources | 0 | hashes agree with `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, target `x86_64-unknown-linux-gnu`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `cd Formalizations/Lean && lake --version` | 0 | Lake `5.0.0-src+98dc76e`, Lean 4.29.0 |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package status | 0 | pinned revision and tree agree with the fingerprint; package worktree is clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0262/IntakeProbe.lean` | 0 | eleven adjacent pinned APIs elaborated; no canonical target or proof body was declared; complete output SHA-256 `416ae386be218d8d2bfb2725fd6c9a8407d65d4352875bd90921d08d4b931e27` |
| bounded repo-local and pinned-mathlib Lean `rg` searches for the target terms | 0 then 1 | the repo-local search matched only the probe disclaimer; the pinned-mathlib search had the expected no-match exit; discovery only, not an anchor audit |
| `python3 -B Stage1_Instances/THM-M-0262/check_intake.py` | 1 | historical intake checker stops at line 128 because it freezes intake authority state `[ ]` while the integrated DAG records provisional `[_]`; this statement phase records rather than rewrites historical evidence |
| prohibited Lean declaration scan over the owned path | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, axiom, bodyless declaration, or unsafe declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0262/statement-blocker.json` | 0 | the finalized structured blocker parsed as valid JSON |
| scoped statement-blocker invariant assertions | 0 | IDs, open state, null target and imports, unchanged vector, four undefined mutations, false completion flags, exact two-file change scope, and absent self-test agree |
| `git diff --check -- Stage1_Instances/THM-M-0262` plus `git diff --no-index --check -- /dev/null <each blocker artifact>` | 0 for the scoped check; expected added-file status 1 with empty output for each no-index check | no whitespace diagnostics in either blocker artifact |
| `test ! -e .stage1-worker-selftest.json` | 0 | the self-test manifest is absent because the exact-statement deliverable did not pass |

The historical intake checker is frozen to its original authority state and nine-file intake
inventory. Integration subsequently promoted the intake worker evidence to provisional `[_]`, so
the checker already fails before its inventory assertion. Adding these two statement artifacts also
makes that intake-only inventory historical. This run records the limitation instead of rewriting
the intake checker, intake receipt, instance, task DAG, generated blueprint, or authoritative DAG
to manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must then
lawfully preserve and hash one complete primary or authoritative source edition, select and
transcribe one exact truth-valued proposition with pinpoint locators and every incorporated
definition, reconcile corrections and errata, independently approve the source crosswalk, and
explicitly resolve its relationship to `THM-M-1434`. They must freeze the rational-map and sphere
models, degree restrictions, iterates at poles and infinity, classified objects, relation or
invariants, complete conclusion, ordered binders, hypotheses, foundation profile, and every
exceptional and degenerate case.

A later statement worker can then encode that same claim with real Lean definitions, minimize its
pinned imports, serialize and hash the elaborated expression and environment, compile every
credited transport, and run all four mutation classes.

This is a blocked-attempt record, not completion of the statement node or any downstream node. The
root remains `[H5, M4, R4]`, with `audit_complete: false` and `theorem_complete: false`; no debt
change is proposed. Because the assigned phase is not genuinely self-tested to its completion gate,
no `.stage1-worker-selftest.json`, node receipt, worker `[_]`, or master acceptance is claimed.
