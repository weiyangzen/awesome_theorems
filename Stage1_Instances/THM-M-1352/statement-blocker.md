# Exact-statement gate: blocked

Item: `S56-M-1352-STATEMENT`

Theorem: `THM-M-1352`

Base revision: `0d26adeae663d55eb536120f7d93ede975fe8f49` (tree
`6b5ab44050900e9a4a181b4fc56b1e965183f2c9`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1352-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. Rev-5.6 section 10.2 permits this dependency-ordered
attempt from a provisional predecessor, but the integration lane must accept the intake before it
can accept any future statement transition. The intake receipt itself declares `accepted: false`,
is not content-addressed, contains no accepted receipt ID, and intentionally leaves both the
canonical mathematical statement and Lean target null.

Independently, the exact-statement gate cannot be passed from the authoritative repository record.
It supplies only the title `Floquet理论` (Floquet theory), Gaston Floquet, the year 1883, and the
gloss `周期线性系统的理论` (the theory of periodic linear systems). There is no citation, formula,
equation model, domain, ordered binder, hypothesis, conclusion, incorporated definition, boundary
case, proof boundary, correction history, or reviewer. The catalog's `已验证` label is explicitly
untrusted under rev-5.6.

This wording names a subject family rather than one truth-valued proposition. The inspected modern
source lead separates at least these materially different roots:

- time-shift periodicity of a principal matrix solution and the induced monodromy relation;
- Floquet decomposition into a periodic factor and a matrix exponential;
- a real decomposition at twice the coefficient period versus a complex form at the original
  period;
- definitions and results for multipliers and characteristic exponents;
- reduction by a periodic change of variables to constant coefficients; and
- periodic-solution, stability, and asymptotic-stability criteria.

The neighboring catalog records sharpen the ownership boundary: `THM-M-1353` separately names the
Floquet theorem and a fundamental solution matrix, `THM-M-1354` names characteristic exponents,
and `THM-M-1355` names stability of linear systems. Selecting a familiar decomposition, bundling a
chapter's results into one conjunction, or taking a neighbor's conclusion would invent, broaden,
or substitute mathematics.

The system model is also unresolved. A source decision must fix the scalar field, dimension,
coefficient regularity, time domain, positive and possibly minimal period, local or global solution
notion, fundamental-matrix normalization and base time, multiplication convention, monodromy,
matrix-logarithm existence and branch policy, real versus complex form, and all degenerate cases.
These choices alter the proposition rather than merely its notation.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing expression
fingerprint hard blockers. There is consequently no honest canonical expression for which minimal
imports, a normalized expression hash, checked transports, or removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations can be certified. Those mutations are undefined,
not passed. The root vector remains `[H5, M4, R4]`.

## Pinned Lean boundary

The existing `IntakeProbe.lean` re-elaborates with the pinned toolchain. Its three direct imports
expose generic periodic-function, integral-curve, derivative, matrix, determinant, and
matrix-exponential interfaces. All eight checks pass. This is real substrate validation, but the
probe defines no periodic linear system, principal or fundamental matrix solution, monodromy,
Floquet decomposition, exponent, reducibility result, stability criterion, canonical target,
checked source transport, or proof body. Its imports therefore cannot be certified minimal for an
absent target.

A bounded exact-topic search of pinned mathlib and repo-local Lean found no candidate beyond the
probe's explanatory comment. That observation is discovery-only evidence, not the downstream
immutable anchor audit or a claim of global absence.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No update, build, clone, fetch, or dependency
mutation was run.

## Validation record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1352` | 0 | rank 962; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| `sed`/`python3 -m json.tool` inspection of the authoritative manifest, catalog, Stage0, blueprint, skill, intake dossier, and recorded modern source-family crosswalk | 0 | confirmed the sparse theory label, null intake target, inequivalent Floquet result families, and neighbor ownership boundaries |
| `sha256sum` over authority, intake, toolchain, lock, probe, and three pinned mathlib source inputs | 0 | exact hashes are recorded in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1352/IntakeProbe.lean` | 0 | eight adjacent pinned APIs elaborated; no canonical target or proof body was declared |
| bounded exact-topic `rg` search in pinned mathlib, repo-local Lean, and the owned path | 0 | a broad search matched only the probe's negative explanatory comment; a strict declaration-oriented search excluding the probe returned 1 (no match); discovery-only evidence |
| `python3 -B Stage1_Instances/THM-M-1352/check_intake.py` | 1 | historical intake replay stops at line 129 because it freezes intake authority state `[ ]` while the current authoritative DAG records `[_]`; its original nine-file inventory is also historical after this phase |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-1352/statement-blocker.json` plus the exact scoped Python assertion recorded in the structured blocker | 0 | identity, dependency state, null target/imports, unchanged vector, four undefined mutations, false completion flags, and no-self-test boundary agree |
| scoped whitespace checks for both new files and `git diff --check -- Stage1_Instances/THM-M-1352` | 0 aggregate | each no-index check returned the expected difference exit 1 with no diagnostic; tracked-diff check returned 0; no whitespace errors |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The historical intake checker is frozen to its original authority bytes and nine-file intake
inventory. The integration lane subsequently changed the generated intake state to `[_]`, so replay
already fails before its inventory assertion. Adding these two statement artifacts also makes that
intake-only inventory historical. This phase records the limitation instead of rewriting the intake
checker, receipt, instance, task DAG, generated blueprint, or authoritative execution DAG to
manufacture agreement.

## Retry condition and status boundary

The integration lane must first master-accept the intake dependency. Accountable reviewers must
then preserve and hash a lawful immutable primary or authoritative source, select and independently
approve one exact proposition or explicitly sourced conjunction, transcribe every incorporated
definition, ordered binder, hypothesis, conclusion, proof boundary, correction, and boundary case,
and reconcile `THM-M-1353` through `THM-M-1355` ownership.

A fresh statement worker can then encode precisely that source model, minimize pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport, and
execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
