# Exact-statement gate: blocked

Item: `S56-M-1587-STATEMENT`

Theorem: `THM-M-1587`

Base revision: `8a13381618b241479a4786ca67704af7322f77aa` (tree
`0cc75f807f4c75d2a0aa8a72062e025083bd18ad`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1587-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. Rev-5.6 permits this dependency-ordered assessment,
but the intake receipt is unsigned and non-content-addressed, declares `accepted: false`, and has
no accepted receipt ID. Master acceptance remains necessary before any eventual accepted statement
transition.

Independently, the exact-statement gate cannot pass. The repository record supplies only the title
`Singleton界`, Richard Singleton, 1964, and the gloss `MDS码的界` (a bound for MDS codes). It gives
no formula, source locator, alphabet, code object, length, distance, dimension, nonemptiness,
parameter range, ordered binders, hypotheses, conclusion, proof boundary, correction history, or
boundary conventions. The parallel Stage0-only computer-science row says `MDS码的Singleton界`, but
it neither selects a proposition nor belongs to the rev-5.6 target set. The catalog's `已验证`
label is untrusted metadata.

The intake identifies the exact bibliography of Richard C. Singleton's 1964 paper *Maximum
distance q-nary codes*, but only bibliographic metadata was admitted. The paper text, an exact
theorem or equation locator, incorporated definitions, assumptions, proof boundary, corrections,
errata, and independent review were not inspected or credited. A modern secondary record confirms
that the following are related but materially different roots:

- an unrestricted q-ary code-size inequality, commonly written `|C| <= q^(n-d+1)`;
- its linear finite-field specialization, commonly written `k <= n-d+1` or `d <= n-k+1`;
- a puncturing-injection theorem from which one of those inequalities follows; and
- the definition or characterization of an MDS code by equality in a selected linear inequality.

The gloss does not decide whether "MDS" identifies the equality case, a restriction of the bound,
or a different existence or length claim. The variants also differ on arbitrary versus linear
codes, coordinate and alphabet carriers, minimum-distance conventions, natural subtraction,
cardinality arithmetic, puncturing maps, and whether empty, singleton, zero-length, zero-distance,
or overlarge-distance cases are included. Selecting the familiar general inequality, a linear
special case, or an equality definition from convention would invent, narrow, broaden, or
substitute proposition-changing mathematics.

Sections 5 and 5.1 of the rev-5.6 standard make statement ambiguity and a missing expression
fingerprint hard blockers. There is therefore no honest canonical Lean expression for which
minimal imports, a serialized elaborated-expression hash, checked alternate transports, or the
required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations can
be certified. Those mutation checks are undefined, not passed. The root vector remains
`[H1, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates eight adjacent interfaces from the two direct imports
`Mathlib.Data.Fintype.BigOperators` and `Mathlib.InformationTheory.Hamming`: Hamming distance and
its zero, coordinate-count, and coordinatewise-map facts, finite function-space cardinality,
injective cardinality, cardinality transport, and finite-domain transport. Its deterministic
output is 1,465 bytes with SHA-256
`a3547fa913bcfd9addfd9938fbbbd94e3d322c55eea4efa8948de94a6a7dc814`.

This is real substrate validation, but the probe defines no code, minimum-distance function,
puncturing map, Singleton inequality, MDS predicate, canonical target, checked transport, or proof
body. Its imports cannot be certified minimal for an absent target and receive no statement or
proof credit. A bounded exact-topic search found no fixed-length block-code, minimum-distance,
Singleton-bound, or MDS-code declaration in pinned mathlib or repository-local Lean. The q-ary
entropy hits and variable-length uniquely-decodable-code APIs use different models. This is
discovery-only feasibility evidence, not the downstream anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No update, build, clone, fetch, or other
dependency mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1587` | 0 | rank 1209; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| scoped source, Stage0, manifest, blueprint, execution-DAG, skill, and intake-dossier inspection | 0 | confirmed the family-only gloss, null canonical target, unrestricted/linear/puncturing/equality variants, duplicate boundary, and unresolved cases |
| `git blame -L 11693,11698 -- Docs/researches/math_theorems.md`; source-block hashes | 0 | all six uncited catalog fields originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`; exact current source-block hashes are recorded in `statement-blocker.json` |
| `sha256sum` over current authority, source, intake, probe, toolchain, and pinned-library inputs | 0 | exact current fingerprints are recorded in `statement-blocker.json`; historical intake hashes were not rewritten |
| `python3 -B Stage1_Instances/THM-M-1587/check_intake.py` | 1 | historical replay stops at its stale pre-integration blueprint hash; the checker also freezes the original nine-file intake inventory, so this phase records rather than rewrites it |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| pinned mathlib revision, tree, and package-status checks | 0 | revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-1587/IntakeProbe.lean` | 0 | eight adjacent APIs elaborated; output byte count and hash recorded above; no canonical target or proof body |
| bounded Singleton/MDS/block-code search in pinned mathlib and repo-local Lean | 0 | only unrelated q-ary-entropy, variable-length source-code, and prose hits; no exact target declaration located; discovery only |
| prohibited-construct scan over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| structured JSON parse and scoped blocker assertions | 0 | identity, dependency, null target and imports, unchanged vector, four undefined mutations, false completion flags, exact two-file change scope, and absent self-test agree |
| scoped `git diff --check` plus per-new-file no-index checks | 0 aggregate | no whitespace diagnostics; no-index exit 1 is only the expected added-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest absent because the exact-statement deliverable did not pass |

The historical intake checker is bound to earlier authority bytes and its original intake-only
artifact inventory. This statement run does not rewrite the intake checker, receipt, instance,
task DAG, generated blueprint, or authoritative execution DAG to manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must master-accept refreshed intake evidence before accepting a later
statement transition. Accountable reviewers must also lawfully preserve and hash one immutable
primary or authoritative source, select and independently approve one exact Singleton-bound
proposition, reconcile `THM-C-0371`, and transcribe every incorporated definition, ordered binder,
hypothesis, conclusion, proof boundary, correction, erratum, arithmetic convention, and boundary
case. They must explicitly fix the alphabet and code model, length and distance, linear dimension
if applicable, puncturing map, cardinal arithmetic, subtraction and power conventions, quantifier
order, equality role, and all degenerate cases.

A fresh statement run can then encode precisely that approved claim, minimize pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement item or any
downstream item. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
