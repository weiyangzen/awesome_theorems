# Exact-statement gate: blocked

Item: `S56-M-0641-STATEMENT`

Theorem: `THM-M-0641`

Base revision: `a07fc18923e20fd2876d04809a15d5b31e55512f` (tree
`1268491c8f2677e1c8e38754fa93dd190892e69e`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0641-INTAKE` has provisional state `[_]`
in the execution DAG, but no accepted receipt. Rev-5.6 section 10.2 permits this dependency-ordered
statement attempt while acceptance remains pending. Independently, the exact Lean 4 target cannot
be truthfully elaborated from the authoritative repository record.

The complete claim-bearing catalog record gives the name `莱夫谢茨不动点定理`, Solomon Lefschetz,
the year 1926, and only the gloss `莱夫谢茨数与不动点` ("the Lefschetz number and fixed points").
It supplies no cited theorem or page, incorporated definitions, ordered binders, hypotheses,
conclusion, proof boundary, corrections, or errata. Stage0 explicitly leaves precise definitions
and premises open, and the catalog's `已验证` status is untrusted under rev-5.6.

The gloss identifies a classical theorem family, but it does not select any of the
proposition-changing data required by the statement gate:

- the admissible space class, such as a finite simplicial complex, compact polyhedron, finite CW
  complex, compact ENR, or another source-defined class;
- a simplicial or continuous self-map and its representation, continuity, approximation, and
  invariance assumptions;
- homology or cohomology, the coefficient ring or field, and the finite-dimensional and
  finite-support hypotheses needed for traces and the alternating sum;
- integral, rationalized, reduced, or unreduced conventions, including the degree-zero term and
  alternating-sign normalization;
- a nonzero-Lefschetz-number implication, a coincidence theorem, or a stronger global/local
  fixed-point-index formula; and
- all universes, typeclasses, binder order, and empty, disconnected, zero-dimensional, torsion,
  identity-map, constant-map, zero-number, and nonisolated-fixed-set cases.

These choices yield materially different propositions. Selecting a familiar compact-polyhedron,
finite-complex, finite-CW, or index-formula version would add or substitute mathematics absent from
the record. The 1926 and 1937 primary-source leads recorded at intake do not resolve the choice:
neither primary text, an exact proposition and definition chain, the relationship between the two
papers, nor an independent source review has been accepted.

Section 5.1 therefore fails at exact source-statement identity before proof evidence may be
inspected. There is no canonical expression on which to certify minimal imports, serialize an
expression fingerprint, compile checked alternate transports, or run the required removed-
hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations. Those tests are
undefined, not passed. The root remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` directly imports
`Mathlib.AlgebraicTopology.SingularHomology.Basic`, `Mathlib.Dynamics.FixedPoints.Basic`, and
`Mathlib.LinearAlgebra.Trace`. It re-elaborates six adjacent singular-chain, singular-homology,
topological-singular-set, linear-trace, and fixed-point interfaces. It defines neither a
Lefschetz number nor a target theorem. Its imports are discovery candidates and cannot be called
minimal for an absent canonical target.

A bounded source search of the repo-local Lean tree and pinned mathlib found unrelated Lefschetz
principle and fixed-point results, plus separately owned legacy topic artifacts, but no classical
Lefschetz fixed-point target. This is narrow feasibility evidence, not the downstream anchor audit
and not a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided `.lake` link to canonical
pinned artifacts was used read-only. No update, build, clone, fetch, or dependency mutation was
run.

## Validation Evidence

Commands ran in this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0641` | 0 | rank 1058, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` before edits | 0 | only the pre-existing automation `.lake` link was untracked; base revision and tree are recorded above |
| repository search for the theorem ID, Chinese name and gloss, and English name | 0 | found only the sparse catalog/Stage0 record and the intake's explicit null target; Stage0 leaves exact definitions and premises open |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| SHA-256 over authority, intake, toolchain, dependency-lock, and probe inputs | 0 | exact digests are recorded in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0641/IntakeProbe.lean` | 0 | six adjacent pinned APIs elaborated; no canonical statement or proof body was declared |
| bounded topic search in repo-local and pinned mathlib Lean sources | 0 | unrelated Lefschetz-principle, other fixed-point, and legacy-topic hits only; discovery evidence, not an anchor audit |
| `python3 -B Stage1_Instances/THM-M-0641/check_intake.py` | 1 | historical intake checker freezes its original execution item as `[ ]`, while current authority records provisional `[_]`; it fails before its now-historical nine-file inventory check |
| `python3 -m json.tool Stage1_Instances/THM-M-0641/statement-blocker.json` and scoped blocker assertions | 0 | identity, dependency state, null target/imports, four undefined mutations, unchanged vector, false completion flags, and no-self-test boundary agree |
| prohibited-construct scan over owned Lean files | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| scoped byte-level whitespace checks and `git diff --check -- Stage1_Instances/THM-M-0641` | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | no self-test manifest exists because the exact-statement deliverable is blocked |

The intake checker is a historical intake-only validator. The integration lane changed the intake
execution item from `[ ]` to provisional `[_]` without rewriting that checker, so its replay already
fails before considering the two statement artifacts. This statement run does not rewrite the
intake manifest, receipt, checker, task DAG, generated blueprint, or authoritative execution DAG to
manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must accept the intake dependency through a valid receipt. Accountable
reviewers must then preserve and hash an immutable primary or authoritative source, select one
exact proposition with a page or section locator, transcribe every incorporated definition,
ordered binder, hypothesis, conclusion, proof boundary, correction, erratum, and boundary case,
resolve the 1926-versus-1937 and implication-versus-index-formula choices, and independently
approve the mapping.

A later statement worker can then encode that same claim with real Lean definitions, minimize its
pinned imports, serialize and hash the elaborated expression and environment, compile every
credited transport, and run all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
