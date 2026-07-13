# Exact-statement gate: blocked

Item: `S56-M-0236-STATEMENT`

Theorem: `THM-M-0236`

Base revision: `c2e294becadae6ce784f27ee69f2e8dbf57e0b30` (tree
`3f567e7f76b189432b73444354070c0ff75925b9`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0236-INTAKE` has provisional worker
state `[_]`, not a master-accepted receipt. Independently, no exact Lean 4 target can be truthfully
elaborated from the authoritative repository record. That record supplies only the title
`单值性定理` (monodromy theorem), an attribution to many mathematicians, a nineteenth-century date,
and the gloss `全纯函数沿曲线的解析延拓` ("analytic continuation of holomorphic functions along
paths"). It gives no bibliography, formula, incorporated definitions, ordered binders,
hypotheses, conclusion, proof boundary, correction history, formal artifact, or reviewer. Its
`已验证` label is explicitly untrusted under rev-5.6.

The intake identifies but deliberately does not choose between two standard branches:

- analytic continuations of one initial element along endpoint-fixed homotopic paths have equal
  terminal elements; and
- an element continuable along every path in a simply-connected domain determines a
  path-independent or global single-valued analytic branch.

These branches are related only after fixing substantial analytic and topological infrastructure;
they are not interchangeable received statements. The repository also leaves open the domain,
codomain, analytic-element or germ model, representative equivalence, basepoint and endpoint,
continuation predicate, path regularity, relative-homotopy convention, connectedness hypotheses,
ordered binders, conclusion, and all boundary cases. Selecting any of these from mathematical
memory would invent proposition-changing mathematics.

Section 5 of the rev-5.6 blueprint makes statement ambiguity and a missing expression fingerprint
hard blockers. There is consequently no canonical expression for which minimal imports, checked
alternate transports, or removed-hypothesis, changed-domain, changed-binder-scope, and boundary
mutations can be certified. Those mutation tests are undefined, not passed. No `Statement.lean`,
statement receipt, or proof body was created. The root remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated using the pinned environment. Its sole direct
import, `Mathlib.Topology.Homotopy.Lifting`, exposes
`IsLocalHomeomorph.monodromy_theorem`, `SimplyConnectedSpace.paths_homotopic`, and
`IsCoveringMap.existsUnique_continuousMap_lifts`. The abstract theorem proves endpoint invariance
for a homotopy family of lifts through a separated local homeomorphism, and reports axioms
`[propext, Classical.choice, Quot.sound]`.

The theorem's docstring describes the intended application to the etale space of analytic germs,
but neither the probe nor the target dossier constructs that space, proves its projection is a
separated local homeomorphism, defines analytic continuation, or checks the continuation-to-lift
bridge. The theorem therefore remains adjacent pinned substrate. Treating it as the catalog's exact
analytic claim would substitute an abstract theorem and omit proposition-changing bridges. Its
one-module import is not certified minimal for a canonical analytic target that does not yet exist.

A bounded search over repo-local Lean and pinned mathlib found the exact analytic-germ application
wording only in this abstract theorem's docstring; other matches concern unrelated special-function
continuations or unrelated monodromy data. This is narrow statement-feasibility evidence, not the
downstream anchor audit and not a proof of global absence.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided `Formalizations/Lean/.lake`
symlink was used read-only. No `lake update`, `lake build`, dependency clone or fetch, or other
`.lake` mutation was run.

## Validation Record

Commands ran from this worker clone on 2026-07-13 (Asia/Shanghai).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0236` | 0 | rank 1248; planned; `L0/rework_required`; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all && git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree are recorded above |
| `git blame -L 1703,1708 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sha256sum` over authority, source, intake, toolchain, probe, and pinned homotopy-lifting inputs | 0 | exact current hashes are recorded in `statement-blocker.json`; historical intake evidence was not rewritten |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 and Lake 5.0.0 at the revisions above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and `status --short` | 0 | pinned revision and tree recorded above; empty package status |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0236/IntakeProbe.lean` | 0 | three pinned topology declarations elaborated; stdout SHA-256 `0efdb83aabf8679f06ff10f26d3a099a69f3c78382c5756cafe4d13ed9b0efbc`; empty stderr; candidate axioms printed; no analytic target declared |
| bounded `rg` search for analytic-germ continuation and monodromy declarations | 0 | only the abstract theorem docstring supplied the exact analytic application wording; discovery-only result |
| `python3 -B Stage1_Instances/THM-M-0236/check_intake.py` (after adding blocker artifacts) | 1 | known intake-only inventory assertion: the frozen checker accepts exactly the original nine intake files; this statement run records but does not rewrite historical intake evidence |
| prohibited-construct `rg` scan over owned Lean files | 1 | expected no match: no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0236/statement-blocker.json` and scoped `jq -e` assertions | 0 each | blocker JSON parses; identity, null target/imports, undefined mutations, unchanged `H1/M4/R4`, false completion flags, and no-self-test gate agree |
| `git diff --check -- Stage1_Instances/THM-M-0236` and no-index checks for both new files | 0 / 1 each | no whitespace diagnostics; no-index exit 1 is the expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

## Retry And Boundary

The integration lane must first master-accept refreshed intake evidence. Accountable reviewers must
then preserve and hash an immutable primary or approved authoritative source, select one exact
homotopy-invariance or simply-connected single-valuedness proposition, transcribe all incorporated
definitions, ordered binders, hypotheses, conclusions, exceptional cases, proof boundary,
corrections, and errata, and independently approve the source-to-target mapping. They must also
freeze the analytic domain and germ model, continuation predicate, path and homotopy conventions,
connectedness assumptions, profiles, alternate encodings, and degenerate cases.

A later statement worker can then encode only that reviewed claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and run all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
