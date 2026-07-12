# Exact-statement gate: blocked

Item: `S56-M-1386-STATEMENT`

Theorem: `THM-M-1386`

Base revision: `9890b8ae7278d1978497acce2be86f8fc4072af3` (tree
`b90a6c34f533284f14d1d71b0ba11c76095110d8`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1386-INTAKE` has provisional worker
state `[_]` in the authoritative execution DAG, rather than master-accepted state `[x]`. The intake
receipt declares `accepted: false`, has no accepted receipt ID, and deliberately leaves the
canonical mathematical statement and Lean target null. Rev-5.6 section 10.2 permits a
dependency-ordered statement attempt while the predecessor is provisional, but master acceptance
cannot occur until that dependency is accepted.

Independently, the exact-statement gate cannot be passed from the repository record. Its complete
mathematical wording is only the title `Sturm separation theorem` and the gloss "the zeros of
linearly independent solutions interlace." It supplies no citation, differential equation,
definition, ordered binder, hypothesis, conclusion, boundary case, proof boundary, or correction
history. The catalog's verified label is explicitly untrusted under rev-5.6.

The existing intake source review confirms that these omissions change the proposition. Paul R.
Beesack's *On Sturm's Separation Theorem*, page 481, distinguishes a classical compact-interval
theorem for `(r y')' + s y = 0` from Theorem 1 on an open interval. The latter separates
nonsingular consecutive-zero case 1(b) from materially different singular-endpoint cases 1(c)-
1(e). The catalog cites neither this article nor one of those variants. The 1836 Sturm memoir lead
also has a separately linked errata item whose exact effect has not been transcribed or reviewed.
These are source-family leads, not authority to choose a root silently.

An exact proposition must still select all of the following:

- self-adjoint, normal, Sturm--Liouville, or another second-order equation form, with any checked
  transports between forms;
- coefficient domains, continuity or integrability, positivity or nonvanishing assumptions, and
  the solution regularity and derivative semantics they support;
- real or complex scalar field, the interval and endpoint model, and treatment of singular or
  infinite endpoints;
- the domain on which the two solutions are linearly independent and whether nontriviality,
  nonzero Wronskian, simple zeros, or common-zero exclusion is assumed or derived;
- the exact consecutive-zero predicate, including endpoint membership and isolation; and
- existence versus uniqueness, reciprocal separation, or global alternation, with exact ordered
  binders and all empty, singleton, identically-zero, dependent, and endpoint boundary cases.

These choices yield inequivalent statements. Selecting the familiar compact theorem, Beesack
Theorem 1(b), the full singular-endpoint extension, an eigenfunction-interlacing theorem, or a
convenient special equation would invent, narrow, broaden, or substitute mathematics rather than
elaborate the exact received target.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing expression
fingerprint hard blockers. There is therefore no honest canonical declaration whose imports can be
certified minimal. No `Statement.lean`, exact expression, checked transport, or mutation suite was
created. The removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations
are undefined rather than passed. The root vector remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates with the pinned environment. Its five direct imports
expose derivative product, subtraction and quotient rules, pairwise linear independence,
monotonicity from derivative signs, intermediate value, and Rolle interfaces. All eight checks
pass. The probe defines no coefficient contract, solution predicate, consecutive-zero predicate,
canonical target, checked transport, or proof body. Its imports therefore cannot be certified
minimal for the absent target and receive no statement or proof credit.

A bounded topic search in pinned mathlib and repository-local Lean finds polynomial Wronskian
material and unrelated comments, but no functional Sturm-separation terminal declaration. This is
discovery-only feasibility evidence, not the downstream immutable anchor audit or a global absence
claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No update, build, clone, fetch, or dependency
mutation was run.

## Validation Record

Commands ran on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1386` | 0 | rank 996; planned; `L0/rework_required`; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `Formalizations/Lean/.lake` symlink was untracked; base revision and tree appear above |
| repository authority, source crosswalk, scope map, and intake inspection | 0 | confirmed the sparse family wording, provisional dependency, null target, and inequivalent source variants; no source-selected proposition |
| `sha256sum` over authority, intake, source, probe, toolchain, and dependency inputs | 0 | exact digests are recorded in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean and Lake versions match the pinned environment above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree match the values above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1386/IntakeProbe.lean` | 0 | eight adjacent APIs elaborated; stdout was 2,143 bytes with SHA-256 `08fbf7036a959b8b77588d2f4855706f17f7dcf59bd2d489e1279ec34cd7650f`; no target declaration or proof body |
| bounded `rg` search for `sturm`, `wronskian`, or `interlac` in pinned mathlib and repository-local Lean | 0 | only polynomial Wronskian material and unrelated comments matched; no functional Sturm-separation target |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1386-pycache python3 -B Stage1_Instances/THM-M-1386/check_intake.py` | 1 | historical intake replay first fails because it freezes authoritative intake state `[ ]`, while integration now records `[_]`; its original nine-file inventory is also intake-only |
| prohibited declaration scan over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-1386/statement-blocker.json` and scoped blocker-invariant validation | 0 | identity, base, null target fields, unchanged vector, four unrunnable mutations, false completion fields, changed paths, and absent self-test agree |
| scoped `git diff --check` plus per-new-file no-index checks | 0 aggregate | no whitespace diagnostics; each no-index exit 1 was only the expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest is absent because the exact-statement deliverable did not pass |

The intake validator is a historical intake receipt checker. It binds the earlier authoritative
`[ ]` state and exact nine-file intake inventory; integration changed the former to `[_]`, and this
statement attempt adds files beyond the latter. This attempt records those exact limits rather than
rewriting the intake receipt, instance, task DAG, generated blueprint, or authoritative execution
DAG to manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must accept refreshed intake evidence before a future statement can be
accepted. Accountable reviewers must preserve and hash one lawful complete primary or authoritative
source edition, select and independently approve one exact theorem and proof boundary, and
transcribe every incorporated definition, ordered binder, hypothesis, conclusion, correction,
erratum, and boundary case. The decision must explicitly distinguish the classical compact result,
Beesack Theorem 1(b), the singular-endpoint extension, and neighboring comparison,
Sturm--Liouville, oscillation, and eigenfunction-interlacing targets.

A fresh statement attempt can then encode precisely that approved claim, minimize pinned imports,
serialize and hash its elaborated expression and environment, compile every credited transport,
and run all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement item or any
downstream item. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
