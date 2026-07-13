# Exact-statement gate: blocked

Item: `S56-M-0946-STATEMENT`

Theorem: `THM-M-0946`

Base revision: `d66b6e80968b53d5b99774584721ae8976f303a5` (tree
`aaa82721074fccea81033a9a18d21652af89f8e4`). Attempt date: 2026-07-13
(`Asia/Shanghai`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0946-INTAKE` is provisional worker state
`[_]`, not master-accepted state `[x]`; its receipt declares `accepted: false`, is not a terminal
content-addressed receipt, and has no accepted receipt ID. The intake checker is also bound to an
older base and execution-DAG row: replay against the current integrated row fails closed. Rev-5.6
section 10.2 permits this dependency-ordered blocker investigation while concurrency is enabled,
but master closure remains dependency ordered.

Independently and decisively, the exact-source-statement gate fails. The complete catalog claim is
the title `Green-Tao-Ziegler定理`, the Green/Tao/Ziegler attribution, the year 2006, and the gloss
`线性方程组在素数中的解` (solutions of systems of linear equations in the primes). It gives no
bibliography, formula, definitions, domains, binders, hypotheses, conclusion, proof boundary,
correction history, or formal artifact. Stage0 explicitly leaves those fields open.

The matching source family exposes materially different possible roots:

- Green and Tao's 2006 preprint *Linear Equations in Primes* gives a general finite-complexity
  affine-form asymptotic conditional on `GI(s)` and `MN(s)`;
- its Corollary 1.7 gives an unconditional result only for complexity at most two;
- its Theorem 1.8 gives a conditional von-Mangoldt-weighted matrix-equation asymptotic for
  solutions of `Ax = b`; and
- its Corollary 1.9 gives a qualitative existence consequence under local solvability.

Later Green-Tao-Ziegler work proves inverse-Gowers input used for an unconditional arbitrary
finite-complexity package, but that is later than the catalog date and represents a different
dependency and result boundary. The closest 2006 paper has only Green and Tao as authors. The
catalog does not choose one source, revision, result, conditionality, affine-form or matrix
encoding, prime or von-Mangoldt convention, local-factor normalization, asymptotic convention,
binder list, boundary case, or dependency boundary. Choosing and encoding one candidate now would
invent, narrow, broaden, or substitute proposition-changing mathematics.

Sections 5 and 5.1 of the rev-5.6 standard make statement ambiguity and a missing elaborated
expression fingerprint hard blockers. Without one approved canonical proposition, no exact Lean
expression exists for which direct imports can be certified minimal. The expression and environment
fingerprints, checked alternate transports, and required removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations are undefined, not passed. No `Statement.lean`,
surrogate theorem, axiom, placeholder, broadened interface, or proof body was added. The root remains
`[H1, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with the pinned environment. Its four direct
imports expose eight adjacent prime-counting, von Mangoldt, generic affine-map, and linear-map
interfaces. Complete stdout has SHA-256
`5b66078e382fd3068381d7f6f859826f23c376dcf96ced619fe01ee59029aa7e`; stderr is empty. Three
adjacent-library axiom reports contain only `propext`, `Classical.choice`, and `Quot.sound`.

The probe's own header marks it as discovery only. It defines no finite-complexity system,
complexity or local-factor predicate, canonical root, checked transport, or proof body. Its imports
therefore cannot be certified minimal for an absent target and receive no statement or proof credit.
A bounded exact-topic search found no Green-Tao-Ziegler, linear-equations-in-primes,
finite-complexity prime-pattern, generalized Hardy-Littlewood, inverse-Gowers, or nilsequence root
declaration in the selected repository-local and pinned-mathlib Lean roots. This is narrow
feasibility evidence, not the downstream anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink points to the canonical pinned artifacts and was used read-only.
No `lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran in this isolated worker clone on 2026-07-13 (`Asia/Shanghai`), from the repository root
unless another working directory is shown.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0946` | 0 | rank 1485; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| `git blame -L 6910,6915 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| scoped authority, source, and intake inspection | 0 | the catalog does not select one source result; intake deliberately freezes a null canonical statement and Lean target |
| `sha256sum` over authority, source, intake, probe, toolchain, lockfile, and imported mathlib inputs | 0 | current fingerprints are recorded in `statement-blocker.json`; historical intake evidence was not rewritten |
| `python3 -B Stage1_Instances/THM-M-0946/check_intake.py` | 1 | historical intake replay stops at the changed canonical execution-DAG intake row; this phase records rather than rewrites frozen intake evidence |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| pinned mathlib revision, tree, and package-status checks | 0 | revision and tree agree with the fingerprint; the package worktree is clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0946/IntakeProbe.lean` | 0 | eight adjacent APIs elaborated; stdout hash above; no canonical target or proof body |
| bounded exact-topic `rg` search over repository-local and pinned-mathlib Lean | 1 (expected no match) | no target-specific declaration matched the recorded terms; discovery-only evidence |
| prohibited Lean construct scan over the owned path | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |

Final JSON parsing, scoped invariant, whitespace, and absent-self-test checks are recorded in the
structured blocker beside this report.

## Retry Condition And Status Boundary

The integration lane must first master-accept fresh intake evidence. Accountable reviewers must
then lawfully preserve one immutable source edition and independently select one exact truth-valued
result or explicitly typed package. They must crosswalk every incorporated definition, domain,
ordered binder, hypothesis, conclusion, affine or matrix encoding, complexity and nondegeneracy
condition, coefficient and range bound, prime and weight convention, local and archimedean factor,
asymptotic and quantifier convention, `GI`/`MN` dependency boundary, proof boundary, correction,
erratum, and degenerate case.

A fresh statement worker may then encode exactly that reviewed claim, minimize its pinned direct
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute the four required mutation classes.

This is a truthful first-gate blocker, not completion of the statement node or any downstream node.
Lifecycle remains `planned`; `audit_complete: false` and `theorem_complete: false`; no debt-vector
change is proposed. Because the exact-statement deliverable did not pass, no
`.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof credit, or master acceptance is
claimed.
