# Exact-statement gate: blocked

Item: `S56-M-0239-STATEMENT`

Theorem: `THM-M-0239`

Base revision: `2eea98305d46266f078a50cf0e85853bf6a5e702` (tree
`02279a8caa5f31ed8e37e35c8584a336eed9b974`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0239-INTAKE` has provisional worker
state `[_]`, not a master-accepted receipt. Independently, no exact Lean 4 target can be truthfully
elaborated from the authoritative repository record.

That record supplies only the title Jacobi inversion theorem, the attribution Carl Jacobi, the
year 1834, and the gloss "inversion of Abelian integrals." It provides no bibliography, formula,
incorporated definitions, ordered binders, assumptions, conclusion, proof boundary, correction
history, reviewer, or formal artifact. Stage0 explicitly leaves the precise definitions and
premises open. The catalog status `verified` is untrusted metadata under rev-5.6.

The intake identifies four plausible roots but deliberately credits none as canonical:

- surjectivity of the degree-`g` Abel-Jacobi map from `X^(g)` to `J(X)`;
- representation of every relevant class by `D - g P0` for an effective degree-`g` divisor `D`;
- simultaneous inversion of first-kind Abelian integrals modulo a period lattice; and
- a stronger explicit genus-`g` theta-function inversion theorem, including normal and
  exceptional cases.

These are not interchangeable without checked definitions and transports. The repository also
does not fix the analytic or algebraic curve model, connectedness and genus hypotheses, geometric
symmetric product or divisor representation, Jacobian or Picard-zero construction, Abel-Jacobi
base point and normalization, exact conclusion, special-divisor behavior, or boundary with
`THM-M-0238` and `THM-M-0240`. Selecting conventional answers would manufacture a nearby theorem.

The fixed Encyclopedia of Mathematics revision is a credible exposition lead, and the inspected
arXiv version gives a modern surjectivity sentence. Neither is an accepted primary or authoritative
proof source with a complete definition, assumption, exception, correction, and independent-review
crosswalk. Section 5 of the rev-5.6 blueprint makes this ambiguity and the missing expression
fingerprint hard blockers.

There is consequently no canonical expression for which minimal imports, alternate transports,
or removed-hypothesis, changed-domain, changed-binder-scope, and boundary mutations can be
certified. Those mutation tests are undefined, not passed. The first failed gate is exact
source-statement identity and its definition chain. The root remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with the pinned environment. Its six direct
imports expose a combinatorial symmetric power, general complex-manifold and compactness
interfaces, a one-dimensional Jacobi theta function, commutative group-scheme infrastructure, a
ring Picard group, and Weierstrass Jacobian-coordinate points. It defines no compact-curve
Jacobian, Abel-Jacobi map, period quotient, arbitrary-genus Riemann theta function, canonical
target, transport, or proof body. Its imports therefore cannot be certified minimal for a target
that has not been selected.

A bounded repository search found only the intake disclaimer and planning text that explicitly
marks Abel-Jacobi or Jacobian bridges missing. The same exact-topic search over pinned mathlib
found no matching declaration. This is narrow feasibility evidence only, not the downstream
anchor audit or a proof of global absence.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided untracked
`Formalizations/Lean/.lake` symlink points to the canonical pinned artifacts and was used read
only. The mathlib package worktree remained clean. No `lake update`, `lake build`, dependency
clone or fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran in the isolated automation checkout on 2026-07-13 (Asia/Shanghai).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0239` | 0 | rank 1250; planned; `L0/rework_required`; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 each | only the automation `.lake` symlink was untracked; base revision and tree are recorded above |
| `git blame -L 1724,1729 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog fields originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| exact `sha256sum` commands recorded in `statement-blocker.json` | 0 | current authority, source, intake, toolchain, dependency, probe, and pinned API fingerprints recorded |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 and Lake 5.0.0 at the revisions above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package `status --short` | 0 each | pinned mathlib revision and tree above; package status empty |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0239/IntakeProbe.lean` | 0 | eleven adjacent API checks elaborated; stdout SHA-256 `2358cd59c5204de50b54da93f01d537366ffc762522cf183ffae38402fcd31b0`; no target theorem stated |
| bounded repository and pinned-mathlib `rg` searches for Jacobi inversion, Abel-Jacobi, Jacobian variety, Riemann theta, and theta divisor | 0 / 1 | repository results were disclaimers or explicit missing-bridge plans; pinned exact-topic search had no match; discovery-only evidence |
| `python3 -B Stage1_Instances/THM-M-0239/check_intake.py` | 1 | historical intake freshness failure: `AssertionError: stale source hash: authoritative_blueprint_sha256`; historical evidence was not rewritten |
| `python3 -m json.tool Stage1_Instances/THM-M-0239/statement-blocker.json`; scoped `jq -e` invariant check | 0 each | blocker parsed; identity, null target/imports, four undefined mutations, unchanged vector, false completion flags, and blocked state passed |
| prohibited-declaration `rg` scan over owned Lean files | 1 | expected no match: no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| scoped `git diff --check`; separate `git diff --no-index --check` commands for both new files | 0 / 1 each | no whitespace diagnostics; no-index statuses are expected new-file differences |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The historical intake checker is not a current statement validator. Its receipt and hashes bind it
to the intake worker's earlier authority snapshot. Rewriting that provisional history is outside
this phase and would not cure the absent proposition.

## Retry Condition And Status Boundary

The integration lane must master-accept the intake before an eventual accepted statement
transition. Accountable reviewers must preserve and hash a lawful immutable primary or
authoritative source, select and transcribe one exact theorem and every incorporated definition,
ordered binder, hypothesis, conclusion, proof boundary, correction, erratum, exceptional case,
and historical claim, reconcile `THM-M-0238` and `THM-M-0240`, and independently approve the
mapping. A later statement worker can then encode only that claim with concrete Lean definitions,
minimize pinned imports, serialize and hash the elaborated expression and environment, compile
every credited transport, and run all four required mutation classes.

This records the first failed gate. It does not complete the statement node or any downstream
node. The root remains `[H1, M4, R4]`; `audit_complete` and `theorem_complete` remain false, and no
debt change is proposed. The assigned phase is not genuinely self-tested to its completion gate,
so no `.stage1-worker-selftest.json`, node-specific receipt, worker `[_]`, proof credit, or master
acceptance is claimed.
