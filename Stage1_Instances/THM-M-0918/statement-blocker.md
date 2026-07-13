# Exact-statement gate: blocked

Item: `S56-M-0918-STATEMENT`

Theorem: `THM-M-0918`

Base revision: `d66b6e80968b53d5b99774584721ae8976f303a5` (tree
`aaa82721074fccea81033a9a18d21652af89f8e4`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0918-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. Its receipt is non-content-addressed, declares
`accepted: false`, and supplies no accepted receipt ID. Rev-5.6 section 10.2 permits this
dependency-ordered investigation, but master acceptance remains necessary before any eventual
statement transition can be accepted.

Independently and decisively, the exact-statement gate fails. The authoritative catalog supplies
only the title "Rogers-Ramanujan identities," the Rogers/Ramanujan attribution, the year 1894, and
the gloss "an identity of the partition function." It supplies no formula, citation, definition,
ordered binder, hypothesis, conclusion, proof boundary, correction history, or boundary policy.
Its `verified` label is untrusted metadata under rev-5.6.

The conventional name denotes two identities, while the singular gloss does not select the first
identity, the second identity, their conjunction, or an explicitly composed two-root package. The
modern DLMF leads inspected at intake expose further proposition-changing choices:

- analytic complex q-series/product identities under a convergence domain;
- formal-power-series identities over a selected coefficient ring; or
- restricted-partition count equalities for every natural number.

These are related but not definitionally interchangeable claims. The analytic form requires an
exact `q` domain, denominator and convergence facts, and infinite sum/product conventions. The
formal form requires a coefficient ring and inverse-factor semantics. The combinatorial form
requires an exact partition representation, adjacent-difference predicate, residue predicate,
minimum-part convention, and cardinality codomain. The repository also does not decide whether
transports among these encodings are part of the root.

DLMF 17.2.49-50 and 26.10.13-14 are strong modern statement leads, and the Rogers paper identified
by DOI `10.1112/plms/s1-25.1.318` is a historical lead. None is a lawfully admitted, independently
reviewed source selection for this repository target. The original-paper metadata also conflicts
with the catalog date. Selecting one familiar formula or convenient Lean encoding would invent,
narrow, or substitute mathematics rather than elaborate the exact received target.

Rev-5.6 sections 5 and 5.1 make ambiguity and a missing elaborated-expression fingerprint hard
blockers. There is therefore no honest canonical target for which a minimal import set,
serialized expression, canonical-target environment fingerprint, or checked alternate transport
can be certified. The required removed-hypothesis, changed-domain, changed-binder-scope, and
boundary-case mutations are undefined, not passed. No `Statement.lean`, declaration, axiom,
placeholder, weakened special case, or broadened interface was added. The root vector remains
`[H1, M4, R4]`.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` re-elaborates under the pinned environment using
the direct import `Mathlib.Combinatorics.Enumerative.Partition.Glaisher`. Its checks expose adjacent
partition, restricted-count, power-series, infinite-sum, and infinite-product interfaces. All
checks pass, and the three printed axiom reports contain only `propext`, `Classical.choice`, and
`Quot.sound`.

The probe defines no Rogers-Ramanujan restriction, canonical target, checked source transport, or
proof body. Its broad discovery import cannot be certified minimal for an absent target and gives
no statement or proof credit. A bounded exact-topic search, excluding the probe, found no
Rogers-Ramanujan declaration in pinned mathlib, repository-local Lean, or this target. A generic
q-Pochhammer comment and an unrelated modular-forms TODO mentioning Ramanujan identities are not
target declarations. This is scoped feasibility evidence, not the downstream anchor audit or a
global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was reused read-only. No `lake update`, `lake build`, dependency
clone or fetch, or other dependency mutation was run. The mathlib package worktree remained clean.

## Validation Record

Commands ran in the isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0918` | 0 | rank 1460; planned; `L0/rework_required`; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base identifiers appear above |
| `sha256sum` over the authority, source, intake, toolchain, lock, and named pinned mathlib inputs | 0 | exact current hashes are recorded in `statement-blocker.json`; historical intake authority hashes were not rewritten |
| `python3 -B Stage1_Instances/THM-M-0918/check_intake.py` | 1 | historical intake replay stops at line 166 because it expects intake authority state `[ ]`, while the integrated execution DAG records provisional `[_]` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0918/IntakeProbe.lean` | 0 | 15 adjacent APIs elaborated and three axiom reports printed; captured output 2,707 bytes, SHA-256 `dd94c45218c0428699e7371cbad8d1867196ea4798a22a8f6a1b2872aa866ae5`; no canonical target or proof body |
| bounded exact-topic `rg` search excluding `IntakeProbe.lean` | 1 (expected no match) | no Rogers-Ramanujan declaration; empty output SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| prohibited declaration scan over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0918/statement-blocker.json`; scoped `jq -e` invariants | 0 | finalized blocker is valid JSON and records the correct identity, null target, unchanged vector, four undefined mutations, false completion flags, and exact two-file change scope |
| scoped `git diff --check` plus per-added-file `git diff --no-index --check` | 0 aggregate | no whitespace diagnostics; each no-index status 1 is only the expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | worker self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The intake checker is a historical receipt checker. It binds the earlier intake authority state,
shared-input hashes, base revision, and original nine-file inventory. This statement attempt
records its exact replay limitation rather than rewriting the intake checker, receipt, instance,
target-local task DAG, generated blueprint, or authoritative execution DAG to manufacture
agreement.

## Retry Condition And Status Boundary

The integration lane must master-accept refreshed intake evidence before a future statement can be
accepted. Accountable reviewers must preserve and hash one lawful immutable source edition,
select and independently approve the exact root shape, reconcile the date and provenance boundary,
and transcribe every incorporated definition, ordered binder, hypothesis, conclusion, proof
boundary, correction, erratum, and degenerate case. In particular, they must decide first versus
second identity versus an explicit pair, analytic versus formal versus combinatorial semantics,
and whether checked transports are part of the root.

A fresh statement attempt can then encode precisely that approved claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and run all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement item or any
downstream item. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof
credit, or master acceptance is claimed.
