# Exact-statement gate: blocked

Item: `S56-M-0636-STATEMENT`

Theorem: `THM-M-0636`

Base revision: `4b93dbd88c5b39d7b83f2f9278c3371f53703d76` (tree
`a526f0ad0273426336b064730ac8b85143e3e5db`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the received source record. The
catalog gives only the title `不动点定理`, attributes it to Brouwer in 1910, and says
`紧凸集上连续映射有不动点` (a continuous map on a compact convex set has a fixed point). It
does not cite a proposition or specify the scalar field, ambient space, finite-dimensionality,
nonemptiness, self-map condition, continuity domain, ordered binders, exact conclusion, or boundary
cases. Stage0 explicitly leaves the precise definitions and premises open. The catalog's `已验证`
label is untrusted under rev-5.6.

These omissions are proposition-changing. In an arbitrary infinite-dimensional Banach space, a
nonempty compact convex set is the domain of Schauder's theorem, while a general locally convex
space points toward the Tychonoff family. Brouwer's usual finite-dimensional theorem can itself be
encoded over `EuclideanSpace Real (Fin n)` or an arbitrary finite-dimensional real normed space,
with a subtype self-map or an ambient map plus `ContinuousOn` and `MapsTo`. The catalog does not
select among these formulations.

There is also unresolved target identity. `THM-M-0319` separately owns the explicit catalog wording
`欧氏空间紧凸集上的不动点定理` and has a provisional Euclidean compact-convex statement.
`THM-M-0640` separately owns the closed-ball wording. Those artifacts are useful discovery inputs,
but their scopes, receipts, and proof credit cannot be inherited by `THM-M-0636`. Copying
`THM-M-0319` would silently resolve this target's documented source and duplicate-scope blocker;
choosing the more general finite-dimensional normed-space form would make a different unresolved
choice. Neither is exact merely because both elaborate.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing expression
fingerprint hard blockers. With no approved canonical human proposition, there is no honest Lean
expression for which direct imports can be certified minimal or for which alternate transports and
the required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations
can be credited. No `Statement.lean`, assumed theorem interface, axiom, placeholder, weakened
special case, or broadened theorem was introduced. The root remains `[H1, M4, R4]`.

The prerequisite `S56-M-0636-INTAKE` is only provisional worker state `[_]`, not master-accepted
`[x]`. Rev-5.6 section 10.2 permits this dependency-ordered blocker attempt while concurrency is
enabled, but its receipt is non-content-addressed, declares `accepted: false`, and contains no
accepted receipt ID. Master acceptance remains independently required before any future statement
transition can be accepted.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates in the pinned environment. Its three direct imports
expose compactness, convexity, continuity, self-map, finite-dimensional, and fixed-point vocabulary;
all nine checks pass. The probe does not state a Brouwer theorem, select the ambient space, provide
a checked source transport, or contain a proof body. Its imports cannot be certified minimal for a
target that has not been selected and receive no statement or proof credit.

Two prospective targets were checked outside the repository-owned target path as feasibility
tests only. The concrete Euclidean ambient-map form elaborates with the single import
`Mathlib.Analysis.InnerProductSpace.PiL2`; the arbitrary finite-dimensional real normed-space form
and a subtype-map variant elaborate with the single import
`Mathlib.Analysis.Normed.Module.FiniteDimension`. Successful elaboration shows that the pinned APIs
can express familiar Brouwer formulations. It does not determine which proposition the sparse
catalog record means.

A bounded search of pinned mathlib and repository-local Lean found no terminal Brouwer
compact-convex theorem. It found the separate `THM-M-0319` statement and its audit of the immutable
external candidate `harfe/fixed-point-theorems-lean4@11a9f041246d28374edae384241757f9a0cbd5e4`.
That candidate is only another source/anchor lead for this target: it has not been independently
adopted as `THM-M-0636`'s source proposition or placed in this repository's pinned proof closure.
These observations are discovery-only evidence, not the later anchor audit or a claim of global
absence.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No `lake update`, `lake build`, dependency
clone or fetch, or other `.lake` mutation was run.

## Validation Evidence

Commands ran in this worker clone on 2026-07-13 (`Asia/Shanghai`), from the repository root unless
another working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0636` | 0 | rank 1053, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree are recorded above |
| scoped manifest, blueprint, skill, catalog, Stage0, intake, scope, crosswalk, and neighboring-target inspection | 0 | the target record is not binder-complete and the dossier deliberately leaves the canonical claim and formal target null pending source selection and duplicate-scope review |
| `python3 -B Stage1_Instances/THM-M-0636/check_intake.py` before adding blocker artifacts | 0 | current target membership, provisional intake semantics, H1/M4/R4 boundary, and six open tasks agreed |
| the same historical intake-only replay after adding blocker artifacts | 1 | its frozen nine-file inventory rejects the two statement-phase files; this phase records rather than rewrites historical intake evidence |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean and Lake agree with the pinned environment above |
| pinned mathlib revision/tree and package-status checks | 0 | revision and tree agree with the fingerprint above; package worktree is clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0636/IntakeProbe.lean` | 0 | nine adjacent APIs elaborated; stdout SHA-256 `96d96af1d387d3b5ab38193cc224dd6e14d0eea1782b1542746407b200d3f151`; no canonical target was declared |
| `lake env lean` on `/tmp/THM_M_0636_Minimal.lean`, `/tmp/THM_M_0636_FiniteDimensionOnly.lean`, and `/tmp/THM_M_0636_Subtype.lean` | 0 each | concrete Euclidean, abstract finite-dimensional ambient, and subtype-map candidate statements elaborated as feasibility probes only |
| bounded Brouwer/fixed-point search in pinned mathlib and repository-local Lean | 0 | no pinned-mathlib terminal Brouwer theorem; only the separate `THM-M-0319` statement/audit and unrelated Brouwerian or fixed-point material |
| prohibited Lean construct scan over the owned path | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, axiom, bodyless declaration, or unsafe declaration |
| JSON parse and scoped invariant check for `statement-blocker.json` | 0 each | IDs, open state, null target/imports, unchanged vector, four undefined mutations, false completion flags, exact two-file change scope, and absent self-test agree |
| whitespace checks for both added blocker artifacts | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | no worker self-test manifest exists because the exact-statement deliverable is blocked |

The intake checker is deliberately scoped to its original nine-file intake inventory. It passed
before this phase wrote its owned blocker evidence and now fails only at that historical inventory
assertion. Rewriting `check_intake.py`, `instance.json`, the intake receipt, or the target-local DAG
would alter the prior phase's evidence rather than validate this blocked statement attempt.

## Retry Condition

The integration lane must first master-accept refreshed intake evidence. Accountable reviewers must
then preserve and hash a lawful immutable primary or authoritative source, select and independently
approve one exact proposition, and transcribe every incorporated definition, ordered binder,
hypothesis, conclusion, proof boundary, correction, erratum, translation, and boundary case. They
must issue an explicit identity and ownership decision for `THM-M-0636` relative to the overlapping
Euclidean `THM-M-0319` and closed-ball `THM-M-0640` targets.

A fresh statement worker can then encode precisely that approved claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport, and
execute all four required mutation classes.

This is a blocked-attempt record, not completion of the statement node or any downstream node. The
root remains `[H1, M4, R4]`, with `audit_complete: false` and `theorem_complete: false`; no debt
change is proposed. Because the assigned phase is not genuinely self-tested to its completion gate,
no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or master acceptance is claimed.
