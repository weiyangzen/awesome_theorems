# Exact-statement gate: blocked

Item: `S56-M-1351-STATEMENT`

Theorem: `THM-M-1351`

Base revision: `9898aa12e1dd435f018a54a6266ec411ed09a26a` (tree
`c0abfcd8c20a1be4b894a7664746d02086072b9d`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1351-INTAKE` has provisional worker
state `[_]` in the authoritative execution DAG, not master-accepted state `[x]`. The intake receipt
also declares `accepted: false`, has no accepted receipt ID, and deliberately leaves the canonical
mathematical statement and Lean target null. Master acceptance remains required before any future
statement transition can be accepted. Rev-5.6 section 10.2 permits this dependency-ordered attempt
from a provisional predecessor, so the dependency did not prevent the scoped blocker analysis.

Independently, the exact Lean 4 target cannot be truthfully elaborated from the received repository
catalog record. Its entire mathematical content is the title `Poincaré映射` (Poincare map), the
attribution to Henri Poincare, the year 1881, and the gloss `周期轨道的稳定性` (stability of periodic
orbits). It gives no bibliography, exact proposition, definition, ordered binder, hypothesis,
conclusion, proof boundary, correction, erratum, or formal artifact. Stage0 explicitly leaves the
precise definitions and premises open, and rev-5.6 treats the catalog value `已验证` as untrusted
metadata.

The modern discovery source inspected during intake confirms rather than resolves the ambiguity.
Gerald Teschl's *Ordinary Differential Equations and Dynamical Systems*, Section 12.2,
separates at least four materially different results:

- equation (12.9) defines a local Poincare first-return map using a transverse section and a return
  time;
- Lemma 12.2 relates stability and asymptotic stability of a periodic orbit to stability of the
  corresponding return-map fixed point;
- Corollary 12.3 gives an asymptotic-stability criterion from eigenvalues of the derivative of the
  return map; and
- Theorem 12.4 compares the derivative spectrum with nontrivial monodromy multipliers.

The catalog does not cite Teschl or select one of these roots, their conjunction, or a different
classical result such as independence under changing the section. It also does not fix the
continuous-time system, phase space, scalar field, regularity, local or global flow model, periodic
orbit and period convention, transverse section, return-time branch and domain, stability notion,
spectral conventions, base point, or time direction. Equilibria, zero or nonminimal periods,
tangential or missing returns, zero-dimensional sections, incomplete flows, unit-circle
multipliers, the neutral flow multiplier, and section changes all remain unresolved boundary cases.

Those choices change the proposition. Selecting a familiar construction, orbit/fixed-point
equivalence, derivative criterion, monodromy comparison, or section-independence theorem would
invent, broaden, specialize, or substitute mathematics rather than elaborate the exact received
target. Assuming the desired return map, stability equivalence, or spectral conclusion as a
structure field would only hide the same gap. Neighboring Floquet and Poincare-Bendixson targets
cannot supply statement identity or proof credit.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing elaborated
expression fingerprint hard blockers. Consequently there is no honest canonical declaration for
which imports can be certified minimal. No `Statement.lean`, exact expression, checked alternate
transport, or mutation suite was created. The required removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations are undefined rather than passed. The intake
vector remains `[H5, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with the pinned environment. Its direct imports
expose generic implicit-function, ODE, flow, fixed-point, periodic-point, and derivative APIs.
All seven checks pass. They do not construct a transverse section or first-return time, define a
Poincare map, state an orbit/fixed-point stability theorem, or provide a monodromy bridge. The
probe's imports therefore cannot be certified minimal for an absent target, and the successful
check receives no statement, anchor, or proof credit.

A bounded search of pinned mathlib and repository-local Lean found only unrelated partial-function
and combinatorial first-return APIs, prose references, generic circle-map motivation, and another
target's Poincare-Bendixson boundary. No target-specific declaration appeared under the recorded
return-map, periodic-orbit-stability, or multiplier terms. This is local feasibility evidence only,
not the downstream immutable anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` link to canonical pinned artifacts was used read-only. No update, build,
dependency clone, fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (Asia/Shanghai).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1351` | 0 | rank 961; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| repository, intake, source-family, and target-boundary inspection | 0 | found the sparse catalog record, explicit null intake target, and four inequivalent source-family results; no source-selected proposition |
| `sha256sum` over authority, intake, source, probe, toolchain, and pinned mathlib inputs | 0 | exact hashes are recorded in `statement-blocker.json` |
| `python3 -B Stage1_Instances/THM-M-1351/check_intake.py` | 1 | the historical intake receipt's blueprint hash is stale after integration; the checker also freezes its earlier base, intake state, and exact nine-file inventory, so this phase did not rewrite it |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1351/IntakeProbe.lean` | 0 | seven generic adjacent APIs elaborated; no canonical target was declared |
| bounded return-map and periodic-orbit-stability search in pinned mathlib and repository-local Lean | 0 | only adjacent or unrelated references appeared; no target-specific declaration was located under the recorded terms |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| JSON parse and scoped invariant check for `statement-blocker.json` | 0 each | blocker identity, null target and imports, unchanged vector, four undefined mutations, false completion flags, and absent-self-test boundary agree |
| scoped whitespace checks for both new artifacts | 0; 1 each | no whitespace diagnostics; per-file no-index exits are only the expected new-file difference status |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

## Retry Condition And Status Boundary

The integration lane must first master-accept refreshed intake evidence. Accountable reviewers must
then preserve and hash a lawful immutable primary or authoritative source, select and independently
approve one exact root theorem or explicit conjunction, and transcribe every incorporated
definition, ordered binder, hypothesis, conclusion, proof boundary, correction, and erratum. The
selection must fix the dynamics, phase space, orbit and period, section, transversality, return-time
construction, regularity, stability, derivative and multiplier conventions, base point, time
direction, and every degenerate case while preserving the boundaries with neighboring targets.

A fresh statement run can then encode precisely that source-selected claim using real definitions,
minimize pinned imports, serialize and hash the elaborated expression and environment, compile every
credited transport, and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
