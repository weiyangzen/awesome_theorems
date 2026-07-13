# THM-M-1456 exact-statement gate: blocked

Item: `S56-M-1456-STATEMENT`

Base revision: `2d82479e32843fd52283dcd9bb305954729c1199` (tree
`30134b43ab41e973d2558be90371bf18d6edb259`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1456-INTAKE` has only provisional worker
state `[_]`: `intake-receipt.json` has `accepted: false`, is not content-addressed, and has no
accepted receipt IDs. It also binds older blueprint and execution-DAG hashes. There is no
master-accepted dependency receipt.

Independently and decisively, the exact-statement gate fails. The complete repository record is the
technique-family label `preconditioning techniques` and the gloss `techniques for accelerating
iterative convergence`. It supplies no bibliography, formula, truth-valued proposition, problem
class, scalar field or space, ordered binders, hypotheses, iterative recurrence, preconditioner
object or placement, convergence observable, comparator, rate or cost conclusion, arithmetic
convention, stopping rule, breakdown policy, or boundary cases. Stage0 leaves its exact definitions
and premises open, and intake accordingly records a null human claim and null formal target.

Materially inequivalent theorem families fit the gloss: solution equivalence under an invertible
left transformation, convergence of one stationary method under a spectral-radius premise, an SPD
preconditioned-CG error estimate, or correctness and effectiveness of one concrete construction.
None is selected by an immutable source. An identity preconditioner gives no strict improvement;
`M = A` may merely move the original solve into applying `M^-1`; a singular, indefinite,
incompatible, or poor preconditioner may make an iteration invalid or worse. These cases rule out a
universal acceleration reading but do not select a corrected proposition.

Choosing a conventional theorem would therefore invent, narrow, broaden, or substitute
proposition-changing mathematics. There is no canonical Lean expression whose imports can be
minimized, no expression or environment fingerprint, no approved alternate encoding, and no
meaningful removed-hypothesis, changed-domain, changed-binder-scope, or boundary-case mutation. All
four mutation classes are undefined, not passed. No `Statement.lean`, theorem declaration, proof
body, weakened special case, or broadened interface was added. The root remains `[H5, M4, R4]`.

## Source And Lean Boundary

The intake inspected Barrett et al., *Templates for the Solution of Linear Systems*, second
edition, Chapter 3 Section 3.1. The observed Netlib HTML has SHA-256
`006eb59144d9292245c3b0f9a65d7b60b4f08f196220ebbeecb35f66036b83a3`. It describes equivalent
transformed systems, illustrates left preconditioning by `M^-1 A x = M^-1 b`, distinguishes
placement choices, and discusses setup and application costs. The repository does not cite or
adopt this source, its bytes have not been independently admitted here, and it does not say every
preconditioner accelerates every iterative method. It remains a discovery-only specification lead.

The existing `IntakeProbe.lean` imports four adjacent mathlib modules and checks fifteen
inverse-cancellation, matrix-vector, positive-definite, norm, and fixed-point interfaces. Those are
possible ingredients only. The probe defines no preconditioner, selects no iterative method or
convergence comparison, and declares no canonical target. Its four imports cannot be certified
minimal for a target that does not exist.

A bounded exact-topic search over the repo-local, pinned-mathlib, and owned Lean roots matched only
the probe's two explanatory lines and located no source-identical terminal declaration. This is
narrow feasibility evidence, not the downstream anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided canonical `.lake` symlink was
used read-only. No dependency update, build, clone, fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1456` | 0 | rank 1133; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| authority and null-target assertions over the manifest, execution DAG, and `instance.json` | 0 | rank, dependency, intake `[_]`, statement `[ ]`, null canonical claim and target, and H5/M4/R4 agree |
| `git blame -L 10630,10635 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `python3 -B Stage1_Instances/THM-M-1456/check_intake.py` | 1 | historical intake checker expects authoritative intake state `[ ]`, while integration now records provisional `[_]`; this phase records rather than rewrites stale intake evidence |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| mathlib `git rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1456/IntakeProbe.lean` | 0 | fifteen adjacent APIs elaborated; stdout SHA-256 `904accb882716517b08f977449b54da0a2d8561f41b8198ce6b3e2e56b3c2526`; representative axiom reports list only `propext`, `Classical.choice`, and `Quot.sound`; no target declaration |
| `rg -n -i --glob '*.lean' 'precondition(er\|ing)\|condition[ _-]?number\|preconditioned[ _-]?(cg\|conjugate\|gmres\|iteration)' Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib Stage1_Instances/THM-M-1456` | 0 | only two explanatory probe lines matched; output SHA-256 `09bba4d34fa882a1165a5d8d1757e5d5940f4f91c0556185b14f9241097a9848`; no source-identical declaration located |
| prohibited-construct scan over owned Lean files | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |

Final JSON, invariant, whitespace, and absent-self-test checks are recorded in the structured
blocker beside this report.

## Retry Condition

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must admit
an immutable pinpoint source and independently select one exact proposition. That selection must
fix the problem and domain, iterative method and recurrence, preconditioner and placement,
admissibility assumptions, convergence observable and comparator, quantifier order, rate, cost and
arithmetic conventions, stopping and breakdown behavior, ordered binders, conclusion, and every
boundary case.

A fresh statement worker can then encode precisely that reviewed claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This is a truthful blocked statement attempt, not completion of this node or any downstream node.
Lifecycle remains `planned`; `audit_complete: false` and `theorem_complete: false`; no debt-vector
change is proposed. Because the exact-statement deliverable did not pass, no
`.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof credit, or master acceptance
is claimed.
