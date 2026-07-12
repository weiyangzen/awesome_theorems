# THM-M-1393 exact-statement gate: blocked

- Item: `S56-M-1393-STATEMENT`
- Base revision: `d3cbfa8941a8bcaafa3b8a690d1333f9643288ad` (tree
  `e912a107150c6f9c3fc096901412fce0337c7c01`)
- Attempt date: 2026-07-13 (Asia/Shanghai)
- Verdict: blocked; no statement receipt, worker `[_]`, or theorem-completion claim

## First failed gate

The prerequisite `S56-M-1393-INTAKE` has only provisional worker state `[_]`, not master-accepted
state `[x]`. Its receipt declares `accepted: false`, and its instance deliberately leaves the
canonical mathematical statement and Lean target null. This independently prevents acceptance of
the statement node.

The first statement-specific failure is exact source-statement and Fredholm-variant selection. The
repository record gives only the name "Fredholm alternative," Erik Fredholm, 1903, and the gloss
"solvability of linear boundary-value problems." It supplies no equation or differential order,
operator domain, interval, state and forcing spaces, coefficient regularity, boundary or adjoint
boundary conditions, compactness or Fredholm hypothesis, parameter, forcing quantifier,
homogeneous kernel, range or orthogonality convention, alternative branches, conclusion, or
boundary cases. Stage0 explicitly leaves exact definitions and premises open, and the catalog's
`verified` label is untrusted under rev-5.6.

These omissions distinguish materially different propositions: a differential boundary-value
alternative, an adjoint-kernel compatibility criterion, an identity-minus-compact theorem,
injectivity versus surjectivity, an integral-equation theorem, and a spectral alternative. The
historical 1903 paper is currently only a bibliographic source lead; no complete immutable edition,
exact result and incorporated-definition map, proof boundary, correction and translation audit, or
independent approval has been admitted. Choosing a conventional formulation would invent or
substitute mathematics rather than elaborate the received target.

The catalog also schedules the functional-analysis Fredholm alternative as `THM-M-0315` and
Fredholm integral equations as `THM-M-1161`. Generic boundary-value problems, Sturm-Liouville
theory, and Green functions belong to `THM-M-1383`, `THM-M-1384`, and `THM-M-1392`. Their scope and
evidence cannot be transferred into this target.

Sections 5 and 5.1 of the rev-5.6 blueprint make ambiguity and a missing expression fingerprint
hard blockers. There is consequently no honest canonical expression for which imports can be
proved minimal. No `Statement.lean`, exact expression, checked transport, or mutation fixture was
created. The removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations
are not runnable without fixed binders and premises. The root vector remains `[H1, M4, R4]`.

## Pinned Lean boundary

The existing `IntakeProbe.lean` re-elaborates with its two direct imports,
`Mathlib.Analysis.Normed.Operator.FredholmAlternative` and `Mathlib.Analysis.ODE.Basic`. All seven
checked interfaces pass. In particular, pinned mathlib supplies
`IsCompactOperator.hasEigenvalue_or_mem_resolventSet`, which says that a nonzero scalar is an
eigenvalue of a compact continuous linear endomorphism or belongs to its resolvent set. That is a
real compact-operator spectral theorem, not the unspecified ODE boundary-value theorem. The probe
defines no differential operator, boundary conditions, adjoint problem, Green reduction, or
source-faithful transport. Its imports therefore cannot be certified minimal for this target and
receive no statement or proof credit.

A bounded search found that pinned spectral theorem and adjacent repo-local planning or anchor
material, but no source-selected ODE boundary-value Fredholm alternative containing the missing
operator and boundary data. This is feasibility evidence only, not the downstream anchor audit or
a global absence claim.

The environment is Lean 4.29.0 at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No `lake update`, `lake build`, dependency
clone or fetch, or other `.lake` mutation was run.

## Validation record

Commands ran in this worker clone on 2026-07-13 (Asia/Shanghai). Structured argument and result
records are preserved in `statement-blocker.json`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1393` | 0 | rank 1003; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree are recorded above |
| scoped authority, source, manifest, DAG, and intake inspection plus input hashing | 0 | confirmed the family-only wording, null intake target, and unresolved variant selection; fingerprints are in the JSON artifact |
| `python3 -B Stage1_Instances/THM-M-1393/check_intake.py` | 1 | historical intake replay stopped at a stale blueprint receipt hash after integration; this phase did not rewrite intake evidence |
| pinned Lean, Lake, and mathlib revision/tree/status checks | 0 | Lean 4.29.0, Lake 5.0.0, expected mathlib revision/tree, clean package worktree |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1393/IntakeProbe.lean` | 0 | all seven adjacent APIs elaborated; no canonical target or proof body was declared; output SHA-256 `ed83cfc1...270f` |
| bounded Fredholm and boundary-value search | 0 | found the compact spectral theorem and adjacent material, but no source-selected ODE boundary-value target |
| prohibited-construct scan over owned Lean files | 1 expected | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| JSON parse, scoped blocker invariants, and whitespace checks | 0 | identity, null target, unchanged vector, false completion fields, exact path scope, and clean whitespace agree |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the completion gate failed |

## Retry condition and status boundary

The integration lane must first master-accept refreshed intake evidence. Accountable reviewers must
then preserve and hash one immutable primary or approved authoritative source, select and
independently approve one exact root theorem, and transcribe every incorporated definition,
ordered binder, hypothesis, conclusion, operator and differential convention, space and
regularity requirement, boundary and adjoint condition, compactness or Fredholm bridge, parameter,
alternative branch, and degenerate case. The decision must preserve the neighboring target
boundaries.

A fresh statement run can then encode precisely that claim, prove its pinned direct imports
minimal, serialize and hash its elaborated expression and environment, compile every credited
transport, and run all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; audit and theorem completion remain false; no debt
change is proposed. Because the exact-statement deliverable did not pass, no
`.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or master acceptance is claimed.
