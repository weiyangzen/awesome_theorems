# THM-M-0263 rev-5.6 statement blocker

## Decision

`S56-M-0263-STATEMENT` remains `[ ]`. Its prerequisite `S56-M-0263-INTAKE` is provisional worker
state `[_]`, not master-accepted state `[x]`; its receipt has `accepted: false`, is not
content-addressed, and has no accepted receipt ID. Rev-5.6 permits provisional preparation of this
blocker, but master closure remains dependency ordered.

Independently and decisively, the exact-source-statement gate fails. The catalog records the title
`实数完备性定理`, the joint Richard Dedekind/Karl Weierstrass attribution, the year 1872, the gloss
`实数集的完备性` (completeness of the set of real numbers), high importance, and an untrusted verified
label. It gives no cited work or passage, formula, incorporated definition, ordered binder,
hypothesis, conclusion, proof boundary, correction history, or reviewer. Stage0 explicitly leaves
the precise definitions and premises, formal system, equivalent forms, axiom policy, machine status,
and artifacts open. The catalog's `已验证` label supplies no source or kernel credit under rev-5.6.

The gloss identifies a theorem family, not one binder-complete proposition. Materially different
roots fit it:

- least-upper-bound completeness for nonempty bounded-above subsets of `Real`;
- the greatest-lower-bound dual;
- Dedekind-cut continuity with a unique real boundary;
- metric or uniform Cauchy completeness of `Real`; and
- monotone-convergence, nested-interval, and related equivalent principles.

These are mathematically related but not definitionally identical, and the repository supplies no
accepted transport selecting one as the root. An inspected source lead, Dedekind's *Continuity and
Irrational Numbers*, Section V theorem IV in Beman's authorized 1901 translation, states a cut
continuity theorem. The catalog does not cite that edition or passage, the joint Weierstrass
attribution remains unmapped, the original edition and correction record are not independently
reviewed, and no accepted bridge identifies it with a modern LUB or Cauchy proposition. Selecting a
familiar form would therefore invent a source bridge or substitute proposition-changing
mathematics.

The unresolved choices continue inside every candidate. An LUB root must fix the subset carrier,
nonemptiness and boundedness hypotheses, `IsLUB` versus a chosen `sSup`, quantifier order,
uniqueness, and the status of the GLB dual. A cut root must fix coverage, disjointness, class
nonemptiness, strict separation, endpoint ownership, production of the separation, and uniqueness.
A metric root must fix sequences versus filters or nets, indexing, the Cauchy predicate, topology
or uniformity, an explicit limit versus a `CompleteSpace` instance, and convergence mode. Empty,
unbounded, singleton, endpoint, and constant-sequence cases are likewise unresolved.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing elaborated
expression fingerprint hard blockers. There is therefore no canonical expression whose imports can
honestly be certified minimal, no credited alternate form for a checked transport, and no canonical
target against which the required removed-hypothesis, changed-domain, changed-binder-scope, and
boundary mutations can run. Those mutations are undefined, not passed. No `Statement.lean`, Lean
declaration, proof body, broadened interface, or substituted special case was added. The root vector
remains `[H1, M3, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with its two direct imports:

- `Mathlib.Data.Real.Archimedean`
- `Mathlib.Topology.UniformSpace.Real`

It checks these pinned candidate interfaces:

- `Real.exists_isLUB` and `Real.exists_isGLB`;
- `Real.isLUB_sSup` and `Real.instConditionallyCompleteLinearOrder`;
- `Real.instCompleteSpace`; and
- `cauchySeq_tendsto_of_complete`.

All six elaborate. The order declarations concern nonempty bounded sets and LUB/GLB witnesses or an
order instance. The metric interfaces instead expose a complete uniform space and convergence of a
Cauchy sequence under a completeness instance. Their binders, structures, premises, and conclusions
are materially different. Representative axiom reports list only `propext`, `Classical.choice`, and
`Quot.sound`, but this is candidate-interface evidence only. The probe deliberately defines no
canonical target, source-to-Lean transport, statement mutation, or proof body, and its two imports
cannot be certified minimal for an absent target.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided canonical `.lake` symlink was
used read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation
was run.

## Validation Record

Commands ran from the isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0263` | 0 | rank 1271; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision `2eea98305d46266f078a50cf0e85853bf6a5e702`, tree `02279a8caa5f31ed8e37e35c8584a336eed9b974` |
| `git blame -L 1894,1899 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| authority, source, intake, probe, toolchain, lockfile, and relevant mathlib `sha256sum` checks | 0 | exact current fingerprints are preserved in `statement-blocker.json`; historical intake hashes were not rewritten |
| `python3 -B Stage1_Instances/THM-M-0263/check_intake.py` | 1 | the historical intake checker expects authoritative intake state `[ ]` with zero attempts, while integration now records provisional `[_]` with one attempt; this run records rather than rewrites stale intake evidence |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| mathlib `git rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree recorded above; package source worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0263/IntakeProbe.lean` | 0 | six distinct candidate APIs and both relevant instances elaborated; five representative axiom reports named the three axioms above; stdout SHA-256 `eebd83c158257addb356e904d089b3bb9b23089416849fef9663a01700f67386`; no target declaration or proof body |
| bounded declaration-name `rg` over repo-local and pinned-mathlib Lean | 0 | probe, pinned declarations, downstream uses, and one legacy inventory string found; no source-identical canonical mapping credited |
| prohibited-declaration `rg` over owned Lean files | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration token; diagnostic `#print axioms` commands are permitted |
| `python3 -m json.tool Stage1_Instances/THM-M-0263/statement-blocker.json` and scoped `jq` assertions | 0 | valid JSON; identity, blocked state, provisional dependency, null target/imports, unchanged vector, four undefined mutations, false completion flags, and exact two-file scope agree |
| exact byte assertions plus tracked and per-new-file `git diff --check` checks | 0; 1 expected difference per new file | no whitespace, missing-newline, carriage-return, or NUL diagnostics; each no-index check emitted an empty diagnostic stream |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The intake checker freezes the intake run's original authority state and nine-file artifact
inventory. It is historical evidence, not a later-phase validator. This run records its stale-state
failure instead of rewriting the intake instance, receipt, checker, target-local task DAG, generated
blueprint, or authoritative execution DAG to manufacture agreement.

## Retry Condition

The integration lane must first master-accept refreshed intake evidence. Accountable reviewers must
then preserve and hash one immutable primary or approved authoritative source, select and
independently approve one exact real-completeness proposition, map both catalog attributions and
every incorporated definition, ordered binder, hypothesis, conclusion, proof boundary, correction,
erratum, and boundary case, and approve checked relationships to any alternate formulation.

A fresh statement worker may then encode only that approved claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport, and
execute all four mutation classes.

This is a truthful blocked statement attempt, not completion of this node or any downstream node.
Lifecycle remains `planned`; `audit_complete: false` and `theorem_complete: false`; no debt-vector
change is proposed. Because the exact-statement deliverable did not pass, no
`.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof credit, or master acceptance
is claimed.
