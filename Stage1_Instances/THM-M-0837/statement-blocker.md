# THM-M-0837 rev-5.6 statement blocker

## Decision

`S56-M-0837-STATEMENT` remains `[ ]`. Its prerequisite `S56-M-0837-INTAKE` is only provisional
worker state `[_]`, not master-accepted state `[x]`. The intake receipt is explicitly unaccepted,
non-content-addressed, and has no accepted receipt ID. Rev-5.6 section 10.2 permits this
dependency-ordered blocker attempt, but it does not permit an accepted statement transition before
the predecessor passes.

Independently and decisively, the exact-source-statement gate fails. The complete target-bearing
catalog record is only `Robertson-Sanders-Seymour-Thomas证明`, Robertson and coauthors, 1997, and
the gloss `四色定理的新证明` ("a new proof of the Four-Colour Theorem"). It supplies no citation,
definitions, ordered binders, hypotheses, exact conclusion, proof or computation boundary,
correction, erratum, formal declaration, or independent reviewer. Its `已验证` label is untrusted
inventory metadata under rev-5.6.

The label identifies a proof family rather than one stable proposition. The inspected discovery
sources expose materially different possible roots:

- the ordinary Four-Colour Theorem conclusion;
- that conclusion coupled to required RSST proof and computation provenance;
- the minimal-counterexample reduction with the reducibility and unavoidability clauses;
- correctness and completeness of the 633-configuration and 32-rule computational corpus;
- the total-correctness and quadratic-complexity theorem for the colouring algorithm; or
- an exact conjunction and composition of some or all of those claims.

Those roots have different domains, conclusions, proof bodies, computation and trust boundaries,
and ownership relationships. Selecting the ordinary theorem alone would discard the RSST
proof-route identity and silently duplicate `THM-M-0833`. Borrowing the Appel-Haken computation
from `THM-M-0836` or Gonthier's formal proof from `THM-M-0838` would also substitute provenance.

The repository has not frozen finite graph versus map or plane-embedding representations; loops,
parallel edges, faces, connectedness, triangulation, or planarity; minimal counterexamples and
internal 6-connectivity; configurations, rings, appearance, reducibility, discharging, charges,
rules, and the exact corpora; program, data, certificate, compiler, runtime, and hardware trust;
algorithm input, output, recursion, reconstruction, and cost model; or the ordered binders,
hypotheses, conclusion, transports, and degenerate cases. Choosing any familiar formulation would
therefore invent, broaden, narrow, or substitute proposition-changing mathematics.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing expression
fingerprint hard blockers. The intake correctly leaves the canonical human statement, Lean module
and expression, minimal imports, and expression and environment fingerprints null at
`[H5, M4, R4]`. Without a canonical target, checked transports and the required removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations are undefined, not passed. No
`Statement.lean`, theorem declaration, proof body, assumed planarity interface, axiom, placeholder,
weakened special case, or broadened theorem was introduced.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` re-elaborates in the pinned environment with its one
direct import, `Mathlib.Combinatorics.SimpleGraph.Coloring`. Its eight checks authenticate adjacent
simple-graph colouring interfaces only. The module itself lists planar graphs as future work. A
bounded search over repository-local and pinned-mathlib Lean found only unrelated uses of
"reducible," planar-vector-field names, and affine coplanarity; it identified no Four-Colour,
RSST, good-configuration, internal-6-connectivity, or `SimpleGraph` planarity declaration.

The probe's successful elaboration has stdout SHA-256
`d1603a5b562207c41f04798f19bc0fc69bd1b2aab5366567bb811ccf55405d9e` and empty stderr. It states
no target and owns no proof body. Its import therefore cannot be certified minimal for an absent
canonical target and supplies no statement or proof credit. The search is bounded discovery
evidence, not the downstream anchor audit or a claim of global absence.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided canonical
`Formalizations/Lean/.lake` symlink was used read-only. No `lake update`, `lake build`, dependency
clone or fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran from the isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0837` | 0 | rank 1394; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base `db4b8793e70ce8af74c9c9490acfa50aa3684d5e`, tree `6434a20532ae7c523ad293e67a6228ab384bfb8a` |
| catalog, Stage0, blueprint, skill, manifest, and complete intake-dossier inspection | 0 | confirmed the sparse proof-family label, null canonical target and fingerprints, candidate roots, computation boundary, and neighbor exclusions |
| authority, source, intake, toolchain, lockfile, probe, and pinned-mathlib SHA-256 checks | 0 | exact current fingerprints are recorded in `statement-blocker.json` |
| `python3 -B Stage1_Instances/THM-M-0837/check_intake.py` | 1 | historical intake checker freezes authority state `[ ]` with attempt 0 while the integrated DAG records provisional `[_]` with attempt 1; it was preserved rather than rewritten |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions agree with the recorded environment |
| pinned mathlib `git rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree agree; dependency worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0837/IntakeProbe.lean` | 0 | eight adjacent colouring APIs elaborated; stdout SHA-256 `d1603a5b...05d9e`; no target or proof body |
| bounded Four-Colour, RSST, configuration, reducibility, discharging, and planarity declaration searches | 0 | only unrelated text matched; no exact target or `SimpleGraph` planarity declaration identified; discovery only |
| prohibited Lean construct scan over the owned path | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |

The historical intake checker freezes intake-time authority. Integration advanced the intake cursor,
so its failure is recorded rather than rewriting historical evidence to manufacture a passing
statement attempt.

## Retry Condition

The integration lane must first master-accept refreshed intake evidence. Accountable independent
source, graph-theory, formal, computation, and neighbor-scope reviewers must preserve and hash a
lawful immutable authoritative source; select the generic theorem, an RSST-provenance package, the
source clause suite, a computation-correctness package, the algorithm theorem, or an exact
conjunction; reconcile ownership with `THM-M-0833`, `THM-M-0836`, and `THM-M-0838`; and approve
every incorporated graph, planarity, configuration, discharging, computation, trust, algorithm,
binder, hypothesis, conclusion, transport, and boundary choice.

A fresh statement worker may then encode only that reviewed claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and execute all four required mutation classes.

This is a truthful blocked statement attempt, not completion of this node or any downstream node.
Lifecycle remains `planned`; the item remains `[ ]`; the root remains `[H5, M4, R4]`;
`audit_complete: false` and `theorem_complete: false`; no debt-vector change is proposed. Because
the exact-statement deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt,
worker `[_]`, proof credit, or master acceptance is claimed.
