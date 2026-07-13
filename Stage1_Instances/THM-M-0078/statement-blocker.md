# Exact-statement gate: blocked

Item: `S56-M-0078-STATEMENT`

Theorem: `THM-M-0078`

Base revision: `48abbb2d2eeb89816c5ffc0ad8faafa4b9d24dd0` (tree
`0f26e2c78fb5fff9277cbbdfef5e145fd4ef06f1`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0078-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. Its receipt has `accepted: false`, is not
content-addressed, and has no accepted receipt ID. More decisively, the intake intentionally leaves
the canonical human statement, Lean module, expression, elaborated-expression hash, and
canonical-target environment fingerprint null.

The complete repository claim is only `关于群扩张的分类` ("about the classification of group
extensions"). This names a subject, not a stable proposition. It does not fix the classified
extension objects, endpoint data, action, equivalence relation, classifying invariant, theorem
direction, domains, ordered binders, hypotheses, conclusion, or boundary cases.

The attribution also fails to identify the theorem. The catalog says Hans Zassenhaus and 1937.
Bibliographic metadata for that author and year identifies *Beweis eines Satzes ueber diskrete
Gruppen*, while the title that matches finite group-extension equivalence is the coauthored 1971
Johnson-Zassenhaus paper *On equivalence of finite group extensions*. No primary proposition from
either paper, incorporated definition chain, immutable edition, correction or errata disposition,
or independent source review is accepted.

Selecting the butterfly lemma, Schur-Zassenhaus, an abelian-kernel `H^2` classification, a
factor-set classification, or a split or central extension special case would therefore substitute
proposition-changing mathematics. Rev-5.6 treats statement ambiguity and a missing elaborated
expression fingerprint as hard blockers. There is no truthful canonical target whose imports can
be certified minimal, no credited alternate form for a checked transport, and no target against
which the required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case
mutations can run. Those mutation results are undefined, not passed. The root vector remains
`[H5, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with its two direct imports,
`Mathlib.GroupTheory.GroupExtension.Basic` and
`Mathlib.RepresentationTheory.Homological.GroupCohomology.LowDegree`. It checks extension,
equivalence, section, splitting, semidirect-extension, split-equivalence, and `groupCohomology.H2`
interfaces. Its two representative terms elaborate, and the two imported group-extension facts
report `[propext, Classical.choice, Quot.sound]`.

This confirms that the pinned discovery surface is available, but the probe declares no canonical
target, checked source transport, expression fingerprint, or proof body. Its imports are direct
imports for a discovery-only probe, not a minimal-import claim for an absent target. Mathlib's
group-extension and low-degree-cohomology documentation explicitly lists the likely
equivalence-class/`H^2` relationship as future work. A bounded Lean-source search found this
infrastructure, those TODOs, and the distinct Schur-Zassenhaus theorem; it was not an exhaustive
anchor audit or a global absence proof.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided `.lake` symlink was used
read-only. No update, build, dependency clone, fetch, or dependency mutation was run.

## Validation Record

Commands ran from this worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0078` | 0 | rank 1528; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| initial `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `Formalizations/Lean/.lake` symlink was untracked; base revision and tree appear above |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| mathlib package status, revision, and tree queries | 0 | package worktree clean; pinned revision and tree recorded above |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0078/IntakeProbe.lean` | 0 | eight APIs and two representative terms elaborated; two axiom sets printed; no canonical target or proof declared; stdout SHA-256 `007f233dcdd2699cc4aea9a2192745727c716e5d6d94d69dc5a7637d84441d5c` |
| one concurrent replay of the preceding Lean command | 1 | Lake reported `external command 'git' exited with code 128` while another scheduler worker was populating the shared canonical `flt-regular` package; after that external activity finished, the final replay below passed; this transient run is not credited as target evidence |
| bounded group-extension/Zassenhaus search over owned, repo-local, and pinned mathlib Lean | 0 | found definitions, basic facts, explicit `H2` classification TODOs, and distinct Schur-Zassenhaus matches; no exact source-mapped target located |
| `python3 -B Stage1_Instances/THM-M-0078/check_intake.py` | 1 | historical intake checker rejected the integration-updated intake state `[_]`; it was not edited or represented as statement evidence |
| JSON parse and scoped blocker-invariant checks | 0 | valid JSON; null target/imports, four undefined mutations, unchanged vector, false completion flags, and no-self-test boundary agree |
| prohibited-declaration scan over owned Lean files | 0 | no `sorry`, `admit`, `sorryAx`, axiom, constant, opaque, or unsafe declaration found |
| scoped whitespace checks for the two new blocker artifacts | expected new-file difference | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the statement deliverable did not pass |

The historical intake checker is bound to the intake's original authoritative `[ ]` state. The
integration lane now records intake `[_]`, so it fails closed on that changed input. It was neither
edited nor represented as passing for this statement attempt.

The automation clone shares the canonical `.lake` artifact target with other scheduler workers. A
concurrent worker began populating the pinned `flt-regular` dependency between two probe replays,
causing one transient Lake/Git exit 1. This worker did not run an update, clone, fetch, or build.
After the external operation completed, `flt-regular` resolved to its manifest-pinned revision and
the final narrow probe plus the full scoped blocker validation passed. This dirty shared-cache
observation reinforces the nonrelease evidence boundary and does not alter the statement blocker.

## Retry Condition And Status Boundary

Accountable reviewers must lawfully preserve and hash an immutable primary or authoritative source,
resolve the 1937/1971 identity conflict, and independently approve one exact group-extension
classification proposition. They must transcribe every incorporated definition, domain, binder,
hypothesis, conclusion, proof boundary, correction, erratum, translation decision, and boundary
case. A later statement run can then encode precisely that claim, minimize its pinned imports,
serialize the elaborated expression and environment, compile every credited transport, and execute
all four mutation classes. Master acceptance of the intake also remains required before an accepted
statement transition.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. No `.stage1-worker-selftest.json`,
statement receipt, worker `[_]`, master acceptance, statement fingerprint, or proof credit is
claimed.
