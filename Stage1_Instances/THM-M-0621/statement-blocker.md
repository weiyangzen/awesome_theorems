# Exact-statement gate: blocked

Item: `S56-M-0621-STATEMENT`

Theorem: `THM-M-0621`

Base revision: `113a7f4d7029a7905d85af76bec7896f679d8c52` (tree
`264a3a56a1cf2a90cd148082a358dd27edb2b0ea`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0621-INTAKE` is provisional worker
state `[_]`, not master-accepted state `[x]`. The intake receipt is explicitly unaccepted and
non-content-addressed and contains no accepted receipt ID. Rev-5.6 section 10.2 permits this
dependency-ordered provisional assessment, but master closure remains dependency ordered.

Independently, the exact Lean 4 target cannot be selected truthfully from the complete repository
source record. The catalog supplies only the Urysohn's lemma title, Pavel Urysohn attribution,
the year 1925, and the gloss "separation of closed sets in a normal space." It supplies no
bibliography, exact proposition, incorporated definitions, ordered binders, proof passage,
translation, correction or errata record, or independent review. Stage0 explicitly leaves the
precise definitions and premises, equivalent forms, axioms, machine status, and artifacts open.

Those omissions leave proposition-changing choices. In particular, the gloss does not select the
continuous real-valued separation conventionally called Urysohn's lemma over the separated-open-
neighborhood property built into normality. It also does not decide whether "normal" includes T1,
whether disjointness is explicit, the ambient universe and topology, a real-valued function versus
a continuous map into the unit interval, the zero/one orientation, the range clause, the exact
equality encoding, or empty-space and empty-set behavior.

The intake therefore deliberately freezes `canonical_statement`, `canonical_claim`, the Lean
module and declaration/expression, expression hash, and target environment fingerprint as null. It
records mathlib's `exists_continuous_zero_one_of_isClosed` only as a candidate. Selecting that
declaration now would silently choose mathlib's `NormalSpace` convention, real codomain, endpoint
orientation, `[0, 1]` range packaging, and `EqOn` conclusion without an approved source identity.
Selecting `NormalSpace.normal` or `normal_separation` would instead replace the named functional
lemma with the neighborhood-separation premise. Neither choice is a harmless elaboration detail.

Consequently there is no honest canonical declaration whose direct import can be certified
minimal. No `Statement.lean`, theorem declaration, checked transport, expression fingerprint, or
mutation fixture was created. The required removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations are undefined, not passed. The canonical root
vector remains unclassified because no canonical root exists; the intake's provisional family
boundary remains `[H unclassified, M3, R4]`. Audit and theorem completion remain false.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` was re-elaborated with its single direct import
`Mathlib.Topology.UrysohnsLemma`. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, it authenticates `NormalSpace`,
`NormalSpace.normal`, `normal_separation`, `normal_exists_closure_subset`, and
`exists_continuous_zero_one_of_isClosed`. The direct candidate has the following shape:

```text
[NormalSpace X] -> IsClosed s -> IsClosed t -> Disjoint s t ->
  exists f : C(X, Real),
    EqOn f 0 s and EqOn f 1 t and forall x, f x in Set.Icc 0 1
```

The probe output is 958 bytes with SHA-256
`14e804991e42d6c82801e9ac7f84dca022e5de508280950b9523206935b45328`. The candidate's
axiom report is exactly `propext`, `Classical.choice`, and `Quot.sound`.

This is real pinned interface evidence only. The probe declares no canonical target, source
transport, mutation, wrapper, or proof body. Its single import is minimal for the probe, not
certified minimal for an absent target, and receives no statement or proof credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided canonical `.lake` symlink
was reused read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake`
mutation was performed. The pinned mathlib worktree was clean after validation.

## Validation Record

Commands ran in this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0621` | 0 | rank 1315; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| scoped blueprint, skill, manifest, catalog, Stage0, intake, scope, crosswalk, and DAG inspection | 0 | the theorem family and direct pinned candidate are known, but the exact source proposition and every root-defining choice above remain open |
| `sha256sum` over authority, source, intake, toolchain, lock, and pinned candidate inputs | 0 | exact fingerprints are recorded in `statement-blocker.json` |
| `git blame -L 4608,4613 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| pre-edit `python3 -B Stage1_Instances/THM-M-0621/check_intake.py` | 0 | target identity, base ancestry and immutable base blobs, null root, H-unclassified/M3/R4 family boundary, pinned probe, and six open downstream tasks agreed before statement artifacts were added |
| finalized `python3 -B Stage1_Instances/THM-M-0621/check_intake.py` | 1 | historical intake replay stops at its frozen exact nine-file intake inventory after the two statement-blocker artifacts are added; this phase does not rewrite historical intake evidence |
| `cd Formalizations/Lean && lake env lean --version`; `lake --version` | 0 | pinned Lean and Lake versions recorded above |
| pinned mathlib revision/tree and `git status --short` | 0 | revision and tree recorded above; package source worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0621/IntakeProbe.lean` | 0 | five normality/Urysohn interfaces elaborated; candidate axiom report and output fingerprint appear above; no canonical target was declared |
| bounded exact-topic repo-local Lean search outside the intake probe | 1 (expected no match) | no separate repo-local Urysohn target declaration matched; this is discovery-only, not an exhaustive anchor audit |
| prohibited-declaration scan over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration; diagnostic `#print axioms` remains permitted |
| `python3 -m json.tool Stage1_Instances/THM-M-0621/statement-blocker.json` plus scoped blocker assertions | 0 | structured blocker parses; identity, dependency, null target/imports, undefined mutations, false completion flags, exact two-file scope, and absent self-test agree |
| scoped `git diff --check` and new-file text-hygiene checks | 0 aggregate | no whitespace, carriage-return, NUL, or final-newline diagnostic |
| `test ! -e .stage1-worker-selftest.json` | 0 | the worker self-test manifest is intentionally absent because exact target elaboration did not pass |

## Retry Condition And Status Boundary

The integration lane must master-accept the intake dependency before accepting a future statement
transition. Accountable reviewers must lawfully preserve and hash one immutable primary or
authoritative source, transcribe and independently approve one exact proposition, and map every
incorporated definition, ordered binder, hypothesis, conclusion, proof boundary, translation,
correction, erratum, and boundary case. They must explicitly decide functional versus neighborhood
separation, normal versus normal-T1, disjointness, universe and topology, codomain and range,
endpoint orientation, equality encoding, and all empty or vacuous cases.

A later statement worker can then encode precisely that approved claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

The intake checker is historical intake evidence with a deliberately closed nine-file inventory.
It passed before this phase added its artifacts and then failed closed on that inventory. Rewriting
the intake checker, dossier, receipt, target-local DAG, generated blueprint, or authoritative DAG
would neither resolve the missing proposition nor be valid statement evidence, so none was changed.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, node-specific receipt, worker `[_]`,
master acceptance, statement fingerprint, mutation certificate, or proof credit is claimed.
