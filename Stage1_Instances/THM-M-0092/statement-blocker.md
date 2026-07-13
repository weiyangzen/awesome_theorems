# Exact-statement gate: blocked

Item: `S56-M-0092-STATEMENT`

Theorem: `THM-M-0092`

Base revision: `771d5d4800fbd95eaaa343e9bc55ebfdde20b364` (tree
`a98ba0c37e56a7c04256f7d7df305c88e5cbe76e`).

## Decision

The statement item remains `[ ]`. Its prerequisite, `S56-M-0092-INTAKE`, has provisional worker
state `[_]`, not master-accepted state `[x]`. The intake receipt has `accepted: false`, is not
content-addressed, and has no accepted receipt ID. It deliberately leaves the canonical human
statement, Lean expression, expression hash, and canonical-target environment fingerprint null.
The historical intake validator also cannot replay the current authoritative execution state: it
expects the intake item to remain `[ ]`, whereas the integration lane now records provisional
`[_]`. Rev-5.6 section 10.2 permits provisional later-node preparation when concurrency is enabled,
as it is for this assigned worker task, so `[_]` does not by itself prevent this inspection. It does
prevent master closure until the dependency is accepted. This attempt records the mismatch rather
than rewriting the intake evidence.

Independently and decisively, the exact-statement gate cannot pass from the received catalog
record. The record gives only the label "Cartan-Weyl theorem" and the gloss "classification and
representations of semisimple Lie algebras." That wording does not select a unique mathematical
proposition. It may refer to Cartan-Dynkin-Killing classification by root data or Dynkin diagrams,
decomposition into simple factors, Weyl complete reducibility, highest-weight classification, a
Cartan-Weyl-basis result, or a conjunction of algebra-classification and representation results.
These readings have different objects, binders, hypotheses, conclusions, and proof boundaries.
Highest-weight classification is also separately owned by `THM-M-0093`.

The catalog supplies no primary-source edition or proposition locator, incorporated definitions,
scalar field, characteristic or algebraic-closure assumptions, finite-dimensionality assumptions,
semisimplicity encoding, classification data and equivalence relation, representation object and
conclusion, correction history, boundary policy, or independent source approval. The catalog's
`已验证` label is explicitly untrusted under rev-5.6.

The intake inspected immutable secondary encyclopedia revisions for semisimple Lie algebras and a
Cartan-Weyl basis, DOI metadata for Weyl's 1925 representation paper, and bibliography leads in
pinned mathlib. These leads materially disagree about the theorem family and attribution: pinned
mathlib calls the algebra result the Cartan-Dynkin-Killing classification, while the Cartan-Weyl
basis lead points to Weyl's 1925 work rather than the catalog's unexplained 1913 date. No complete
primary or authoritative theorem passage, definition chain, proof boundary, translation or errata
record, or independent review was admitted. The leads remain `H1`, not an approved source root.

Choosing the familiar complex semisimple classification, complete reducibility alone, or a
combined classification from mathematical memory would therefore invent, narrow, or substitute
the target. Rev-5.6 sections 5 and 5.1 make statement ambiguity and a missing elaborated-expression
fingerprint hard blockers. There is no honest canonical expression whose imports can be certified
minimal, no approved alternate encoding for a checked transport, and no meaningful
removed-hypothesis, changed-domain, changed-binder-scope, or boundary-case mutation suite. Those
mutation results are undefined, not passed. Lifecycle remains `planned`; the debt vector remains
`[H1, M3, R4]`; no statement receipt or worker completion claim is emitted.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` was re-elaborated in the pinned environment. Its
five direct imports expose adjacent semisimple, Cartan-subalgebra, root-system, classical-algebra,
Cartan-matrix, and irreducibility APIs. It checks nine declarations, including
`LieAlgebra.IsSemisimple`, `LieAlgebra.IsKilling.rootSystem`, `LieAlgebra.SpecialLinear.sl`, and
`LieModule.IsIrreducible`.

The probe does not declare a classification theorem, a representation-classification theorem, a
checked source transport, or a proof body. A bounded exact-topic search found only mathlib
documentation describing Cartan-Killing or Cartan-Dynkin-Killing classification and a legacy file
for the unrelated infinite-dimensional Kac-Moody target that explicitly denies classification
proof credit. Therefore the probe's imports are only a statement-feasibility boundary and cannot
be called minimal imports for an absent target. The complete probe stdout has SHA-256
`dbb3d4c9739dc713d56d3c05fdc1882448a98811feff633e02b43ea11afe50f6`.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No update, build, dependency clone, fetch,
or other `.lake` mutation was performed.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0092` | 0 | rank 1109; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `pwd`; `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | worker clone confirmed; only the automation-provided `.lake` symlink was untracked; base identifiers appear above |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short`; `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | package worktree clean; pinned mathlib revision and tree recorded above |
| `sha256sum` on the target manifest, blueprint, execution DAG, skill, source records, pins, intake artifacts, and nine inspected mathlib source modules | 0 | exact input hashes are recorded in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0092/IntakeProbe.lean` | 0 | nine adjacent APIs elaborated; stdout SHA-256 recorded above; no canonical target or proof body declared |
| bounded case-insensitive classification-name search in pinned mathlib, repo-local Lean, and the owned dossier | 0 | documentation/context matches and one unrelated Kac-Moody noncompletion disclaimer only; no exact broad Cartan-Weyl classification-and-representation declaration found |
| `python3 -B Stage1_Instances/THM-M-0092/check_intake.py` | 1 | historical intake replay stops because it freezes intake authority state `[ ]`, while the current authoritative DAG records provisional `[_]` |

The structured blocker was also parsed and checked for the exact item identity, null target and
fingerprints, unchanged debt vector, four unavailable mutation classes, false completion flags,
and blocked status with the recorded `jq -e` predicate. A prohibited Lean construct scan found no
`sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration. Scoped and
new-file whitespace checks passed. Exact commands and results are duplicated in
`statement-blocker.json` for machine inspection. The Markdown groups some related invocations for
readability; the structured artifact preserves their full argument lists.

## Retry Condition And Status Boundary

Accountable reviewers must lawfully preserve and hash one complete primary or authoritative source
edition, select and independently approve one exact proposition, and transcribe every incorporated
definition, ordered binder, hypothesis, conclusion, proof boundary, attribution, translation,
correction, and boundary case. They must resolve algebra versus group scope; scalar field and finite
dimensionality; semisimplicity encoding; classification data, exhaustiveness, uniqueness, and
equivalence; the representation object and conclusion; the logical relation between the algebra
and representation clauses; and zero, trivial, repeated-factor, disconnected-diagram, and other
boundary cases.

A fresh statement run may then encode exactly that source model, minimize pinned imports, serialize
and hash the elaborated expression and environment, compile every credited transport, and execute
all four required mutation classes. The integration lane must also revalidate and master-accept the
intake dependency before accepting that transition.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. `audit_complete: false` and `theorem_complete: false`; no debt-vector change is
proposed. Because the exact-statement deliverable did not pass, no
`.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or master acceptance is claimed.
