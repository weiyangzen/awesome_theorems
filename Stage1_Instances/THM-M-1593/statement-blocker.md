# Exact-statement gate: blocked

Item: `S56-M-1593-STATEMENT`

Theorem: `THM-M-1593`

Base revision: `f23ca64267b6746e12a641dcc66cc4dbaf1e2191` (tree
`d1872d3251ef6a9c395116467608691849d80496`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1593-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. Rev-5.6 section 10.2 permits this dependency-ordered
attempt, so pending master acceptance did not prevent the work. The intake receipt is
non-content-addressed, declares `accepted: false`, has no accepted receipt ID, and intentionally
leaves the canonical mathematical statement and Lean target null. Master acceptance remains
required before any eventual accepted statement transition.

Independently, the exact-statement gate cannot pass from the authoritative repository record. It
supplies only the title `LDPC码`, the attribution Robert Gallager, the year 1963, and the noun phrase
`低密度奇偶校验码` (low-density parity-check codes). It contains no cited proposition, formula,
definition chain, ordered binder, hypothesis, conclusion, boundary case, proof boundary, or
correction history. Stage0 explicitly leaves the precise definitions and premises open, and the
catalog's `已验证` label is untrusted under rev-5.6.

The inspected authoritative source family confirms rather than removes the ambiguity. Gallager's
1963 monograph and 1962 article distinguish materially different claims, including:

- construction of a regular binary sparse parity-check ensemble;
- typical minimum-distance growth, including exceptional low-degree behavior;
- maximum-likelihood error bounds and comparisons with random codes;
- a probabilistic iterative decoder and finite or asymptotic decoding bounds;
- equipment or data-handling complexity; and
- stronger hypothesized or experimentally observed decoder performance.

The repository selects none of them. It also leaves open the alphabet; deterministic-code versus
ensemble scope; regularity and degree conventions; matrix or Tanner-graph quotient; rank and
divisibility assumptions; probability space; distance and rate conventions; channel, decoder, tie,
and iteration rules; asymptotic parameters and quantifier order; exact conclusion; and every
zero-size, rank-deficient, graph, endpoint, and nontermination case. These choices produce
inequivalent propositions.

Selecting a familiar minimum-distance or decoding theorem, conjoining several results, treating the
sparse-code definition as the theorem, or using the elementary kernel identity as a performance
claim would invent, narrow, broaden, or substitute mathematics rather than elaborate the exact
received target. The distinct computer-science catalog record `THM-C-0385` is outside the Stage1
Lean target set and supplies no authority to select or broaden this root.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing expression
fingerprint hard blockers. There is consequently no honest canonical expression for which minimal
imports, checked transports, or removed-hypothesis, changed-domain, changed-binder-scope, and
boundary-case mutations can be certified. Those mutations are undefined, not passed. The vector
remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates in the pinned environment. Its two direct imports
expose generic Hamming-distance, Hamming-weight, matrix, matrix-vector, and linear-map interfaces.
All seven checks pass. This is real substrate validation, but the probe defines no alphabet-specific
LDPC code, sparse ensemble, probability space, channel, decoder, asymptotic proposition, canonical
target, checked transport, or proof body. Its imports therefore cannot be certified minimal for an
absent target.

A bounded lexical search of pinned mathlib and repository-local Lean found no `LDPC`, low-density
parity-check, or parity-check-code declaration under the recorded terms. This is discovery-only
feasibility evidence, not the downstream immutable anchor audit or a claim of global absence.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No update, build, clone, fetch, or dependency
mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1593` | 0 | rank 1019; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| repository, Stage0, intake dossier, and Gallager source-family inspection | 0 | confirmed the noun-phrase catalog record, multiple inequivalent source results, null intake target, and absence of an approved root selection |
| `sha256sum` over authority, source, intake, probe, toolchain, and pinned mathlib inputs | 0 | exact current hashes are recorded in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1593/IntakeProbe.lean` | 0 | seven generic APIs elaborated; stdout SHA-256 `4ca1b5ba...d50f`; no canonical target or proof body |
| bounded LDPC search in pinned mathlib and repo-local Lean | 1 | expected no-match result; discovery-only evidence |
| `python3 -B Stage1_Instances/THM-M-1593/check_intake.py` | 1 | historical intake replay stops at its stale pre-integration blueprint hash; its original nine-file inventory is also intentionally historical after this phase |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |

The historical intake checker is frozen to its original authority bytes and nine-file intake
inventory. Integration subsequently changed the generated blueprint and execution DAG. Adding
these statement artifacts also makes that intake-only inventory historical. This statement run
records the limitation instead of rewriting the intake checker, receipt, instance, task DAG,
generated blueprint, or authoritative execution DAG to manufacture agreement.

## Retry Condition And Status Boundary

Accountable reviewers must preserve and hash an immutable primary or authoritative source, select
and independently approve one exact LDPC proposition, and transcribe every incorporated definition,
convention, ordered binder, hypothesis, conclusion, proof boundary, correction, erratum,
proved-versus-hypothesized boundary, and degenerate case while preserving neighboring-target
boundaries. The integration lane must also master-accept the intake dependency before accepting a
future statement transition.

A fresh statement worker can then encode precisely that source-selected claim, minimize pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
