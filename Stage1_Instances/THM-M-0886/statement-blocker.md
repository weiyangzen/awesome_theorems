# Exact-statement gate: blocked

Item: `S56-M-0886-STATEMENT`

Theorem: `THM-M-0886`

Base revision: `5c38e670073bc890a78e61556f36d2c6b35d257d` (tree
`95a189ecdfe548d9cff4faaebc111079babceb92`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0886-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. Rev-5.6 section 10.2 permits this
dependency-ordered investigation, but the intake receipt declares `accepted: false`, is not
content-addressed, contains no accepted receipt ID, and requires independent source and formal
review before dependent statement work. Master acceptance remains necessary before a future
statement transition can be accepted.

Independently, the exact-statement gate cannot pass. The repository record supplies only the title
`Marcus-Spielman-Srivastava theorem`, the 2015 attribution, and the gloss `existence of biregular
Ramanujan graphs`. It omits the degree range, graph category, bipartition and degree conventions,
spectral multiplicity convention, infinite-family semantics, every ordered binder, the proof
boundary, corrections, and boundary cases. Its `verified` label is untrusted under rev-5.6.

The intake identifies Marcus, Spielman, and Srivastava, *Interlacing families I: Bipartite
Ramanujan graphs of all degrees*, Annals of Mathematics 182 (2015), Theorem 5.6 on pages 316-317,
as the exact published candidate. Section 2.3 supplies its incorporated biregular and spectral
definitions. That candidate is not an accepted canonical root: the repository does not cite or
adopt it, no complete correction and errata disposition is recorded, and no independent reviewer
has approved the source-to-statement translation or the cross-edition quantifier reading.

Proposition-changing formal choices remain explicitly open:

- whether the ordinary finite graphs in the selected edition are represented by Lean simple
  graphs and whether nonempty parts or connectedness are part of the root;
- how named bipartition sides cover the carrier and how their respective degrees are witnessed;
- how the two trivial adjacency eigenvalues are recognized and removed with algebraic
  multiplicity, especially for repeated trivial eigenvalues or disconnected graphs;
- the exact coercions and natural subtraction in the non-strict Ramanujan bound; and
- whether `infinite sequence` is encoded by strict size growth, unbounded size, pairwise
  nonisomorphism, or another checked equivalent nonrepetition condition.

The source proof repeatedly uses 2-lifts, but that observation alone does not authorize the worker
to replace the published conclusion by a strictly increasing-cardinality family without an
accepted source translation. Conversely, a bare `Nat -> Graph` permits a constant sequence and is
too weak. Selecting either encoding now would manufacture source acceptance rather than elaborate
the exact received target.

Sections 5 and 5.1 make statement ambiguity and a missing expression fingerprint hard blockers.
There is consequently no accepted canonical expression for which minimal imports, checked
alternate transports, or the required removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations can be certified. All four mutation classes are
undefined, not passed. No `Statement.lean`, proof body, weakened special case, broadened theorem,
or circular graph interface was added. The root remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates under the pinned toolchain. Its seven direct imports
expose finite simple graphs, multigraphs, bipartiteness, degrees, real adjacency matrices,
Hermitian eigenvalues, and permutation matrices. All ten interface checks pass, with complete
output SHA-256
`32df9e2c8d621a1d482584389db446453d89d25353d634bf9131b8b6374eb046`.
The probe defines no biregular Ramanujan predicate, source-selected family semantics, canonical
target, checked source transport, or proof body. Its imports therefore cannot be certified minimal
for an absent accepted target and receive no statement or proof credit.

A bounded exact-topic search over pinned mathlib and repository-local Lean found no biregular
Ramanujan or MSS declaration under the recorded search terms. This is discovery-only evidence,
not the downstream immutable anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No dependency update, build, clone, fetch,
or other `.lake` mutation was run.

## Validation Record

Commands ran in this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0886` | 0 | rank 1037; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| scoped catalog, Stage0, manifest, blueprint, skill, guidelines, and intake inspection | 0 | confirmed the sparse catalog claim, exact published candidate, null canonical target, and open source and encoding decisions |
| `sha256sum` over authority, intake, source, probe, toolchain, and pinned mathlib inputs | 0 | exact hashes are recorded in `statement-blocker.json` |
| `python3 -B Stage1_Instances/THM-M-0886/check_intake.py` | 1 | historical intake replay rejects authoritative intake state `[_]` because its worker-time validator froze `[ ]`; the provisional receipt also freezes older authority hashes and its original nine-file inventory, so this phase records rather than rewrites it |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0886/IntakeProbe.lean` | 0 | ten adjacent graph, degree, bipartite, adjacency, Hermitian-spectrum, multigraph, and permutation-matrix signatures elaborated; output SHA-256 recorded above; no canonical target or proof body |
| bounded exact-topic search in pinned mathlib and repo-local Lean | 1 | expected no-match result; discovery-only evidence |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |

Final JSON, invariant, whitespace, and absent-self-test checks are recorded in the structured
blocker beside this report.

## Retry Condition And Status Boundary

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must
preserve and hash a lawful immutable edition of the MSS paper, adopt and independently approve
Theorem 5.6 with every incorporated definition, settle the published/arXiv binder wording,
complete the proof-boundary and correction/errata review, and freeze the graph, bipartition,
degree, spectral-multiplicity, Ramanujan-bound, sequence, and boundary conventions.

A fresh statement worker can then encode precisely that reviewed claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
