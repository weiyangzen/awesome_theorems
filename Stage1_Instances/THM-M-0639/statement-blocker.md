# Exact-statement gate: blocked

Item: `S56-M-0639-STATEMENT`

Theorem: `THM-M-0639`

Base revision: `ec27eb0336c89f0aed87200fc7cbf03a09996597` (tree
`3fe77e381bf94ce1ed347bed17c94af25de8d543`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0639-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. Rev-5.6 section 10.2 permits this dependency-ordered
attempt from a provisional predecessor, but master acceptance would still be required for any
future statement transition.

Independently, the exact-statement deliverable cannot be completed from the authoritative
repository record. The catalog gives only the title Kakutani fixed-point theorem, the attribution
Shizuo Kakutani, the year 1941, and the gloss `集值映射的不动点` ("a fixed point of a set-valued
map"). It gives no formula, source citation, incorporated definition, ordered binder, hypothesis,
conclusion, proof boundary, erratum, boundary case, or formal artifact. Its `已验证` label is
explicitly untrusted under rev-5.6.

The primary lead is Shizuo Kakutani, *A generalization of Brouwer's fixed point theorem*, **Duke
Mathematical Journal** 8(3) (1941), 457-459, DOI
`10.1215/S0012-7094-41-00838-4`. Crossref metadata confirms the article, but the Project Euclid
article and download endpoints again returned access-control HTML in this worker environment.
Consequently Theorem 1, its preceding point-set-function definition, exact assumptions, proof
boundary, and any correction history have not been inspected or independently approved.

Without that source passage, the following proposition-critical choices remain open:

- Euclidean space versus an abstract finite-dimensional real topological vector space;
- a closed bounded domain versus a compact domain, including explicit domain nonemptiness;
- closed versus compact values and the exact nonempty, convex, and containment premises;
- Kakutani's source semicontinuity definition versus mathlib's `UpperHemicontinuousOn`;
- an ambient correspondence with explicit containment versus a subtype correspondence;
- ordered binders, dimension zero, empty or singleton cases, boundary points, and escaping values;
  and
- whether a closed-graph formulation is equivalent under the selected hypotheses or a distinct
  theorem candidate.

These choices produce materially different propositions. Selecting the familiar modern
formulation would add unapproved mathematics, not elaborate the exact received target. The same
title and theorem family also appear under the separately scheduled `THM-M-0320`. There is no
accepted alias, deduplication, variant, or canonical-root ownership decision between the records.
That target's `Statement.lean` is therefore a discovery lead only; its statement, proof, receipt,
debt, and status cannot transfer to `THM-M-0639`.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing expression
fingerprint hard blockers. There is no honest canonical expression for which minimal imports,
checked transports, or removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case
mutations can be certified. Those mutations are undefined, not passed. The vector remains
`[H1, M4, R4]`.

## Pinned Lean Boundary

`IntakeProbe.lean` re-elaborates against the pinned environment. Its two direct imports expose nine
adjacent Euclidean-space, set, closedness, boundedness, compactness, convexity, and upper
hemicontinuity APIs. It defines neither a Kakutani target nor a proof body. Those discovery-only
imports therefore cannot be certified as minimal imports for an absent canonical target.

A bounded exact-topic search of pinned mathlib found no Kakutani set-valued fixed-point
declaration. This is narrow discovery evidence, not the later immutable anchor audit and not proof
of global absence.

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
| `python3 scripts/stage1_target.py show THM-M-0639` | 0 | rank 1056; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| repository source, intake, and duplicate-target inspection | 0 | confirmed the sparse catalog gloss, null intake target, uninspected primary theorem text, and unresolved duplicate boundary |
| Crossref and Project Euclid endpoint checks | 0 | metadata confirmed; four article/download URLs returned small `text/html` access-control responses rather than the primary paper |
| `sha256sum` over authority, intake, duplicate, toolchain, and pinned mathlib inputs | 0 | exact hashes are recorded in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0639/IntakeProbe.lean` | 0 | nine adjacent pinned APIs elaborated and printed; no canonical target or proof body was declared |
| bounded exact-topic search in pinned mathlib | 1 | expected no-match result; discovery-only evidence |
| `python3 -B Stage1_Instances/THM-M-0639/check_intake.py` | 1 | historical intake replay stops at line 129 because it freezes intake state `[ ]` while current authority records `[_]`; its original nine-file inventory is also historical after this phase |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0639/statement-blocker.json` plus scoped blocker invariants | 0 | identity, dependency, null target/imports, unchanged vector, four undefined mutations, false completion flags, and no-self-test boundary agree |
| scoped no-index whitespace checks and `git diff --check -- Stage1_Instances/THM-M-0639` | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The historical intake checker is frozen to the intake-era authority state and original nine-file
inventory. The integration lane later changed the intake state to `[_]`, so replay already fails
before its inventory assertion. This statement run records that limitation rather than rewriting
intake evidence or authority to manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must master-accept the intake before it can accept a future statement
transition. Accountable reviewers must lawfully preserve and hash an immutable primary or
authoritative source, inspect and transcribe the exact theorem and incorporated definitions,
resolve every assumption, proof boundary, correction, erratum, and boundary case, decide the
`THM-M-0320` duplicate or variant identity and canonical-root ownership, and independently approve
the source-to-target mapping.

A fresh statement worker can then encode precisely that approved claim, minimize pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
