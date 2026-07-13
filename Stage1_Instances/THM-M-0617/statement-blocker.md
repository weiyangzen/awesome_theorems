# Exact-statement gate: blocked

Item: `S56-M-0617-STATEMENT`

Theorem: `THM-M-0617`

Base revision: `adc87f8ea24dcc7c5e2668c0a5ede0ca5c5f0f55` (tree
`3c83596059f716cde0d50a5f6b390ada6ca7c8e1`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the received source record. The
catalog gives only the title, a broad nineteenth-century attribution, and the gloss
`紧集的闭子集紧，连续像紧`: closed subsets of compact sets are compact, and continuous images of
compact sets are compact. It supplies no bibliography, theorem locator, definitions, ordered
binders, exact root packaging, proof boundary, errata record, translation, or independent source
review. Stage0 explicitly leaves precise definitions and premises open, and rev-5.6 treats the
catalog's `已验证` label as untrusted inventory metadata.

The omissions are proposition-changing. In particular, "closed subset of a compact set" can mean
a subset closed in the ambient space, as required by `IsCompact.of_isClosed_subset`, or a set
closed in the compact subspace. These encodings are not interchangeable without an explicit
subtype or relative-closedness transport when the compact set itself need not be ambient closed,
especially in a non-Hausdorff space. Likewise, "continuous image" does not decide global
`Continuous f` versus `ContinuousOn f s`, nor whether the domain and map are independently
quantified for the image branch. The comma does not select a Lean conjunction, a structure, or two
canonical child propositions plus a checked composition root.

The intake deliberately records all of these choices as open, leaves the formal module,
declaration, elaborated-expression hash, and canonical-target environment fingerprint null, and
names source identity and independent root composition as the statement blocker. Selecting the
familiar conjunction of `IsCompact.of_isClosed_subset` and `IsCompact.image` now would invent
scope and packaging decisions rather than elaborate an admitted exact proposition. Substituting
the more general local `ContinuousOn` theorem with its weaker hypothesis, adding `T2Space`, or
coupling both branches under one flat collection of assumptions would change the received claim.

Sections 5 and 5.1 of the rev-5.6 blueprint make ambiguity, unresolved binders, and a missing
expression fingerprint hard blockers. With no approved canonical proposition, no import can be
certified minimal for the target, no exact elaborated expression or environment-expression
fingerprint can be admitted, no alternate transport can be credited, and the required removed-
hypothesis, changed-domain, changed-binder-scope, and boundary mutations are undefined rather than
passed. No `Statement.lean`, axiom, placeholder, weakened special case, broadened theorem, or proof
body was introduced. The root remains `[H1, M3, R4]`.

The prerequisite `S56-M-0617-INTAKE` has provisional worker state `[_]`, not accepted state `[x]`.
Its receipt has `accepted: false`, is not content-addressed, and lists no accepted receipt ID.
Dependency-ordered preparation can inspect that dossier, but the statement transition cannot be
accepted until both the dependency and this node independently pass their gates.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with the pinned environment and the one direct
import `Mathlib.Topology.Compactness.Compact`. It confirms the exact types of `IsCompact`,
`IsCompact.of_isClosed_subset`, `IsCompact.image_of_continuousOn`, and `IsCompact.image`. Both
direct catalog-topic interfaces report only `propext`, `Classical.choice`, and `Quot.sound` in
their axiom output. The complete output SHA-256 is
`1ba2ff9c58728fdf189ec19105f478c2d8a96c20a12e514bb23e86c561484d75`.

This is real pinned interface evidence, but the probe declares no canonical root, checked source-
to-Lean transport, statement mutation, or proof body. The import is sufficient for the adjacent
interfaces; it is not certified as the minimal import for an absent canonical target.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symbolic link and pinned artifacts were used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0617` | 0 | rank 1311; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base revision and tree appear above |
| catalog, Stage0, manifest, blueprint, skill, intake dossier, scope map, crosswalk, and target-local DAG inspection | 0 | the received record does not select a binder-complete proposition, and intake deliberately leaves the exact root null |
| `git blame -L 4580,4585 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `rg -n '^theorem IsCompact\.(of_isClosed_subset\|image)(_of_continuousOn)?' Formalizations/Lean/.lake/packages/mathlib/Mathlib/Topology/Compactness/Compact.lean` plus the recorded target-local searches | 0 | lines 103, 107, and 121 are the ambient-closed, continuous-on, and global-continuous interfaces; no admitted source-identical composed root was found |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | pinned revision and tree recorded above; package status produced no output |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0617/IntakeProbe.lean` | 0 | four interfaces elaborated; both direct candidate axiom reports list `propext`, `Classical.choice`, and `Quot.sound`; output hash recorded above |
| `python3 -B Stage1_Instances/THM-M-0617/check_intake.py` | 1 | the historical intake checker expects intake authority state `[ ]` and attempts 0; current integration state is provisional `[_]` and attempts 1, so it fails before this phase and was not rewritten |
| prohibited-declaration scan over owned Lean files | 1 | expected no-match: no `sorry`, `admit`, `sorryAx`, axiom, constant, opaque, or unsafe declaration; diagnostic `#print axioms` is permitted |
| `python3 -m json.tool` plus scoped blocker identity, inventory, self-test-absence, newline, carriage-return, and trailing-whitespace assertions | 0 | the JSON parses; blocked identity and two-file inventory agree; no root self-test exists; both new files pass byte-level hygiene checks |
| `git diff --no-index --check /dev/null` on each new blocker file | 1 | expected content-difference exit for each new file; neither command emitted a whitespace diagnostic |

The intake checker is bound to intake-time authority hashes, its original state, and its original
artifact inventory. It is historical intake evidence, not a statement validator. This phase
records the stale-authority failure rather than modifying the intake manifest, receipt, checker,
target-local DAG, generated blueprint, or authoritative execution DAG to manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must master-accept the intake dependency before accepting a later statement
transition. Accountable reviewers must preserve and hash a lawful immutable primary or
authoritative source and independently approve one exact proposition with every incorporated
definition, ordered binder, hypothesis, conclusion, proof boundary, correction, erratum,
translation, and boundary case. In particular, they must decide ambient versus relative
closedness, global versus on-set continuity, independent branch binders, root packaging, universe
and topology conventions, and all non-Hausdorff and empty-set cases.

A fresh statement worker can then encode only that approved claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile each credited transport,
and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`,
master acceptance, statement fingerprint, or proof credit is claimed.
