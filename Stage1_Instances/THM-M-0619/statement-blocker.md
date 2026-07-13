# Exact-statement gate: blocked

Item: `S56-M-0619-STATEMENT`

Theorem: `THM-M-0619`

Base revision: `0f70149d61a952d44f907f4662a143372bcb4c44` (tree
`35328e4f56f47446a4e1dfdbe361a1b70a4b18a7`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0619-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. The intake receipt declares `accepted: false`, is not
content-addressed, and has no accepted receipt ID. It deliberately leaves the canonical human
statement, Lean module and expression, elaborated-expression hash, and target environment
fingerprint null.

Independently, the exact Lean 4 target cannot be selected truthfully from the received source
record. The catalog supplies only the Bolzano-Weierstrass name, the Bernard Bolzano/Karl
Weierstrass attribution, the year 1817, and the gloss `紧度量空间序列有收敛子列` (every sequence
in a compact metric space has a convergent subsequence). It supplies no cited edition, theorem or
page, formula, incorporated definitions, ordered binders, proof passage, translation record,
errata disposition, or independent review. Stage0 explicitly leaves precise definitions and
premises, equivalent formulations, axioms, and machine artifacts open.

Those omissions leave proposition-changing choices. In particular, no admitted source selects a
compact metric carrier versus a sequence contained in a compact subset of an ambient metric
space; `MetricSpace` versus `PseudoMetricSpace`; universes and natural-number indexing; a strictly
increasing natural selector versus another subsequence representation; the exact convergence
expression; explicit membership of the limit in a compact subset; binder order; or empty-carrier,
empty-set, and other boundary conventions.

The intake records this conventional carrier formulation only as a resolution candidate:

```text
for every type X with MetricSpace X and CompactSpace X and every x : Nat -> X, there exist
a : X and phi : Nat -> Nat such that StrictMono phi and x composed with phi tends to a.
```

Selecting that candidate now would turn an unapproved interpretation into the canonical source
statement. Selecting the compact-subset form would instead add a set, term-membership hypotheses,
and limit membership. Replacing the metric condition with the broader first-countable topological
interface exposed by mathlib would also broaden the received wording. None of these is a harmless
pretty-printing choice, and no checked source relationship has been approved.

Rev-5.6 sections 5 and 5.1 make statement ambiguity, an unresolved canonical expression, and a
missing expression fingerprint hard blockers. There is consequently no honest target whose direct
imports can be certified minimal. Checked alternate transports and the removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutation suites are undefined, not passed.
The lifecycle remains `planned`, and the root vector remains `[H-unclassified, M3, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with its single discovery import
`Mathlib.Topology.Sequences`. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, it authenticates these interfaces:

```text
CompactSpace.tendsto_subseq :
  [TopologicalSpace X] -> [FirstCountableTopology X] -> [CompactSpace X] ->
  (x : Nat -> X) -> exists a phi, StrictMono phi and Tendsto (x composed with phi) atTop (nhds a)

IsCompact.tendsto_subseq :
  IsCompact s -> (forall n, x n in s) ->
  exists a in s, exists phi, StrictMono phi and Tendsto (x composed with phi) atTop (nhds a)
```

The probe also checks `SeqCompactSpace.tendsto_subseq`, `isCompact_iff_isSeqCompact`, and
`compactSpace_iff_seqCompactSpace`. The carrier and subset declarations report exactly `propext`,
`Classical.choice`, and `Quot.sound`; the sequential-compactness extraction reports `propext` and
`Quot.sound`. The complete probe output is 1,414 bytes with SHA-256
`d93c9a2c064586f9f08ce2b41e4388ceef9271a818a8b0eddd2483bb777fe38f`.

This is real pinned API evidence only. The first declaration is broader than a metric-space target,
the second is a different compact-subset proposition, and the supporting equivalences are bridge
candidates. The probe declares no canonical target, source transport, statement mutation, or new
proof body. Its import therefore cannot be certified as the minimal import for an absent target.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symbolic link was used read-only. No `lake update`, `lake build`,
dependency clone or fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0619` | 0 | rank 1313; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` link was untracked; base revision and tree appear above |
| source record, Stage0, manifest, blueprint, intake dossier, dependency, and source-boundary inspection | 0 | the compact-metric sequence family is identified, but proposition-changing choices and the canonical target remain null |
| `sha256sum` over authority, source, toolchain, lock, intake, and pinned-candidate inputs | 0 | exact fingerprints are recorded in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean --version`; `lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package status | 0 | pinned mathlib revision and tree recorded above; package source worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0619/IntakeProbe.lean` | 0 | five direct or supporting interfaces elaborated; axiom reports and output fingerprint appear above |
| bounded exact-topic `rg` over the pinned sequence modules and target probe | 0 | the five named declarations were located; no source-identical root mapping was inferred; output SHA-256 `afb3dedd6580cfd9a61e58c1f48621d3c95a51cd5fbe8eb4c69faa4d3ad13782` |
| `python3 -B Stage1_Instances/THM-M-0619/check_intake.py` | 1 | historical intake replay stops because it froze the intake row as `[ ]`, attempt 0, while integration now records `[_]`, attempt 1; intake evidence was not rewritten |
| `python3 -m json.tool Stage1_Instances/THM-M-0619/statement-blocker.json` plus scoped blocker invariants | 0 | structured blocker parses; identity, dependency, null target/imports, undefined mutations, unchanged vector, false completion flags, exact two-file change scope, and absent self-test agree |
| prohibited-declaration scan over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration; diagnostic `#print axioms` commands are permitted |
| scoped `git diff --check` and per-new-file no-index checks | 0 aggregate | no whitespace diagnostics; raw no-index exit 1 is only the expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | the worker self-test manifest is intentionally absent because the exact-statement deliverable did not pass |

The intake checker is historical intake evidence bound to the earlier authority row and closed
nine-file inventory. Integration later advanced only the provisional intake cursor. Rewriting the
checker, intake dossier, receipt, target-local task DAG, generated blueprint, or authoritative DAG
would not resolve the missing source proposition and is outside this phase.

## Retry Condition And Status Boundary

The integration lane must master-accept the intake dependency before accepting a future statement
transition. Accountable reviewers must preserve and hash an immutable primary or authoritative
source, transcribe and independently approve one exact proposition, and map every incorporated
definition, ordered binder, hypothesis, conclusion, proof boundary, translation, correction,
erratum, attribution, and boundary case. They must specifically decide carrier versus compact
subset, metric structure, universe, index, selector, convergence, limit membership, binder order,
and the boundary with `THM-M-0264`.

A later statement worker can then encode precisely that approved claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, node-specific receipt, worker `[_]`,
master acceptance, statement fingerprint, mutation certificate, or proof credit is claimed.
