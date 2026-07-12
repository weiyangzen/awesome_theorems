# Exact-statement gate: blocked

Item: `S56-M-1389-STATEMENT`

Theorem: `THM-M-1389`

Base revision: `d3cbfa8941a8bcaafa3b8a690d1333f9643288ad` (tree
`e912a107150c6f9c3fc096901412fce0337c7c01`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1389-INTAKE` has provisional worker
state `[_]` in the authoritative execution DAG, not master-accepted state `[x]`. Rev-5.6 section
10.2 permits this dependency-ordered attempt, but no statement transition can be accepted before
the dependency is accepted. The intake receipt declares `accepted: false`, has no accepted receipt
ID, and deliberately leaves the canonical mathematical statement and Lean target null.

Independently, the exact-statement gate cannot be entered truthfully from the repository record.
Its complete mathematical wording is the title `Weyl渐近公式` (Weyl asymptotic formula), Hermann
Weyl, 1911, and the gloss `特征值的渐近分布` (asymptotic distribution of eigenvalues). It provides
no bibliography, formula, operator, dimension, domain, boundary conditions, spectrum convention,
ordered binders, hypotheses, conclusion, proof boundary, correction history, or formal artifact.
Stage0 explicitly leaves exact definitions and premises open, and the catalog's `已验证` label is
untrusted under rev-5.6.

The intake source work confirms a theorem family rather than selecting a proposition. Weyl's
1912 paper on linear partial differential equations, with a possible 1911 announcement, is a
strong historical lead for a multidimensional PDE spectral law. The catalog, however, places this
target in the ordinary-differential-equations category. The modern regular Sturm-Liouville result
located in Teschl, Theorem 5.25, is aligned with that category but is a propositionally different
secondary formulation and is not cited by the catalog. Neither source lead was admitted as the
canonical root or independently approved at intake.

The unresolved choices include:

- a Dirichlet or Neumann Laplacian, variable-coefficient elliptic operator, Laplace-Beltrami
  operator, regular or singular Sturm-Liouville operator, or another spectral model;
- a bounded Euclidean domain, compact manifold, finite interval, half-line, or another carrier,
  with its dimension, measure, metric, coefficient regularity, and positivity assumptions;
- boundary conditions, self-adjointness, semiboundedness, compact-resolvent assumptions, zero and
  negative modes, multiplicity, disconnected domains, and index origin;
- an eigenvalue enumeration, spectral counting function, heat trace, or another encoding, and the
  exact checked relationships among them;
- the asymptotic variable and filter, exponent, normalization, volume or coefficient factor,
  Fourier convention, leading constant, equality or equivalence notation, and remainder; and
- every ordered binder, hypothesis, conclusion, exceptional case, incorporated definition, and
  proof boundary of one approved result.

The classic bounded-domain counting law, its inverse eigenvalue form, a geometric manifold law,
an elliptic phase-space law, and the one-dimensional Sturm-Liouville `n^2` formula are related but
not interchangeable. Choosing one from mathematical memory, silently reconciling the PDE/ODE
conflict, or packaging the desired asymptotic as a premise would invent, narrow, broaden, or
substitute mathematics.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing elaborated
expression fingerprint hard blockers. There is consequently no canonical proposition for which
minimal imports can be claimed. No `Statement.lean`, target declaration, expression hash, checked
transport, or mutation fixture was added. Removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations are undefined rather than passed. The intake
vector remains `[H5, M4, R4]`; `H5` classifies the received record as unstable, not the established
mathematics conventionally called Weyl's law.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` directly imports
`Mathlib.Analysis.Asymptotics.AsymptoticEquivalent` and
`Mathlib.Analysis.InnerProductSpace.Spectrum`. It re-elaborates seven adjacent asymptotic and
finite-dimensional spectral interfaces. It defines no infinite-dimensional operator, discrete
spectrum, eigenvalue enumeration, spectral counting function, Weyl constant, target theorem, or
proof body. Its imports are discovery candidates only and cannot be certified minimal for an
absent target.

A bounded exact-topic search found no Weyl-law, Weyl-asymptotic, spectral-counting-law, or
eigenvalue-asymptotic declaration in pinned mathlib or repository-local Lean. This is narrow
feasibility evidence, not the downstream immutable anchor audit and not a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink points to the canonical pinned artifacts and was used read-only.
No update, build, clone, fetch, or dependency mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (Asia/Shanghai).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1389` | 0 | rank 999; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| source, Stage0, manifest, blueprint, skill, and intake inspection | 0 | confirmed the sparse family wording, null target, PDE/ODE conflict, and materially different candidate formulations |
| `git blame -L 10118,10123 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sha256sum` over authority, source, intake, probe, toolchain, and dependency inputs | 0 | exact input hashes are recorded in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| mathlib `rev-parse HEAD 'HEAD^{tree}'` and package `git status --short` | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1389/IntakeProbe.lean` | 0 | seven adjacent pinned APIs elaborated; complete stdout SHA-256 `2ae8729c94c785976149ed3be161298cc11953cabf021cedd60103d96fef12dc`; no target declaration or proof body |
| bounded exact-topic `rg` search over pinned mathlib and repo-local Lean | 1 | expected no-match result; discovery-only evidence |
| `python3 -B Stage1_Instances/THM-M-1389/check_intake.py` | 1 | historical intake replay stops because it freezes intake authority state `[ ]`, while the integrated DAG now records provisional `[_]`; its original nine-file inventory also becomes historical after this phase |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-1389/statement-blocker.json` plus scoped blocker invariants | 0 | blocker JSON parses; identity, dependency state, null target/imports, unchanged vector, four undefined mutations, false completion fields, and no-self-test boundary agree |
| `git diff --check -- Stage1_Instances/THM-M-1389` | 0 | no tracked whitespace diagnostics |
| `git diff --no-index --check -- /dev/null` for each new blocker file | 1 each | expected added-file difference status; no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The historical intake checker is frozen to its original authority bytes and nine-file intake
inventory. Integration subsequently changed the intake state to `[_]`, so replay already fails at
that state assertion. Adding these blocker artifacts also makes the original inventory historical.
This statement attempt records that limitation rather than rewriting intake evidence or an
authoritative state file to manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must master-accept the intake dependency before it can accept a future
statement transition. Accountable reviewers must preserve and hash one lawful immutable primary
or authoritative source, resolve the 1911 announcement, 1912 PDE source, and catalog ODE placement,
select and independently approve one exact result, and transcribe every incorporated definition,
ordered binder, hypothesis, conclusion, proof boundary, correction, translation, and boundary
case. The decision must explicitly map or reject the multidimensional counting, inverse
eigenvalue, geometric or elliptic, and one-dimensional Sturm-Liouville variants.

A fresh statement worker can then encode precisely that source-selected claim, minimize pinned
imports, serialize and hash its elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, node-specific completion receipt,
worker `[_]`, or master acceptance is claimed.
