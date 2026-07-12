# Exact-statement gate: blocked

Item: `S56-M-1428-STATEMENT`

Theorem: `THM-M-1428`

Base revision: `a4c7dbb600e52683335f2d2fdce53507a6a71422` (tree
`4e208cb1f379cd8fbfcca0c9860db5b5df0a3dd6`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1428-INTAKE` has a provisional worker
receipt but no master-accepted receipt. Independently, the exact Lean 4 target cannot be truthfully
elaborated from the authoritative repository record. The entire mathematical record is the object
label `Julia集` ("Julia set"), Gaston Julia, 1918, and the gloss `复动力学的排斥集` ("the repelling
set of complex dynamics"). It supplies no truth-valued proposition, bibliography, exact source
passage, definitions, ordered binders, hypotheses, conclusion, proof boundary, or errata. The
catalog status `已验证` is explicitly untrusted under rev-5.6.

A Julia set is relative to a selected dynamical map and ambient space. The record does not choose
any of the proposition-changing data required by the statement gate:

- a polynomial, rational self-map of the Riemann sphere, or another holomorphic or meromorphic map,
  including its coefficient field, degree, and exceptional cases;
- the complex plane, extended complex plane, or Riemann-sphere model, its topology or spherical
  metric, and the treatment of infinity, poles, critical points, and exceptional points;
- non-normality of the iterate family, the complement of a Fatou set, the closure of repelling
  periodic points, the boundary of a filled Julia set, or another definition of the Julia set;
- all iterate, normal-family, periodicity, minimal-period, multiplier, repelling, closure, and
  boundary conventions used by the selected definition; or
- one exact conclusion, such as an equality between definitions, density, nonemptiness,
  perfectness, invariance, a boundary identity, or a result for one concrete map.

These alternatives are not interchangeable until a source fixes their definitions and the
hypotheses under which any equivalence is asserted. Boundary choices also change the claim: degree
zero or one, the identity and Mobius cases, infinity and poles, period zero versus positive or
minimal period, strict multiplier norm greater than one, empty or whole-space candidate sets, and
affine versus spherical boundary conventions all remain open.

Selecting a standard characterization from memory, choosing the Julia set of `z |-> z^2`, or
repackaging a desired property as a structure field would invent or substitute mathematics.
Neighboring targets separately own complex dynamical systems (`THM-M-1427`), Fatou sets
(`THM-M-1429`), Mandelbrot sets (`THM-M-1430`), and the Douady-Hubbard, Yoccoz, Sullivan, and
McMullen results. None may replace this target merely because it is easier to state.

Section 5 of the rev-5.6 blueprint makes statement ambiguity and a missing expression fingerprint
hard blockers. There is consequently no canonical expression on which to certify minimal target
imports, checked alternate transports, or removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations. Those tests are undefined, not passed. The
first failed substantive gate is exact source-statement identity, and the root remains
`[H5, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` directly imports `Mathlib.Analysis.Analytic.Basic`,
`Mathlib.Analysis.Complex.Basic`, `Mathlib.Dynamics.PeriodicPts.Defs`, and
`Mathlib.Topology.Closure`. It successfully re-elaborates adjacent complex, analytic, iterate,
periodic-point, closure, and frontier interfaces. The probe states no target theorem. Its imports
are discovery candidates only and cannot be called minimal for a target that does not exist.

A bounded source-name search of pinned mathlib found no `Julia`, `Mandelbrot`, or queried
complex/rational/holomorphic-dynamics declaration in Lean sources. This is narrow feasibility
evidence, not the downstream anchor audit and not proof of global absence.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The SHA-256 values of `lean-toolchain`,
`lake-manifest.json`, and `IntakeProbe.lean` are, respectively,
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`,
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`, and
`ca6e8124114d919992d4578dde29dd77009b773c8409c8ddef313ee611a0e9c2`.

The worker clone's pre-existing `Formalizations/Lean/.lake` link points to the canonical pinned
artifacts and was used read-only. No `lake update`, `lake build`, dependency clone or fetch, or
other `.lake` mutation was run.

## Validation Evidence

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1428` | 0 | rank 926, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all && git rev-parse HEAD && git rev-parse HEAD^{tree}` | 0 | before statement edits, only the pre-existing untracked `.lake` link was present; base revision and tree are recorded above |
| `rg -n -C 5 'Julia集\|复动力学的排斥集' Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md Docs/Stage1_Targets_rev-5.6.json Stage1_Instances/THM-M-1428/instance.json Stage1_Instances/THM-M-1428/source-statement-crosswalk.md` | 0 | found the object label and repelling-set gloss, neighboring references to Julia sets, and the intake's explicit null target; Stage0 leaves exact definitions and premises open |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 and Lake 5.0.0 at the revisions above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD && git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD^{tree} && git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | pinned mathlib revision and tree recorded above; empty status output confirms the package worktree is clean |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Stage1_Instances/THM-M-1428/IntakeProbe.lean Docs/Stage1_Targets_rev-5.6.json Docs/Stage1_Blueprint_rev-5.6.md skills/execute-stage1-rev56/SKILL.md` | 0 | environment and authority inputs were fingerprinted; values are recorded in the structured blocker |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1428/IntakeProbe.lean` | 0 | ten adjacent pinned interfaces elaborated; no canonical target was stated |
| `cd Formalizations/Lean && rg -n -i --glob '*.lean' '\bjulia\b\|\bmandelbrot\b\|complex[ -]dynam\|rational[ -]dynam\|holomorphic[ -]dynam' .lake/packages/mathlib/Mathlib` | 1 | expected no-match exit; discovery-only feasibility evidence, not an anchor audit |
| `python3 Stage1_Instances/THM-M-1428/check_intake.py` | 1 | known intake-only checker failure: it requires the intake worker's now-absent root self-test manifest; this statement run does not recreate or rewrite intake evidence |
| `python3 -m json.tool Stage1_Instances/THM-M-1428/statement-blocker.json` | 0 | structured blocker parsed as JSON |
| `jq -e '.item_id == "S56-M-1428-STATEMENT" and .theorem_id == "THM-M-1428" and .execution_rank == 926 and .verdict == "blocked" and .state == "[ ]" and (.statement_gate_passed == false) and (.canonical_statement == null) and (.canonical_formal_target == null) and (.minimal_imports == null) and ([.statement_gate.mutation_tests[]] \| all(. == "not_meaningful_without_a_canonical_statement")) and (.root_vector == {"H":"H5","M":"M4","R":"R4"}) and (.statement_elaborated == false) and (.theorem_complete == false) and (.gate_state == "blocked_no_worker_selftest")' Stage1_Instances/THM-M-1428/statement-blocker.json` | 0 | item identity, null target, four undefined mutations, unchanged debt vector, false completion flags, and no-self-test boundary agree |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)\b' Stage1_Instances/THM-M-1428` | 1 | expected no-match exit; no prohibited proof escape or declaration |
| `git diff --check -- Stage1_Instances/THM-M-1428` | 0 | no tracked whitespace diagnostics |
| `git diff --no-index --check -- /dev/null Stage1_Instances/THM-M-1428/statement-blocker.md` and likewise for `statement-blocker.json` | 1 each | expected added-file difference status with no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | no self-test manifest exists because the exact-statement deliverable is blocked |

The historical `check_intake.py` already exits 1 at this integration base because it
unconditionally loads the intake worker's root self-test manifest, which was not retained. After
the blocker artifacts are added, its closed intake-only inventory would also be stale. This
statement run does not rewrite the intake manifest, receipt, checker, historical hashes, task DAG,
generated blueprint, or authoritative execution DAG to manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must first accept the intake dependency. Accountable reviewers must then
preserve and hash an immutable primary or authoritative source, select one exact truth-valued
proposition or definition-plus-theorem with a page or section locator, transcribe every
incorporated definition, ordered binder, hypothesis, conclusion, proof boundary, correction,
erratum, and boundary case, and justify why it represents `THM-M-1428` rather than a neighboring
target. A second qualified reviewer must approve the mapping.

A later statement worker can then encode that same claim with real Lean definitions, minimize its
pinned imports, serialize and hash the elaborated expression and environment, compile every
credited transport, and run all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the phase is not genuinely
self-tested to its completion gate, no `.stage1-worker-selftest.json` is emitted and no statement
receipt, worker `[_]`, or master acceptance is claimed.
