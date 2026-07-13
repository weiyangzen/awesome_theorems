# Exact-statement gate: blocked

Item: `S56-M-0040-STATEMENT`

Theorem: `THM-M-0040` (Amitsur-Levitzki theorem)

Base revision: `72e9e8092182121a6794921f61fcc9cae22f726d` (tree
`0d6c1fdf06d1573c256af331c6b198e5a787af43`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0040-INTAKE` has only provisional
worker state `[_]`, not master-accepted state `[x]`. The intake receipt declares `accepted: false`,
is non-content-addressed, and lists no accepted receipt ID. Dependency-ordered inspection is
possible, but an accepted statement transition still requires master acceptance of its intake.

Independently and decisively, the exact-statement gate cannot pass from the received claim. The
repository supplies only the Amitsur-Levitzki name, an inconsistent Shimshon Amitsur/Alexander
Levitzki attribution, the year 1950, and the gloss "matrix rings satisfy a polynomial identity."
It supplies no formula, exact proposition, matrix size or coefficient domain, ordered binders,
hypotheses, conclusion, boundary convention, bibliography, proof boundary, correction record, or
reviewer. Stage0 explicitly leaves the exact definitions and premises open.

The inspected 1950 paper by A. S. Amitsur and J. Levitzki does not remove the target-selection
ambiguity. Formula (2) and Theorem 1 give the standard identity over the paper's underlying field;
Theorem 2 combines it with a lower bound to obtain a minimal-degree result and a uniqueness clause;
later theorems treat broader classifications, characteristic-two exceptions, and other algebras.
The sparse catalog gloss does not select the identity alone, minimality, uniqueness, or a
conjunction. The paper is an `H1` source lead because target-clause ownership, the Alexander/J.
Levitzki discrepancy, correction and errata review, durable source admission, complete source-node
mapping, and independent approval remain open.

The following proposition-changing decisions are therefore unresolved:

- the paper's field scope versus a later arbitrary-commutative-ring generalization;
- positive `n`, fixed `n`, or a theorem over every size, and `Fin n` versus another finite index;
- an evaluated alternating matrix identity versus an equality in a free noncommutative polynomial
  algebra, including sign casts, permutation action, and ordered-product convention;
- standard identity alone versus lower-degree minimality or uniqueness/classification; and
- `n = 0`, `n = 1`, zero rings, characteristic two, finite fields, empty products, repeated
  arguments, and other boundary cases.

Selecting the familiar evaluated `S_(2n)` identity now would invent missing scope. Adding
minimality or uniqueness, silently generalizing fields to commutative rings, or replacing the
target with Cayley-Hamilton, Hopkins-Levitzki, a determinant alternation lemma, or a special case
would likewise broaden, narrow, or substitute the received theorem.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing expression
fingerprint hard blockers. There is no canonical expression whose imports can be certified
minimal, no approved alternate encoding to transport, and no meaningful removed-hypothesis,
changed-domain, changed-binder-scope, or boundary-case mutation. Those four mutation classes are
undefined, not passed. No `Statement.lean`, theorem declaration, assumed interface, axiom,
placeholder, or proof body was introduced. The root remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` uses three direct imports:

```lean
import Mathlib.GroupTheory.Perm.Sign
import Mathlib.Data.Matrix.Mul
import Mathlib.Algebra.BigOperators.Group.List.Defs
```

A fresh pinned replay elaborated nine adjacent permutation, sign, finite-sum, ordered-list-product,
and matrix-ring APIs. A bounded exact-topic search found no obvious Amitsur-Levitzki or standard-
polynomial declaration in repo-local Lean or pinned mathlib. The probe defines no standard
polynomial or canonical target, checked source transport, or proof body. Its imports therefore
cannot be certified as minimal imports for an absent target and receive no statement or proof
credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The probe's complete stdout was 954 bytes with
SHA-256 `a1bf44b428058428f702d1fa276b1099bed27b8fb0f3309affdf401f803d7db6`.

The automation-provided `Formalizations/Lean/.lake` symlink to the canonical pinned artifacts was
used read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake`
mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`). Lean commands ran
from `Formalizations/Lean`; all others ran from the repository root unless noted.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0040` | 0 | rank 1518; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| `sha256sum` over authority, source, intake, toolchain, lockfile, and relevant pinned mathlib inputs | 0 | exact current digests are recorded in `statement-blocker.json` |
| `git blame -L 305,310 --porcelain Docs/researches/math_theorems.md` | 0 | all six sparse catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| mathlib revision, tree, and package-status checks | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0040/IntakeProbe.lean` | 0 | nine adjacent APIs elaborated; stdout hash recorded above; no canonical target or proof body |
| bounded exact-topic `rg` over repo-local Lean and pinned mathlib | 1, expected no match | no obvious target declaration found; discovery-only evidence |
| `python3 -B Stage1_Instances/THM-M-0040/check_intake.py` | 1 | historical intake replay stops at line 137 because it expects authoritative intake state `[ ]`, while integration now records `[_]`; the historical checker was not rewritten |
| prohibited-construct scan over owned Lean | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |

The finalized JSON parse, scoped blocker invariants, standard replay, change-scope check, whitespace
checks, and absent-self-test check are recorded in the structured blocker. The intake checker
freezes intake-time authority and its original file inventory; this phase does not rewrite it, the
intake receipt, the generated checklist, or the authoritative execution DAG to manufacture
agreement.

## Retry Condition And Status Boundary

The integration lane must revalidate and master-accept the intake dependency. Accountable source
reviewers must preserve and hash a lawful immutable primary or approved authoritative source,
resolve the Alexander/J. Levitzki attribution and earlier lower-bound dependency, select and
independently approve one exact proposition, and map every incorporated definition, ordered binder,
hypothesis, conclusion, proof boundary, correction, erratum, and degenerate case. They must freeze
the identity/minimality/uniqueness boundary, coefficient and size scope, index model, sign and
product conventions, evaluation representation, characteristic assumptions, and foundation,
TCB, and computation profiles.

A fresh statement worker can then encode precisely that reviewed claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof
credit, or master acceptance is claimed.
