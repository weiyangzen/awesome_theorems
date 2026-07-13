# Exact-statement gate: blocked

Item: `S56-M-0096-STATEMENT`

Theorem: `THM-M-0096`

Base revision: `250f9e73cbbb3ebd2da9d0cefff78f0ab8c0d056` (tree
`b6e8138c58e31e82f8209cb70fbc0fb253f3654a`).

## Decision

The statement item remains `[ ]`. Its prerequisite, `S56-M-0096-INTAKE`, has provisional worker
state `[_]`, not master-accepted state `[x]`. The intake receipt is explicitly unaccepted and
non-content-addressed and has no accepted receipt ID. It deliberately leaves both the canonical
mathematical statement and Lean target null. The provisional dossier can be inspected in dependency
order, but it cannot be treated as accepted statement authority.

Independently, the repository source cannot identify one exact proposition. Its complete claim is
the phrase `半单李代数的整基` ("an integral basis of a semisimple Lie algebra"), with the title
`谢瓦莱基定理`, attribution to Claude Chevalley, and year 1948. It supplies no bibliography,
theorem locator, formula, incorporated definitions, ordered binders, assumptions, exact conclusion,
proof boundary, correction history, boundary policy, or independent review. The catalog's
`verified` label is explicitly untrusted under rev-5.6.

The missing choices change the proposition rather than its notation:

- the scalar field, characteristic, algebraic closure or splitting assumptions, and finite
  dimensionality;
- simple versus semisimple scope and the Lean encoding of semisimplicity;
- a module basis with integer bracket constants, a normalized Chevalley basis, or a bracket-closed
  free `Z`-form whose scalar extension recovers the Lie algebra;
- the Cartan subalgebra, roots, positive and simple roots, coroots, signs, ordering, basis index, and
  coefficient embedding;
- the full root-vector bracket relations and their normalization;
- existence alone versus uniqueness, equivalence, or independence from choices; and
- the zero algebra, empty and reducible root systems, direct sums, nonsplitting fields, positive
  characteristic, and reductive algebras with center.

Selecting the familiar complex Chevalley-basis theorem, a more general characteristic-zero
variant, or a `Z`-form formulation would therefore add proposition-changing mathematics. Encoding
the desired basis as a structure field or hypothesis would instead assume the result. Both moves
are prohibited substitutions.

Section 5 of the rev-5.6 blueprint makes statement ambiguity and a missing elaborated-expression
fingerprint hard blockers. There is consequently no canonical expression for which minimal imports,
fixed binders and typeclass context, checked alternate transports, or removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations can be certified. Those mutation
tests are undefined, not passed. The root remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated using three direct imports:

- `Mathlib.Algebra.Lie.Basis`
- `Mathlib.Algebra.Lie.SerreConstruction`
- `Mathlib.LinearAlgebra.RootSystem.GeckConstruction.Basis`

Nine adjacent Lie-basis, crystallographic-root, Geck-construction, and Serre-construction
declarations elaborated. The probe defines no canonical target, transport, or proof body, so its
imports cannot be certified minimal for the absent target.

Pinned mathlib's `LieAlgebra.Basis` is explicitly weaker than a Weyl or Chevalley basis: the module
documentation says that further structure-constant axioms are required and lists both the stronger
definition and general semisimple existence theorem as TODOs. `RootPairing.GeckConstruction.basis`
constructs the weaker basis only for its particular Lie algebra built from irreducible reduced
crystallographic root data. `Matrix.ToLieAlgebra` constructs a Serre-relation quotient. Neither is
an existence theorem for an arbitrary semisimple Lie algebra, and no checked equivalence to the
received root is available.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink exposed the canonical pinned artifacts and was used read-only.
No `lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran from this worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0096` | 0 | rank 1113; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD`; `git rev-parse 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided untracked `.lake` symlink existed; base revision and tree appear above |
| `git blame -L 705,710 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD`; the corresponding tree and package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0096/IntakeProbe.lean` | 0 | nine adjacent declarations elaborated; complete stdout SHA-256 `4765c4f5a9fe359aadf00e1a433b812c2dea6a41f5e663f43e4091b561e38d81`; no target or proof body declared |
| bounded `rg` search for Chevalley/Weyl bases and `Z`-forms in repo-local Lean and pinned mathlib | 0 | only this target's probe and mathlib's explicit weaker-basis documentation/TODO matched; no terminal target declaration located; bounded discovery only |
| `python3 -B Stage1_Instances/THM-M-0096/check_intake.py` | 1 | historical intake replay stops at its assertion that the authoritative intake state is `[ ]`; integration now records provisional `[_]`; this known stale-intake failure is not statement evidence |

The structured blocker was also parsed and checked for item identity, null target/import/fingerprint,
unchanged debt, four undefined mutation classes, false completion flags, and the no-self-test
boundary. A prohibited declaration scan over the owned Lean probe found no `sorry`, `admit`,
`sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration. New-file and scoped whitespace
checks passed.

## Retry Condition And Status Boundary

Accountable reviewers must lawfully preserve and hash an immutable primary or authoritative source,
select and independently approve one exact theorem, and transcribe every incorporated definition,
ordered binder, hypothesis, conclusion, proof boundary, correction, erratum, and boundary case. They
must fix the scalar field and characteristic, finite-dimensional semisimple domain, Cartan and root
data, integrality and normalization convention, complete bracket relations, `Z`-form relationship,
choice dependence, and existence or uniqueness scope. The intake dependency must also be refreshed
and master-accepted.

A later statement run can then encode exactly that source model, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport, and
execute all four mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. No `.stage1-worker-selftest.json`,
statement receipt, worker `[_]`, accepted state, statement fingerprint, or proof credit is claimed.
