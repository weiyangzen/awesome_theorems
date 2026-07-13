# Exact-statement gate: blocked

Item: `S56-M-0894-STATEMENT`

Theorem: `THM-M-0894`

Base revision: `46a0f2a3ea74765a0467c489264b838ffbb70675` (tree
`7b1b5269d7da840fd086da731d6f92903c209c35`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0894-INTAKE` is only provisional worker
state `[_]`, not master-accepted `[x]`. Rev-5.6 section 10.2 permits this later-node blocker attempt
while concurrency is enabled, but master acceptance remains required before any future statement
transition.

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
The complete mathematical wording is the title `距离正则图` (distance-regular graphs) and the gloss
`距离正则图的理论` (the theory of distance-regular graphs). The record also gives only a collective
attribution, the twentieth century, and an untrusted `已验证` label. It cites no source and supplies
no definition, truth-valued proposition, ordered binder, hypothesis, conclusion, proof boundary,
correction, erratum, or formal artifact.

Distance-regular graph theory is a field, not one theorem. The repository does not select among:

- a definition or equivalent characterization by constant neighbor counts between distance layers;
- existence or basepoint independence of intersection parameters or an intersection array;
- connectedness, regularity, fixed layer valencies, or parameter recurrences;
- intersection-array feasibility identities, adjacency-algebra or spectral results;
- constructions, existence, nonexistence, uniqueness, or classifications; or
- a diameter or valency bound.

It also does not fix finite versus locally finite graphs, connectedness and nontriviality, natural or
extended distance and diameter, the intersection-count encoding, parameter indexing, binder order,
or empty, disconnected, small-diameter, out-of-range, empty-layer, and endpoint cases. These choices
change the domain, hypotheses, and conclusion. Selecting one familiar result would invent, narrow,
broaden, or substitute the target. It could also silently absorb the separate Hoffman-Singleton,
Bannai-Ito, strongly regular graph, or finite-geometry targets.

The intake identified Brouwer, Cohen, and Neumaier's 1989 book *Distance-Regular Graphs* as an
authoritative subject-reference lead. The repository does not cite it, however, and the intake
admitted only metadata and a publisher description. No exact edition passage, proposition,
incorporated definition chain, proof, correction map, immutable source snapshot, or independent
review selects a root. The book confirms the subject's breadth; it does not repair the missing
statement.

Sections 5 and 5.1 of the rev-5.6 standard make statement ambiguity and a missing elaborated
expression fingerprint hard blockers. Without a canonical proposition, there is no exact Lean
expression for which imports can be certified minimal, no elaborated expression or environment
fingerprint, no credited alternate transport, and no meaningful removed-hypothesis, changed-domain,
changed-binder-scope, or boundary-case mutation. Those mutation classes are undefined, not passed.
No surrogate theorem, weakened special case, axiom, placeholder, broadened interface, or proof body
was added.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with the pinned environment. Its imports expose
graph distance and diameter, finite neighborhoods, regularity, common-neighbor sets, and the related
strongly regular graph parameter API. All eleven interface checks pass. Its two existing-library
axiom reports list only `propext`, `Classical.choice`, and `Quot.sound`.

The probe defines no distance-regular predicate or intersection array, states no canonical target,
selects no source proposition, supplies no checked transport, and has no proof body. Its imports
therefore cannot be certified minimal for an absent expression. In particular,
`Mathlib.Combinatorics.SimpleGraph.StronglyRegular` is a related special-family boundary, not a
generic distance-regular graph theorem.

A bounded pinned-mathlib search found no exact `DistanceRegular`, distance-regular, or
intersection-array/number declaration. The only target-local matches were comments in the
discovery-only probe. This is scoped feasibility evidence, not the downstream immutable anchor audit
or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The complete probe output has SHA-256
`9a167e7242d1f659694e1aaf289f7bfe02f8fe3e1120235255aff5f4e928f825`.

The automation-provided `Formalizations/Lean/.lake` link points to canonical pinned artifacts and
was used read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake`
mutation was run.

## Validation Evidence

Commands ran in this isolated worker clone on 2026-07-13 (Asia/Shanghai), from the repository root
unless a different working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0894` | 0 | rank 1443, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; the base revision and tree are recorded above |
| repository source, Stage0, blueprint, skill, intake dossier, source crosswalk, and scope-map inspection | 0 | only a subject label and gloss are authoritative; the intake deliberately freezes a null canonical claim and target at `[H5, M4, R4]` |
| `git blame -L 6544,6549 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa...`; no later source-statement refinement |
| `sha256sum` over authority, source, intake, probe, toolchain, lockfile, and relevant mathlib inputs | 0 | current fingerprints are recorded in `statement-blocker.json`; historical intake artifacts were not rewritten |
| `python3 -B Stage1_Instances/THM-M-0894/check_intake.py` | 1 | the historical intake checker expects authoritative intake state `[ ]`, attempts 0, while the current DAG records provisional `[_]`, attempts 1; this run records rather than rewrites phase-frozen evidence |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean and Lake agree with the pinned environment above |
| pinned mathlib revision, tree, and package-status checks | 0 | revision and tree agree with the fingerprint; the package worktree is clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0894/IntakeProbe.lean` | 0 | eleven adjacent graph APIs elaborated; no canonical target or proof body was declared |
| bounded repo-local and pinned-mathlib Lean searches | 1 expected no match / 0 comments only | no source-identical distance-regular graph declaration was found |
| prohibited Lean construct scan over the owned path | 1 | expected no-match exit: no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| JSON parse and exact scoped invariant/input-hash check | 0 each | identity, open blocked state, null target and imports, unchanged vector, four undefined mutations, false completion flags, exact two-file scope, current fingerprints, and absent self-test agree |
| tracked and new-file whitespace checks | 0 | no whitespace diagnostics in either blocker artifact |
| `test ! -e .stage1-worker-selftest.json` | 0 | no worker self-test manifest exists because the exact-statement deliverable is blocked |

The intake receipt declares `accepted: false`, is not content-addressed, and has no accepted receipt
ID. Its validator is also intake-specific and freezes the original nine-file inventory. This
statement run does not rewrite that historical receipt, validator, instance manifest, target-local
DAG, generated checklist, or authoritative DAG to manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must first master-accept refreshed intake evidence. Accountable reviewers must
preserve and hash an immutable primary or approved authoritative source, select and independently
approve one exact truth-valued proposition, and map every incorporated definition, binder, premise,
conclusion, proof boundary, correction, and erratum. They must freeze the graph model, distance and
diameter conventions, intersection-count or algebraic encoding, parameter indexing, computation
policy, alternate transports, boundary cases, and neighboring-target ownership.

A fresh statement worker may then encode precisely that source-selected claim, minimize its pinned
imports, serialize and hash its elaborated expression and environment, compile every credited
transport, and run all four required mutation classes.

The first failed gate is exact source-statement identity and scope freeze. The root remains
`[H5, M4, R4]`, with `audit_complete: false` and `theorem_complete: false`; no debt-vector change is
proposed. This is blocked-attempt evidence, not completion of the statement node or any downstream
node. Because the assigned phase is not genuinely self-tested to its completion gate, no
`.stage1-worker-selftest.json` is emitted and no statement receipt, worker `[_]`, or master
acceptance is claimed.
