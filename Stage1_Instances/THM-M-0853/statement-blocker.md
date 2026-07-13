# Exact-statement gate: blocked

Item: `S56-M-0853-STATEMENT`

Theorem: `THM-M-0853`

Base revision: `0c019b7194c9c43fa5f683fa82d637a0b275410d` (tree
`43cf6ac322b1dba09be739b52ab3d02e9f9d8f3e`).

## Decision

The exact Lean 4 target cannot be truthfully selected from the authoritative repository record.
That record gives only the family name `Dirac定理`, Gabriel Dirac, the year 1952, and the gloss
`Hamilton圈存在的度条件` (a degree condition for the existence of a Hamiltonian cycle). It cites no
theorem passage and supplies no exact graph model, order boundary, degree inequality, rounding
convention, ordered binders, hypotheses, conclusion, proof boundary, correction, or erratum.
Stage0 explicitly leaves the exact definitions and premises open, and the catalog's `已验证` label
is untrusted under rev-5.6.

The intake bibliographically identifies G. A. Dirac, "Some Theorems on Abstract Graphs,"
*Proceedings of the London Mathematical Society* s3-2(1), 69-81 (1952), DOI
`10.1112/plms/s3-2.1.69`, as the likely primary source. The article text and a proposition-level
crosswalk were not admitted. Fresh publisher, DOI, and text-mining endpoint probes again returned
access errors; Crossref, zbMATH, MathWorld, and other metadata remain discovery or secondary
evidence rather than an immutable, independently reviewed theorem passage.

Consequently, the received record does not decide:

- the finite simple undirected graph model and its labelled carrier and typeclass context;
- whether the order premise is exactly `3 <= n` and how orders zero, one, two, and three are treated;
- whether the degree condition is pointwise or stated through minimum degree;
- whether "at least half the order" is a real/rational inequality, `n <= 2 * d`,
  `(n + 1) / 2 <= d`, or another exact integral encoding;
- whether Hamiltonian-cycle existence maps directly to `SimpleGraph.IsHamiltonian` or to an
  explicit `Walk.IsHamiltonianCycle` witness with a checked transport; or
- the ordered universes, binders, hypotheses, conclusion, credited alternates, and boundary cases.

These decisions are proposition-changing. In particular, the floor formula `n / 2 <= d` is
strictly weaker at odd order than the conventional half-order condition. Selecting the familiar
formula

```text
3 <= card V -> card V <= 2 * G.minDegree -> G.IsHamiltonian
```

from memory or formal convenience would invent proposition identity that the repository intake
deliberately leaves open. Ore's theorem, Chvatal-Erdos, a Hamiltonian path, connectedness, a long
cycle, and random-graph Hamiltonicity are different roots and cannot be substituted.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing expression
fingerprint hard blockers. The intake therefore correctly leaves `canonical_statement`, the Lean
module and expression, minimal imports, and the expression/environment fingerprints null. Without
a canonical target, alternate transports and the required removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations are undefined, not passed. No `Statement.lean`,
axiom, placeholder, assumed theorem, weakened special case, or broadened target was introduced.

The prerequisite `S56-M-0853-INTAKE` has provisional worker state `[_]` rather than
master-accepted `[x]`. Dependency-ordered inspection can record this blocker, but master acceptance
remains independently required before any future statement transition can be accepted.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates in the pinned environment with the single direct
import `Mathlib.Combinatorics.SimpleGraph.Hamiltonian`. It checks eleven finite-graph degree and
Hamiltonicity interfaces and four candidate proposition shapes. All checks pass. The probe declares
no canonical target, checked source transport, or proof body. Its import is therefore a statement
substrate import, not a minimal-import certificate for an absent target, and receives no statement
or proof credit.

A bounded pinned-source search found only mathlib's two-vertex Hamiltonicity boundary lemma in the
graph-theoretic search scope; unrelated physics occurrences of "Dirac Hamiltonian" were excluded.
This is discovery-only feasibility evidence, not the downstream immutable anchor audit and not a
global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was run.

## Validation Evidence

Commands ran in this isolated worker clone on 2026-07-13 (`Asia/Shanghai`), from the repository root
unless another working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0853` | 0 | rank 1407, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; the base revision and tree are recorded above |
| manifest, blueprint sections 5/5.1, skill, catalog, Stage0, and intake inspection | 0 | only a broad degree-condition gloss is authoritative; every proposition-changing statement choice remains open |
| primary-source and open-access metadata probes | 0 at the command layer | Crossref confirmed only bibliographic and text-mining metadata; publisher/DOI/PDF endpoints returned HTTP 403 and no article theorem passage was admitted |
| `python3 -B Stage1_Instances/THM-M-0853/check_intake.py` before adding blocker files | 0 | historical intake invariants replayed: planned `[H1, M3, R4]`, null canonical target, and six open tasks; its exact nine-file inventory makes it historical after this phase |
| the same intake checker after adding blocker files | 1 | expected historical-inventory failure at `check_intake.py:226`; it rejects the two new statement-blocker artifacts and is not claimed as the current statement validator |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions agree with the environment above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree agree; package worktree is clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0853/IntakeProbe.lean` | 0 | eleven interfaces and four candidate shapes elaborated; stdout is 1966 bytes over 23 lines with SHA-256 `b424c7fc4cd79a80de801f75081d34dc5ec6a1e2768b16db2157de644d7ff6bd`; no canonical target was declared |
| bounded exact-topic search in pinned mathlib and repo-local Lean | 0 with only boundary/unrelated matches | no Dirac minimum-degree-to-Hamiltonicity closure found in the graph-theoretic search scope; discovery only |
| prohibited Lean declaration scan over `IntakeProbe.lean` | 1 | expected no-match result; no prohibited proof/declaration construct occurs in the only Lean artifact |
| `python3 -m json.tool ...` plus the exact inline Python invariant recipe recorded in `statement-blocker.json` | 0 | current artifact identity, blocked open state, null target/imports, unchanged vector, four undefined mutations, false completion flags, exact two-file change scope, byte hygiene, and absent self-test agree |
| scoped whitespace checks | 0 | no whitespace diagnostics in the two blocker artifacts |
| `test ! -e .stage1-worker-selftest.json` | 0 | the self-test manifest is absent because the exact-statement deliverable did not pass |

## Retry Condition

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must then
lawfully preserve and hash an immutable primary or accepted authoritative source, pinpoint and
independently approve its exact theorem passage and incorporated definitions, and crosswalk every
ordered binder, hypothesis, conclusion, proof boundary, correction, erratum, and boundary case.
They must freeze the graph model, order boundary, degree scope, odd-order rounding, and
Hamiltonicity convention.

A fresh statement worker can then encode precisely that source-selected claim, minimize pinned
imports, serialize and hash its elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This is a blocked-attempt record, not completion of the statement node or any downstream node. The
root remains `[H1, M3, R4]`, with `audit_complete: false` and `theorem_complete: false`; no debt
change is proposed. Because the assigned phase is not genuinely self-tested to its completion gate,
no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or master acceptance is claimed.
