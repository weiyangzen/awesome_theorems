# Exact-statement gate: blocked

Item: `S56-M-1390-STATEMENT`

Theorem: `THM-M-1390`

Base revision: `9890b8ae7278d1978497acce2be86f8fc4072af3` (tree
`b90a6c34f533284f14d1d71b0ba11c76095110d8`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1390-INTAKE` has provisional worker
state `[_]` in the authoritative execution DAG, not master-accepted state `[x]`. Rev-5.6 section
10.2 permits this dependency-ordered attempt, so pending master acceptance did not prevent the
work. The intake receipt is non-content-addressed, declares `accepted: false`, has no accepted
receipt ID, and deliberately leaves the canonical mathematical statement and Lean target null.
Master acceptance remains necessary before any future statement transition can be accepted.

Independently, the exact-statement gate cannot be passed from the authoritative repository record.
It supplies only the title `Courant极小极大原理`, Richard Courant, 1920, and the gloss
`特征值的变分刻画` ("a variational characterization of eigenvalues"). It contains no
bibliography, formula, operator, function space, boundary condition, ordered binder, hypothesis,
conclusion, proof boundary, correction history, or formal artifact. Stage0 explicitly leaves the
precise definitions and premises open, and the catalog's `已验证` label is untrusted under
rev-5.6.

The intake's historical-source inspection confirms rather than resolves the ambiguity. Richard
Courant's 1920 paper *Ueber die Eigenwerte bei den Differentialgleichungen der mathematischen
Physik*, Section 3, Satz 3a, journal pages 18-19, is a strong source lead. In its weighted
self-adjoint elliptic boundary-value setting, it characterizes the nth eigenvalue as the supremum
over `n - 1` test-function systems of the constrained energy infimum, subject to normalization,
boundary conditions, and orthogonality, with an attainment clause. But the catalog does not cite
the paper or Satz 3a. The inspected scan is not a repository-owned admitted source, its OCR is
imperfect, and the exact German statement, incorporated definitions and regularity assumptions,
energy and boundary-term signs, index and multiplicity conventions, minimum/infimum and
maximum/supremum distinctions, proof boundary, corrections, translation, and independent review
remain open.

Nor does the catalog select a modern replacement. Courant's elliptic-PDE result, the
finite-dimensional Courant-Fischer theorem, a compact self-adjoint operator theorem, a semibounded
operator or closed-form theorem, and a Sturm-Liouville specialization have materially different
domains, assumptions, spectra, competitor classes, and boundary cases. Choosing one familiar
variant, conjoining variants, or packaging the desired equality as a premise would invent,
broaden, substitute, or circularly assume mathematics rather than elaborate the exact received
target. A merely extremal Rayleigh-quotient theorem would also collapse the boundary with the
separate `THM-M-0055` target and lose the indexed-eigenvalue content.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing elaborated
expression fingerprint hard blockers. Consequently there is no honest canonical declaration for
which minimal imports can be claimed. No `Statement.lean`, exact expression, checked alternate
transport, or mutation suite was created. The required removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations are undefined rather than passed. The vector
remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with the pinned environment. Its direct imports
expose generic Rayleigh-quotient, global extremal-eigenvalue, sorted-eigenvalue, and eigenbasis APIs;
all nine checks pass. None states an indexed subspace or constrained-orthogonality min-max equality,
and the probe declares no canonical target or proof body. Although the probe itself can be reduced
to the transitive `Mathlib.Analysis.InnerProductSpace.Spectrum` import, that observation is not a
minimal-import result for the unidentified theorem.

A bounded exact-topic search of pinned mathlib and repository-local Lean found no Courant-Fischer
or indexed eigenvalue-minimax declaration. This is feasibility evidence only, not the downstream
immutable anchor audit and not a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No update, build, clone, fetch, or dependency
mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (Asia/Shanghai).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1390` | 0 | rank 1000; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| repository, intake, scope, and source-crosswalk inspection | 0 | confirmed the sparse catalog record, null canonical target, inequivalent historical and modern variants, and open independent source review |
| `sha256sum` over authority, intake, source, probe, toolchain, and pinned mathlib inputs | 0 | exact hashes are recorded in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1390/IntakeProbe.lean` | 0 | nine adjacent pinned Rayleigh and spectral APIs elaborated; no canonical target or proof body was declared |
| bounded exact-topic search in pinned mathlib and repo-local Lean | 1 | expected no-match result; discovery-only evidence |
| `python3 -B Stage1_Instances/THM-M-1390/check_intake.py` | 1 | historical intake replay freezes authority state `[ ]`, but the integrated DAG now records provisional `[_]`; its original nine-file inventory also becomes historical after this phase |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-1390/statement-blocker.json` plus scoped blocker invariants | 0 | identity, dependency state, null target/imports, unchanged vector, four undefined mutations, false completion flags, and no-self-test boundary agree |
| scoped whitespace checks for both new files and `git diff --check -- Stage1_Instances/THM-M-1390` | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The historical intake checker is frozen to its original authority bytes and nine-file intake
inventory. Integration subsequently changed the intake state to `[_]`, so replay already fails at
that state assertion. Adding these blocker artifacts also makes the old inventory historical. This
statement run records the limitation rather than rewriting intake evidence or an authoritative
state file to manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must master-accept the intake dependency before it can accept a future
statement transition. Accountable reviewers must preserve and hash one lawful immutable primary or
authoritative source, select and independently approve one exact proposition, transcribe every
incorporated definition, ordered binder, hypothesis, conclusion, proof boundary, correction, and
boundary case, and approve its relationship to the historical PDE, modern operator, finite-
dimensional, Sturm-Liouville, and neighboring-target variants.

A fresh statement worker can then encode precisely that source-selected claim, minimize pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, node-specific completion receipt,
worker `[_]`, or master acceptance is claimed.
