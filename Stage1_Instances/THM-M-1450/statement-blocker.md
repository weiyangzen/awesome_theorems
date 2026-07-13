# Exact-statement gate: blocked

Item: `S56-M-1450-STATEMENT`

Theorem: `THM-M-1450`

Base revision: `58fbed45d2c785466ee920c7696f0f7b3686d9a5` (tree
`36198f7c90045b3b21d338a3d0ce47aa4ff930f1`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1450-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. Rev-5.6 section 10.2 permits provisional preparation
of a later node, but the intake receipt declares `accepted: false`, contains no accepted receipt
ID, and explicitly leaves the canonical mathematical statement and Lean target null. Master
acceptance remains necessary before a future statement transition can be accepted.

Independently and decisively, the exact-statement gate cannot pass. The complete repository record
is the title `Power iteration`, attribution only to "many mathematicians" in the 20th century, and
the gloss `An iterative method for the largest eigenvalue.` It supplies no bibliography, formula,
domain, ordered binder, hypothesis, recurrence, exact conclusion, proof boundary, correction
history, or boundary convention. Its `verified` label is untrusted under rev-5.6.

Materially inequivalent theorem families fit that gloss. The input may be a finite real or complex
matrix or a linear operator, and it may be self-adjoint, normal, diagonalizable, positive, or more
general. "Largest" may mean largest algebraic value, greatest modulus, spectral radius, or a
dominant invariant subspace. A theorem may require a simple nonzero dominant eigenvalue, a strict
modulus gap, and a start with nonzero dominant projection, but none of those premises is selected.
The iteration may use raw powers or normalized vectors, with different indexing, norms, zero
conventions, and eigenvalue estimators. Its conclusion may be projective convergence, sign- or
phase-adjusted vector convergence, convergence of a Rayleigh quotient or norm ratio, residual
convergence, a geometric error bound, an asymptotic rate, iteration complexity, or finite-precision
correctness. Repeated or modulus-tied eigenvalues, defective operators, zero starts and iterates,
low-dimensional spaces, and exact versus floating-point arithmetic lead to different boundaries.

Choosing a familiar version from memory or promoting the secondary source lead would silently
resolve these open decisions. It would invent, narrow, broaden, or substitute proposition-changing
mathematics rather than elaborate the exact received target.

Sections 5 and 5.1 make statement ambiguity and a missing expression fingerprint hard blockers.
There is consequently no canonical expression for which minimal imports, a serialized elaborated
type, an environment fingerprint, checked alternate transports, or the required removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations can be certified. All four
mutation classes are undefined, not passed. No `Statement.lean`, theorem declaration, proof body,
weakened special case, or broadened interface was added. The root remains `[H5, M4, R4]`.

## Source And Lean Boundary

The intake inspected M. Gu's "Power Method" section in *Templates for the Solution of Algebraic
Eigenvalue Problems* (SIAM, 2000). The mutable Netlib HTML observed on 2026-07-13 has SHA-256
`541ab6f6f74f3ee1c28396d9b4828e3703c4220500fd7f2d44271122b0844070`. It describes a Hermitian
dominant-by-modulus method, a nonorthogonal-start condition, increasing parallelism, and rate
dependence on the two leading eigenvalue magnitudes. The repository does not cite or adopt it, and
no independent reviewer has admitted an immutable pinpoint proposition with all definitions,
assumptions, proof boundary, corrections, and boundary cases. It remains a discovery-only
secondary scope lead.

The existing `IntakeProbe.lean` imports
`Mathlib.Analysis.InnerProductSpace.Spectrum` and
`Mathlib.LinearAlgebra.Matrix.ToLin`. It checks twelve adjacent eigenspace, power, matrix-action,
and self-adjoint spectral-coordinate interfaces. These are possible ingredients only. The power
identity applies to a vector already assumed to be an exact eigenvector; the matrix and spectrum
APIs contain no selected recurrence, mixed-start decomposition, normalization, convergence, or
rate theorem. The two imports cannot be called minimal for a canonical target that does not exist.

A bounded search of repository-local Lean and pinned mathlib found no declaration named or
documented as power iteration, the power method, or convergence of a dominant-eigenvalue iteration.
One generic documentation line in `Spectrum.lean` mentions eigenvalues converging to zero and is
unrelated to the target. This is narrow feasibility evidence, not a downstream anchor audit or a
global absence claim.

The worker environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No dependency update, build, clone, fetch,
or other `.lake` mutation was run.

## Validation Record

Commands ran in this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1450` | 0 | rank 1127; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| exact `sed` reads of blueprint sections 5, 10.1-10.5, and the item rows, plus the catalog and Stage0 records | 0 | confirmed the statement gate, worker rules, method-only gloss, and explicitly open Stage0 fields |
| exact Python authority/null-target assertions over the target manifest, execution DAG, and `instance.json` | 0 | rank and dependency agree; statement state is `[ ]`; canonical claim, Lean target, and target fingerprint fields are null |
| `git blame -L 10588,10593 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `python3 -B Stage1_Instances/THM-M-1450/check_intake.py` | 1 | historical intake checker expects authoritative state `[ ]`; integration now records provisional `[_]`, so this phase records rather than rewrites stale intake evidence |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| mathlib `git rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1450/IntakeProbe.lean` | 0 | twelve adjacent APIs elaborated; stdout SHA-256 `5e5919ea5fd5e8ff67632b94cd691044a9e04439ab9a22c8aa093cb9629152ee`; no canonical target |
| bounded exact-topic search in repository-local Lean and pinned mathlib | 0 | only one unrelated generic Spectrum documentation line matched; no power-iteration declaration was located |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |

Final JSON, invariant, whitespace, and absent-self-test checks are recorded in the structured
blocker beside this report.

## Retry Condition And Status Boundary

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must
admit an immutable pinpoint source and independently select one exact proposition, including all
incorporated definitions and its proof boundary. That selection must fix the operator and scalar
domains, dimensions, dominance and multiplicity premises, starting-vector condition, recurrence,
normalization and zero behavior, estimator, convergence and rate conclusions, sign or phase,
arithmetic model, ordered binders, and boundary conventions.

A fresh statement worker can then encode precisely that reviewed claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
