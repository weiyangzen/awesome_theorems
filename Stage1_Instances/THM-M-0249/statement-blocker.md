# Exact-statement gate: blocked

Item: `S56-M-0249-STATEMENT`

Theorem: `THM-M-0249`

Base revision: `bd81d4853a030765585ef6fed4310484ceb1e458` (tree
`fb92fc7476bff9a2ce8c20f1d7be34c6655ca6b4`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0249-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. Independently of that dependency, the intake leaves
the canonical human claim and Lean target null. The catalog supplies only Mergelyan's name, 1951,
and `紧集上连续函数的多项式逼近` ("polynomial approximation of continuous functions on compact
sets"). That sentence is not the standard true theorem: it omits the complex plane, connected
complement, complex codomain, and holomorphicity on the compact set's interior.

The inspected immutable secondary witnesses agree on the familiar family. Encyclopedia of
Mathematics revision `32115` says that for compact `K` in the complex plane with connected
complement, every function continuous on `K` and holomorphic at its interior points is uniformly
approximable on `K` by polynomials in `z`. Danielyan, arXiv:1501.00247v1, page 1, Theorem A states
the corresponding positive-epsilon form. They identify Mergelyan's 1951 and 1952 works, but no
primary text, exact theorem and incorporated-definition locator, translation/correction or errata
disposition, assumption map, or independent source approval is admitted in the dossier.

Even after selecting that family, proposition-changing Lean choices remain open:

- whether the complement is `IsConnected Kᶜ`, or nonempty plus `IsPreconnected Kᶜ`, and which
  source convention controls the empty-set boundary;
- whether `f` is an ambient `Complex -> Complex` function or a bundled map on the subtype `K`;
- whether interior holomorphicity is `DifferentiableOn Complex f (interior K)`,
  `AnalyticOnNhd Complex f (interior K)`, or a checked source-equivalent predicate;
- whether uniform approximation is a pointwise positive-epsilon proposition, a supremum-norm or
  closure statement, or sequential uniform convergence; and
- the exact quantifier order, strictness of the error bound, polynomial evaluation convention,
  and empty, singleton, finite, empty-interior, and constant-function cases.

Selecting the textbook epsilon form from memory would add uncited clauses that the intake
expressly keeps open. Rev-5.6 section 5 makes unresolved statement identity and a missing expression
fingerprint hard blockers. There is therefore no canonical target for which minimal imports,
checked transports, or the four required statement mutations can be certified. Those mutation
tests are undefined, not passed. The vector remains `[H1, M4, R4]`.

## Pinned Lean Boundary

`IntakeProbe.lean` re-elaborates compactness, connectedness, continuity, interior, analytic,
polynomial-evaluation, continuous-map polynomial, real Weierstrass, and complex star-closure APIs.
It has the two direct discovery imports `Mathlib.Analysis.Analytic.Basic` and
`Mathlib.Topology.ContinuousMap.StoneWeierstrass`. The probe's successful output authenticates
adjacent interfaces only. In particular, complex Stone-Weierstrass after star closure includes
conjugation and is not Mergelyan's holomorphic-polynomial theorem. The probe neither selects a
source-faithful target nor supplies an expression fingerprint, source transport, statement
receipt, terminal proof body, or proof credit. Its imports cannot be certified minimal for a
canonical target that does not exist.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No `lake update`, `lake build`, dependency
clone or fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran from this worker clone on 2026-07-13 (Asia/Shanghai).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0249` | 0 | rank 1259; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | pre-edit status contained only the automation-provided `.lake` symlink; base revision and tree are recorded above |
| `git blame -L 1794,1799 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog fields originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| immutable source inspection | 0 | Encyclopedia revision `32115` and arXiv:1501.00247v1 page 1 agree on the standard family; both remain secondary statement leads, not admitted primary/H0 evidence |
| bounded repo-local and pinned-mathlib topic search | 1 | expected no exact-topic match; only adjacent real Weierstrass and complex star-closure results were found, and neither is credited as a substitute |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean 4.29.0 and Lake 5.0.0 at the revisions above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and `status --short` | 0 | pinned revision and tree recorded above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0249/IntakeProbe.lean)` | 0 | eleven adjacent API type reports elaborated; stdout SHA-256 `297e6dd65a55cb54bfc752cb25b0834af367be9130b08f851010b3d5acb3b7e4`; no target declared |
| `python3 -B Stage1_Instances/THM-M-0249/check_intake.py` | 1 | historical intake checker expects authoritative intake state `[ ]`; current authority records `[_]`; it was not rewritten as statement evidence |
| prohibited-construct scan over owned Lean files | 1 | expected no match for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declarations |
| `python3 -m json.tool Stage1_Instances/THM-M-0249/statement-blocker.json` and scoped invariant check | 0 each | blocker identity, null target/imports, undefined mutations, unchanged vector, false completion flags, and absent self-test agree |
| scoped `git diff --check` and no-index checks for both new files | 0 / 1 each | no whitespace diagnostics; no-index exit 1 is the expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because exact target elaboration did not pass |

The historical intake checker is frozen to intake-time authority and its original nine-file
inventory. Integration has since advanced the authoritative intake cursor from `[ ]` to `[_]`, and
this statement attempt adds two blocker files. Its fail-closed replay is recorded rather than
repaired by modifying historical intake evidence.

## Retry Condition And Status Boundary

The integration lane must first master-accept refreshed intake evidence. Accountable reviewers
must preserve and hash an immutable primary or approved authoritative source, pinpoint its theorem
and every incorporated definition, resolve translation, corrections and errata, map the complex
domain, connected complement, continuity, interior holomorphicity, positive-error quantifiers,
polynomial evaluation, and every boundary case, and independently approve the source-to-Lean map.

A later statement worker can then encode exactly that reviewed claim, minimize its pinned imports,
serialize and hash its elaborated expression and environment, compile every credited transport,
and run the removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
