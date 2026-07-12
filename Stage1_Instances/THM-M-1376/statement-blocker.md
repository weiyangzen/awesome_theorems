# Exact-statement gate: blocked

Item: `S56-M-1376-STATEMENT`

Theorem: `THM-M-1376`

Base revision: `1fc66febfddf404bb914cec34962d66862b96f2b` (tree
`49ae48302378d63f3c54b2a43eeca26433c6b7c5`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
The record supplies only the title Poincare recurrence theorem, Henri Poincare, 1890, and the gloss
`有界系统的回归性` ("recurrence of bounded systems"). It supplies no citation, carrier, dynamics,
ordered binders, hypotheses, recurrence predicate, conclusion, proof boundary, or boundary cases.
Stage0 explicitly leaves the exact definitions and premises, proof route, alternate forms, axioms,
machine status, and artifacts open. The catalog's `已验证` value is untrusted metadata under
rev-5.6.

The wording does not select among materially different propositions. A discrete finite-measure
form says that a measure-preserving self-map returns almost every point of each measurable set to
that set infinitely often. A topological form quantifies over every neighborhood. An ODE or
Hamiltonian form additionally needs a flow or time map, an invariant finite-measure region or
energy shell, measure preservation, completeness, and checked bridges from physical boundedness to
the measure-theoretic hypotheses. The record fixes none of these, nor the exceptional-set and
return-time quantifier order, whether iteration zero counts, or the treatment of null sets,
equilibria, incomplete trajectories, and boundary escape.

There is also an unresolved identity boundary. `THM-M-1521` has the translated title and identical
attribution, date, gloss, importance, and untrusted status under a separate target ID. Its dossier
selected a discrete finite-measure formulation, but no accepted alias, deduplication,
specialization, canonical-root ownership, or evidence-sharing decision transfers that choice to
`THM-M-1376`. The stronger physics-catalog wording about almost all orbits of a bounded conservative
system is also a separate uncited gloss without the required definitions and bridges. Copying the
foreign statement would therefore substitute mathematics rather than elaborate the exact received
target.

The intake correctly leaves the canonical mathematical statement, Lean module and expression,
minimal imports, elaborated-expression hash, and target environment fingerprint null at
`[H1, M4, R4]`. Rev-5.6 treats statement ambiguity and a missing expression fingerprint as hard
blockers. Without a canonical target, checked transports and the required removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations are undefined rather than passed.
No `Statement.lean`, assumed recurrence field, weakened special case, axiom, placeholder, or
broadened theorem was introduced.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated using the pinned environment. Its direct import,
`Mathlib.Dynamics.Ergodic.Conservative`, exposes the finite-measure preservation-to-conservativity
bridge, measurable-set recurrence, and topological recurrence. Nine adjacent declarations and the
foreign candidate expression type all elaborate. This is real feasibility evidence, but the probe
declares no target or proof body and supplies no source transport or ownership decision. Its import
therefore cannot be certified minimal for the absent canonical target and receives no statement,
anchor, or proof credit.

A bounded exact-topic search located this pinned recurrence family, the separately owned
`THM-M-1521` wrappers, and its legacy file. This is discovery evidence only, not the downstream
immutable anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No `lake update`, `lake build`, dependency
clone or fetch, or other `.lake` mutation was run.

## Validation Evidence

Commands ran in this worker clone on 2026-07-13 (Asia/Shanghai), from the repository root unless a
different working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1376` | 0 | rank 986; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| initial `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| scoped catalog, Stage0, manifest, DAG, intake, duplicate, and pinned-source inspection | 0 | confirmed the sparse theorem-family gloss, null intake target, unresolved duplicate ownership, foreign candidate, and open physical bridges |
| `sha256sum` over authority, source, intake, duplicate, toolchain, manifest, probe, and pinned-source inputs | 0 | exact hashes are recorded in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean and Lake versions agree with the pinned environment above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package status | 0 | pinned revision and tree agree; package worktree is clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1376/IntakeProbe.lean` | 0 | nine adjacent APIs and the foreign candidate expression type elaborated; output SHA-256 `8eeaf030f3e9c63f3b1944dd36c636561ef1e1ed9ccb57afa882c561ea9d1f4f`; no target or proof body |
| bounded exact-topic search in pinned mathlib, repo-local Lean, and `THM-M-1521` | 0 | found the pinned theorem family and foreign wrappers; discovery only |
| `python3 -B Stage1_Instances/THM-M-1376/check_intake.py` | 1 | historical intake checker stops because it freezes intake authority state `[ ]`, while current authority records provisional `[_]`; it was not rewritten during statement work |
| prohibited Lean construct scan over the owned path | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-1376/statement-blocker.json` plus scoped blocker invariants | 0 | identity, open blocked state, null target/import/hash, unchanged vector, four undefined mutations, false completion flags, exact two-file scope, and absent self-test agree |
| scoped whitespace checks for both blocker files | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest is absent because the exact-statement deliverable did not pass |

The intake prerequisite has provisional worker state `[_]`, not master-accepted state `[x]`; its
receipt declares `accepted: false` and contains no accepted receipt ID. Section 10.2 permits this
dependency-ordered attempt, so that did not prevent the investigation. It remains an independent
acceptance prerequisite, while the first substantive statement failure is the missing exact source
statement and duplicate/root-ownership decision.

## Retry Condition And Status Boundary

Accountable reviewers must preserve and hash a lawful immutable primary or authoritative source,
select and transcribe one exact proposition and every incorporated definition with pinpoint
locators, audit translation, corrections, errata, and proof boundary, and independently approve the
mapping. They must issue an accountable alias, deduplication, specialization, or distinct-root
decision for `THM-M-1376` versus `THM-M-1521`; fix the discrete, topological, flow, ODE, or
Hamiltonian model; and freeze the carrier, measure, finiteness, invariance, preservation,
exceptional-set, return-time, quantifier, ordered-binder, and boundary conventions. The integration
lane must also master-accept the intake dependency before accepting a future statement transition.

A later statement worker can then encode precisely that approved claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; the vector remains `[H1, M4, R4]`;
`audit_complete: false` and `theorem_complete: false`; no debt change is proposed. Because the
exact-statement deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt,
worker `[_]`, or master acceptance is claimed.
