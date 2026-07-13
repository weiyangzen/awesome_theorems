# Exact-statement gate: blocked

Item: `S56-M-0850-STATEMENT`

Theorem: `THM-M-0850`

Base revision: `748243faadc15828fb087059337fd05b7be9fdeb` (tree
`e46d642646f80980838b6f016f5d69b817bd464d`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0850-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. More importantly, that intake truthfully leaves the
canonical human proposition and Lean target null because the repository supplies only the title
"giant-component theorem" and the gloss "the appearance of a giant component in a random graph."

That wording does not choose a random-graph law (`G(n,m)`, binomial `G(n,p)`, or a coupled graph
process), parameter scaling, regime, ordered asymptotic quantifiers, probability mode, or exact
component-size conclusion. It also does not decide whether the theorem asserts supercritical
existence alone, uniqueness and asymptotic density, a subcritical contrast, a critical-window law,
or an emergence/hitting-time result. Rounding, ties, critical equality, small carriers, and endpoint
probabilities are unresolved. These choices change the proposition; they are not notation that Lean
can infer.

The 1960 Erdos-Renyi paper recorded at intake is only a bibliographic discovery candidate. No
immutable complete edition, numbered theorem and page, incorporated definitions, errata review, or
independent source-to-target approval selects one of its results. The separately scheduled duplicate
`THM-M-1114` has the same gloss but supplies no transferable statement or evidence. Selecting a
familiar modern `G(n,c/n)` theorem would invent a theorem variant and could silently replace the
historical uniform fixed-edge model with the binomial model.

Rev-5.6 makes statement ambiguity and a missing elaborated-expression fingerprint hard blockers.
There is therefore no honest canonical expression whose imports can be certified minimal, no
approved alternate encoding for checked transport, and no target against which the required
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations can run. Those
mutation results are undefined, not passed. The root vector remains `[H5, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with these direct imports:

- `Mathlib.Combinatorics.SimpleGraph.Connectivity.Finite`
- `Mathlib.Probability.Combinatorics.BinomialRandomGraph.Defs`

It checks eight adjacent connected-component and binomial-random-graph APIs. A bounded search of
repo-local Lean and pinned mathlib found the binomial distribution definitions but no giant- or
largest-component theorem. The probe declares no canonical target, transport, or proof body, and
its imports cannot be certified minimal for an absent target.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided `.lake` symlink was used
read-only. No update, build, clone, fetch, or dependency mutation was run.

## Validation Record

Commands ran from this worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0850` | 0 | rank 1405; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `pwd; git status --short --untracked-files=all; git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | worker clone confirmed; only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| `git blame -L 6236,6242 -- Docs/researches/math_theorems.md` | 0 | all sparse catalog fields originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version; lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'; git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | package worktree clean; pinned revision and tree recorded above |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0850/IntakeProbe.lean` | 0 | eight adjacent APIs elaborated; stdout SHA-256 `4f8df7e001d682e2fa75975d4eca884132fb7d01033b8798cddb6aa7cc5c9a21`; no canonical target or proof declared |
| bounded repo-local and pinned-mathlib `rg` search for giant/largest/random components | 0 | only the intake disclaimer, unrelated Erdos-Renyi material, and binomial-random-graph definitions matched; no exact giant-component target was found |
| `python3 -B Stage1_Instances/THM-M-0850/check_intake.py` | 1 | historical intake validator is stale against the integration-updated authoritative intake state `[_]`; it is not statement evidence and was not modified |
| scoped prohibited-declaration scan over `Stage1_Instances/THM-M-0850/*.lean` | 0 | the inner `rg` returned expected no-match exit 1; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration was found |
| `python3 -m json.tool Stage1_Instances/THM-M-0850/statement-blocker.json` plus scoped structured assertions | 0 | blocker JSON parsed; identity, dependency state, null target/imports, unchanged vector, four undefined mutations, false completion flags, and no-self-test boundary agree |
| `git diff --check -- Stage1_Instances/THM-M-0850` plus per-new-file no-index checks | 0 / expected difference exits | no whitespace diagnostics in tracked or newly added owned artifacts |
| scoped final-newline/trailing-whitespace check over both blocker artifacts | 0 | both files have final newlines, no CR/NUL bytes, and no trailing whitespace |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the statement deliverable did not pass |

## Retry Condition And Status Boundary

Accountable reviewers must lawfully preserve and hash an immutable complete primary or authoritative
source, select and independently approve one exact proposition, and transcribe every incorporated
definition, ordered binder, hypothesis, conclusion, probability limit, proof boundary, correction,
and boundary case. They must explicitly fix the graph law, scaling and regime, theorem strength,
component-size and uniqueness conventions, and any historical-to-modern model transport. A later
statement run can then encode precisely that claim, minimize its pinned imports, serialize the
elaborated expression and environment, compile every credited transport, and execute all four
mutation classes. Master acceptance of the intake remains required before an accepted statement
transition.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. No `.stage1-worker-selftest.json`,
statement receipt, worker `[_]`, master acceptance, statement fingerprint, or proof credit is
claimed.
