# Exact-statement gate: blocked

Item: `S56-M-0064-STATEMENT`

Theorem: `THM-M-0064`

Base revision: `ebd5f75831296a8a35e7b33013b964f2baf31bb9` (tree
`d1e4bc83c803eefcd9898aac57352265a29f0658`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0064-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. More importantly, that intake deliberately leaves the
canonical human statement, Lean module, declaration or expression, expression hash, and
canonical-target environment fingerprint null.

The repository's complete mathematical wording is only `五次及以上一般多项式方程无根式解`
(general polynomial equations of degree five and above have no solution by radicals). It does not
define `general`, choose generic-formula impossibility versus existence of counterexamples, fix
degree exactly five versus every degree at least five, specify the base and extension fields, or
define whether radical solvability concerns one root, every root, or a splitting field. It also
does not settle characteristic, irreducibility, separability, roots of unity, generic
specialization, or degenerate cases. These choices give materially different propositions.

The identified Abel sources are still bibliographic leads. No lawful immutable exact passage,
incorporated definitions, proof boundary, translation, correction or errata disposition,
attribution/date reconciliation, or independent source review has been accepted. Selecting a
familiar modern form without those inputs would invent missing mathematics rather than elaborate
the exact source claim.

Rev-5.6 treats statement ambiguity and a missing elaborated-expression fingerprint as hard
blockers. There is consequently no truthful target whose direct imports can be certified minimal,
no credited alternate encoding for a checked transport, and no canonical expression against which
the required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations
can run. Those mutation results are undefined, not passed. The root vector remains
`[H1, M3, R4]`.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` was re-elaborated with its sole direct import,
`Mathlib.FieldTheory.AbelRuffini`. It checks `solvableByRad`, the two radical-root-to-solvable-Galois
declarations, and nonsolvability of symmetric groups. The two printed axiom reports are
`[propext, Classical.choice, Quot.sound]`.

Pinned mathlib's module documentation explicitly says that it proves only one direction: a root
solvable by radicals gives a solvable Galois group. The symmetric-group results do not construct a
general polynomial with that Galois group. Thus the probe confirms that relevant pinned interfaces
are available, but declares no catalog target, checked generic-polynomial transport, or root proof.
Its single import is a probe fact, not a minimal-import result for the absent target.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided `.lake` symlink was used
read-only. No update, build, clone, fetch, or dependency mutation was run.

## Validation Record

Commands ran from this worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0064` | 0 | rank 1095; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| initial `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `Formalizations/Lean/.lake` symlink was untracked; base revision and tree appear above |
| `git blame -L 477,482 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog fields originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `python3 -B Stage1_Instances/THM-M-0064/check_intake.py` | 1 | the historical intake checker rejects the integration-updated authoritative intake state `[_]`; it expects the intake-time state `[ ]`, was not modified, and is not statement evidence |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions above |
| mathlib revision, tree, and worktree-status queries | 0 | pinned revision and tree above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0064/IntakeProbe.lean` | 0 | five adjacent APIs elaborated and both axiom reports printed; no canonical target or proof declared |
| bounded repo-local and pinned-mathlib search for Abel-Ruffini, general/generic polynomial, and `solvableByRad` | 0 | found only this probe and mathlib's one-direction module; no exact generic-polynomial root or Galois-realization bridge |
| finalized JSON parse and scoped blocker-invariant check | 0 | structured blocker is valid; identity, null target/imports, unchanged vector, four undefined mutations, false completion flags, and no-self-test boundary agree |
| prohibited-declaration scan over owned Lean files | 0 | no `sorry`, `admit`, `sorryAx`, axiom, constant, opaque, or unsafe declaration found |
| scoped whitespace checks for both new blocker artifacts | expected new-file difference | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because exact target elaboration did not pass |

## Retry Condition And Status Boundary

Accountable reviewers must preserve and hash a lawful immutable primary or authoritative source and
independently approve one exact proposition with every incorporated definition, ordered binder,
hypothesis, conclusion, proof boundary, translation, correction, erratum, and boundary case. They
must settle generic-formula versus counterexample scope; degree quantification; coefficient and
extension fields; characteristic, irreducibility, and separability; one root versus full splitting;
radical-tower and roots-of-unity conventions; the Galois realization; and higher-degree transport.
A later statement run can then encode precisely that claim, minimize its pinned imports, serialize
its elaborated expression and environment, compile every credited transport, and execute all four
mutation classes. Master acceptance of refreshed intake evidence is also required before an
accepted statement transition.

This is the assigned phase's truthful blocker result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. No `.stage1-worker-selftest.json`,
statement receipt, worker `[_]`, master acceptance, statement fingerprint, proof body, or proof
credit is claimed.
