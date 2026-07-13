# Exact-statement gate: blocked

Item: `S56-M-0916-STATEMENT`

Theorem: `THM-M-0916`

Base revision: `a3b18eec39bf04be025b1641cae02f4d44fdf11a` (tree
`fdfff18dea4c6798c5b322b6088dfe556109c134`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0916-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`; the intake receipt declares `accepted: false`, is not
content-addressed, and has no accepted receipt ID. Dependency-ordered inspection can proceed from
that evidence, but no statement transition can be accepted from it.

Independently and decisively, the exact-statement gate fails. The authoritative catalog record
supplies only the title "Euler's pentagonal number theorem," a 1750 attribution, and the gloss "a
generating-function identity for integer partitions." It supplies no displayed equation, citation,
definition, coefficient domain, convergence regime, ordered binders, hypotheses, conclusion,
boundary policy, correction history, or independent source approval. Its `verified` label is
untrusted metadata under rev-5.6.

The intake correctly leaves the canonical mathematical statement and Lean target null. The name
and gloss do not select among materially different possible roots:

- the product over positive `m` of `(1 - X^m)` equals the signed generalized-pentagonal series;
- the integer-indexed expansion versus its paired positive-natural-index presentation;
- the reciprocal product equals the ordinary partition-number generating series;
- the coefficient recurrence for `p(n)` derived from those identities; or
- an analytic q-series identity under a convergence hypothesis versus an identity of formal power
  series over a source-selected coefficient ring.

These forms require real proposition-level decisions about infinite product and sum semantics,
coefficient ring and topology, signs and exponent coercions, indexing and the constant term,
`p(0)`, invertibility, and analytic boundary cases. Choosing the convenient DLMF paired formula,
an integer-indexed formal-power-series formula, the reciprocal partition identity, or the
recurrence would invent or substitute mathematics rather than elaborate one approved exact
received statement.

Euler E244 Proposition 3 is a matching primary-text proof lead, and DLMF 27.14.E4-E5 is a strong
modern statement lead. Neither has been admitted through the complete source, translation,
assumption, semantics, correction, and independent-review gate. The catalog's 1750 date is
plausibly a first-proof date rather than the 1760 E244 publication date and remains to be
reconciled with the selected source boundary.

Rev-5.6 sections 5 and 5.1 make statement ambiguity and a missing elaborated-expression
fingerprint hard blockers. With no approved canonical proposition, there is no honest import set
to minimize, no canonical expression or environment fingerprint, and no credited alternate
transport. The required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case
mutations are undefined, not passed. The root vector remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates under the pinned environment using the single direct
import `Mathlib.Combinatorics.Enumerative.Partition.GenFun`. Its eight checks expose adjacent
partition and formal-power-series APIs, including `Nat.Partition.genFun`,
`Nat.Partition.hasProd_genFun`, and `Nat.Partition.genFun_eq_tprod`. All checks pass. The imported
module itself marks the weight-one ordinary partition-function specialization as TODO and provides
no signed pentagonal expansion.

The probe declares no canonical target, checked source transport, or proof body, and its header
marks it as discovery only. Its import cannot be certified minimal for an absent target and
receives no statement or proof credit. A bounded exact-topic search over pinned mathlib,
repository-local Lean, and the owned target (excluding the probe) found no pentagonal-number or
partition-recurrence declaration under the recorded terms. This is feasibility evidence only, not
the downstream anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was reused read-only. No update, build, dependency clone,
fetch, or other dependency-mutation command was run, and the pinned mathlib worktree remained
clean.

## Validation Record

Commands ran on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0916` | 0 | rank 1458; planned; `L0/rework_required`; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `Formalizations/Lean/.lake` symlink was untracked; base identifiers appear above |
| exact-path `sha256sum` commands recorded in `statement-blocker.json` | 0 | authority, source, intake, probe, toolchain, dependency-lock, and pinned mathlib digests agree with the structured blocker |
| `cd Formalizations/Lean && lake env lean --version`; `lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package status | 0 | pinned mathlib revision and tree match the values above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0916/IntakeProbe.lean` | 0 | eight adjacent APIs elaborated; stdout was 1,017 bytes with SHA-256 `7f51f5c65e6380eea5d47dc3eaa13ecc9c6d4adaf19f838abc8c1da7d77c1129`; no target declaration or proof body |
| bounded exact-topic `rg` search excluding `IntakeProbe.lean` | 1 (expected no match) | no target-specific declaration matched the recorded terms |
| `python3 -B Stage1_Instances/THM-M-0916/check_intake.py` | 1 | the historical intake checker stops because it freezes the intake authority state as `[ ]`, while the integrated execution DAG now records `[_]`; its frozen shared-input hashes, base revision, and intake-only inventory also predate this phase |
| prohibited declaration scan over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0916/statement-blocker.json` | 0 | finalized structured blocker parses as valid JSON |
| scoped `python3 -c` semantic invariant check over `statement-blocker.json` | 0 | identity, blocked state, null target and imports, unchanged H1/M4/R4 vector, four undefined mutations, false completion flags, exact two-file change scope, empty receipt/fingerprint IDs, and absent self-test agree |
| scoped `git diff --check` plus per-new-file no-index checks | 0 aggregate | no whitespace diagnostics; each no-index exit 1 is only the expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest is absent because the exact-statement deliverable did not pass |

The intake checker is a historical receipt checker. It binds the earlier intake authority state,
shared-input hashes, base revision, and original nine-file inventory. This statement attempt
records its exact replay limitation rather than rewriting the intake receipt, checker, instance,
target-local task DAG, generated blueprint, or authoritative execution DAG to manufacture
agreement.

## Retry Condition And Status Boundary

The integration lane must master-accept refreshed intake evidence before a future statement can be
accepted. Accountable reviewers must preserve and hash a lawful immutable source edition, select
and independently approve the exact root, reconcile the catalog date, and transcribe every
incorporated definition, ordered binder, hypothesis, conclusion, formal or analytic semantic
choice, product and sum convention, index and sign convention, coefficient and inverse condition,
correction, erratum, and degenerate case.

A fresh statement attempt can then encode precisely that approved claim, minimize the pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and run all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement item or any
downstream item. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
