# THM-M-1463 exact-statement gate: blocked

Item: `S56-M-1463-STATEMENT`

Base revision: `521bd42e5ab5e30513a3c2b7377ea4a1516c0d16` (tree
`6f3d9fcf297fe5251a1dc839c1e67930001a86fc`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1463-INTAKE` is provisional worker
state `[_]`, not master-accepted state `[x]`. The intake receipt has `accepted: false`, is not
content addressed, and contains no accepted receipt ID. Its historical checker also fails closed
because it expects the execution DAG's former `[ ]` intake state while the current authority records
`[_]`. This statement-only attempt does not rewrite that earlier evidence.

Independently and decisively, there is no exact mathematical target to elaborate. The entire
repository claim is the title `Petrov-Galerkin方法` and the gloss `推广的Galerkin方法` ("a
generalized Galerkin method"). A method-family name is not a truth-valued proposition. It does not
select:

- real or complex scalars, Banach or Hilbert trial and test spaces, universes, subspaces, or
  inclusion maps;
- a bilinear or sesquilinear convention, continuous or discrete variational problem, form,
  right-hand-side functional, or quantifier order;
- coercivity, primal and adjoint inf-sup conditions, a kernel condition, dimension compatibility,
  a Fortin operator, or another stability contract;
- existence and uniqueness, stability, quasi-optimality, best approximation, an a priori error
  estimate, convergence, a Fortin criterion, or a sourced conjunction; or
- norms, constants, approximation families, regularity and consistency assumptions, ordered
  binders, exact conclusion, and degenerate cases.

These choices change the theorem. Babuška's 1973 paper is only a bibliographic theorem-family lead:
the catalog does not cite it, and intake inspected no immutable theorem passage, exact assumptions,
proof boundary, corrections, source-to-target selection, or independent review. Choosing a
well-known Babuška estimate, Banach-Nečas-Babuška result, finite-dimensional solvability theorem,
Lax-Milgram specialization, or concrete finite-element scheme would therefore invent or substitute
mathematics. A structure or premise that stores the desired solution or estimate would be a
placeholder rather than a proof of a source-selected result.

Rev-5.6 sections 5 and 5.1 make statement ambiguity and a missing elaborated-expression fingerprint
hard blockers. There is no canonical Lean expression whose imports can be minimized, no canonical-
target environment fingerprint, and no approved alternate encoding to transport. The mandatory
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations are undefined,
not passed. The lifecycle remains `planned`, and the root vector remains `[H5, M4, R4]`. Here `H5`
classifies the catalog wording as unstable; it does not refute established Petrov-Galerkin results.

## Lean Boundary

The discovery-only `IntakeProbe.lean` was re-elaborated against the existing pinned environment. Its
three direct imports expose ten adjacent bilinear-map, Hilbert-subspace projection, coercivity, and
Lax-Milgram interfaces. The complete stdout SHA-256 was
`fca28174be61b20686a7db6249af514c234e66c209a8d2d81eab76db0f7919a3`.
Representative axiom reports name only `propext`, `Classical.choice`, and `Quot.sound`.

That probe declares no distinct trial/test-space problem, inf-sup condition, discrete solution,
stability or error conclusion, canonical target, checked source transport, or proof body. Its
imports cannot be certified minimal for an absent target and receive no statement or proof credit.
A bounded exact-topic search found no Petrov-Galerkin-, Babuška-, Nečas-, or
Banach-Nečas-Babuška-named declaration in pinned mathlib or repository-local Lean. This is limited
discovery evidence, not the downstream anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided canonical `.lake` symlink was
used read-only. No update, build, clone, fetch, or dependency mutation was run.

## Validation Record

Commands ran in this worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1463` | 0 | rank 1140; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| exact `python3 -c` authority/intake assertions recorded in `statement-blocker.json` | 0 | rank and dependency agree; intake is provisional `[_]`; statement is `[ ]`; canonical claim, target, imports, and fingerprints are null; root is H5/M4/R4 |
| `git blame -L 10679,10684 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `python3 -B Stage1_Instances/THM-M-1463/check_intake.py` | 1 | historical intake replay expects authority state `[ ]`; integration now records `[_]`; this known stale-intake failure is not statement evidence |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| mathlib `git rev-parse HEAD 'HEAD^{tree}'` and `git status --short` | 0 | pinned revision/tree recorded above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-1463/IntakeProbe.lean` | 0 | ten adjacent APIs elaborated; stdout digest recorded above; no target theorem |
| exact-pattern bounded topic `rg` command recorded in `statement-blocker.json` | 1 | expected no-match; no exact-topic terminal declaration; discovery only |
| exact-pattern prohibited-declaration `rg` command recorded in `statement-blocker.json` | 1 | expected no-match; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-1463/statement-blocker.json` | 0 | finalized blocker is valid JSON |
| exact `python3 -c` blocker assertions recorded in `statement-blocker.json` | 0 | identity, null target/import/fingerprints, unchanged vector, four undefined mutations, false completion flags, exact two-file scope, and no-self-test boundary agree |
| owned-file inventory and `git status --short --untracked-files=all` | 0 | exactly nine historical intake files plus two blocker files; only `.lake` and the two blocker files are untracked |
| scoped whitespace checks | 0 | no whitespace diagnostics in either blocker artifact |
| `test ! -e .stage1-worker-selftest.json` | 0 | no self-test manifest exists because the exact-statement deliverable did not pass |

## Retry Condition

The integration lane must first accept fresh intake evidence. Accountable reviewers must then
preserve an immutable source, independently approve one exact Petrov-Galerkin proposition, and map
its definitions, assumptions, proof boundary, corrections, and errata. The approved correction
must freeze the scalar field, trial and test spaces, inclusions, form convention, right-hand side,
continuous and discrete equations, stability assumptions, dimensions, approximation family, norms,
constants, ordered binders, conclusion, alternate encodings, neighbor boundary, and every
degenerate case.

A later statement run can encode only that approved proposition, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport, and
execute all four mutation classes.

This blocker is the assigned phase's truthful result, not completion of this node or a downstream
node. No statement receipt, root worker self-test packet, worker `[_]`, proof credit, anchor audit,
audit completion, theorem completion, or master acceptance is claimed.
