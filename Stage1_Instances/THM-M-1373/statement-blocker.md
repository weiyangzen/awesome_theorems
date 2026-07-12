# Exact-statement gate: blocked

Item: `S56-M-1373-STATEMENT`

Theorem: `THM-M-1373`

Base revision: `73c9cdb8a4086ef1fc18f25aa52185f4b68a0094` (tree
`96d5d58add62468ac9e9de9ce525ec7b4319bacd`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
That record supplies only `哈密顿系统` (Hamiltonian systems), William Hamilton, 1834, and the gloss
`经典力学的数学框架` (a mathematical framework for classical mechanics). It contains no formula,
cited theorem, incorporated definition, ordered binder, hypothesis, truth-valued conclusion, proof
boundary, correction history, or reviewer. Stage0 repeats the gloss but explicitly leaves the exact
definitions and premises, proof route, equivalent forms, axioms, machine status, and artifact links
open. The catalog value `已验证` is untrusted metadata under rev-5.6.

The wording identifies a formalism, not one proposition. It does not select among:

- Hamilton's canonical coordinate equations;
- a coordinate-free characterization of Hamiltonian vector fields;
- equivalence with Euler-Lagrange dynamics under a regular Legendre transform;
- conservation of an autonomous Hamiltonian along a trajectory;
- preservation of a symplectic form or phase-space volume by Hamiltonian flow; or
- Liouville-Arnold integrability and action-angle coordinates.

These have different domains, hypotheses, conclusions, and boundary cases. Several also have their
own repository targets. Choosing one, conjoining them, or assuming the desired conclusion in an
abstract data structure would invent, narrow, broaden, or substitute mathematics rather than
elaborate the exact received target.

Hamilton's 1834 paper *On a general method in dynamics* is only a bibliographic source-family lead.
The intake records DOI `10.1098/rstl.1834.0017`, issue 124, pages 247-308, but no lawful complete
edition, exact result passage, incorporated definitions, premise map, proof boundary, correction or
errata audit, or independent review was admitted. The paper-family attribution therefore cannot
select a root. The near-synonymous `THM-M-1516` target has no accepted alias, deduplication, or root-
ownership decision, so its historical Lean artifact and unpinned external lead cannot supply
statement identity or inherited credit here.

The intake correctly leaves the canonical human statement, Lean module and expression, minimal
imports, and expression and environment fingerprints null at `[H5, M4, R4]`. Sections 5 and 5.1 of
the rev-5.6 blueprint make that ambiguity and missing fingerprint hard blockers. Without a
canonical target, checked alternate transports and the required removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations are undefined rather than passed. No
`Statement.lean`, axiom, placeholder, weakened special case, broadened interface, or assumed
Hamiltonian-system conclusion was introduced.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with the pinned environment. Its three direct
imports expose thirteen adjacent integral-curve, flow, derivative, canonical symplectic-matrix, and
linear symplectic-group interfaces. All checks pass, with complete stdout SHA-256
`db22dedd6b2f69a558430227fcff6c08724f74f2df118497582370262c2834b7`. The probe defines no
Hamiltonian, Hamiltonian vector field, trajectory semantics, source-selected conclusion, canonical
target, or proof body. Its imports therefore cannot be certified minimal for an absent target and
receive no statement or proof credit.

The legacy `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_185.lean` also re-elaborates, but it
belongs to `THM-M-1516`. Its `StatementShape` quantifies over data whose proposed premises and
outputs include unrelated unconstrained `Prop` fields, and the file explicitly records the terminal
Hamiltonian-mechanics theorem as open. Successful elaboration authenticates only that discovery
artifact; it is not a source-faithful transport or an exact statement for this target.

A bounded exact-topic search found no Hamiltonian-system, Hamiltonian-mechanics, Hamiltonian-flow,
Hamiltonian-vector-field, or Hamilton-equations occurrence in pinned mathlib. Repository-local
matches were other targets' interfaces, open-debt records, and unrelated uses. This is narrow
discovery evidence, not the downstream immutable anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The `lean-toolchain`,
`lake-manifest.json`, and automation-provided `.lake` link-target SHA-256 values are respectively
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`,
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`, and
`e8714e9ebb75a5da1eeb16fdb6f50831a6cab29f115df43fa8e7535b38f59826`.

The `.lake` link points to the canonical pinned artifacts and was used read-only. No `lake update`,
`lake build`, dependency clone or fetch, or other `.lake` mutation was run.

## Validation Evidence

Commands ran in this worker clone on 2026-07-13 (Asia/Shanghai), from the repository root unless a
different working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1373` | 0 | rank 983, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base revision and tree are recorded above |
| scoped repository source, Stage0, manifest, blueprint, skill, intake, crosswalk, scope, and neighboring-target inspection | 0 | only a framework label and gloss are authoritative; every proposition-changing choice remains open |
| `sha256sum` over authority, intake, toolchain, probe, legacy candidate, and pinned mathlib inputs | 0 | hashes agree with `statement-blocker.json` |
| `python3 -B Stage1_Instances/THM-M-1373/check_intake.py` | 1 | historical intake replay stops because its frozen execution-DAG projection expected the intake item at `[ ]`, while integration now projects it as provisional `[_]`; this phase does not rewrite historical evidence |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean and Lake agree with the pinned environment above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | revision and tree agree with the fingerprint; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1373/IntakeProbe.lean` | 0 | thirteen adjacent APIs elaborated; no canonical target was stated; stdout SHA-256 is `db22de...b7` |
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_185.lean` | 0 | other-target legacy interface and debt markers elaborated; no source identity or target credit; stdout SHA-256 is `89dd39...25` |
| bounded pinned-mathlib and repo-local exact-topic searches | 1 and 0 | no pinned-mathlib occurrence; repo-local matches are discovery-only foreign artifacts, not an exact root |
| prohibited Lean construct scan over `Stage1_Instances/THM-M-1373` | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, axiom, bodyless declaration, or unsafe declaration |
| JSON parse and scoped invariant/fingerprint checks for `statement-blocker.json` | 0 | IDs, open state, null target/imports, unchanged vector, four undefined mutations, false completion flags, exact paths, current input hashes, and absent self-test agree |
| whitespace checks for both added blocker artifacts | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | no worker self-test manifest exists because the exact-statement deliverable is blocked |

The intake prerequisite is only provisional `[_]` and is not master-accepted. That acceptance
boundary independently prevents statement-node acceptance, but the first substantive failure is
the missing exact source statement and root selection.

## Retry Condition

The integration lane must first master-accept refreshed intake evidence. Accountable reviewers
must preserve and hash one lawful immutable complete primary or authoritative source, select and
independently approve one exact truth-valued result, transcribe every incorporated definition,
ordered binder, hypothesis, conclusion, convention, proof boundary, correction, erratum, and
boundary case, and reconcile `THM-M-1373` with `THM-M-1516` and the neighboring conservation and
integrability targets. They must freeze the phase space, scalar and time fields, dimensions and
universes, symplectic and sign conventions, Hamiltonian regularity and time dependence, trajectory
or flow semantics, existence and uniqueness premises, and local or global conclusion.

A later statement worker can then encode that same claim using real Lean definitions, minimize its
pinned imports, serialize and hash the elaborated expression and environment, compile every
credited transport, and run all four required mutation classes.

This is a blocked-attempt record, not completion of the statement node or any downstream node. The
root remains `[H5, M4, R4]`, with `audit_complete: false` and `theorem_complete: false`; no debt
change is proposed. Because the assigned phase is not genuinely self-tested to its completion gate,
no `.stage1-worker-selftest.json`, node receipt, worker `[_]`, or master acceptance is claimed.
