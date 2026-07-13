# Exact-statement gate: blocked

Item: `S56-M-0939-STATEMENT`

Theorem: `THM-M-0939`

Base revision: `f3910e9d9c9dde383801913343b9244462e6173a` (tree
`28f0e995eac01d75999b013a02e02eb792c07754`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0939-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. The intake receipt is unsigned, non-content-addressed,
declares `accepted: false`, has no accepted receipt ID, and deliberately leaves the canonical
mathematical statement and Lean target null. Its blueprint input hash is also stale after the
integration lane regenerated the checklist. Dependency-ordered investigation is possible, but
these facts independently prevent an accepted statement transition.

The repository record does not determine one truth-valued Kemperman proposition. It gives the name,
Johannes Kemperman, the year 1960, and only `阿贝尔群上子集和的结构` (structure of subset sums in
abelian groups). That gloss is identical to the neighboring Kneser entry and supplies no
bibliography, definition, binder, hypothesis, conclusion, correction history, or formal artifact.
The catalog's `已验证` label is untrusted under rev-5.6.

The intake finds a precise theorem family, but not a canonical member. J. H. B. Kemperman's *On
small sumsets in an abelian group*, *Acta Mathematica* 103 (1960), 63-88, is the matching primary
bibliographic candidate; its theorem body has not been admitted and mapped at theorem resolution.
The inspected modern sources provide two materially different roots:

- Lev, arXiv `math/0508179v2`, Theorem C, gives a pair-form characterization using finite nonempty
  sets, the small-sumset inequality, Kemperman's aperiodic-or-unique condition, an elementary
  residual pair, a nonzero subgroup, quotient cardinality, and a unique quotient representation.
- Boothby, DeVos, and Montejano, arXiv `1301.0095v2`, Theorem 4.5, gives a recursive classification
  of maximal nontrivial critical trios by a finite descending chain of impure beat/chord
  continuations ending in a pure beat or chord.

The intake explicitly admits neither root and establishes no original-to-modern or pair-to-trio
equivalence. Choosing the shorter trio theorem, the pair theorem, or an unreviewed package would
invent or substitute proposition-changing mathematics. The Kemperman-Scherk inequality, Kneser's
theorem, Vosper's theorem, and Cauchy-Davenport are distinct results and cannot replace the target.

The unresolved definition chain is substantive: finite pairs versus finite/cofinite trios;
criticality and deficiency; periods and stabilizers; representation multiplicity; all four
elementary-pair types; pure and impure beats and chords; maximality, similarity, continuation,
quotients, and termination; `Set`/`Finset` transports; ordered binders; and degenerate cases. Until
an immutable source root and these conventions are independently approved, there is no honest
canonical expression whose imports can be minimized or whose expression/environment fingerprint
can be serialized.

Sections 5 and 5.1 make statement ambiguity and a missing expression fingerprint hard blockers.
There is likewise no approved alternate encoding for a checked transport and no canonical target
against which the required removed-hypothesis, changed-domain, changed-binder-scope, and
boundary-case mutations can run. Those four mutation results are undefined, not passed. No
`Statement.lean`, axiom, placeholder, circular witness, weakened special case, or broadened theorem
was introduced. The root remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` re-elaborates using two direct imports:

- `Mathlib.Algebra.Pointwise.Stabilizer`
- `Mathlib.Combinatorics.Additive.CauchyDavenport`

It checks six adjacent Cauchy-Davenport and additive stabilizer signatures. All checks pass in the
pinned environment. The probe defines no critical pair or trio, elementary type, beat, chord,
continuation, canonical target, checked source transport, or proof body. Its imports therefore
cannot be certified as minimal imports for an absent target and receive no statement or proof
credit.

A bounded exact-topic search over pinned mathlib and repository-local Lean found no Kemperman,
Scherk, critical-pair/trio, or beat/chord match. This is discovery-only feasibility evidence, not
the downstream immutable anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No `lake update`, `lake build`, dependency
clone or fetch, or other dependency mutation was run.

## Validation Record

Commands ran in this isolated worker clone on 2026-07-13 (`Asia/Shanghai`). Exact executable
arguments, results, hashes, and boundaries are preserved in `statement-blocker.json`.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0939` | 0 | rank 1478; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| scoped reads of the standard, skill, guidelines, manifest, catalog, Stage0 projection, execution DAG, and complete intake dossier | 0 | confirmed the null canonical target, distinct pair/trio roots, and unresolved proposition-defining choices |
| `git blame -L 6861,6866 -- Docs/researches/math_theorems.md`; current `sha256sum` over authority, source, intake, toolchain, lockfile, and relevant mathlib inputs | 0 | catalog provenance and exact current hashes are recorded in the structured blocker |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| pinned mathlib revision/tree and package-status checks | 0 | expected revision and tree; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0939/IntakeProbe.lean` | 0 | six adjacent signatures elaborated; combined output SHA-256 `896394b18678fc9f20456f3e056b1859ba0771a0dfe4dc07b58aa6593901e8ff`; no target or proof body |
| bounded exact-topic search in pinned mathlib and repo-local Lean | 1 (expected no match) | no exact-topic match; discovery-only evidence |
| `python3 -B Stage1_Instances/THM-M-0939/check_intake.py` | 1 | historical intake validator failed closed on its stale blueprint input hash after checklist regeneration; it was not rewritten or represented as statement evidence |
| prohibited-construct scan over owned Lean | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, axiom, constant, opaque, or unsafe declaration |

Final JSON parsing, blocker invariant checks, whitespace checks, and the absent-self-test check are
also recorded in the structured blocker after finalization.

## Retry Condition And Status Boundary

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must
lawfully preserve and hash one immutable primary or approved authoritative source; select and
independently approve Kemperman's original pair form, Lev Theorem C, Boothby-DeVos-Montejano
Theorem 4.5, or one explicit equivalent package; and transcribe every incorporated definition,
ordered binder, hypothesis, conclusion, proof boundary, correction, erratum, pair/trio transport,
finiteness convention, and boundary case.

A fresh statement worker can then encode precisely that reviewed claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
