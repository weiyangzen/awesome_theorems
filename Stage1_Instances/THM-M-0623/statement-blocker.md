# Exact-statement gate: blocked

Item: `S56-M-0623-STATEMENT`

Theorem: `THM-M-0623`

Base revision: `561d83df037004ceb2259292d7c63be930b40391` (tree
`6eb02475bf5a70139d60615c924b31c930efc2bb`).

## Decision

The statement item remains `[ ]`. Its intake prerequisite is provisional worker state `[_]`, not
master-accepted state `[x]`. More importantly, the exact Lean 4 target cannot be truthfully selected
from the complete repository source record.

The catalog supplies only the title `乌雷松度量化定理` (Urysohn metrization theorem), the gloss
`第二可数正则空间可度量化` (a second-countable regular space is metrizable), an attribution to
Pavel Urysohn in 1925, and an untrusted `已验证` label. It does not define whether "regular"
includes T0, T1, or Hausdorff separation, whether "metrizable" means metric or pseudometric, the
compatible-structure encoding, ordered binders, or boundary cases. Stage0 explicitly leaves the
precise definitions and premises open.

The historical article locator does not resolve the ambiguity. The primary text was not available
to the intake worker, and no exact theorem passage, incorporated definitions, translation,
assumption map, proof boundary, correction or erratum disposition, or independent source review is
accepted. Choosing a familiar modern convention would therefore add, remove, or reinterpret a
material condition without source authority.

Pinned mathlib makes the difference concrete. Its `RegularSpace` does not include `T0Space`, and
its exact-topic Urysohn module supplies two inequivalent surfaces:

- `RegularSpace` plus `SecondCountableTopology` yields `PseudoMetrizableSpace`; and
- `T3Space` plus `SecondCountableTopology` yields `MetrizableSpace`, where `T3Space` includes
  `T0Space` and `RegularSpace`.

The unrestricted reading from bare mathlib `RegularSpace` to `MetrizableSpace` is false. The
existing probe checks a two-point indiscrete space that is regular and second-countable but is not
T0 or metrizable. Selecting the pseudometric surface would weaken a source-required metric
conclusion; selecting the T3 surface would silently strengthen the received regularity hypothesis.

There is consequently no canonical expression on which to certify minimal imports, serialize an
expression and environment fingerprint, check alternate encodings, or run the required
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations. These checks
are undefined, not passed. No `Statement.lean`, theorem declaration, proof body, axiom,
placeholder, assumed metrizability certificate, or altered target was added. The root remains
`[H1, M3, R4]`, and both audit and theorem completion remain false.

Rev-5.6 section 10.2 permits a dependency-ordered provisional attempt while concurrency is enabled,
but master closure remains dependency ordered. The intake receipt declares `accepted: false`, is
not content-addressed, and supplies no accepted receipt ID. Neither the intake nor this blocked
attempt receives master acceptance here.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` imports
`Mathlib.Topology.Metrizable.Urysohn`. In the pinned environment it re-elaborates both candidate
instances, their separation and countability interfaces, their inducing-map and embedding
constructions, and four two-point-indiscrete boundary examples. The declarations
`TopologicalSpace.PseudoMetrizableSpace.of_regularSpace_secondCountableTopology` and
`TopologicalSpace.metrizableSpace_of_t3_secondCountable` both report axioms
`[propext, Classical.choice, Quot.sound]`.

These surfaces establish formal feasibility and the non-substitution boundary only. The probe
declares no canonical target or proof body, and its import cannot be certified minimal until an
approved proposition selects a surface.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided `.lake` symlink was reused
read only. No update, build, clone, fetch, or dependency mutation was run.

## Validation Evidence

Commands ran in this isolated worker clone on 2026-07-13 (`Asia/Shanghai`). Lean commands ran from
`Formalizations/Lean`; other commands ran from the repository root unless noted.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0623` | 0 | rank 1317, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| pre-edit `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree are recorded above |
| scoped manifest, blueprint, skill, catalog, Stage0, intake, scope-map, crosswalk, and pinned-source inspection | 0 | the sources identify the theorem family but do not select one binder-complete proposition; intake deliberately leaves the canonical claim, target, import, and target fingerprints null |
| `python3 -B Stage1_Instances/THM-M-0623/check_intake.py` | 1 | the historical intake checker expects authoritative intake state `[ ]`; the current execution DAG records provisional `[_]`; this phase does not rewrite prior intake evidence |
| `lake env lean --version`, `lake --version`, and pinned mathlib revision/tree/status checks | 0 | Lean, Lake, and mathlib agree with the environment above; the mathlib package worktree is clean |
| `LC_ALL=C LANG=C NO_COLOR=1 lake env lean ../../Stage1_Instances/THM-M-0623/IntakeProbe.lean` | 0 | eleven interfaces and four indiscrete-space boundary examples elaborated; both candidate axiom reports are `[propext, Classical.choice, Quot.sound]`; stdout SHA-256 `0af3b056e401a08ca15f56f80bd2a6dec87b8b0ab34363b69bb0189d9e6baa4e`; no target or proof was declared |
| `python3 -m json.tool Stage1_Instances/THM-M-0623/statement-blocker.json` plus scoped assertions | 0 | blocker syntax, IDs, null-target boundary, unchanged vector, completion flags, mutations, hashes, changed paths, and absent-self-test invariants passed |
| prohibited-construct scan over owned Lean files | 1 | expected no-match: no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| scoped whitespace checks and `git diff --check -- Stage1_Instances/THM-M-0623` | 0 | both blocker artifacts passed text-hygiene checks; no tracked whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | no self-test manifest exists because the exact-statement deliverable did not pass |

## Retry Condition

The integration lane must master-accept refreshed intake evidence. An accountable reviewer must
preserve and hash one lawful immutable primary or authoritative source, select and independently
approve one exact proposition, and transcribe every incorporated definition, ordered binder,
hypothesis, conclusion, proof boundary, correction, erratum, translation, and boundary case. The
review must explicitly fix the regularity/separation convention, metric versus pseudometric
meaning, compatible-structure encoding, attribution/version boundary, and required transports.

A later statement worker can then encode exactly that approved claim, minimize pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport, and
run all four mutation classes.

This is a fail-closed blocker report, not completion of the statement node or any downstream node.
No statement receipt, worker `[_]`, proof, audit completion, theorem completion, or master acceptance
is claimed. Because the assigned deliverable did not pass, no `.stage1-worker-selftest.json` is
emitted.
