# Exact-statement gate: blocked

Item: `S56-M-1460-STATEMENT`

Theorem: `THM-M-1460`

Base revision: `2a5d4172283e286ab471a929ea09dfe1eaab55cb` (tree
`1fbe559d4eb9b58c24b3f80d1e3ffc19a95907c0`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1460-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. Rev-5.6 section 10.2 permits provisional preparation
of this later node, but the intake receipt declares `accepted: false`, is not content-addressed,
contains no accepted receipt ID, and deliberately leaves the canonical mathematical statement and
Lean target null. Master acceptance remains necessary before any future statement transition can
be accepted.

Independently and decisively, the exact-statement gate cannot pass from the authoritative
repository record. The complete record is the title `谱方法` (`spectral methods`), attribution to
many mathematicians in the twentieth century, and the gloss `基于正交多项式的数值方法` ("numerical
methods based on orthogonal polynomials"). It supplies no bibliography, formula, definition,
ordered binder, hypothesis, conclusion, proof boundary, correction, erratum, or reviewer. The
catalog label `已验证` is untrusted metadata under rev-5.6.

Spectral methods are a numerical-analysis family, not one truth-valued proposition. Materially
inequivalent roots fit the gloss:

- weighted orthogonality or completeness of a Fourier, Chebyshev, Legendre, or other basis;
- best approximation, interpolation, projection, coefficient decay, or quadrature exactness;
- algebraic convergence under finite regularity or exponential convergence under analyticity;
- solvability, consistency, stability, convergence, or an error estimate for a Galerkin, tau,
  collocation, or pseudospectral discretization; and
- conditioning, aliasing, complexity, conservation, or finite-precision correctness of a solver.

The repository selects none of these. It also fixes no equation or operator, domain and boundary
conditions, scalar and function spaces, basis and weight, trial and test spaces, nodes, truncation,
regularity class, norm, constants and rate, arithmetic model, or degenerate cases. Neighbor targets
separately own the fast Fourier transform, finite element, Galerkin, Petrov-Galerkin, discontinuous
Galerkin, finite-difference, finite-volume, and spectral-element method families. Choosing a
convenient Chebyshev theorem, Fourier expansion, Weierstrass approximation result, or PDE scheme
would invent, narrow, broaden, or substitute proposition-changing mathematics.

Sections 5 and 5.1 make statement ambiguity and a missing expression fingerprint hard blockers.
There is consequently no canonical Lean expression for which imports can be certified minimal, no
serialized elaborated type or environment-expression fingerprint, no credited alternate transport,
and no meaningful removed-hypothesis, changed-domain, changed-binder-scope, or boundary-case
mutation. Those four mutation classes are undefined, not passed. No `Statement.lean`, theorem
declaration, proof body, weakened special case, or broadened interface was added. The root remains
`[H5, M3, R4]`.

## Source And Lean Boundary

The intake records Gottlieb and Orszag (1977), Canuto et al. (1988), Trefethen (2000), and Boyd
(2001) only as uncited method-family leads. No immutable edition, pinpoint theorem, incorporated
definition, assumption list, proof boundary, correction record, or independent review has admitted
one of them as the canonical source. They cannot select the missing proposition.

The existing `IntakeProbe.lean` re-elaborates with the pinned environment. Its three direct imports
expose nine adjacent interfaces for Chebyshev polynomials and weighted orthogonality, Chebyshev-Gauss
quadrature, an `L2` Fourier basis and expansion, and existential polynomial approximation. All nine
checks pass. Three representative imported theorems report only `propext`, `Classical.choice`, and
`Quot.sound`. None states a spectral discretization or target-specific convergence, error, or solver
correctness theorem. The probe's imports therefore cannot be certified minimal for an absent
canonical target and receive no statement, anchor, or proof credit.

A bounded exact-topic search of repository-local Lean and pinned mathlib found no declaration named
or documented as a spectral numerical method, spectral collocation, spectral Galerkin/tau method,
or pseudospectral method. This is narrow discovery evidence, not the downstream immutable anchor
audit or a global absence claim.

The worker environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The complete probe output has SHA-256
`764e3a18c3f5304e16bb3b6f8cfe3047b368e1a1186929182449ed2d53ae20fc`.

The automation-provided `Formalizations/Lean/.lake` symlink points to canonical pinned artifacts and
was used read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake`
mutation was run.

## Validation Record

Commands ran in this isolated worker clone on 2026-07-13 (`Asia/Shanghai`), from the repository
root unless another working directory is shown.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1460` | 0 | rank 1137; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| exact authority, catalog, Stage0, intake, scope, and crosswalk inspection | 0 | statement state is `[ ]`; the complete catalog record is a method-family gloss; intake deliberately leaves the canonical claim and formal target null at `[H5, M3, R4]` |
| `git blame -L 10658,10663 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sha256sum` over authority, intake, toolchain, lockfile, and inspected mathlib inputs | 0 | exact current fingerprints are recorded in `statement-blocker.json` |
| `python3 -B Stage1_Instances/THM-M-1460/check_intake.py` | 1 | historical intake replay stops at a stale blueprint input hash; its receipt and original nine-file inventory are intake-only evidence, so this phase records rather than rewrites them |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| pinned mathlib revision, tree, and package-status checks | 0 | revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1460/IntakeProbe.lean` | 0 | nine adjacent APIs elaborated; three axiom reports contained only the three principles above; no canonical target was declared |
| bounded exact-topic Lean search | 1 | expected no-match result; no target-specific spectral numerical-method declaration was located |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |

Final JSON, invariant, whitespace, and absent-self-test checks are recorded in the structured
blocker beside this report.

## Retry Condition And Status Boundary

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must
lawfully preserve and hash an immutable primary or approved authoritative source, select and
independently approve one exact truth-valued proposition, and map every incorporated definition,
binder, premise, conclusion, proof boundary, correction, and erratum. They must freeze the
problem/operator, domain and boundary data, basis and weight, scheme, spaces, nodes and truncation,
regularity, norm, constants and rate, arithmetic model, all boundary cases, and ownership boundaries
with the neighboring numerical-method targets.

A fresh statement worker can then encode precisely that reviewed claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
